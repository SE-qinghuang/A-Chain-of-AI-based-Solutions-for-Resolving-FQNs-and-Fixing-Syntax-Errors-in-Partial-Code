#coding=utf-8
#coding=utf-8
import pandas as pd

# # 读取csv文件
# df = pd.read_csv('Content_representation.csv')
# # 填充空值
# df = df.fillna("True")
#
# accuracy = df["ERROR_For_Code_Fix"].value_counts(normalize=True).loc["True"]
# # 打印df["ERROR_For_Code_Fix"]列中true的个数
# df["ERROR_For_Code_Fix"] = df["ERROR_For_Code_Fix"].apply(lambda x: True if x == "True" else False)
# print(df["ERROR_For_Code_Fix"].sum())
# print("Content_representation accuracy: ", accuracy)

# 读取csv文件
df = pd.read_csv('Content_representation_change_example.csv')
# 填充空值
df = df.fillna("True")

accuracy = df["ERROR_For_Code_Fix"].value_counts(normalize=True).loc["True"]
# 打印df["ERROR_For_Code_Fix"]列中true的个数
df["ERROR_For_Code_Fix"] = df["ERROR_For_Code_Fix"].apply(lambda x: True if x == "True" else False)
print(df["ERROR_For_Code_Fix"].sum())
print("Content_representation change_example accuracy: ", accuracy)

# 读取csv文件
df = pd.read_csv('Content_representation_change_example_again.csv')
# 填充空值
df = df.fillna("True")
accuracy = df["ERROR_For_Code_Fix"].value_counts(normalize=True).loc["True"]

# 打印df["ERROR_For_Code_Fix"]列中true的个数
df["ERROR_For_Code_Fix"] = df["ERROR_For_Code_Fix"].apply(lambda x: True if x == "True" else False)
print(df["ERROR_For_Code_Fix"].sum())
print("Content_representation change_example_again accuracy: ", accuracy)

# 读取csv文件
df = pd.read_csv('E:\All_Project\PCR-Extension\Experiment\RQ2\PCR-Chain\Java\AI_Chain_example_change.csv')
# 填充空值
df = df.fillna("True")
accuracy = df["ERROR_For_Code_Fix"].value_counts(normalize=True).loc["True"]

# 打印df["ERROR_For_Code_Fix"]列中true的个数
df["ERROR_For_Code_Fix"] = df["ERROR_For_Code_Fix"].apply(lambda x: True if x == "True" else False)
print(df["ERROR_For_Code_Fix"].sum())
print("AI_Chain accuracy: ", accuracy)