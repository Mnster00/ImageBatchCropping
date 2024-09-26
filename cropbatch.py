# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 03:17:21 2024

@author: Administrator
"""

import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class ImageCropper:
    def __init__(self, master):
        self.master = master
        master.title("Image Cropper")
        master.geometry("900x600")
        master.minsize(900, 600)

        self.folder_path = ""
        self.center_x, self.center_y = 0, 0
        self.image_paths = []
        self.current_image = None
        self.original_image = None
        self.displayed_image = None
        self.crop_box = None
        self.scale_factor = 1
        self.image_position = (0, 0)

        self.create_widgets()

        # Bind window resize event
        master.bind("<Configure>", self.on_window_resize)

    def create_widgets(self):
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Top frame for folder selection
        top_frame = tk.Frame(self.master)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        top_frame.grid_columnconfigure(1, weight=1)

        tk.Label(top_frame, text="Select folder:").grid(row=0, column=0)
        self.folder_entry = tk.Entry(top_frame)
        self.folder_entry.grid(row=0, column=1, sticky="ew")
        tk.Button(top_frame, text="Browse", command=self.select_folder).grid(row=0, column=2)

        # Middle frame for image display
        self.image_frame = tk.Frame(self.master, bg="white")
        self.image_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.image_label = tk.Label(self.image_frame, bg="white")
        self.image_label.grid(row=0, column=0, sticky="nsew")
        self.image_label.bind("<Button-1>", self.get_mouse_position)

        # Bottom frame for controls
        bottom_frame = tk.Frame(self.master)
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        bottom_frame.grid_columnconfigure(1, weight=1)

        # Position display
        self.position_label = tk.Label(bottom_frame, text="Selected center: (Not set)")
        self.position_label.grid(row=0, column=0)

        # Crop dimensions
        dim_frame = tk.Frame(bottom_frame)
        dim_frame.grid(row=0, column=1)
        tk.Label(dim_frame, text="Width:").grid(row=0, column=0)
        self.width_entry = tk.Entry(dim_frame, width=5)
        self.width_entry.grid(row=0, column=1)
        tk.Label(dim_frame, text="Height:").grid(row=0, column=2)
        self.height_entry = tk.Entry(dim_frame, width=5)
        self.height_entry.grid(row=0, column=3)

        # Crop button
        tk.Button(bottom_frame, text="Crop Images", command=self.crop_images).grid(row=0, column=2)

        # Result label
        self.result_label = tk.Label(bottom_frame, text="")
        self.result_label.grid(row=0, column=3)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, self.folder_path)
        self.image_paths = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path)
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        if self.image_paths:
            self.load_image(self.image_paths[0])

    def load_image(self, image_path):
        self.original_image = Image.open(image_path)
        self.update_image()

    def update_image(self):
        if self.original_image:
            self.fit_image_to_frame()

    def fit_image_to_frame(self):
        if self.original_image:
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            if frame_width <= 1 or frame_height <= 1:
                self.master.after(100, self.fit_image_to_frame)
                return

            img_width, img_height = self.original_image.size
            self.scale_factor = min(frame_width / img_width, frame_height / img_height)

            new_size = (int(img_width * self.scale_factor), int(img_height * self.scale_factor))
            self.displayed_image = self.original_image.copy().resize(new_size, Image.LANCZOS)

            new_img = Image.new("RGB", (frame_width, frame_height), "white")
            paste_x = (frame_width - new_size[0]) // 2
            paste_y = (frame_height - new_size[1]) // 2
            new_img.paste(self.displayed_image, (paste_x, paste_y))
            self.image_position = (paste_x, paste_y)

            self.current_image = ImageTk.PhotoImage(new_img)
            self.image_label.config(image=self.current_image)

            if self.crop_box:
                self.draw_crop_rectangle()

    def on_window_resize(self, event):
        if event.widget == self.master:
            self.master.after(100, self.fit_image_to_frame)

    def get_mouse_position(self, event):
        self.center_x, self.center_y = event.x - self.image_position[0], event.y - self.image_position[1]
        self.position_label.config(text=f"Selected center: ({self.center_x}, {self.center_y})")
        self.draw_crop_rectangle()

    def draw_crop_rectangle(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
        except ValueError:
            return

        if self.displayed_image:
            img_copy = self.displayed_image.copy()
            draw = ImageDraw.Draw(img_copy)

            left = max(0, self.center_x - width // 2)
            top = max(0, self.center_y - height // 2)
            right = min(img_copy.width, self.center_x + width // 2)
            bottom = min(img_copy.height, self.center_y + height // 2)

            self.crop_box = (left, top, right, bottom)

            draw.rectangle(self.crop_box, outline="red", width=2)

            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()
            new_img = Image.new("RGB", (frame_width, frame_height), "white")
            new_img.paste(img_copy, self.image_position)

            self.current_image = ImageTk.PhotoImage(new_img)
            self.image_label.config(image=self.current_image)

    def crop_images(self):
        if not self.folder_path or not self.crop_box:
            self.result_label.config(text="Please select a folder and set crop area!")
            return

        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
        except ValueError:
            self.result_label.config(text="Please enter valid dimensions!")
            return

        output_folder = os.path.join(self.folder_path, "cropped_images")
        os.makedirs(output_folder, exist_ok=True)

        for img_path in self.image_paths:
            with Image.open(img_path) as img:
                orig_width, orig_height = img.size
                scale_x = orig_width / self.original_image.width
                scale_y = orig_height / self.original_image.height

                left = int(max(0, self.crop_box[0] * scale_x / self.scale_factor))
                top = int(max(0, self.crop_box[1] * scale_y / self.scale_factor))
                right = int(min(orig_width, self.crop_box[2] * scale_x / self.scale_factor))
                bottom = int(min(orig_height, self.crop_box[3] * scale_y / self.scale_factor))

                cropped_img = img.crop((left, top, right, bottom))
                cropped_img = cropped_img.resize((width, height), Image.LANCZOS)
                
                output_filename = f"cropped_{os.path.basename(img_path)}"
                output_path = os.path.join(output_folder, output_filename)
                cropped_img.save(output_path)

        self.result_label.config(text="Cropping completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropper(root)
    root.mainloop()