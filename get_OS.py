import subprocess

from datetime import datetime

user_list = set()
processes_count = 0
total_used_memory = 0
total_used_cpu = 0.0
max_memory_process = ""
max_memory_process_val = -1
max_cpu_process = ""
max_cpu_process_val = -1
users_processes_count = {}

process_output = subprocess.run(["ps", "aux"], capture_output=True)
process_output = process_output.stdout.decode()

process_output_list = process_output.split("\n")

for line_index in range(1, len(process_output_list)):
    output_line = process_output_list[line_index]
    output_cols = output_line.split(maxsplit=10)
    if not len(output_cols):
        continue
    processes_count += 1
    user_name = output_cols[0]
    cpu_usage = output_cols[2]
    total_used_cpu += float(cpu_usage)
    memory_usage = output_cols[3]
    total_used_memory += float(memory_usage)
    command = output_cols[10][:20]
    if max_memory_process_val < float(memory_usage):
        max_memory_process_val = float(memory_usage)
        max_memory_process = command
    if max_cpu_process_val < float(cpu_usage):
        max_cpu_process_val = float(cpu_usage)
        max_cpu_process = command

    user_list.add(user_name)

    users_processes_count[user_name] = users_processes_count.get(
        user_name, 0) + 1

users_processes_count_list = []
for k, v in users_processes_count.items():
    users_processes_count_list.append(f"{k}: {v}")

prosesses_by_users_str = '\n'.join(users_processes_count_list)
result = f"""
Отчёт о состоянии системы:
Пользователи системы: {', '.join(user_list)}
Процессов запущено: {processes_count}
Пользовательских процессов: 
{prosesses_by_users_str}
Всего памяти используется: {total_used_memory}%
Всего CPU используется: {total_used_cpu}%
Больше всего памяти использует: {max_memory_process}
Больше всего CPU использует: {max_cpu_process}
"""
print(result)

date_time_string = datetime.now().strftime("%d-%m-%Y-%H:%M")
file_name = f"{date_time_string}-scan.txt"

with open(file_name, "w") as file:
    file.write(result)
