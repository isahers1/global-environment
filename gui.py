# from tkinter import PhotoImage
# from tkinter import ttk
# from tkinter import *
# from turtle import undo
# from proof import *
# from tkinter.scrolledtext import ScrolledText
# import fitz
# from ttkwidgets.autocomplete import AutocompleteCombobox


# proof_methods = ['MultElem', 'accessAssumption', 'andElim', 'breakPower', 'cancelLeft', 
# 'cancelRight', 'closure', 'combinePower', 'concludeSubproof', 'forAllIntroduction', 'forallElim',
# 'identleft', 'identright', 'impliesIntroduction', 'introAssumption', 'introCases', 'introElement',
# 'introGroup', 'introReflexive', 'introSubproof', 'inverseElimLHS', 'inverseElimRHS', 'leftMult',
# 'leftSidesEq', 'modus', 'notElim', 'qed', 'reduceLogic', 'rightMult', 'rightSidesEq', 'show',
# 'showReturn', 'splitPowerAddition', 'splitPowerMult', 'substituteLHS', 'substituteRHS',
# 'switchSidesOfEqual', 'thereexistsElim', 'undo', 'writeLaTeXfile']

# class PDFViewer(ScrolledText):
#     def show(self, pdf_file):
#         self.delete('1.0', 'end') # clear current content
#         pdf = fitz.open(pdf_file) # open the PDF file
#         self.images = []   # for storing the page images
#         for page in pdf:
#             pix = page.get_pixmap()
#             pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
#             photo = PhotoImage(data=pix1.tobytes('ppm'))
#             # insert into the text box
#             self.image_create('end', image=photo)
#             self.insert('end', '\n')
#             # save the image to avoid garbage collected
#             self.images.append(photo)


# def enter(*args):
#     input = entry.get()
#     input = "p."+input
#     print(input)
#     try:
#         exec(input)
#     except:
#         messagebox.showerror('Syntax Error', 'You have either called a function that does not exist or passed a variable that is not defined - or both!')
#     showing.set(p.showReturn())
#     entry_bar.delete(0,"end")
    

# def generateLaTeX(*args):
#     p.writeLaTeXfile()
#     pdf1.show('Simple Abelian Proof.pdf')

# G = group('G','*')
# abelianG = forall(['x', 'y'], G, Eq(Mult(['x', 'y']), Mult(['y','x']),G))
# p = Proof('Simple Abelian Proof', forall(['x'], G, Eq(Mult(['x', 'x']), G.elements['e'],G)), goal=abelianG)

# root = Tk()
# root.title("Proof-Check")

# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# pdf1 = PDFViewer(mainframe, width=80, height=30, spacing3=5, bg='blue')
# pdf1.grid(row=5, column=1, sticky='nsew')
# pdf1.show('Simple Abelian Proof.pdf')


# def match_string():
#     hits = []
#     got = entry_bar.get()
#     for item in proof_methods:
#         if item.startswith(got):
#             hits.append(item)
#     return hits   

# def match_string_del():
#     hits = []
#     got = entry_bar.get()[:-1]
#     for item in proof_methods:
#         if item.startswith(got):
#             hits.append(item)
#     return hits 

# def check_empty(event):
#     if len(entry_bar.get()) == 1:
#         suggestions.set("") 
#     else:
#         hits = match_string_del()
#         show_hit(hits)

# def get_typed(event):
#     if len(event.keysym) == 1:
#         hits = match_string()
#         show_hit(hits)

# def show_hit(lst):
#     suggestions.set(lst)
#     if len(lst) == 1:
#         entry.set(lst[0])
#         detect_pressed.filled = True
#         entry_bar.icursor(END)

# def detect_pressed(event):    
#     key = event.keysym
#     if len(key) == 1 and detect_pressed.filled is True:
#         pos = entry_bar.index(INSERT)
#         entry_bar.delete(pos, END)

# detect_pressed.filled = False


# entry = StringVar()
# entry_bar = Entry(
#     mainframe, 
#     width = 50,
#     bg='black',
#     insertbackground='white',
#     fg='white',
#     textvariable=entry)
# entry_bar.grid(column=1, row=3, sticky=(W, E))
# entry_bar.focus_set()
# entry_bar.bind('<KeyRelease>', get_typed)
# entry_bar.bind('<Key>', detect_pressed)
# entry_bar.bind('<BackSpace>', check_empty)

# def undo(*args):
#     p.undo()
#     showing.set(p.showReturn())


# #entry_bar = AutocompleteCombobox(mainframe, width=50, textvariable=entry, completevalues = proof_methods)


# showing = StringVar()
# showing.set("Proof : Simple Abelian Proof\n--------------------------------")

# showProof = ttk.Label(mainframe, background="white", textvariable=showing).grid(column=1, row=2, sticky=(W, E))

# ttk.Button(mainframe, text="Enter", command=enter).grid(column=3, row=3, sticky=W)

# ttk.Button(mainframe, text="Undo", command=undo).grid(column=3, row=2, sticky=W)

# ttk.Button(mainframe, text="Generate Latex", command=generateLaTeX).grid(column=3, row=4, sticky=W)

# suggestions = StringVar()
# showSuggestions = ttk.Label(mainframe, width = 50, background="white", textvariable=suggestions).grid(column=1, row=4, sticky=(W, E))

# for child in mainframe.winfo_children(): 
#     child.grid_configure(padx=5, pady=5)

# entry_bar.focus()
# root.bind("<Return>", enter)

# # creating object of ShowPdf from tkPDFViewer.
# #v1 = pdf.ShowPdf().pdf_view(mainframe, pdf_location = r"Simple Abelian Proof.pdf").grid(column=1, row=4, sticky=W)
  
  
# # Placing Pdf in my gui.
# #v2.grid(column=1, row=4, sticky=W)

# root.mainloop()