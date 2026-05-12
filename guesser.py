import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
from rapidocr_onnxruntime import RapidOCR
import cv2
import numpy as np
import mss
import keyboard
import os
import re

# Initialize OCR
ocr = RapidOCR()

class RegionSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-fullscreen', True)
        self.root.attributes("-topmost", True)
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        # Instruction text on the screen
        self.canvas.create_text(self.root.winfo_screenwidth()//2, 100, 
                                text="1. Draw box over MIN number", 
                                font=("Consolas", 32, "bold"), fill="yellow", tags="instruction")
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.selections = []

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        
        # Avoid accidental clicks
        if abs(end_x - self.start_x) < 5 or abs(end_y - self.start_y) < 5:
            return
            
        region = (min(self.start_x, end_x), min(self.start_y, end_y), 
                  max(self.start_x, end_x), max(self.start_y, end_y))
        self.selections.append(region)
        
        # Turn the completed rectangle green
        self.canvas.itemconfig(self.rect, outline="green")
        self.rect = None
        
        if len(self.selections) == 1:
            self.canvas.itemconfig("instruction", text="2. Draw box over MAX number")
        elif len(self.selections) == 2:
            self.root.destroy()

    def get_selection(self):
        self.root.mainloop()
        return self.selections

def preprocess_image(img):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    # Thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def get_numbers_from_screen(region):
    with mss.mss() as sct:
        monitor = {"top": region[1], "left": region[0], "width": region[2]-region[0], "height": region[3]-region[1]}
        img = sct.grab(monitor)
        img_np = np.array(img)
        img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGRA2RGB)
        
        # --- RapidOCR Preprocessing ---
        # RapidOCR is extremely smart and handles complex fonts and backgrounds naturally.
        # We just need to scale the image up slightly to help it see tiny game fonts.
        scaled = cv2.resize(img_rgb, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        # Run OCR
        result, _ = ocr(scaled)
        
        text = ""
        if result:
            for line in result:
                text += line[1] + " "
        
        # Extract numbers using regex
        nums = re.findall(r'\d+', text)
        return [int(n) for n in nums]

def main():
    print("=== OCR Binary Search Guesser ===")
    selector = RegionSelector()
    regions = selector.get_selection()
    
    if len(regions) < 2:
        print("Not enough regions selected. Exiting.")
        return

    region_min = regions[0]
    region_max = regions[1]
    
    # --- Overlay UI ---
    overlay = tk.Tk()
    overlay.title("OCR Guesser Overlay")
    overlay.attributes("-topmost", True)
    overlay.attributes("-alpha", 0.85)
    overlay.overrideredirect(True) # Remove window borders
    overlay.geometry("+20+20") # Spawn at top-left
    overlay.configure(bg='#1e1e1e')
    
    label = tk.Label(overlay, text="Ready. Press F9 to guess.\nPress ESC to exit.", 
                     font=("Consolas", 14, "bold"), fg="#00FF00", bg="#1e1e1e", justify="left")
    label.pack(padx=15, pady=10)

    # Variables for drag functionality
    drag_data = {"x": 0, "y": 0}

    def start_drag(event):
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def drag(event):
        deltax = event.x - drag_data["x"]
        deltay = event.y - drag_data["y"]
        x = overlay.winfo_x() + deltax
        y = overlay.winfo_y() + deltay
        overlay.geometry(f"+{x}+{y}")

    overlay.bind("<ButtonPress-1>", start_drag)
    overlay.bind("<B1-Motion>", drag)

    def process_guess():
        try:
            nums_min = get_numbers_from_screen(region_min)
            nums_max = get_numbers_from_screen(region_max)
            
            if nums_min and nums_max:
                low = nums_min[0]
                high = nums_max[0]
                
                mid = (low + high) / 2
                if mid.is_integer():
                    guess_str = str(int(mid))
                else:
                    guess_str = f"{int(mid)} or {int(mid) + 1}"
                    
                label.config(text=f"Detected: {low} - {high}\nSuggest: {guess_str}")
            else:
                label.config(text=f"Failed to read.\nMin: {nums_min}, Max: {nums_max}")
        except Exception as e:
            label.config(text=f"Error: {e}")

    def on_f9():
        overlay.after(0, process_guess)
        
    def on_esc():
        overlay.after(0, overlay.destroy)
        os._exit(0)

    keyboard.add_hotkey('f9', on_f9)
    keyboard.add_hotkey('esc', on_esc)

    overlay.mainloop()

if __name__ == "__main__":
    main()
