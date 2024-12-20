import os

gcc_revisions_str = """"""
# gcc_revisions_str = """57303,r198967,-O0,-O1,checkIsPass_wrongcodeOneline,install_no
# 57488,r199531,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 57521,r199601,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 57719,r200388,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 58223,r201915,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 58418,r202556,-m64+-O2,-m32+-O2,checkIsPass_wrongcodeOneline,install_no
# 58570,r203003,-O1,-Os,checkIsPass_wrongcodeOneline,install_no
# 58640,r203223,-O2,-O3,checkIsPass_zeroandsegmentoneline,install_no
# 58662,r203235,-Os,-O2,checkIsPass_wrongcodeOneline,install_no
# 58726,r203511,-O1,-Os,checkIsPass_wrongcodeOneline,install_no
# 59221,r205097,-O1,-O2,checkIsPass_zeroandsegmentoneline,install_no
# 59715,r206387,-O1,-Os,checkIsPass_wrongcodeOneline,install_no
# 59747,r206472,-m64+-O1,-m64+-Os,checkIsPass_wrongcodeOneline,install_no
# 60452,r208366,-O2,-O1,checkIsPass_zeroandsegmentoneline,install_no
# 61140,r210259,-O0,-O1,checkIsPass_wrongcodeOneline,install_no
# 61306,r210888,-O1,-Os,checkIsPass_zeroandsegmentoneline,install_no
# 61383,r211110,-Os,-O2,checkIsPass_zeroandsegmentoneline,install_no
# 61517,r211685-1,-O1,-Os,checkIsPass_zeroandsegmentoneline,install_no
# 61518,r211685-2,-O2,-O3,checkIsPass_zeroandsegmentoneline,install_no
# 61578,r211848,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 61681,r212218-1,-O1,-Os,checkIsPass_wrongcodeOneline,install_no
# 62151,r213937,-Os,-O2,checkIsPass_zeroandsegmentoneline,install_no
# 63551,r216217,-O1,-Os,checkIsPass_zeroandsegmentoneline,install_no
# 63605,r216429,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 63659,r216691,-Os,-O2,checkIsPass_zeroandsegmentoneline,install_no
# 64682,r219832,-Os,-O2,checkIsPass_wrongcodeOneline,install_no
# 64756,r220011,-m64+-O3,-m32+-O3,checkIsPass_zeroandsegmentoneline,install_no
# 64853,r220198,-O1,-Os,checkIsPass_zeroandsegmentoneline,install_no
# 65318,r221192,-O1,-Os,checkIsPass_zeroandonenumber,install_no
# 66272,r223630,-O2,-O3,checkIsPass_zeroandsegmentoneline,install_no
# 66375,r223995,-Os,-O2,checkIsPass_zeroandsegmentoneline,install_no
# 66863,r225727,-O1,-Os,checkIsPass_zeroandsegmentoneline,install_no
# 66894,r225804,-O1,-Os,checkIsPass_zeroandsegmentoneline,install_no
# 66952,r225987,-Os,-O2,checkIsPass_zeroandsegmentoneline,install_no
# 67121,r226592,-O2,-O3,checkIsPass_zeroandsegmentoneline,install_no
# 67456,r227491,-Os,-O2,checkIsPass_wrongcodeOneline,install_no
# 67786,r228291,-Os,-O2,checkIsPass_wrongcodeOneline,install_no
# 67828,r228389,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 68194,r229639,-Os,-O2,checkIsPass_wrongcodeOneline,install_no
# 56478,r196310,x,-O2+-c,install_no
# 58068,r201397,x,-O3+-c,install_no
# 58343,r202308,x,-O1,install_no
# 58451,r202643,x,-O3+-c,install_no
# 58539,r202882,x,-O3+-g+-c,install_no
# 57341,r199099,-O3+-m64,-O3+-m32,checkIsPass_wrongcodeOneline,install_no
# 66186,r223265,-O2,-O3,checkIsPass_zeroandsegmentoneline,install_no
# 68990,r231807,-O2+-w+-m32,-O3+-w+-m32,checkIsPass_onenumberandzero,install_no
# 70138,r234026,-O2,-O3,checkIsPass_zeroandsegmentoneline,install_no
# 70586,r234805,-O1+-w+-m32,-O3+-w+-m32,checkIsPass_zeroandsegmentoneline,install_no
# 71439,r237156,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 80622,r247550,-O0+-m32,-O1+-m32,checkIsPass_wrongcodeOneline,install_no
# 81740,r250895,-O0,-O3,checkIsPass_wrongcodeOneline,install_no
# 82078,r251580,-O0,-O3,checkIsPass_wrongcodeOneline,install_no
# 71518,r237336,-O3+-m32,-O3+-m64,checkIsPass_zeroandsegmentoneline,install_no
# 58759,r203716,-m64+-O2,-m32+-O2,checkIsPass_zeroandsegmentoneline,install_no
# 59594,r206194,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 64041,r217971,-O1,-O3,checkIsPass_onenumberandzero,install_no
# 68250,r229937,-m32+-O3,-m64+-O3,checkIsPass_wrongcodeOneline,install_no
# 58696,r203458,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
# 69951,r233678,-O0,-O1,checkIsPass_zeroandsegmentoneline,install_no
# """
gcc_revisions = gcc_revisions_str.split("\n")
for gcc_revision in gcc_revisions:
    maxnum=0
    gcccount={}
    bugid = gcc_revision.split(",")[0]

    os.chdir('/data01/xxxx/AutoCBI/gccPass-r0828/1/' + bugid + '/passcov')
    maxnum = len(os.listdir())

    os.chdir('/data01/xxxxx/AutoCBI/gccInfo-r0828/' + bugid + '/fail')
    filenames = os.listdir()
    for filename in filenames:
        if filename == 'method_info.txt':
            method_info = open(filename, 'r')
            method_info_line = method_info.readlines()
            for line in method_info_line:
                gccfilename = line.strip().split(':')[0].split('-build/')[1].split(',')[0]
                if gccfilename not in gcccount:
                    gcccount[gccfilename] = 1
                else: gcccount[gccfilename] += 1
    for key in gcccount:
        gcccount[key] = gcccount[key]*maxnum
    gcccountold=gcccount.copy()
    print(gcccountold['gcc/tree-ssa-threadupdate.c'])

    os.chdir('/data01/xxxx/AutoCBI/gccPass-r0828/1/'+bugid+'/passcov')
    filenames = os.listdir()
    for filename in filenames:
        print(filename)
        os.chdir(filename)
        passcovs=os.listdir()
        for passcov in passcovs:
            if passcov == 'method_info.txt':
               method_info=open(passcov,'r')
               method_info_line=method_info.readlines()
               for line in method_info_line:
                   gccfilename=line.strip().split(':')[0].split('-build/')[1].split(',')[0]
                   if gccfilename in gcccount:
                       gcccount[gccfilename]-=1

        os.chdir('/data01/xxxx/AutoCBI/gccPass-r0828/1/'+bugid+'/passcov')
    # for key in gcccount:
    #     if gcccount[key]>=0:
    #        gcccount[key] = gcccount[key]/gcccountold[key]
    #     else:
    #         gcccount[key]=0
    sorted_dict = dict(sorted(gcccount.items(), key=lambda x: x[1], reverse=True))
    # sorted_dict1 = dict(sorted(gcccountold.items(), key=lambda x: x[1], reverse=True))
    # fgcc={}
    # loop=20
    # for key in sorted_dict1:
    #     loop-=1
    #     fgcc[key]=gcccount[key]/gcccountold[key]
    #     if loop<=0 :
    #         break
    print(sorted_dict['gcc/tree-ssa-threadupdate.c'])
    #print(fgcc)
    print(sorted_dict)


