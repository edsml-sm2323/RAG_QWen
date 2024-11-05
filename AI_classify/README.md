# AI classify

## 具体流程

第一步：使用查找的AI关键词与AI相关的IPC number对数据进行初步的过滤

（关键词与IPC number可以在config.py中查询）

第二步：对仍然没有判定为AI专利的数据使用prompt+few shot方法使用openai的模型进行分类

第三步：使用result.py查看分类的结果

