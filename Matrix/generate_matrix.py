import os
import xml.etree.ElementTree as ET
import time

code = """# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import colorchooser, Scale, IntVar, StringVar, OptionMenu
import random
import time
import os
import xml.etree.ElementTree as ET

class MatrixRainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Rain")
        self.root.attributes('-fullscreen', False)
        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.cols = self.canvas.winfo_screenwidth() // 10
        self.drops = [0] * self.cols
        self.rain_color, self.density, self.speed, self.width, self.height = self.load_settings()
        self.root.geometry(f"{self.width}x{self.height}")
        self.create_buttons()
        self.animate()

    def create_buttons(self):
        color_button = tk.Button(self.root, text="Farbe ändern", command=self.choose_color)
        color_button.pack()
        settings_button = tk.Button(self.root, text="Einstellungen", command=self.open_settings)
        settings_button.pack()
        exit_button = tk.Button(self.root, text="Beenden", command=self.root.destroy)
        exit_button.pack()

    def choose_color(self):
        color = colorchooser.askcolor(title="Wähle eine Farbe")
        if color[1]:
            self.rain_color = color[1]
            self.save_settings()

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Einstellungen")

        density_scale = Scale(settings_window, from_=0.01, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, label="Dichte", variable=tk.DoubleVar(value=self.density))
        density_scale.pack()

        speed_scale = Scale(settings_window, from_=10, to=200, orient=tk.HORIZONTAL, label="Geschwindigkeit", variable=tk.IntVar(value=self.speed))
        speed_scale.pack()

        presets = {
            "Klein": (800, 600),
            "Mittel": (1024, 768),
            "Groß": (1280, 720)
        }

        def apply_preset(preset):
            width, height = presets[preset]
            self.width = width
            self.height = height
            self.root.geometry(f"{self.width}x{self.height}")

        preset_var = StringVar(settings_window)
        preset_var.set("Größe wählen")
        preset_menu = OptionMenu(settings_window, preset_var, *presets.keys(), command=apply_preset)
        preset_menu.pack()

        save_button = tk.Button(settings_window, text="Speichern", command=lambda: self.save_settings(density_scale.get(), speed_scale.get(), settings_window))
        save_button.pack()

        reset_button = tk.Button(settings_window, text="Zurücksetzen", command=lambda: self.reset_settings(density_scale, speed_scale))
        reset_button.pack()

    def reset_settings(self, density_scale, speed_scale):
        self.density = 0.1
        self.speed = 50
        density_scale.set(self.density)
        speed_scale.set(self.speed)

    def animate(self):
        self.canvas.delete("all")
        for i in range(self.cols):
            text = chr(random.randint(33, 126))
            y = self.drops[i] * 10
            self.canvas.create_text(i * 10, y, text=text, fill=self.rain_color, font=("Courier", 10))
            if random.random() > 1 - self.density:
                self.drops[i] = 0
            self.drops[i] += 1
        self.root.after(self.speed, self.animate)

    def get_save_dir(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(script_dir, 'save')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        return save_dir

    def save_settings(self, density=None, speed=None, settings_window=None):
        if density is not None:
            self.density = density
        if speed is not None:
            self.speed = int(speed)

        save_dir = self.get_save_dir()
        config_path = os.path.join(save_dir, 'settings.xml')
        root = ET.Element('settings')
        ET.SubElement(root, 'color').text = self.rain_color
        ET.SubElement(root, 'density').text = str(self.density)
        ET.SubElement(root, 'speed').text = str(self.speed)
        ET.SubElement(root, 'width').text = str(self.width)
        ET.SubElement(root, 'height').text = str(self.height)
        tree = ET.ElementTree(root)
        tree.write(config_path)

        if settings_window:
            settings_window.destroy()

    def load_settings(self):
        save_dir = self.get_save_dir()
        config_path = os.path.join(save_dir, 'settings.xml')
        try:
            tree = ET.parse(config_path)
            root = tree.getroot()
            color = root.find('color').text if root.find('color') is not None else "green"
            density = float(root.find('density').text) if root.find('density') is not None else 0.1
            speed = int(root.find('speed').text) if root.find('speed').text is not None else 50
            width = int(root.find('width').text) if root.find('width').text is not None else 800
            height = int(root.find('height').text) if root.find('height').text is not None else 600
            return color, density, speed, width, height
        except FileNotFoundError:
            return "green", 0.1, 50, 800, 600

def create_default_settings(save_dir):
    default_settings_path = os.path.join(save_dir, 'default_settings.xml')
    root = ET.Element('settings')
    ET.SubElement(root, 'color').text = 'green'
    ET.SubElement(root, 'density').text = '0.1'
    ET.SubElement(root, 'speed').text = '50'
    ET.SubElement(root, 'width').text = '800'
    ET.SubElement(root, 'height').text = '600'
    tree = ET.ElementTree(root)
    tree.write(default_settings_path)

def create_logfile(script_dir):
    log_path = os.path.join(script_dir, 'log.txt')
    with open(log_path, 'w') as f:
        f.write('Logfile erstellt: ' + time.strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixRainGUI(root)
    root.mainloop()
"""

# Ermittle das Verzeichnis des Skripts
script_dir = os.path.dirname(os.path.abspath(__file__))

# Erstelle das 'save'-Verzeichnis, falls es nicht existiert
save_dir = os.path.join(script_dir, 'save')
if not os