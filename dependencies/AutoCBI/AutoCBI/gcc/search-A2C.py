#experimental environment
#torch version 1.4.0
#python version 3.7.3
import os, time, sys
from random import choice, random
from failmessage_gcc_12_30 import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import *
from configparser import ConfigParser
from pathlib import Path

def exccmd(cmd):
    p=os.popen(cmd,"r")
    rs=[]
    line=""
    while True:
         line=p.readline()
         if not line:
              break
         #print line
         #rs.append(line.strip())
    return rs
def collectCov(testname):
    print("begin")
    os.system('mkdir -p ' + passdir + '/passcov/' + testname)
    print("end")
    methodfile=open(passdir+'/passcov/'+testname+'/method_info.txt','w')
    stmtfile=open(passdir+'/passcov/'+testname+'/stmt_info.txt','w')

    if os.path.exists('gcdalist'): # all files to be collected
        os.system('rm gcdalist')
    os.system('find '+srcdir+' -name \"*.c\" > gcdalist')
    os.system('find '+srcdir+' -name \"*.h\" >> gcdalist')

    f=open('gcdalist')
    lines=f.readlines()
    f.close()

    for i in range(len(lines)):
        gcdafile=lines[i].strip().replace(srcdir,covdir)
        if '/gcc/testsuite/' in gcdafile:
            continue
        path_tmp = Path(gcdafile)
        if not path_tmp.parent.exists():
            path_tmp.parent.mkdir(parents=True)
        os.system('cp '+lines[i].strip()+' '+gcdafile)
        os.system('rm *.gcov')
        if os.path.exists('gcovfile'):
            os.system('rm gcovfile')
        os.system(gcovpath+' -f '+gcdafile+' > gcovfile')
        if not os.path.exists('./'+gcdafile.strip().split('/')[-1]+'.gcov'):
            continue

        f=open('gcovfile')
        gcovlines=f.readlines()
        f.close()

        for j in range(len(gcovlines)):
            if 'Function \'' in gcovlines[j].strip():
                if 'Lines executed:' in gcovlines[j+1].strip() and float(gcovlines[j+1].strip().split('Lines executed:')[1].split('%')[0].strip())!=0.0:
                    methodfile.write(gcdafile+','+gcovlines[j].strip().split('\'')[1]+','+gcovlines[j+1].strip().split('Lines executed:')[1].split('%')[0].strip()+','+gcovlines[j+1].strip().split('of')[-1].strip()+'\n')

        f=open(gcdafile.strip().split('/')[-1]+'.gcov')
        stmtlines=f.readlines()
        f.close()

        tmp=[]
        for j in range(len(stmtlines)):
            # print(stmtlines[j])
            if ":" not in stmtlines[j]:
                continue
            covcnt=stmtlines[j].strip().split(':')[0].strip()
            linenum=stmtlines[j].strip().split(':')[1].strip()
            if covcnt!='-' and covcnt!='#####':
                tmp.append(linenum)
        if len(tmp)==0:
            continue
        stmtfile.write(gcdafile+':'+','.join(tmp)+'\n')
    stmtfile.close()
    methodfile.close()
def diffWithExistingCov(testname):
    if len(os.listdir(passdir+'/passcov'))==1:
        thisfile=open(passdir+'/passcov/'+testname+'/stmt_info.txt')
        thislines=thisfile.readlines()
        thisfile.close()

        thisset=set()
        for i in range(len(thislines)):
            filenameitem=thislines[i].strip().split(':')[0]
            lineitems=thislines[i].strip().split(':')[1].split(',')
            for j in range(len(lineitems)):
                thisset.add(filenameitem+':'+lineitems[j])
        existingcovset[testname]=thisset&failset
        return 0 # different

    thisfile=open(passdir+'/passcov/'+testname+'/stmt_info.txt')
    thislines=thisfile.readlines()
    thisfile.close()

    thisset=set()
    for i in range(len(thislines)):
        filenameitem=thislines[i].strip().split(':')[0]
        lineitems=thislines[i].strip().split(':')[1].split(',')
        for j in range(len(lineitems)):
            thisset.add(filenameitem+':'+lineitems[j])

    for key in existingcovset.keys():
        similarity=float(len(existingcovset[key]&(thisset&failset)))/len(existingcovset[key]|(thisset&failset))
        # print similarity
        # sys.exit()
        if similarity==1:
            # existingcovset[testname]=thisset&failset
            return 1 # same
    existingcovset[testname]=thisset&failset
    return 0 #different


