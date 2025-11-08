#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AutoCAD Helper
-------------

Ứng dụng hỗ trợ hiển thị các lệnh AutoCAD thông dụng với giao diện trong suốt
và khả năng tùy chỉnh cao.

Author: lastnight0305
License: MIT
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import json
import os
import sys
import pyautogui

class SettingsDialog:
    def __init__(self, app, parent, config, command_groups, save_callback):
        self.app = app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚙️ Cài đặt - AutoCAD Helper")
        self.dialog.geometry("720x680")
        self.dialog.minsize(650, 600)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.config = config.copy()
        self.command_groups = command_groups.copy()
        self.save_callback = save_callback
        self.command_lists = {}
        
        # Apply modern styling
        self.setup_modern_styles()
        
        # Create main container with padding
        container = ttk.Frame(self.dialog, style="Container.TFrame")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(container)
        
        # Content area with notebook
        self.notebook = ttk.Notebook(container, style="Modern.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Create tabs
        self.create_appearance_tab()
        self.create_customization_tab()
        self.create_hotkeys_tab()
        self.create_command_groups_tab()
        
        # Footer with action buttons
        self.create_footer(container)
        
    def setup_modern_styles(self):
        """Setup modern Windows 11 inspired styles"""
        style = ttk.Style()
        
        # Determine color scheme
        is_dark = self.config["theme"] == "dark"
        
        # Modern color palette
        if is_dark:
            bg_primary = "#202020"
            bg_secondary = "#2b2b2b"
            bg_tertiary = "#323232"
            fg_primary = "#FFFFFF"
            fg_secondary = "#B0B0B0"
            accent = "#60CDFF"
            hover_bg = "#3a3a3a"
            border_color = "#3f3f3f"
        else:
            bg_primary = "#F3F3F3"
            bg_secondary = "#FFFFFF"
            bg_tertiary = "#FAFAFA"
            fg_primary = "#1F1F1F"
            fg_secondary = "#605E5C"
            accent = "#0078D4"
            hover_bg = "#E5E5E5"
            border_color = "#EDEBE9"
        
        self.colors = {
            'bg_primary': bg_primary,
            'bg_secondary': bg_secondary,
            'bg_tertiary': bg_tertiary,
            'fg_primary': fg_primary,
            'fg_secondary': fg_secondary,
            'accent': accent,
            'hover_bg': hover_bg,
            'border': border_color,
            'success': '#107C10',
            'danger': '#D13438'
        }
        
        # Configure dialog background
        self.dialog.configure(bg=bg_primary)
        
        # Container styles
        style.configure("Container.TFrame", background=bg_primary)
        style.configure("Card.TFrame", background=bg_secondary, relief="flat")
        style.configure("Section.TFrame", background=bg_secondary)
        
        # Label styles
        style.configure("Header.TLabel", 
                       background=bg_primary,
                       foreground=fg_primary,
                       font=("Segoe UI", 20, "bold"))
        style.configure("SectionTitle.TLabel",
                       background=bg_secondary,
                       foreground=fg_primary,
                       font=("Segoe UI", 12, "bold"))
        style.configure("Modern.TLabel",
                       background=bg_secondary,
                       foreground=fg_primary,
                       font=("Segoe UI", 10))
        style.configure("SubText.TLabel",
                       background=bg_secondary,
                       foreground=fg_secondary,
                       font=("Segoe UI", 9))
        style.configure("Value.TLabel",
                       background=bg_secondary,
                       foreground=accent,
                       font=("Segoe UI Semibold", 10))
        style.configure("Preview.TLabel",
                       background=bg_tertiary,
                       foreground=fg_primary,
                       font=("Segoe UI", 10),
                       padding=15,
                       relief="flat")
        
        # Button styles
        style.configure("Accent.TButton",
                       background=accent,
                       foreground="#FFFFFF",
                       borderwidth=0,
                       relief="flat",
                       font=("Segoe UI Semibold", 10),
                       padding=(20, 8))
        style.map("Accent.TButton",
                 background=[('active', '#005A9E' if not is_dark else '#4FB3E8')])
        
        style.configure("Secondary.TButton",
                       background=bg_tertiary,
                       foreground=fg_primary,
                       borderwidth=0,
                       relief="flat",
                       font=("Segoe UI", 10),
                       padding=(20, 8))
        style.map("Secondary.TButton",
                 background=[('active', hover_bg)])
        
        # Notebook styles
        style.configure("Modern.TNotebook", background=bg_primary, borderwidth=0)
        style.configure("Modern.TNotebook.Tab",
                       background=bg_secondary,
                       foreground=fg_secondary,
                       padding=(20, 10),
                       borderwidth=0,
                       font=("Segoe UI", 10))
        style.map("Modern.TNotebook.Tab",
                 background=[('selected', bg_primary)],
                 foreground=[('selected', accent)])
        
        # Checkbutton and Radiobutton styles
        style.configure("Modern.TCheckbutton",
                       background=bg_secondary,
                       foreground=fg_primary,
                       font=("Segoe UI", 10))
        style.configure("Modern.TRadiobutton",
                       background=bg_secondary,
                       foreground=fg_primary,
                       font=("Segoe UI", 10))
        
        # Entry styles - Fix white-on-white contrast issue
        style.configure("TEntry",
                       fieldbackground=bg_tertiary,  # Dark gray background
                       foreground=fg_primary,         # White text in dark mode, dark text in light mode
                       bordercolor=border_color,
                       lightcolor=border_color,
                       darkcolor=border_color,
                       insertcolor=fg_primary,        # Cursor color matches text
                       font=("Segoe UI", 10))
        style.map("TEntry",
                 fieldbackground=[('focus', bg_tertiary)],
                 foreground=[('focus', fg_primary)],
                 bordercolor=[('focus', accent)])
        
        # Combobox styles - Ensure proper contrast
        style.configure("TCombobox",
                       fieldbackground=bg_tertiary,
                       foreground=fg_primary,
                       background=bg_tertiary,
                       bordercolor=border_color,
                       arrowcolor=fg_primary,
                       insertcolor=fg_primary,
                       font=("Segoe UI", 10))
        style.map("TCombobox",
                 fieldbackground=[('readonly', bg_tertiary), ('focus', bg_tertiary)],
                 foreground=[('readonly', fg_primary), ('focus', fg_primary)],
                 background=[('readonly', bg_tertiary)],
                 bordercolor=[('focus', accent)])
        
        # LabelFrame style
        style.configure("Modern.TLabelframe",
                       background=bg_secondary,
                       borderwidth=0,
                       relief="flat")
        style.configure("Modern.TLabelframe.Label",
                       background=bg_secondary,
                       foreground=fg_primary,
                       font=("Segoe UI Semibold", 11))
        
    def create_header(self, parent):
        """Create modern header section"""
        header = ttk.Frame(parent, style="Container.TFrame")
        header.pack(fill=tk.X, padx=20, pady=(20, 15))
        
        title = ttk.Label(header, text="Cài đặt", style="Header.TLabel")
        title.pack(side=tk.LEFT)
        
    def create_footer(self, parent):
        """Create footer with action buttons"""
        footer = ttk.Frame(parent, style="Container.TFrame")
        footer.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Separator line
        separator = ttk.Frame(footer, height=1, style="Container.TFrame")
        separator.configure(relief="sunken")
        separator.pack(fill=tk.X, pady=(0, 15))
        
        # Button container
        btn_container = ttk.Frame(footer, style="Container.TFrame")
        btn_container.pack(fill=tk.X)
        
        ttk.Button(btn_container, 
                  text="✓ Lưu thay đổi", 
                  command=self.save, 
                  style="Accent.TButton").pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(btn_container, 
                  text="Hủy bỏ", 
                  command=self.dialog.destroy, 
                  style="Secondary.TButton").pack(side=tk.RIGHT)

    def create_appearance_tab(self):
        """Create modern appearance settings tab"""
        tab = ttk.Frame(self.notebook, style="Container.TFrame")
        self.notebook.add(tab, text="🎨 Giao diện")
        
        # Scrollable container
        canvas = tk.Canvas(tab, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Container.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # === INTERFACE SECTION ===
        interface_card = self.create_card(scrollable_frame, "Giao diện")
        
        # Theme selector with modern toggle
        theme_container = ttk.Frame(interface_card, style="Section.TFrame")
        theme_container.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(theme_container, 
                 text="Chế độ hiển thị", 
                 style="Modern.TLabel").pack(anchor=tk.W, pady=(0, 8))
        
        # Custom theme toggle
        toggle_frame = ttk.Frame(theme_container, style="Section.TFrame")
        toggle_frame.pack(fill=tk.X)
        
        self.theme_var = tk.StringVar(value=self.config["theme"])
        
        dark_btn = tk.Frame(toggle_frame, 
                           bg=self.colors['accent'] if self.theme_var.get() == "dark" else self.colors['bg_tertiary'],
                           cursor="hand2")
        dark_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        dark_label = tk.Label(dark_btn, 
                             text="🌙 Tối", 
                             bg=self.colors['accent'] if self.theme_var.get() == "dark" else self.colors['bg_tertiary'],
                             fg="#FFFFFF" if self.theme_var.get() == "dark" else self.colors['fg_primary'],
                             font=("Segoe UI", 10, "bold" if self.theme_var.get() == "dark" else "normal"),
                             padx=30, pady=10, cursor="hand2")
        dark_label.pack()
        dark_label.bind("<Button-1>", lambda e: self.toggle_theme("dark", dark_btn, light_btn))
        dark_btn.bind("<Button-1>", lambda e: self.toggle_theme("dark", dark_btn, light_btn))
        
        light_btn = tk.Frame(toggle_frame,
                            bg=self.colors['accent'] if self.theme_var.get() == "light" else self.colors['bg_tertiary'],
                            cursor="hand2")
        light_btn.pack(side=tk.LEFT)
        
        light_label = tk.Label(light_btn,
                              text="☀️ Sáng",
                              bg=self.colors['accent'] if self.theme_var.get() == "light" else self.colors['bg_tertiary'],
                              fg="#FFFFFF" if self.theme_var.get() == "light" else self.colors['fg_primary'],
                              font=("Segoe UI", 10, "bold" if self.theme_var.get() == "light" else "normal"),
                              padx=30, pady=10, cursor="hand2")
        light_label.pack()
        light_label.bind("<Button-1>", lambda e: self.toggle_theme("light", dark_btn, light_btn))
        light_btn.bind("<Button-1>", lambda e: self.toggle_theme("light", dark_btn, light_btn))
        
        self.dark_toggle_widgets = (dark_btn, dark_label)
        self.light_toggle_widgets = (light_btn, light_label)
        
        # === DISPLAY ADJUSTMENT SECTION ===
        adjust_card = self.create_card(scrollable_frame, "Điều chỉnh hiển thị")
        
        # Font size slider
        self.create_modern_slider(
            adjust_card,
            "Cỡ chữ",
            "Điều chỉnh kích thước văn bản trong ứng dụng",
            8, 20,
            self.config["font_size"],
            lambda v: f"{int(float(v))} px",
            self.on_font_change
        )
        
        # Opacity slider
        self.create_modern_slider(
            adjust_card,
            "Độ trong suốt",
            "Điều chỉnh độ mờ của cửa sổ (càng thấp càng trong suốt)",
            0.3, 1.0,
            self.config["opacity"],
            lambda v: f"{int(float(v)*100)}%",
            self.on_opacity_change
        )
        
        # Lines per page slider
        self.create_modern_slider(
            adjust_card,
            "Số dòng mỗi trang",
            "Số lượng lệnh hiển thị trên mỗi trang",
            3, 10,
            self.config["lines_per_page"],
            lambda v: f"{int(float(v))} dòng",
            self.on_lines_change
        )
        
        # === PREVIEW SECTION ===
        preview_card = self.create_card(scrollable_frame, "Xem trước")
        
        # Preview area with rounded corners effect
        preview_container = ttk.Frame(preview_card, style="Section.TFrame")
        preview_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        preview_bg = tk.Frame(preview_container, 
                             bg=self.colors['bg_tertiary'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        preview_bg.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.preview_label = tk.Label(
            preview_bg,
            text="LINE (L) - Vẽ đường thẳng\nCIRCLE (C) - Vẽ đường tròn\nARC (A) - Vẽ cung tròn",
            bg=self.colors['bg_tertiary'],
            fg=self.colors['fg_primary'],
            font=("Segoe UI", self.config["font_size"]),
            justify=tk.LEFT,
            padx=20,
            pady=15
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        
        # Info text
        info_label = ttk.Label(preview_container,
                              text="💡 Các thay đổi sẽ được áp dụng ngay lập tức",
                              style="SubText.TLabel")
        info_label.pack(pady=(10, 0))
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=15)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def create_card(self, parent, title):
        """Create a modern card container"""
        card_container = ttk.Frame(parent, style="Container.TFrame")
        card_container.pack(fill=tk.X, pady=(0, 20))
        
        card = ttk.Frame(card_container, style="Card.TFrame")
        card.pack(fill=tk.X, padx=2, pady=2)
        
        # Card header
        header = ttk.Frame(card, style="Section.TFrame")
        header.pack(fill=tk.X, padx=20, pady=(20, 15))
        
        ttk.Label(header, text=title, style="SectionTitle.TLabel").pack(anchor=tk.W)
        
        # Card content
        content = ttk.Frame(card, style="Section.TFrame")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        return content
    
    def create_modern_slider(self, parent, label, description, from_val, to_val, current_val, format_func, callback):
        """Create a modern slider with label and value display"""
        container = ttk.Frame(parent, style="Section.TFrame")
        container.pack(fill=tk.X, pady=(0, 25))
        
        # Header row with label and value
        header = ttk.Frame(container, style="Section.TFrame")
        header.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(header, text=label, style="Modern.TLabel").pack(side=tk.LEFT)
        
        # Value display
        value_var = tk.DoubleVar(value=current_val) if isinstance(current_val, float) else tk.IntVar(value=current_val)
        value_label = ttk.Label(header, text=format_func(current_val), style="Value.TLabel")
        value_label.pack(side=tk.RIGHT)
        
        # Description
        if description:
            ttk.Label(container, text=description, style="SubText.TLabel").pack(anchor=tk.W, pady=(0, 8))
        
        # Modern slider
        slider = ttk.Scale(
            container,
            from_=from_val,
            to=to_val,
            variable=value_var,
            command=lambda v: self.on_slider_change(v, value_label, format_func, callback)
        )
        slider.pack(fill=tk.X)
        
        # Store reference for later use
        if label == "Cỡ chữ":
            self.font_var = value_var
            self.font_label = value_label
        elif label == "Độ trong suốt":
            self.opacity_var = value_var
            self.opacity_label = value_label
        elif label == "Số dòng mỗi trang":
            self.lines_var = value_var
            self.lines_label = value_label
    
    def on_slider_change(self, value, label, format_func, callback):
        """Handle slider value changes"""
        label.configure(text=format_func(value))
        if callback:
            callback(value)
    
    def toggle_theme(self, theme, dark_btn, light_btn):
        """Toggle between dark and light themes with animation"""
        self.theme_var.set(theme)
        
        # Update button states
        if theme == "dark":
            dark_btn.configure(bg=self.colors['accent'])
            dark_btn.winfo_children()[0].configure(
                bg=self.colors['accent'],
                fg="#FFFFFF",
                font=("Segoe UI", 10, "bold")
            )
            light_btn.configure(bg=self.colors['bg_tertiary'])
            light_btn.winfo_children()[0].configure(
                bg=self.colors['bg_tertiary'],
                fg=self.colors['fg_primary'],
                font=("Segoe UI", 10, "normal")
            )
        else:
            light_btn.configure(bg=self.colors['accent'])
            light_btn.winfo_children()[0].configure(
                bg=self.colors['accent'],
                fg="#FFFFFF",
                font=("Segoe UI", 10, "bold")
            )
            dark_btn.configure(bg=self.colors['bg_tertiary'])
            dark_btn.winfo_children()[0].configure(
                bg=self.colors['bg_tertiary'],
                fg=self.colors['fg_primary'],
                font=("Segoe UI", 10, "normal")
            )
    
    def on_font_change(self, value):
        """Handle font size changes with live preview"""
        size = int(float(value))
        self.preview_label.configure(font=("Segoe UI", size))
        
    def on_opacity_change(self, value):
        """Handle opacity changes with live preview"""
        opacity = float(value)
        self.dialog.attributes('-alpha', opacity)
    
    def on_lines_change(self, value):
        """Handle lines per page changes with live preview"""
        lines = int(float(value))
        # Update preview with dynamic number of lines
        sample_commands = [
            "LINE (L) - Vẽ đường thẳng",
            "CIRCLE (C) - Vẽ đường tròn",
            "ARC (A) - Vẽ cung tròn",
            "RECTANGLE (REC) - Vẽ hình chữ nhật",
            "POLYGON (POL) - Vẽ đa giác",
            "ELLIPSE (EL) - Vẽ hình elip",
            "SPLINE (SPL) - Vẽ đường cong",
            "POLYLINE (PL) - Vẽ đường gấp khúc",
            "HATCH (H) - Tô bóng mặt",
            "DIMENSION (DIM) - Đánh kích thước"
        ]
        preview_text = "\n".join(sample_commands[:lines])
        self.preview_label.configure(text=preview_text)
    
    def create_customization_tab(self):
        """Create comprehensive button and group customization tab"""
        tab = ttk.Frame(self.notebook, style="Container.TFrame")
        self.notebook.add(tab, text="🎨 Tùy chỉnh")
        
        # Main container with two columns
        main_container = ttk.Frame(tab, style="Container.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Left panel - Customization options
        left_panel = ttk.Frame(main_container, style="Container.TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel - Live preview
        right_panel = ttk.Frame(main_container, style="Container.TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # === LEFT PANEL: Customization Controls ===
        # Scrollable container
        canvas = tk.Canvas(left_panel, bg=self.colors['bg_primary'], highlightthickness=0, width=350)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Container.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Button Style Section
        style_card = self.create_card(scrollable_frame, "Kiểu nút lệnh")
        
        # Font Family
        font_frame = ttk.Frame(style_card, style="Section.TFrame")
        font_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(font_frame, text="Font chữ", style="Modern.TLabel").pack(anchor=tk.W)
        self.font_family_var = tk.StringVar(value=self.config.get("button_style", {}).get("font_family", "Segoe UI"))
        font_combo = ttk.Combobox(font_frame, textvariable=self.font_family_var, 
                                  values=["Segoe UI", "Arial", "Calibri", "Consolas", "Tahoma"],
                                  state="readonly", width=25)
        font_combo.pack(fill=tk.X, pady=(5, 0))
        font_combo.bind('<<ComboboxSelected>>', lambda e: self.update_preview())
        
        # Font Size
        self.create_modern_slider(
            style_card,
            "Cỡ chữ nút",
            "Kích thước văn bản trên nút lệnh",
            8, 16,
            self.config.get("button_style", {}).get("font_size", 10),
            lambda v: f"{int(float(v))} px",
            lambda v: self.update_preview()
        )
        
        # Text Color
        color_frame = ttk.Frame(style_card, style="Section.TFrame")
        color_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(color_frame, text="Màu chữ", style="Modern.TLabel").pack(side=tk.LEFT)
        self.text_color_var = tk.StringVar(value=self.config.get("button_style", {}).get("text_color", "#FFFFFF"))
        text_color_entry = ttk.Entry(color_frame, textvariable=self.text_color_var, width=10)
        text_color_entry.pack(side=tk.RIGHT)
        text_color_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        color_btn = tk.Button(color_frame, text="🎨", command=lambda: self.pick_color(self.text_color_var),
                              bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'], bd=0, padx=5)
        color_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Background Color
        bg_color_frame = ttk.Frame(style_card, style="Section.TFrame")
        bg_color_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(bg_color_frame, text="Màu nền", style="Modern.TLabel").pack(side=tk.LEFT)
        self.btn_bg_color_var = tk.StringVar(value=self.config.get("button_style", {}).get("bg_color", "#3a3a3a"))
        bg_color_entry = ttk.Entry(bg_color_frame, textvariable=self.btn_bg_color_var, width=10)
        bg_color_entry.pack(side=tk.RIGHT)
        bg_color_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        bg_color_btn = tk.Button(bg_color_frame, text="🎨", command=lambda: self.pick_color(self.btn_bg_color_var),
                                 bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'], bd=0, padx=5)
        bg_color_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Hover Color
        hover_color_frame = ttk.Frame(style_card, style="Section.TFrame")
        hover_color_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(hover_color_frame, text="Màu hover", style="Modern.TLabel").pack(side=tk.LEFT)
        self.hover_color_var = tk.StringVar(value=self.config.get("button_style", {}).get("hover_color", "#4a4a4a"))
        hover_color_entry = ttk.Entry(hover_color_frame, textvariable=self.hover_color_var, width=10)
        hover_color_entry.pack(side=tk.RIGHT)
        hover_color_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        hover_color_btn = tk.Button(hover_color_frame, text="🎨", command=lambda: self.pick_color(self.hover_color_var),
                                    bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'], bd=0, padx=5)
        hover_color_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Border Radius
        self.create_modern_slider(
            style_card,
            "Bo góc",
            "Độ cong của góc nút",
            0, 20,
            self.config.get("button_style", {}).get("border_radius", 4),
            lambda v: f"{int(float(v))} px",
            lambda v: self.update_preview()
        )
        
        # Shadow Depth
        self.create_modern_slider(
            style_card,
            "Độ sâu bóng",
            "Độ nổi của nút",
            0, 10,
            self.config.get("button_style", {}).get("shadow_depth", 2),
            lambda v: f"{int(float(v))} px",
            lambda v: self.update_preview()
        )
        
        # Padding
        padding_card = self.create_card(scrollable_frame, "Khoảng cách")
        
        self.create_modern_slider(
            padding_card,
            "Padding ngang",
            "Khoảng cách trái/phải trong nút",
            5, 30,
            self.config.get("button_style", {}).get("padding_x", 15),
            lambda v: f"{int(float(v))} px",
            lambda v: self.update_preview()
        )
        
        self.create_modern_slider(
            padding_card,
            "Padding dọc",
            "Khoảng cách trên/dưới trong nút",
            3, 20,
            self.config.get("button_style", {}).get("padding_y", 8),
            lambda v: f"{int(float(v))} px",
            lambda v: self.update_preview()
        )
        
        # Group Management Section
        group_card = self.create_card(scrollable_frame, "Quản lý nhóm")
        
        # Group selector
        group_frame = ttk.Frame(group_card, style="Section.TFrame")
        group_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(group_frame, text="Chọn nhóm", style="Modern.TLabel").pack(anchor=tk.W, pady=(0, 5))
        self.selected_group_var = tk.StringVar()
        group_list = list(self.command_groups.keys())
        if group_list:
            self.selected_group_var.set(group_list[0])
        group_combo = ttk.Combobox(group_frame, textvariable=self.selected_group_var,
                                   values=group_list, state="readonly", width=25)
        group_combo.pack(fill=tk.X)
        
        # Group action buttons
        action_frame = ttk.Frame(group_card, style="Section.TFrame")
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(action_frame, text="➕ Tạo mới", command=self.create_new_group,
                 bg=self.colors['accent'], fg="#FFFFFF", font=("Segoe UI", 9),
                 bd=0, padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(action_frame, text="✏️ Đổi tên", command=self.rename_group,
                 bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'], font=("Segoe UI", 9),
                 bd=0, padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=2)
        
        tk.Button(action_frame, text="🗑️ Xóa", command=self.delete_group,
                 bg="#D13438", fg="#FFFFFF", font=("Segoe UI", 9),
                 bd=0, padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=2)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # === RIGHT PANEL: Live Preview ===
        preview_card = self.create_card(right_panel, "Xem trước trực tiếp")
        
        # Preview info
        info_frame = tk.Frame(preview_card, bg=self.colors['accent'], height=50)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        info_frame.pack_propagate(False)
        tk.Label(info_frame, text="💡 Thay đổi sẽ hiển thị ngay lập tức",
                bg=self.colors['accent'], fg="#FFFFFF",
                font=("Segoe UI", 9)).pack(expand=True)
        
        # Preview container
        self.preview_container = tk.Frame(preview_card, bg=self.colors['bg_tertiary'])
        self.preview_container.pack(fill=tk.BOTH, expand=True)
        
        # Initial preview
        self.update_preview()
    
    def update_preview(self):
        """Update the live preview with current settings"""
        # Clear existing preview buttons
        for widget in self.preview_container.winfo_children():
            widget.destroy()
        
        # Get current style settings
        font_family = self.font_family_var.get() if hasattr(self, 'font_family_var') else "Segoe UI"
        font_size = int(float(self.font_var.get())) if hasattr(self, 'font_var') else 10
        text_color = self.text_color_var.get() if hasattr(self, 'text_color_var') else "#FFFFFF"
        bg_color = self.btn_bg_color_var.get() if hasattr(self, 'btn_bg_color_var') else "#3a3a3a"
        hover_color = self.hover_color_var.get() if hasattr(self, 'hover_color_var') else "#4a4a4a"
        
        # Sample commands for preview
        sample_commands = [
            "LINE (L) - Vẽ đường thẳng",
            "CIRCLE (C) - Vẽ đường tròn",
            "RECTANGLE (REC) - Vẽ hình chữ nhật"
        ]
        
        for i, cmd in enumerate(sample_commands):
            btn = tk.Button(
                self.preview_container,
                text=cmd,
                bg=bg_color,
                fg=text_color,
                font=(font_family, font_size),
                bd=0,
                padx=15,
                pady=8,
                anchor=tk.W,
                cursor="hand2"
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn, hc=hover_color: b.configure(bg=hc))
            btn.bind("<Leave>", lambda e, b=btn, bc=bg_color: b.configure(bg=bc))
    
    def pick_color(self, color_var):
        """Open color picker dialog"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(initialcolor=color_var.get(), title="Chọn màu")
        if color[1]:
            color_var.set(color[1])
            self.update_preview()
    
    def create_new_group(self):
        """Create a new command group"""
        dialog = tk.Toplevel(self.dialog)
        dialog.title("Tạo nhóm mới")
        dialog.geometry("400x150")
        dialog.transient(self.dialog)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_primary'])
        
        frame = tk.Frame(dialog, bg=self.colors['bg_primary'])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Tên nhóm:", bg=self.colors['bg_primary'],
                fg=self.colors['fg_primary'], font=("Segoe UI", 10)).pack(anchor=tk.W)
        
        name_var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=name_var, width=40)
        entry.pack(fill=tk.X, pady=(5, 15))
        entry.focus()
        
        def save():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên nhóm")
                return
            if name in self.command_groups:
                messagebox.showwarning("Cảnh báo", "Nhóm này đã tồn tại")
                return
            
            self.command_groups[name] = {
                "active": True,
                "commands": []
            }
            self.config["active_groups"][name] = True
            
            # Update group selector
            if hasattr(self, 'selected_group_var'):
                current_groups = list(self.command_groups.keys())
                # Need to update the combobox values - will be done on save
            
            messagebox.showinfo("Thành công", f"Đã tạo nhóm '{name}'")
            dialog.destroy()
        
        btn_frame = tk.Frame(frame, bg=self.colors['bg_primary'])
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Tạo", command=save,
                 bg=self.colors['accent'], fg="#FFFFFF", bd=0,
                 padx=20, pady=8, cursor="hand2").pack(side=tk.RIGHT)
        tk.Button(btn_frame, text="Hủy", command=dialog.destroy,
                 bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'], bd=0,
                 padx=20, pady=8, cursor="hand2").pack(side=tk.RIGHT, padx=(0, 10))
        
        entry.bind('<Return>', lambda e: save())
    
    def rename_group(self):
        """Rename an existing command group"""
        if not hasattr(self, 'selected_group_var'):
            return
        
        old_name = self.selected_group_var.get()
        if not old_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhóm để đổi tên")
            return
        
        dialog = tk.Toplevel(self.dialog)
        dialog.title("Đổi tên nhóm")
        dialog.geometry("400x150")
        dialog.transient(self.dialog)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_primary'])
        
        frame = tk.Frame(dialog, bg=self.colors['bg_primary'])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text=f"Tên mới cho '{old_name}':", bg=self.colors['bg_primary'],
                fg=self.colors['fg_primary'], font=("Segoe UI", 10)).pack(anchor=tk.W)
        
        name_var = tk.StringVar(value=old_name)
        entry = ttk.Entry(frame, textvariable=name_var, width=40)
        entry.pack(fill=tk.X, pady=(5, 15))
        entry.focus()
        entry.select_range(0, tk.END)
        
        def save():
            new_name = name_var.get().strip()
            if not new_name:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên nhóm")
                return
            if new_name != old_name and new_name in self.command_groups:
                messagebox.showwarning("Cảnh báo", "Nhóm này đã tồn tại")
                return
            
            if new_name != old_name:
                # Rename the group
                self.command_groups[new_name] = self.command_groups.pop(old_name)
                if old_name in self.config["active_groups"]:
                    self.config["active_groups"][new_name] = self.config["active_groups"].pop(old_name)
                
                self.selected_group_var.set(new_name)
                messagebox.showinfo("Thành công", f"Đã đổi tên thành '{new_name}'")
            
            dialog.destroy()
        
        btn_frame = tk.Frame(frame, bg=self.colors['bg_primary'])
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Lưu", command=save,
                 bg=self.colors['accent'], fg="#FFFFFF", bd=0,
                 padx=20, pady=8, cursor="hand2").pack(side=tk.RIGHT)
        tk.Button(btn_frame, text="Hủy", command=dialog.destroy,
                 bg=self.colors['bg_tertiary'], fg=self.colors['fg_primary'], bd=0,
                 padx=20, pady=8, cursor="hand2").pack(side=tk.RIGHT, padx=(0, 10))
        
        entry.bind('<Return>', lambda e: save())
    
    def delete_group(self):
        """Delete a command group"""
        if not hasattr(self, 'selected_group_var'):
            return
        
        group_name = self.selected_group_var.get()
        if not group_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhóm để xóa")
            return
        
        if len(self.command_groups) <= 1:
            messagebox.showwarning("Cảnh báo", "Không thể xóa nhóm cuối cùng")
            return
        
        result = messagebox.askyesno("Xác nhận", 
                                     f"Bạn có chắc muốn xóa nhóm '{group_name}'?")
        if result:
            del self.command_groups[group_name]
            if group_name in self.config["active_groups"]:
                del self.config["active_groups"][group_name]
            
            # Select first remaining group
            remaining_groups = list(self.command_groups.keys())
            if remaining_groups:
                self.selected_group_var.set(remaining_groups[0])
            
            messagebox.showinfo("Thành công", f"Đã xóa nhóm '{group_name}'")
    
    def create_hotkeys_tab(self):
        """Create modern hotkeys settings tab"""
        tab = ttk.Frame(self.notebook, style="Container.TFrame")
        self.notebook.add(tab, text="⌨️ Phím tắt")
        
        # Main container
        main_frame = ttk.Frame(tab, style="Container.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Hotkeys card
        card = self.create_card(main_frame, "Tùy chỉnh phím tắt")
        
        # Info banner
        info_banner = tk.Frame(card, bg=self.colors['accent'], height=60)
        info_banner.pack(fill=tk.X, pady=(0, 20))
        info_banner.pack_propagate(False)
        
        info_label = tk.Label(info_banner,
                             text="ℹ️ Nhấn vào nút 'Thay đổi' để gán phím tắt mới",
                             bg=self.colors['accent'],
                             fg="#FFFFFF",
                             font=("Segoe UI", 10))
        info_label.pack(expand=True)
        
        # Previous page hotkey
        self.create_hotkey_row(card, "⬅️ Phím lùi trang", "prev_key", 
                              "Phím để chuyển về trang trước")
        
        # Next page hotkey
        self.create_hotkey_row(card, "➡️ Phím tiến trang", "next_key",
                              "Phím để chuyển đến trang kế tiếp")
    
    def create_hotkey_row(self, parent, title, key_name, description):
        """Create a modern hotkey configuration row"""
        container = ttk.Frame(parent, style="Section.TFrame")
        container.pack(fill=tk.X, pady=(0, 20))
        
        # Header
        header = ttk.Frame(container, style="Section.TFrame")
        header.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(header, text=title, style="Modern.TLabel").pack(side=tk.LEFT)
        
        # Description
        ttk.Label(container, text=description, style="SubText.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        # Hotkey display and button
        hotkey_frame = tk.Frame(container, bg=self.colors['bg_tertiary'], height=45)
        hotkey_frame.pack(fill=tk.X)
        hotkey_frame.pack_propagate(False)
        
        # Store key variable
        if key_name == "prev_key":
            self.prev_key_var = tk.StringVar(value=self.config["prev_key"])
            key_var = self.prev_key_var
        else:
            self.next_key_var = tk.StringVar(value=self.config["next_key"])
            key_var = self.next_key_var
        
        # Key display
        key_display = tk.Label(hotkey_frame,
                              textvariable=key_var,
                              bg=self.colors['bg_tertiary'],
                              fg=self.colors['fg_primary'],
                              font=("Segoe UI Semibold", 11),
                              padx=15)
        key_display.pack(side=tk.LEFT, fill=tk.Y)
        
        # Change button
        change_btn = tk.Button(hotkey_frame,
                              text="Thay đổi",
                              bg=self.colors['accent'],
                              fg="#FFFFFF",
                              font=("Segoe UI", 10),
                              bd=0,
                              padx=20,
                              cursor="hand2",
                              command=lambda: self.change_hotkey(key_name))
        change_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Hover effect
        change_btn.bind("<Enter>", lambda e: change_btn.configure(bg=self.colors['hover_bg']))
        change_btn.bind("<Leave>", lambda e: change_btn.configure(bg=self.colors['accent']))
    
    def change_hotkey(self, key_name):
        """Open dialog to change hotkey"""
        dialog = HotkeyDialog(self.dialog, key_name)
        if dialog.result:
            if key_name == "prev_key":
                self.prev_key_var.set(dialog.result)
            else:
                self.next_key_var.set(dialog.result)
    
    def create_command_groups_tab(self):
        """Create modern command groups settings tab"""
        tab = ttk.Frame(self.notebook, style="Container.TFrame")
        self.notebook.add(tab, text="📋 Nhóm lệnh")
        
        # Main container
        main_frame = ttk.Frame(tab, style="Container.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Autostart card
        autostart_card = self.create_card(main_frame, "Tùy chọn khởi động")
        
        self.autostart_var = tk.BooleanVar(value=os.path.exists(self.app.startup_path))
        
        check_frame = tk.Frame(autostart_card, bg=self.colors['bg_secondary'])
        check_frame.pack(fill=tk.X, pady=(0, 10))
        
        autostart_check = ttk.Checkbutton(
            check_frame,
            text="🚀 Tự động khởi động cùng Windows",
            variable=self.autostart_var,
            style="Modern.TCheckbutton"
        )
        autostart_check.pack(anchor=tk.W)
        
        ttk.Label(check_frame,
                 text="Ứng dụng sẽ tự động khởi động khi Windows khởi động",
                 style="SubText.TLabel").pack(anchor=tk.W, padx=(25, 0), pady=(5, 0))
        
        # Command groups card
        groups_card = self.create_card(main_frame, "Quản lý nhóm lệnh")
        
        # Scrollable container for groups
        canvas = tk.Canvas(groups_card, bg=self.colors['bg_secondary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(groups_card, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Section.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.group_vars = {}
        self.command_lists = {}
        
        for group_name in self.command_groups:
            var = tk.BooleanVar(value=self.command_groups[group_name]["active"])
            self.group_vars[group_name] = var
            
            # Modern group container
            group_container = tk.Frame(scrollable_frame, 
                                      bg=self.colors['bg_tertiary'],
                                      highlightbackground=self.colors['border'],
                                      highlightthickness=1)
            group_container.pack(fill=tk.X, pady=(0, 15))
            
            # Group header
            header = tk.Frame(group_container, bg=self.colors['bg_tertiary'])
            header.pack(fill=tk.X, padx=15, pady=12)
            
            # Checkbox and title
            check_frame = tk.Frame(header, bg=self.colors['bg_tertiary'])
            check_frame.pack(side=tk.LEFT)
            
            check = ttk.Checkbutton(
                check_frame,
                text=f"✓ {group_name}",
                variable=var,
                style="Modern.TCheckbutton"
            )
            check.pack(side=tk.LEFT)
            
            # Command count badge
            count_badge = tk.Label(header,
                                  text=f"{len(self.command_groups[group_name]['commands'])}",
                                  bg=self.colors['accent'],
                                  fg="#FFFFFF",
                                  font=("Segoe UI Semibold", 9),
                                  padx=8, pady=2)
            count_badge.pack(side=tk.LEFT, padx=(10, 0))
            
            # Manage button
            manage_btn = tk.Button(header,
                                  text="⚙ Quản lý lệnh",
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['fg_primary'],
                                  font=("Segoe UI", 9),
                                  bd=0,
                                  padx=15, pady=5,
                                  cursor="hand2",
                                  command=lambda g=group_name: self.manage_commands(g))
            manage_btn.pack(side=tk.RIGHT)
            
            # Hover effect for manage button
            manage_btn.bind("<Enter>", lambda e, btn=manage_btn: btn.configure(bg=self.colors['hover_bg']))
            manage_btn.bind("<Leave>", lambda e, btn=manage_btn: btn.configure(bg=self.colors['bg_secondary']))
            
            # Commands preview (first 3 commands)
            preview_frame = tk.Frame(group_container, bg=self.colors['bg_tertiary'])
            preview_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
            
            preview_commands = self.command_groups[group_name]["commands"][:3]
            if preview_commands:
                for cmd in preview_commands:
                    cmd_label = tk.Label(preview_frame,
                                        text=f"• {cmd}",
                                        bg=self.colors['bg_tertiary'],
                                        fg=self.colors['fg_secondary'],
                                        font=("Segoe UI", 9),
                                        anchor=tk.W)
                    cmd_label.pack(fill=tk.X, pady=1)
                
                if len(self.command_groups[group_name]["commands"]) > 3:
                    more_label = tk.Label(preview_frame,
                                         text=f"... và {len(self.command_groups[group_name]['commands']) - 3} lệnh khác",
                                         bg=self.colors['bg_tertiary'],
                                         fg=self.colors['fg_secondary'],
                                         font=("Segoe UI Italic", 8),
                                         anchor=tk.W)
                    more_label.pack(fill=tk.X, pady=(5, 0))
            else:
                empty_label = tk.Label(preview_frame,
                                      text="Chưa có lệnh nào",
                                      bg=self.colors['bg_tertiary'],
                                      fg=self.colors['fg_secondary'],
                                      font=("Segoe UI Italic", 9))
                empty_label.pack()
            
            # Store reference for listbox (for compatibility)
            listbox = tk.Listbox(group_container, height=0)  # Hidden
            for cmd in self.command_groups[group_name]["commands"]:
                listbox.insert(tk.END, cmd)
            self.command_lists[group_name] = listbox
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
            
    def add_command(self, group_name):
        dialog = CommandDialog(self.dialog, "Thêm lệnh mới", "")
        if dialog.result:
            self.command_groups[group_name]["commands"].append(dialog.result)
            self.command_lists[group_name].insert(tk.END, dialog.result)
    
    def edit_command(self, group_name):
        selection = self.command_lists[group_name].curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một lệnh để sửa")
            return
            
        index = selection[0]
        old_command = self.command_lists[group_name].get(index)
        
        dialog = CommandDialog(self.dialog, "Sửa lệnh", old_command)
        if dialog.result:
            self.command_groups[group_name]["commands"][index] = dialog.result
            self.command_lists[group_name].delete(index)
            self.command_lists[group_name].insert(index, dialog.result)
    
    def remove_command(self, group_name):
        selection = self.command_lists[group_name].curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một lệnh để xóa")
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa lệnh này?"):
            index = selection[0]
            self.command_lists[group_name].delete(index)
            del self.command_groups[group_name]["commands"][index]
    
    def manage_commands(self, group_name):
        dialog = tk.Toplevel(self.dialog)
        dialog.title(f"Quản lý lệnh - {group_name}")
        dialog.geometry("400x500")
        dialog.transient(self.dialog)
        dialog.grab_set()
        
        if self.config["theme"] == "dark":
            dialog.configure(bg="#2E2E2E")
        
        # Frame chính
        main_frame = ttk.Frame(dialog, style="Settings.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox cho danh sách lệnh
        list_frame = ttk.Frame(main_frame, style="Settings.TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            bg=self.config["bg_color"],
            fg=self.config["fg_color"]
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        # Nạp danh sách lệnh hiện tại
        current_commands = list(self.command_lists[group_name].get(0, tk.END))
        for cmd in current_commands:
            listbox.insert(tk.END, cmd)
        
        # Frame cho các nút
        button_frame = ttk.Frame(main_frame, style="Settings.TFrame")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Entry để nhập lệnh mới
        entry_var = tk.StringVar()
        entry = ttk.Entry(button_frame, textvariable=entry_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Nút Thêm
        add_btn = ttk.Button(
            button_frame,
            text="Thêm",
            style="Settings.TButton",
            command=lambda: self.add_command(listbox, entry_var)
        )
        add_btn.pack(side=tk.LEFT, padx=2)
        
        # Nút Xóa
        delete_btn = ttk.Button(
            button_frame,
            text="Xóa",
            style="Settings.TButton",
            command=lambda: self.delete_command(listbox)
        )
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        # Nút Di chuyển
        move_up_btn = ttk.Button(
            button_frame,
            text="↑",
            style="Settings.TButton",
            command=lambda: self.move_command(listbox, -1)
        )
        move_up_btn.pack(side=tk.LEFT, padx=2)
        
        move_down_btn = ttk.Button(
            button_frame,
            text="↓",
            style="Settings.TButton",
            command=lambda: self.move_command(listbox, 1)
        )
        move_down_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame cho nút Lưu/Hủy
        save_frame = ttk.Frame(main_frame, style="Settings.TFrame")
        save_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Nút Lưu
        save_btn = ttk.Button(
            save_frame,
            text="Lưu",
            style="Save.TButton",
            command=lambda: self.save_commands(dialog, group_name, listbox)
        )
        save_btn.pack(side=tk.RIGHT, padx=2)
        
        # Nút Hủy
        cancel_btn = ttk.Button(
            save_frame,
            text="Hủy",
            style="Cancel.TButton",
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT, padx=2)
        
    def add_command(self, listbox, entry_var):
        command = entry_var.get().strip()
        if command:
            listbox.insert(tk.END, command)
            entry_var.set("")  # Clear entry
            
    def delete_command(self, listbox):
        selection = listbox.curselection()
        if selection:
            listbox.delete(selection)
            
    def move_command(self, listbox, direction):
        selection = listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        if direction == -1 and index > 0:  # Di chuyển lên
            text = listbox.get(index)
            listbox.delete(index)
            listbox.insert(index - 1, text)
            listbox.selection_set(index - 1)
        elif direction == 1 and index < listbox.size() - 1:  # Di chuyển xuống
            text = listbox.get(index)
            listbox.delete(index)
            listbox.insert(index + 1, text)
            listbox.selection_set(index + 1)
            
    def save_commands(self, dialog, group_name, listbox):
        # Cập nhật danh sách lệnh trong listbox chính
        main_listbox = self.command_lists[group_name]
        main_listbox.delete(0, tk.END)
        for i in range(listbox.size()):
            main_listbox.insert(tk.END, listbox.get(i))
        dialog.destroy()
        
    def save(self):
        try:
            # Cập nhật trạng thái active của các nhóm
            for group_name, var in self.group_vars.items():
                self.command_groups[group_name]["active"] = var.get()
                self.config["active_groups"][group_name] = var.get()
                
                # Lưu các lệnh đã sửa đổi
                self.command_groups[group_name]["commands"] = list(self.command_lists[group_name].get(0, tk.END))
            
            # Cập nhật trạng thái tự động khởi động
            if self.autostart_var.get() != os.path.exists(self.app.startup_path):
                if self.autostart_var.get():
                    try:
                        import winshell
                        from win32com.client import Dispatch
                        shell = Dispatch('WScript.Shell')
                        shortcut = shell.CreateShortCut(self.app.startup_path)
                        shortcut.Targetpath = self.app.bat_path
                        shortcut.WorkingDirectory = os.path.dirname(self.app.bat_path)
                        shortcut.save()
                    except Exception as e:
                        messagebox.showerror("Lỗi", f"Không thể tạo shortcut: {str(e)}")
                else:
                    try:
                        os.remove(self.app.startup_path)
                    except Exception as e:
                        messagebox.showerror("Lỗi", f"Không thể xóa shortcut: {str(e)}")
            
            # Cập nhật cấu hình chung
            self.config.update({
                "theme": self.theme_var.get(),
                "opacity": self.opacity_var.get(),
                "font_size": self.font_var.get(),
                "lines_per_page": self.lines_var.get(),
                "command_groups": self.command_groups  # Lưu toàn bộ cấu hình nhóm lệnh
            })
            
            # Gọi callback để lưu
            self.save_callback(self.config)
            
            # Cập nhật lại giao diện chính
            if hasattr(self.app, "reload_commands"):
                self.app.reload_commands()
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi khi lưu cấu hình: {str(e)}")
        
    def change_hotkey(self, key_type):
        dialog = HotkeyDialog(self.dialog)
        self.dialog.wait_window(dialog.dialog)
        if dialog.result:
            self.config[key_type] = dialog.result.lower()
            if key_type == "prev_key":
                self.prev_key_var.set(dialog.result.lower())
            else:
                self.next_key_var.set(dialog.result.lower())

class CommandDialog:
    def __init__(self, parent, title, initial_value=""):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.result = None
        
        # Style
        if hasattr(parent, 'config') and parent.config["theme"] == "dark":
            self.dialog.configure(bg="#2E2E2E")
        
        # Frame chính
        main_frame = ttk.Frame(self.dialog, style="Settings.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label
        ttk.Label(
            main_frame,
            text="Nhập lệnh (ví dụ: LINE (L) - Vẽ đường thẳng):",
            style="Settings.TLabel"
        ).pack(pady=(0, 5))
        
        # Entry
        self.command_var = tk.StringVar(value=initial_value)
        entry = ttk.Entry(
            main_frame,
            textvariable=self.command_var
        )
        entry.pack(fill=tk.X, pady=5)
        entry.focus()
        
        # Frame cho các nút
        button_frame = ttk.Frame(main_frame, style="Settings.TFrame")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Nút Lưu
        ttk.Button(
            button_frame,
            text="Lưu",
            style="Save.TButton",
            command=self.save
        ).pack(side=tk.RIGHT, padx=2)
        
        # Nút Hủy
        ttk.Button(
            button_frame,
            text="Hủy",
            style="Cancel.TButton",
            command=self.dialog.destroy
        ).pack(side=tk.RIGHT, padx=2)
        
        # Bind phím Enter cho entry
        entry.bind("<Return>", lambda e: self.save())
        
        # Bind phím Escape cho dialog
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
        
        self.dialog.wait_window()
        
    def save(self):
        value = self.command_var.get().strip()
        if value:
            self.result = value
            self.dialog.destroy()
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
        # Định nghĩa các nhóm lệnh
        self.command_groups = {
            "Cơ bản": {
                "active": True,
                "commands": [
                    "LINE (L) - Vẽ đường thẳng",
                    "CIRCLE (C) - Vẽ đường tròn",
                    "RECTANGLE (REC) - Vẽ hình chữ nhật",
                    "ARC (A) - Vẽ cung tròn",
                    "POLYLINE (PL) - Vẽ đường đa tuyến"
                ]
            },
            "Chỉnh sửa": {
                "active": True,
                "commands": [
                    "MOVE (M) - Di chuyển đối tượng",
                    "COPY (CO) - Sao chép đối tượng",
                    "ROTATE (RO) - Xoay đối tượng",
                    "SCALE (SC) - Thay đổi tỷ lệ",
                    "STRETCH (S) - Kéo giãn đối tượng"
                ]
            },
            "Sửa đổi nâng cao": {
                "active": True,
                "commands": [
                    "TRIM (TR) - Cắt đối tượng",
                    "EXTEND (EX) - Kéo dài đối tượng",
                    "FILLET (F) - Bo tròn góc",
                    "CHAMFER (CHA) - Vát góc",
                    "OFFSET (O) - Tạo đối tượng song song"
                ]
            },
            "Đo lường": {
                "active": True,
                "commands": [
                    "DISTANCE (DI) - Đo khoảng cách",
                    "AREA (AREA) - Tính diện tích",
                    "LIST (LI) - Xem thông tin đối tượng",
                    "ALIGN (AL) - Căn chỉnh đối tượng",
                    "MEASURE (ME) - Đo đạc"
                ]
            },
            "Layer & Thuộc tính": {
                "active": True,
                "commands": [
                    "LAYER (LA) - Quản lý layer",
                    "MATCHPROP (MA) - Sao chép thuộc tính",
                    "PROPERTIES (PR) - Bảng thuộc tính",
                    "COLOR (COL) - Đổi màu",
                    "LINETYPE (LT) - Đổi loại đường"
                ]
            },
            "Text & Dimension": {
                "active": True,
                "commands": [
                    "TEXT (T) - Thêm văn bản",
                    "MTEXT (MT) - Văn bản nhiều dòng",
                    "DIMLINEAR (DLI) - Dim đường thẳng",
                    "DIMALIGNED (DAL) - Dim theo góc",
                    "DIMRADIUS (DRA) - Dim bán kính"
                ]
            },
            "Block & Reference": {
                "active": True,
                "commands": [
                    "BLOCK (B) - Tạo block",
                    "INSERT (I) - Chèn block",
                    "XREF (XR) - Tham chiếu ngoài",
                    "EXPLODE (X) - Phá vỡ block",
                    "WBLOCK (W) - Xuất block"
                ]
            },
            "Công cụ hỗ trợ": {
                "active": True,
                "commands": [
                    "ORTHO (F8) - Bật/tắt vẽ vuông góc",
                    "SNAP (F9) - Bật/tắt bắt điểm",
                    "GRID (F7) - Bật/tắt lưới",
                    "OSNAP (F3) - Thiết lập bắt điểm",
                    "UCS (UC) - Hệ tọa độ người dùng"
                ]
            }
        }
        
        # Khởi tạo danh sách lệnh từ các nhóm
        self.commands = []
        all_commands = []
        for group_data in self.command_groups.values():
            if group_data["active"]:
                all_commands.extend(group_data["commands"])
        
        # Tổ chức lại theo số dòng mỗi trang
        lines_per_page = self.config["lines_per_page"]
        self.commands = [
            all_commands[i:i + lines_per_page]
            for i in range(0, len(all_commands), lines_per_page)
        ]
        if not self.commands:
            self.commands = [[]]
        
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
            "theme": "dark",
            "active_groups": {
                "Cơ bản": True,
                "Chỉnh sửa": True,
                "Sửa đổi nâng cao": True,
                "Đo lường": True,
                "Layer & Thuộc tính": True,
                "Text & Dimension": True,
                "Block & Reference": True,
                "Công cụ hỗ trợ": True
            },
            # Customizable styling options
            "button_style": {
                "font_family": "Segoe UI",
                "font_size": 10,
                "font_weight": "normal",
                "text_color": "#FFFFFF",
                "bg_color": "#3a3a3a",
                "hover_color": "#4a4a4a",
                "border_radius": 4,
                "border_width": 0,
                "border_color": "#555555",
                "shadow_depth": 2,
                "padding_x": 15,
                "padding_y": 8
            },
            "group_hotkeys": {
                # Per-group keyboard shortcuts
                # Format: "Group Name": "hotkey"
            },
            "group_styles": {
                # Per-group custom styling (overrides global button_style)
                # Format: "Group Name": { style_properties }
            },
            "show_tooltips": True,
            "tooltip_delay": 500,  # milliseconds
            "group_switcher_style": "tabs"  # "tabs" or "dropdown"
        }
        
        # Đọc cấu hình từ file nếu có
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except:
                pass
                
        # Cập nhật trạng thái active của các nhóm từ cấu hình
        if hasattr(self, 'command_groups'):
            for group_name in self.command_groups:
                self.command_groups[group_name]["active"] = \
                    self.config["active_groups"].get(group_name, True)
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
            
    def reload_commands(self):
        # Cập nhật trạng thái active của các nhóm
        for group_name, group_info in self.command_groups.items():
            # Cập nhật trạng thái active
            group_info["active"] = self.config["active_groups"].get(group_name, False)
            
            # Cập nhật danh sách lệnh
            if group_name in self.config["command_groups"]:
                group_info["commands"] = self.config["command_groups"][group_name]["commands"]
            
        # Lưu trạng thái vào config
        self.config["command_groups"] = self.command_groups
            
        # Tổ chức lại các lệnh
        self.reorganize_commands()
        
        # Cập nhật hiển thị
        self.update_commands()
        
    def show_command_menu(self, group_name):
        """Hiển thị menu cho một nhóm lệnh cụ thể"""
        if group_name not in self.command_groups:
            return
            
        menu = tk.Menu(self.root, tearoff=0)
        for cmd in self.command_groups[group_name]["commands"]:
            menu.add_command(
                label=cmd,
                command=lambda c=cmd: pyautogui.write(c.split(" -")[0].strip("()") + " ")
            )
            
        # Xác định vị trí menu
        for widget in self.command_buttons.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == group_name:
                x = widget.winfo_rootx()
                y = widget.winfo_rooty() + widget.winfo_height()
                menu.post(x, y)
                break
                
    def navigate_commands(self, direction):
        """Di chuyển giữa các lệnh"""
        total_pages = len(self.commands)
        if total_pages == 0:
            return
            
        if direction == "prev":
            self.current_page = (self.current_page - 1) % total_pages
        else:
            self.current_page = (self.current_page + 1) % total_pages
            
        self.update_commands()
    
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
        
        # Cấu hình màu sắc dựa trên theme
        bg_color = "#000000" if self.config["theme"] == "dark" else "#FFFFFF"
        fg_color = "#FFFFFF" if self.config["theme"] == "dark" else "#000000"
        
        # Cấu hình màu nền cho cửa sổ chính
        self.root.configure(bg=bg_color)
        self.config["bg_color"] = bg_color
        
        # Style cho các widget cơ bản
        style.configure("Custom.TFrame", background=bg_color)
        style.configure("Custom.TLabel", 
                      font=("Arial", self.config["font_size"]),
                      background=bg_color,
                      foreground=fg_color)
        style.configure("Custom.TButton",
                      background=bg_color,
                      foreground=fg_color)
        style.configure("Custom.TMenubutton",
                      background=bg_color,
                      foreground=fg_color)
        style.configure("Custom.TCombobox",
                      fieldbackground=bg_color,
                      foreground=fg_color)
        
        # Style cho nút Save/Cancel
        style.configure("Save.TButton",
                      background="#28a745",
                      foreground="#FFFFFF")
        style.configure("Cancel.TButton",
                      background="#dc3545",
                      foreground="#FFFFFF")
                      
        # Map hover states
        style.map('Save.TButton',
                background=[('active', '#218838')],
                foreground=[('active', '#FFFFFF')])
        style.map('Cancel.TButton',
                background=[('active', '#c82333')],
                foreground=[('active', '#FFFFFF')])
                
        # Cập nhật màu chữ trong config
        self.config["text_color"] = fg_color
        
        # Tạo toolbar
        self.create_toolbar()
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
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
        
        # Cập nhật hiển thị ban đầu
        self.update_commands()
        
    def create_toolbar(self):
        # Frame chính cho toolbar
        self.toolbar = ttk.Frame(self.root, style="Custom.TFrame")
        self.toolbar.pack(side="top", fill="x")
        
        # Frame cho các nút điều khiển
        self.control_buttons = ttk.Frame(self.toolbar, style="Custom.TFrame")
        self.control_buttons.pack(side=tk.LEFT)
        
        # Frame cho các nút nhóm lệnh
        self.command_buttons = ttk.Frame(self.toolbar, style="Custom.TFrame")
        self.command_buttons.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Nút Cài đặt
        ttk.Button(
            self.control_buttons,
            text="⚙️ Cài đặt",
            command=self.show_settings,
            style="Custom.TButton"
        ).pack(side=tk.LEFT, padx=2)
        
        # Nút Chuyển chủ đề
        ttk.Button(
            self.control_buttons,
            text="🌓",
            command=self.toggle_theme,
            style="Custom.TButton",
            width=3
        ).pack(side=tk.LEFT, padx=2)
        
        # Nút điều chỉnh độ trong suốt
        ttk.Button(
            self.control_buttons,
            text="👁️",
            command=self.toggle_opacity,
            style="Custom.TButton",
            width=3
        ).pack(side=tk.LEFT, padx=2)
        
        # Cập nhật trạng thái toolbar
        self.update_command_toolbar()
        
    def update_command_toolbar(self):
        # Xóa các nút cũ
        for widget in self.command_buttons.winfo_children():
            widget.destroy()
        
        # Tạo nút cho mỗi nhóm lệnh active
        for group_name, group_info in self.command_groups.items():
            if group_info["active"]:
                btn = ttk.Button(
                    self.command_buttons,
                    text=group_name,
                    command=lambda g=group_name: self.show_command_menu(g),
                    style="Custom.TButton"
                )
                btn.pack(side=tk.LEFT, padx=2)
                
        # Nút điều hướng
        ttk.Button(
            self.command_buttons,
            text="←",
            command=lambda: self.navigate_commands("prev"),
            style="Custom.TButton",
            width=3
        ).pack(side=tk.RIGHT, padx=2)
        
        ttk.Button(
            self.command_buttons,
            text="→",
            command=lambda: self.navigate_commands("next"),
            style="Custom.TButton",
            width=3
        ).pack(side=tk.RIGHT, padx=2)
    
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
        dialog = SettingsDialog(self, self.root, self.config, self.command_groups, self.apply_settings)
        self.root.wait_window(dialog.dialog)
    
    def apply_settings(self, new_config):
        # Lưu và áp dụng cấu hình mới
        self.config.update(new_config)
        self.save_config()
        
        # Thiết lập lại style và theme
        self.apply_theme()
        
        # Cập nhật các thành phần
        self.reorganize_commands()  # Tổ chức lại lệnh theo số dòng mới
        self.setup_keyboard()  # Cập nhật phím tắt
        self.update_commands()  # Cập nhật hiển thị
        
    def apply_theme(self):
        """Áp dụng theme và style cho toàn bộ ứng dụng"""
        style = ttk.Style()
        
        # Xác định màu sắc dựa trên theme
        bg_color = "#000000" if self.config["theme"] == "dark" else "#FFFFFF"
        fg_color = "#FFFFFF" if self.config["theme"] == "dark" else "#000000"
        
        # Cấu hình màu nền cho cửa sổ chính
        self.root.configure(bg=bg_color)
        self.config["bg_color"] = bg_color
        self.config["text_color"] = fg_color
        
        # Áp dụng độ trong suốt
        self.root.attributes('-alpha', self.config["opacity"])
        
        # Style cho các widget cơ bản
        style.configure("Custom.TFrame", background=bg_color)
        style.configure("Custom.TLabel", 
                      font=("Arial", self.config["font_size"]),
                      background=bg_color,
                      foreground=fg_color)
        style.configure("Custom.TButton",
                      background=bg_color,
                      foreground=fg_color)
        style.configure("Custom.TMenubutton",
                      background=bg_color,
                      foreground=fg_color)
        style.configure("Custom.TCombobox",
                      fieldbackground=bg_color,
                      foreground=fg_color)
        
        # Style cho các nút đặc biệt
        style.configure("Save.TButton",
                      background="#28a745",
                      foreground="#FFFFFF")
        style.map('Save.TButton',
                background=[('active', '#218838')],
                foreground=[('active', '#FFFFFF')])
                
        style.configure("Cancel.TButton",
                      background="#dc3545",
                      foreground="#FFFFFF")
        style.map('Cancel.TButton',
                background=[('active', '#c82333')],
                foreground=[('active', '#FFFFFF')])
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        if self.config["theme"] == "dark":
            self.config["theme"] = "light"
        else:
            self.config["theme"] = "dark"
        self.save_config()
        self.apply_theme()
        self.update_commands()
    
    def toggle_opacity(self):
        """Cycle through opacity levels"""
        opacity_levels = [0.5, 0.7, 0.9, 1.0]
        current = self.config["opacity"]
        
        # Find next opacity level
        try:
            current_index = opacity_levels.index(current)
            next_index = (current_index + 1) % len(opacity_levels)
        except ValueError:
            next_index = 0
        
        self.config["opacity"] = opacity_levels[next_index]
        self.save_config()
        self.root.attributes('-alpha', self.config["opacity"])
    
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
        # Lấy danh sách các lệnh từ các nhóm đang active
        all_commands = []
        selected_group = self.group_var.get() if hasattr(self, 'group_var') else "Tất cả"
        
        for group_name, group_data in self.command_groups.items():
            if group_data["active"] and (selected_group == "Tất cả" or selected_group == group_name):
                all_commands.extend(group_data["commands"])
        
        # Chia thành các nhóm mới theo số dòng mỗi trang
        lines_per_page = self.config["lines_per_page"]
        self.commands = [
            all_commands[i:i + lines_per_page]
            for i in range(0, len(all_commands), lines_per_page)
        ]
        
        # Đảm bảo trang hiện tại hợp lệ
        if not self.commands:
            self.commands = [[]]
        if self.current_page >= len(self.commands):
            self.current_page = len(self.commands) - 1
    
    def toggle_group(self, group_name):
        # Đảo trạng thái active của nhóm
        self.command_groups[group_name]["active"] = not self.command_groups[group_name]["active"]
        # Cập nhật lại danh sách lệnh và hiển thị
        self.reorganize_commands()
        self.update_commands()
        # Lưu cấu hình
        self.save_config()
    
    def on_group_selected(self, event=None):
        # Được gọi khi người dùng chọn một nhóm từ combobox
        self.current_page = 0  # Reset về trang đầu
        self.reorganize_commands()
        self.update_commands()
    
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
