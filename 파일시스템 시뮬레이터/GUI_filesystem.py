import os
import shutil
import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Button, Scrollbar, VERTICAL


class CustomMessageBox(Toplevel):
    def __init__(self, parent, title, message, width=300, height=200):
        super().__init__(parent)

        self.title(title)

        self.geometry(f"{width}x{height}")

        self.message_text = Text(self, wrap="word", width=width, height=height)
        self.message_text.insert("1.0", message)
        self.message_text.config(state="disabled")
        self.message_text.pack(pady=10)

        scrollbar = Scrollbar(self, orient=VERTICAL,
                              command=self.message_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.message_text.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        ok_button = Button(button_frame, text="OK", command=self.destroy)
        ok_button.pack()

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)


def show_custom_messagebox(parent, title, message, width=300, height=200):
    CustomMessageBox(parent, title, message, width, height)


class FileSystemSimulatorGUI:
    def __init__(self, root):
        self.current_dir = os.getcwd()
        self.root = root
        self.root.title("File System Simulator")

        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(pady=20, padx=20)

        buttons = [
            ("파일 생성", self.create_file, 0, 0),
            ("파일 삭제", self.delete_file, 0, 1),
            ("파일 읽기", self.read_file, 1, 0),
            ("파일 쓰기", self.write_file, 1, 1),
            ("파일 찾기", self.search_file, 2, 0),
            ("폴더 생성", self.create_directory, 3, 0),
            ("폴더 삭제", self.delete_directory, 3, 1),
            ("경로 이동", self.change_directory, 4, 1),
            ("파일/폴더 이동", self.move, 4, 0),
            ("파일/폴더 목록 보기", self.list_directory, 5, 0),
            ("도움말", self.show_help, 6, 0),
            ("종료", self.root.quit, 6, 1),
        ]

        for (text, command, row, column) in buttons:
            button = tk.Button(self.main_menu_frame,
                               text=text, width=20, command=command)
            button.grid(row=row, column=column, pady=5, padx=5, sticky="nsew")

        for column in range(2):
            self.main_menu_frame.grid_columnconfigure(column, weight=1)

    def create_file(self):
        self.open_input_window("파일 생성", self.create_file_operation)

    def delete_file(self):
        self.open_input_window("파일 삭제", self.delete_file_operation)

    def read_file(self):
        self.open_input_window("파일 읽기", self.read_file_operation)

    def write_file(self):
        self.open_input_window("파일 쓰기", self.write_file_operation)

    def search_file(self):
        self.open_input_window("파일 찾기", self.search_file_operation)

    def create_directory(self):
        self.open_input_window("폴더 생성", self.create_directory_operation)

    def delete_directory(self):
        self.open_input_window("폴더 삭제", self.delete_directory_operation)

    def change_directory(self):
        self.open_input_window("경로 이동", self.change_directory_operation)

    def move(self):
        self.open_input_window("파일/폴더 이동", self.move_operation, is_move=True)

    def list_directory(self):
        files = os.listdir(self.current_dir)
        file_list = "\n".join(files)
        messagebox.showinfo(
            "Directory List", f"현재 경로: {self.current_dir}\n{file_list}")

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
exit                            - 프로그램을 종료합니다.
        """
        show_custom_messagebox(root, "도움말", help_text, width=800, height=250)

    def open_input_window(self, title, operation, is_move=False):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=10)

        self.operation = operation

        tk.Label(self.input_frame,
                 text=f"{title} - 파일/디렉토리 이름").grid(row=0, column=0, sticky='w')
        self.name_entry = tk.Entry(self.input_frame, width=50)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        if is_move:
            tk.Label(self.input_frame, text="이동할 경로").grid(
                row=1, column=0, sticky='w')
            self.dest_entry = tk.Entry(self.input_frame, width=50)
            self.dest_entry.grid(row=1, column=1, pady=5, padx=5)

        if title in ["파일 생성", "파일 쓰기"]:
            tk.Label(self.input_frame, text="내용").grid(
                row=2, column=0, sticky='nw')
            self.content_text = tk.Text(self.input_frame, width=50, height=10)
            self.content_text.grid(row=2, column=1, pady=5, padx=5)

        tk.Button(self.input_frame, text="뒤로가기", command=self.create_main_menu).grid(
            row=3, column=0, pady=5)
        tk.Button(self.input_frame, text="완료", command=self.perform_operation).grid(
            row=3, column=1, pady=5, sticky='e')

    def perform_operation(self):
        name = self.name_entry.get()
        content = self.content_text.get("1.0", tk.END) if hasattr(
            self, 'content_text') and self.content_text.winfo_exists() else None
        dest = self.dest_entry.get() if hasattr(
            self, 'dest_entry') and self.dest_entry.winfo_exists() else None

        if name:
            if dest:
                self.operation(name, dest)
            else:
                self.operation(name, content)
            self.create_main_menu()
        else:
            messagebox.showerror("에러", "파일/디렉토리 이름을 입력하세요.")

    def create_file_operation(self, name, content):
        with open(name, 'w') as f:
            f.write(content.strip())
        messagebox.showinfo("성공", f"파일 '{name}'이 생성되었습니다.")

    def delete_file_operation(self, name, _):
        try:
            os.remove(name)
            messagebox.showinfo("성공", f"파일 '{name}'이 삭제되었습니다.")
        except FileNotFoundError:
            messagebox.showerror("에러", f"에러: 파일 '{name}'이 없습니다.")

    def read_file_operation(self, name, _):
        try:
            with open(name, 'r') as f:
                content = f.read()
            messagebox.showinfo(f"파일이름: '{name}'", content)
        except FileNotFoundError:
            messagebox.showerror("에러", f"에러: 파일 '{name}'이 없습니다.")

    def write_file_operation(self, name, content):
        if not os.path.exists(name):
            create_new = messagebox.askyesno(
                "파일이 없습니다", f"파일 '{name}'이 없습니다. 새로 생성하시겠습니까?")
            if create_new:
                with open(name, 'w') as f:
                    f.write(content.strip())
                messagebox.showinfo("성공", f"파일 '{name}'이 생성되었습니다.")
            else:
                messagebox.showinfo("취소", "실행이 취소되었습니다.")
        else:
            with open(name, 'a') as f:
                f.write('\n' + content.strip())
            messagebox.showinfo("성공", f"파일 '{name}'이 수정되었습니다.")

    def create_directory_operation(self, name, _):
        original_dirname = name
        count = 1
        while os.path.exists(name):
            name = f"{original_dirname}({count})"
            count += 1
        os.makedirs(name)
        messagebox.showinfo("성공", f"폴더 '{name}'가 생성되었습니다.")

    def delete_directory_operation(self, name, _):
        try:
            os.rmdir(name)
            messagebox.showinfo("성공", f"폴더 '{name}'가 삭제되었습니다.")
        except FileNotFoundError:
            messagebox.showerror("에러", f"에러: 폴더 '{name}'가 없습니다.")
        except OSError:
            messagebox.showerror("에러", f"에러: 폴더 '{name}'가 비어있지 않습니다.")

    def change_directory_operation(self, name, _):
        try:
            os.chdir(name)
            self.current_dir = os.getcwd()
            messagebox.showinfo("성공", f"'{self.current_dir}'로 이동했습니다.")
        except FileNotFoundError:
            messagebox.showerror("에러", f"에러: 경로 '{name}'가 없습니다.")

    def search_file_operation(self, name, _):
        found = False
        for root, dirs, files in os.walk(self.current_dir):
            if name in files:
                file_path = os.path.join(root, name)
                messagebox.showinfo("성공", f"파일 '{name}'은 '{file_path}'에 있습니다.")
                found = True
                break
        if not found:
            messagebox.showinfo("실패", f"파일 '{name}'을 찾을 수 없습니다.")

    def move_operation(self, src, dest):
        try:
            shutil.move(src, dest)
            messagebox.showinfo("성공", f"'{src}'이 '{dest}'로 이동되었습니다.")
        except FileNotFoundError:
            messagebox.showerror("에러", f"에러: '{src}'가 존재하지 않습니다.")
        except shutil.Error as e:
            messagebox.showerror("에러", f"에러: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSystemSimulatorGUI(root)
    root.mainloop()