def selectMutationStrategy():
    mutationStrategy=random.randint(1,132);
    # fistroundSelected=choice(firstRoundStrategy)
    if mutationStrategy>=1 and mutationStrategy<=6:
        secondRoundSelected=mutationStrategy
        commandMutate=secondRoundforQualifier(secondRoundSelected)
    elif mutationStrategy>=7 and mutationStrategy<=14:
        secondRoundSelected=mutationStrategy-6
        commandMutate=secondRoundforModifier(secondRoundSelected)
    elif mutationStrategy>=15 and mutationStrategy<=102:
        secondRoundSelected=mutationStrategy-14
        commandMutate=secondRoundforBinaryOp(secondRoundSelected)
    elif mutationStrategy>=103 and mutationStrategy<=127:
        secondRoundSelected=mutationStrategy-102
        commandMutate=secondRoundforUnaryOp(secondRoundSelected)
    elif mutationStrategy>=128 and mutationStrategy<=131:
        secondRoundSelected=mutationStrategy-127
        commandMutate=secondRoundforConstant(secondRoundSelected)
    else:
        commandMutate=secondRoundforVariable()
    return (commandMutate,mutationStrategy)


def diffWithExistingPass(passtestdir):
    if os.path.exists('difffilefail'):
        exccmd('rm difffilefail')
    if os.path.exists(failtestdir + '/fail.c'):
        exccmd('diff mainvar.c ' + failtestdir + '/fail.c' + ' >difffilefail')
    else:
        exccmd('diff mainvar.c ' + failtestdir + 'ori' + '/fail.c' + ' >difffilefail')
    difffail = open('difffilefail')
    difffaillines = difffail.readlines()
    difffail.close()
    if len(difffaillines) == 0:
        return 0  # exist
    for i in range(len(difffaillines)):
        if 'printf' in difffaillines[i]:
            return 0  # faking passing

    for f in os.listdir(passtestdir):
        if os.path.exists('difffile'):
            exccmd('rm difffile')
        exccmd('diff mainvar.c ' + passtestdir + '/' + f + ' >difffile')
        difff = open('difffile')
        diffflines = difff.readlines()
        difff.close()
        if len(diffflines) == 0:
            return 0  # exist

    return 1




def findIndex(tmplist,element):
    for i in range(len(tmplist)):
        if tmplist[i][0]==element:
            return (i,tmplist[i][1])
    return (-1,-1)





def updateScore(tmplist,index2,testname,succval,totalval):
    e1=tmplist[index2][0]
    e2=tmplist[index2][1]

    if len(os.listdir(passdir+'/passcov'))==1:
        tmplist[index2]=(e1,1.0)
        return tmplist

    diversitysum=0.0
    existingnum=0
    thistestset=set()

    for key in existingcovset.keys():
        if key==testname:
            continue
        diversitysum+=(1-(float(len(existingcovset[key]&existingcovset[testname])))/float(len(existingcovset[key]|existingcovset[testname])))
        existingnum+=1

    newe2=(diversitysum/existingnum)*(succval/totalval)
    tmplist[index2]=(e1,newe2)
    return tmplist

