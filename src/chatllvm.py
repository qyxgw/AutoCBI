import requests
import json
import time
import os

# API key
api_key = "sk-xxxxxxx"
# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"
# OpenAI API URL
url = 'https://xxxxxxx'


headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}


messages = [
    {"role": "system", "content": "You are a compiler bug detection expert."}
]

requests.adapters.DEFAULT_RETRIES = 5
def send_message(user_input):

    messages.append({"role": "user", "content": user_input})


    data = {
        "model": "gpt-4o",
        "messages": messages

    }


    response = requests.post(url, headers=headers, data=json.dumps(data))


    if response.status_code == 200:
        reply = response.json()
        assistant_message = reply['choices'][0]['message']['content']


        messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message
    else:
        return f"Error: {response.status_code}"


gcc = open('src/llvm.txt', 'r').read() #Document Summary
gcc1 = open('src/llvm1.txt', 'r').read()#Document Summary
gcc2 = open('src/llvm2.txt', 'r',encoding='utf-8').read()#Document Summary
prompt0 = "The functional description between [llvm-star] and [llvm-end] is related to the source code files of llvm. I will give you these contents in three parts.Learn the functions of these files and complete the following tasks based on the functions of these files."
assistant_reply = send_message("Forget about previous memories")
print(f"Assistant: {assistant_reply}")
assistant_reply = send_message(prompt0)
print(f"Assistant: {assistant_reply}")
assistant_reply = send_message(gcc)

assistant_reply = send_message(gcc1)

assistant_reply = send_message(gcc2)



llvm_revisions_str = """26256,4e971da2723972b589f617301b7c838f00c8e2c7,-Os,-O2,checkIsPass_zeroandonenumber,install_yes"""



llvm_revisions = llvm_revisions_str.split("\n")
for llvm_revision in llvm_revisions:
    bugid = llvm_revision.split(",")[0]
    filesourse = open('xxxxx/xxxx/' + bugid + '/small_' + bugid + '.c',
                      'r').read()  # Source code of the failing test program
    output = open('xxxx/xxxx/' + bugid + '/version_' + bugid,
                  'r').read()  # Compilation outputs under different compilation configurations
    rankfile = open('xxxx/xxxx/' + bugid + '/rankFile_' + bugid + '.txt',
                    'r').read()  # Suspicious file list generated by traditional SBFL

    cov = open('xxxx/xxxx/rankFile_' + bugid + '.txt',
               'r').read()  # Suspicious file list generated by finer-grained execution coverage

    prompt2 = "[source code-start]" + filesourse + "[source code-end]" + "[rankfile-start]" + rankfile + "[rankfile-end]" + "[result-start]" + output + "[result-end]"+ "[executedfile-start]" + cov + "[executedfile-end]"
    # prompt2 = "[source code-start]" + small + "[source code-end]" + "[rankfile-start]" + rankfile + "[rankfile-end]" + "[result-start]" + version + "[result-end]"
    # prompt21="[source code-start]" + small + "[source code-end]"
    # prompt22="[rankfile-start]" + rankfile + "[rankfile-end]"
    # prompt23="[result-start]" + version + "[result-end]"
    # prompt24="[cov-start]" + cov + "[cov-end]"
    prompt1 = (
        "The intermediate between [source code-start] and [source code-end] refers to the source code that triggers a compiler bug."
        "The intermediate between [rankfile-start] and [rankfile-end] refers to the ranking of suspicious files with compiler bugs. The higher the ranking, the greater the possibility of bugs."
        "The intermediate between [result-start] and [result-end] refers to the result of the code running under different optimization options."
        "The files between [executed file start] and [executed file end] are compiler files that are frequently executed by test cases that trigger compiler bugs.The higher the ranking, the higher the execution frequency.")
    # prompt3 = ("Reorder these suspicious files between [rankfile-start] and [rankfile-end]"
    #            " according to the functional description of the corresponding llvm source code, code features of the source code between [source code-start] and [source code-end] , the list of the executed files and the result of the source code running under different optimization options."
    #            "According to the degree of suspicion of the defect, 0 represents the lowest degree of suspicion, and 10 represents the highest degree of suspicion.Assign a score to each file between [rankfile-start] and [rankfile-end], add the score to the end of each line. The file will be sorted in descending order according to the score.You just need to return me a reordered list of results and "
    #            "The format of the results is as follows:"
    #            "FileName1"
    #            "FileName2"
    #            ".......")
    prompt3 = ("Reorder these suspicious files between [rankfile-start] and [rankfile-end]"
           " Select these three types of information as needed, including the functional description of the corresponding LLVM source code, the code characteristics of the source code between [source code-start] and [source code-end], the list of executable files, and the results of running the source code under different optimization options."
           "According to the degree of suspicion of the defect, 0 represents the lowest degree of suspicion, and 10 represents the highest degree of suspicion.Assign a score to each file between [rankfile-start] and [rankfile-end], add the score to the end of each line. The file will be sorted in descending order according to the score.You just need to return me a reordered list of results and "
           "The format of the results is as follows:"
           "FileName1"
           "FileName2"
           ".......")

    # prompt1 = (
    #     "The intermediate between [source code-start] and [source code-end] refers to the source code that triggers a compiler bug."
    #     "The intermediate between [rankfile-start] and [rankfile-end] refers to the ranking of suspicious files with compiler bugs. The higher the ranking, the greater the possibility of bugs."
    #     "The intermediate between [result-start] and [result-end] refers to the result of the code running under different optimization options.")
    #
    # prompt3 = ("Reorder these suspicious files between [rankfile-start] and [rankfile-end]"
    #            " according to the functional description of the corresponding llvm source code, code features of the source code between [source code-start] and [source code-end] ,and the result of the source code running under different optimization options."
    #            "According to the degree of suspicion of the defect, 0 represents the lowest degree of suspicion, and 10 represents the highest degree of suspicion.Assign a score to each file between [rankfile-start] and [rankfile-end], add the score to the end of each line. The file will be sorted in descending order according to the score.You just need to return me a reordered list of results and "
    #            "The format of the results is as follows:"
    #            "FileName1"
    #            "FileName2"
    #            ".......")

    assistant_reply = send_message(prompt1)

    assistant_reply = send_message(prompt2)
    # assistant_reply = send_message(prompt22)
    # assistant_reply = send_message(prompt23)
    # assistant_reply = send_message(prompt24)

    assistant_reply = send_message(prompt3)  # The List of Suspicious Files
    f = open('xxxx/xxx/rankFile_' + bugid + '.txt', 'a')
    f.write(assistant_reply)
    f.close()
    print(bugid+'success')



