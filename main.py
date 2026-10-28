import tkinter as tk
from src.app import ParticleApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ParticleApp(root, file_path="pattern.txt")
    root.mainloop()
