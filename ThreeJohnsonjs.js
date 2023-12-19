// JavaScript 版本的 Johnson's Rule
function johnsonRule(jobs) {
    let n = jobs.length;
    let jobb = [...jobs];
    jobs.sort((a, b) => Math.min(a[0] + a[1], a[1] + a[2]) - Math.min(b[0] + b[1], b[1] + b[2]));

    let schedule_job1 = [];  // Front
    let schedule_job2 = [];  // Back
    let machine1_jobs = jobs.map(job => job[0] + job[1]);
    let machine2_jobs = jobs.map(job => job[1] + job[2]);

    for (let i = 0; i < n; i++) {
        let index = jobb.indexOf(jobs[i]) + 1;
        if (machine1_jobs[i] < machine2_jobs[i]) {
            schedule_job1.push(index);
        } else {
            schedule_job2.unshift(index);
        }
    }
    return schedule_job1.concat(schedule_job2);
}

// 這裡我們假設你已經有一個 HTML 元素來顯示圖表，例如：<canvas id="myChart"></canvas>
//schedule = ["Start Time", "End Time", "Machine", "Job Name"]
function plotGanttChart(n, m, schedule) {
    let ctx = document.getElementById('myChart').getContext('2d');


    let machineName = [];
    for (let i = 1; i <= n; i++) {
        machineName.push("Machine " + i.toString());
    };
    // 將排程轉換成 Chart.js 所需的格式
    let datasets = [];
    let currentMachine = null;
    let currentData = [];
    let currentBackgroundColor = [];
    let labels = [];
    let temp = [];

    //schedule = ["Start Time", "End Time", "Machine", "Job Name"]
    schedule.forEach((job, index) => {
        temp.push([job[0], job[1]]);
        //put job start time and End time into labels
        if (index % n == n - 1) {
            labels.push(temp);
            temp = [];
        }
    });
    console.log(labels);

    for (let i = 0; i < m; i++) {
        RandonColor = `hsl(${i / n * 360}, 100%, 75%)`;
        datasets.push({
            label: `job ${i + 1}`,
            data: labels[i],
            backgroundColor: RandonColor,
            borderColor: RandonColor,
            borderWidth: 1,
            borderSkipped: 'false'
        });
    }


    const data = {
        //schedule = ["Start Time", "End Time", "Machine", "Job Name"]
        labels: machineName,
        datasets: datasets
    };
    const config = {
        type: 'bar',
        data,
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    stacked: false
                },
                y: {
                    stacked: true,
                    beginAtZero: true
                }
            }
            // 懸浮不顯示提示
            ,
            plugins: {
                tooltip: {
                    enabled: false
                },
                datalabels: {
                formatter: function (value, context) {
                    console.log(context)
                    console.log(value)
                    return value[1] - value[0];
                }
            }
            }
        },
        plugins: [ChartDataLabels]
    };
    new Chart(ctx, config);
}
// test
function test() {
    let ctx = document.getElementById('myChart').getContext('2d');


    // setup 
    const data = {
        //schedule = ["Start Time", "End Time", "Machine", "Job Name"]
        //schedule Machine 
        labels: ['Mon', 'Tue', 'Wed'],
        datasets: [{
            label: 'Weekly Sales',
            data: [[0, 3], [3, 4], [5, 6]],
            backgroundColor: 'rgba(255, 26, 104, 1)',
            borderColor: 'rgba(255, 26, 104, 1)',
            borderWidth: 1,
            borderSkipped: 'false'
        }, {
            label: 'Weekly Sales',
            data: [[3, 5], [4, 10], [5, 6]],
            backgroundColor: 'rgba(1, 0, 0, 1)',
            borderColor: 'rgba(1, 0, 0, 1)',
            borderWidth: 1,
            borderSkipped: 'false'
        }]
    };
    const config = {
        type: 'bar',
        data,
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    stacked: false
                },
                y: {
                    stacked: true,
                    beginAtZero: true
                }
            },
            // 懸浮不顯示提示
            plugins: {
                tooltip: {
                    enabled: false
                }
            },
            formatter: function (value, context) {
                console.log(context);
            }
        },
        plugins: [ChartDataLabels]
    };
    new Chart(ctx, config);
}

// 主函數
function main() {
    let user_jobs = [[10, 5, 12], [5, 10, 18], [7, 3, 15], [1, 5, 20]];
    console.log("用戶輸入的工作：", user_jobs);
    let Ojob = [...user_jobs];
    let user_optimal_schedule = johnsonRule(user_jobs);
    console.log("最佳排程的工作順序：", user_optimal_schedule);

    let schedule = [];
    let time_counter_machine1 = 0;
    let time_counter_machine2 = 0;
    let time_counter_machine3 = 0;
    for (let job of user_optimal_schedule) {
        schedule.push([time_counter_machine1, time_counter_machine1 + Ojob[job - 1][0], 1, job]);
        time_counter_machine1 += Ojob[job - 1][0];
        if (time_counter_machine1 <= time_counter_machine2) {
            schedule.push([time_counter_machine2, time_counter_machine2 + Ojob[job - 1][1], 2, job]);
            time_counter_machine2 += Ojob[job - 1][1];
        } else {
            time_counter_machine2 = time_counter_machine1;
            schedule.push([time_counter_machine2, time_counter_machine2 + Ojob[job - 1][1], 2, job]);
            time_counter_machine2 += Ojob[job - 1][1];
        }
        if (time_counter_machine2 <= time_counter_machine3) {
            schedule.push([time_counter_machine3, time_counter_machine3 + Ojob[job - 1][2], 3, job]);
            time_counter_machine3 += Ojob[job - 1][2];
        } else {
            time_counter_machine3 = time_counter_machine2;
            schedule.push([time_counter_machine3, time_counter_machine3 + Ojob[job - 1][2], 3, job]);
            time_counter_machine3 += Ojob[job - 1][2];
        }
    }
    console.log(user_jobs.length, schedule);
    // test();
    //(機器數量,工作數量,排程=[開始時間,結束時間,機器,工作])
    plotGanttChart(user_jobs[0].length, user_jobs.length, schedule);
}

main();