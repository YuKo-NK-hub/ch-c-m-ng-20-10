import tkinter as tk
import random
import time


root = tk.Tk()
root.title("Chúc mừng 20/10 🌸")
root.geometry("600x400")
root.config(bg="#ffe6f0")

canvas = tk.Canvas(root, width=600, height=400, bg="#ffe6f0", highlightthickness=0)
canvas.pack(fill="both", expand=True)


message = "💐 Chúc mừng ngày Phụ nữ Việt Nam 20/10 💖\nChúc các chị em luôn xinh đẹp, hạnh phúc và thành công!"
text = canvas.create_text(300, 200, text=message, font=("Arial", 14, "bold"), fill="#e91e63", justify="center")


flowers = ["🌸", "🌷", "🌹", "🌼", "💐"]

falling_flowers = []


def create_flower():
    x = random.randint(0, 600)
    flower = canvas.create_text(x, 0, text=random.choice(flowers), font=("Arial", 18))
    falling_flowers.append(flower)
    root.after(random.randint(300, 800), create_flower)  # tạo hoa liên tục


def animate():
    for flower in falling_flowers:
        canvas.move(flower, 0, 3)
        pos = canvas.coords(flower)
        if pos[1] > 400:
            canvas.move(flower, 0, -400)  
    root.after(50, animate)


def fade_in(alpha=0):
    color = f"#{int(255 - alpha):02x}{int(102 + alpha/2):02x}{int(150 + alpha/3):02x}"
    canvas.itemconfig(text, fill=color)
    if alpha < 255:
        root.after(30, lambda: fade_in(alpha + 5))


create_flower()
animate()
fade_in()

root.mainloop()