def updateScore2(tmplist,index2,testname,succval,totalval):
    e1=tmplist[index2][0]
    e2=tmplist[index2][1]

    if len(os.listdir(passdir+'/passcov'))==1:
        tmplist[index2]=(e1,1.0)
        return tmplist

    diversitysum=0.0
    existingnum=0
    thistestset=set()

    stmtcov=open(passdir+'/passcov/'+testname+'/stmt_info.txt')
    stmtlines=stmtcov.readlines()
    stmtcov.close()

    for i in range(len(stmtlines)):
        filename=stmtlines[i].strip().split(':')[0]
        stmtlist=stmtlines[i].strip().split(':')[1].split(',')
        for j in range(len(stmtlist)):
            thistestset.add(filename+':'+stmtlist[j])

    for f in os.listdir(resdir+'/passcov'):
        if f!=testname:
            passset=set()
            stmtcov=open(resdir+'/passcov/'+f+'/stmt_info.txt')
            stmtlines=stmtcov.readlines()
            stmtcov.close()

            for i in range(len(stmtlines)):
                filename=stmtlines[i].strip().split(':')[0]
                stmtlist=stmtlines[i].strip().split(':')[1].split(',')

                for j in range(len(stmtlist)):
                    passset.add(filename+':'+stmtlist[j])
            diversitysum+=(1-(float(len(passset&thistestset&failset)))/float(len((passset&failset)|(thistestset&failset))))
            existingnum+=1

    newe2=(diversitysum/existingnum)*(succval/totalval)
    tmplist[index2]=(e1,newe2)
    return tmplist
def secondRoundforQualifier(secondRoundSelected):
    if secondRoundSelected == 1:
        return 'addQualifier;volatile'
    elif secondRoundSelected == 2:
        return 'addQualifier;const'
    elif secondRoundSelected == 3:
        return 'addQualifier;restrict'
    elif secondRoundSelected == 4:
        return 'remModifierQualifier;volatile'
    elif secondRoundSelected == 5:
        return 'remModifierQualifier;const'
    else:
        return 'remModifierQualifier;restrict'


def secondRoundforModifier(secondRoundSelected):
    if secondRoundSelected == 1:
        return 'addRepModifier;unsigned'
    elif secondRoundSelected == 2:
        return 'addRepModifier;signed'
    elif secondRoundSelected == 3:
        return 'addRepModifier;short'
    elif secondRoundSelected == 4:
        return 'addRepModifier;long'
    elif secondRoundSelected == 5:
        return 'remModifierQualifier;unsigned'
    elif secondRoundSelected == 6:
        return 'remModifierQualifier;signed'
    elif secondRoundSelected == 7:
        return 'remModifierQualifier;short'
    else:
        return 'remModifierQualifier;long'


