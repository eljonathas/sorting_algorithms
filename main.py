import tkinter as tk
import random
import math

root = tk.Tk()
root.title("Visualização de Algoritmos de Ordenação")

current_algorithm = None
menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)
canvas = tk.Canvas(root, width=800, height=300, bg="white")
controls_frame = tk.Frame(root)

def clear_controls_frame():
    for widget in controls_frame.winfo_children():
        widget.destroy()

def voltar_menu():
    canvas.unbind("<Button-1>")
    canvas.pack_forget()
    controls_frame.pack_forget()
    menu_frame.pack(pady=20)

# QuickSort
steps_qs = []
array_qs = []
current_step_qs = 0
selected_pivot_index = None
pivot_selected = False

def record_step_qs(arr, low, high, i, j, pivot, msg):
    steps_qs.append({
        "array": arr.copy(),
        "low": low,
        "high": high,
        "i": i,
        "j": j,
        "pivot": pivot,
        "msg": msg
    })

def partition_qs(arr, low, high):
    pivot = arr[high]
    record_step_qs(arr, low, high, None, None, high, "Pivot selecionado")
    i = low - 1
    for j in range(low, high):
        record_step_qs(arr, low, high, i, j, high, f"Comparando {arr[j]} com pivot {pivot}")
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            record_step_qs(arr, low, high, i, j, high, f"Swap: {arr[i]} e {arr[j]}")
    arr[i+1], arr[high] = arr[high], arr[i+1]
    record_step_qs(arr, low, high, i+1, high, i+1, "Pivot para posição correta")
    return i+1

def quick_sort_qs(arr, low, high):
    if low < high:
        pi = partition_qs(arr, low, high)
        quick_sort_qs(arr, low, pi - 1)
        quick_sort_qs(arr, pi + 1, high)

def start_quick_sort():
    global steps_qs, current_step_qs
    steps_qs = []
    arr_copy = array_qs.copy()
    quick_sort_qs(arr_copy, 0, len(arr_copy) - 1)
    record_step_qs(arr_copy, 0, len(arr_copy) - 1, None, None, None, "Ordenação concluída")
    current_step_qs = 0
    draw_state_qs(steps_qs[current_step_qs])
    next_button_qs.config(state=tk.NORMAL)
    prev_button_qs.config(state=tk.DISABLED)
    history_button_qs.config(state=tk.NORMAL)
    iniciar_button_qs.config(state=tk.DISABLED)

def next_step_qs():
    global current_step_qs
    if current_step_qs < len(steps_qs) - 1:
        current_step_qs += 1
        draw_state_qs(steps_qs[current_step_qs])
    if current_step_qs == len(steps_qs) - 1:
        next_button_qs.config(state=tk.DISABLED)
    if current_step_qs > 0:
        prev_button_qs.config(state=tk.NORMAL)

def prev_step_qs():
    global current_step_qs
    if current_step_qs > 0:
        current_step_qs -= 1
        draw_state_qs(steps_qs[current_step_qs])
    if current_step_qs == 0:
        prev_button_qs.config(state=tk.DISABLED)
    if current_step_qs < len(steps_qs) - 1:
        next_button_qs.config(state=tk.NORMAL)

def show_history_qs():
    history_window = tk.Toplevel(root)
    history_window.title("Histórico das Instruções - QuickSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_qs):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def draw_state_qs(state):
    canvas.delete("all")
    arr = state["array"]
    n = len(arr)
    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    margin = 20
    rect_width = (cw - 2 * margin) / n
    rect_height = 50
    base_y = ch / 2 - rect_height / 2
    for i in range(n):
        x0 = margin + i * rect_width
        y0 = base_y
        x1 = x0 + rect_width
        y1 = y0 + rect_height
        if state["low"] is not None and state["high"] is not None and state["low"] <= i <= state["high"]:
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue", outline="black", width=2)
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(arr[i]), font=("Arial", 16))
        labels = []
        if state["pivot"] is not None and state["pivot"] == i:
            labels.append("P")
        if state["i"] is not None and state["i"] == i:
            labels.append("i")
        if state["j"] is not None and state["j"] == i:
            labels.append("j")
        if labels:
            canvas.create_text((x0 + x1) / 2, y0 - 10, text=",".join(labels), font=("Arial", 12), fill="red")
    canvas.create_text(cw / 2, ch - 20, text=state["msg"], font=("Arial", 14), fill="green")

