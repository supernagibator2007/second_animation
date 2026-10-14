import math
import os
import random
import tkinter as tk


class Particle:

    def __init__(self, target_x, target_y):
        # Начальная позиция частиц (случайная на экране)
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 400)
        self.target_x = target_x
        self.target_y = target_y
        self.vx = 0
        self.vy = 0

        # Настройки физики
        self.speed_factor = 0.05  # Сила притяжения к цели
        self.friction = 0.6  # Затухание скорости
        self.repulsion_radius = 70  # Радиус отталкивания от мыши
        self.repulsion_strength = 0.8  # Сила отталкивания

    def update(self, mouse_x, mouse_y):
        # 1. Притяжение к целевой точке
        ax = (self.target_x - self.x) * self.speed_factor
        ay = (self.target_y - self.y) * self.speed_factor

        # 2. Отталкивание от курсора мыши
        if mouse_x is not None and mouse_y is not None:
            dx = self.x - mouse_x
            dy = self.y - mouse_y
            distance = math.hypot(dx, dy)

            if distance < self.repulsion_radius and distance > 0:
                force = (self.repulsion_radius - distance) * self.repulsion_strength
                ax += (dx / distance) * force
                ay += (dy / distance) * force

        # Обновление скорости и координат
        self.vx = (self.vx + ax) * self.friction
        self.vy = (self.vy + ay) * self.friction
        self.x += self.vx
        self.y += self.vy


class ParticleSystemApp:

    def __init__(self, root, file_path="pattern.txt"):
        self.root = root
        self.root.title("Система частиц из TXT файла")

        # Создаем холст (темный фон, чтобы белые точки хорошо читались)
        self.canvas = tk.Canvas(root, width=800, height=400, bg="#111111")
        self.canvas.pack()

        # Координаты мыши
        self.mouse_x = None
        self.mouse_y = None

        # Привязка событий мыши
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)

        # Автоматическое создание файла по умолчанию, если его нет
        self.ensure_default_file(file_path)

        # Загрузка точек из TXT файла и инициализация частиц
        self.particles = []
        self.load_targets_from_txt(file_path)

        # Запуск главного цикла анимации
        self.animate()

    def ensure_default_file(self, file_path):
        # Если файла нет, создаем его и записываем слово "train"
        if not os.path.exists(file_path):
            default_pattern = (
                "*****  ****    ***   *****  *   *\n"
                "  *    *   *  *   *    *    **  *\n"
                "  *    ****   *****    *    * * *\n"
                "  *    *  *   *   *    *    *  **\n"
                "  *    *   *  *   *  *****  *   *\n"
            )
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(default_pattern)
            print(f"Файл '{file_path}' не был найден и создан автоматически.")

    def load_targets_from_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Настройки шага сетки (расстояние между точками в пикселях)
        pixel_step = 14

        # Находим максимальную длину строки для центрирования
        max_cols = max(len(line.rstrip("\n")) for line in lines) if lines else 0
        max_rows = len(lines)

        # Вычисляем отступы, чтобы текст встал ровно по центру окна (800x400)
        offset_x = (800 - (max_cols * pixel_step)) // 2
        offset_y = (400 - (max_rows * pixel_step)) // 2

        for row_idx, line in enumerate(lines):
            clean_line = line.rstrip("\r\n")
            for col_idx, char in enumerate(clean_line):
                # Любой символ, кроме пробела, становится белой точкой
                if char != " ":
                    target_x = offset_x + col_idx * pixel_step
                    target_y = offset_y + row_idx * pixel_step
                    self.particles.append(Particle(target_x, target_y))

    def on_mouse_move(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def on_mouse_leave(self, event):
        self.mouse_x = None
        self.mouse_y = None

    def animate(self):
        # Очищаем холст перед новым кадром
        self.canvas.delete("particle")

        for p in self.particles:
            p.update(self.mouse_x, self.mouse_y)
            # Рисуем частицы белым цветом (#ffffff)
            radius = 3
            self.canvas.create_oval(
                p.x - radius,
                p.y - radius,
                p.x + radius,
                p.y + radius,
                fill="#ffffff",
                outline="",
                tags="particle",
            )

        # Смена кадров каждые 16 мс (~60 FPS)
        self.root.after(16, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = ParticleSystemApp(root, file_path="pattern.txt")
    root.mainloop()
