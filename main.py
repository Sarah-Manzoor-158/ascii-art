"""ASCII Art Generator — GUI."""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from converter import image_to_ascii


class AsciiArtApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ASCII Art Generator")
        self.root.geometry("720x560")
        self.root.minsize(480, 400)

        self.image_path: str | None = None
        self.ascii_result: str = ""

        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill=tk.X)

        ttk.Label(header, text="ASCII Art Generator", font=("Segoe UI", 16, "bold")).pack(
            anchor=tk.W
        )
        ttk.Label(
            header,
            text="Choose an image and convert it to ASCII art.",
            font=("Segoe UI", 10),
        ).pack(anchor=tk.W, pady=(4, 0))

        controls = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        controls.pack(fill=tk.X)

        ttk.Button(controls, text="Choose Image", command=self._choose_image).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(controls, text="Generate", command=self._generate).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(controls, text="Save as .txt", command=self._save).pack(side=tk.LEFT)

        ttk.Label(controls, text="Width:").pack(side=tk.LEFT, padx=(16, 4))
        self.width_var = tk.IntVar(value=100)
        width_spin = ttk.Spinbox(
            controls,
            from_=40,
            to=200,
            width=6,
            textvariable=self.width_var,
        )
        width_spin.pack(side=tk.LEFT)

        self.path_label = ttk.Label(self.root, text="No image selected", padding=(12, 0))
        self.path_label.pack(fill=tk.X, anchor=tk.W)

        preview_frame = ttk.Frame(self.root, padding=12)
        preview_frame.pack(fill=tk.BOTH, expand=True)

        self.preview = scrolledtext.ScrolledText(
            preview_frame,
            wrap=tk.NONE,
            font=("Consolas", 8),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
        )
        self.preview.pack(fill=tk.BOTH, expand=True)

        status = ttk.Frame(self.root, padding=(12, 8))
        status.pack(fill=tk.X)
        self.status_label = ttk.Label(status, text="Ready")
        self.status_label.pack(anchor=tk.W)

    def _choose_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        self.image_path = path
        name = path.split("/")[-1].split("\\")[-1]
        self.path_label.config(text=f"Selected: {name}")
        self.status_label.config(text="Image loaded — click Generate")

    def _generate(self) -> None:
        if not self.image_path:
            messagebox.showinfo("No image", "Please choose an image first.")
            return

        try:
            width = self.width_var.get()
            self.ascii_result = image_to_ascii(self.image_path, width=width)
        except Exception as exc:
            messagebox.showerror("Error", f"Could not convert image:\n{exc}")
            return

        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, self.ascii_result)
        self.status_label.config(text="ASCII art generated")

    def _save(self) -> None:
        if not self.ascii_result:
            messagebox.showinfo("Nothing to save", "Generate ASCII art first.")
            return

        path = filedialog.asksaveasfilename(
            title="Save ASCII art",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.ascii_result)

        self.status_label.config(text=f"Saved to {path.split('/')[-1].split(chr(92))[-1]}")


def main() -> None:
    root = tk.Tk()
    AsciiArtApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
