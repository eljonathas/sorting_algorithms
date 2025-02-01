import tkinter as tk
import random

steps_qs = []
array_qs = []
current_step_qs = 0
selected_pivot_index = None
pivot_selected = False
current_canvas = None

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

def draw_state_qs(canvas, state):
    canvas.delete("all")
    arr = state["array"]
    n = len(arr)
    cw = int(canvas['width'])
    ch = int(canvas['height'])
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
    canvas.create_text(cw/2, ch - 20, text=state["msg"], font=("Arial", 14), fill="green")

def select_pivot(event, canvas):
    global selected_pivot_index, pivot_selected, array_qs
    if pivot_selected:
        return
    cw = int(canvas['width'])
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
    record_step_qs(array_qs, 0, len(array_qs)-1, None, None, n-1, msg)
    draw_state_qs(canvas, {
        "array": array_qs.copy(),
        "low": None,
        "high": None,
        "i": None,
        "j": None,
        "pivot": n-1,
        "msg": msg
    })
    canvas.unbind("<Button-1>")
    iniciar_button_qs.config(state=tk.NORMAL)

def generate_new_array_qs(canvas, num):
    global array_qs, steps_qs, current_step_qs, pivot_selected, selected_pivot_index
    array_qs = [random.randint(1, 999) for _ in range(num)]
    steps_qs = []
    current_step_qs = 0
    pivot_selected = False
    selected_pivot_index = None
    draw_initial_array_qs(canvas)
    canvas.bind("<Button-1>", lambda event: select_pivot(event, canvas))
    iniciar_button_qs.config(state=tk.DISABLED)
    next_button_qs.config(state=tk.DISABLED)
    prev_button_qs.config(state=tk.DISABLED)
    history_button_qs.config(state=tk.DISABLED)

def draw_initial_array_qs(canvas):
    state = {
        "array": array_qs.copy(),
        "low": None,
        "high": None,
        "i": None,
        "j": None,
        "pivot": None,
        "msg": "Vetor gerado - Clique em uma célula para selecionar o pivot"
    }
    draw_state_qs(canvas, state)

def start_quick_sort(canvas):
    global steps_qs, current_step_qs
    steps_qs = []
    arr_copy = array_qs.copy()
    quick_sort_qs(arr_copy, 0, len(arr_copy)-1)
    record_step_qs(arr_copy, 0, len(arr_copy)-1, None, None, None, "Ordenação concluída")
    current_step_qs = 0
    draw_state_qs(canvas, steps_qs[current_step_qs])
    next_button_qs.config(state=tk.NORMAL)
    prev_button_qs.config(state=tk.DISABLED)
    history_button_qs.config(state=tk.NORMAL)
    iniciar_button_qs.config(state=tk.DISABLED)

def next_step_qs():
    global current_step_qs
    if current_step_qs < len(steps_qs)-1:
        current_step_qs += 1
        draw_state_qs(current_canvas, steps_qs[current_step_qs])
    if current_step_qs == len(steps_qs)-1:
        next_button_qs.config(state=tk.DISABLED)
    if current_step_qs > 0:
        prev_button_qs.config(state=tk.NORMAL)

def prev_step_qs():
    global current_step_qs
    if current_step_qs > 0:
        current_step_qs -= 1
        draw_state_qs(current_canvas, steps_qs[current_step_qs])
    if current_step_qs == 0:
        prev_button_qs.config(state=tk.DISABLED)
    if current_step_qs < len(steps_qs)-1:
        next_button_qs.config(state=tk.NORMAL)

def show_history_qs():
    history_window = tk.Toplevel()
    history_window.title("Histórico das Instruções - QuickSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_qs):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def setup_quicksort_interface(root, canvas, controls_frame, menu_frame, voltar_menu):
    global iniciar_button_qs, next_button_qs, prev_button_qs, history_button_qs, current_canvas
    menu_frame.pack_forget()
    canvas.pack()
    controls_frame.pack(pady=10)
    for widget in controls_frame.winfo_children():
        widget.destroy()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale = tk.Scale(controls_frame, from_=5, to=50, orient=tk.HORIZONTAL)
    num_scale.set(10)
    num_scale.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=lambda: generate_new_array_qs(canvas, num_scale.get())).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_qs = tk.Button(controls_frame, text="Iniciar Ordenação", command=lambda: start_quick_sort(canvas), state=tk.DISABLED)
    iniciar_button_qs.grid(row=1, column=1, padx=5, pady=5)
    prev_button_qs = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_qs, state=tk.DISABLED)
    prev_button_qs.grid(row=2, column=0, padx=5, pady=5)
    next_button_qs = tk.Button(controls_frame, text="Próximo Passo", command=next_step_qs, state=tk.DISABLED)
    next_button_qs.grid(row=2, column=1, padx=5, pady=5)
    history_button_qs = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_qs, state=tk.DISABLED)
    history_button_qs.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_qs(canvas, num_scale.get())
    current_canvas = canvas
