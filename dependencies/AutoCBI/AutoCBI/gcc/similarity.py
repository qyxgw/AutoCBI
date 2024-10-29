import os, time, sys


gcc_revisions_str = """57303
57341
57488
57521
57719
58223
58418
58570
58640
58662
58696
58726
58759
59221
59594
59747
59715
60452
61140
61306
61383
61517
61518
61578
61681
62151
63551
63605
63659
64041
64682
64756
64853
65318
66186
66272
66375
66863
66894
66952
67121
67456
67786
67828
68194
68250
68990
69951
70138
70586
80622
81740
"""

gcc_revisions = gcc_revisions_str.split("\n")
for gcc_revision in gcc_revisions:
    bugid = gcc_revision.split(",")[0]
    existingcovset = dict()
    failset = set()
    os.chdir('/data01/qiyixian/AutoCBI/gccInfo-r0828/' + bugid + '/fail')
    filenames = os.listdir()
    for filename in filenames:
        if filename == 'stmt_info.txt':
            method_info = open(filename, 'r')
            method_info_line = method_info.readlines()
            for line in method_info_line:
                gccfilename = line.strip().split(':')[0].split('-build/')[1].split(',')[0]
                lines=line.strip().split(':')[1].split(',')
                for j in range(0,len(lines)):
                    if gccfilename.endswith('.h'):
                        break
                    else:
                        failset.add(gccfilename+ ':' + lines[j])
    for j in range(1,2):
        thisset = set()
        os.chdir('/data01/qiyixian/AutoCBI/gccPass-r0828/'+str(j)+'/' + bugid + '/passcov')
        filenames = os.listdir()
        for filename in filenames:
            # print(filename)
            os.chdir('/data01/qiyixian/AutoCBI/gccPass-r0828/'+str(j)+'/' + bugid + '/passcov/'+filename)
            passcovs = os.listdir()
            for passcov in passcovs:
                if passcov == 'stmt_info.txt':
                    method_info = open(passcov, 'r')
                    method_info_line = method_info.readlines()
                    for line in method_info_line:
                        gccfilename = line.strip().split(':')[0].split('-build/')[1].split(',')[0]
                        lines = line.strip().split(':')[1].split(',')
                        for i in range(0,len(lines)):
                            if gccfilename.endswith('.h'):
                                break
                            else:
                                thisset.add(gccfilename + ':' + lines[i])
            similarity = float(len(thisset & failset)/ len(thisset | failset))
            existingcovset[filename] = similarity

    sorted_dict = dict(sorted(existingcovset.items(), key=lambda x: x[1], reverse=True))
    for key in sorted_dict:
        print(bugid+':'+key)
        break

    # for key in existingcovset.keys():
    #
    #     print(similarity)
    #



