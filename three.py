import random
import matplotlib.pyplot as plt
import pandas as pd

def johnsonRule(jobs):
    n = len(jobs)
    jobb = list(jobs)
    jobs.sort(key=lambda x: min(x[0] + x[1], x[1] + x[2]))

    schedule_job1 = []  # Front
    schedule_job2 = []  # Back
    machine1_jobs = [job[0] + job[1] for job in jobs]
    machine2_jobs = [job[1] + job[2] for job in jobs]
    # print("11:",machine1_jobs)
    # print("22",machine2_jobs)
    
    for i in range(n):
        index = jobb.index(jobs[i]) + 1
        if machine1_jobs[i] < machine2_jobs[i]:
            schedule_job1.append(index)
        else:
            schedule_job2.insert(0, index)
    return schedule_job1 + schedule_job2

def get_user_input():
    try:
        num_jobs = int(input("請輸入工作的數量："))
        jobs = []

        for i in range(num_jobs):
            processing_time_machine1 = int(input(f"請輸入第{i+1}個工作在機器1上的處理時間："))
            processing_time_machine2 = int(input(f"請輸入第{i+1}個工作在機器2上的處理時間："))
            processing_time_machine3 = int(input(f"請輸入第{i+1}個工作在機器3上的處理時間："))
            jobs.append((processing_time_machine1, processing_time_machine2, processing_time_machine3))

        return jobs

    except ValueError:
        print("請輸入有效的數字。")

def generate_colors(num_colors):
    return ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(num_colors)]

def plot_gantt_chart(schedule, x,title="Gantt Chart"):
    df = pd.DataFrame(schedule, columns=["Start Time", "End Time", "Machine", "Job Name"])
    unique_jobs = df["Job Name"].unique()
    job_colors = dict(zip(unique_jobs, generate_colors(len(unique_jobs))))
    df["Color"] = df["Job Name"].map(job_colors)

    fig, ax = plt.subplots(figsize=(10,5))
    
    for label, color in job_colors.items():
        ax.barh(df[df["Job Name"]==label]["Machine"],
                df[df["Job Name"]==label]["End Time"] - df[df["Job Name"]==label]["Start Time"],
                left=df[df["Job Name"]==label]["Start Time"],
                color=color,
                label=label)

        for index, row in df[df["Job Name"]==label].iterrows():
            ax.text((row["Start Time"] + row["End Time"]) / 2, row["Machine"],
                    row["Job Name"], color='black', ha='center', va='center')

    ax.set_xlabel("time")
    ax.set_title(title)
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.0))
    plt.xticks(ticks=x)

    plt.show()

def main():
    user_jobs = [(10, 5, 12), (5, 10, 18), (7, 3, 15), (1, 5, 20)]
    # user_jobs = get_user_input()
    print("用戶輸入的工作：", user_jobs)
    Ojob = list(user_jobs)
    user_optimal_schedule = johnsonRule(user_jobs)
    print("最佳排程的工作順序：", user_optimal_schedule)

    schedule = []
    time =[0]
    time_counter_machine1 = 0
    time_counter_machine2 = 0
    time_counter_machine3 = 0
    for job in user_optimal_schedule:
        schedule.append((time_counter_machine1, time_counter_machine1 + Ojob[job - 1][0], "Machine1",str(job)))
        time_counter_machine1 += Ojob[job - 1][0]
        time.append(time_counter_machine1)
        if time_counter_machine1 <= time_counter_machine2:
            schedule.append((time_counter_machine2, time_counter_machine2 + Ojob[job - 1][1], "Machine2",str(job)))
            time_counter_machine2 += Ojob[job - 1][1]
            time.append(time_counter_machine2)
        else:
            time_counter_machine2 = time_counter_machine1
            schedule.append((time_counter_machine2, time_counter_machine2 + Ojob[job - 1][1], "Machine2",str(job)))
            time_counter_machine2 += Ojob[job - 1][1]
            time.append(time_counter_machine2)
        if time_counter_machine2 <= time_counter_machine3:
            schedule.append((time_counter_machine3, time_counter_machine3 + Ojob[job - 1][2], "Machine3",str(job)))
            time_counter_machine3 += Ojob[job - 1][2]
            time.append(time_counter_machine3)
        else:
            time_counter_machine3 = time_counter_machine2
            schedule.append((time_counter_machine3, time_counter_machine3 + Ojob[job - 1][2], "Machine3",str(job)))
            time_counter_machine3 += Ojob[job - 1][2]
            time.append(time_counter_machine3)
    plot_gantt_chart(schedule, time, title="Johnson's Rule")

if __name__ == '__main__':
    main()