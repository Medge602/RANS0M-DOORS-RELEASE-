import os
import sys
import random
import subprocess
import tkinter as tk
import winsound
import threading

URL = "https://youtube.com"
SECONDS = 63  # 1 минута и 3 секунды
CLICKS_NEEDED = 100

# --- УМНЫЙ ПОИСК МУЗЫКИ (В EXE ИЛИ НА РАБОЧЕМ СТОЛЕ) ---
def get_music_path(filename):
    # 1. Если программа запущена как EXE (PyInstaller распаковывает файлы в _MEIPASS)
    if hasattr(sys, '_MEIPASS'):
        exe_path = os.path.join(sys._MEIPASS, filename)
        if os.path.exists(exe_path):
            return exe_path
            
    # 2. Если запущен просто скрипт - ищем на рабочем столе
    paths = [
        os.path.join(os.path.expanduser("~"), "Desktop", filename),
        os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    ]
    return next((p for p in paths if os.path.exists(p)), None)

music_path = get_music_path("popa123.mp4")

# --- ЗАПУСК МУЗЫКИ ---
if music_path:
    os.startfile(music_path)

# --- Главное окно ---
root = tk.Tk()
root.title("RANSOM")
root.resizable(False, False)
root.attributes("-topmost", True)
root.configure(bg="black")

W, H = 650, 420
root.geometry(f"{W}x{H}")

