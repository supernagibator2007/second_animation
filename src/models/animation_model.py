import math
import os
import random


class Particle:

    def __init__(self, target_x, target_y):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 400)
        self.target_x = target_x
        self.target_y = target_y

        self.speed_factor = 0.05  # Сила притяжения к цели
        self.friction = 0.6  # Затухание скорости
        self.repulsion_radius = 70  # Радиус отталкивания от мыши

    def update(self, mouse_x, mouse_y):
        ax = (self.target_x - self.x) * self.speed_factor
        ay = (self.target_y - self.y) * self.speed_factor

        if mouse_x is not None and mouse_y is not None:
            dx = self.x - mouse_x
            dy = self.y - mouse_y
            distance = math.hypot(dx, dy)

            if distance < self.repulsion_radius and distance > 0:
                force = self.repulsion_radius - distance
                ax += (dx / distance) * force
                ay += (dy / distance) * force

        self.x += ax
        self.y += ay


class AnimationModel:

  def __init__(self, file_path="pattern.txt"):
    self.particles = []
    self.file_path = file_path
    self.ensure_default_file()
    self.load_targets_from_txt()

  def ensure_default_file(self):
    if not os.path.exists(self.file_path):
      default_pattern = (
          "*****  ****    ***   *****  *   *\n"
          "  *    *   *  *   *    *    **  *\n"
          "  *    ****   *****    *    * * *\n"
          "  *    *  *   *   *    *    *  **\n"
          "  *    *   *  *   *  *****  *   *\n"
      )
      with open(self.file_path, "w", encoding="utf-8") as f:
        f.write(default_pattern)

  def load_targets_from_txt(self):
    with open(self.file_path, "r", encoding="utf-8") as f:
      lines = f.readlines()

    pixel_step = 14
    max_cols = max(len(line.rstrip("\n")) for line in lines)
    max_rows = len(lines)

    offset_x = (800 - (max_cols * pixel_step)) // 2
    offset_y = (400 - (max_rows * pixel_step)) // 2

    for row_idx, line in enumerate(lines):
      clean_line = line.rstrip("\r\n")
      for col_idx, char in enumerate(clean_line):
        if char != " ":
          target_x = offset_x + col_idx * pixel_step
          target_y = offset_y + row_idx * pixel_step
          self.particles.append(Particle(target_x, target_y))

  def update_particles(self, mouse_x, mouse_y):
    for p in self.particles:
      p.update(mouse_x, mouse_y)
