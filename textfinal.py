import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
from tkinter import font
from PIL import Image, ImageDraw, ImageTk, ImageFont

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        # 기본 설정 (이미지 크기, 색상, 펜 타입 등)
        self.image = Image.new("RGBA", (500, 700), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.last_x, self.last_y = None, None
        self.shape = "pen"  # 기본 도형은 펜
        self.pen_color = "black"
        self.text_color = "black"
        self.stroke = 5
        self.pen_type = "기본"

        # 캔버스 생성 및 이미지 표시 설정
        self.canvas = tk.Canvas(self.root, width=500, height=700)
        self.canvas.pack()
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas_image, anchor=tk.NW)

        # UI 버튼 생성
        self.create_buttons()

        # 마우스 이벤트 처리 (클릭, 드래그)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        # 텍스트를 위한 리스트
        self.text_boxes = []  # 텍스트 상자 목록 초기화

    def create_buttons(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill=tk.X)

        buttons = [
            ("펜", self.toggle_pen_menu),
            ("지우개", self.set_eraser),
            ("펜 색상", self.choose_pen_color),
            ("텍스트 색상", self.choose_text_color),
            ("텍스트", self.add_text),
            ("전체 지우기", self.clear_canvas),
            ("저장", self.save_image),
        ]
        for i, (text, command) in enumerate(buttons):
            tk.Button(self.menu_frame, text=text, command=command).grid(row=0, column=i)

        self.stroke_label = tk.Label(self.menu_frame, text="선 굵기:")
        self.stroke_label.grid(row=0, column=8, sticky="w")
        self.stroke_scale = tk.Scale(self.menu_frame, from_=1, to=20, orient=tk.HORIZONTAL)
        self.stroke_scale.set(self.stroke)
        self.stroke_scale.grid(row=0, column=9)

        self.font_size_label = tk.Label(self.menu_frame, text="텍스트 크기:")
        self.font_size_label.grid(row=0, column=10, sticky="w")
        self.font_size_scale = tk.Scale(self.menu_frame, from_=1, to_=100, orient=tk.HORIZONTAL)
        self.font_size_scale.set(20)
        self.font_size_scale.grid(row=0, column=11)

    def toggle_pen_menu(self):
        pen_types = ["기본", "두껍게", "가늘게", "점선"]
        pen_type_menu = tk.Menu(self.root, tearoff=0)
        for pen_type in pen_types:
            pen_type_menu.add_command(label=pen_type, command=lambda pt=pen_type: self.set_pen_type(pt))
        pen_type_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def set_pen_type(self, pen_type):
        self.pen_type = pen_type
        if pen_type == "기본":
            self.stroke = 5
        elif pen_type == "두껍게":
            self.stroke = 10
        elif pen_type == "가늘게":
            self.stroke = 1
        elif pen_type == "점선":
            self.stroke = 5
        print(f"현재 선택된 펜 종류: {pen_type} / 굵기: {self.stroke}")

    def set_eraser(self):
        self.shape = "eraser"
        print("지우개 활성화됨")

    def choose_pen_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_color = color

    def on_click(self, event):
        self.last_x, self.last_y = event.x, event.y

    def on_drag(self, event):
        if self.shape == "pen":
            pen_width = self.stroke
            if self.pen_type in ["기본", "두껍게"]:
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color, width=pen_width)
            elif self.pen_type == "가늘게":
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color, width=1)
            elif self.pen_type == "점선":
                self.draw_dotted_line(self.last_x, self.last_y, event.x, event.y)

            self.update_canvas_image()
            self.last_x, self.last_y = event.x, event.y
        elif self.shape == "eraser":
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill="white", width=self.stroke)
            self.update_canvas_image()
            self.last_x, self.last_y = event.x, event.y

    def draw_dotted_line(self, x1, y1, x2, y2):
        step = 10
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        for i in range(0, int(distance / step)):
            start_x = x1 + (i * step) * (x2 - x1) / distance
            start_y = y1 + (i * step) * (y2 - y1) / distance
            end_x = x1 + ((i + 1) * step) * (x2 - x1) / distance
            end_y = y1 + ((i + 1) * step) * (y2 - y1) / distance
            self.draw.line([(start_x, start_y), (end_x, end_y)], fill=self.pen_color, width=self.stroke)

    def update_canvas_image(self):
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas_image, anchor=tk.NW)

    def add_text(self):
        text = simpledialog.askstring("텍스트 입력", "추가할 텍스트 입력:")
        if text:
            x = simpledialog.askinteger("X 좌표", "텍스트의 X 좌표 입력 (0~500):")
            y = simpledialog.askinteger("Y 좌표", "텍스트의 Y 좌표 입력 (0~700):")
            font_size = self.font_size_scale.get()

            # 한글 폰트 설정 (필요시 폰트 경로 수정)
            try:
                font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows에서 '맑은 고딕' 경로
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                font = ImageFont.load_default()  # 기본 폰트 사용

            # 텍스트를 canvas에 추가
            self.canvas.create_text(x, y, text=text, fill=self.text_color, font=("Arial", font_size))

            # 텍스트를 image에도 반영 (이미지에 그리기)
            draw = ImageDraw.Draw(self.image)
            draw.text((x, y), text, fill=self.text_color, font=font)  # 폰트 크기 설정

            self.update_canvas_image()

    def clear_canvas(self):
        self.image = Image.new("RGBA", (500, 700), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.delete("all")  # 캔버스의 모든 위젯 삭제
        self.update_canvas_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