def secondRoundforBinaryOp(secondRoundSelected):
    if secondRoundSelected == 1:
        return 'repBinaryOp;+,-'
    elif secondRoundSelected == 2:
        return 'repBinaryOp;+,*'
    elif secondRoundSelected == 3:
        return 'repBinaryOp;+,/'
    elif secondRoundSelected == 4:
        return 'repBinaryOp;+,%'

    elif secondRoundSelected == 5:
        return 'repBinaryOp;-,+'
    elif secondRoundSelected == 6:
        return 'repBinaryOp;-,*'
    elif secondRoundSelected == 7:
        return 'repBinaryOp;-,/'
    elif secondRoundSelected == 8:
        return 'repBinaryOp;-,%'

    elif secondRoundSelected == 9:
        return 'repBinaryOp;*,+'
    elif secondRoundSelected == 10:
        return 'repBinaryOp;*,-'
    elif secondRoundSelected == 11:
        return 'repBinaryOp;*,/'
    elif secondRoundSelected == 12:
        return 'repBinaryOp;*,%'

    elif secondRoundSelected == 13:
        return 'repBinaryOp;/,+'
    elif secondRoundSelected == 14:
        return 'repBinaryOp;/,-'
    elif secondRoundSelected == 15:
        return 'repBinaryOp;/,*'
    elif secondRoundSelected == 16:
        return 'repBinaryOp;/,%'

    elif secondRoundSelected == 17:
        return 'repBinaryOp;%,+'
    elif secondRoundSelected == 18:
        return 'repBinaryOp;%,-'
    elif secondRoundSelected == 19:
        return 'repBinaryOp;%,*'
    elif secondRoundSelected == 20:
        return 'repBinaryOp;%,/'

    elif secondRoundSelected == 21:
        return 'repBinaryOp;>,>='
    elif secondRoundSelected == 22:
        return 'repBinaryOp;>,<'
    elif secondRoundSelected == 23:
        return 'repBinaryOp;>,<='
    elif secondRoundSelected == 24:
        return 'repBinaryOp;>,=='
    elif secondRoundSelected == 25:
        return 'repBinaryOp;>,!='

    elif secondRoundSelected == 26:
        return 'repBinaryOp;>=,>'
    elif secondRoundSelected == 27:
        return 'repBinaryOp;>=,<'
    elif secondRoundSelected == 28:
        return 'repBinaryOp;>=,<='
    elif secondRoundSelected == 29:
        return 'repBinaryOp;>=,=='
    elif secondRoundSelected == 30:
        return 'repBinaryOp;>=,!='

    elif secondRoundSelected == 31:
        return 'repBinaryOp;<,>'
    elif secondRoundSelected == 32:
        return 'repBinaryOp;<,>='
    elif secondRoundSelected == 33:
        return 'repBinaryOp;<,<='
    elif secondRoundSelected == 34:
        return 'repBinaryOp;<,=='
    elif secondRoundSelected == 35:
        return 'repBinaryOp;<,!='

    elif secondRoundSelected == 36:
        return 'repBinaryOp;<=,>'
    elif secondRoundSelected == 37:
        return 'repBinaryOp;<=,>='
    elif secondRoundSelected == 38:
        return 'repBinaryOp;<=,<'
    elif secondRoundSelected == 39:
        return 'repBinaryOp;<=,=='
    elif secondRoundSelected == 40:
        return 'repBinaryOp;<=,!='

    elif secondRoundSelected == 41:
        return 'repBinaryOp;==,>'
    elif secondRoundSelected == 42:
        return 'repBinaryOp;==,>='
    elif secondRoundSelected == 43:
        return 'repBinaryOp;==,<'
    elif secondRoundSelected == 44:
        return 'repBinaryOp;==,<='
    elif secondRoundSelected == 45:
        return 'repBinaryOp;==,!='

    elif secondRoundSelected == 46:
        return 'repBinaryOp;!=,>'
    elif secondRoundSelected == 47:
        return 'repBinaryOp;!=,>='
    elif secondRoundSelected == 48:
        return 'repBinaryOp;!=,<'
    elif secondRoundSelected == 49:
        return 'repBinaryOp;!=,<='
    elif secondRoundSelected == 50:
        return 'repBinaryOp;!=,=='

    elif secondRoundSelected == 51:
        return 'repBinaryOp;&,^'
    elif secondRoundSelected == 52:
        return 'repBinaryOp;&,|'

    elif secondRoundSelected == 53:
        return 'repBinaryOp;|,^'
    elif secondRoundSelected == 54:
        return 'repBinaryOp;|,&'

    elif secondRoundSelected == 55:
        return 'repBinaryOp;^,&'
    elif secondRoundSelected == 56:
        return 'repBinaryOp;^,|'

    elif secondRoundSelected == 57:
        return 'repBinaryOp;<<,>>'

    elif secondRoundSelected == 58:
        return 'repBinaryOp;>>,<<'

    elif secondRoundSelected == 59:
        return 'repBinaryOp;&&,||'

    elif secondRoundSelected == 60:
        return 'repBinaryOp;||,&&'

    elif secondRoundSelected == 61:
        return 'repBinaryOp;+=,-='
    elif secondRoundSelected == 62:
        return 'repBinaryOp;+=,*='
    elif secondRoundSelected == 63:
        return 'repBinaryOp;+=,/='
    elif secondRoundSelected == 64:
        return 'repBinaryOp;+=,%='

    elif secondRoundSelected == 65:
        return 'repBinaryOp;-=,+='
    elif secondRoundSelected == 66:
        return 'repBinaryOp;-=,*='
    elif secondRoundSelected == 67:
        return 'repBinaryOp;-=,/='
    elif secondRoundSelected == 68:
        return 'repBinaryOp;-=,%='

    elif secondRoundSelected == 69:
        return 'repBinaryOp;*=,+='
    elif secondRoundSelected == 70:
        return 'repBinaryOp;*=,-='
    elif secondRoundSelected == 71:
        return 'repBinaryOp;*=,/='
    elif secondRoundSelected == 72:
        return 'repBinaryOp;*=,%='

    elif secondRoundSelected == 73:
        return 'repBinaryOp;/=,+='
    elif secondRoundSelected == 74:
        return 'repBinaryOp;/=,-='
    elif secondRoundSelected == 75:
        return 'repBinaryOp;/=,*='
    elif secondRoundSelected == 76:
        return 'repBinaryOp;/=,%='

    elif secondRoundSelected == 77:
        return 'repBinaryOp;%=,+='
    elif secondRoundSelected == 78:
        return 'repBinaryOp;%=,-='
    elif secondRoundSelected == 79:
        return 'repBinaryOp;%=,*='
    elif secondRoundSelected == 80:
        return 'repBinaryOp;%=,/='

    elif secondRoundSelected == 81:
        return 'repBinaryOp;<<=,>>='

    elif secondRoundSelected == 82:
        return 'repBinaryOp;>>=,<<='

    elif secondRoundSelected == 83:
        return 'repBinaryOp;&=,^='
    elif secondRoundSelected == 84:
        return 'repBinaryOp;&=,|='

    elif secondRoundSelected == 85:
        return 'repBinaryOp;|=,^='
    elif secondRoundSelected == 86:
        return 'repBinaryOp;|=,&='

    elif secondRoundSelected == 87:
        return 'repBinaryOp;^=,&='
    else:
        return 'repBinaryOp;^=,|='


