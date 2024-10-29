from AutoCBI.llvm import *
from AutoCBI.util import metrics
from configparser import ConfigParser

from dependencies.AutoCBI.AutoCBI.llvm.rank import rank_

cfg = ConfigParser()
cfg.read('config/config.ini')
configFile = cfg.get('llvm-locations', 'configFile')
bugList = cfg.get('llvm-locations', 'bugList')
compilersdir = cfg.get('llvm-locations', 'compilersdir')
infodir = cfg.get('llvm-locations', 'infodir')

revisions = []
bugIds = []
rights = []
wrongs = []
checkpasses = []

revfile = open(bugList)
revlines = revfile.readlines()
revfile.close()

for i in range(len(revlines)):
    bugIds.append(revlines[i].strip().split(',')[0])
    revisions.append(revlines[i].strip().split(',')[1])
    rights.append(revlines[i].strip().split(',')[2])
    wrongs.append(revlines[i].strip().split(',')[3])
    checkpasses.append(revlines[i].strip().split(',')[4])

reduced = cfg.get('llvm-rev', 'reduced').split(',')
#print(reduced)

bugIds = list(set(bugIds) - set(reduced))

mode = cfg.get('mode', 'mode')
if mode != 'verification' and mode != 'utilization':
    raise Exception('Unknown mode... Please check config.ini and correct it.')

for i in range(len(bugIds)):
    bugId = [bugIds[i]]
    revision = [revisions[i]]
    right = [rights[i]]
    wrong = [wrongs[i]]
    checkpass = [checkpasses[i]]
    os.chdir("/data/AutoCBI/dependencies/AutoCBI")
    cfg.set('gcc-locations', 'rankFile', "/data/AutoCBI/llvmbugs/rankFile" + "_" + str(bugIds[i]) + ".txt")
    f = open('/data/AutoCBI/dependencies/AutoCBI/config/config.ini', 'w')
    cfg.write(f)
    f.close()
    os.system("find /dev/shm/ -name \"*\" | xargs rm -rf \"*\"")
    print('\033[1;35m Begin batchrun\033[0m')
    batchrun(bugId, revision, right, wrong, checkpass, configFile)
    print('\033[1;35m Begin delete\033[0m')
    delete(configFile)
    print('\033[1;35m mode::utilization\033[0m')
    print('\033[1;35m Begin rank_\033[0m')
    rank_(revision, bugId, configFile)
    rankFile = cfg.get('gcc-locations', 'rankFile')
    print('\033[1;35m Ranking list has been recorded in ', rankFile, '\033[0m')

