# coding=utf-8
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import json
import os
import sys

class SettingsDialog:
    def __init__(self, parent, config, save_callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Cài đặt")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.config = config.copy()
        self.save_callback = save_callback
        
        # Style cho dialog
        style = ttk.Style()
        if self.config["theme"] == "dark":
            self.dialog.configure(bg="#2E2E2E")
            style.configure("Settings.TFrame", background="#2E2E2E")
            style.configure("Settings.TLabel", background="#2E2E2E", foreground="#FFFFFF")
            style.configure("Settings.TLabelframe", background="#2E2E2E", foreground="#FFFFFF")
            style.configure("Settings.TLabelframe.Label", background="#2E2E2E", foreground="#FFFFFF")
            style.configure("Settings.TButton", background="#000000", foreground="#FFFFFF")
            # Nút Lưu màu xanh, Hủy màu đỏ với nền đen
            style.configure("Save.TButton", background="#000000", foreground="#28a745")
            style.configure("Cancel.TButton", background="#000000", foreground="#dc3545")
        
        # Notebook để tạo các tab
        self.notebook = ttk.Notebook(self.dialog)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab Giao diện
        self.create_appearance_tab()
        
        # Tab Phím tắt
        self.create_hotkeys_tab()
        
        # Nút lưu và hủy
        btn_frame = ttk.Frame(self.dialog, style="Settings.TFrame")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(btn_frame, text="Lưu", command=self.save, style="Save.TButton", width=10).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Hủy", command=self.dialog.destroy, style="Cancel.TButton", width=10).pack(side=tk.RIGHT)

    def create_appearance_tab(self):
        tab = ttk.Frame(self.notebook, style="Settings.TFrame")
        self.notebook.add(tab, text="Giao diện")
        
        # Frame chính
        main_frame = ttk.Frame(tab, style="Settings.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Chọn theme
        theme_frame = ttk.LabelFrame(main_frame, text="Giao diện", style="Settings.TLabelframe")
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.theme_var = tk.StringVar(value=self.config["theme"])
        ttk.Radiobutton(
            theme_frame,
            text="Tối",
            value="dark",
            variable=self.theme_var,
            command=self.preview_theme,
            style="Settings.TRadiobutton"
        ).pack(side=tk.LEFT, padx=20, pady=5)
        ttk.Radiobutton(
            theme_frame,
            text="Sáng",
            value="light",
            variable=self.theme_var,
            command=self.preview_theme,
            style="Settings.TRadiobutton"
        ).pack(side=tk.LEFT, padx=20, pady=5)
        
        # Cỡ chữ và độ trong suốt
        controls_frame = ttk.LabelFrame(main_frame, text="Điều chỉnh hiển thị", style="Settings.TLabelframe")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Cỡ chữ
        font_frame = ttk.Frame(controls_frame, style="Settings.TFrame")
        font_frame.pack(fill=tk.X, padx=20, pady=(5,0))
        ttk.Label(font_frame, text="Cỡ chữ:", style="Settings.TLabel").pack(side=tk.LEFT)
        self.font_var = tk.IntVar(value=self.config["font_size"])
        self.font_label = ttk.Label(font_frame, text=str(self.font_var.get()), style="Settings.TLabel", width=3)
        self.font_label.pack(side=tk.RIGHT)
        
        font_scale = ttk.Scale(
            controls_frame,
            from_=8,
            to=20,
            variable=self.font_var,
            command=self.on_font_change
        )
        font_scale.pack(fill=tk.X, padx=20, pady=5)
        
        # Độ trong suốt
        opacity_frame = ttk.Frame(controls_frame, style="Settings.TFrame")
        opacity_frame.pack(fill=tk.X, padx=20, pady=(5,0))
        ttk.Label(opacity_frame, text="Độ trong suốt:", style="Settings.TLabel").pack(side=tk.LEFT)
        self.opacity_var = tk.DoubleVar(value=self.config["opacity"])
        self.opacity_label = ttk.Label(opacity_frame, text=f"{int(self.opacity_var.get()*100)}%", style="Settings.TLabel", width=4)
        self.opacity_label.pack(side=tk.RIGHT)
        
        opacity_scale = ttk.Scale(
            controls_frame,
            from_=0.1,
            to=1.0,
            variable=self.opacity_var,
            command=self.on_opacity_change
        )
        opacity_scale.pack(fill=tk.X, padx=20, pady=5)
        
        # Số dòng hiển thị
        lines_frame = ttk.Frame(controls_frame, style="Settings.TFrame")
        lines_frame.pack(fill=tk.X, padx=20, pady=(5,0))
        ttk.Label(lines_frame, text="Số dòng mỗi trang:", style="Settings.TLabel").pack(side=tk.LEFT)
        self.lines_var = tk.IntVar(value=self.config["lines_per_page"])
        self.lines_label = ttk.Label(lines_frame, text=str(self.lines_var.get()), style="Settings.TLabel", width=3)
        self.lines_label.pack(side=tk.RIGHT)
        
        lines_scale = ttk.Scale(
            controls_frame,
            from_=3,
            to=10,
            variable=self.lines_var,
            command=self.on_lines_change
        )
        lines_scale.pack(fill=tk.X, padx=20, pady=5)
        
        # Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Xem trước", style="Settings.TLabelframe")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.preview_label = ttk.Label(
            preview_frame,
            text="LINE (L) - Vẽ đường thẳng\nCIRCLE (C) - Vẽ đường tròn",
            style="Settings.TLabel",
            justify=tk.LEFT
        )
        self.preview_label.pack(padx=20, pady=10)
    
    def create_hotkeys_tab(self):
        tab = ttk.Frame(self.notebook, style="Settings.TFrame")
        self.notebook.add(tab, text="Phím tắt")
        
        # Phím lùi
        prev_frame = ttk.LabelFrame(tab, text="Phím lùi trang", style="Settings.TLabelframe")
        prev_frame.pack(fill=tk.X, padx=10, pady=5)
        self.prev_key_var = tk.StringVar(value=self.config["prev_key"])
        ttk.Label(prev_frame, textvariable=self.prev_key_var, style="Settings.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Button(prev_frame, text="Thay đổi", command=lambda: self.change_hotkey("prev_key")).pack(side=tk.RIGHT, padx=10)
        
        # Phím tiến
        next_frame = ttk.LabelFrame(tab, text="Phím tiến trang", style="Settings.TLabelframe")
        next_frame.pack(fill=tk.X, padx=10, pady=5)
        self.next_key_var = tk.StringVar(value=self.config["next_key"])
        ttk.Label(next_frame, textvariable=self.next_key_var, style="Settings.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Button(next_frame, text="Thay đổi", command=lambda: self.change_hotkey("next_key")).pack(side=tk.RIGHT, padx=10)
    
    def on_font_change(self, value):
        size = int(float(value))
        self.font_label.configure(text=str(size))
        self.preview_label.configure(font=("Arial", size))
        
    def on_opacity_change(self, value):
        opacity = float(value)
        self.opacity_label.configure(text=f"{int(opacity*100)}%")
        self.dialog.attributes('-alpha', opacity)
    
    def preview_theme(self):
        theme = self.theme_var.get()
        if theme == "dark":
            self.preview_label.configure(style="Settings.TLabel")
        else:
            self.preview_label.configure(style="")
    
    def on_lines_change(self, value):
        lines = int(float(value))
        self.lines_label.configure(text=str(lines))
        # Cập nhật xem trước với số dòng mới
        preview_text = "\n".join([f"LINE {i+1} - Dòng mẫu {i+1}" for i in range(lines)])
        self.preview_label.configure(text=preview_text)
    
    def save(self):
        self.config.update({
            "theme": self.theme_var.get(),
            "opacity": self.opacity_var.get(),
            "font_size": self.font_var.get(),
            "lines_per_page": self.lines_var.get(),
        })
        self.save_callback(self.config)
        self.dialog.destroy()
        
    def change_hotkey(self, key_type):
        dialog = HotkeyDialog(self.dialog)
        self.dialog.wait_window(dialog.dialog)
        if dialog.result:
            self.config[key_type] = dialog.result.lower()
            if key_type == "prev_key":
                self.prev_key_var.set(dialog.result.lower())
            else:
                self.next_key_var.set(dialog.result.lower())

class HotkeyDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Cài đặt phím tắt")
        self.dialog.geometry("300x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.result = None
        self.keys = []
        
        ttk.Label(self.dialog, text="Nhấn tổ hợp phím bạn muốn sử dụng\nVí dụ: Ctrl + 1, Alt + S,...").pack(pady=10)
        self.key_label = ttk.Label(self.dialog, text="")
        self.key_label.pack(pady=10)
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="OK", command=self.ok, style="Settings.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Hủy", command=self.cancel, style="Settings.TButton").pack(side=tk.LEFT, padx=5)
        
        self.dialog.bind('<KeyPress>', self.on_key_press)
        self.dialog.bind('<KeyRelease>', self.on_key_release)
        
    def on_key_press(self, event):
        if event.keysym not in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
            key = []
            if event.state & 0x4:
                key.append('Ctrl')
            if event.state & 0x1:
                key.append('Shift')
            if event.state & 0x8:
                key.append('Alt')
            key.append(event.keysym)
            self.keys = key
            self.key_label.config(text=" + ".join(self.keys))
    
    def on_key_release(self, event):
        if len(self.keys) > 0:
            self.result = "+".join(self.keys)
    
    def ok(self):
        self.dialog.destroy()
        
    def cancel(self):
        self.result = None
        self.dialog.destroy()

class AutoCADHelper:
    def __init__(self):
        self.current_page = 0
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.bat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start_helper.bat")
        self.startup_path = os.path.join(
            os.getenv('APPDATA'),
            r'Microsoft\Windows\Start Menu\Programs\Startup\AutoCADHelper.lnk'
        )
        self.load_config()
        self.commands_source = [
            # Trang 1: Lệnh vẽ cơ bản
            [
                "LINE (L) - Vẽ đường thẳng",
                "CIRCLE (C) - Vẽ đường tròn",
                "RECTANGLE (REC) - Vẽ hình chữ nhật",
                "ARC (A) - Vẽ cung tròn",
                "POLYLINE (PL) - Vẽ đường đa tuyến"
            ],
            # Trang 2: Chỉnh sửa đối tượng
            [
                "MOVE (M) - Di chuyển đối tượng",
                "COPY (CO) - Sao chép đối tượng",
                "ROTATE (RO) - Xoay đối tượng",
                "SCALE (SC) - Thay đổi tỷ lệ",
                "STRETCH (S) - Kéo giãn đối tượng"
            ],
            # Trang 3: Sửa đổi nâng cao
            [
                "TRIM (TR) - Cắt đối tượng",
                "EXTEND (EX) - Kéo dài đối tượng",
                "FILLET (F) - Bo tròn góc",
                "CHAMFER (CHA) - Vát góc",
                "OFFSET (O) - Tạo đối tượng song song"
            ],
            # Trang 4: Công cụ đo lường
            [
                "DISTANCE (DI) - Đo khoảng cách",
                "AREA (AREA) - Tính diện tích",
                "LIST (LI) - Xem thông tin đối tượng",
                "ALIGN (AL) - Căn chỉnh đối tượng",
                "MEASURE (ME) - Đo đạc"
            ],
            # Trang 5: Layer và thuộc tính
            [
                "LAYER (LA) - Quản lý layer",
                "MATCHPROP (MA) - Sao chép thuộc tính",
                "PROPERTIES (PR) - Bảng thuộc tính",
                "COLOR (COL) - Đổi màu",
                "LINETYPE (LT) - Đổi loại đường"
            ],
            # Trang 6: Text và Dimension
            [
                "TEXT (T) - Thêm văn bản",
                "MTEXT (MT) - Văn bản nhiều dòng",
                "DIMLINEAR (DLI) - Dim đường thẳng",
                "DIMALIGNED (DAL) - Dim theo góc",
                "DIMRADIUS (DRA) - Dim bán kính"
            ],
            # Trang 7: Block và Reference
            [
                "BLOCK (B) - Tạo block",
                "INSERT (I) - Chèn block",
                "XREF (XR) - Tham chiếu ngoài",
                "EXPLODE (X) - Phá vỡ block",
                "WBLOCK (W) - Xuất block"
            ],
            # Trang 8: Công cụ hỗ trợ
            [
                "ORTHO (F8) - Bật/tắt vẽ vuông góc",
                "SNAP (F9) - Bật/tắt bắt điểm",
                "GRID (F7) - Bật/tắt lưới",
                "OSNAP (F3) - Thiết lập bắt điểm",
                "UCS (UC) - Hệ tọa độ người dùng"
            ]
        ]
        
        # Lưu danh sách lệnh gốc và tổ chức lại theo số dòng cấu hình
        self.commands = []
        all_commands = []
        for group in self.commands_source:
            all_commands.extend(group)
        
        lines_per_page = self.config["lines_per_page"]
        self.commands = [
            all_commands[i:i + lines_per_page]
            for i in range(0, len(all_commands), lines_per_page)
        ]
        
        self.setup_window()
        self.setup_keyboard()
        
    def load_config(self):
        # Cấu hình mặc định
        self.config = {
            "prev_key": "ctrl+left",
            "next_key": "ctrl+right",
            "opacity": 0.95,
            "bg_color": "#2E2E2E",
            "text_color": "#FFFFFF",
            "font_size": 10,
            "lines_per_page": 5,
            "window_position": {
                "x": 100,
                "y": 100
            },
            "window_size": {
                "width": 350,
                "height": 300
            },
            "theme": "dark"
        }
        
        # Đọc cấu hình từ file nếu có
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except:
                pass
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def setup_window(self):
        self.root = tk.Tk()
        self.root.title("AutoCAD Helper")
        
        # Thiết lập cửa sổ
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.config["opacity"])
        
        # Thiết lập kích thước và vị trí cửa sổ
        window_width = self.config["window_size"]["width"]
        window_height = self.config["window_size"]["height"]
        x = self.config["window_position"]["x"]
        y = self.config["window_position"]["y"]
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Thiết lập style
        style = ttk.Style()
        if self.config["theme"] == "dark":
            # Cấu hình màu nền đen cho cửa sổ chính
            self.root.configure(bg="#000000")
            self.config["bg_color"] = "#000000"
            
            # Style cho frame và label
            style.configure("Custom.TFrame", background="#000000")
            style.configure(
                "Custom.TLabel",
                font=("Arial", self.config["font_size"]),
                background="#000000",
                foreground=self.config["text_color"]
            )
            style.configure(
                "Custom.TButton",
                background="#000000",
                foreground=self.config["text_color"]
            )
        else:
            style.configure(
                "Custom.TLabel",
                font=("Arial", self.config["font_size"])
            )
            style.configure(
                "Custom.TButton",
                background="#000000",
                foreground="#FFFFFF"
            )
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label hiển thị số trang
        self.page_label = ttk.Label(
            self.main_frame,
            style="Custom.TLabel",
            font=("Arial", self.config["font_size"], "bold")
        )
        self.page_label.pack(pady=(0, 10))
        
        # Frame chứa danh sách lệnh
        self.commands_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.commands_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bind chuột phải để hiện menu
        self.root.bind('<Button-3>', self.show_context_menu)
        
        # Bind sự kiện thay đổi kích thước cửa sổ
        self.root.bind('<Configure>', self.on_window_configure)
    
    def setup_keyboard(self):
        try:
            keyboard.remove_hotkey(self.config["prev_key"])
            keyboard.remove_hotkey(self.config["next_key"])
        except:
            pass
        
        keyboard.add_hotkey(self.config["prev_key"], self.prev_page)
        keyboard.add_hotkey(self.config["next_key"], self.next_page)
    
    def show_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(
            label="Tự động khởi động ✓" if os.path.exists(self.startup_path) else "Tự động khởi động",
            command=self.toggle_startup
        )
        menu.add_command(label="Cài đặt...", command=self.show_settings)
        menu.add_separator()
        menu.add_command(label="Thoát", command=self.root.quit)
        menu.tk_popup(event.x_root, event.y_root)
        
    def show_settings(self):
        dialog = SettingsDialog(self.root, self.config, self.apply_settings)
        self.root.wait_window(dialog.dialog)
    
    def apply_settings(self, new_config):
        # Lưu cấu hình mới
        self.config.update(new_config)
        self.save_config()
        
        # Áp dụng theme
        style = ttk.Style()
        if self.config["theme"] == "dark":
            self.root.configure(bg="#000000")
            self.config["bg_color"] = "#000000"
            
            # Style cho frame và label
            style.configure("Custom.TFrame", background="#000000")
            style.configure(
                "Custom.TLabel",
                font=("Arial", self.config["font_size"]),
                background="#000000",
                foreground=self.config["text_color"]
            )
        else:
            self.root.configure(bg="SystemButtonFace")
            style.configure(
                "Custom.TLabel",
                font=("Arial", self.config["font_size"]),
                background="SystemButtonFace",
                foreground="SystemWindowText"
            )
            style.configure("Custom.TFrame", background="SystemButtonFace")
        
        # Tổ chức lại lệnh theo số dòng mới
        self.reorganize_commands()
        
        # Áp dụng độ trong suốt
        self.root.attributes('-alpha', self.config["opacity"])
        
        # Cập nhật phím tắt
        self.setup_keyboard()
        
        # Cập nhật hiển thị
        self.update_commands()
    
    def toggle_startup(self):
        if os.path.exists(self.startup_path):
            os.remove(self.startup_path)
            messagebox.showinfo("Thông báo", "Đã tắt tự động khởi động")
        else:
            try:
                import winshell
                from win32com.client import Dispatch
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(self.startup_path)
                shortcut.Targetpath = self.bat_path
                shortcut.WorkingDirectory = os.path.dirname(self.bat_path)
                shortcut.save()
                messagebox.showinfo("Thông báo", "Đã bật tự động khởi động")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo shortcut: {str(e)}")
    
    def on_window_configure(self, event=None):
        if event and event.widget == self.root:
            # Lưu kích thước mới
            self.config["window_size"] = {
                "width": self.root.winfo_width(),
                "height": self.root.winfo_height()
            }
            # Lưu vị trí mới
            self.config["window_position"] = {
                "x": self.root.winfo_x(),
                "y": self.root.winfo_y()
            }
            self.save_config()
    
    def reorganize_commands(self):
        # Tổ chức lại danh sách lệnh dựa trên số dòng mỗi trang
        lines_per_page = self.config["lines_per_page"]
        all_commands = []
        for group in self.commands:
            all_commands.extend(group)
        
        # Chia thành các nhóm mới theo số dòng mỗi trang
        self.commands = [
            all_commands[i:i + lines_per_page]
            for i in range(0, len(all_commands), lines_per_page)
        ]
        
        # Đảm bảo trang hiện tại hợp lệ
        if self.current_page >= len(self.commands):
            self.current_page = len(self.commands) - 1
    
    def update_commands(self):
        # Xóa tất cả widgets cũ trong commands_frame
        for widget in self.commands_frame.winfo_children():
            widget.destroy()
            
        # Hiển thị các lệnh của trang hiện tại
        for cmd in self.commands[self.current_page]:
            label = ttk.Label(
                self.commands_frame,
                text=cmd,
                style="Custom.TLabel"
            )
            label.pack(anchor=tk.W, pady=2)
            
            # Thêm hiệu ứng hover nếu đang ở theme tối
            if self.config["theme"] == "dark":
                label.bind('<Enter>', lambda e, l=label: l.configure(foreground="#00FF00"))
                label.bind('<Leave>', lambda e, l=label: l.configure(foreground=self.config["text_color"]))
        
        # Cập nhật label số trang
        self.page_label.config(text=f"Trang {self.current_page + 1}/{len(self.commands)}")
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_commands()
    
    def next_page(self):
        if self.current_page < len(self.commands) - 1:
            self.current_page += 1
            self.update_commands()
    
    def run(self):
        self.update_commands()
        self.root.mainloop()

if __name__ == "__main__":
    app = AutoCADHelper()
    app.run()
