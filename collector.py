import tkinter as tk
from tkinter import filedialog, simpledialog
import os
import re
from PIL import Image, ImageTk

class CharacterImageData:
    def __init__(self, name):
        self.name = name
        self.highest_number = 0

    def update_highest_number(self, number):
        if number > self.highest_number:
            self.highest_number = number

    def update_from_directory(self, directory):
        pattern = re.compile(r'.*_(\d+)\.png')
        subdir_path = os.path.join(directory, self.name.lower())

        if not os.path.isdir(subdir_path):
            print('Error Loading Images')
            return

        for image in os.listdir(subdir_path):
            match = pattern.match(image)
            if match:
                number = int(match.group(1))
                self.update_highest_number(number+1)

    def __str__(self):
        return f"{self.name}: {self.highest_number}"

# Usage
character_directory = '/Users/ltk/Documents/Datasets/opimagedata'
luffy = CharacterImageData('Luffy')
chopa = CharacterImageData('Chopa')
nami = CharacterImageData('Nami')

luffy.update_from_directory(character_directory)
chopa.update_from_directory(character_directory)
nami.update_from_directory(character_directory)

print(luffy.highest_number)
print(chopa)
print(nami)




class Rectangle:
    def __init__(self, canvas, x1, y1, x2, y2, outline, width, label, number):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, outline=outline, width=width)
        self.label = label
        self.canvas.tag_bind(self.rect, "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind(self.rect, "<B1-Motion>", self.on_drag)
        self.number = number
        self.start_x = None
        self.start_y = None

    def on_start(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.rect, dx, dy)
        self.start_x = event.x
        self.start_y = event.y

    def get_coords(self):
        return self.canvas.coords(self.rect)

class ImageCollectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Collector")
        self.root.geometry("500x500")  # Set the main window size
        
        # Load Multiple Images button
        self.load_multiple_images_button = tk.Button(root, text="Load Multiple Images", command=self.load_multiple_images)
        self.load_multiple_images_button.pack(pady=10)
        
        # Load Image button
        self.load_image_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_image_button.pack(pady=10)
        
        # Create Rectangle button
        self.create_rectangle_button = tk.Button(root, text="Nami", command=self.create_nami_rectangle)
        self.create_rectangle_button.pack(pady=10)
        
        # Create Small Rectangle button
        self.create_small_rectangle_button = tk.Button(root, text="Chopa", command=self.create_chopa_rectangle)
        self.create_small_rectangle_button.pack(pady=10)
        
        # Crop Image button
        self.crop_image_button = tk.Button(root, text="Crop Image", command=self.crop_image)
        self.crop_image_button.pack(pady=10)
        
        # Character button
        self.character_button = tk.Button(root, text="Luffy", command=self.create_luffy_rectangle)
        self.character_button.pack(pady=10)
        
        # Checkboxes for rectangle sizes
        self.size_var_25 = tk.IntVar()
        self.size_var_50 = tk.IntVar()
        self.size_var_100 = tk.IntVar()
        self.size_var_150 = tk.IntVar()
        self.size_var_200 = tk.IntVar()

        self.checkbox_25 = tk.Checkbutton(root, text="25x25", variable=self.size_var_25)
        self.checkbox_25.pack(pady=5)

        self.checkbox_50 = tk.Checkbutton(root, text="50x50", variable=self.size_var_50)
        self.checkbox_50.pack(pady=5)
        
        self.checkbox_100 = tk.Checkbutton(root, text="100x100", variable=self.size_var_100)
        self.checkbox_100.pack(pady=5)
        
        self.checkbox_150 = tk.Checkbutton(root, text="150x150", variable=self.size_var_150)
        self.checkbox_150.pack(pady=5)
        
        self.checkbox_200 = tk.Checkbutton(root, text="200x200", variable=self.size_var_200)
        self.checkbox_200.pack(pady=5)
        
        self.image_window = None
        self.image = None
        self.image_id = None
        self.canvas = None
        self.image_names = []
        self.current_image_index = 0
        self.rectangles = []  # Store rectangle objects

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg")])
        if file_path:
            self.image = Image.open(file_path)
            original_width, original_height = self.image.size

            # Scale down the image by 70%
            new_width = int(original_width * 0.7)
            new_height = int(original_height * 0.7)
            self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

            # Create a new window for the image
            self.image_window = tk.Toplevel(self.root)
            self.image_window.title("Image Viewer")
            self.image_window.geometry(f"{new_width}x{new_height}")

            # Create a canvas in the new window
            self.canvas = tk.Canvas(self.image_window, width=new_width, height=new_height)
            self.canvas.pack()

            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def load_multiple_images(self):
        directory = filedialog.askdirectory()
        if directory:
            self.image_names = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.jpg')]
            self.current_image_index = 0
            if self.image_names:
                self.display_image(self.image_names[self.current_image_index])

    def display_image(self, file_path):
        self.image = Image.open(file_path)
        original_width, original_height = self.image.size

        # Scale down the image by 70%
        new_width = int(original_width * 0.7)
        new_height = int(original_height * 0.7)
        self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

        # Create a new window for the image if it doesn't exist
        if not self.image_window or not self.canvas:
            self.image_window = tk.Toplevel(self.root)
            self.image_window.title("Image Viewer")
            self.image_window.geometry(f"{new_width}x{new_height}")
            self.canvas = tk.Canvas(self.image_window, width=new_width, height=new_height)
            self.canvas.pack()

        self.image_tk = ImageTk.PhotoImage(self.image)
        if self.image_id:
            self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        # Bind the next image display to the button click
        self.load_multiple_images_button.config(command=self.show_next_image)

    def show_next_image(self):
        self.current_image_index += 1
        if self.current_image_index < len(self.image_names):
            self.display_image(self.image_names[self.current_image_index])
        else:
            self.current_image_index = 0
            self.display_image(self.image_names[self.current_image_index])

    def create_chopa_rectangle(self):
        if self.canvas:
            size = None
            if self.size_var_25.get():
                size = 125
            elif self.size_var_50.get():
                size = 150
            elif self.size_var_100.get():
                size = 200
            elif self.size_var_150.get():
                size = 250
            elif self.size_var_200.get():
                size = 300
            
            if size:
                rect = Rectangle(self.canvas, 100, 100, size, size, outline="brown", width=2, label='chopa', number=chopa.highest_number)
                self.rectangles.append(rect)

    def create_nami_rectangle(self):
        if self.canvas:
            size = None
            if self.size_var_25.get():
                size = 125
            elif self.size_var_50.get():
                size = 150
            elif self.size_var_100.get():
                size = 200
            elif self.size_var_150.get():
                size = 250
            elif self.size_var_200.get():
                size = 300
            
            if size:
                rect = Rectangle(self.canvas, 100, 100, size, size, outline="orange", width=2, label='nami', number=nami.highest_number)
                self.rectangles.append(rect)

    def create_luffy_rectangle(self):
        if self.canvas:
            size = None
            if self.size_var_25.get():
                size = 125
            elif self.size_var_50.get():
                size = 150
            elif self.size_var_100.get():
                size = 200
            elif self.size_var_150.get():
                size = 250
            elif self.size_var_200.get():
                size = 300
            
            if size:
                rect = Rectangle(self.canvas, 100, 100, size, size, outline="red", width=2, label='luffy', number=luffy.highest_number)
                self.rectangles.append(rect)

    def crop_image(self):
        if self.rectangles and self.image:
            for rect in self.rectangles:
                x1, y1, x2, y2 = rect.get_coords()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cropped_image = self.image.crop((x1, y1, x2, y2))
                match rect.label:
                    case 'luffy':
                        cropped_image.save(os.path.join('/Users/ltk/Documents/Datasets/opimagedata/luffy', f"{rect.label}_{rect.number}.png"))
                    case 'nami':
                        cropped_image.save(os.path.join('/Users/ltk/Documents/Datasets/opimagedata/nami', f"{rect.label}_{rect.number}.png"))
                    case 'chopa':
                        cropped_image.save(os.path.join('/Users/ltk/Documents/Datasets/opimagedata/chopa', f"{rect.label}_{rect.number}.png"))
                    case _:
                        cropped_image.save(f"{rect.label}_{rect.number}.png")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCollectorApp(root)
    root.mainloop()