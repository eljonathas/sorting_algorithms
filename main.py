import tkinter as tk
from quicksort import setup_quicksort_interface
from mergesort import setup_mergesort_interface
from heapsort import setup_heapsort_interface
from insertionsort import setup_insertionsort_interface
from bubblesort import setup_bubblesort_interface

root = tk.Tk()
root.title("Visualização de Algoritmos de Ordenação")

menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)

canvas = tk.Canvas(root, width=800, height=300, bg="white")
controls_frame = tk.Frame(root)

def voltar_menu():
    canvas.delete("all")
    canvas.pack_forget()
    controls_frame.pack_forget()
    menu_frame.pack(pady=20)

tk.Label(menu_frame, text="Selecione o Algoritmo para Visualização", font=("Arial", 16)).pack(pady=10)
tk.Button(menu_frame, text="QuickSort", command=lambda: setup_quicksort_interface(root, canvas, controls_frame, menu_frame, voltar_menu), width=20).pack(pady=5)
tk.Button(menu_frame, text="MergeSort", command=lambda: setup_mergesort_interface(root, canvas, controls_frame, menu_frame, voltar_menu), width=20).pack(pady=5)
tk.Button(menu_frame, text="HeapSort", command=lambda: setup_heapsort_interface(root, canvas, controls_frame, menu_frame, voltar_menu), width=20).pack(pady=5)
tk.Button(menu_frame, text="InsertionSort", command=lambda: setup_insertionsort_interface(root, canvas, controls_frame, menu_frame, voltar_menu), width=20).pack(pady=5)
tk.Button(menu_frame, text="BubbleSort", command=lambda: setup_bubblesort_interface(root, canvas, controls_frame, menu_frame, voltar_menu), width=20).pack(pady=5)

root.mainloop()
