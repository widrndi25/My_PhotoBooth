import tkinter as tk
def close_windows():
    cap.release()
    window.destroy()
window = tk.Tk()
window.title("나만의 포토 부스")
window.geometry("880x680")
window.protocol("WM_DELETE_WINDOW", close_windows)
window.resizable(False, False)

# GUI 시작
window.mainloop()
