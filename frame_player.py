# Created by Yusuf Emre ALBAYRAK for project HÜMA in TEKNOFEST 2025 HYZ competition.
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import os
from PIL import Image, ImageTk
import glob
import argparse
import sys

class FramePlayer:
    def __init__(self, root, frames_dir=None):
        self.root = root
        self.root.title("Frame Player")
        
        # Set default window size
        self.frame_width = 1000
        self.frame_height = 600
        
        # Set default playback speed (ms between frames)
        self.speeds = {
            "0.25": 132,  # 7.5 fps
            "0.5": 66,    # 15 fps
            "1x": 33,     # 30 fps
            "2x": 16,     # 60 fps
            "4x": 8,      # 120 fps
            "8x": 4,      # 240 fps
            "16x": 2,     # 480 fps
            "32x": 1,     # 960 fps
        }
        self.current_speed = "1x"
        
        # Create menu bar
        self.create_menu_bar()
        
        if frames_dir is None:
            # Show folder selection button if no directory provided
            self.show_folder_selection()
        else:
            self.load_frames_directory(frames_dir)
    
    def load_frames_directory(self, frames_dir):
        # Load frames
        self.frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.webp")))
        self.current_frame = 0
        self.total_frames = len(self.frame_files)
        self.playing = False
        self.photo = None
        
        if self.total_frames == 0:
            messagebox.showerror("Error", "No frames found in the selected directory!")
            if not hasattr(self, 'folder_button'):
                self.show_folder_selection()
            return
        
        # Calculate scale from first frame
        try:
            first_frame = cv2.imread(self.frame_files[0])
            if first_frame is not None:
                height, width = first_frame.shape[:2]
                self.scale = min(1000/width, 600/height)
                self.frame_width = int(width * self.scale)
                self.frame_height = int(height * self.scale)
            else:
                self.scale = 1.0
                self.frame_width = 1000
                self.frame_height = 600
        except Exception as e:
            print(f"Error reading first frame: {e}")
            self.scale = 1.0
            self.frame_width = 1000
            self.frame_height = 600
        
        # Create GUI elements
        self.create_widgets()
        
        # Load first frame
        self.load_frame()
    
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Folder", command=self.select_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_separator()
        help_menu.add_command(label="GitHub", command=lambda: os.startfile("https://github.com/ysfemreAlbyrk/frames-player"))
    
    def show_about(self):
        messagebox.showinfo("About Frame Player", 
                          "Frame Player v0.1\n\n" 
                          "A simple application to view and play image frames.\n\n" 
                          "Created by Yusuf Emre ALBAYRAK for project HÜMA in TEKNOFEST 2025 HYZ competition.")
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select Frames Directory")
        if folder_path:
            # Clear existing widgets if any
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Menu):
                    continue
                widget.destroy()
            self.load_frames_directory(folder_path)
    
    def show_folder_selection(self):
        # Create canvas with default size
        self.canvas = tk.Canvas(self.root, width=self.frame_width, height=self.frame_height)
        self.canvas.pack(pady=10,padx=10)
        
        # Create a centered button for folder selection
        self.folder_button = ttk.Button(self.root, text="Select Frames Folder", 
                                      command=self.select_folder)
        self.folder_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def create_widgets(self):
        # Frame display
        self.canvas = tk.Canvas(self.root, width=self.frame_width, height=self.frame_height)
        self.canvas.pack(pady=10,padx=10)
        
        # Controls frame
        controls = ttk.Frame(self.root)
        controls.pack(pady=10)
        
        # Speed control
        speed_frame = ttk.Frame(controls)
        speed_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value=self.current_speed)
        speed_menu = ttk.OptionMenu(speed_frame, self.speed_var, self.current_speed, 
                                   *self.speeds.keys(), command=self.change_speed)
        speed_menu.pack(side=tk.LEFT)
        
        # Buttons
        self.play_button = ttk.Button(controls, text="▶", command=self.toggle_play)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls, text="<<", command=self.prev_frame).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text=">>", command=self.next_frame).pack(side=tk.LEFT, padx=5)
        
        # Slider
        if self.total_frames > 0:
            self.slider = ttk.Scale(self.root, from_=0, to=self.total_frames-1, 
                                  orient=tk.HORIZONTAL, command=self.slider_changed)
            self.slider.pack(fill=tk.X, padx=20, pady=10)
        else:
            print("No frames found in the specified directory")
            sys.exit(1)
        
        # Frame counter
        self.counter_label = ttk.Label(self.root, text="0/0")
        self.counter_label.pack(pady=5)
        
    def load_frame(self):
        if not (0 <= self.current_frame < self.total_frames):
            return
            
        try:
            # Read and resize image
            img = cv2.imread(self.frame_files[self.current_frame])
            if img is None:
                print(f"Error: Could not read frame {self.frame_files[self.current_frame]}")
                return
                
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (self.frame_width, self.frame_height))
            
            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(Image.fromarray(img))
            
            # Update canvas
            self.canvas.config(width=self.frame_width, height=self.frame_height)
            self.canvas.delete("all")
            self.canvas.create_image(self.frame_width//2, self.frame_height//2, image=self.photo)
            
            # Update counter
            self.counter_label.config(text=f"Frame {self.current_frame + 1}/{self.total_frames}")
        except Exception as e:
            print(f"Error loading frame: {e}")
            return
    
    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % self.total_frames
        self.slider.set(self.current_frame)
        self.load_frame()
        
    def prev_frame(self):
        self.current_frame = (self.current_frame - 1) % self.total_frames
        self.slider.set(self.current_frame)
        self.load_frame()
    
    def toggle_play(self):
        self.playing = not self.playing
        self.play_button.config(text="||" if self.playing else "▶")
        if self.playing:
            self.play_animation()
    
    def play_animation(self):
        if self.playing:
            self.next_frame()
            self.root.after(self.speeds[self.current_speed], self.play_animation)
    
    def change_speed(self, speed):
        self.current_speed = speed
    
    def slider_changed(self, value):
        try:
            new_frame = int(float(value))
            if new_frame != self.current_frame:
                self.current_frame = new_frame
                self.load_frame()
        except ValueError:
            pass

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Frame Player')
    parser.add_argument('frames_dir', nargs='?', help='Directory containing the frames')
    args = parser.parse_args()
    
    root = tk.Tk()
    app = FramePlayer(root, args.frames_dir if args.frames_dir else None)
    root.mainloop()