def secondRoundforUnaryOp(secondRoundSelected):
    if secondRoundSelected == 1:
        return 'repRemUnaryOp;pre++,pre--'
    elif secondRoundSelected == 2:
        return 'repRemUnaryOp;pre++,post++'
    elif secondRoundSelected == 3:
        return 'repRemUnaryOp;pre++,post--'
    elif secondRoundSelected == 4:
        return 'repRemUnaryOp;pre++,~'
    elif secondRoundSelected == 5:
        return 'repRemUnaryOp;pre++,delete'

    elif secondRoundSelected == 6:
        return 'repRemUnaryOp;pre--,pre++'
    elif secondRoundSelected == 7:
        return 'repRemUnaryOp;pre--,post++'
    elif secondRoundSelected == 8:
        return 'repRemUnaryOp;pre--,post--'
    elif secondRoundSelected == 9:
        return 'repRemUnaryOp;pre--,~'
    elif secondRoundSelected == 10:
        return 'repRemUnaryOp;pre--,delete'

    elif secondRoundSelected == 11:
        return 'repRemUnaryOp;post++,pre++'
    elif secondRoundSelected == 12:
        return 'repRemUnaryOp;post++,pre--'
    elif secondRoundSelected == 13:
        return 'repRemUnaryOp;post++,post--'
    elif secondRoundSelected == 14:
        return 'repRemUnaryOp;post++,~'
    elif secondRoundSelected == 15:
        return 'repRemUnaryOp;post++,delete'

    elif secondRoundSelected == 16:
        return 'repRemUnaryOp;post--,pre++'
    elif secondRoundSelected == 17:
        return 'repRemUnaryOp;post--,pre--'
    elif secondRoundSelected == 18:
        return 'repRemUnaryOp;post--,post++'
    elif secondRoundSelected == 19:
        return 'repRemUnaryOp;post--,~'
    elif secondRoundSelected == 20:
        return 'repRemUnaryOp;post--,delete'

    elif secondRoundSelected == 21:
        return 'repRemUnaryOp;~,pre++'
    elif secondRoundSelected == 22:
        return 'repRemUnaryOp;~,pre--'
    elif secondRoundSelected == 23:
        return 'repRemUnaryOp;~,post++'
    elif secondRoundSelected == 24:
        return 'repRemUnaryOp;~,post--'
    else:
        return 'repRemUnaryOp;~,delete'


