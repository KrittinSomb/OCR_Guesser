# OCR Binary Search Guesser

An automated utility designed to assist in "Binary Search" style games or tasks by reading numerical ranges (Min - Max) directly from the screen using Optical Character Recognition (OCR).

## Key Features
- **Interactive Region Selection:** Easily define the screen area to monitor with a drag-and-drop selector.
- **Accurate OCR:** Leverages Tesseract OCR with custom pre-processing for reliable digit recognition.
- **Real-time Calculation:** Instantly calculates the optimal binary search guess (Midpoint) at the press of a hotkey.
- **High Performance:** Utilizes the `mss` library for rapid screen capturing with minimal latency.

## Prerequisites
- **Python 3.x**
- **Tesseract OCR:** Must be installed on your system.
  - [Download Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
  - *Note: If Tesseract is not in your system PATH, you may need to uncomment and set the path in `guesser.py`.*

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/OCR_Guesser.git
   cd OCR_Guesser
   ```

2. **Install dependencies:**
   - On Windows, you can run:
     ```bash
     setup.bat
     ```
   - Or install manually via pip:
     ```bash
     pip install -r requirements.txt
     ```

## Usage

1. **Start the Application:**
   ```bash
   python guesser.py
   ```
2. **Select the Target Area:** The screen will dim. Click and drag to highlight the region where the "Min" and "Max" numbers appear.
3. **Operations:**
   - **Press F9:** Triggers the OCR to read the numbers and print the suggested guess in the console.
   - **Press ESC:** Safely exits the application.

## Tech Stack
- **Python**
- **PyTesseract:** OCR Engine.
- **OpenCV:** Image pre-processing (Grayscale & Thresholding).
- **MSS:** Efficient screen capture.
- **Tkinter:** Transparent overlay for region selection.
