import cv2
import tkinter as tk
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

        # 영상을 3x3 격자 셀에 표시
        for i in range(3):
            for j in range(3):
                number += 1
                apply_effect(canvases[i][j], frame, number)
    window.after(1, update)



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
        canvas.grid(row=i, column=j, padx=5, pady=5)
        canvases[i][j] = canvas

take_photo_button = tk.Button(window, text="Take a Photo", command=take_screenshot)
take_photo_button.grid(row=4, column=1, pady=10)

update()

window.protocol("WM_DELETE_WINDOW", close_windows)
window.resizable(False, False)

window.mainloop()



