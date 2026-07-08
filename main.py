import os
import shutil
import threading
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("MMJ Client Installer")
app.geometry("500x350")
app.resizable(False, False)

# Detect .minecraft folder
minecraft_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft")

title = ctk.CTkLabel(app, text="MMJ Client Installer", font=("Arial", 24, "bold"))
title.pack(pady=20)

path_label = ctk.CTkLabel(app, text="Minecraft Folder:")
path_label.pack()

path_entry = ctk.CTkEntry(app, width=420)
path_entry.pack(pady=5)
path_entry.insert(0, minecraft_folder)

progress = ttk.Progressbar(app, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=20)

status = ctk.CTkLabel(app, text="Ready")
status.pack()


def install():
    source = "modpack"
    destination = path_entry.get()

    if not os.path.exists(source):
        messagebox.showerror("Error", "The 'modpack' folder was not found.")
        return

    files = []

    for root, dirs, filenames in os.walk(source):
        for file in filenames:
            files.append(os.path.join(root, file))

    total = len(files)

    if total == 0:
        messagebox.showwarning("Warning", "No files found in the modpack folder.")
        return

    progress["maximum"] = total
    progress["value"] = 0

    count = 0

    for file in files:
        relative = os.path.relpath(file, source)
        dest_file = os.path.join(destination, relative)

        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(file, dest_file)

        count += 1
        progress["value"] = count
        status.configure(text=f"Installing... ({count}/{total})")
        app.update_idletasks()

    status.configure(text="Installation Complete!")
    messagebox.showinfo("Done", "MMJ Client installed successfully!")


def start_install():
    threading.Thread(target=install).start()


install_button = ctk.CTkButton(
    app,
    text="Install",
    command=start_install,
    width=200,
    height=40
)

install_button.pack(pady=20)

app.mainloop()