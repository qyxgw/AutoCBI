import os
from pathlib import Path

left_gcc_versions = """57488,r199531,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
57521,r199601,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
57719,r200388,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
58223,r201915,-O2,-O3,checkIsPass_wrongcodeOneline,install_no
58418,r202556,-m64+-O2,-m32+-O2,checkIsPass_wrongcodeOneline,install_no
58570,r203003,-O1,-Os,checkIsPass_wrongcodeOneline,install_no
58640,r203223,-O2,-O3,checkIsPass_zeroandsegmentoneline,install_no
58662,r203235,-Os,-O2,checkIsPass_wrongcodeOneline,install_no
58726,r203511,-O1,-Os,checkIsPass_wrongcodeOneline,install_no
59221,r205097,-O1,-O2,checkIsPass_zeroandsegmentoneline,install_no
59715,r206387,-O1,-Os,checkIsPass_wrongcodeOneline,install_no
59747,r206472,-m64+-O1,-m64+-Os,checkIsPass_wrongcodeOneline,install_no
60452,r208366,-O2,-O1,checkIsPass_zeroandsegmentoneline,install_no
61140,r210259,-O0,-O1,checkIsPass_wrongcodeOneline,install_no
61306,r210888,-O1,-Os,checkIsPass_zeroandsegmentoneline,install_no
61383,r211110,-Os,-O2,checkIsPass_zeroandsegmentoneline,install_no
61517,r211685-1,-O1,-Os,checkIsPass_zeroandsegmentoneline,install_no"""

left_gcc_list = left_gcc_versions.split("\n")

def zip():
    zip_dir = "/Users/xxxxx/Postgraduate/AutoCBI/compilers/gcc/"

    version_ids = []
    cmd = "zip -q ./leftgcc_2.zip"

    for gcc in left_gcc_list:
        version_id = gcc.split(",")[1]
        print(version_id)
        cmd += " " + zip_dir + version_id + ".zip"

    print(cmd)
    os.system(cmd)

def unzip():
    os.chdir("/data/compilers/gcc/")
    for gcc_line in left_gcc_list:
        rvision_id = gcc_line.split(",")[1]
        os.system("rm -rf ./{}".format(rvision_id))
        if not Path(rvision_id).exists():
            os.system("unzip {}.zip".format(rvision_id))
        else:
            continue

unzip()
# zip()

