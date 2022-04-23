from tkinter import *
from tkinter import ttk
from proof import *

def enter(*args):
    input = entry.get()
    input = "p."+input
    print(input)
    exec(input)
    showing.set(p.show())

G = group('G','*')
abelianG = forall(['x', 'y'], G, Eq(Mult(['x', 'y']), Mult(['y','x']),G))
p = Proof('Simple Abelian Proof', forall(['x'], G, Eq(Mult(['x', 'x']), G.elements['e'],G)), goal=abelianG)

root = Tk()
root.title("Proof-Check")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

entry = StringVar()
entry_bar = ttk.Entry(mainframe, width=50, textvariable=entry)
entry_bar.grid(column=1, row=3, sticky=(W, E))

showing = StringVar()
showing.set("Proof : Simple Abelian Proof\n--------------------------------")

showProof = ttk.Label(mainframe, background="white", textvariable=showing).grid(column=1, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Enter", command=enter).grid(column=3, row=3, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

entry_bar.focus()
root.bind("<Return>", enter)

root.mainloop()