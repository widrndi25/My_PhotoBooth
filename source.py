import tkinter as tk
from PIL import Image, ImageTk, ImageGrab


def take_screenshot():
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    width = window.winfo_width()
    height = window.winfo_height()

    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot.save("screenshot.png")


def close_windows():
    cap.release()
    window.destroy()
window = tk.Tk()
window.title("나만의 포토 부스")
window.geometry("880x680")
window.protocol("WM_DELETE_WINDOW", close_windows)
window.resizable(False, False)

take_photo_button = tk.Button(window, text="Take a Photo", command=take_screenshot)
take_photo_button.grid(row=4, column=1, pady=10)

window.mainloop()