# --- ХОЛСТ ---
canvas = tk.Canvas(root, width=W, height=H, bg="red", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 1. ЧЕРЕП
canvas.create_text(80, 80, text="☠", font=("Segoe UI", 90, "bold"), fill="black")

# 2. ЗАГОЛОВОК
canvas.create_text(400, 50, text="YOUR FILES", fill="white", font=("Courier", 32, "bold"))
canvas.create_text(400, 95, text="HAVE BEEN", fill="white", font=("Courier", 32, "bold"))
canvas.create_text(400, 140, text="ENCRYPTED", fill="white", font=("Courier", 32, "bold"))

# 3. ЧЕРНАЯ ПЛАШКА С ТЕКСТОМ
canvas.create_rectangle(10, 180, 640, 250, fill="black", outline="white", width=2)
canvas.create_text(325, 200, text="IF YOU DO NOT PAY THIS RANSOM BY THE END", fill="white", font=("Courier", 11, "bold"))
canvas.create_text(325, 220, text="OF THE TIMER, YOUR FILES WILL BE", fill="white", font=("Courier", 11, "bold"))
canvas.create_text(325, 240, text="UNRECOVERABLE BY ANY MEANS.", fill="white", font=("Courier", 11, "bold"))

# 4. НИЖНЯЯ ПАНЕЛЬ
# Блок с 500
canvas.create_rectangle(10, 260, 240, 350, fill="black", outline="white", width=2)
canvas.create_text(60, 305, text="500", fill="yellow", font=("Courier", 36, "bold"))

# МОНЕТА (объемная)
coin_cx, coin_cy = 150, 305
coin_r = 25
canvas.create_oval(coin_cx-coin_r-2, coin_cy-coin_r-2, coin_cx+coin_r-2, coin_cy+coin_r-2, fill="#B8860B", outline="")
canvas.create_oval(coin_cx-coin_r, coin_cy-coin_r, coin_cx+coin_r, coin_cy+coin_r, fill="#FFD700", outline="#8B6508", width=3)
canvas.create_oval(coin_cx-coin_r+5, coin_cy-coin_r+5, coin_cx+coin_r-5, coin_cy+coin_r-5, fill="#FFC107", outline="#8B6508", width=1)
canvas.create_text(coin_cx, coin_cy, text="$", fill="#8B6508", font=("Segoe UI", 20, "bold"))

# Блок с таймером
canvas.create_rectangle(250, 260, 640, 350, fill="black", outline="white", width=2)
canvas.create_text(270, 305, text="TIME:", fill="red", font=("Courier", 36, "bold"), anchor="w")
# Стартовое значение таймера (01:03)
timer_text = canvas.create_text(430, 305, text="01:03", fill="red", font=("Courier", 36, "bold"), anchor="w")

# 5. СЧЕТЧИК КЛИКОВ
click_text = canvas.create_text(325, 380, text="КЛИКИ: 0 / 100", fill="yellow", font=("Courier", 16, "bold"))

# --- ЛОГИКА ---
clicks = 0
remaining = SECONDS
won = False
dragging = False

root.update_idletasks()
pos_x = root.winfo_x()
pos_y = root.winfo_y()
win_w = root.winfo_width()
win_h = root.winfo_height()
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

def on_press(event): global dragging; dragging = True
def on_release(event):
    global dragging, pos_x, pos_y
    dragging = False
    pos_x = root.winfo_x()
    pos_y = root.winfo_y()

root.bind("<ButtonPress-1>", on_press, add="+")
root.bind("<ButtonRelease-1>", on_release, add="+")

def jitter():
    global pos_x, pos_y
    if won: return
    if dragging:
        root.after(150, jitter)
        return
    dx = random.choice([-6, -5, -4, -3, 3, 4, 5, 6])
    dy = random.choice([-6, -5, -4, -3, 3, 4, 5, 6])
    new_x = max(0, min(screen_w - win_w, pos_x + dx))
    new_y = max(0, min(screen_h - win_h, pos_y + dy))
    root.geometry(f"+{new_x}+{new_y}")
    root.after(random.randint(30, 80), lambda: root.geometry(f"+{pos_x}+{pos_y}"))
    root.after(random.randint(400, 900), jitter)

def stop_music():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    players = ["wmplayer.exe", "Video.UI.exe", "Music.UI.exe", "vlc.exe", "mpc-hc64.exe", "PotPlayerMini64.exe"]
    for player in players:
        subprocess.run(["taskkill", "/F", "/IM", player], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)

def tick():
    global remaining
    if won: return
    remaining -= 1
    if remaining > 0:
        m, s = divmod(remaining, 60)
        canvas.itemconfig(timer_text, text=f"{m:02d}:{s:02d}")
        root.after(1000, tick)
    else:
        canvas.itemconfig(timer_text, text="00:00")
        stop_music()
        root.destroy()
        subprocess.Popen(["cmd", "/c", "start", "chrome", URL])

def on_click(event):
    global clicks, won
    if (coin_cx - coin_r) < event.x < (coin_cx + coin_r) and (coin_cy - coin_r) < event.y < (coin_cy + coin_r):
        if won: return
        threading.Thread(target=lambda: winsound.Beep(1500, 30), daemon=True).start()
        clicks += 1
        canvas.itemconfig(click_text, text=f"КЛИКИ: {clicks} / {CLICKS_NEEDED}")
        
        if clicks >= CLICKS_NEEDED:
            won = True
            stop_music()
            show_thanks()
            root.withdraw()

canvas.bind("<Button-1>", on_click)

# --- ОКНО БЛАГОДАРНОСТИ ---
def show_thanks():
    thanks = tk.Toplevel(root)
    thanks.title("Thanks")
    thanks.geometry("400x300")
    thanks.configure(bg="green")
    thanks.resizable(False, False)
    thanks.attributes("-topmost", True)
    
    canvas_t = tk.Canvas(thanks, width=400, height=300, bg="green", highlightthickness=0)
    canvas_t.pack(fill="both", expand=True)
    
    # Лайк
    canvas_t.create_rectangle(150, 130, 190, 210, fill="white", outline="white")
    canvas_t.create_polygon(150, 130, 150, 100, 165, 90, 185, 95, 190, 130, fill="white", outline="white")
    canvas_t.create_rectangle(190, 130, 260, 150, fill="white", outline="white")
    canvas_t.create_rectangle(190, 155, 255, 175, fill="white", outline="white")
    canvas_t.create_rectangle(190, 180, 250, 200, fill="white", outline="white")
    canvas_t.create_rectangle(150, 210, 190, 225, fill="white", outline="white")
    
    canvas_t.create_text(200, 260, text="THANKS FOR PAYING", fill="white", font=("Segoe UI", 22, "bold"))
    
    thanks.after(3000, thanks.destroy)

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.after(1000, tick)
root.after(500, jitter)
root.mainloop()