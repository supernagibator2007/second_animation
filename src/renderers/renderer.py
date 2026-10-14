class ParticleRenderer:

  def __init__(self, canvas):
    self.canvas = canvas

  def render(self, particles):
    self.canvas.delete("particle")

    radius = 3
    for p in particles:
      self.canvas.create_oval(
          p.x - radius,
          p.y - radius,
          p.x + radius,
          p.y + radius,
          fill="#ffffff",
          outline="",
          tags="particle",
      )
