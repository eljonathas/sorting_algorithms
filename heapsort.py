import tkinter as tk
import random
import math

steps_hs = []
array_hs = []
current_step_hs = 0
current_canvas = None

def record_step_hs(arr, current, heapify_index, msg):
    steps_hs.append({
        "array": arr.copy(),
        "current": current,
        "heapify_index": heapify_index,
        "msg": msg
    })

def heapify_hs(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    record_step_hs(arr, i, largest, f"Heapify: comparando índice {i} com {largest}")
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        record_step_hs(arr, i, largest, f"Swap: {arr[i]} e {arr[largest]}")
        heapify_hs(arr, n, largest)

def heap_sort_hs(arr):
    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        heapify_hs(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        record_step_hs(arr, 0, i, f"Swap do topo com índice {i}")
        heapify_hs(arr, i, 0)

def draw_tree_state(canvas, state):
    canvas.delete("all")
    arr = state["array"]
    n = len(arr)
    cw = int(canvas['width'])
    ch = int(canvas['height'])
    top_margin = 20
    bottom_margin = 50
    depth = math.ceil(math.log2(n+1)) if n > 0 else 1
    vertical_spacing = (ch - top_margin - bottom_margin) / (depth if depth > 0 else 1)
    positions = {}
    for level in range(depth):
        start_index = 2**level - 1
        end_index = min(n, 2**(level+1) - 1)
        count = end_index - start_index
        if count <= 0:
            continue
        for i in range(count):
            index = start_index + i
            # Distribui os nós uniformemente horizontalmente
            x = cw * (i+1) / (count+1)
            y = top_margin + level * vertical_spacing
            positions[index] = (x, y)
    for i in range(n):
        parent_pos = positions.get(i)
        left_index = 2 * i + 1
        right_index = 2 * i + 2
        if left_index < n:
            child_pos = positions.get(left_index)
            canvas.create_line(parent_pos[0], parent_pos[1], child_pos[0], child_pos[1])
        if right_index < n:
            child_pos = positions.get(right_index)
            canvas.create_line(parent_pos[0], parent_pos[1], child_pos[0], child_pos[1])
    r = 20
    for i in range(n):
        (x, y) = positions[i]
        canvas.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="black")
        canvas.create_text(x, y, text=str(arr[i]), font=("Arial", 12))
        if state.get("current") is not None and state["current"] == i:
            canvas.create_text(x, y-30, text="C", font=("Arial", 12), fill="red")
        if state.get("heapify_index") is not None and state["heapify_index"] == i:
            canvas.create_text(x, y+30, text="H", font=("Arial", 12), fill="blue")
    canvas.create_text(cw/2, ch - 10, text=state["msg"], font=("Arial", 14), fill="green")

def generate_new_array_hs(canvas, num):
    global array_hs, steps_hs, current_step_hs
    array_hs = [random.randint(1, 999) for _ in range(num)]
    steps_hs = []
    current_step_hs = 0
    depth = math.ceil(math.log2(num+1)) if num > 0 else 1
    # Ajusta a altura do canvas conforme a profundidade da árvore
    top_margin = 20
    bottom_margin = 50
    vertical_spacing = 80
    new_height = top_margin + depth * vertical_spacing + bottom_margin
    canvas.config(height=new_height)
    draw_initial_tree_hs(canvas)
    iniciar_button_hs.config(state=tk.NORMAL)
    next_button_hs.config(state=tk.DISABLED)
    prev_button_hs.config(state=tk.DISABLED)
    history_button_hs.config(state=tk.DISABLED)

def draw_initial_tree_hs(canvas):
    state = {
        "array": array_hs.copy(),
        "current": None,
        "heapify_index": None,
        "msg": "Árvore gerada"
    }
    draw_tree_state(canvas, state)

def start_heap_sort(canvas):
    global steps_hs, current_step_hs
    steps_hs = []
    arr_copy = array_hs.copy()
    heap_sort_hs(arr_copy)
    record_step_hs(arr_copy, None, None, "Ordenação concluída")
    current_step_hs = 0
    draw_tree_state(canvas, steps_hs[current_step_hs])
    next_button_hs.config(state=tk.NORMAL)
    prev_button_hs.config(state=tk.DISABLED)
    history_button_hs.config(state=tk.NORMAL)
    iniciar_button_hs.config(state=tk.DISABLED)

def next_step_hs():
    global current_step_hs
    if current_step_hs < len(steps_hs) - 1:
        current_step_hs += 1
        draw_tree_state(current_canvas, steps_hs[current_step_hs])
    if current_step_hs == len(steps_hs) - 1:
        next_button_hs.config(state=tk.DISABLED)
    if current_step_hs > 0:
        prev_button_hs.config(state=tk.NORMAL)

def prev_step_hs():
    global current_step_hs
    if current_step_hs > 0:
        current_step_hs -= 1
        draw_tree_state(current_canvas, steps_hs[current_step_hs])
    if current_step_hs == 0:
        prev_button_hs.config(state=tk.DISABLED)
    if current_step_hs < len(steps_hs) - 1:
        next_button_hs.config(state=tk.NORMAL)

def show_history_hs():
    history_window = tk.Toplevel()
    history_window.title("Histórico das Instruções - HeapSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_hs):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def setup_heapsort_interface(root, canvas, controls_frame, menu_frame, voltar_menu):
    global iniciar_button_hs, next_button_hs, prev_button_hs, history_button_hs, current_canvas
    menu_frame.pack_forget()
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    controls_frame.pack(side=tk.BOTTOM, pady=10)
    for widget in controls_frame.winfo_children():
        widget.destroy()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale = tk.Scale(controls_frame, from_=5, to=50, orient=tk.HORIZONTAL)
    num_scale.set(10)
    num_scale.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Nova Árvore", command=lambda: generate_new_array_hs(canvas, num_scale.get())).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_hs = tk.Button(controls_frame, text="Iniciar Ordenação", command=lambda: start_heap_sort(canvas), state=tk.NORMAL)
    iniciar_button_hs.grid(row=1, column=1, padx=5, pady=5)
    prev_button_hs = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_hs, state=tk.DISABLED)
    prev_button_hs.grid(row=2, column=0, padx=5, pady=5)
    next_button_hs = tk.Button(controls_frame, text="Próximo Passo", command=next_step_hs, state=tk.DISABLED)
    next_button_hs.grid(row=2, column=1, padx=5, pady=5)
    history_button_hs = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_hs, state=tk.DISABLED)
    history_button_hs.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_hs(canvas, num_scale.get())
    current_canvas = canvas
