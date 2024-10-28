# RAG_QWen
基于大语言模型LLM构建一个问答系统，问答内容涉及基金/股票/债券/招股书等不同数据来源

## 初步准备
竞赛的主要流程为使用RAG结合.db与.pdf数据构建一个基于大语言模型LLM的问答系统。

首先，我将只考虑将大语言模型与pdf数据进行结合，获得答案。之后再做NL2SQL的任务。

### PDF文件转txt文件
对于PDF数据，首先需要将其转化为.txt文件，以使得LLM更好的理解。竞赛题中给了转化好的txt文件，但是转化效果一般，且pdf文件中的表格数据没有被很好地抓取出来。于是，在这一步我首先尝试使用pdfplumber，这样能在保留pdf内容的情况下更好的获取pdf文件中的表格数据。还有很多其他的方式，我将后续尝试pdfminer、gptpdf、RAGFlow等一系列工具。`（如何查看并比较不同方法转化的效果？）`

问题一：如何更好的读取PDF中的数据

问题二：如何将文件以公司名进行命名 （方便后续的检索）

问题三：如何抓取PDF中的表格数据

问题四：模块化，方便后续修改

pdf2txt文件夹中提供了pdfplumber的使用过程，以及使用LLM分析并抓取文件中公司名称并且修改文件名的过程。
处理过后的文件可以从下方链接下载。
https://drive.google.com/drive/folders/1kiMREC8LdFsgJt6VpJk6cVvuU-LwQhH8?usp=drive_link

### 文档分块

### 文档检索与重排

### 结果生成


### 检查RAG的效果