def select_pivot(event):
    global selected_pivot_index, pivot_selected, array_qs
    if pivot_selected:
        return
    cw = canvas.winfo_width()
    margin = 20
    n = len(array_qs)
    rect_width = (cw - 2 * margin) / n
    x = event.x
    if x < margin or x > cw - margin:
        return
    index = int((x - margin) // rect_width)
    if index < 0 or index >= n:
        return
    selected_pivot_index = index
    pivot_value = array_qs[index]
    if index != n - 1:
        array_qs[index], array_qs[n - 1] = array_qs[n - 1], array_qs[index]
        msg = f"Pivot selecionado manualmente: {pivot_value} (movido para a última posição)"
    else:
        msg = f"Pivot selecionado manualmente: {pivot_value}"
    pivot_selected = True
    record_step_qs(array_qs, 0, len(array_qs) - 1, None, None, n - 1, msg)
    draw_state_qs({
        "array": array_qs.copy(),
        "low": None,
        "high": None,
        "i": None,
        "j": None,
        "pivot": n - 1,
        "msg": msg
    })
    canvas.unbind("<Button-1>")
    iniciar_button_qs.config(state=tk.NORMAL)

def generate_new_array_qs():
    global array_qs, steps_qs, current_step_qs, pivot_selected, selected_pivot_index
    n = num_scale_qs.get()
    array_qs = [random.randint(1, 999) for _ in range(n)]
    steps_qs = []
    current_step_qs = 0
    pivot_selected = False
    selected_pivot_index = None
    draw_initial_array_qs()
    canvas.bind("<Button-1>", select_pivot)
    iniciar_button_qs.config(state=tk.DISABLED)
    next_button_qs.config(state=tk.DISABLED)
    prev_button_qs.config(state=tk.DISABLED)
    history_button_qs.config(state=tk.DISABLED)

def draw_initial_array_qs():
    state = {
        "array": array_qs.copy(),
        "low": None,
        "high": None,
        "i": None,
        "j": None,
        "pivot": None,
        "msg": "Vetor gerado - Clique em uma célula para selecionar o pivot"
    }
    draw_state_qs(state)

# MergeSort
steps_ms = []
array_ms = []
current_step_ms = 0

def record_step_ms(arr, left, right, msg):
    steps_ms.append({
        "array": arr.copy(),
        "left": left,
        "right": right,
        "msg": msg
    })

def merge_ms(arr, left, mid, right):
    L = arr[left:mid+1]
    R = arr[mid+1:right+1]
    i = 0
    j = 0
    k = left
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1
    record_step_ms(arr, left, right, f"Merge de índices {left} a {right}")

def merge_sort_ms(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_ms(arr, left, mid)
        merge_sort_ms(arr, mid+1, right)
        merge_ms(arr, left, mid, right)

def start_merge_sort():
    global steps_ms, current_step_ms
    steps_ms = []
    arr_copy = array_ms.copy()
    merge_sort_ms(arr_copy, 0, len(arr_copy) - 1)
    record_step_ms(arr_copy, 0, len(arr_copy) - 1, "Ordenação concluída")
    current_step_ms = 0
    draw_state_ms(steps_ms[current_step_ms])
    next_button_ms.config(state=tk.NORMAL)
    prev_button_ms.config(state=tk.DISABLED)
    history_button_ms.config(state=tk.NORMAL)
    iniciar_button_ms.config(state=tk.DISABLED)

def next_step_ms():
    global current_step_ms
    if current_step_ms < len(steps_ms) - 1:
        current_step_ms += 1
        draw_state_ms(steps_ms[current_step_ms])
    if current_step_ms == len(steps_ms) - 1:
        next_button_ms.config(state=tk.DISABLED)
    if current_step_ms > 0:
        prev_button_ms.config(state=tk.NORMAL)

def prev_step_ms():
    global current_step_ms
    if current_step_ms > 0:
        current_step_ms -= 1
        draw_state_ms(steps_ms[current_step_ms])
    if current_step_ms == 0:
        prev_button_ms.config(state=tk.DISABLED)
    if current_step_ms < len(steps_ms) - 1:
        next_button_ms.config(state=tk.NORMAL)

def show_history_ms():
    history_window = tk.Toplevel(root)
    history_window.title("Histórico das Instruções - MergeSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_ms):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def draw_state_ms(state):
    canvas.delete("all")
    arr = state["array"]
    n = len(arr)
    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    margin = 20
    rect_width = (cw - 2 * margin) / n
    rect_height = 50
    base_y = ch / 2 - rect_height / 2
    for i in range(n):
        x0 = margin + i * rect_width
        y0 = base_y
        x1 = x0 + rect_width
        y1 = y0 + rect_height
        if state["left"] is not None and state["right"] is not None and state["left"] <= i <= state["right"]:
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightyellow", outline="black", width=2)
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(arr[i]), font=("Arial", 16))
    canvas.create_text(cw / 2, ch - 20, text=state["msg"], font=("Arial", 14), fill="green")

def generate_new_array_ms():
    global array_ms, steps_ms, current_step_ms
    n = num_scale_ms.get()
    array_ms = [random.randint(1, 999) for _ in range(n)]
    steps_ms = []
    current_step_ms = 0
    draw_initial_array_ms()
    iniciar_button_ms.config(state=tk.NORMAL)
    next_button_ms.config(state=tk.DISABLED)
    prev_button_ms.config(state=tk.DISABLED)
    history_button_ms.config(state=tk.DISABLED)

def draw_initial_array_ms():
    state = {
        "array": array_ms.copy(),
        "left": None,
        "right": None,
        "msg": "Vetor gerado"
    }
    draw_state_ms(state)

# HeapSort
steps_hs = []
array_hs = []
current_step_hs = 0

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

def start_heap_sort():
    global steps_hs, current_step_hs
    steps_hs = []
    arr_copy = array_hs.copy()
    heap_sort_hs(arr_copy)
    record_step_hs(arr_copy, None, None, "Ordenação concluída")
    current_step_hs = 0
    draw_tree_state(steps_hs[current_step_hs])
    next_button_hs.config(state=tk.NORMAL)
    prev_button_hs.config(state=tk.DISABLED)
    history_button_hs.config(state=tk.NORMAL)
    iniciar_button_hs.config(state=tk.DISABLED)

def next_step_hs():
    global current_step_hs
    if current_step_hs < len(steps_hs) - 1:
        current_step_hs += 1
        draw_tree_state(steps_hs[current_step_hs])
    if current_step_hs == len(steps_hs) - 1:
        next_button_hs.config(state=tk.DISABLED)
    if current_step_hs > 0:
        prev_button_hs.config(state=tk.NORMAL)

def prev_step_hs():
    global current_step_hs
    if current_step_hs > 0:
        current_step_hs -= 1
        draw_tree_state(steps_hs[current_step_hs])
    if current_step_hs == 0:
        prev_button_hs.config(state=tk.DISABLED)
    if current_step_hs < len(steps_hs) - 1:
        next_button_hs.config(state=tk.NORMAL)

def show_history_hs():
    history_window = tk.Toplevel(root)
    history_window.title("Histórico das Instruções - HeapSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_hs):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def draw_tree_state(state):
    canvas.delete("all")
    arr = state["array"]
    n = len(arr)
    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    level = 0
    nodes = []
    i = 0
    while i < n:
        count = 2 ** level
        level_nodes = []
        for j in range(count):
            if i < n:
                level_nodes.append(arr[i])
                i += 1
        nodes.append(level_nodes)
        level += 1
    vertical_spacing = 60
    for lvl, level_nodes in enumerate(nodes):
        num_nodes = len(level_nodes)
        horizontal_spacing = cw / (num_nodes + 1)
        y = vertical_spacing * (lvl + 1)
        for idx, value in enumerate(level_nodes):
            x = horizontal_spacing * (idx + 1)
            r = 20
            canvas.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="black")
            canvas.create_text(x, y, text=str(value), font=("Arial", 12))
            index_in_array = (2**lvl - 1) + idx
            if state["current"] is not None and state["current"] == index_in_array:
                canvas.create_text(x, y-30, text="C", font=("Arial", 12), fill="red")
            if state["heapify_index"] is not None and state["heapify_index"] == index_in_array:
                canvas.create_text(x, y+30, text="H", font=("Arial", 12), fill="blue")
            left_index = 2*index_in_array + 1
            right_index = 2*index_in_array + 2
            if left_index < n:
                child_lvl = math.floor(math.log2(left_index+1))
                child_pos = left_index - (2**child_lvl - 1)
                num_child = 2**child_lvl
                child_horizontal_spacing = cw / (num_child + 1)
                child_x = child_horizontal_spacing * (child_pos + 1)
                child_y = vertical_spacing * (child_lvl + 1)
                canvas.create_line(x, y, child_x, child_y)
            if right_index < n:
                child_lvl = math.floor(math.log2(right_index+1))
                child_pos = right_index - (2**child_lvl - 1)
                num_child = 2**child_lvl
                child_horizontal_spacing = cw / (num_child + 1)
                child_x = child_horizontal_spacing * (child_pos + 1)
                child_y = vertical_spacing * (child_lvl + 1)
                canvas.create_line(x, y, child_x, child_y)
    canvas.create_text(cw/2, ch - 20, text=state["msg"], font=("Arial", 14), fill="green")

def generate_new_array_hs():
    global array_hs, steps_hs, current_step_hs
    n = num_scale_hs.get()
    array_hs = [random.randint(1, 999) for _ in range(n)]
    steps_hs = []
    current_step_hs = 0
    draw_initial_tree_hs()
    iniciar_button_hs.config(state=tk.NORMAL)
    next_button_hs.config(state=tk.DISABLED)
    prev_button_hs.config(state=tk.DISABLED)
    history_button_hs.config(state=tk.DISABLED)

def draw_initial_tree_hs():
    state = {
        "array": array_hs.copy(),
        "current": None,
        "heapify_index": None,
        "msg": "Árvore gerada"
    }
    draw_tree_state(state)

# Interfaces de Algoritmos
def setup_quicksort_interface():
    global current_algorithm, num_scale_qs, iniciar_button_qs, next_button_qs, prev_button_qs, history_button_qs
    current_algorithm = "quicksort"
    menu_frame.pack_forget()
    canvas.pack()
    controls_frame.pack(pady=10)
    clear_controls_frame()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale_qs = tk.Scale(controls_frame, from_=5, to=50, orient=tk.HORIZONTAL)
    num_scale_qs.set(10)
    num_scale_qs.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=generate_new_array_qs).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_qs = tk.Button(controls_frame, text="Iniciar Ordenação", command=start_quick_sort, state=tk.DISABLED)
    iniciar_button_qs.grid(row=1, column=1, padx=5, pady=5)
    prev_button_qs = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_qs, state=tk.DISABLED)
    prev_button_qs.grid(row=2, column=0, padx=5, pady=5)
    next_button_qs = tk.Button(controls_frame, text="Próximo Passo", command=next_step_qs, state=tk.DISABLED)
    next_button_qs.grid(row=2, column=1, padx=5, pady=5)
    history_button_qs = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_qs, state=tk.DISABLED)
    history_button_qs.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_qs()

