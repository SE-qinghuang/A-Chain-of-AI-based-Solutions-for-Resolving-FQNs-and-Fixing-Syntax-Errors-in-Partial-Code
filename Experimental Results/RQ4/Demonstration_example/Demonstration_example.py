#coding=utf-8
import openai
import pandas as pd
import tqdm as tqdm
import random
import sys
import os
import subprocess
sys.path.append('E:\All_Project\PCR-Chain\Experiment\RQ2\PCR-Chain\Java')
from FQN_implement import FQN_Supplement
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import chardet
import numpy as np

# 加载预训练的 BERT 模型
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

java_dataset = "E:\All_Project\PCR-Extension\Experiment\dataset\Java_SO_Dataset.csv"

result_path = "Demonstration_example_dont_reverse.csv"

simplenameExtraction = "Prompt_For_Java_Simplename_Extraction.txt"

simplename2FQN = "Prompt_For_Java_Simplename_to_FQN.txt"

Error_Message_Enhance = "Prompt_For_Java_Error_Message_Enhance.txt"

code_fix = "Prompt_For_Java_Code_Fix.txt"

with open('E:\All_Project\PCR-Chain\Experiment\key.txt', 'r', encoding='utf-8') as openai_keys:
    openai_keys = openai_keys.readlines()
    for i in range(len(openai_keys)):
        openai_keys[i] = openai_keys[i].strip()

def chatgpt(prompt):
    response = None
    while response is None:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["</Fixed Code>", "</FQNs>", "</Simple names>", "</Error Message Explanation>"]
            )
        except Exception as e:
            print(type(e), e)
            if str(type(e)) == "<class 'openai.error.InvalidRequestError'>":
                response = "null"
            openai.api_key = openai_keys[random.randint(0, len(openai_keys) - 1)]

    return (response['choices'][0]['message']['content'])

def compile_code(code, filename):
    java_file_path = filename
    with open(java_file_path, "w") as f:
        f.write(code)
    command = f"javac -cp E:/so/so/* -J-Duser.language=en {java_file_path}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    error_output = result.stderr.decode('utf-8')
    # subprocess.run(command, shell=True, check=True)  # 使用check参数捕获编译错误
    # 删除生成的java文件
    os.remove(java_file_path)
    if error_output:
        return error_output
    else:
        # 获取当前目录名
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(current_dir):
            if filename.endswith('.java') or filename.endswith('.class'):
                file_path = os.path.join(current_dir, filename)
                os.remove(file_path)
        return "True"

# 读取数据集
df = pd.read_csv(java_dataset, encoding='utf-8')

# 填充nan
df = df.fillna("True")

# 打开DE.csv文件
df_DE = pd.read_csv("DE.csv", encoding='utf-8')
df_DE = df_DE.fillna("")
code_list = df_DE["code"].tolist()
simplenames_list = df_DE["simplenames"].tolist()
FQNs_list = df_DE["FQNs"].tolist()
error_message_list = df_DE["Error_message"].tolist()[:2]
error_message_enhance_list = df_DE["Error_message_enhance"].tolist()[:2]
fixed_code_list = df_DE["Fixed_code"].tolist()[:2]

# 使用 BERT 模型将关键字向量化，这步耗时较长，所以将向量保存到磁盘上
code_embeddings = model.encode(code_list)
simplenames_embeddings = model.encode(simplenames_list)
# FQNs_embeddings = model.encode(FQNs_list)
error_message_embeddings = model.encode(error_message_list)
error_message_enhance_embeddings = model.encode(error_message_enhance_list)

promptTemplate_for_Simplename_Extraction = open(simplenameExtraction, 'r', encoding='gbk').read()
promptTemplate_for_Simplename_to_FQN = open(simplename2FQN, 'r', encoding='gbk').read()
promptTemplate_for_Error_Message_Enhance = open(Error_Message_Enhance, 'r', encoding='gbk').read()
promptTemplate_for_Code_Fix = open(code_fix, 'r', encoding='gbk').read()

