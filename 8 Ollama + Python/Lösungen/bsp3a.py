import tkinter as tk
click_count = 0

def say_hello():
    global click_count
    click_count += 1
    label.config(text=f"Hello, world! (Klick {click_count})")
    if click_count == 1:
        button.config(text="Nochmal klicken")

root = tk.Tk()
root.title("Hello Tkinter")

label = tk.Label(root, text="")
label.pack(pady=10)

button = tk.Button(root, text="Klick mich", command=say_hello)
button.pack(padx=20, pady=10)

root.mainloop()
