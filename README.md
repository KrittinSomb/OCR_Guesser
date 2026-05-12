# OCR Binary Search Guesser

An automated utility designed to assist in "Binary Search" style games or tasks by reading numerical ranges (Min - Max) directly from the screen using Optical Character Recognition (OCR).

## Key Features
- **Two-Step Region Selection:** Precisely define the exact locations of the Minimum and Maximum numbers for flawless reading.
- **Accurate & Lightweight OCR:** Leverages RapidOCR (ONNX) for ultra-fast, robust digit recognition without requiring external executable installations.
- **Real-time Overlay:** Instantly calculates the optimal binary search guess and displays it on a transparent, draggable on-screen overlay.
- **High Performance:** Utilizes the `mss` library for rapid screen capturing with minimal latency.

## Prerequisites
- **Python 3.x**
- No external programs required! Everything runs entirely self-contained via Python packages.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/OCR_Guesser.git
   cd OCR_Guesser
   ```

2. **Install dependencies (Windows):**
   Simply double-click `setup.bat`. This will automatically create an isolated Python virtual environment (`venv`) and install all required libraries safely.

## Usage

1. **Start the Application:**
   Double-click `run.bat` to launch the script. The terminal will start minimized automatically.
   
2. **Select the Target Areas:** 
   - The screen will dim and display instructions. 
   - Draw a box over the **MIN** number. The box will turn green to lock in.
   - Draw a second box over the **MAX** number.
   
3. **Operations:**
   - A transparent overlay will appear on your screen. You can drag it to any convenient position.
   - **Press F9:** Triggers the OCR to read the numbers from your selected regions and instantly updates the overlay with the mathematically optimal guess.
   - **Press ESC:** Safely closes the overlay and exits the application.

## Tech Stack
- **Python**
- **RapidOCR (ONNX):** Lightweight, high-accuracy OCR Engine powered by PaddleOCR models.
- **OpenCV:** Image pre-processing and scaling.
- **MSS:** High-speed screen capture.
- **Tkinter:** Transparent UI overlay and interactive region selection tool.
