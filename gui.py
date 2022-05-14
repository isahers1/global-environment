from tkinter import PhotoImage
from tkinter import *
from tkinter import ttk
from regex import P

from sympy import GoldenRatio
from proof import *
from tkinter.scrolledtext import ScrolledText

G = ''
p = ''

def enter(*args):
    global p
    global G
    input = entry.get()
    input = "p."+input
    print(input)
    exec(input)
    showing.set(p.show())

def generateLaTeX(*args):
    p.writeLaTeXfile()

#G = group('G','*')
#abelianG = forall(['x', 'y'], G, Eq(Mult(['x', 'y']), Mult(['y','x']),G))
#p = Proof('Simple Abelian Proof', forall(['x'], G, Eq(Mult(['x', 'x']), G.elements['e'],G)), goal=abelianG)

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

showProof = ttk.Label(mainframe, background="white", textvariable=showing).grid(column=1, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Enter", command=enter).grid(column=3, row=3, sticky=W)

ttk.Button(mainframe, text="Generate Latex", command=generateLaTeX).grid(column=3, row=4, sticky=W)

goal = StringVar()
name = StringVar()
assum = StringVar()


def new():
    newProof = Toplevel(root)
    newProof.title = "New Proof"
    Label(newProof,
          text ="Proof Name:").pack()
    ttk.Entry(newProof, width=50, textvariable=name).pack()

    Label(newProof,
          text ="Assumptions:").pack()
    ttk.Entry(newProof, width=50, textvariable=assum).pack()

    Label(newProof,
          text ="Goal:").pack()
    ttk.Entry(newProof, width=50, textvariable=goal).pack()

    #p = Proof('Simple Abelian Proof', forall(['x'], G, Eq(Mult(['x', 'x']), G.elements['e'],G)), goal=abelianG)

    Button(newProof,text = "Create Proof", command=lambda: createProof(newProof)).pack()


def createProof(window):
    global G
    global p
    G = group('G','*')
    p=''
    line = f"global p; p = Proof('{name.get()}',{assum.get()},goal={goal.get()})"
    try:
        exec(line)
        showing.set(p.show())
        window.destroy()
    except:
        messagebox.showinfo(title="Error", message="Invalid Entry")

def open():
    return

def save():
    return

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=new)
filemenu.add_command(label="Open", command=open)
filemenu.add_command(label="Save", command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

def commandList():
    return

def about():
    return

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Command List", command=commandList)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

entry_bar.focus()
root.bind("<Return>", enter)

# creating object of ShowPdf from tkPDFViewer.
#v1 = pdf.ShowPdf().pdf_view(mainframe, pdf_location = r"Simple Abelian Proof.pdf").grid(column=1, row=4, sticky=W)
  
  
# Placing Pdf in my gui.
#v2.grid(column=1, row=4, sticky=W)

root.mainloop()