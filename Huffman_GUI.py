import tkinter as tk
from tkinter import filedialog, messagebox
import os
from File_Compressor_Using_Huffman_Encoding_Algorithm_Project import Huffmancode

class HuffmanGUI:
    huffman = Huffmancode()

    def __init__(self, master):
        self.master = master
        self.master.title("Huffman Coding GUI")

        self.file_path_label = tk.Label(self.master, text="File Path:")
        self.file_path_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_entry = tk.Entry(self.master, width=50)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        self.compress_button = tk.Button(self.master, text="Compress", command=self.compress_file)
        self.compress_button.grid(row=1, column=0, padx=10, pady=10)

        self.decompress_button = tk.Button(self.master, text="Decompress", command=self.decompress_file)
        self.decompress_button.grid(row=1, column=1, padx=10, pady=10)

        self.file_size_label = tk.Label(self.master, text="Original File Size: N/A")
        self.file_size_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.compressed_size_label = tk.Label(self.master, text="Compressed File Size: N/A")
        self.compressed_size_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)

    def compress_file(self):
        file_path = self.file_path_entry.get()
        if file_path:
            self.huffman.path = file_path
            try:
                compressed_file = self.huffman.Compression()
                self.update_file_size_labels(file_path, compressed_file)
                messagebox.showinfo("Success", "Compressing data: Compression successful")
            except Exception as e:
                messagebox.showerror("Error", f"Compressing data failed: {str(e)}")
                print(f"Exception during compression: {e}")
        else:
            messagebox.showwarning("Error", "Please select a file for compression.")

    def decompress_file(self):
        file_path = self.file_path_entry.get()
        if file_path:
            try:
                decompressed_file = self.huffman.Decompress(file_path)
                messagebox.showinfo("Success", "Decompressing: Decompression successful")
            except Exception as e:
                messagebox.showerror("Error", f"Decompression failed: {str(e)}")
        else:
            messagebox.showwarning("Error", "Please select a file for decompression.")

    def update_file_size_labels(self, original_file, new_file):
        original_size = os.path.getsize(original_file)
        compressed_size = os.path.getsize(new_file)
        self.file_size_label.config(text=f"Original File Size: {original_size} bytes")
        self.compressed_size_label.config(text=f"Compressed File Size: {compressed_size} bytes")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()