def secondRoundforConstant(secondRoundSelected):
    if secondRoundSelected == 1:
        return 'repIntConstant;+1'
    elif secondRoundSelected == 2:
        return 'repIntConstant;-1'
    elif secondRoundSelected == 3:
        return 'repIntConstant;*-1'
    else:
        return 'repIntConstant;*0'


def secondRoundforVariable():
    return 'repVarSameScope;'

# --------------------------------------- main process begin---------------------------------------
os.environ["OMP_NUM_THREADS"] = "1"
revisionnumber = sys.argv[1]
compilationOptionsRight = sys.argv[2].replace('+', ' ')
compilationOptionsWrong = sys.argv[3].replace('+', ' ')
checkpass = sys.argv[4]
roundcount = sys.argv[5]
configFile = sys.argv[6]
bugId = sys.argv[7]
cfg = ConfigParser()
cfg.read(configFile)
# password = cfg.get('password', 'password')
# autosudo = 'echo ' + password + ' | sudo -S '
GAMMA = cfg.getfloat('params', 'gamma')
compilersdir = cfg.get('gcc-locations', 'compilersdir') + revisionnumber + '/' + revisionnumber
passdir = cfg.get('gcc-locations', 'passdir') + roundcount + '/' + bugId
infodir = cfg.get('gcc-locations', 'infodir') + bugId

if os.path.exists(passdir):
    os.system('rm -rf ' + passdir)
os.system('mkdir -p ' + passdir)
os.chdir(passdir)
gccpath = compilersdir + '-build/bin/gcc'
gcovpath = compilersdir + '-build/bin/gcov'
covdir = compilersdir + '-build/gcc'
srcdir = compilersdir + '/gcc'

mutatedir = cfg.get('gcc-locations', 'mutatedir')
os.system('cp -r ' + mutatedir + '* .')

if os.path.exists(passdir + '/failtest'):
    os.system('rm -rf ' + passdir + '/failtest')
os.system('mkdir -p ' + passdir + '/failtest')
os.system('cp ' + infodir + '/fail.c ' + passdir + '/failtest')
os.system('mkdir -p ' + passdir + '/passcov')
failtestdir = './failtest'
firstfailtestdir = './firstfailtest'
os.system('mkdir -p ' + firstfailtestdir)
passtestdir = './passtest'
os.system('mkdir -p ' + passtestdir)

mutateRecord = open('mutateRecode', 'w')
successRecord = open('successRecord', 'w')

os.system('cp ' + failtestdir + '/fail.c ' + './')
if os.path.exists('a.out'):
    os.system('rm a.out')
os.system(gccpath + ' ' + compilationOptionsWrong + ' fail.c')
if os.path.exists('oriwrongfile'):
    os.system('rm oriwrongfile')
if not os.path.exists('a.out'):
    sys.exit(1)
# os.system('./a.out 2>&1 | tee oriwrongfile')
os.system('{ timeout 10 ./a.out ; } >oriwrongfile 2>&1')
# print 'start'
failcovpath = cfg.get('gcc-locations', 'infodir')
if os.path.exists(failcovpath + bugId + '/failcov/stmt_info.txt'):
    tarpath = failcovpath + bugId + '/failcov/stmt_info.txt'
elif os.path.exists(failcovpath + bugId + '/fail/stmt_info.txt'):
    tarpath = failcovpath + bugId + '/fail/stmt_info.txt'
else:
    print ("Error!!")
    sys.exit(1)
failfile = open(tarpath)
faillines = failfile.readlines()
failfile.close()
failset = set()
for i in range(len(faillines)):
    filename = faillines[i].strip().split(':')[0].split('-build/')[1]
    stmtlist = faillines[i].strip().split(':')[1].split(',')
    for j in range(len(stmtlist)):
        failset.add(filename + ':' + stmtlist[j])
