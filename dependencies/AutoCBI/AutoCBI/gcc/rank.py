import os,sys,math
from configparser import ConfigParser

def rank(revisions, bugIds, configFile):

    cfg = ConfigParser()
    cfg.read(configFile)
    loops = cfg.getint('params', 'loops')
    infodir = cfg.get('gcc-locations', 'infodir')
    passdir = cfg.get('gcc-locations', 'passdir')
    bugList = cfg.get('gcc-locations', 'bugList')
    rankFile = cfg.get('gcc-locations', 'rankFile')
    resultFile = cfg.get('gcc-locations', 'resultFile')

    ranks_list = []
    scores_list = []

    for loop in range(1, loops+1):

        # revisions = []
        # bugIds = []
        # revfile = open(bugList)
        # revlines = revfile.readlines()
        # revfile.close()
        #
        # for i in range(len(revlines)):
        #     revisions.append(revlines[i].strip().split(',')[1])
        #     bugIds.append(revlines[i].strip().split(',')[0])

        passdir_tmp = passdir + str(loop)

        resultFile2 = resultFile.split('.csv')[0] + str(loop) + '.csv'
        result = open(resultFile2,'w')

        for i in range(len(revisions)):
            rev = revisions[i]
            bugId = bugIds[i]
            result.write(rev+ '  bug' + bugId + ':\n')
            locationfile = open(infodir+'/'+bugId+'/locations')
            locationlines = locationfile.readlines()
            locationfile.close()
            buggyfiles = set()

            for i in range(len(locationlines)):
                if 'file' in locationlines[i].strip() and 'method' in locationlines[i].strip():
                    buggyfile = locationlines[i].strip().split(';')[0].strip().split(':')[1].strip().split('trunk/')[-1]
                    buggyfiles.add(buggyfile)

            if os.path.exists(infodir+'/'+bugId+'/failcov/stmt_info.txt'):
                tarpath=infodir+'/'+bugId+'/failcov/stmt_info.txt'
            elif os.path.exists(infodir+'/'+bugId+'/fail/stmt_info.txt'):
                tarpath=infodir+'/'+bugId+'/fail/stmt_info.txt'
            else:
                print ("Error!!")
                sys.exit(1)

            failfile = open(tarpath)
            faillines = failfile.readlines()
            failfile.close()

            failstmt = dict()
            passstmt = dict()
            failfileset = set()
            failfilemapstmt = dict()
            for i in range(len(faillines)):
                # print faillines[i]
                filename = faillines[i].strip().split(':')[0].split('-build/')[1]
                if not filename.endswith('.c'):
                    continue
                failfileset.add(filename)
                stmtlist = faillines[i].strip().split(':')[1].split(',')
                failfilemapstmt[filename] = set(stmtlist)
                for stmt in stmtlist:
                    failstmt[filename + ',' + stmt] = 1
                    passstmt[filename + ',' + stmt] = 0

            for i in os.listdir(passdir_tmp + '/' + bugId + '/passcov'):
                passfile = open(passdir_tmp + '/' + bugId + '/passcov/' + i + '/stmt_info.txt')
                passlines = passfile.readlines()
                passfile.close()
                for j in range(len(passlines)):
                    filename = passlines[j].strip().split(':')[0].split('-build/')[1]
                    if not filename.endswith('.c'):  # consider c and h files
                        continue
                    if filename not in failfileset:
                        continue
                    stmtlist = passlines[j].strip().split(':')[1].split(',')
                    for stmt in set(stmtlist) & failfilemapstmt[filename]:
                        # if filename+','+stmt in failstmt.keys():
                        passstmt[filename + ',' + stmt] += 1

            score = dict()
            filescore = dict()
            for key in failstmt.keys():
                score[key] = float(failstmt[key]) / math.sqrt(
                    float(failstmt[key]) * (failstmt[key] + passstmt[key]))
                # if passstmt[key]==0:
                #   score[key]=1.0
                # else:
                #   score[key]=float(failstmt[key])/passstmt[key]

                keyfile = key.split(',')[0]
                if keyfile not in filescore.keys():
                    filescore[keyfile] = []
                    filescore[keyfile].append(score[key])
                else:
                    filescore[keyfile].append(score[key])

            fileaggstmtscore = dict()
            for key in filescore.keys():
                fileaggstmtscore[key] = float(sum(filescore[key])) / len(filescore[key])
            scorelist = sorted(fileaggstmtscore.items(), key=lambda d: d[1], reverse=True)
            scores_list.append(scorelist)



            for bf in buggyfiles:
                tmp = []
                for i in range(len(scorelist)):
                    if fileaggstmtscore[bf] == scorelist[i][1]:
                        tmp.append(i)
                result.write(
                    bf + ',' + str(min(tmp) + 1) + ',' + str(max(tmp) + 1) + ',' + str(fileaggstmtscore[bf]) + '\n')
                ranks_list.append(max(tmp) + 1)
            result.write('\n')
            result.flush()
        result.close()

    idx = ranks_list.index(min(ranks_list))
    scorelist = scores_list[idx]
    f = open(rankFile, 'w')
    for score in scorelist:
        file = score[0]
        value = score[1]
        if 'CMakeFiles' in file:
            files = file.split('/')
            files2 = '/'
            for i in range(len(files)):
                if files[i] != 'CMakeFiles' and not '.dir' in files[i] and files[i] != '':
                    files2 += files[i]
                    files2 += '/'
            file = files2[:-1]
        f.write(file + ',' + str(value) + '\n')
    f.close()


