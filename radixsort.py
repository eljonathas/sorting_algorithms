import tkinter as tk
import random

steps_radix = []
array_radix = []
current_step_radix = 0
current_canvas = None

def record_step_radix(arr, exp, count_array, output_array, msg):
    steps_radix.append({
        "array": arr.copy(),
        "exp": exp,
        "count": count_array.copy() if count_array is not None else None,
        "output": output_array.copy() if output_array is not None else None,
        "msg": msg
    })

def counting_sort_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    record_step_radix(arr, exp, count, output, f"Iniciando contagem para exp={exp}")
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
        record_step_radix(arr, exp, count, output, f"Contando dígito {index} para arr[{i}]={arr[i]}")
    for i in range(1, 10):
        count[i] += count[i-1]
        record_step_radix(arr, exp, count, output, f"Acumulando count para dígito {i}")
    for i in range(n-1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        record_step_radix(arr, exp, count, output, f"Colocando {arr[i]} na posição {count[index]-1}")
        count[index] -= 1
        record_step_radix(arr, exp, count, output, f"Decrementando count para dígito {index}")
    return output

def radix_sort(arr):
    max_val = max(arr) if arr else 0
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort_radix(arr, exp)
        record_step_radix(arr, exp, [0]*10, arr, f"Passo concluído para exp={exp}")
        exp *= 10
    return arr

def draw_state_radix(canvas, state):
    canvas.delete("all")
    cw = int(canvas['width'])
    ch = int(canvas['height'])
    top_margin = 20
    cell_width = 40
    cell_height = 40
    # Array row
    array_y = top_margin
    arr = state["array"]
    n = len(arr)
    for i in range(n):
        x0 = 20 + i * cell_width
        y0 = array_y
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue")
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(arr[i]), font=("Arial", 12))
    canvas.create_text(20, array_y + cell_height + 5, text="Array", anchor="w", font=("Arial", 10))
    
    # Count row
    if state["count"] is not None:
        count_arr = state["count"]
        count_n = len(count_arr)
        count_cell_width = 30
        count_y = array_y + cell_height + 5 + cell_height + 10
        for i in range(count_n):
            x0 = 20 + i * count_cell_width
            y0 = count_y
            x1 = x0 + count_cell_width
            y1 = y0 + cell_height
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightyellow")
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(count_arr[i]), font=("Arial", 10))
        canvas.create_text(20, count_y + cell_height + 5, text="Count", anchor="w", font=("Arial", 10))
    
    # Output row
    if state["output"] is not None:
        output_arr = state["output"]
        output_y = array_y + cell_height + 5 + cell_height + 10 + cell_height + 10
        for i in range(len(output_arr)):
            x0 = 20 + i * cell_width
            y0 = output_y
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen")
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(output_arr[i]), font=("Arial", 12))
        canvas.create_text(20, output_y + cell_height + 5, text="Output", anchor="w", font=("Arial", 10))
    
    canvas.create_text(cw/2, ch - 30, text=f"Exp = {state['exp']}", font=("Arial", 14), fill="blue")
    canvas.create_text(cw/2, ch - 10, text=state["msg"], font=("Arial", 14), fill="green")

def start_radix_sort(canvas):
    global steps_radix, current_step_radix, array_radix
    steps_radix = []
    sorted_array = radix_sort(array_radix)
    record_step_radix(array_radix, 1, [0]*10, sorted_array, "Ordenação concluída")
    current_step_radix = 0
    draw_state_radix(canvas, steps_radix[current_step_radix])
    next_button_radix.config(state=tk.NORMAL)
    prev_button_radix.config(state=tk.DISABLED)
    history_button_radix.config(state=tk.NORMAL)
    iniciar_button_radix.config(state=tk.DISABLED)

def next_step_radix():
    global current_step_radix
    if current_step_radix < len(steps_radix) - 1:
        current_step_radix += 1
        draw_state_radix(current_canvas, steps_radix[current_step_radix])
    if current_step_radix == len(steps_radix) - 1:
        next_button_radix.config(state=tk.DISABLED)
    if current_step_radix > 0:
        prev_button_radix.config(state=tk.NORMAL)

def prev_step_radix():
    global current_step_radix
    if current_step_radix > 0:
        current_step_radix -= 1
        draw_state_radix(current_canvas, steps_radix[current_step_radix])
    if current_step_radix == 0:
        prev_button_radix.config(state=tk.DISABLED)
    if current_step_radix < len(steps_radix) - 1:
        next_button_radix.config(state=tk.NORMAL)

def show_history_radix():
    history_window = tk.Toplevel()
    history_window.title("Histórico das Instruções - RadixSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_radix):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def generate_new_array_radix(canvas, num):
    global array_radix, steps_radix, current_step_radix
    array_radix = [random.randint(0, 999) for _ in range(num)]
    steps_radix = []
    current_step_radix = 0
    canvas.config(height=250)
    draw_initial_array_radix(canvas)
    iniciar_button_radix.config(state=tk.NORMAL)
    next_button_radix.config(state=tk.DISABLED)
    prev_button_radix.config(state=tk.DISABLED)
    history_button_radix.config(state=tk.DISABLED)

def draw_initial_array_radix(canvas):
    state = {
        "array": array_radix.copy(),
        "exp": 1,
        "count": None,
        "output": None,
        "msg": "Vetor gerado"
    }
    draw_state_radix(canvas, state)

def setup_radixsort_interface(root, canvas, controls_frame, menu_frame, voltar_menu):
    global iniciar_button_radix, next_button_radix, prev_button_radix, history_button_radix, current_canvas
    menu_frame.pack_forget()
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    controls_frame.pack(side=tk.BOTTOM, pady=10)
    for widget in controls_frame.winfo_children():
        widget.destroy()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale = tk.Scale(controls_frame, from_=5, to=30, orient=tk.HORIZONTAL)
    num_scale.set(10)
    num_scale.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=lambda: generate_new_array_radix(canvas, num_scale.get())).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_radix = tk.Button(controls_frame, text="Iniciar Ordenação", command=lambda: start_radix_sort(canvas), state=tk.NORMAL)
    iniciar_button_radix.grid(row=1, column=1, padx=5, pady=5)
    prev_button_radix = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_radix, state=tk.DISABLED)
    prev_button_radix.grid(row=2, column=0, padx=5, pady=5)
    next_button_radix = tk.Button(controls_frame, text="Próximo Passo", command=next_step_radix, state=tk.DISABLED)
    next_button_radix.grid(row=2, column=1, padx=5, pady=5)
    history_button_radix = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_radix, state=tk.DISABLED)
    history_button_radix.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_radix(canvas, num_scale.get())
    current_canvas = canvas
