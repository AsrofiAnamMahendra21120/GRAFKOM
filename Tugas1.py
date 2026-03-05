import math
import tkinter as tk
from tkinter import messagebox

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0: return Vector3(0, 0, 0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

class Matrix4:
    def __init__(self):
        self.mat = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]

    def __str__(self):
        return "\n".join(["  ".join([f"{v:6.1f}" for v in row]) for row in self.mat])

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Geometri 3D")
        self.root.geometry("400x550")
        
        # UI Setup
        tk.Label(root, text="Input Koordinat Segitiga (x, y, z)", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.inputs = []
        for i, label in enumerate(['Titik A', 'Titik B', 'Titik C']):
            frame = tk.Frame(root)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{label}: ", width=10).pack(side=tk.LEFT)
            entries = []
            for j in range(3):
                e = tk.Entry(frame, width=5)
                e.insert(0, "0")
                e.pack(side=tk.LEFT, padx=2)
                entries.append(e)
            self.inputs.append(entries)

        tk.Button(root, text="Hitung Sekarang", command=self.calculate, bg="#4CAF50", fg="white", font=('Arial', 10, 'bold')).pack(pady=20)

        self.result_text = tk.Text(root, height=15, width=45, state='disabled', font=('Courier', 10))
        self.result_text.pack(pady=10, padx=10)

    def calculate(self):
        try:
            coords = []
            for group in self.inputs:
                coords.append(Vector3(*(float(e.get()) for e in group)))
            
            A, B, C = coords
            sisi_AB = B - A
            sisi_AC = C - A
            cp = sisi_AB.cross(sisi_AC)
            normal = cp.normalize()
            luas = 0.5 * cp.magnitude()
            m4 = Matrix4()

            output = (
                f"HASIL PERHITUNGAN:\n"
                f"{'-'*30}\n"
                f"Sisi AB : {sisi_AB}\n"
                f"Sisi AC : {sisi_AC}\n\n"
                f"Normal  : {normal}\n"
                f"Luas    : {luas:.2f} satuan\n"
                f"{'-'*30}\n"
                f"Matrix4 (Identity):\n{m4}"
            )

            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, output)
            self.result_text.config(state='disabled')

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()