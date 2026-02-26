import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# --- CONFIGURATION ---
OUTPUT_FOLDER = os.path.expanduser("~/Desktop/output_images")  # Save to Desktop
URL_COLUMN = "url"        # The header name of the URL column
NAME_COLUMN = "filename"  # The header name of the Filename column (optional)

def setup_driver():
    """Sets up Chrome driver with FAST settings (keeping JS/images for quality)."""
    chrome_options = Options()
    
    # Speed Optimizations (keeping rendering enabled)
    chrome_options.add_argument("--headless=new")  # NEW headless mode (faster)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-component-extensions-with-background-pages")
    
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def sanitize_filename(text):
    """Clean strings to make them valid filenames."""
    return "".join([c for c in text if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).strip()

def select_csv_file():
    """Open file dialog to select CSV or Excel file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    file_path = filedialog.askopenfilename(
        title="Select your CSV or Excel file",
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
    )
    
    return file_path

def process_bulk_urls(file_path, progress_window, progress_label, status_text):
    """Process URLs with screenshot capture."""
    
    # 1. Check if file exists
    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"File not found: {file_path}")
        progress_window.destroy()
        return

    # 2. Read the file (Excel or CSV)
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            print(f"✅ Reading CSV file: {file_path}")
        else:
            df = pd.read_excel(file_path)
            print(f"✅ Reading Excel file: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {e}")
        progress_window.destroy()
        return

    print(f"📊 Found {len(df)} rows in the file.")

    # Check if URL column exists
    if URL_COLUMN not in df.columns:
        messagebox.showerror("Error", f"Column '{URL_COLUMN}' not found!")
        progress_window.destroy()
        return

    # 3. Create output folder if it doesn't exist
    try:
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
    except Exception as e:
        messagebox.showerror("Error", f"Error creating folder: {e}")
        progress_window.destroy()
        return

    # Update progress window
    status_text.config(text=f"📁 Output Folder:\n{OUTPUT_FOLDER}\n\n⏳ Starting browser...")
    progress_window.update()

    # 4. Initialize Browser
    driver = setup_driver()

    successful = 0
    failed = 0
    total = len(df)

    # 5. Loop through the rows
    for index, row in df.iterrows():
        url = row.get(URL_COLUMN)

        # Skip empty rows
        if pd.isna(url):
            continue

        # Clean up URL
        url = str(url).strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Determine Filename - ALWAYS use filename column if it exists
        if NAME_COLUMN in df.columns and not pd.isna(row[NAME_COLUMN]):
            fname = sanitize_filename(str(row[NAME_COLUMN]).strip())
        else:
            # Only fallback to URL if no filename column
            fname = sanitize_filename(url.replace("https://", "").replace("http://", "").split('/')[0])[:30]
            if not fname:
                fname = f"screenshot_{index+1}"

        # Add counter to ensure unique filenames
        output_path = os.path.join(OUTPUT_FOLDER, f"{fname}_{index+1}.png")

        # Update progress
        progress = int((index + 1) / total * 100)
        progress_label.config(text=f"Progress: {index + 1}/{total} ({progress}%)")
        status_text.config(text=f"📁 Saving to:\n{OUTPUT_FOLDER}\n\n🌐 Processing: {url}\n💾 Saving as: {fname}.png")
        progress_window.update()

        print(f"[{index+1}/{total}] {url} → {fname}.png")

        try:
            driver.get(url)
            time.sleep(2)  # Wait for page to load

            # Save screenshot directly as PNG
            driver.save_screenshot(output_path)
            
            # Verify file was created and has content
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024
                
                if file_size > 10:  # At least 10KB means it has content
                    print(f"   ✅ SUCCESS ({file_size:.1f} KB)")
                    successful += 1
                else:
                    print(f"   ⚠️  BLANK: File too small ({file_size:.1f} KB)")
                    failed += 1
            else:
                print(f"   ❌ FAILED: File not created")
                failed += 1

        except Exception as e:
            print(f"   ❌ FAILED: {str(e)[:50]}")
            failed += 1

    # 6. Clean up
    driver.quit()

    # 7. Final Summary
    summary = f"""
✅ DOWNLOAD COMPLETE!

✅ Successful: {successful}
⚠️  Failed/Blank: {failed}
📊 Total: {total}

📁 Files saved to:
{OUTPUT_FOLDER}

Click "Open Folder" to view your screenshots!
"""
    
    print("\n" + "="*60)
    print(summary)
    print("="*60)
    
    # Update final window
    progress_label.config(text=f"Progress: {total}/{total} (100%)")
    status_text.config(text=summary)
    progress_window.update()
    
    # Add Open Folder Button
    def open_folder():
        os.system(f"open '{OUTPUT_FOLDER}'")
    
    open_btn = tk.Button(progress_window, text="📂 Open Output Folder", command=open_folder, 
                        bg="#2196F3", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    open_btn.pack(pady=10)

# --- RUN IT ---
if __name__ == "__main__":
    # Create main GUI window
    root = tk.Tk()
    root.title("🎯 Website Screenshot Downloader")
    root.geometry("500x300")
    root.resizable(False, False)
    
    # Title
    title_label = tk.Label(root, text="🎯 Website Screenshot Downloader\n(FAST & QUALITY MODE)", 
                          font=("Arial", 14, "bold"))
    title_label.pack(pady=15)
    
    # Instructions
    instructions = tk.Label(root, text="Click the button below to select your CSV or Excel file\nwith URLs to download screenshots", 
                           font=("Arial", 11), justify=tk.CENTER)
    instructions.pack(pady=10)
    
    # File path display
    file_path_var = tk.StringVar(value="No file selected")
    file_path_label = tk.Label(root, text=file_path_var.get(), font=("Arial", 9), fg="gray")
    file_path_label.pack(pady=10)
    
    # Select File Button
    def select_and_process():
        file_path = select_csv_file()
        if file_path:
            file_path_var.set(f"Selected: {os.path.basename(file_path)}")
            file_path_label.config(text=file_path_var.get())
            root.update()
            
            # Ask for confirmation
            confirm = messagebox.askyesno("Confirm", f"Start downloading?\n{file_path}\n\n🚀 Fast & Quality Mode")
            if confirm:
                # Create progress window
                progress_window = tk.Tk()
                progress_window.title("⏳ Downloading...")
                progress_window.geometry("600x400")
                progress_window.resizable(False, False)
                
                # Progress bar label
                progress_label = tk.Label(progress_window, text="Progress: 0/0 (0%)", 
                                         font=("Arial", 12, "bold"), fg="#4CAF50")
                progress_label.pack(pady=10)
                
                # Status text
                status_text = tk.Label(progress_window, text="⏳ Starting...", 
                                      font=("Arial", 10), justify=tk.LEFT, wraplength=550)
                status_text.pack(pady=20, padx=20)
                
                # Run processing in separate thread
                thread = threading.Thread(target=process_bulk_urls, args=(file_path, progress_window, progress_label, status_text))
                thread.start()
                
                root.destroy()
                progress_window.mainloop()
    
    select_button = tk.Button(root, text="📁 Select CSV/Excel File", font=("Arial", 12, "bold"), 
                             command=select_and_process, bg="#4CAF50", fg="white", 
                             padx=20, pady=10, cursor="hand2")
    select_button.pack(pady=20)
    
    # Info text
    info_text = tk.Label(root, text="⚡ Fast Mode: Optimized for speed while keeping image quality\nScreenshots saved to: Desktop/output_images", 
                        font=("Arial", 9), fg="gray", justify=tk.CENTER)
    info_text.pack(pady=20)
    
    # Run the GUI
    root.mainloop()