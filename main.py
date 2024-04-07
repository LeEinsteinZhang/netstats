
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime, timedelta

pass_few_hours = 6
log = 0

# Change the path to your directory
directory_path = '/home/lez/ping_result'

eight_hours_ago = datetime.now() - timedelta(hours=pass_few_hours)

count = 0
sum = 0
loss = 0

graph_date = []
graph_latency = []
highest_pings = [0,0,0,0,0,0,0,0,0,0]
n = 0

# List all files and sort them
all_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
sorted_files = sorted(all_files)

for filename in sorted_files:
    file_path = os.path.join(directory_path, filename)
    with open(file_path, mode='r') as file:
        data = csv.DictReader(file)
        for row in data:
            timestamp = datetime.fromisoformat(row['testTime'])
            if pass_few_hours:
                if timestamp < eight_hours_ago:
                    continue
            latency = row['latency']
            graph_date.append(n)
            if latency == 'NULL':
                loss += 1
                graph_latency.append('')
            else:
                latency = float(latency)
                sum += latency
                count += 1
                graph_latency.append(latency)

                if latency > min(highest_pings):
                    highest_pings.append(latency)
                    highest_pings = sorted(highest_pings, reverse=True)[:10]
            n += 1

mean = round(np.mean(graph_latency), 4)
median = round(np.median(graph_latency), 4)
variance = round(np.var(graph_latency), 4)
std_dev = round(np.std(graph_latency), 4)
max_ping = max(graph_latency)
min_ping = min(graph_latency)
loss_rate = round(loss/len(graph_latency) * 100,4)

print(f"highest: {max_ping:10.2f}ms | lowest: {min_ping:10.2f}ms")
print(f"mean:    {mean:10.2f}ms | median:  {median:10.2f}ms")
print(f"variance: {variance:10.2f}  | std_dev: {std_dev:10.2f}")
print(f"loss rate: {loss_rate}%")

stats_text = f'''Highest: {max_ping:.2f}ms
Lowest: {min_ping:.2f}ms
Mean: {mean:.2f}ms
Median: {median:.2f}ms
Variance: {variance:.2f}
Std Dev: {std_dev:.2f}
Loss Rate: {loss_rate}%'''

ping_mean = [mean] * len(graph_date)

y_string = "Latency (ms)"
if log:
    y_string = "log Latency (ms)"
    graph_latency = np.log(graph_latency)
    ping_mean = np.log(ping_mean)

# 设置图形的整体布局大小
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制延迟和平均延迟线
ax.plot(graph_date, graph_latency, linestyle='-', color='royalblue', label='Latency')
ax.plot(graph_date, ping_mean, linestyle='-', color='red', label='Mean Latency')

# 添加统计数据文本
stats_text = f'''Highest: {max_ping:.2f}ms
Lowest: {min_ping:.2f}ms
Mean: {mean:.2f}ms
Median: {median:.2f}ms
Variance: {variance:.2f}
Std Dev: {std_dev:.2f}
Loss Rate: {loss_rate}%'''

# 添加文本框到图形外的右侧
fig.text(0.85, 0.5, stats_text, verticalalignment='center', fontsize=10, bbox=dict(boxstyle="round", alpha=0.5, color='lightgrey'))

# 调整子图参数，为右侧文本留出空间
plt.subplots_adjust(right=0.8)

# 添加图例和标题
ax.legend()
ax.set_title('Ping Latency Over Time')
ax.set_xlabel('Date/Time')
ax.set_ylabel(y_string)

# 显示图形
plt.savefig('/home/lez/git/netstats/ping_latency_over_time.png')
plt.show()
