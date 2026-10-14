import tkinter as tk
from src.models.animation_model import AnimationModel
from src.renderers.renderer import ParticleRenderer


class ParticleApp:

  def __init__(self, root, file_path="pattern.txt"):
    self.root = root
    self.root.title("Система частиц из TXT файла")

    self.canvas = tk.Canvas(root, width=800, height=400, bg="#111111")
    self.canvas.pack()

    self.mouse_x = None
    self.mouse_y = None

    self.model = AnimationModel(file_path)
    self.renderer = ParticleRenderer(self.canvas)

    self.canvas.bind("<Motion>", self.on_mouse_move)
    self.canvas.bind("<Leave>", self.on_mouse_leave)

    self.animate()

  def on_mouse_move(self, event):
    self.mouse_x = event.x
    self.mouse_y = event.y

  def on_mouse_leave(self, event):
    self.mouse_x = None
    self.mouse_y = None

  def animate(self):
    self.model.update_particles(self.mouse_x, self.mouse_y)

    self.renderer.render(self.model.particles)

    self.root.after(16, self.animate)
