
pythonRouge 使用

1. pythonROUGE(summary_path,reference_path):调用只需要指定当前待评测的摘要路径和对应的评价文档集路径
2. 如果是DUC语料，摘要的命名方式以duc的主题命名（多个摘要需要文件名包含主题号或者说需要根据命名获得主题号就行）
3. 具体的ROUGE/rougedata地址根据ROUGE-1.5.5存放地址具体设定即可
4. ROUGE的参数根据不同需求，更改options选项即可
5. 如果不是duc语料，在创建rouge对应xml时，格式如下：
    <version>
        repeat:
        <evalID ..> : 当前要评测的摘要
        <peers path> : 摘要路径
        <model path> : 官方摘要路径
        <peers> : 当前主题下，其他摘要（生成一个就不需要了）
        <models> : 当前主题所有的官方评价摘要

    使用可以产生、保存好摘要后，直接pythonROUGE，也可以直接嵌入到程序中
    当前的输出的是文件，全部指标输出，如果需要某一个指标可以在输出中另写函数抽取（即从result中抽）
