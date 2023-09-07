import time
from collections import deque

class Process:
    def init(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time

class Scheduler:
    def init(self, time_slice):
        self.processes = deque()
        self.time_slice = time_slice

    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        current_time = 0
        while self.processes:
            process = self.processes.popleft()
            if process.arrival_time > current_time:
                current_time = process.arrival_time
            print(f"Running process {process.name} at time {current_time}")
            if process.burst_time <= self.time_slice:
                time.sleep(process.burst_time)
                current_time += process.burst_time
            else:
                time.sleep(self.time_slice)
                process.burst_time -= self.time_slice
                current_time += self.time_slice
                self.processes.append(process)

# Criação dos processos
p1 = Process().init("P1", 0, 8)
p2 = Process().init("P2", 2, 4)
p3 = Process().init("P3", 4, 6)

# Criação do escalonador e adição dos processos
scheduler = Scheduler().init(time_slice=3)
Scheduler().add_process()
scheduler = Scheduler.add_process(p1)
scheduler = Scheduler.add_process(p2)
scheduler = Scheduler.add_process(p3)

# Execução do escalonador
scheduler.run()