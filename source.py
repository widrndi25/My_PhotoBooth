import cv2
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImageGrab


def take_screenshot():
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    width = window.winfo_width()
    height = window.winfo_height()

    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot.save("screenshot.png")


def update():
    ret, frame = cap.read()

    number = 0;
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        for i in range(3):
            for j in range(3):
                number += 1
                apply_effect(canvases[i][j], frame, number)
    window.after(1, update)


def apply_effect(canvas, frame, canvas_number):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    resized_frame = cv2.resize(frame, (canvas_width, canvas_height))
    resized_frame = cv2.flip(resized_frame, 1)

    gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    effect_name = {
        1: "흑백",
        2: "스케치(BLACK)",
        3: "브라운관",
        4: "스케치(WHITE)",
        5: "원본",
        6: "컬러 반전",
        7: "모자이크",
        8: "만화",
        9: "상하 반전",

    }

    if canvas_number == 1:
        img = Image.fromarray(gray)

    elif canvas_number == 2:
        edges = cv2.Canny(gray, 100, 200)
        img = Image.fromarray(edges)

    if canvas_number == 3:  # 볼록 렌즈 효과
        height, width = resized_frame.shape[:2]
        center_x, center_y = width // 2, height // 2

        max_dist = np.sqrt(center_x ** 2 + center_y ** 2)
        bulge_amount = 0.00001
        bulge_radius = max_dist * 1.5

        new_image = np.zeros(resized_frame.shape, dtype=resized_frame.dtype)

        for y in range(height):
            for x in range(width):
                offset_x, offset_y = x - center_x, y - center_y
                r = np.sqrt(offset_x ** 2 + offset_y ** 2)
                theta = np.arctan2(offset_y, offset_x)

                if r < bulge_radius:
                    new_r = r + bulge_amount * r ** 3
                    new_x = int(center_x + new_r * np.cos(theta))
                    new_y = int(center_y + new_r * np.sin(theta))

                    if 0 <= new_x < width and 0 <= new_y < height:
                        canvas_x = int((new_x / width) * canvas_width)
                        canvas_y = int((new_y / height) * canvas_height)
                        new_image[y, x] = resized_frame[canvas_y, canvas_x]

        new_image = cv2.resize(new_image, (canvas_width, canvas_height))

        img = Image.fromarray(new_image)

    elif canvas_number == 4:
        edges = cv2.Canny(gray, 100, 200)
        ret, img = cv2.threshold(edges, 70, 255, cv2.THRESH_BINARY_INV)
        img = Image.fromarray(img)

    elif canvas_number == 5:
        apply_original(canvas, frame, canvas_number)
        img = Image.fromarray(resized_frame)

    elif canvas_number == 6:
        img = cv2.bitwise_not(resized_frame)
        img = Image.fromarray(img)

    elif canvas_number == 7:
        img = cv2.resize(resized_frame, (20, 20), interpolation=cv2.INTER_AREA)
        img = cv2.resize(img, (canvas_width, canvas_height), interpolation=cv2.INTER_AREA)
        img = Image.fromarray(img)

    elif canvas_number == 8:
        img_gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray, 5)
        edges = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(resized_frame, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        img = Image.fromarray(cartoon)

    elif canvas_number == 9:
        img = cv2.flip(resized_frame, 0)
        img = Image.fromarray(img)

    img_tk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.img = img_tk  # 이미지 객체 유지

    text = f"{effect_name.get(canvas_number, 'Custom Effect')}"
    text_size = 18
    text_font = ("Helvetica", text_size)
    text_x = canvas_width / 2
    text_y = canvas_height - 15

    canvas.create_text(text_x, text_y, text=text, font=text_font, fill='black' if canvas_number == 4 else 'white')


def apply_original(canvas, frame, canvas_number):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    resized_frame = cv2.resize(frame, (canvas_width, canvas_height))
    resized_frame = cv2.flip(resized_frame, 1)

    img = Image.fromarray(resized_frame)
    img_tk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.img = img_tk  # 이미지 객체 유지

    canvas.create_text(10, canvas_height - 10, text=f"Canvas {canvas_number}", anchor=tk.W, fill='white')


def close_windows():
    cap.release()
    window.destroy()


cap = cv2.VideoCapture(1)

window = tk.Tk()
window.title("나만의 포토 부스")
window.geometry("880x680")

canvases = [[None] * 3 for _ in range(3)]
for i in range(3):
    for j in range(3):
        canvas = tk.Canvas(window, highlightthickness=0)
        canvas.grid(row=i, column=j, padx=5, pady=5)  # 셀 간 여백 설정
        canvases[i][j] = canvas


take_photo_button = tk.Button(window, text="Take a Photo", command=take_screenshot)
take_photo_button.grid(row=4, column=1, pady=10)

update()

window.protocol("WM_DELETE_WINDOW", close_windows)
window.resizable(False, False)

window.mainloop()