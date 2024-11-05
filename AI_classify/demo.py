import re

import pandas as pd

from llm_filter import LLM_filter

# DEMO1: 关键词的匹配
class AIfilter:
    def __init__(self, keywords, ipc_list=None, include_with_exclusions=None):
        self.Keywords = keywords
        self.IPC = ipc_list if ipc_list else []
        self.include_with_exclusions = include_with_exclusions if include_with_exclusions else {}

    def keywords_filter(self, text):
        # 使用单词边界确保完整匹配
        keywords_pattern = r'\b(' + '|'.join([re.escape(keyword) for keyword in self.Keywords]) + r')\b'
        match = re.search(keywords_pattern, text, re.IGNORECASE)
        if match:
            return True, f"Matched Keyword: {match.group(0)}"
        return False, None

    def ipc_filter(self, ipc_numbers):
        cleaned_ipc_numbers = ipc_numbers.strip("[]").replace('"', '')
        print('ipc_clean', cleaned_ipc_numbers)

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

# 测试 DEMO1: 关键词匹配
keywords = ["actuator"]
text = "Linear actuator a linear actuator is configured to provide the moving force for adjustable furniture such as beds chairs or tables the linear actuator includes a drive assembly rigid arm and linkage assembly the rigid arm includes a pusher block with one or more attachment projections where the linkage assembly is attached."

# 创建 AIfilter 实例
aifilter = AIfilter(keywords)

# 测试 keywords_filter 方法
match_result, reason = aifilter.keywords_filter(text)

# 输出结果
print("DEMO1 - Keywords Match Result:", match_result)
print("Reason:", reason)


# DEMO2: 使用LLM API进行分类
# 示例文本
test_text = "This patent involves a machine learning model for image recognition tasks, a core AI technology."

# 创建 LLM_filter 实例
llm_filter = LLM_filter(model_path=None, local=False)
llm_filter.load_model_tokenizer(model="gpt-4o-mini", key="your_openai_api_key")

# 调用 model_predict 进行测试
is_ai_related = llm_filter.model_predict(test_text)
print("DEMO2 - Is AI related:", is_ai_related)


# DEMO3: IPC编号匹配
ipc_list = ["C01B33/12", "A61B5"]
include_with_exclusions = {
    "A61B5": ["A61B5/0476", "A61B5/0478"]
}
ipc_numbers = "G06F40; A61B5/0478; A61B5/0000"
df = pd.read_csv('data/base_data.csv')
ipc1 = df['ipc'][1]
print(ipc1)
# 创建包含 IPC 列表和排除条件的 AIfilter 实例
aifilter_ipc = AIfilter(keywords=[], ipc_list=ipc_list, include_with_exclusions=include_with_exclusions)

# 测试 ipc_filter 方法
ipc_match_result, ipc_reason = aifilter_ipc.ipc_filter(ipc1)

# 输出结果
print("DEMO3 - IPC Match Result:", ipc_match_result)
print("Reason:", ipc_reason)

