import tkinter as tk
import random

steps_bucket = []
array_bucket = []
current_step_bucket = 0
current_canvas = None

def record_step_bucket(input_arr, buckets, output, msg):
    steps_bucket.append({
       "input": input_arr.copy(),
       "buckets": [b.copy() for b in buckets] if buckets is not None else None,
       "output": output.copy() if output is not None else None,
       "msg": msg
    })

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def bucket_sort(arr, bucket_count=10):
    if not arr:
        return arr
    min_val = min(arr)
    max_val = max(arr)
    buckets = [[] for _ in range(bucket_count)]
    record_step_bucket(arr, buckets, [], "Buckets criados vazios")
    for num in arr:
        index = int((num - min_val) / (max_val - min_val + 1) * bucket_count)
        if index >= bucket_count:
            index = bucket_count - 1
        buckets[index].append(num)
        record_step_bucket(arr, buckets, [], f"Adicionando {num} no bucket {index}")
    for i in range(bucket_count):
        buckets[i] = insertion_sort(buckets[i])
        record_step_bucket(arr, buckets, [], f"Bucket {i} ordenado")
    output = []
    for b in buckets:
        output.extend(b)
    record_step_bucket(arr, buckets, output, "Buckets concatenados")
    return output

def draw_state_bucket(canvas, state):
    canvas.delete("all")
    cw = int(canvas['width'])
    ch = int(canvas['height'])
    top_margin = 20
    cell_width = 40
    cell_height = 40
    
    # Draw Input row
    input_arr = state["input"]
    input_y = top_margin
    for i in range(len(input_arr)):
        x0 = 20 + i * cell_width
        y0 = input_y
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue")
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(input_arr[i]), font=("Arial", 12))
    canvas.create_text(20, input_y + cell_height + 5, text="Input", anchor="w", font=("Arial", 10))
    
    # Draw Buckets row
    if state["buckets"] is not None:
        buckets = state["buckets"]
        bucket_count = len(buckets)
        bucket_width = (cw - 40) / bucket_count
        buckets_y = input_y + cell_height + 5 + 60  # extra vertical spacing
        for i in range(bucket_count):
            x0 = 20 + i * bucket_width
            y0 = buckets_y
            x1 = x0 + bucket_width - 5
            y1 = y0 + 150
            canvas.create_rectangle(x0, y0, x1, y1, outline="black")
            for j, val in enumerate(buckets[i]):
                bx0 = x0 + 5
                by0 = y0 + j * (cell_height/2 + 5)
                bx1 = bx0 + bucket_width - 15
                by1 = by0 + cell_height/2
                canvas.create_rectangle(bx0, by0, bx1, by1, fill="lightyellow")
                canvas.create_text((bx0+bx1)/2, (by0+by1)/2, text=str(val), font=("Arial", 10))
            canvas.create_text(x0 + 5, y0 + 155, text=f"B{i}", anchor="w", font=("Arial", 10))
    
    # Draw Output row
    if state["output"] is not None and len(state["output"]) > 0:
        output_arr = state["output"]
        output_y = (input_y + cell_height + 5 + 60 + 150 + 10)
        for i in range(len(output_arr)):
            x0 = 20 + i * cell_width
            y0 = output_y
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen")
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(output_arr[i]), font=("Arial", 12))
        canvas.create_text(20, output_y + cell_height + 5, text="Output", anchor="w", font=("Arial", 10))
    
    canvas.create_text(cw/2, ch - 20, text=state["msg"], font=("Arial", 14), fill="green")

def start_bucket_sort(canvas):
    global steps_bucket, current_step_bucket, array_bucket
    steps_bucket = []
    sorted_array = bucket_sort(array_bucket)
    record_step_bucket(array_bucket, [[] for _ in range(10)], sorted_array, "Ordenação concluída")
    current_step_bucket = 0
    draw_state_bucket(canvas, steps_bucket[current_step_bucket])
    next_button_bucket.config(state=tk.NORMAL)
    prev_button_bucket.config(state=tk.DISABLED)
    history_button_bucket.config(state=tk.NORMAL)
    iniciar_button_bucket.config(state=tk.DISABLED)