for index, row in tqdm.tqdm(df.iterrows()):
    # if row["ERROR_For_With_import"] == "True":
    #     continue
    code_embedding_in_csv = model.encode([row["without_import"]])[0]
    # 计算每个关键字和查询关键字之间的余弦相似度
    similarity_scores = cosine_similarity(code_embedding_in_csv.reshape(1, -1), code_embeddings)[0]

    # 升序排序相似度分数
    sorted_scores = np.argsort(similarity_scores)
    # 降序排序相似度分数
    # de_scores = similarity_scores.argsort()[::-1]

    for idx, score in enumerate(sorted_scores, 1):
        if idx == 1:
            print(f'{{{{code{idx}}}}}')
            prompt_for_Simplename_Extraction = promptTemplate_for_Simplename_Extraction.replace(f'{{{{code{idx}}}}}', code_list[score])
            prompt_for_Simplename_Extraction = prompt_for_Simplename_Extraction.replace(f'{{{{simplenames{idx}}}}}',
                                                                                                simplenames_list[score])
        else:
            prompt_for_Simplename_Extraction = prompt_for_Simplename_Extraction.replace(f'{{{{code{idx}}}}}', code_list[score])
            prompt_for_Simplename_Extraction = prompt_for_Simplename_Extraction.replace(f'{{{{simplenames{idx}}}}}',
                                                                                                simplenames_list[score])
    prompt_for_Simplename_Extraction = prompt_for_Simplename_Extraction.replace('{{code}}', row["without_import"])
    simplenames = chatgpt(prompt_for_Simplename_Extraction)
    # 附加在csv文件后面
    df.loc[index, 'simplenames'] = simplenames
    simplenames_embedding_in_csv = model.encode([simplenames])[0]
    # 计算每个关键字和查询关键字之间的余弦相似度
    similarity_scores = cosine_similarity(simplenames_embedding_in_csv.reshape(1, -1), simplenames_embeddings)[0]

    # 降序排序相似度分数
    sorted_scores = similarity_scores.argsort()[::-1]
    for idx, score in enumerate(sorted_scores, 1):
        if idx == 1:
            prompt_for_Simplename_to_FQN = promptTemplate_for_Simplename_to_FQN.replace(f'{{{{code{idx}}}}}', code_list[score])
            prompt_for_Simplename_to_FQN = prompt_for_Simplename_to_FQN.replace(f'{{{{simplenames{idx}}}}}',
                                                                                                simplenames_list[score])
            prompt_for_Simplename_to_FQN = prompt_for_Simplename_to_FQN.replace(f'{{{{fqns{idx}}}}}',
                                                                                FQNs_list[score])
        else:
            prompt_for_Simplename_to_FQN = prompt_for_Simplename_to_FQN.replace(f'{{{{code{idx}}}}}', code_list[score])
            prompt_for_Simplename_to_FQN = prompt_for_Simplename_to_FQN.replace(f'{{{{simplenames{idx}}}}}',
                                                                                                simplenames_list[score])
            prompt_for_Simplename_to_FQN = prompt_for_Simplename_to_FQN.replace(f'{{{{fqns{idx}}}}}',
                                                                                FQNs_list[score])
    prompt_for_Simplename_to_FQN = prompt_for_Simplename_to_FQN.replace('{{code}}', row["without_import"])
    prompt_for_Simplename_to_FQN = prompt_for_Simplename_to_FQN.replace('{{simplenames}}', simplenames)
    FQNs = chatgpt(prompt_for_Simplename_to_FQN)
    # 附加在csv文件后面
    df.loc[index, 'FQNs'] = FQNs
    with_import = FQN_Supplement(row["without_import"], FQNs)
    # 附加在csv文件后面
    df.loc[index, 'with_import'] = with_import
    Error_Message = compile_code(with_import, row["filename"])
    # 附加在csv文件后面
    if Error_Message == "True":
        df.loc[index, 'ERROR_For_With_import'] = "True"
        continue
    else:
        df.loc[index, 'ERROR_For_With_import'] = Error_Message
        error_message_embeddings_in_csv = model.encode([Error_Message])[0]
        # 计算每个关键字和查询关键字之间的余弦相似度
        similarity_scores = cosine_similarity(error_message_embeddings_in_csv.reshape(1, -1), error_message_embeddings)[0]
        # 降序排序相似度分数
        sorted_scores = similarity_scores.argsort()[::-1]
        for idx, score in enumerate(sorted_scores[:2], 1):
            if idx == 1:
                prompt_for_Error_Message_Enhance = promptTemplate_for_Error_Message_Enhance.replace(f'{{{{code{idx}}}}}', code_list[score])
                prompt_for_Error_Message_Enhance = prompt_for_Error_Message_Enhance.replace(f'{{{{error_message{idx}}}}}',
                                                                                                    error_message_list[score])
                prompt_for_Error_Message_Enhance = prompt_for_Error_Message_Enhance.replace(
                    f'{{{{error_message_explanation{idx}}}}}', error_message_enhance_list[score])
            else:
                prompt_for_Error_Message_Enhance = prompt_for_Error_Message_Enhance.replace(f'{{{{code{idx}}}}}', code_list[score])
                prompt_for_Error_Message_Enhance = prompt_for_Error_Message_Enhance.replace(
                    f'{{{{error_message{idx}}}}}',
                    error_message_list[score])
                prompt_for_Error_Message_Enhance = prompt_for_Error_Message_Enhance.replace(
                    f'{{{{error_message_explanation{idx}}}}}', error_message_enhance_list[score])
    prompt_for_Error_Message_Enhance = prompt_for_Error_Message_Enhance.replace('{{code}}', with_import)
    prompt_for_Error_Message_Enhance = prompt_for_Error_Message_Enhance.replace('{{error message}}', Error_Message)
    ERROR_MESSAGE_EXPLANATION = chatgpt(prompt_for_Error_Message_Enhance)
    # 附加在csv文件后面
    df.loc[index, 'ERROR_MESSAGE_EXPLANATION'] = ERROR_MESSAGE_EXPLANATION

    for idx, score in enumerate(sorted_scores[:2], 1):
        if idx == 1:
            prompt_for_Code_Fix = promptTemplate_for_Code_Fix.replace(f'{{{{code{idx}}}}}',
                                                                                                code_list[score])
            prompt_for_Code_Fix = prompt_for_Code_Fix.replace(f'{{{{error_message_explanation{idx}}}}}',
                                                                                        error_message_enhance_list[score])
            prompt_for_Code_Fix = prompt_for_Code_Fix.replace(
                f'{{{{fixed_code{idx}}}}}', fixed_code_list[score])
        else:
            prompt_for_Code_Fix = prompt_for_Code_Fix.replace(f'{{{{code{idx}}}}}',
                                                                      code_list[score])
            prompt_for_Code_Fix = prompt_for_Code_Fix.replace(f'{{{{error_message_explanation{idx}}}}}',
                                                              error_message_enhance_list[score])
            prompt_for_Code_Fix = prompt_for_Code_Fix.replace(
                f'{{{{fixed_code{idx}}}}}', fixed_code_list[score])

    prompt_for_Code_Fix = prompt_for_Code_Fix.replace('{{code}}', with_import)
    prompt_for_Code_Fix = prompt_for_Code_Fix.replace('{{error_message_explanation}}', ERROR_MESSAGE_EXPLANATION)
    Code_Fix = chatgpt(prompt_for_Code_Fix)
    # 附加在csv文件后面
    df.loc[index, 'Code_Fix'] = Code_Fix
    # 再次编译
    Error_Message = compile_code(Code_Fix, row["filename"])
    # 附加在csv文件后面
    if Error_Message == "True":
        df.loc[index, 'ERROR_For_Code_Fix'] = "True"
        continue
    else:
        df.loc[index, 'ERROR_For_Code_Fix'] = Error_Message
    # 保存到csv文件
    df.to_csv(result_path, index=False, encoding='utf-8')
# 统计ERROR_For_Code_Fix列中True的个数, 并计算准确率
accuracy = df["ERROR_For_Code_Fix"].value_counts(normalize=True).loc["True"]
print("accuracy: ", accuracy)