import os
from pathlib import Path

gcc_bugs_dir = "../dependencies/AutoCBI/benchmark/llvmbugs/{id}/locations"
res_files = "/data/AutoCBI/xxxxx"


def parse_locations_file(path: Path):
    lines = path.open("r").readlines()
    for line in lines:
        if line.startswith("file:"):
            content = line[5:].split(";")[0].split("/")[-1]
            return content

res_files_path = Path(res_files)
res = {}
for file in res_files_path.iterdir():
    if file.is_file() and "rankFile" in str(file):
        bugid = str(file).split("/")[-1].split("rankFile_")[1].split(".txt")[0]
        buggy_file_name = parse_locations_file(Path(gcc_bugs_dir.format(id=bugid)))
        lines = file.open("r").readlines()
        for i, line in enumerate(lines):
            # file_name, score = line.split("")
            file_name=line
            if buggy_file_name in file_name:
                if i + 1 not in res.keys():
                    res[i + 1] = 1
                else:
                    res[i + 1] += 1
print(res)                  
res_format ={1: 0, 5: 0, 10: 0, 20: 0, 50: 0, 100: 0}

for key in res.keys():
    final_keyset = sorted(res_format.keys())
    for key2 in final_keyset:
        if key <= key2:
            res_format[key2] += res[key]
print(res_format)