def setup_merge_sort_interface():
    global current_algorithm, num_scale_ms, iniciar_button_ms, next_button_ms, prev_button_ms, history_button_ms
    current_algorithm = "mergesort"
    menu_frame.pack_forget()
    canvas.pack()
    controls_frame.pack(pady=10)
    clear_controls_frame()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale_ms = tk.Scale(controls_frame, from_=5, to=50, orient=tk.HORIZONTAL)
    num_scale_ms.set(10)
    num_scale_ms.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=generate_new_array_ms).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_ms = tk.Button(controls_frame, text="Iniciar Ordenação", command=start_merge_sort, state=tk.NORMAL)
    iniciar_button_ms.grid(row=1, column=1, padx=5, pady=5)
    prev_button_ms = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_ms, state=tk.DISABLED)
    prev_button_ms.grid(row=2, column=0, padx=5, pady=5)
    next_button_ms = tk.Button(controls_frame, text="Próximo Passo", command=next_step_ms, state=tk.DISABLED)
    next_button_ms.grid(row=2, column=1, padx=5, pady=5)
    history_button_ms = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_ms, state=tk.DISABLED)
    history_button_ms.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_ms()

def setup_heap_sort_interface():
    global current_algorithm, num_scale_hs, iniciar_button_hs, next_button_hs, prev_button_hs, history_button_hs
    current_algorithm = "heapsort"
    menu_frame.pack_forget()
    canvas.pack()
    controls_frame.pack(pady=10)
    clear_controls_frame()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale_hs = tk.Scale(controls_frame, from_=5, to=50, orient=tk.HORIZONTAL)
    num_scale_hs.set(10)
    num_scale_hs.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Nova Árvore", command=generate_new_array_hs).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_hs = tk.Button(controls_frame, text="Iniciar Ordenação", command=start_heap_sort, state=tk.NORMAL)
    iniciar_button_hs.grid(row=1, column=1, padx=5, pady=5)
    prev_button_hs = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_hs, state=tk.DISABLED)
    prev_button_hs.grid(row=2, column=0, padx=5, pady=5)
    next_button_hs = tk.Button(controls_frame, text="Próximo Passo", command=next_step_hs, state=tk.DISABLED)
    next_button_hs.grid(row=2, column=1, padx=5, pady=5)
    history_button_hs = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_hs, state=tk.DISABLED)
    history_button_hs.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_hs()

tk.Label(menu_frame, text="Selecione o Algoritmo para Visualização", font=("Arial", 16)).pack(pady=10)
tk.Button(menu_frame, text="QuickSort", command=setup_quicksort_interface, width=20).pack(pady=5)
tk.Button(menu_frame, text="MergeSort", command=setup_merge_sort_interface, width=20).pack(pady=5)
tk.Button(menu_frame, text="HeapSort", command=setup_heap_sort_interface, width=20).pack(pady=5)

root.mainloop()
