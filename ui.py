import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from barcode_detector import BarcodeDetector
import threading
import sys


class BarcodeDetectorUI:
    """GUI for OCR Barcode Detector"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Barcode Detector")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        # Initialize detector (no blocking operations)
        self.detector = BarcodeDetector()
        self.current_image_path = None
        self.detection_in_progress = False
        
        # Configure style
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass  # Use default theme if clam not available
        
        # Create UI
        self.create_widgets()
        
        # Center window on screen
        self.root.update_idletasks()
        self.center_window()
    
    def create_widgets(self):
        """Create all UI elements"""
        
        # Top Frame - Title and Instructions
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X, pady=0)
        
        title_label = tk.Label(
            title_frame,
            text="OCR Barcode Detector",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel - Image Display
        left_panel = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        image_label = tk.Label(left_panel, text="Image Preview", font=("Arial", 12, "bold"), bg='white')
        image_label.pack(pady=10)
        
        self.image_display = tk.Label(
            left_panel,
            text="No image selected\n\nClick 'Browse Image' to select a barcode image",
            font=("Arial", 10),
            bg='#ecf0f1',
            fg='#7f8c8d',
            width=40,
            height=25,
            relief=tk.SUNKEN
        )
        self.image_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right Panel - Controls and Results
        right_panel = tk.Frame(main_frame, bg='#f0f0f0')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0))
        
        # Buttons Frame
        button_frame = tk.Frame(right_panel, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=10)
        
        # Browse Button
        self.browse_btn = tk.Button(
            button_frame,
            text="📁 Browse Image",
            command=self.browse_image,
            font=("Arial", 11, "bold"),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.browse_btn.pack(fill=tk.X, pady=5)
        
        # Detect Button
        self.detect_btn = tk.Button(
            button_frame,
            text="🔍 Detect Barcode",
            command=self.detect_barcode,
            font=("Arial", 11, "bold"),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.detect_btn.pack(fill=tk.X, pady=5)
        
        # Clear Button
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️  Clear",
            command=self.clear_all,
            font=("Arial", 11, "bold"),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.clear_btn.pack(fill=tk.X, pady=5)
        
        # Results Frame
        results_frame = tk.LabelFrame(
            right_panel,
            text="Detection Results",
            font=("Arial", 11, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # Status Label
        status_label = tk.Label(results_frame, text="Status:", font=("Arial", 10, "bold"), bg='#f0f0f0')
        status_label.pack(anchor=tk.W, pady=(5, 2))
        
        self.status_text = tk.Label(
            results_frame,
            text="Ready",
            font=("Arial", 9),
            bg='#d4edda',
            fg='#155724',
            wraplength=300,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=10,
            pady=8
        )
        self.status_text.pack(fill=tk.X, pady=(0, 10))
        
        # Method Label
        method_label = tk.Label(results_frame, text="Detection Method:", font=("Arial", 10, "bold"), bg='#f0f0f0')
        method_label.pack(anchor=tk.W, pady=(10, 2))
        
        self.method_text = tk.Label(
            results_frame,
            text="N/A",
            font=("Arial", 9),
            bg='#e7f3ff',
            fg='#0c5aa0',
            wraplength=300,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=10,
            pady=8
        )
        self.method_text.pack(fill=tk.X, pady=(0, 10))
        
        # Barcode Content Label
        barcode_label = tk.Label(results_frame, text="Barcode Content:", font=("Arial", 10, "bold"), bg='#f0f0f0')
        barcode_label.pack(anchor=tk.W, pady=(10, 2))
        
        self.barcode_text = tk.Label(
            results_frame,
            text="No barcode detected",
            font=("Courier New", 12, "bold"),
            bg='#fff3cd',
            fg='#856404',
            wraplength=300,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=10,
            pady=12
        )
        self.barcode_text.pack(fill=tk.X, pady=(0, 10))
        
        # Full Output Label
        output_label = tk.Label(results_frame, text="Full Output:", font=("Arial", 10, "bold"), bg='#f0f0f0')
        output_label.pack(anchor=tk.W, pady=(10, 2))
        
        self.output_text = tk.Label(
            results_frame,
            text="Waiting for detection...",
            font=("Courier New", 9),
            bg='#f8f9fa',
            fg='#212529',
            wraplength=300,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=10,
            pady=10
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Loading indicator
        self.loading_label = tk.Label(
            results_frame,
            text="",
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#3498db'
        )
        self.loading_label.pack(pady=5)
    
    def browse_image(self):
        """Open file dialog to select image"""
        file_path = filedialog.askopenfilename(
            title="Select Barcode Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.detect_btn.config(state=tk.NORMAL)
            self.status_text.config(
                text=f"Image loaded: {os.path.basename(file_path)}",
                bg='#d4edda',
                fg='#155724'
            )
    
    def display_image(self, image_path):
        """Display image in the preview area"""
        try:
            image = Image.open(image_path)
            
            # Resize image to fit the display area
            max_width = 350
            max_height = 450
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            self.image_display.config(image=photo, text="")
            self.image_display.image = photo
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not display image: {str(e)}")
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def detect_barcode(self):
        """Detect barcode in selected image"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        
        if self.detection_in_progress:
            messagebox.showwarning("Warning", "Detection already in progress...")
            return
        
        # Disable button and show loading
        self.detection_in_progress = True
        self.detect_btn.config(state=tk.DISABLED)
        self.loading_label.config(text="⏳ Processing... This may take a moment.")
        self.root.update()
        
        # Run detection in separate thread to prevent UI freezing
        thread = threading.Thread(target=self._detect_in_thread, daemon=True)
        thread.start()
    
    def _detect_in_thread(self):
        """Run barcode detection in background thread"""
        try:
            result = self.detector.extract_barcode(self.current_image_path)
            
            # Update UI in main thread
            self.root.after(0, self._update_results, result)
        
        except Exception as e:
            import traceback
            error_msg = f'Error: {str(e)}\n{traceback.format_exc()}'
            self.root.after(0, self._update_results, {
                'success': False,
                'message': error_msg
            })
        finally:
            self.detection_in_progress = False
    
    def _update_results(self, result):
        """Update UI with detection results"""
        self.detect_btn.config(state=tk.NORMAL)
        self.loading_label.config(text="")
        self.detection_in_progress = False
        
        if result['success']:
            barcode_content = result['barcode_content']
            method = result['method']
            
            # Update status
            self.status_text.config(
                text="✓ Barcode detected successfully!",
                bg='#d4edda',
                fg='#155724'
            )
            
            # Update method
            self.method_text.config(
                text=f"Method: {method.upper()}",
                bg='#e7f3ff',
                fg='#0c5aa0'
            )
            
            # Update barcode content
            self.barcode_text.config(
                text=f"b'{barcode_content}'",
                bg='#d4f0d9',
                fg='#0f5d3f',
                font=("Courier New", 11, "bold")
            )
            
            # Update full output
            output_msg = result['message']
            self.output_text.config(
                text=output_msg,
                bg='#f8f9fa',
                fg='#155724'
            )
        
        else:
            self.status_text.config(
                text="✗ No barcode detected",
                bg='#f8d7da',
                fg='#721c24'
            )
            
            self.method_text.config(
                text="N/A",
                bg='#ffe7e7',
                fg='#721c24'
            )
            
            self.barcode_text.config(
                text="No barcode found",
                bg='#f5c6cb',
                fg='#721c24'
            )
            
            self.output_text.config(
                text=result['message'],
                bg='#f8f9fa',
                fg='#721c24'
            )
    
    def clear_all(self):
        """Clear all selections and results"""
        self.current_image_path = None
        self.image_display.config(
            image='',
            text="No image selected\n\nClick 'Browse Image' to select a barcode image",
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.image_display.image = None
        
        self.status_text.config(
            text="Ready",
            bg='#d4edda',
            fg='#155724'
        )
        
        self.method_text.config(text="N/A")
        self.barcode_text.config(text="No barcode detected")
        self.output_text.config(text="Waiting for detection...")
        
        self.detect_btn.config(state=tk.DISABLED)
        self.loading_label.config(text="")
        self.detection_in_progress = False


def main():
    try:
        root = tk.Tk()
        app = BarcodeDetectorUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
