import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv('predict_AI_3.csv')
list1 = df['actual']
list2 = df['predict']

#print(list1)

def calculate_accuracy(list1, list2):
    correct_predictions = (list1 == list2).sum()  # 计算预测正确的数量
    total_predictions = len(list1)  # 总预测数
    accuracy = correct_predictions / total_predictions  # 计算准确率
    return accuracy

# 计算分类报告
print(calculate_accuracy(list1,list2))
report = classification_report(list1, list2, target_names=['Class 0', 'Class 1'])
print("Classification Report:\n", report)

print(sum(list2))