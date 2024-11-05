from dataset_process import AIfilter
import config

# 初始化 AIfilter 实例
aifilter = AIfilter(
    file_path="data/US_data.csv",              # 文件路径
    ipc="ipc c",                          # IPC 列名
    title="app number",                  # Title 列名
    abstract="abstract",               # Abstract 列名
    ipc_list=config.IPC_num_list,         # IPC 过滤列表
    keywords_list=config.keywords_list,   # 关键词列表
    model_path=config.local_model_path,   # 本地模型路径
    key =config.key,
    model_name=config.model_name,
    local=False                            # 使用本地模型或调用API
)

# aifilter.load_data_in_chunks(chunksize=2000, output_file='result_US.csv')

aifilter.load_data()
aifilter.filter_data()
aifilter.save_filtered_data("predict_AI_3.csv")