def next_step_bucket():
    global current_step_bucket
    if current_step_bucket < len(steps_bucket) - 1:
        current_step_bucket += 1
        draw_state_bucket(current_canvas, steps_bucket[current_step_bucket])
    if current_step_bucket == len(steps_bucket) - 1:
        next_button_bucket.config(state=tk.DISABLED)
    if current_step_bucket > 0:
        prev_button_bucket.config(state=tk.NORMAL)

def prev_step_bucket():
    global current_step_bucket
    if current_step_bucket > 0:
        current_step_bucket -= 1
        draw_state_bucket(current_canvas, steps_bucket[current_step_bucket])
    if current_step_bucket == 0:
        prev_button_bucket.config(state=tk.DISABLED)
    if current_step_bucket < len(steps_bucket) - 1:
        next_button_bucket.config(state=tk.NORMAL)

def show_history_bucket():
    history_window = tk.Toplevel()
    history_window.title("Histórico das Instruções - BucketSort")
    text_widget = tk.Text(history_window, width=100, height=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(history_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    for index, step in enumerate(steps_bucket):
        text_widget.insert(tk.END, f"Passo {index}: {step['msg']}\n")
    text_widget.config(state=tk.DISABLED)

def generate_new_array_bucket(canvas, num):
    global array_bucket, steps_bucket, current_step_bucket
    array_bucket = [random.randint(0, 100) for _ in range(num)]
    steps_bucket = []
    current_step_bucket = 0
    canvas.config(height=500)
    draw_initial_array_bucket(canvas)
    iniciar_button_bucket.config(state=tk.NORMAL)
    next_button_bucket.config(state=tk.DISABLED)
    prev_button_bucket.config(state=tk.DISABLED)
    history_button_bucket.config(state=tk.DISABLED)

def draw_initial_array_bucket(canvas):
    state = {
        "input": array_bucket.copy(),
        "buckets": None,
        "output": None,
        "msg": "Vetor gerado"
    }
    draw_state_bucket(canvas, state)

def setup_bucketsort_interface(root, canvas, controls_frame, menu_frame, voltar_menu):
    global iniciar_button_bucket, next_button_bucket, prev_button_bucket, history_button_bucket, current_canvas
    menu_frame.pack_forget()
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    controls_frame.pack(side=tk.BOTTOM, pady=10)
    for widget in controls_frame.winfo_children():
        widget.destroy()
    tk.Label(controls_frame, text="Quantidade de Números:").grid(row=0, column=0, padx=5)
    num_scale = tk.Scale(controls_frame, from_=5, to=30, orient=tk.HORIZONTAL)
    num_scale.set(10)
    num_scale.grid(row=0, column=1, padx=5)
    tk.Button(controls_frame, text="Gerar Novo Vetor", command=lambda: generate_new_array_bucket(canvas, num_scale.get())).grid(row=1, column=0, padx=5, pady=5)
    iniciar_button_bucket = tk.Button(controls_frame, text="Iniciar Ordenação", command=lambda: start_bucket_sort(canvas), state=tk.NORMAL)
    iniciar_button_bucket.grid(row=1, column=1, padx=5, pady=5)
    prev_button_bucket = tk.Button(controls_frame, text="Passo Anterior", command=prev_step_bucket, state=tk.DISABLED)
    prev_button_bucket.grid(row=2, column=0, padx=5, pady=5)
    next_button_bucket = tk.Button(controls_frame, text="Próximo Passo", command=next_step_bucket, state=tk.DISABLED)
    next_button_bucket.grid(row=2, column=1, padx=5, pady=5)
    history_button_bucket = tk.Button(controls_frame, text="Mostrar Histórico", command=show_history_bucket, state=tk.DISABLED)
    history_button_bucket.grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(controls_frame, text="Voltar ao Menu", command=voltar_menu).grid(row=4, column=0, columnspan=2, pady=5)
    generate_new_array_bucket(canvas, num_scale.get())
    current_canvas = canvas
