import tkinter as tk
import random
import math


WIDTH, HEIGHT = 800, 500
BG_COLOR = "#fff0f6"
FLOWER_EMOJIS = ["🌸", "🌷", "🌹", "🌼", "💐"]
HEARTS = ["💖", "💗", "💞"]


root = tk.Tk()
root.title("Chúc mừng 20/10 🌸")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
canvas.pack()


message_full = "💐 Chúc mừng ngày Phụ nữ Việt Nam 20/10! Chúc các chị em luôn xinh đẹp, hạnh phúc và thành công! 💐"
message_item = None


falling = []
def create_flower():
    x = random.randint(0, WIDTH)
    emoji = random.choice(FLOWER_EMOJIS)
    size = random.randint(16, 28)
    item = canvas.create_text(x, -20, text=emoji, font=("Arial", size))
    speed = random.uniform(1.0, 3.0)
    falling.append((item, speed))
    # tạo tiếp ngẫu nhiên
    root.after(random.randint(300, 700), create_flower)

def animate_flowers():
    for (item, speed) in list(falling):
        canvas.move(item, 0, speed)
        x, y = canvas.coords(item)
        if y > HEIGHT + 20:
            
            canvas.coords(item, random.randint(0, WIDTH), -20)
    root.after(30, animate_flowers)



gift_x, gift_y = WIDTH//2, HEIGHT - 110
gift = canvas.create_text(gift_x, gift_y, text="🎁", font=("Arial", 44))
gift_label = canvas.create_text(gift_x, gift_y + 50, text="Nhấn để nhận lời chúc", font=("Arial", 12), fill="#a3135a")


glow = canvas.create_oval(gift_x-60, gift_y-60, gift_x+60, gift_y+60, outline="", fill="#ffd9ec")


typing_index = 0
typing_speed = 30  
particles = []  

def show_typing_message():
    global message_item, typing_index
   
    if message_item is None:
        message_item = canvas.create_text(WIDTH//2, HEIGHT//2 - 10, text="", font=("Arial", 18, "bold"), fill="#e91e63", width=600, justify="center")
    typing_index = 0
    canvas.itemconfig(message_item, text="")
    spawn_particles()
    type_next_char()

def type_next_char():
    global typing_index
    if typing_index <= len(message_full):
        text_now = message_full[:typing_index]
        canvas.itemconfig(message_item, text=text_now)
        typing_index += 1
        root.after(typing_speed, type_next_char)
    else:
        
        w = canvas.itemcget(message_item, "font")
        
        pulse_text(0)

def pulse_text(step):

    if step < 8:
        t = int(0 + step * (255-233)/8)
        color = f"#{233+t:02x}{30+t:02x}{99+t:02x}"
        canvas.itemconfig(message_item, fill=color)
        root.after(80, lambda: pulse_text(step+1))
    else:
        canvas.itemconfig(message_item, fill="#e91e63")


def spawn_particles(n=12):
    
    for i in range(n):
        angle = 2*math.pi * i / n
        dist = random.randint(40, 70)
        px = gift_x + math.cos(angle) * (dist + random.randint(-10,10))
        py = gift_y + math.sin(angle) * (dist + random.randint(-10,10))
        emoji = random.choice(HEARTS + FLOWER_EMOJIS)
        size = random.randint(12, 22)
        itm = canvas.create_text(px, py, text=emoji, font=("Arial", size))
        particles.append({
            "id": itm,
            "angle": angle,
            "radius": dist,
            "speed": random.uniform(0.02, 0.07),
            "grow": random.uniform(0.2, 0.6)
        })
    animate_particles()

def animate_particles():
    for p in particles[:]:
        
        p["angle"] += p["speed"]
        p["radius"] += p["grow"]
        x = gift_x + math.cos(p["angle"]) * p["radius"]
        y = gift_y + math.sin(p["angle"]) * p["radius"]
        canvas.coords(p["id"], x, y)
        
        cur_font = int(canvas.itemcget(p["id"], "font").split()[1]) if " " in canvas.itemcget(p["id"], "font") else 14
        new_font = max(6, cur_font - 0.1)
        canvas.itemconfig(p["id"], font=("Arial", int(new_font)))
        
        if p["radius"] > 250:
            canvas.delete(p["id"])
            particles.remove(p)
    if particles:
        root.after(30, animate_particles)


glow_anim_step = 0
def animate_glow():
    global glow_anim_step
    # pulse effect: expand & fade
    s = 1 + 0.02 * math.sin(glow_anim_step / 6)
    r = 60 + 10 * math.sin(glow_anim_step / 4)
    alpha = int(180 + 50 * math.sin(glow_anim_step / 5))
    
    color = f"#ffd9{(200 + (alpha % 55)):02x}"
    canvas.coords(glow, gift_x-r, gift_y-r, gift_x+r, gift_y+r)
    try:
        canvas.itemconfig(glow, fill=color)
    except:
        pass
    glow_anim_step += 1
    root.after(60, animate_glow)


def on_click(event):
   
    dx = event.x - gift_x
    dy = event.y - gift_y
    if dx*dx + dy*dy <= 80*80:  
        show_typing_message()

canvas.bind("<Button-1>", on_click)

# --------- KHỞI CHẠY ----------
create_flower()
animate_flowers()
animate_glow()


hint = canvas.create_text(10, HEIGHT-10, anchor="w", text="Nhấn vào hộp quà 🎁 để nhận lời chúc 💌", font=("Arial", 10), fill="#8c0066")

root.mainloop()
