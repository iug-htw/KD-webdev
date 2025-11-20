import tkinter as tk

def say_hello():
    label.config(text="Hello, world!")

root = tk.Tk()
root.title("Hello Tkinter")

label = tk.Label(root, text="")
label.pack(pady=10)

button = tk.Button(root, text="Klick mich", command=say_hello)
button.pack(padx=20, pady=10)

root.mainloop()