def rank_(revisions, bugIds, configFile):
    cfg = ConfigParser()
    cfg.read(configFile)
    loops = cfg.getint('params', 'loops')
    infodir = cfg.get('gcc-locations', 'infodir')
    passdir = cfg.get('gcc-locations', 'passdir')
    rankFile = cfg.get('gcc-locations', 'rankFile')
    finalrank = {}

    for loop in range(1, loops + 1):

        # revisions = []
        # bugIds = []
        # revfile = open(bugList)
        # revlines = revfile.readlines()
        # revfile.close()
        #
        # for i in range(len(revlines)):
        #     revisions.append(revlines[i].strip().split(',')[1])
        #     bugIds.append(revlines[i].strip().split(',')[0])

        passdir_tmp = passdir + str(loop)


        for i in range(len(revisions)):
            rev = revisions[i]
            print(rev)
            bugId = bugIds[i]
            locationfile = open(infodir + '/' + bugId + '/locations')
            locationlines = locationfile.readlines()
            locationfile.close()
            buggyfiles = set()

            for i in range(len(locationlines)):
                if 'file' in locationlines[i].strip() and 'method' in locationlines[i].strip():
                    buggyfile = locationlines[i].strip().split(';')[0].strip().split(':')[1].strip().split('trunk/')[-1]
                    buggyfiles.add(buggyfile)

            if os.path.exists(infodir + '/' + bugId + '/failcov/stmt_info.txt'):
                tarpath = infodir + '/' + bugId + '/failcov/stmt_info.txt'
            elif os.path.exists(infodir + '/' + bugId + '/fail/stmt_info.txt'):
                tarpath = infodir + '/' + bugId + '/fail/stmt_info.txt'
            else:
                print("Error!!")
                sys.exit(1)

            failfile = open(tarpath)
            faillines = failfile.readlines()
            failfile.close()

            failstmt = dict()
            passstmt = dict()
            failfileset = set()
            failfilemapstmt = dict()
            for i in range(len(faillines)):
                # print faillines[i]
                filename = faillines[i].strip().split(':')[0].split('-build/')[1]
                if not filename.endswith('.c'):
                    continue
                failfileset.add(filename)
                stmtlist = faillines[i].strip().split(':')[1].split(',')
                failfilemapstmt[filename] = set(stmtlist)
                for stmt in stmtlist:
                    failstmt[filename + ',' + stmt] = 1
                    passstmt[filename + ',' + stmt] = 0

            print(passdir_tmp)
            for i in os.listdir(passdir_tmp + '/' + bugId + '/passcov'):
                passfile = open(passdir_tmp + '/' + bugId + '/passcov/' + i + '/stmt_info.txt')
                passlines = passfile.readlines()
                passfile.close()
                for j in range(len(passlines)):
                    filename = passlines[j].strip().split(':')[0].split('-build/')[1]
                    if not filename.endswith('.c'):  # consider c and h files
                        continue
                    if filename not in failfileset:
                        continue
                    stmtlist = passlines[j].strip().split(':')[1].split(',')
                    for stmt in set(stmtlist) & failfilemapstmt[filename]:
                        # if filename+','+stmt in failstmt.keys():
                        passstmt[filename + ',' + stmt] += 1

            score = dict()
            filescore = dict()
            for key in failstmt.keys():
                score[key] = float(failstmt[key]) / math.sqrt(
                    float(failstmt[key]) * (failstmt[key] + passstmt[key]))
                # if passstmt[key]==0:
                #   score[key]=1.0
                # else:
                #   score[key]=float(failstmt[key])/passstmt[key]

                keyfile = key.split(',')[0]
                if keyfile not in filescore.keys():
                    filescore[keyfile] = []
                    filescore[keyfile].append(score[key])
                else:
                    filescore[keyfile].append(score[key])

            fileaggstmtscore = dict()
            for key in filescore.keys():
                fileaggstmtscore[key] = float(sum(filescore[key])) / len(filescore[key])

            if finalrank == {}:
                finalrank = fileaggstmtscore
            else:
                for key in fileaggstmtscore.keys():
                    finalrank[key] += fileaggstmtscore[key]

    scorelist = sorted(finalrank.items(), key=lambda d: d[1], reverse=True)

    f = open(rankFile, 'w')
    for score in scorelist:
        file = score[0]
        value = score[1]
        if 'CMakeFiles' in file:
            files = file.split('/')
            files2 = '/'
            for i in range(len(files)):
                if files[i] != 'CMakeFiles' and not '.dir' in files[i] and files[i] != '':
                    files2 += files[i]
                    files2 += '/'
            file = files2[:-1]
        f.write(file + ',' + str(value) + '\n')
    f.close()