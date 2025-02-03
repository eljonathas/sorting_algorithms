import tkinter as tk
import random

steps_cs = []
array_cs = []
current_step_cs = 0
current_canvas = None

def record_step_cs(input_array, count_array, output_array, msg):
    steps_cs.append({
       "input": input_array.copy(),
       "count": count_array.copy() if count_array is not None else None,
       "output": output_array.copy() if output_array is not None else None,
       "msg": msg
    })

def counting_sort_algorithm(arr):
    max_val = max(arr) if arr else 0
    count = [0] * (max_val + 1)
    output = [0] * len(arr)
    record_step_cs(arr, count, output, "Inicializando contagem (count array zerado)")
    for num in arr:
        count[num] += 1
        record_step_cs(arr, count, output, f"Contando: incrementa count[{num}]")
    for i in range(1, len(count)):
        count[i] += count[i-1]
        record_step_cs(arr, count, output, f"Acumulando: count[{i}] = count[{i}] + count[{i-1}]")
    for num in reversed(arr):
        output[count[num] - 1] = num
        record_step_cs(arr, count, output, f"Colocando {num} na posição {count[num]-1} do output")
        count[num] -= 1
        record_step_cs(arr, count, output, f"Decrementando count[{num}]")
    return output

def draw_state_cs(canvas, state):
    canvas.delete("all")
    cw = int(canvas['width'])
    ch = int(canvas['height'])
    input_arr = state["input"]
    count_arr = state["count"]
    output_arr = state["output"]
    msg = state["msg"]
    
    n = len(input_arr)
    cell_width = min(60, (cw - 40) / n) if n > 0 else 50
    cell_height = 40
    top_margin = 20
    label_gap = 8      # Label is drawn 8px below the cell
    row_gap = 16       # Gap between rows
    
    # Draw Input row
    input_y = top_margin
    for i in range(n):
        x0 = 20 + i * cell_width
        y0 = input_y
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue")
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(input_arr[i]), font=("Arial", 14))
    canvas.create_text(20, input_y + cell_height + label_gap, text="Input", anchor="w", font=("Arial", 12))
    
    current_y = input_y + cell_height + label_gap + row_gap
    
    # Draw Count row if available
    if count_arr is not None:
        count_n = len(count_arr)
        count_cell_width = min(40, (cw - 40) / count_n) if count_n > 0 else 40
        count_y = current_y
        for i in range(count_n):
            x0 = 20 + i * count_cell_width
            y0 = count_y
            x1 = x0 + count_cell_width
            y1 = y0 + cell_height
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightyellow")
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(count_arr[i]), font=("Arial", 12))
        canvas.create_text(20, count_y + cell_height + label_gap, text="Count", anchor="w", font=("Arial", 12))
        current_y = count_y + cell_height + label_gap + row_gap

    # Draw Output row if available
    if output_arr is not None:
        output_y = current_y
        for i in range(len(output_arr)):
            x0 = 20 + i * cell_width
            y0 = output_y
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen")
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(output_arr[i]), font=("Arial", 14))
        canvas.create_text(20, output_y + cell_height + label_gap, text="Output", anchor="w", font=("Arial", 12))
    
    canvas.create_text(cw/2, ch - 20, text=msg, font=("Arial", 14), fill="green")

def start_counting_sort(canvas):
    global steps_cs, current_step_cs, array_cs
    steps_cs = []
    sorted_array = counting_sort_algorithm(array_cs)
    record_step_cs(array_cs, [0]*len(sorted_array), sorted_array, "Ordenação concluída")
    current_step_cs = 0
    draw_state_cs(canvas, steps_cs[current_step_cs])
    next_button_cs.config(state=tk.NORMAL)
    prev_button_cs.config(state=tk.DISABLED)
    history_button_cs.config(state=tk.NORMAL)
    iniciar_button_cs.config(state=tk.DISABLED)

def next_step_cs():
    global current_step_cs
    if current_step_cs < len(steps_cs) - 1:
        current_step_cs += 1
        draw_state_cs(current_canvas, steps_cs[current_step_cs])
    if current_step_cs == len(steps_cs) - 1:
        next_button_cs.config(state=tk.DISABLED)
    if current_step_cs > 0:
        prev_button_cs.config(state=tk.NORMAL)

def prev_step_cs():
    global current_step_cs
    if current_step_cs > 0:
        current_step_cs -= 1
        draw_state_cs(current_canvas, steps_cs[current_step_cs])
    if current_step_cs == 0:
        prev_button_cs.config(state=tk.DISABLED)
    if current_step_cs < len(steps_cs) - 1:
        next_button_cs.config(state=tk.NORMAL)

def show_history_cs():
    history_window = tk.Toplevel()
    history_window.title("Histórico das Instruções - CountingSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_cs):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def generate_new_array_cs(canvas, num):
    global array_cs, steps_cs, current_step_cs
    array_cs = [random.randint(0, 20) for _ in range(num)]
    steps_cs = []
    current_step_cs = 0
    canvas.config(height=300)
    draw_initial_array_cs(canvas)
    iniciar_button_cs.config(state=tk.NORMAL)
    next_button_cs.config(state=tk.DISABLED)
    prev_button_cs.config(state=tk.DISABLED)
    history_button_cs.config(state=tk.DISABLED)

def draw_initial_array_cs(canvas):
    state = {
        "input": array_cs.copy(),
        "count": None,
        "output": None,
        "msg": "Vetor gerado"
    }
    draw_state_cs(canvas, state)

def setup_countingsort_interface(root, canvas, controls_frame, menu_frame, voltar_menu):
    global iniciar_button_cs, next_button_cs, prev_button_cs, history_button_cs, current_canvas
    menu_frame.pack_forget()
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    controls_frame.pack(side=tk.BOTTOM, pady=10)
    for widget in controls_frame.winfo_children():
        widget.destroy()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale = tk.Scale(controls_frame, from_=5, to=30, orient=tk.HORIZONTAL)
    num_scale.set(10)
    num_scale.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=lambda: generate_new_array_cs(canvas, num_scale.get())).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_cs = tk.Button(controls_frame, text="Iniciar Ordenação", command=lambda: start_counting_sort(canvas), state=tk.NORMAL)
    iniciar_button_cs.grid(row=1, column=1, padx=5, pady=5)
    prev_button_cs = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_cs, state=tk.DISABLED)
    prev_button_cs.grid(row=2, column=0, padx=5, pady=5)
    next_button_cs = tk.Button(controls_frame, text="Próximo Passo", command=next_step_cs, state=tk.DISABLED)
    next_button_cs.grid(row=2, column=1, padx=5, pady=5)
    history_button_cs = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_cs, state=tk.DISABLED)
    history_button_cs.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_cs(canvas, num_scale.get())
    current_canvas = canvas
