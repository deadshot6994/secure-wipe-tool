import tkinter as tk
from tkinter import filedialog, messagebox
from app.wipe import wipe_files
from app.verifier import generate_certificate
from app.utils import is_safe_path
import os

class SecureWipeUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure Wipe Tool")
        self.root.geometry("400x250")
        
        self.label = tk.Label(self.root, text="Select files/folders to securely wipe:")
        self.label.pack(pady=10)

        self.select_btn = tk.Button(self.root, text="Select Files/Folders", command=self.select_files)
        self.select_btn.pack(pady=5)

        self.wipe_btn = tk.Button(self.root, text="Start Wipe", command=self.start_wipe, state=tk.DISABLED)
        self.wipe_btn.pack(pady=5)

        self.selected_paths = []

    def select_files(self):
        paths = filedialog.askopenfilenames(title="Select files or folders")
        if paths:
            safe_paths = [p for p in paths if is_safe_path(p)]
            if not safe_paths:
                messagebox.showerror("Error", "No valid files/folders selected.")
                return
            self.selected_paths = safe_paths
            self.wipe_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Selected", f"{len(self.selected_paths)} files/folders selected.")

    def start_wipe(self):
        if not self.selected_paths:
            messagebox.showwarning("Warning", "No files selected.")
            return
        for path in self.selected_paths:
            wipe_files(path)
        cert_path = generate_certificate(self.selected_paths)
        messagebox.showinfo("Success", f"Wipe completed!\nCertificate: {cert_path}")

    def run(self):
        self.root.mainloop()
