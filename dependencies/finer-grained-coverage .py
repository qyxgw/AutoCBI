import os

gcc_revisions_str = """23751
24356
24482
24516
24757
24763
24801
25154
25225
25629
25831
25900
26256
26266
26323
26628
26734
27137
27624
28307
28610
28763
28802
28824
29170
30707
30841
30935
32418
32419
33078
33119
33185
33305
34354
38641
"""

gcc_revisions = gcc_revisions_str.split("\n")
for gcc_revision in gcc_revisions:
    maxnum=0
    gcccount={}
    result={}
    bugid = gcc_revision.split(",")[0]

    # os.chdir('/data01/qiyixian/AutoCBI/gccPass-r/1/' + bugid + '/passcov')
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
                if gccfilename not in gcccount:
                    gcccount[gccfilename] = 1
                else: gcccount[gccfilename] += 1
    # for key in gcccount:
    #     gcccount[key] = gcccount[key]*maxnum
    gcccountold=gcccount.copy()
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
                        gccfilename = line.strip().split(',')[0].split('.gcda')[0]
                        if gccfilename.endswith('.h'):
                            continue
                        if gccfilename in gcccount:
                            gcccount[gccfilename] -= 1
            sorted_dict = dict(sorted(gcccount.items(), key=lambda x: x[1], reverse=True))
            loop = 20
            for key in sorted_dict:
                loop -= 1
                if key not in result:
                    result[key] = 1
                else:
                    result[key] += 1
                if loop <= 0:
                    break
            gcccount = gcccountold.copy()
            os.chdir('/data/AutoCBI/llvm/passdir/'+str(j)+'/' + bugid + '/passcov')



    # for key in gcccount:
    #     if gcccount[key]>=0:
    #        gcccount[key] = gcccount[key]/gcccountold[key]
    #     else:
    #         gcccount[key]=0
    sorted_dict = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
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
    f=open('/data/AutoCBI/wang/rankFile_'+bugid+'.txt','a')
    loop=20
    for key in sorted_dict:
        loop-=1
        print(key)
        f.write(key + '\n')
        if loop<=0 :
            break


        #print(key)
    #print('[unexecutedfile - end]' + '\n')



