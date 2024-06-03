import os
import shutil


class FileSystemSimulatorCLI:
    def __init__(self):
        self.current_dir = os.getcwd()

    def create_file(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)
        print(f"파일 '{filename}'이 생성되었습니다.")

    def delete_file(self, filename):
        try:
            os.remove(filename)
            print(f"파일 '{filename}'이 삭제되었습니다.")
        except FileNotFoundError:
            print(f"에러: 파일 '{filename}'이 없습니다.")

    def read_file(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            print(f"파일이름: '{filename}'\n{content}")
        except FileNotFoundError:
            print(f"에러: 파일 '{filename}'이 없습니다.")

    def write_file(self, filename, content):
        if not os.path.exists(filename):
            create_new = input(
                f"파일 '{filename}'이 없습니다. 새로 생성하시겠습니까? (yes/no): ").strip().lower()
            if create_new == 'yes':
                self.create_file(filename, content)
            else:
                print("실행이 취소되었습니다.")
        else:
            with open(filename, 'a') as f:
                f.write('\n' + content)
            print(f"파일 '{filename}'이 수정되었습니다.")

    def create_directory(self, dirname):
        original_dirname = dirname
        count = 1

        while os.path.exists(dirname):
            dirname = f"{original_dirname}({count})"
            count += 1
        os.makedirs(dirname)
        print(f"폴더 '{dirname}'가 생성되었습니다.")

    def delete_directory(self, dirname):
        try:
            os.rmdir(dirname)
            print(f"폴더 '{dirname}'가 삭제되었습니다.")
        except FileNotFoundError:
            print(f"에러: 폴더 '{dirname}'가 없습니다.")
        except OSError:
            print(f"에러: 폴더 '{dirname}'가 비어있지 않습니다.")

    def change_directory(self, dirname):
        try:
            os.chdir(dirname)
            self.current_dir = os.getcwd()
            print(f"'{self.current_dir}'로 이동했습니다.")
        except FileNotFoundError:
            print(f"에러: 경로 '{dirname}'가 없습니다.")
        except NotADirectoryError:
            print(f"에러: '{dirname}'는 디렉토리가 아닙니다.")
        except Exception as e:
            print(f"에러: {e}")

    def search_file(self, filename):
        found = False
        for root, dirs, files in os.walk(self.current_dir):
            if filename in files:
                file_path = os.path.join(root, filename)
                print(f"파일 '{filename}'은 '{file_path}'에 있습니다.")
                found = True
        if not found:
            print(f"에러: 파일 '{filename}'이 없습니다.")

    def move(self, src, dst):
        try:
            shutil.move(src, dst)
            print(f"'{src}'를 '{self.current_dir}'에서 '{dst}'로 이동합니다.")
        except FileNotFoundError:
            print(f"에러: '{src}'를 찾지 못했습니다.")
        except Exception as e:
            print(f"에러: {e}")

    def list_directory(self):
        files = os.listdir(self.current_dir)
        print(f"현재 경로: {self.current_dir}")
        for file in files:
            print(file)

    def show_help(self):
        help_text = """
        명령어 목록

        create <파일이름> <내용>        - 새 파일을 생성을 생성합니다. 파일이름과 내용 입력이 필수적입니다.
        delete <파일이름>               - 파일을 삭제합니다.
        read <파일이름>                 - 파일을 읽어와서 출력합니다.
        write <파일이름> <내용>         - 파일에 추가합니다. 존재하지 않는 파일일 경우에 새로 파일을 생성할 수 있습니다.
        mkdir <폴더이름>                - 새 폴더를 생성합니다.
        rmdir <폴더이름>                - 폴더를 삭제합니다.
        cd <경로>                       - 경로를 이동합니다.
        search <파일이름>               - 파일을 찾아서 경로를 출력합니다.
        mv <파일이름/폴더이름> <경로>    - 파일이나 폴더를 이동합니다.
        list                            - 현재 경로 내의 모든 파일 및 폴더를 출력합니다.
        help                            - 도움말을 출력합니다.
        exit                            - 프로그램을 종료 합니다.
        """
        print(help_text)

    def run(self):
        while True:
            command = input(f"{self.current_dir}> ").strip().split()
            if not command:
                continue

            cmd = command[0]
            if cmd == "create" and len(command) == 3:
                self.create_file(command[1], command[2])
            elif cmd == "delete" and len(command) == 2:
                self.delete_file(command[1])
            elif cmd == "read" and len(command) == 2:
                self.read_file(command[1])
            elif cmd == "write" and len(command) == 3:
                self.write_file(command[1], command[2])
            elif cmd == "mkdir" and len(command) == 2:
                self.create_directory(command[1])
            elif cmd == "rmdir" and len(command) == 2:
                self.delete_directory(command[1])
            elif cmd == "cd" and len(command) == 2:
                self.change_directory(command[1])
            elif cmd == "search" and len(command) == 2:
                self.search_file(command[1])
            elif cmd == "mv" and len(command) == 3:
                self.move(command[1], command[2])
            elif cmd == "list" and len(command) == 1:
                self.list_directory()
            elif cmd == "help" and len(command) == 1:
                self.show_help()
            elif cmd == "exit":
                print("시뮬레이터를 종료합니다.")
                break
            else:
                print("잘못된 명령어 입니다. 'help' 명령어를 통해 도움말을 볼 수 있습니다.")


if __name__ == "__main__":
    fs_simulator = FileSystemSimulatorCLI()
    fs_simulator.run()
