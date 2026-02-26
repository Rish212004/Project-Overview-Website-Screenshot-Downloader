# 📸 Website Screenshot Downloader

> Batch download website screenshots from a CSV/Excel file with a simple GUI interface.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🎯 Overview

**Website Screenshot Downloader** is a Python automation tool that captures full-page screenshots of websites in bulk. Perfect for competitive analysis, web design research, SEO audits, and dataset creation.

### Key Features

- ✅ **Batch Processing** - Download 100s of screenshots automatically
- 📊 **CSV/Excel Support** - Works with both file formats
- ⚡ **Optimized Speed** - Headless Chrome with performance tweaks
- 🖼️ **Quality Preservation** - High-quality PNG screenshots
- 🎨 **Smart Naming** - Custom filenames or auto-generated names
- 📈 **Live Progress** - Real-time GUI progress tracker
- 💾 **Organized Output** - Auto-organized folder structure
- ✔️ **Validation** - Detects blank/failed screenshots

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Use Cases](#use-cases)
- [Contributing](#contributing)

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install selenium pandas openpyxl webdriver-manager
```

### 2. Ensure Chrome is Installed

```bash
# macOS
brew install --cask google-chrome

# Ubuntu/Debian
sudo apt-get install google-chrome-stable

# Windows
# Download from https://google.com/chrome
```

### 3. Prepare Your CSV File

```csv
url,filename
https://google.com,Google
https://github.com,GitHub
https://stackoverflow.com,Stack Overflow
```

## ⚡ Quick Start

### Step 1: Run the Script

```bash
python screenshot_downloader.py
```

### Step 2: Select Your File

A GUI window will open. Click **"📁 Select CSV/Excel File"** and choose your file.

### Step 3: Confirm & Wait

Confirm the download and watch the progress tracker. Screenshots will be saved to `~/Desktop/output_images/`.

### Step 4: View Results

When complete, click **"📂 Open Output Folder"** to view your screenshots.

## 📖 Usage

### CSV/Excel Format

**Required Column:**
- `url` - The website URL to screenshot

**Optional Column:**
- `filename` - Custom name for the screenshot

### Example CSV

```csv
url,filename
https://apple.com,Apple Homepage
https://microsoft.com,Microsoft Main
https://google.com,Google Search
https://github.com,GitHub Platform
https://twitter.com,Twitter Feed
```

### What Happens

1. Script reads CSV file
2. Initializes headless Chrome browser
3. For each URL:
   - Navigates to website
   - Waits for page load (2 seconds)
   - Captures full-page screenshot
   - Validates file size (> 10 KB)
   - Saves with custom name
4. Generates summary report
5. Opens output folder

## ⚙️ Configuration

Edit the top of `screenshot_downloader.py`:

```python
# --- CONFIGURATION ---
OUTPUT_FOLDER = os.path.expanduser("~/Desktop/output_images")
URL_COLUMN = "url"          # Column name for URLs
NAME_COLUMN = "filename"    # Column name for custom filenames
```

### Adjust Browser Settings

```python
# Change screenshot resolution
chrome_options.add_argument("--window-size=1920,1080")

# Increase wait time for slow sites
time.sleep(5)  # Default is 2 seconds
```

## 🧪 Troubleshooting

### Chrome Not Found

```bash
# Install Chrome
brew install --cask google-chrome  # macOS
sudo apt-get install google-chrome-stable  # Ubuntu
```

### "Column 'url' not found"

Make sure CSV has an `url` column (case-sensitive).

### Blank Screenshots

Increase the wait time:
```python
time.sleep(5)  # Increase from 2 to 5 seconds
```

### Permission Denied

Change output folder to a writable location:
```python
OUTPUT_FOLDER = os.path.expanduser("~/Downloads/screenshots")
```

## 💡 Use Cases

- 🔍 **Competitor Analysis** - Capture competitor website designs
- 📊 **SEO Audits** - Document website layouts and structures
- ✅ **QA Testing** - Test website rendering and document bugs
- 🤖 **ML Datasets** - Create image datasets for machine learning
- 📚 **Documentation** - Archive and document web pages
- 📈 **Research** - Analyze web design trends

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests or open issues.

## 📄 License

MIT License - feel free to use and modify!

## 👨‍💻 Author

Created by [Your Name](https://github.com/Rish212004)

## 🆘 Support

Have questions? Open an issue on GitHub!

---

**Happy screenshotting! 📸✨**
