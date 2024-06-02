import threading
import time
import queue


class Process:
    def __init__(self, id, task, priority, size=None):
        self.id = id
        self.task = task
        self.priority = priority
        self.size = size
        self.execution_count = 0
        self.state = "ready"

    def __lt__(self, other):
        if self.execution_count == other.execution_count:
            return self.priority < other.priority
        else:
            return self.execution_count < other.execution_count

    def million_loop(self, time_slice):
        self.state = "running"
        print(f"process{self.id} state: running")
        count = 0
        total = 0
        start_time = time.time()
        try:
            with open(f"{self.id}.txt", 'r') as file:
                total = int(file.read())
        except FileNotFoundError:
            with open(f"{self.id}.txt", 'w+') as file:
                file.write(str(total))
        while True:
            if scheduler.paused:  # 일시 중지 상태 확인
                print(f"process{self.id} paused")
                print(f"process{self.id} state: ready\n")
                while scheduler.paused:
                    time.sleep(0.1)  # 일시 중지 상태가 해제될 때까지 대기
                print(f"process{self.id} resumed")
                print(f"process{self.id} state: running")
                self.state = "running"
                start_time = time.time()  # 시간을 재설정하여 정확한 시간을 유지

            if total + count > 10000000:
                self.state = "complete"
                print("Repeating complete!!")
                print(f"process{self.id} state: complete")
                break
            count += 1
            if time.time() >= start_time+time_slice:
                total = total + count
                self.state = "ready"
                print(f"{total}times repeats")
                print(f"CPU time over - process{self.id} state: ready")
                with open(f"{self.id}.txt", 'w') as file:
                    file.write(str(total))
                break

    def file_download_simulation(self, size, time_slice):
        self.state = "running"
        print(f"process{self.id} state: running")
        elapsed_time = 0
        total = 0
        start_time = time.time()
        try:
            with open(f"{self.id}.txt", 'r') as file:
                total = float(file.read())
        except FileNotFoundError:
            with open(f"{self.id}.txt", 'w+') as file:
                file.write(str(total))
        while True:
            if scheduler.paused:  # 일시 중지 상태 확인
                print(f"process{self.id} paused")
                print(f"process{self.id} state: ready\n")
                while scheduler.paused:
                    time.sleep(0.1)  # 일시 중지 상태가 해제될 때까지 대기
                print(f"process{self.id} resumed")
                print(f"process{self.id} state: running")
                self.state = "running"
                start_time = time.time()  # 시간을 재설정하여 정확한 시간을 유지

            if (total + elapsed_time) / size > 1:
                self.state = 'complete'
                print("Download complete!!")
                print(f"process{self.id} state: complete")
                break
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_slice:
                total = total + elapsed_time
                self.state = "ready"
                print(f"{total/size*100}% downloading...")
                print(f"CPU time over - process{self.id} state: ready")
                with open(f"{self.id}.txt", 'w') as file:
                    file.write(str(total))
                break


class Scheduler:
    def __init__(self, time_slice):
        self.process_queue = queue.PriorityQueue()
        self.time_slice = time_slice
        self.time = 0
        self.paused = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def add_process(self, process):
        self.process_queue.put(process)

    def start(self):
        while not self.process_queue.empty():
            while self.paused:  # 일시 중지 상태일 때는 대기
                time.sleep(0.1)
            process = self.process_queue.get()
            if process.state != "complete":
                if process.task == 'million_loop':
                    process.million_loop(self.time_slice)
                elif process.task == 'file_download_simulation':
                    process.file_download_simulation(
                        process.size, self.time_slice)
                process.execution_count += 1
                if process.state != "complete":
                    self.add_process(process)


def listen_for_input(scheduler):
    while True:
        input("Press the enter key to pause the process\n")

        # 스케줄러가 이미 일시 중지 상태인 경우 재개
        if scheduler.paused:
            process.state = 'running'
            scheduler.resume()
        else:
            scheduler.pause()
            process.state = 'ready'
            print("Keyboard interrupt!!\n")
            input("Press the enter key to resume the process")
            scheduler.resume()


if __name__ == "__main__":
    time_slice = 1
    scheduler = Scheduler(time_slice)
    processes = [
        Process(0, task='million_loop', priority=3),
        Process(1, task='file_download_simulation', priority=1, size=10.5),
        Process(2, task='million_loop', priority=2),
        Process(3, task='file_download_simulation', priority=2, size=7)
    ]

    for process in processes:
        scheduler.add_process(process)

    input_thread = threading.Thread(target=listen_for_input, args=(scheduler,))
    input_thread.start()

    scheduler_thread = threading.Thread(target=scheduler.start)
    scheduler_thread.start()
    scheduler_thread.join()
