import pandas as pd

# 读取文件
trainSet = pd.read_csv('../liar_dataset/liar_dataset/train.tsv', sep='\t', header=None, index_col=False,
                       names=['id', 'label', 'statement', 'subject', 'speaker', 'jobTitle', 'stateInfo', 'party',
                              'barelyTrueCounts', 'falseCounts', 'halfTrueCounts', 'mostlyTrueCounts', 'onFireCounts'])

# 替换id为数字
id_list = []  # 新建list用于存储数字id
for row in trainSet['id']:
    id_list.append(row.split('.')[0])  # 将id以'.'分割提取数字
ID = pd.DataFrame(data=id_list)  # 创建新列存储数字id
trainSet.drop(columns='id', inplace=True)  # 删除原id
trainSet.insert(0, 'id', ID)  # 插入新id至第1列

# 输出前5行
print(trainSet.head())
