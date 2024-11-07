import os

gcc_revisions_str = """"""

gcc_revisions = gcc_revisions_str.split("\n")
for gcc_revision in gcc_revisions:
    maxnum=0
    cfs={}
    cps = {}
    result={}
    bugid = gcc_revision.split(",")[0]

    # os.chdir('/data01/xxxxx/AutoCBI/gccPass-r/1/' + bugid + '/passcov')
    # maxnum = len(os.listdir())

    os.chdir('/data/AutoCBI/llvm/llvmInfo/' + bugid + '/fail')
    filenames = os.listdir()
    for filename in filenames:
        if filename == 'method_info.txt':
            method_info = open(filename, 'r')
            method_info_line = method_info.readlines()
            for line in method_info_line:
                gccfilename = line.strip().split(',')[0].split('.gcda')[0]
                if gccfilename.endswith('.h'):
                    continue
                if gccfilename not in cfs:
                    cfs[gccfilename] = 1
                    cps[gccfilename] = 0
                else: cfs[gccfilename] += 1
    # for key in gcccount:
    #     gcccount[key] = gcccount[key]*maxnum
    gcccountold=cfs.copy()

    for j in range(1,2):
        os.chdir('/data/AutoCBI/llvm/passdir/'+str(j)+'/' + bugid + '/passcov')
        filenames = os.listdir()
        for filename in filenames:
            # print(filename)
            os.chdir('/data/AutoCBI/llvm/passdir/'+str(j)+'/' + bugid + '/passcov/'+filename)
            passcovs = os.listdir()
            for passcov in passcovs:
                if passcov == 'method_info.txt':
                    method_info = open(passcov, 'r')
                    method_info_line = method_info.readlines()
                    for line in method_info_line:
                        #print(str(j) + ": " + line)
                        # print(line)
                        gccfilename =line.strip().split(',')[0].split('.gcda')[0]
                        if gccfilename.endswith('.h'):
                            continue
                        if gccfilename in cps:
                            cps[gccfilename] += 1
                        else: cps[gccfilename] = 1


            os.chdir('/data/AutoCBI/llvm/passdir/'+str(j)+'/' + bugid + '/passcov')
    dstar2={}
    for key in cfs:
        dstar2[key]= float(cfs[key]**2 / (cfs[key] + cps[key]))







    # for key in gcccount:
    #     if gcccount[key]>=0:
    #        gcccount[key] = gcccount[key]/gcccountold[key]
    #     else:
    #         gcccount[key]=0
    sorted_dict = dict(sorted(dstar2.items(), key=lambda x: x[1], reverse=True))
    # sorted_dict1 = dict(sorted(gcccountold.items(), key=lambda x: x[1], reverse=True))
    # fgcc={}
    # loop=20
    # for key in sorted_dict1:
    #     loop-=1
    #     fgcc[key]=gcccount[key]/gcccountold[key]
    #     if loop<=0 :
    #         break
    #print(sorted_dict['gcc/tree-ssa-pre.c'])
    #print(fgcc)

    #print('[result - end]')
    #print('[unexecutedfile - start]')
    f=open('/data/AutoCBI/dstar2/rankFile_'+bugid+'.txt','a')
    loop=50
    for key in sorted_dict:
        loop-=1
        f.write(key.split('CMakeFiles')[0]+key.split('.dir/')[1] + '\n')
        if loop<=0 :
            break
    loop=50
    for key in sorted_dict:
        loop -= 1
        f.write(key+'\n')
        if loop <= 0:
            break

        #print(key)
    #print('[unexecutedfile - end]' + '\n')



