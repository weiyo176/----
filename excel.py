import pandas as pd
import random

# 讓使用者輸入機器的數量和工作的數量
num_machines = int(input("請輸入機器的數量: "))
num_jobs = int(input("請輸入工作的數量: "))

# 創建一個包含指定數量的工作的列表
jobs = ['Job' + str(i) for i in range(1, num_jobs + 1)]

# 為每個工作生成一個介於1到30的隨機數值，對於指定數量的機器
machines = {f'machine {i+1}': [random.randint(1, 30) for _ in range(num_jobs)] for i in range(num_machines)}

# 將工作列表添加到數據字典中
machines['Job'] = jobs

# 創建一個 DataFrame
df = pd.DataFrame(machines)

# 將 'Job' 列移到其他列之前
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

# 將 DataFrame 寫入 .xlsx 文件
df.to_excel('output.xlsx', index=False)