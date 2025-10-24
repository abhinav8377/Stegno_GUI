import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import stepic
from io import BytesIO

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        self.style.configure('TButton', padding=5)
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_encode_tab()
        self.create_decode_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(5,0))
        self.update_status("Ready")
    
    def create_encode_tab(self):
        # Create encode tab
        self.encode_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.encode_tab, text="Encode")
        
        # Left panel for image preview
        left_frame = ttk.LabelFrame(self.encode_tab, text="Image Preview", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(left_frame, bg='white', bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right panel for controls
        right_frame = ttk.Frame(self.encode_tab, padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Message input
        ttk.Label(right_frame, text="Message to hide:").pack(anchor=tk.W, pady=(0,5))
        self.message_text = tk.Text(right_frame, height=10, width=40, wrap=tk.WORD)
        self.message_text.pack(fill=tk.X, pady=(0,10))
        
        # File selection
        ttk.Label(right_frame, text="Or select a file to hide:").pack(anchor=tk.W, pady=(5,0))
        self.file_path_var = tk.StringVar()
        file_frame = ttk.Frame(right_frame)
        file_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Entry(file_frame, textvariable=self.file_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).pack(side=tk.LEFT, padx=(5,0))
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        ttk.Button(btn_frame, text="Encode & Save", command=self.encode_image).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_decode_tab(self):
        # Create decode tab
        self.decode_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.decode_tab, text="Decode")
        
        # Left panel for image preview
        left_frame = ttk.LabelFrame(self.decode_tab, text="Encoded Image", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.decode_canvas = tk.Canvas(left_frame, bg='white', bd=2, relief=tk.SUNKEN)
        self.decode_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right panel for controls
        right_frame = ttk.Frame(self.decode_tab, padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Decoded message
        ttk.Label(right_frame, text="Decoded Message:").pack(anchor=tk.W, pady=(0,5))
        self.decoded_text = tk.Text(right_frame, height=15, width=40, wrap=tk.WORD)
        self.decoded_text.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Load Image", command=self.load_encoded_image).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        ttk.Button(btn_frame, text="Decode", command=self.decode_image).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="Save to File", command=self.save_decoded_to_file).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var.set(file_path)
    
    def load_image(self):
        file_types = [
            ("Image files", "*.png;*.bmp;*.jpg;*.jpeg;*.tiff;*.tif;*.gif;*.webp"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff;*.tif"),
            ("GIF files", "*.gif"),
            ("WebP files", "*.webp"),
            ("All files", "*.*")
        ]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image, self.canvas)
                self.update_status(f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def load_encoded_image(self):
        file_types = [
            ("Image files", "*.png;*.bmp;*.jpg;*.jpeg;*.tiff;*.tif;*.gif;*.webp"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff;*.tif"),
            ("GIF files", "*.gif"),
            ("WebP files", "*.webp"),
            ("All files", "*.*")
        ]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            try:
                self.encoded_image = Image.open(file_path)
                self.display_image(self.encoded_image, self.decode_canvas)
                self.update_status(f"Loaded encoded image: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image, canvas):
        # Resize image to fit canvas while maintaining aspect ratio
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:  # In case canvas not yet rendered
            canvas_width = 400
            canvas_height = 300
        
        img_ratio = image.width / image.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            new_width = canvas_width - 20
            new_height = int(new_width / img_ratio)
        else:
            new_height = canvas_height - 20
            new_width = int(new_height * img_ratio)
        
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)
        
        # Clear canvas and display image
        canvas.delete("all")
        canvas.config(width=new_width, height=new_height)
        canvas.create_image(new_width//2, new_height//2, image=self.photo)
    
    def encode_image(self):
        if not hasattr(self, 'original_image'):
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        # Get message from text widget or file
        message = self.message_text.get("1.0", tk.END).strip()
        file_path = self.file_path_var.get().strip()
        
        if not message and not file_path:
            messagebox.showwarning("Warning", "Please enter a message or select a file to hide!")
            return
        
        try:
            if file_path:
                with open(file_path, 'rb') as f:
                    data = f.read()
                # Add a header to identify this as a file
                filename = os.path.basename(file_path)
                data = f"FILE:{filename}:{len(data)}:".encode() + data
            else:
                data = message.encode()
            
            # Encode the data into the image
            encoded_image = stepic.encode(self.original_image, data)
            
            # Save the encoded image
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("BMP files", "*.bmp"),
                    ("JPEG files", "*.jpg"),
                    ("TIFF files", "*.tiff"),
                    ("WebP files", "*.webp")
                ],
                initialfile=f"encoded_{os.path.basename(self.original_image.filename or 'image.png')}"
            )
            
            if save_path:
                encoded_image.save(save_path)
                self.update_status(f"Image saved successfully: {os.path.basename(save_path)}")
                messagebox.showinfo("Success", "Message successfully encoded and saved!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode message: {str(e)}")
    
    def clean_decoded_data(self, data):
        """Clean up the decoded data by removing any non-printable characters."""
        if not data:
            return ""
        
        # Try to handle binary data that might be in the string
        try:
            # If it's a file header, return as is
            if data.startswith("FILE:"):
                return data
                
            # Try to decode as UTF-8 first
            try:
                cleaned = data.encode('latin-1').decode('utf-8', errors='ignore')
                # Remove any remaining non-printable characters
                cleaned = ''.join(char for char in cleaned if char.isprintable() or char in '\n\r\t')
                return cleaned.strip()
            except:
                pass
                
            # If UTF-8 fails, try other encodings
            for encoding in ['latin-1', 'utf-16', 'ascii']:
                try:
                    cleaned = data.encode('latin-1').decode(encoding, errors='ignore')
                    cleaned = ''.join(char for char in cleaned if char.isprintable() or char in '\n\r\t')
                    if cleaned.strip():
                        return cleaned.strip()
                except:
                    continue
                    
            # If all else fails, return the raw data with non-printable chars removed
            return ''.join(char for char in data if char.isprintable() or char in '\n\r\t').strip()
            
        except Exception as e:
            return f"[Error processing data: {str(e)}]"

    def decode_image(self):
        if not hasattr(self, 'encoded_image'):
            messagebox.showwarning("Warning", "Please load an encoded image first!")
            return
        
        try:
            # Convert the image to RGB mode if it's not already
            if self.encoded_image.mode != 'RGB':
                self.encoded_image = self.encoded_image.convert('RGB')
            
            # Verify the image has enough data to decode
            if self.encoded_image.size[0] * self.encoded_image.size[1] < 100:  # Arbitrary minimum size
                raise ValueError("Image is too small to contain encoded data")
            
            try:
                # Decode the message
                data = stepic.decode(self.encoded_image)
                
                if not data:
                    raise ValueError("No data found in the image")
                
                # Clean the decoded data
                cleaned_data = self.clean_decoded_data(data)
                
                # Check if it's a file
                if cleaned_data.startswith("FILE:"):
                    try:
                        # Parse file header: FILE:filename:size:data
                        parts = cleaned_data.split(":", 3)
                        if len(parts) >= 4:
                            filename = parts[1]
                            try:
                                size = int(parts[2])
                                file_data = parts[3].encode('latin-1')
                                
                                if len(file_data) >= size:
                                    self.decoded_file_data = file_data[:size]
                                    self.decoded_text.delete("1.0", tk.END)
                                    self.decoded_text.insert(tk.END, f"[Binary file detected]\n")
                                    self.decoded_text.insert(tk.END, f"Filename: {filename}\n")
                                    self.decoded_text.insert(tk.END, f"Size: {size} bytes\n")
                                    self.decoded_text.insert(tk.END, "Click 'Save to File' to extract the file.")
                                    self.update_status("Decoded file data. Click 'Save to File' to extract.")
                                    return
                                else:
                                    raise ValueError("File data is corrupted or incomplete")
                            except (ValueError, IndexError) as e:
                                raise ValueError(f"Invalid file format in encoded data: {str(e)}")
                    except Exception as e:
                        # If parsing fails, treat as normal text but log the error
                        self.update_status(f"Warning: {str(e)}. Displaying as text.")
                
                # If not a file or parsing failed, display as text
                self.decoded_text.delete("1.0", tk.END)
                self.decoded_text.insert(tk.END, cleaned_data)
                self.update_status("Message decoded successfully!")
                
            except Exception as e:
                # Try alternative decoding method if the first one fails
                try:
                    # Convert to RGB and try again
                    rgb_image = self.encoded_image.convert('RGB')
                    data = stepic.decode(rgb_image)
                    if data:
                        cleaned_data = self.clean_decoded_data(data)
                        self.decoded_text.delete("1.0", tk.END)
                        self.decoded_text.insert(tk.END, cleaned_data)
                        self.update_status("Message decoded successfully (using alternative method)!")
                        return
                    raise  # Re-raise if still no data
                except Exception as inner_e:
                    # Try one more time with direct binary processing
                    try:
                        # Try to extract the message by looking for printable characters
                        binary_data = stepic.decode(rgb_image).encode('latin-1')
                        # Look for the first null byte as message terminator
                        null_pos = binary_data.find(b'\x00')
                        if null_pos > 0:
                            message = binary_data[:null_pos].decode('utf-8', errors='ignore')
                            cleaned_message = ''.join(char for char in message if char.isprintable() or char in '\n\r\t')
                            if cleaned_message.strip():
                                self.decoded_text.delete("1.0", tk.END)
                                self.decoded_text.insert(tk.END, cleaned_message.strip())
                                self.update_status("Message decoded successfully (using binary method)!")
                                return
                        raise  # Re-raise if all attempts fail
                    except:
                        raise ValueError(f"Failed to decode message. The image may not contain valid steganography data or may be corrupted. Error: {str(inner_e)}")
        
        except Exception as e:
            error_msg = str(e)
            self.decoded_text.delete("1.0", tk.END)
            self.decoded_text.insert(tk.END, f"Error: {error_msg}\n\n")
            self.decoded_text.insert(tk.END, "Possible reasons:\n")
            self.decoded_text.insert(tk.END, "1. The image was not encoded using this tool\n")
            self.decoded_text.insert(tk.END, "2. The image was modified or saved in a lossy format (like JPEG)\n")
            self.decoded_text.insert(tk.END, "3. The image is corrupted or doesn't contain hidden data\n\n")
            self.decoded_text.insert(tk.END, "Try using a PNG or BMP image that was encoded with this tool.")
            self.update_status("Decoding failed. See details above.")
            messagebox.showerror("Decoding Error", f"Failed to decode message: {error_msg}")
    
    def save_decoded_to_file(self):
        if not hasattr(self, 'decoded_file_data'):
            # If no binary data, save text content
            text = self.decoded_text.get("1.0", tk.END)
            if not text.strip():
                messagebox.showwarning("Warning", "No decoded content to save!")
                return
            
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if save_path:
                try:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    self.update_status(f"Text saved to {os.path.basename(save_path)}")
                    messagebox.showinfo("Success", "Text saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            # Save binary file
            save_path = filedialog.asksaveasfilename(
                defaultextension="",
                filetypes=[("All files", "*.*")]
            )
            
            if save_path:
                try:
                    with open(save_path, 'wb') as f:
                        f.write(self.decoded_file_data)
                    self.update_status(f"File saved as {os.path.basename(save_path)}")
                    messagebox.showinfo("Success", "File extracted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    
    # Set application icon (optional)
    try:
        root.iconbitmap("icon.ico")  # You can add an icon file named icon.ico in the same directory
    except:
        pass  # Icon not found, use default
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