#initialization
mutationlist=[]
successratelist=dict()
for i in range(1,132+1):
    mutationlist.append((i,0.0)) # mutationNO and metric value; index is ranking
    successratelist[i]=(0.0,0.0) # success and total
(commandMutate,mutationNo)=selectMutationStrategy()

cnt=0
firstfailcnt=0
existingcovset=dict()
failtype='fail'
os.system('mkdir '+failtestdir+'ori')




# set the maximum number of witness test programs to 499(of course, it is impossible to
# produce so many programs in only one hour)
starttime = time.time()
while (cnt < 500):
    endtime = time.time()
    gaptime = endtime - starttime
    if gaptime > 3600: # set the time limit to one hour
        if len(os.listdir(passtestdir)) > 0:
            break
        else:
            starttime = time.time()
            os.system('mv ' + failtestdir + '/* ' + failtestdir + 'ori')
            if len(os.listdir(firstfailtestdir)) == 0:
                break
            os.system('mv ' + firstfailtestdir + '/* ' + failtestdir)
            failtype = 'firstfail'

    doesGeneratePassingTestProgram = False
    ############## select seed program
    # averageTimesForLoopToGenerateOnePass += 1
    mutatefile = ''
    # failtype=choice(passorfail)
    if failtype == 'fail':
        mutatefile = failtestdir + '/fail.c'
    elif failtype == 'firstfail':
        if len(os.listdir(passtestdir)) > 0:
            break
        # if len(os.listdir(failtestdir))==0:
        #     continue
        tmpfile = choice(os.listdir(failtestdir))
        mutatefile = failtestdir + '/' + tmpfile
    # else:
    #     if len(os.listdir(passtestdir))==0:
    #         continue
    #     tmpfile=choice(os.listdir(passtestdir))
    #     mutatefile=passtestdir+'/'+tmpfile
        ############## determine k1

    (k1, v1) = findIndex(mutationlist, mutationNo)
    if k1 == -1:
        print('BUG!!!')
        break
        ############## determie k2

    commandMutate = ''
    mutationNo = -1
    k2 = -1
    while (1):
        (commandMutate, mutationNo) = selectMutationStrategy()
        (k2, v2) = findIndex(mutationlist, mutationNo)
        if v1 == v2:
            diffk2k1 = 0
        else:
            diffk2k1 = k2 - k1

        if diffk2k1 <= 0:
            break
        elif random.random() < (1 - 0.023) ** diffk2k1:  # p can be changed
            break
    newtotalvalue = successratelist[mutationNo][1] + 1
    successratelist[mutationNo] = (successratelist[mutationNo][0], newtotalvalue)

    classfile = commandMutate.strip().split(';')[0]
    inputslist = commandMutate.strip().split(';')[1].split(',')
    for i in range(len(inputslist)):
        inputslist[i] = '\"' + inputslist[i] + '\"'
    inputsstr = ' '.join(inputslist)
    ############## mutate program
    os.system('rm *.c')
    os.system('cp ' + mutatefile + ' ./main.c')
    mutateRecord.write(mutatefile + ';' + commandMutate + ';' + str(mutationNo) + '\n')
    mutateRecord.flush()
    if os.path.exists('mainvar.c'):
        os.system('rm mainvar.c')
    os.system('./' + classfile + ' main.c -- ' + inputsstr)  # mutate to generate new test program
    if os.path.exists('difftmp'):
        os.system('rm difftmp')
    os.system('diff main.c mainvar.c > difftmp')
    f = open('difftmp')
    difflines = f.readlines()
    f.close()
    if len(difflines) == 0:
        mutationlist[k2] = (
        mutationlist[k2][0], mutationlist[k2][1] * (successratelist[mutationNo][0] / successratelist[mutationNo][1]))
        mutationlist = sorted(mutationlist, key=lambda x: x[1], reverse=True)
        continue
    else:
        if os.path.exists('bugmessage'):
            os.system('rm bugmessage')
        # os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
        # os.system(gccpath+' '+compilationOptions+' mainvar.c 2>&1 | tee bugmessage')
        flagIsPass = -1
        if checkpass == 'checkIsPass_wrongcodeOneline':
            flagIsPass = checkIsPass_wrongcodeOneline(configFile, revisionnumber, compilationOptionsRight,
                                                                             compilationOptionsWrong)  # 1:pass; 2:still fail
        elif checkpass == 'checkIsPass_zeroandsegmentoneline':
            flagIsPass = checkIsPass_zeroandsegmentoneline(configFile, revisionnumber, compilationOptionsRight,
                                                                                  compilationOptionsWrong)  # 1:pass; 2:still fail
        elif checkpass == 'checkIsPass_onenumberandzero':
            flagIsPass = checkIsPass_onenumberandzero(configFile, revisionnumber, compilationOptionsRight,
                                                                                compilationOptionsWrong)  # 1:pass; 2:still fail
        else:
            raise Exception('unkown checkpass')

        if flagIsPass == 0:
            mutationlist[k2] = (mutationlist[k2][0],
                                mutationlist[k2][1] * (successratelist[mutationNo][0] / successratelist[mutationNo][1]))
            mutationlist = sorted(mutationlist, key=lambda x: x[1], reverse=True)
            continue
        elif flagIsPass == 2:
            mutationlist[k2] = (mutationlist[k2][0],
                                mutationlist[k2][1] * (successratelist[mutationNo][0] / successratelist[mutationNo][1]))
            mutationlist = sorted(mutationlist, key=lambda x: x[1], reverse=True)
            firstfailcnt += 1
            # if len(os.listdir(firstfailtestdir))==5000:
            #     os.system('rm -rf '+firstfailtestdir+'/'+choice(os.listdir(firstfailtestdir)))
            os.system('mv mainvar.c ' + firstfailtestdir + '/firstfail_' + classfile + str(mutationNo) + '_' + str(
                firstfailcnt) + '.c')
            continue
        else:
            flagIsExist = diffWithExistingPass(passtestdir)
            if flagIsExist == 0:
                mutationlist[k2] = (mutationlist[k2][0], mutationlist[k2][1] * (
                            successratelist[mutationNo][0] / successratelist[mutationNo][1]))
                mutationlist = sorted(mutationlist, key=lambda x: x[1], reverse=True)
                continue
            else:
                cnt += 1
                collectCov('pass_' + classfile + str(mutationNo) + '_' + str(cnt))
                flagCovIsRepetitive = diffWithExistingCov('pass_' + classfile + str(mutationNo) + '_' + str(cnt))
                if flagCovIsRepetitive == 1:
                    exccmd('rm -rf ' + passdir + '/passcov/' + 'pass_' + classfile + str(mutationNo) + '_' + str(cnt))
                    mutationlist[k2] = (mutationlist[k2][0], mutationlist[k2][1] * (
                                successratelist[mutationNo][0] / successratelist[mutationNo][1]))
                    mutationlist = sorted(mutationlist, key=lambda x: x[1], reverse=True)
                    cnt -= 1
                    continue
                else:
                    exccmd(
                        'mv mainvar.c ' + passtestdir + '/pass_' + classfile + str(mutationNo) + '_' + str(cnt) + '.c')
                    successRecord.write(mutatefile + ';' + commandMutate + ';' + str(mutationNo) + '\n')
                    successRecord.flush()
                    ############## update for next iteration
                    newtotalvalue = successratelist[mutationNo][0] + 1
                    successratelist[mutationNo] = (newtotalvalue, successratelist[mutationNo][1])
                    mutationlist = updateScore(mutationlist, k2, 'pass_' + classfile + str(mutationNo) + '_' + str(cnt),
                                               successratelist[mutationNo][0],
                                               successratelist[mutationNo][1])  # mutationlist[k2]
                    mutationlist = sorted(mutationlist, key=lambda x: x[1], reverse=True)
                    # starttime=time.time()





successRecord.close()
mutateRecord.close()


