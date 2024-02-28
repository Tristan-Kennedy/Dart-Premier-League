import tkinter as tk

def add_resizable_window(root):
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)
    
    label = tk.Label(frame, text="Window Size")
    label.pack()
    
    slider = tk.Scale(frame, from_=100, to=1000, orient="horizontal", command=lambda value: on_slider_change(value, root))
    slider.set(400)
    slider.pack()
    
    text = tk.Text(frame, height=5, width=50)
    text.pack()
    text.insert(tk.END, "Resizable window with a slider!\nTry adjusting the slider to resize the window.")
    
    button = tk.Button(frame, text="Click Me!", command=on_button_click)
    button.pack()

def on_slider_change(value, root):
    root.geometry(f"{value}x{value}")

def on_button_click():
    print("Button clicked!")
