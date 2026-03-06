import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

folder_counter = 1
save_path = ""

def choose_folder():
    global save_path
    save_path = filedialog.askdirectory()
    path_label.config(text=save_path)

def download_folder(base_url, folder_name):

    global folder_counter

    numbered_folder = f"{folder_counter}-{folder_name}"
    folder_counter += 1

    folder_path = os.path.join(save_path, numbered_folder)
    os.makedirs(folder_path, exist_ok=True)

    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a")
    progress["maximum"] = len(links)
    progress["value"] = 0

    for link in links:

        href = link.get("href")

        if href in ["../", "/"]:
            continue

        full_url = urljoin(base_url, href)

        if href.endswith("/"):
            subfolder = href.strip("/")
            download_folder(full_url, subfolder)

        else:

            file_name = os.path.basename(href)
            file_path = os.path.join(folder_path, file_name)

            log_box.insert(tk.END, f"Downloading: {file_name}\n")
            log_box.see(tk.END)

            file_data = requests.get(full_url)

            with open(file_path, "wb") as f:
                f.write(file_data.content)

        progress["value"] += 1
        root.update_idletasks()


def start_download():

    url = url_entry.get()

    if save_path == "":
        log_box.insert(tk.END, "Choose save folder first\n")
        return

    log_box.insert(tk.END, f"Start downloading: {url}\n")

    download_folder(url, "main_folder")

    log_box.insert(tk.END, "Download completed\n")


root = tk.Tk()
root.title("Folder Downloader Tool")
root.geometry("650x500")

title = tk.Label(root, text="Folder Downloader", font=("Arial", 16))
title.pack(pady=10)

url_label = tk.Label(root, text="Enter URL")
url_label.pack()

url_entry = tk.Entry(root, width=70)
url_entry.pack(pady=5)

choose_btn = tk.Button(root, text="Choose Save Folder", command=choose_folder)
choose_btn.pack(pady=5)

path_label = tk.Label(root, text="No folder selected")
path_label.pack()

download_btn = tk.Button(root, text="Start Download", command=start_download)
download_btn.pack(pady=10)

progress = ttk.Progressbar(root, length=500)
progress.pack(pady=10)

log_box = scrolledtext.ScrolledText(root, width=75, height=15)
log_box.pack(pady=10)

root.mainloop()