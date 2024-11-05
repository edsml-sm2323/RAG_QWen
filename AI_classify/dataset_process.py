from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import re
from llm_filter import LLM_filter

class AIfilter:
    def __init__(self, file_path, ipc, title, abstract, ipc_list, keywords_list, model_path=None, local=False, key=None, model_name=None):
        # 文件路径 文件中ipc那一列的列名 title的列名 abstract的列名
        self.file_path = file_path
        self.ipc = ipc
        self.title = title
        self.abstract = abstract

        # 之后用于过滤数据的IPC number以及Keywords
        self.IPC = ipc_list
        self.Keywords = keywords_list
        # 这个是根据略性新兴产业分类与国际专利分类划分的
        self.include_with_exclusions = {
            "A61B5": ["A61B5/0476", "A61B5/0478"]
        }

        # Placeholder for the dataframe
        self.df = None

        # 创建 LLM_filter 实例，根据local参数判断是否使用本地模型
        self.llm_filter = LLM_filter(model_path=model_path, local=local)
        self.llm_filter.load_model_tokenizer(model=model_name, key=key)

    def load_data(self):
        # 支持输入 csv或者excel文件
        # 检查文件格式并加载数据
        file_ext = Path(self.file_path).suffix
        if file_ext == '.xlsx':
            self.df = pd.read_excel(self.file_path, engine="openpyxl")
        elif file_ext == '.csv':
            self.df = pd.read_csv(self.file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

        # self.df = pd.read_excel(self.file_path)
        # Handle null values for IPC, Title, and Abstract columns
        self.df[self.ipc] = self.df[self.ipc].fillna('no IPC').astype(str)
        self.df[self.title] = self.df[self.title].fillna('no Title').astype(str)
        self.df[self.abstract] = self.df[self.abstract].fillna('no Abstract').astype(str)

        # 数据处理 text是标题和摘要的组合
        # self.df['text'] = 'Title: ' + self.df[self.title] + " " + "Abstract: " + self.df[self.abstract]
        self.df['text'] = self.df[self.abstract]
        # 创建一个新的列 每一列都是0 代表当前所有专利没有经过分类的情况下都是非AI的
        self.df['predict'] = 0

        # 创建一列 用来说明判断为1的原因
        # 原因1：keywords
        # 原因2: IPC Number
        # 原因3：LLM
        self.df['reason']= "0"

    # def ipc_filter(self, ipc_numbers):
    #     # 检查当前专利的IPC number是否在我们找的IPC number中
    #     # 需要从三个list中检查IPC number
    #     # 1. 完全匹配 -- 需要完全与提供的IPC number中的某个匹配 直接返回True
    #     # 2. 前缀匹配 -- 针对有*的IPC number 采用前缀和
    #     # 3. 针对有需要排除的IPC number
    #
    #     # 当前patent有的IPC number 因为每个patent不止一个IPC number 且用;隔开
    #     ipc_list = [ipc.strip() for ipc in ipc_numbers.split(';')]
    #
    #     # 循环检查
    #     for ipc_number in ipc_list:
    #         # 完全匹配
    #         if ipc_number in self.IPC:
    #             return True
    #
    #         # 前缀匹配
    #         if ipc_number.startswith('G06F40'):
    #             return True
    #
    #         # 前缀+排除
    #         for prefix, exclusions in self.include_with_exclusions.items():
    #             if ipc_number.startswith(prefix):
    #                 if any(ipc_number.startswith(exclusion) for exclusion in exclusions):
    #                     return False
    #                 return True
    #     return False

    def ipc_filter(self, ipc_numbers):
        cleaned_ipc_numbers = ipc_numbers.strip("[]").replace('"', '')
        # print('ipc_clean', cleaned_ipc_numbers)

        # 将逗号或分号分隔的字符串转换为列表
        ipc_list = [ipc.strip() for ipc in re.split(r'[;,]', cleaned_ipc_numbers)]

        # 完全匹配和前缀匹配检查
        for ipc_number in ipc_list:
            if ipc_number in self.IPC:
                return True, f"Matched IPC: {ipc_number}"
            if ipc_number.startswith('G06F40'):
                return True, f"Matched IPC Prefix: {ipc_number}"

            # 前缀+排除
            for prefix, exclusions in self.include_with_exclusions.items():
                if ipc_number.startswith(prefix):
                    if any(ipc_number.startswith(exclusion) for exclusion in exclusions):
                        return False, None
                    return True, f"Matched IPC Prefix with Exclusions: {ipc_number}"
        return False, None

    # # 版本一：可能速度不够快
    # def keywords_filter(self, text):
    #     # 关键词匹配
    #     for keyword in self.Keywords:
    #         if keyword.lower() in text.lower():
    #             return True
    #     return False

    # 版本二
    # chair这个次被匹配上了 因为其中有ai这两个字母
    # 使用单词边界
    def keywords_filter(self, text):
        keywords_pattern = r'\b(' + '|'.join([re.escape(keyword) for keyword in self.Keywords]) + r')\b'
        match = re.search(keywords_pattern, text, re.IGNORECASE)
        if match:
            return True, f"Matched Keyword: {match.group(0)}"
        return False, None

    def llm_filter_a(self, text):
        # 使用大模型进行预测
        return self.llm_filter.model_predict(text)

    def filter_data(self):
        # 先用keywords和IPC number进行初步的过滤
        # 把匹配上的都标为1
        # 第一阶段：IPC 和关键词过滤
        print("########################################")
        print("第一阶段：使用IPC number与Keywords进行初步过滤")
        print("########################################\n")
        tqdm.pandas(desc="初步过滤")
        # self.df['actual'] = self.df.progress_apply(
        #     lambda row: 1 if self.ipc_filter(row[self.ipc]) or self.keywords_filter(row['text']) else 0,
        #     axis=1
        # )
        def apply_filters(row):
            ipc_match, ipc_reason = self.ipc_filter(row[self.ipc])
            if ipc_match:
                row['predict'] = 1
                row['reason'] = ipc_reason
                return row

            keyword_match, keyword_reason = self.keywords_filter(row['text'])
            if keyword_match:
                row['predict'] = 1
                row['reason'] = keyword_reason
                return row

            return row

        self.df = self.df.progress_apply(apply_filters, axis=1)


        # 因为大模型的推理耗费资源和时间 所以在ipc与keywords之后单独进行
        # 抽出当前为0的数据 使用大模型进行推理
        # 对初步筛选为0的数据使用大模型进行过滤
        # 第二阶段：使用大模型进一步判断
        print("########################################")
        print("第二阶段：使用大模型进行二次判断")
        print("########################################")
        mask = self.df['predict'] == 0
        remaining_indices = self.df[mask].index
        for idx in tqdm(remaining_indices, desc="大模型过滤"):
            text = self.df.at[idx, 'text']
            if self.llm_filter_a(text):
                self.df.at[idx, 'predict'] = 1
                # gpt判断的
                self.df.at[idx, 'reason'] = "GPT"

    # 因为后续需要处理的文件过大 所以需要进行分块处理
    def load_data_in_chunks(self, chunksize=1000, output_file='result.xlsx'):
        file_ext = Path(self.file_path).suffix
        data_chunks = pd.read_csv(self.file_path, chunksize=chunksize) if file_ext == '.csv' else pd.read_excel(self.file_path)

        filtered_chunks = []  # 用于存储过滤后的块
        chunk_num = 0
        for chunk in data_chunks:
            print('Processing Chunk: ', chunk_num)
            # 处理缺失值
            chunk[self.ipc] = chunk[self.ipc].fillna('no IPC').astype(str)
            chunk[self.title] = chunk[self.title].fillna('no Title').astype(str)
            chunk[self.abstract] = chunk[self.abstract].fillna('no Abstract').astype(str)

            # 合并标题和摘要
            # chunk['text'] = 'Title: ' + chunk[self.title] + " " + "Abstract: " + chunk[self.abstract]
            chunk['text'] = chunk[self.abstract]
            # 针对US data做的修改
            # 初步过滤：关键词和IPC
            chunk['predict'] = chunk.apply(
                lambda row: 1 if self.ipc_filter(row[self.ipc]) or self.keywords_filter(row['text']) else 0, axis=1)

            # 二次过滤：使用大模型
            print("第二阶段：使用大模型进行二次判断")
            print("########################################")
            mask = chunk['predict'] == 0
            remaining_indices = chunk[mask].index
            for idx in tqdm(remaining_indices, desc="大模型过滤"):
                text = chunk.at[idx, 'text']
                if self.llm_filter_a(text):
                    chunk.at[idx, 'predict'] = 1

            # 将处理后的块加入列表
            filtered_chunks.append(chunk)
            chunk_num +=1

        # 合并所有过滤后的块并保存到Excel
        self.df = pd.concat(filtered_chunks, ignore_index=True)
        self.df.to_csv(output_file, index=False)
        print(f"Filtered data with LLM prediction has been saved as {output_file}")

    def save_filtered_data(self, output_file='predict.csv'):
        # 保存文件 最后的预测结果可以从保存的文件的最后一列查看
        self.df.to_csv(output_file, index=False)
        print(f"File has been saved as {output_file}")
