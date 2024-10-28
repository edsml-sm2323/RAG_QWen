import os
import config
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 初始化模型
client = ChatOpenAI(
    # 生成文本随机性的参数
    temperature=0.95,
    model="glm-4",
    openai_api_key="119a9ed4b916a6f10a6e5435a5b5f897.qahjRwuAWqVw6Zbv",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)


df = pd.DataFrame(columns=['filename', 'company'])
i = 1
for filename in os.listdir(config.text_files_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(config.text_files_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            template = ChatPromptTemplate.from_template(
                "你是一个能精准提取信息的AI。"
                "我会给你一篇招股说明书，请输出此招股说明书的主体是哪家公司，若无法查询到，则输出无。\n"
                "{t}\n\n"
                "请指出以上招股说明书属于哪家公司，请只输出公司名。"
            )
            chain = template | client
            response = chain.invoke({"t": content[:5000]})
            print(response.content)
            df.at[i, 'filename'] = filename
            df.at[i, 'company'] = response.content
            i += 1
            print(i)
df.to_csv(config.company_save_path)