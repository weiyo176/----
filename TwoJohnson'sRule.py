import random
import matplotlib.pyplot as plt
import pandas as pd

def johnsonRule(jobs):
    #有幾個工作
    n = len(jobs)
    #保存原本的工作排序
    jobb = list(jobs)
    #排序工作由小到大
    jobs.sort(key=lambda x: min(x[0], x[1]))

    schedule_job1 = []  # Front
    schedule_job2 = []  # Back
    machine1_jobs = [job[0] for job in jobs]
    machine2_jobs = [job[1] for job in jobs]
    
    for i in range(n):
        #排序好的工作去找原始的索引值
        index = jobb.index(jobs[i]) + 1
        print('index',index)
        schedule_job1.append(index)
        #判斷工作要放前面還後面(機器一比較小，放在前)
        # if machine1_jobs[index-1] < machine2_jobs[index-1]:
        #     schedule_job1.append(index)
        # else:
        #     schedule_job2.insert(0, index)
    #前+後就是最佳化排序
    # return schedule_job1 + schedule_job2
    return schedule_job1
def get_user_input():
    try:
        num_jobs = int(input("請輸入工作的數量："))
        jobs = []

        for i in range(num_jobs):
            processing_time_machine1 = int(input(f"請輸入第{i+1}個工作在機器1上的處理時間："))
            processing_time_machine2 = int(input(f"請輸入第{i+1}個工作在機器2上的處理時間："))
            jobs.append((processing_time_machine1, processing_time_machine2))

        return jobs

    except ValueError:
        print("請輸入有效的數字。")
def generate_colors(num_colors):
    # 生成隨機的顏色
    return ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(num_colors)]
#x為每個工作開始的時間軸
def plot_gantt_chart(schedule, x,title="Gantt Chart"):
    df = pd.DataFrame(schedule, columns=["Start Time", "End Time", "Machine", "Job Name"])

     # 生成不同工作的隨機顏色
    unique_jobs = df["Job Name"].unique()
    job_colors = dict(zip(unique_jobs, generate_colors(len(unique_jobs))))

    # 根據工作名稱分配顏色
    df["Color"] = df["Job Name"].map(job_colors)

    fig, ax = plt.subplots(figsize=(10,5))
    
    for label, color in job_colors.items():
        ax.barh(df[df["Job Name"]==label]["Machine"],
                df[df["Job Name"]==label]["End Time"] - df[df["Job Name"]==label]["Start Time"],
                left=df[df["Job Name"]==label]["Start Time"],
                color=color,
                label=label)

        # 在每個條形上標示工作名稱
        for index, row in df[df["Job Name"]==label].iterrows():
            ax.text((row["Start Time"] + row["End Time"]) / 2, row["Machine"],
                    row["Job Name"], color='black', ha='center', va='center')

    ax.set_xlabel("time")
    ax.set_title(title)
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.0))
    plt.xticks(ticks=x)

    plt.show()
def main():
    # user_jobs = get_user_input()  #使用者輸入
    user_jobs = [(5,5),(4,3),(8,9),(2,7),(6,8),(12,15)]#預設
    print("用戶輸入的工作：", user_jobs)
    Ojob = list(user_jobs)
    # 使用 Johnson's Rule 獲得最佳排程
    user_optimal_schedule = johnsonRule(user_jobs)
    print("最佳排程的工作順序：", user_optimal_schedule)

    # 繪製兩台機器的工作時間甘特圖
    schedule = []
    time =[0]
    time_counter_machine1 = 0
    time_counter_machine2 = 0
    for job in user_optimal_schedule:
        print('job',job,user_jobs)
        #把機器1加入
        schedule.append((time_counter_machine1, time_counter_machine1 + Ojob[job - 1][0], "Machine1",str(job)))
        #增加排程時間
        time_counter_machine1 += Ojob[job - 1][0]
        time.append(time_counter_machine1)
        print('time1',time_counter_machine1,'user',Ojob[job - 1][0])
        #判斷機器1是否已經處理完了
        if time_counter_machine1 <= time_counter_machine2:
            schedule.append((time_counter_machine2, time_counter_machine2 + Ojob[job - 1][1], "Machine2",str(job)))
            time_counter_machine2 += Ojob[job - 1][1]
            time.append(time_counter_machine2)
        else:
            time_counter_machine2 = time_counter_machine1
            print(time_counter_machine2)
            schedule.append((time_counter_machine2, time_counter_machine2 + Ojob[job - 1][1], "Machine2",str(job)))
            time_counter_machine2 += Ojob[job - 1][1]
            time.append(time_counter_machine2)
    #畫圖
    plot_gantt_chart(schedule, time, title="Johnson's Rule")

if __name__ == '__main__':
    main()


