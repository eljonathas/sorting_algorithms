import tkinter as tk
import random

steps_ins = []
array_ins = []
current_step_ins = 0
current_canvas = None

def record_step_ins(arr, i, j, msg):
    steps_ins.append({
        "array": arr.copy(),
        "i": i,
        "j": j,
        "msg": msg
    })

def insertion_sort_ins(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        record_step_ins(arr, i, j, f"Iniciando inserção do elemento {key} na posição {i}")
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            record_step_ins(arr, i, j, f"Movendo {arr[j]} para a direita")
            j -= 1
        arr[j+1] = key
        record_step_ins(arr, i, j, f"Inserindo {key} na posição {j+1}")
    return arr

def draw_state_ins(canvas, state):
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
        x0 = margin + i * rect_width
        y0 = base_y
        x1 = x0 + rect_width
        y1 = y0 + rect_height
        fill_color = "white"
        if state["i"] is not None and i == state["i"]:
            fill_color = "lightblue"
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="black")
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(arr[i]), font=("Arial", 16))
    canvas.create_text(cw/2, ch-20, text=state["msg"], font=("Arial", 14), fill="green")

def generate_new_array_ins(canvas, num):
    global array_ins, steps_ins, current_step_ins
    array_ins = [random.randint(1, 999) for _ in range(num)]
    steps_ins = []
    current_step_ins = 0
    draw_initial_array_ins(canvas)
    iniciar_button_ins.config(state=tk.NORMAL)
    next_button_ins.config(state=tk.DISABLED)
    prev_button_ins.config(state=tk.DISABLED)
    history_button_ins.config(state=tk.DISABLED)

def draw_initial_array_ins(canvas):
    state = {
        "array": array_ins.copy(),
        "i": None,
        "j": None,
        "msg": "Vetor gerado"
    }
    draw_state_ins(canvas, state)

def start_insertion_sort(canvas):
    global steps_ins, current_step_ins
    steps_ins = []
    arr_copy = array_ins.copy()
    insertion_sort_ins(arr_copy)
    record_step_ins(arr_copy, None, None, "Ordenação concluída")
    current_step_ins = 0
    draw_state_ins(canvas, steps_ins[current_step_ins])
    next_button_ins.config(state=tk.NORMAL)
    prev_button_ins.config(state=tk.DISABLED)
    history_button_ins.config(state=tk.NORMAL)
    iniciar_button_ins.config(state=tk.DISABLED)

def next_step_ins():
    global current_step_ins
    if current_step_ins < len(steps_ins)-1:
        current_step_ins += 1
        draw_state_ins(current_canvas, steps_ins[current_step_ins])
    if current_step_ins == len(steps_ins)-1:
        next_button_ins.config(state=tk.DISABLED)
    if current_step_ins > 0:
        prev_button_ins.config(state=tk.NORMAL)

def prev_step_ins():
    global current_step_ins
    if current_step_ins > 0:
        current_step_ins -= 1
        draw_state_ins(current_canvas, steps_ins[current_step_ins])
    if current_step_ins == 0:
        prev_button_ins.config(state=tk.DISABLED)
    if current_step_ins < len(steps_ins)-1:
        next_button_ins.config(state=tk.NORMAL)

def show_history_ins():
    history_window = tk.Toplevel()
    history_window.title("Histórico das Instruções - InsertionSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_ins):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def setup_insertionsort_interface(root, canvas, controls_frame, menu_frame, voltar_menu):
    global iniciar_button_ins, next_button_ins, prev_button_ins, history_button_ins, current_canvas
    menu_frame.pack_forget()
    canvas.pack()
    controls_frame.pack(pady=10)
    for widget in controls_frame.winfo_children():
        widget.destroy()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale = tk.Scale(controls_frame, from_=5, to=50, orient=tk.HORIZONTAL)
    num_scale.set(10)
    num_scale.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=lambda: generate_new_array_ins(canvas, num_scale.get())).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_ins = tk.Button(controls_frame, text="Iniciar Ordenação", command=lambda: start_insertion_sort(canvas), state=tk.NORMAL)
    iniciar_button_ins.grid(row=1, column=1, padx=5, pady=5)
    prev_button_ins = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_ins, state=tk.DISABLED)
    prev_button_ins.grid(row=2, column=0, padx=5, pady=5)
    next_button_ins = tk.Button(controls_frame, text="Próximo Passo", command=next_step_ins, state=tk.DISABLED)
    next_button_ins.grid(row=2, column=1, padx=5, pady=5)
    history_button_ins = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_ins, state=tk.DISABLED)
    history_button_ins.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_ins(canvas, num_scale.get())
    current_canvas = canvas
