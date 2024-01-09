import pandas as pd
import random

# 讓使用者輸入機器的數量和工作的數量
num_machines = int(input("請輸入機器的數量 (2 或 3): "))
while num_machines not in [2, 3]:
    print("機器的數量必須為 2 或 3")
    num_machines = int(input("請輸入機器的數量 (2 或 3): "))

num_jobs = int(input("請輸入工作的數量: "))

# 創建一個包含指定數量的工作的列表
jobs = [ str(i) for i in range(1, num_jobs + 1)]

# 為每個工作生成一個介於1到30的隨機數值，對於指定數量的機器
machines = {f'machine {i+1}': [random.randint(1, 100) for _ in range(num_jobs)] for i in range(num_machines)}

# 如果機器的數量為 3，則檢查並滿足特定的條件
if num_machines == 3:
    while not (min(machines['machine 1']) >= max(machines['machine 2']) or min(machines['machine 3']) >= max(machines['machine 2'])):
        machines = {
            'machine 1': [random.randint(31, 50) for _ in range(num_jobs)],
            'machine 2': [random.randint(1, 30) for _ in range(num_jobs)],
            'machine 3': [random.randint(31, 50) for _ in range(num_jobs)]
        }

# 將工作列表添加到數據字典中
machines['Job'] = jobs

# 創建一個 DataFrame
df = pd.DataFrame(machines)

# 將 'Job' 列移到其他列之前
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

# 將 DataFrame 寫入 .xlsx 文件
df.to_excel(f'{num_machines}machine_{num_jobs}.xlsx', index=False)