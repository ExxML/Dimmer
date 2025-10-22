<div align="center">

<img src="public/Dimmer.ico" alt="Dimmer Icon" width="128" height="128"> 

# Dimmer

### A minimalistic screen dimmer for Windows

*Reduce eye strain and create the perfect ambiance with a simple, elegant screen overlay*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.9.1-green.svg)](https://pypi.org/project/PyQt6/)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-royalblue.svg)](https://www.microsoft.com/en-us/windows)

[✨ Features](#-features) • [📖 Usage](#-usage) • [🚀 Installation](#-installation) • [🖼️ Preview](#-preview)

</div>

---

## ✨ Features

- **🖥️ Full-Screen Dimming** - Creates a semi-transparent overlay that dims your entire screen

- **🎛️ Intuitive Controls** - Easy-to-use slider with real-time percentage display (0-100%)

- **💾 Persistent Settings** - Automatically saves and restores your preferred opacity level

- **📱 System Tray Integration** - Minimize to system tray for unobtrusive operation

- **👁️ Colour Accuracy** - Excludes tint overlay from screen captures

- **🎨 Minimalistic UI** - Clean dark theme UI with smooth graphics

- **⚡ Lightweight** - Minimal resource usage with optimized performance

## 📖 Usage

1. Run the application by  downloading the .exe in [Releases](https://github.com/ExxML/Dimmer/releases) or [manually installing the project](#-installation)

2. Adjust opacity using the slider (0% = no dimming, 100% = maximum dimming)

3. Hide the app window by clicking the minimize button

4. Show the app window by clicking the tray icon

5. Close the application by clicking the X button or quit via the system tray menu

6. *[Optional]* Set up auto-run on startup:
   - Create a shortcut for `app.exe`
   - Move the shortcut to the Startup folder (press `Win + R` and type `shell:startup`)

## 🚀 Installation

### Prerequisites
- Windows 10 or 11
- Python 3.10+

### Quick Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/dimmer.git
   cd dimmer
   ```

2. Create virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python src/app.py
   ```

## 🖼️ Preview

### App Interface

![Dimmer Interface](./public/Dimmer_Preview.png)

## 📁 Project Structure
```
dimmer/
├── src/
│   ├── app.py               # Main application and UI
│   └── overlay.py           # Screen overlay implementation
├── config/
│   └── opacity_config.json  # Persistent settings
├── public/
│   └── Dimmer.ico           # Application icon
└── requirements.txt         # Python dependencies
```

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
   <h4>🩵 Gentle screen dimming for visual comfort 🩵</h4>
</div>

