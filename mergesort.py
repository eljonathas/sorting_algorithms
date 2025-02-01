import tkinter as tk
import random

steps_ms = []
array_ms = []
current_step_ms = 0
current_canvas = None

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

def draw_state_ms(canvas, state):
    canvas.delete("all")
    arr = state["array"]
    n = len(arr)
    cw = int(canvas['width'])
    ch = int(canvas['height'])
    margin = 20
    rect_width = (cw - 2 * margin) / n
    rect_height = 50
    base_y = ch/2 - rect_height/2
    for i in range(n):
        x0 = margin + i*rect_width
        y0 = base_y
        x1 = x0 + rect_width
        y1 = y0 + rect_height
        if state["left"] is not None and state["right"] is not None and state["left"] <= i <= state["right"]:
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightyellow", outline="black", width=2)
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(arr[i]), font=("Arial", 16))
    canvas.create_text(cw/2, ch - 20, text=state["msg"], font=("Arial", 14), fill="green")

def generate_new_array_ms(canvas, num):
    global array_ms, steps_ms, current_step_ms
    array_ms = [random.randint(1, 999) for _ in range(num)]
    steps_ms = []
    current_step_ms = 0
    draw_initial_array_ms(canvas)
    iniciar_button_ms.config(state=tk.NORMAL)
    next_button_ms.config(state=tk.DISABLED)
    prev_button_ms.config(state=tk.DISABLED)
    history_button_ms.config(state=tk.DISABLED)

def draw_initial_array_ms(canvas):
    state = {
        "array": array_ms.copy(),
        "left": None,
        "right": None,
        "msg": "Vetor gerado"
    }
    draw_state_ms(canvas, state)

def start_merge_sort(canvas):
    global steps_ms, current_step_ms
    steps_ms = []
    arr_copy = array_ms.copy()
    merge_sort_ms(arr_copy, 0, len(arr_copy)-1)
    record_step_ms(arr_copy, 0, len(arr_copy)-1, "Ordenação concluída")
    current_step_ms = 0
    draw_state_ms(canvas, steps_ms[current_step_ms])
    next_button_ms.config(state=tk.NORMAL)
    prev_button_ms.config(state=tk.DISABLED)
    history_button_ms.config(state=tk.NORMAL)
    iniciar_button_ms.config(state=tk.DISABLED)

def next_step_ms():
    global current_step_ms
    if current_step_ms < len(steps_ms)-1:
        current_step_ms += 1
        draw_state_ms(current_canvas, steps_ms[current_step_ms])
    if current_step_ms == len(steps_ms)-1:
        next_button_ms.config(state=tk.DISABLED)
    if current_step_ms > 0:
        prev_button_ms.config(state=tk.NORMAL)

def prev_step_ms():
    global current_step_ms
    if current_step_ms > 0:
        current_step_ms -= 1
        draw_state_ms(current_canvas, steps_ms[current_step_ms])
    if current_step_ms == 0:
        prev_button_ms.config(state=tk.DISABLED)
    if current_step_ms < len(steps_ms)-1:
        next_button_ms.config(state=tk.NORMAL)

def show_history_ms():
    history_window = tk.Toplevel()
    history_window.title("Histórico das Instruções - MergeSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_ms):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def setup_mergesort_interface(root, canvas, controls_frame, menu_frame, voltar_menu):
    global iniciar_button_ms, next_button_ms, prev_button_ms, history_button_ms, current_canvas
    menu_frame.pack_forget()
    canvas.pack()
    controls_frame.pack(pady=10)
    for widget in controls_frame.winfo_children():
        widget.destroy()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale = tk.Scale(controls_frame, from_=5, to=15, orient=tk.HORIZONTAL)
    num_scale.set(10)
    num_scale.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=lambda: generate_new_array_ms(canvas, num_scale.get())).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_ms = tk.Button(controls_frame, text="Iniciar Ordenação", command=lambda: start_merge_sort(canvas), state=tk.NORMAL)
    iniciar_button_ms.grid(row=1, column=1, padx=5, pady=5)
    prev_button_ms = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_ms, state=tk.DISABLED)
    prev_button_ms.grid(row=2, column=0, padx=5, pady=5)
    next_button_ms = tk.Button(controls_frame, text="Próximo Passo", command=next_step_ms, state=tk.DISABLED)
    next_button_ms.grid(row=2, column=1, padx=5, pady=5)
    history_button_ms = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_ms, state=tk.DISABLED)
    history_button_ms.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_ms(canvas, num_scale.get())
    current_canvas = canvas
