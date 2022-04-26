from tkinter import PhotoImage
from tkinter import *
from tkinter import ttk
from proof import *
from tkinter.scrolledtext import ScrolledText
import fitz

class PDFViewer(ScrolledText):
    def show(self, pdf_file):
        self.delete('1.0', 'end') # clear current content
        pdf = fitz.open(pdf_file) # open the PDF file
        self.images = []   # for storing the page images
        for page in pdf:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            photo = PhotoImage(data=pix1.tobytes('ppm'))
            # insert into the text box
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            # save the image to avoid garbage collected
            self.images.append(photo)


def enter(*args):
    input = entry.get()
    input = "p."+input
    print(input)
    try:
        exec(input)
    except:
        messagebox.showerror('Syntax Error', 'You have either called a function that does not exist or passed a variable that is not defined - or both!')
    showing.set(p.showReturn())
    entry_bar.delete(0,"end")
    

def generateLaTeX(*args):
    p.writeLaTeXfile()
    pdf1.show('Simple Abelian Proof.pdf')

G = group('G','*')
abelianG = forall(['x', 'y'], G, Eq(Mult(['x', 'y']), Mult(['y','x']),G))
p = Proof('Simple Abelian Proof', forall(['x'], G, Eq(Mult(['x', 'x']), G.elements['e'],G)), goal=abelianG)

root = Tk()
root.title("Proof-Check")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

pdf1 = PDFViewer(mainframe, width=80, height=30, spacing3=5, bg='blue')
pdf1.grid(row=5, column=1, sticky='nsew')
pdf1.show('Simple Abelian Proof.pdf')

entry = StringVar()
entry_bar = ttk.Entry(mainframe, width=50, textvariable=entry)
entry_bar.grid(column=1, row=3, sticky=(W, E))

showing = StringVar()
showing.set("Proof : Simple Abelian Proof\n--------------------------------")

showProof = ttk.Label(mainframe, background="white", textvariable=showing).grid(column=1, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Enter", command=enter).grid(column=3, row=3, sticky=W)

ttk.Button(mainframe, text="Generate Latex", command=generateLaTeX).grid(column=3, row=4, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

entry_bar.focus()
root.bind("<Return>", enter)

# creating object of ShowPdf from tkPDFViewer.
#v1 = pdf.ShowPdf().pdf_view(mainframe, pdf_location = r"Simple Abelian Proof.pdf").grid(column=1, row=4, sticky=W)
  
  
# Placing Pdf in my gui.
#v2.grid(column=1, row=4, sticky=W)

root.mainloop()