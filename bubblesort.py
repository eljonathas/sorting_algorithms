import tkinter as tk
import random

steps_bubble = []
array_bubble = []
current_step_bubble = 0
current_canvas = None

def record_step_bubble(arr, i, j, msg):
    steps_bubble.append({
        "array": arr.copy(),
        "i": i,
        "j": j,
        "msg": msg
    })

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            record_step_bubble(arr, i, j, f"Comparando {arr[j]} e {arr[j+1]}")
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                record_step_bubble(arr, i, j, f"Swap: {arr[j]} e {arr[j+1]}")
    return arr

def draw_state_bubble(canvas, state):
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
        if state["j"] is not None and (i == state["j"] or i == state["j"]+1):
            fill_color = "lightblue"
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="black")
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(arr[i]), font=("Arial", 16))
    canvas.create_text(cw/2, ch-20, text=state["msg"], font=("Arial", 14), fill="green")

def generate_new_array_bubble(canvas, num):
    global array_bubble, steps_bubble, current_step_bubble
    array_bubble = [random.randint(1, 999) for _ in range(num)]
    steps_bubble = []
    current_step_bubble = 0
    draw_initial_array_bubble(canvas)
    iniciar_button_bubble.config(state=tk.NORMAL)
    next_button_bubble.config(state=tk.DISABLED)
    prev_button_bubble.config(state=tk.DISABLED)
    history_button_bubble.config(state=tk.DISABLED)

def draw_initial_array_bubble(canvas):
    state = {
        "array": array_bubble.copy(),
        "i": None,
        "j": None,
        "msg": "Vetor gerado"
    }
    draw_state_bubble(canvas, state)

def start_bubble_sort(canvas):
    global steps_bubble, current_step_bubble
    steps_bubble = []
    arr_copy = array_bubble.copy()
    bubble_sort(arr_copy)
    record_step_bubble(arr_copy, None, None, "Ordenação concluída")
    current_step_bubble = 0
    draw_state_bubble(canvas, steps_bubble[current_step_bubble])
    next_button_bubble.config(state=tk.NORMAL)
    prev_button_bubble.config(state=tk.DISABLED)
    history_button_bubble.config(state=tk.NORMAL)
    iniciar_button_bubble.config(state=tk.DISABLED)

def next_step_bubble():
    global current_step_bubble
    if current_step_bubble < len(steps_bubble)-1:
        current_step_bubble += 1
        draw_state_bubble(current_canvas, steps_bubble[current_step_bubble])
    if current_step_bubble == len(steps_bubble)-1:
        next_button_bubble.config(state=tk.DISABLED)
    if current_step_bubble > 0:
        prev_button_bubble.config(state=tk.NORMAL)

def prev_step_bubble():
    global current_step_bubble
    if current_step_bubble > 0:
        current_step_bubble -= 1
        draw_state_bubble(current_canvas, steps_bubble[current_step_bubble])
    if current_step_bubble == 0:
        prev_button_bubble.config(state=tk.DISABLED)
    if current_step_bubble < len(steps_bubble)-1:
        next_button_bubble.config(state=tk.NORMAL)

def show_history_bubble():
    history_window = tk.Toplevel()
    history_window.title("Histórico das Instruções - BubbleSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_bubble):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def setup_bubblesort_interface(root, canvas, controls_frame, menu_frame, voltar_menu):
    global iniciar_button_bubble, next_button_bubble, prev_button_bubble, history_button_bubble, current_canvas
    menu_frame.pack_forget()
    canvas.pack()
    controls_frame.pack(pady=10)
    for widget in controls_frame.winfo_children():
        widget.destroy()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale = tk.Scale(controls_frame, from_=5, to=50, orient=tk.HORIZONTAL)
    num_scale.set(10)
    num_scale.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=lambda: generate_new_array_bubble(canvas, num_scale.get())).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_bubble = tk.Button(controls_frame, text="Iniciar Ordenação", command=lambda: start_bubble_sort(canvas), state=tk.NORMAL)
    iniciar_button_bubble.grid(row=1, column=1, padx=5, pady=5)
    prev_button_bubble = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_bubble, state=tk.DISABLED)
    prev_button_bubble.grid(row=2, column=0, padx=5, pady=5)
    next_button_bubble = tk.Button(controls_frame, text="Próximo Passo", command=next_step_bubble, state=tk.DISABLED)
    next_button_bubble.grid(row=2, column=1, padx=5, pady=5)
    history_button_bubble = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_bubble, state=tk.DISABLED)
    history_button_bubble.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_bubble(canvas, num_scale.get())
    current_canvas = canvas
