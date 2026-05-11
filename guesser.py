import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
import pytesseract
import cv2
import numpy as np
import mss
import keyboard
import os
import re

# --- CONFIGURATION ---
# If tesseract is not in your PATH, uncomment and set the path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class RegionSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-fullscreen', True)
        self.root.attributes("-topmost", True)
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.selection = None

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
        self.selection = (min(self.start_x, end_x), min(self.start_y, end_y), 
                          max(self.start_x, end_x), max(self.start_y, end_y))
        self.root.destroy()

    def get_selection(self):
        self.root.mainloop()
        return self.selection

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
        # Convert BGRA to RGB
        img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGRA2RGB)
        
        processed = preprocess_image(img_rgb)
        text = pytesseract.image_to_string(processed, config='--psm 6 digits')
        # Extract numbers using regex
        nums = re.findall(r'\d+', text)
        return [int(n) for n in nums]

def main():
    print("=== OCR Binary Search Guesser ===")
    print("1. Please select the region where the numbers (min - max) are displayed.")
    selector = RegionSelector()
    region = selector.get_selection()
    
    if not region:
        print("No region selected. Exiting.")
        return

    print(f"Region selected: {region}")
    print("Press F9 to capture and calculate the next guess.")
    print("Press ESC to exit.")

    while True:
        if keyboard.is_pressed('f9'):
            try:
                nums = get_numbers_from_screen(region)
                if len(nums) >= 2:
                    low = min(nums)
                    high = max(nums)
                    guess = (low + high) // 2
                    print(f"Detected: {low} - {high} | Suggest Guess: {guess}")
                else:
                    print(f"Could not find enough numbers. Detected: {nums}")
            except Exception as e:
                print(f"Error: {e}")
            
            # Wait a bit to prevent multiple triggers
            keyboard.wait('f9', trigger_on_release=True)
            
        if keyboard.is_pressed('esc'):
            break

if __name__ == "__main__":
    main()
