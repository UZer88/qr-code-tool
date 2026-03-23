import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import pyperclip
import os

# Цветовая схема
COLORS = {
    'bg': '#1e1e2e',
    'fg': '#cdd6f4',
    'accent': '#89b4fa',
    'button_bg': '#313244',
    'button_fg': '#cdd6f4',
    'entry_bg': '#313244',
    'entry_fg': '#cdd6f4',
    'hover': '#45475a'
}


class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Tool")
        self.root.geometry("650x700")
        self.root.minsize(500, 600)
        self.root.configure(bg=COLORS['bg'])

        # Устанавливаем иконку
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'qr_icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                png_path = os.path.join(os.path.dirname(__file__), 'qr_icon.png')
                if os.path.exists(png_path):
                    icon_image = tk.PhotoImage(file=png_path)
                    self.root.iconphoto(True, icon_image)
        except:
            pass

        self.qr_image = None
        self.current_qr_path = None
        self.result_data = None

        # Настройка сетки
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.center_window()

    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

    def reset_window_size(self):
        """Сбрасывает размер окна к стандартному"""
        self.root.geometry("650x700")
        self.root.minsize(500, 600)
        self.center_window()

    def create_widgets(self):
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg=COLORS['bg'])
        top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        top_frame.grid_columnconfigure(0, weight=1)

        title = tk.Label(
            top_frame,
            text="📱 QR Code Tool",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title.pack()

        # Кнопки вкладок
        tab_frame = tk.Frame(self.root, bg=COLORS['bg'])
        tab_frame.grid(row=1, column=0, pady=10)

        self.btn_generate = self.create_tab_button(
            tab_frame, "✨ Создать QR", self.show_generate
        )
        self.btn_generate.pack(side=tk.LEFT, padx=10)

        self.btn_scan = self.create_tab_button(
            tab_frame, "🔍 Сканировать QR", self.show_scan
        )
        self.btn_scan.pack(side=tk.LEFT, padx=10)

        # Контейнер для содержимого
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Контейнеры для вкладок
        self.frame_generate = tk.Frame(self.content_frame, bg=COLORS['bg'])
        self.frame_scan = tk.Frame(self.content_frame, bg=COLORS['bg'])

        self.create_generate_tab()
        self.create_scan_tab()

        self.show_generate()

    def create_tab_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 11),
            bg=COLORS['button_bg'],
            fg=COLORS['button_fg'],
            activebackground=COLORS['hover'],
            activeforeground=COLORS['fg'],
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=command
        )
        return btn

    def create_generate_tab(self):
        # Контейнер с прокруткой
        canvas = tk.Canvas(self.frame_generate, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_generate, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # === Карточка ввода текста ===
        input_card = tk.Frame(scrollable_frame, bg=COLORS['button_bg'], relief=tk.FLAT, bd=0)
        input_card.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(
            input_card,
            text="📝 Введите текст или URL:",
            font=("Segoe UI", 10),
            bg=COLORS['button_bg'],
            fg=COLORS['fg']
        ).pack(anchor=tk.W, padx=15, pady=(15, 5))

        self.text_entry = tk.Text(
            input_card,
            height=4,
            font=("Segoe UI", 10),
            bg=COLORS['entry_bg'],
            fg=COLORS['entry_fg'],
            relief=tk.FLAT,
            insertbackground=COLORS['fg'],
            padx=10,
            pady=10
        )
        self.text_entry.pack(padx=15, pady=(0, 15), fill=tk.X)

        # Размер QR
        size_frame = tk.Frame(input_card, bg=COLORS['button_bg'])
        size_frame.pack(padx=15, pady=(0, 15), fill=tk.X)

        tk.Label(
            size_frame,
            text="📏 Размер QR:",
            font=("Segoe UI", 10),
            bg=COLORS['button_bg'],
            fg=COLORS['fg']
        ).pack(anchor=tk.W)

        self.qr_size = tk.Scale(
            size_frame,
            from_=100,
            to=500,
            orient=tk.HORIZONTAL,
            bg=COLORS['button_bg'],
            fg=COLORS['fg'],
            highlightthickness=0,
            troughcolor=COLORS['entry_bg']
        )
        self.qr_size.set(250)
        self.qr_size.pack(fill=tk.X)

        # Кнопка создания
        self.generate_btn = tk.Button(
            input_card,
            text="Создать QR код",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['accent'],
            fg=COLORS['bg'],
            activebackground=COLORS['hover'],
            activeforeground=COLORS['bg'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.generate_qr
        )
        self.generate_btn.pack(pady=(15, 10), padx=15, fill=tk.X)

        # Кнопка сброса размера окна
        reset_btn = tk.Button(
            input_card,
            text="↺ Сбросить размер окна",
            font=("Segoe UI", 10),
            bg=COLORS['entry_bg'],
            fg=COLORS['fg'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.reset_window_size
        )
        reset_btn.pack(pady=(0, 10), padx=15, fill=tk.X)

        # === Предпросмотр QR ===
        preview_card = tk.Frame(scrollable_frame, bg=COLORS['button_bg'])
        preview_card.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        tk.Label(
            preview_card,
            text="🖼️ Предпросмотр:",
            font=("Segoe UI", 10),
            bg=COLORS['button_bg'],
            fg=COLORS['fg']
        ).pack(anchor=tk.W, padx=15, pady=(15, 5))

        self.qr_preview = tk.Label(
            preview_card,
            text="Здесь появится QR код",
            bg=COLORS['button_bg'],
            fg=COLORS['fg'],
            font=("Segoe UI", 10)
        )
        self.qr_preview.pack(pady=10, padx=15)

        # === Кнопки действий ===
        action_frame = tk.Frame(preview_card, bg=COLORS['button_bg'])
        action_frame.pack(pady=(0, 15), padx=15, fill=tk.X)
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)

        self.save_btn = tk.Button(
            action_frame,
            text="💾 Сохранить",
            bg=COLORS['entry_bg'],
            fg=COLORS['fg'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.save_qr,
            state=tk.DISABLED
        )
        self.save_btn.grid(row=0, column=0, padx=5, sticky="ew")

        self.copy_text_btn = tk.Button(
            action_frame,
            text="📋 Копировать текст",
            bg=COLORS['entry_bg'],
            fg=COLORS['fg'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.copy_text,
            state=tk.DISABLED
        )
        self.copy_text_btn.grid(row=0, column=1, padx=5, sticky="ew")

    def create_scan_tab(self):
        # Контейнер с прокруткой
        canvas = tk.Canvas(self.frame_scan, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_scan, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Карточка сканирования
        scan_card = tk.Frame(scrollable_frame, bg=COLORS['button_bg'])
        scan_card.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(
            scan_card,
            text="🔍 Выберите изображение с QR кодом:",
            font=("Segoe UI", 11),
            bg=COLORS['button_bg'],
            fg=COLORS['fg']
        ).pack(pady=(15, 5))

        self.scan_btn = tk.Button(
            scan_card,
            text="Выбрать файл",
            font=("Segoe UI", 11),
            bg=COLORS['accent'],
            fg=COLORS['bg'],
            activebackground=COLORS['hover'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.scan_qr
        )
        self.scan_btn.pack(pady=10, padx=15, fill=tk.X)

        # Предпросмотр
        preview_card = tk.Frame(scrollable_frame, bg=COLORS['button_bg'])
        preview_card.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        tk.Label(
            preview_card,
            text="🖼️ Изображение:",
            font=("Segoe UI", 10),
            bg=COLORS['button_bg'],
            fg=COLORS['fg']
        ).pack(anchor=tk.W, padx=15, pady=(15, 5))

        self.scan_preview = tk.Label(
            preview_card,
            text="Здесь появится изображение",
            bg=COLORS['button_bg'],
            fg=COLORS['fg'],
            font=("Segoe UI", 10)
        )
        self.scan_preview.pack(pady=10, padx=15)

        # Результат
        result_card = tk.Frame(scrollable_frame, bg=COLORS['button_bg'])
        result_card.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(
            result_card,
            text="📄 Результат:",
            font=("Segoe UI", 10),
            bg=COLORS['button_bg'],
            fg=COLORS['fg']
        ).pack(anchor=tk.W, padx=15, pady=(15, 5))

        self.result_label = tk.Label(
            result_card,
            text="",
            bg=COLORS['button_bg'],
            fg=COLORS['accent'],
            font=("Segoe UI", 10),
            wraplength=450,
            justify=tk.LEFT
        )
        self.result_label.pack(pady=5, padx=15)

        self.copy_result_btn = tk.Button(
            result_card,
            text="📋 Копировать результат",
            bg=COLORS['entry_bg'],
            fg=COLORS['fg'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.copy_result,
            state=tk.DISABLED
        )
        self.copy_result_btn.pack(pady=(5, 15), padx=15, fill=tk.X)

    def show_generate(self):
        self.frame_scan.pack_forget()
        self.frame_generate.pack(fill=tk.BOTH, expand=True)
        self.btn_generate.config(bg=COLORS['accent'], fg=COLORS['bg'])
        self.btn_scan.config(bg=COLORS['button_bg'], fg=COLORS['button_fg'])

    def show_scan(self):
        self.frame_generate.pack_forget()
        self.frame_scan.pack(fill=tk.BOTH, expand=True)
        self.btn_scan.config(bg=COLORS['accent'], fg=COLORS['bg'])
        self.btn_generate.config(bg=COLORS['button_bg'], fg=COLORS['button_fg'])

    def generate_qr(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Ошибка", "Введите текст для QR кода")
            return

        size = self.qr_size.get()
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size), Image.Resampling.LANCZOS)

        self.qr_image = img
        self.current_qr_path = "temp_qr.png"
        img.save(self.current_qr_path)

        photo = ImageTk.PhotoImage(img)
        self.qr_preview.config(image=photo, text="")
        self.qr_preview.image = photo

        self.save_btn.config(state=tk.NORMAL)
        self.copy_text_btn.config(state=tk.NORMAL)

    def save_qr(self):
        if self.qr_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.qr_image.save(file_path)
                messagebox.showinfo("Успех", f"QR код сохранён:\n{file_path}")

    def copy_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            pyperclip.copy(text)
            messagebox.showinfo("Успех", "Текст скопирован в буфер обмена")

    def scan_qr(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if not file_path:
            return

        img = Image.open(file_path)
        display_size = (300, 300)
        img.thumbnail(display_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.scan_preview.config(image=photo, text="")
        self.scan_preview.image = photo

        try:
            from pyzbar.pyzbar import decode
            img_full = Image.open(file_path)
            decoded = decode(img_full)

            if decoded:
                self.result_data = decoded[0].data.decode('utf-8')
                self.result_label.config(text=self.result_data)
                self.copy_result_btn.config(state=tk.NORMAL)
            else:
                self.result_label.config(text="❌ QR код не найден")
                self.copy_result_btn.config(state=tk.DISABLED)

        except Exception as e:
            self.result_label.config(text=f"Ошибка: {e}")
            self.copy_result_btn.config(state=tk.DISABLED)

    def copy_result(self):
        if hasattr(self, 'result_data') and self.result_data:
            pyperclip.copy(self.result_data)
            messagebox.showinfo("Успех", "Результат скопирован в буфер обмена")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.mainloop()