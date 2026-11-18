import tkinter as tk

def on_button_click():
      print("button clicked")
      
root = tk.Tk()
root.geometry("1000x500")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

button_img = tk.PhotoImage(file="buttons/Execute.png")
button = tk.Button(canvas, image=button_img, command=on_button_click, borderwidth=0, highlightthickness=0)
button.place(x=150, y=100)

root.mainloop()