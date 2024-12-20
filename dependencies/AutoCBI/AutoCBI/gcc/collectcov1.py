import os
from RecBi.util import exccmd
from pathlib import Path

def collect(compilersdir, infodir, bugIds, revisions, wrongoptions):

    for i in range(len(bugIds)):

        wrongoption = wrongoptions[i]
        bugId = bugIds[i]
        revision = revisions[i]

        testname = 'fail'

        covdir = compilersdir + revision + '/' + revision + '-build/gcc'
        srcdir = compilersdir + revision + '/' + revision + '/gcc'
        gccdir = compilersdir + revision + '/' + revision + '-build/bin'
        resdir = infodir + bugId
        

        os.chdir(resdir)

        # if os.path.exists(resdir + '/' + testname):
        #     exccmd('rm -rf ' + resdir + '/' + testname)


        os.system('mkdir ' + resdir + '/' + testname)
        if os.path.exists(resdir + '/' + testname + '/method_info.txt') \
                and os.path.exists(resdir + '/' + testname + '/stmt_info.txt'):
            methodfile = open(resdir + '/' + testname + '/method_info.txt', 'r')
            methodlines = methodfile.readlines()
            methodfile.close()
            stmtfile = open(resdir + '/' + testname + '/stmt_info.txt', 'r')
            stmtlines = stmtfile.readlines()
            stmtfile.close()
            if len(stmtlines) > 0 and len(methodlines) > 0:
                continue

        methodfile = open(resdir + '/' + testname + '/method_info.txt', 'w')
        stmtfile = open(resdir + '/' + testname + '/stmt_info.txt', 'w')
        # delete all .gcda files
        os.system('find ' + covdir + ' -name \"*.gcda\" | xargs rm -f')
        # compile test program
        os.system(gccdir + '/gcc ' + wrongoption + ' ' + testname + '.c')  # change per bug

        if os.path.exists('gcdalist'):
            os.system('rm gcdalist')
        os.system('find ' + srcdir + ' -name \"*.c\" > gcdalist')
        os.system('find ' + srcdir + ' -name \"*.h\" >> gcdalist')

        f = open('gcdalist')
        lines = f.readlines()
        f.close()

        for i in range(len(lines)):
            gcdafile=lines[i].strip().replace(srcdir,covdir)
            # gcdafile=lines[i].strip()
            if '/gcc/testsuite/' in gcdafile:
                continue
            path_tmp = Path(gcdafile)
            if not path_tmp.parent.exists():
                path_tmp.parent.mkdir(parents=True)
            os.system('cp ' + lines[i].strip() + ' ' + lines[i].strip().replace(srcdir, covdir))
            os.system('rm *.gcov')
            if os.path.exists('gcovfile'):
                os.system('rm gcovfile')
            os.system(gccdir+'/gcov -f '+gcdafile+' > gcovfile')
            # input("test")
            if not os.path.exists('./' + gcdafile.strip().split('/')[-1] + '.gcov'):
                continue
            f = open('gcovfile')
            gcovlines = f.readlines()
            f.close()
            for j in range(len(gcovlines)):
                if 'Function \'' in gcovlines[j].strip():
                    if 'Lines executed:' in gcovlines[j + 1].strip() and float(
                            gcovlines[j + 1].strip().split('Lines executed:')[1].split('%')[0].strip()) != 0.0:
                        methodfile.write(gcdafile + ',' + gcovlines[j].strip().split('\'')[1] + ',' +
                                         gcovlines[j + 1].strip().split('Lines executed:')[1].split('%')[
                                             0].strip() + ',' + gcovlines[j + 1].strip().split('of')[-1].strip() + '\n')

            f = open(gcdafile.strip().split('/')[-1] + '.gcov')
            stmtlines = f.readlines()
            f.close()

            tmp = []
            for j in range(len(stmtlines)):
                if stmtlines[j] == '------------------\n':
                    continue
                covcnt = stmtlines[j].strip().split(':')[0].strip()
                linenum = stmtlines[j].strip().split(':')[1].strip()
                if covcnt != '-' and covcnt != '#####':
                    tmp.append(linenum)
            if len(tmp) == 0:
                continue
            stmtfile.write(gcdafile+':'+','.join(tmp)+'\n')
        stmtfile.close()
        methodfile.close()