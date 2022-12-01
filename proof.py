import os, sys
from email import message
from re import L

from element import *
from group import *
from integer import *
from logicObjects import *
from tkinter import messagebox
from pylatex import Document, Section, Subsection, Command, Enumerate
from pylatex.utils import italic, NoEscape

class Proof:
    def __init__(self, label, assumption, goal=None, steps=[], justifications = [], depth=0, linestart=0): # make goal optional
        self.linestart = linestart
        self.label = label
        self.depth = depth
        self.assumption = assumption
        self.goal = goal # this is an implies
        self.steps = steps
        self.justifications = justifications
        self.env = {}
        self.subproof = None
    
    def qed(self, lineNum):
        if self.goal == self.steps[lineNum]:
            self.steps+=["."]
            self.justifications += ["QED"]
            self.show()
        else:
            print("This is not the same as the goal")

    def undo(self):
        self.steps = self.steps[:-1]
        self.justifications = self.justifications[:-1]
        self.show()
    
    def writeLaTeXfile(self):
        doc = Document(page_numbers=False)
        doc.preamble.append(Command('title', self.label))
        doc.append(NoEscape(r'\maketitle'))
        doc.append(italic("Proof:"))
        with doc.create(Enumerate()) as enum:
            doc.append(NoEscape(r"\addtocounter{enumi}{-1}"))
            for i in range(len(self.steps)):
                if isinstance(self.steps[i],str):
                    enum.add_item(NoEscape(self.steps[i]+r"\hfill"))
                else:
                    enum.add_item(NoEscape("$"+self.steps[i].toLaTeX()+r"$\hfill"))
                enum.append(" by " + str(self.justifications[i]))
        doc.generate_tex(self.label)
        doc.generate_pdf(self.label)

    def showReturn(self):
        showstr = ""
        if self.depth==0:
            showstr += 'Proof : '
            showstr += self.label
            showstr += '\n'
            showstr += '--------------------------------'
            showstr += '\n'
        else:
            showstr += 'Subproof : assume '
            showstr += str(self.assumption)
            showstr += '\n'
            showstr += '--------------------------------'
            showstr += '\n'
        i = self.linestart
        while i < len(self.steps):
            if isinstance(self.steps[i],Proof):
                showstr += self.steps[i].show()
                i+=len(self.steps[i].steps)-self.steps[i].linestart-1
            else:
                linestr = "\t"*self.depth + str(i) + ': ' + str(self.steps[i]) + '\t' + str(self.justifications[i]) + '\n'
                showstr += linestr
            i+=1 
        return showstr

    def show(self):
        if self.depth==0:
            print('')
            print('Proof : ' + self.label)
            print('--------------------------------')
        else:
            print('Subproof : assume ' + str(self.assumption))
            print('--------------------------------')
        i = self.linestart
        while i < len(self.steps):
            if isinstance(self.steps[i],Proof):
                self.steps[i].show()
                i+=len(self.steps[i].steps)-self.steps[i].linestart-1
            else:
                print("\t"*self.depth + str(i) + ': ' + str(self.steps[i]) + '\t' + str(self.justifications[i]))
            i+=1

    def introAssumption(self, expr):
        self.steps += [expr]
        self.justifications += ['introAssumption'] 
        self.show()
    
    def introGroup(self, groupName):
        self.steps += [group(groupName)]
        self.justifications += ["introGroup"]
        self.show()

    def introGroup(self, grp):
        self.steps += [grp]
        self.justifications += ["introGroup"]
        #deal with environments
        self.env[grp.groupName] = grp
        self.show()
    
    def introSet(self, setName, grp, property):
        if 'sets' not in self.env:
            self.env['sets'] = [setName]
            self.env['setProperty'] = {setName:[grp,property]}
            self.env['setElements'] = {setName:[]}
            self.steps += [f'{setName} with property {property}']
            self.justifications += [f'Introduced set {setName} in {grp}']
            self.show()
        else:
            if setName in self.env['sets']:
                messagebox.showerror("A set with this name already exists, maybe try another name?")
            else:
                self.env['sets'].append(setName)
                self.env['setProperty'][setName] = [grp,property]
                self.env['setElements'][setName] = []
                self.steps += [setName]
                self.justifications += [f'Introduced set {setName} in {grp}']
                self.show()
    
    def addElemToSet(self, setName, elementName, grp):
        """"
        Given a set, and a grp it belongs to, introduce element from that group into the set
        :param setName: name of set to take add element to
        :param elementName: name of the element
        :param grp: grp that contains the element
        """
        print(grp.elements)
        if 'sets' in self.env:
            if setName in self.env['sets']:
                if elementName not in self.env['setElements'][setName]:
                    if grp.contains(elementName):
                        if isinstance(self.env['setProperty'][setName][1],In):
                            if self.env['setProperty'][setName][0] == grp:
                                elemDeclaration = In(elementName, grp)
                                self.env['setElements'][setName].append(elementName)
                                self.steps += [elemDeclaration]
                                self.justifications += [f'Added element {elementName} to set {setName}']
                                self.show()
                            else:
                                messagebox.showerror('Proof Error', f'Set {setName} is in a different group than {grp}')
                    else:
                        messagebox.showerror('Proof Error', f"{elementName} is not in {grp}")
                else:
                    messagebox.showerror("You have already defined an element in this set with that name, maybe try another name?")
            else:
                messagebox.showerror("You haven't defined a set with that name yet!")
        else:
            messagebox.showerror("You haven't defined any sets yet!")


    def getArbElem(self, setName, elementName):
        """"
        Given a set, select an arbitrary element and put it on it's own line
        :param setName: name of set to take element from
        :param elementName: name of the arbitrary element
        """
        if 'sets' in self.env:
            if setName in self.env['sets']:
                if elementName not in self.env['setElements'][setName]:
                    pg = self.env['setProperty'][setName][0]
                    if not pg.contains(elementName):
                        self.env[elementName] = pg.newElement(elementName)
                        self.env['setElements'][setName].append(elementName)
                        if isinstance(self.env['setProperty'][setName][1],In):
                            elemDeclaration = In(elementName, pg)
                        elif isinstance(self.env['setProperty'][setName][1],Eq):
                            elemDeclaration = Eq(elementName,self.env['setProperty'][setName][1].RHS,pg)
                        self.steps += [elemDeclaration]
                        self.justifications += [f'Introduced arbitrary element {elementName} in set {setName}']
                        self.show()
                    else:
                        messagebox.showerror('Proof Error', f"{elementName} is already in {pg}")
                else:
                    messagebox.showerror("You have already defined an element in this set with that name, maybe try another name?")
            else:
                messagebox.showerror("You haven't defined a set with that name yet!")
        else:
            messagebox.showerror("You haven't defined any sets yet!")
    
    def getSpecificElem(self, setName, elementName):
        """"
        Given a set, select an specific element and put it on it's own line
        :param setName: name of set to take element from
        :param elementName: name of the specific element
        """
        if 'sets' in self.env:
            if setName in self.env['sets']:
                if elementName not in self.env['setElements'][setName]:
                    pg = self.env['setProperty'][setName][0]
                    if pg.contains(elementName):
                        self.env['setElements'][setName].append(elementName)
                        self.steps += [Eq(elementName,pg.elements[elementName],pg)]
                        self.justifications += [f'Introduced element {elementName} in set {setName}']
                        self.show()
                    else:
                        messagebox.showerror('Proof Error', f"{elementName} is not in {pg}")
                else:
                    messagebox.showerror("You have already defined an element in this set with that name, maybe try another name?")
            else:
                messagebox.showerror("You haven't defined a set with that name yet!")
        else:
            messagebox.showerror("You haven't defined any sets yet!")
    
    def multBothSides(self, lineNum1, lineNum2):
        """
        Given two lines multiply the left hand sides together and the right hand sides together
        :param lineNum1: Line to substitute into
        :param lineNum2: Line with substitutsion of x = y, will replace all instances of x with y in lineNum1
        """
        ev1 = self.steps[lineNum1]
        ev2 = self.steps[lineNum2]
        if isinstance(ev1, Eq):
            if isinstance(ev2, Eq) and ev1.group == ev2.group:
                LHSproduct = self.MultElem(ev1.LHS, ev2.LHS)
                RHSproduct = self.MultElem(ev1.RHS, ev2.RHS)
                result = Eq(LHSproduct, RHSproduct, ev1.group)
                self.steps += [result]
                self.justifications += [f'Multiplied line {lineNum1} by line {lineNum2}'] 
                self.show()
            else:
                messagebox.showerror('Proof Error',f"The statement on line {lineNum2} is not an equality, multiplication is not possible")
        else:
            messagebox.showerror('Proof Error',f"The statement on line {lineNum1} is not an equality, multiplication is not possible")

    def setClosure(self, setName, arbIntros, closure):
        """
        Given a set, two arbitrary elements, and their multiplication, confirm that the set is closed
        :param setName: Name of set we are trying to prove closure for
        :param arbIntros: List of lineNums which contain the arbitrary element intros.
        :param closure: Line where multiplication of arbitrary elements is on LHS and RHS is an element of set
        """
        ev = self.steps[closure]
        if setName in self.env['sets']:
            if len(arbIntros) == 2:
                arb1 = self.steps[arbIntros[0]]
                arb2 = self.steps[arbIntros[1]]
                if isinstance(ev, Eq):
                    # check that lines are intros?
                    if arb1.LHS in self.env['setElements'][setName] and arb2.LHS in self.env['setElements'][setName]:
                        if isinstance(self.env['setProperty'][setName][1],Eq): 
                            if len(ev.LHS.products) == 2 and arb1.LHS in ev.LHS.products and arb2.LHS in ev.LHS.products:
                                self.env['setProperty'][setName].append('Closure')
                                self.steps += [f'Set {setName} is closed']
                                self.justifications += [f'Introduction on lines {arbIntros[0]},{arbIntros[1]} and closure on line {closure}'] 
                                self.show()
                            else:
                                messagebox.showerror('Proof error',f'These lines do not prove closure, double check you typed everythin in correctly')
                elif isinstance(ev,In):
                    if isinstance(self.env['setProperty'][setName][1],In): 
                        if len(ev.elem.products) == 2 and arb1.elem in ev.elem.products and arb2.elem in ev.elem.products and ev.group == arb1.group and ev.group == arb2.group:
                            self.env['setProperty'][setName].append('Closure')
                            self.steps += [f'Set {setName} is closed']
                            self.justifications += [f'Introduction on lines {arbIntros[0]},{arbIntros[1]} and closure on line {closure}'] 
                            self.show()
                        else:
                            messagebox.showerror('Proof error',f'These lines do not prove closure, double check you typed everythin in correctly')
                else:
                    messagebox.showerror('Proof error',f'Line proving closure must be an equation of the form a*b=c where a,b are arbitrary elements of set {setName} and c is in set {setName}')
            else:
                messagebox.showerror('Proof error',f"To prove closure you need 2 arbitrary elements, but you did not pass 2 line numbers")
        else:
            messagebox.showerror('Proof error',f'Set {setName} does not exist, did you type the name wrong?')
    
    def setContainsIdentity(self, setName, lineNum):
        """
        Given a set, verify there exists an element equal to the identity
        :param setName: Name of set we are trying to show contains the identity
        :param lineNum: Line whith left hand side equal to element in set, right hand side is identity
        """
        ev = self.steps[lineNum]
        if setName in self.env['sets']:
            if isinstance(ev, Eq):
                if ev.LHS in self.env['setElements'][setName]:
                    if self.env['setProperty'][setName][0].elements['e'] == ev.RHS:
                        self.env['setProperty'][setName].append('Identity')
                        self.steps += [f'Set {setName} contains the identity']
                        self.justifications += [f'Identity equal to element of set {setName} on line {lineNum}'] 
                        self.show()
                    else:
                        messagebox.showerror('Proof error', f'Right hand side of line {lineNum} is not the identity')
                else:
                    messagebox.showerror('Proof error', f'Left hand side of line {lineNum} is not element of set {setName}')
            else:
                messagebox.showerror('Proof error',f'Line proving identity is in set must be an equation')
        else:
            messagebox.showerror('Proof error',f'Set {setName} does not exist, did you type the name wrong?')

    def setInverse(self, setName, lineNum):
        """
        Given a set, verify that inverse exists for arbitrary element
        :param setName: Name of set we are trying to show contains inverses
        :param lineNum: Line whith left hand side equal to two elements in set multiplied, right hand side is identity
        """
        ev = self.steps[lineNum]
        if setName in self.env['sets']:
            if isinstance(ev, Eq):
                if len(ev.LHS.products) == 2:
                    el1 = ev.LHS.products[0]
                    el2 = ev.LHS.products[1]
                    if str(el1) in self.env['setElements'][setName] and str(el2) in self.env['setElements'][setName]:
                        print(type(ev.RHS), type(self.env['setProperty'][setName][0].elements['e']))
                        if self.env['setProperty'][setName][0].elements['e'] == ev.RHS:
                            self.env['setProperty'][setName].append('Inverses')
                            self.steps += [f'Set {setName} contains inverses']
                            self.justifications += [f'Identity equal to product of two elements of {setName} on line {lineNum}'] 
                            self.show()
                        else:
                            messagebox.showerror('Proof error', f'Right hand side of line {lineNum} is not the identity')
                    else:
                        messagebox.showerror('Proof error', f'One or more elements of left hand side of line {lineNum} is not element of set {setName}')
                else:
                    messagebox.showerror('Proof error',f'Line {lineNum} does not contain two elements on the right hand side')
            else:
                messagebox.showerror('Proof error',f'Line proving identity is in set must be an equation')
        else:
            messagebox.showerror('Proof error',f'Set {setName} does not exist, did you type the name wrong?')
    
    def concludeSubgroup(self, setName):
        """
        Given a set, verify that it is a subgroup
        :param setName: Name of set we are trying to show contains inverses
        """
        if setName in self.env['sets']:
            if 'Closure' in self.env['setProperty'][setName][2:] and 'Identity' in self.env['setProperty'][setName][2:] and 'Inverses' in self.env['setProperty'][setName][2:]:
                pg = self.env['setProperty'][setName][0]
                self.steps += [pg.subGroup(self.env['setProperty'][setName][1])]
                self.justifications += [f'Set {setName} meets all requirements to be a subgroup'] 
                self.show()
            else:
                messagebox.showerror('Proof error',f'Set {setName} does not contain all of the requisites for subgroup (Closure,Identity,Inverses)')
        else:
            messagebox.showerror('Proof error',f'Set {setName} does not exist, did you type the name wrong?')

    def accessAssumption(self):
        self.steps += [self.assumption]
        self.justifications += ["Accessed Assumption"]
        self.show()

    def MultElem(self, e1, e2):
        element1 = copy.deepcopy(e1)
        element2 = copy.deepcopy(e2)
        l=[]
        if isinstance(element1,Mult) and isinstance(element2, Mult):
            l=element1.products+element2.products
        elif isinstance(element1,Mult) and isinstance(element2, Mult) == False:
            l= element1.products
            l.append(element2)
        elif isinstance(element1,Mult)==False and isinstance(element2, Mult):
            l = element2.products
            l.insert(0, element1)
        else:
            l.append(element1)
            l.append(element2)
        return Mult(l)

    def introInverse(self, G, name):
        if isinstance(name,str):
            if not G.contains(name):
                print('Proof Error', f"{name} is not defined")
                return
        else:
            for x in name.products:
                if not G.contains(x):
                   print('Proof Error', f"{x} is not defined")
                   return
        if isinstance(name,str):
            lhs = self.MultElem(inverse(name,G),G.elements[name])    
        else:
            name_ = Mult([G.elements[x] for x in name.products])
            lhs = self.MultElem(inverse(name_,G),name_)
        G.newInverse(name)
        rhs = G.elements["e"]
        self.steps += [Eq(lhs,rhs,G)]
        self.justifications += ["Introducing the inverse of an element"]
        self.show()

    def substituteRHS(self, lineNum1, lineNum2):
        """
        Given a representation of a mult object, replace all instances of it in one equation
        :param lineNum1: Line to substitute into
        :param lineNum2: Line with substitutsion of x = y, will replace all instances of x with y in lineNum1
        """
        ev1 = self.steps[lineNum1]
        ev2 = self.steps[lineNum2]
        if isinstance(ev1, Eq):
            if isinstance(ev2, Eq):
                replacement = ev1.replace(ev2.LHS,ev2.RHS)
                self.steps += [replacement]
                self.justifications += [f'Replaced all instances of {ev2.LHS} with {ev2.RHS} on line {lineNum1}']
                self.show()
            else:
                print('Proof Error',f"The statement on line {lineNum2} is not an equality, substitutition is not possible")
        else:
            print('Proof Error',f"The statement on line {lineNum1} is not an equality, substitutition is not possible")

    def substituteLHS(self, lineNum1, lineNum2):
        """
        Given a representation of a mult object, replace all instances of it in one equation
        :param lineNum1: Line to substitute into
        :param lineNum2: Line with substitutsion of y = x, will replace all instances of y with x in lineNum1
        """
        ev1 = self.steps[lineNum1]
        ev2 = self.steps[lineNum2]
        if isinstance(ev1, Eq):
            if isinstance(ev2, Eq):
                replacement = ev1.replace(ev2.RHS,ev2.LHS)
                self.steps += [replacement]
                self.justifications += [f'Replaced all instances of {ev2.RHS} with {ev2.LHS} on line {lineNum1}']
                self.show()
            else:
                print('Proof Error',f"The statement on line {lineNum2} is not an equality, substitutition is not possible")
        else:
            print('Proof Error',f"The statement on line {lineNum1} is not an equality, substitutition is not possible")
    
    def modus(self, lineNum1, lineNums): # lineNums because multiple assumptions may be neccessary (I think)
        """
        modus pones: given A->B and A, the function concludes B and add it as a new line in the proof
        :param lineNum1 and lineNum2: one line in the proof where the person showed A->B and one line the proof where the person showed A
        """
        ev1 = self.steps[lineNum1]
        if isinstance(lineNums, list):
            ev2 = []
            for line in lineNums:
                ev2 += self.steps[line]
            if isinstance(ev1, Implies): 
                A = ev1.assum
                B = ev1.conc
                if A == ev2: 
                    self.steps += [B]
                    self.justifications += [f'Modus Ponens on {str(lineNum1)}, {str(lineNums)}'] 
                    self.show() 
            else:
                print('Proof Error',f"Line {str(lineNum1)} is not an implies statement")
        else:
            print('Proof Error',"The second argument should be a list, maybe you only have one assumption - make sure to put it into a singleton list")

    def inverseElimRHS(self,lineNum):
        """
        finds the first pair of group element and its inverse and returns the group element
        :param lineNum: the line of the proof to be modified on the right hand side
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence,Eq): 
            l = evidence.RHS.products.copy()
            lawApplied = False
            for i in range(len(l)-1):
                if isinstance(l[i],element) and isinstance(l[i+1],inverse) and (l[i].elementName == l[i+1].elementName):
                    group = l[i].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.identity_identifier
                    newProducts = Mult(l[:i+1]+l[i+2:])
                    lawApplied=True
                    break
                elif isinstance(l[i],inverse) and isinstance(l[i+1],element) and (l[i].elementName == l[i+1].elementName):
                    group = l[i+1].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.identity_identifier
                    newProducts = Mult(l[:i+1]+l[i+2:]) # should we include 'e' in the Mult object?
                    lawApplied=True
                    break
            if lawApplied==False:
                print('Proof Error',f"Inverse laws can't be applied on line {lineNum}")
            else:
                self.steps += [newProducts]
                self.justifications += [f'Right hand side inverse elimination on line {lineNum}'] 
                self.show()
        else:
            print('Proof Error',f"It doesn't seem like line {lineNum} contains an equation")
        

    def inverseElimLHS(self,lineNum):
        """
        finds the first pair of group element and its inverse and returns the group element
        :param lineNum: the line of the proof to be modified on the left hand side
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence,Eq): 
            l = evidence.LHS.products.copy()
            lawApplied = False
            for i in range(len(l)-1):
                if isinstance(l[i],element) and isinstance(l[i+1],inverse) and (l[i].elementName == l[i+1].elementName):
                    group = l[i].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.elements[group.identity_identifier]
                    newProducts = Mult(l[:i+1]+l[i+2:])
                    lawApplied=True
                    break
                elif isinstance(l[i],inverse) and isinstance(l[i+1],element) and (l[i].elementName == l[i+1].elementName):
                    group = l[i+1].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.elements[group.identity_identifier]
                    newProducts = Mult(l[:i+1]+l[i+2:]) # should we include 'e' in the Mult object?
                    lawApplied=True
                    break
            if lawApplied==False:
                print('Proof Error',f"Inverse laws can't be applied on line {lineNum}")
            else:
                self.steps += [Eq(newProducts,evidence.RHS,evidence.group)]
                self.justifications += [f'Left hand side inverse elimination on line {lineNum}'] 
                self.show()
        else:
            print('Proof Error',f"It doesn't seem like line {lineNum} contains an equation")
    
    ## For all and there exists elimination
     
    def forallElim(self, lineNum, replacements): 
        """
        Given an expression forall(a,b,statement), forallElim substitutes a with another input
         variable to create a new forall statement
        :param lineNum: The line number of the line that showed the original forall statement 
        :param replacements: the list of elements to replace the existential elements
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence, forall):
            expr = evidence.replace(replacements)
            self.steps += [expr]
            self.justifications += [f'For all elimination on line {lineNum}'] 
            self.show() 
        else:
            print('Proof Error',f"There is no forall statmenent on line {lineNum}")
            
    
    def thereexistsElim(self, lineNum, replacements): # We can only do this once!
        """
        Given an expression forall(a,b,statement), forallElim substitutes a with another input variable to create a new forall statement
        :param lineNum: The line number of the line that showed the original forall statement 
        :param replacements: the list of elements to replace the existential elements
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence, thereexists):
            expr = evidence.replace(replacements)
            self.steps += [expr]
            self.justifications += [f'There exists elimination on line {lineNum}'] 
            self.show() 
        else:
            print('Proof Error', f"There is no there exists statmenent on line {lineNum}")
            

    ## Multiplication manipulation
    def leftMult(self, elemName, lineNum):
        """
        Left Multiply both sides of an equation with the input element 
        :param lineNum: the equation in the proof that is to be modified 
        :param elemName: the name of the element to left Multiply with 
        """
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq): 
            if elemName in eq.group.elements:
                elem = eq.group.elements[elemName]
                product = self.MultElem(elem, eq.LHS)
                result = Eq(product, self.MultElem(elem,eq.RHS), eq.group)
                self.steps += [result]
                self.justifications += [f'Left multiply line {lineNum} by {elem}'] 
                self.show()
            else:
                print('Proof Error', "The element " + elemName + " is not in the " + str(eq.group))
        else:
            print('Proof Error', f"Line {lineNum} is not an equation")

    def rightMult (self, elemName, lineNum):
        """
        Right Multiply both sides of an equation with the input element 
        :param lineNum: the line in the proof that is to be modified 
        :param elemName: the name of the element to right Multiply with
        """
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq):
            if elemName in eq.group.elements:
                elem = eq.group.elements[elemName]
                product = self.MultElem(eq.LHS, elem)
                result = Eq(product, self.MultElem(eq.RHS, elem), eq.group)
                self.steps += [result]
                self.justifications += [f'Right multiply line {lineNum} by {elem}'] 
                self.show()
            else:
                print('Proof Error', "The element " + elemName + " is not in the " + str(eq.group))
        else:
            print('Proof Error', f"Line {lineNum} is not an equation")


    def rightMultInverse (self, elemName, lineNum):
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq):
            if elemName in eq.group.elements:
                product = self.MultElem(eq.LHS,inverse(elemName,eq.group))
                result = Eq(product, self.MultElem(eq.RHS, inverse(elemName,eq.group)), eq.group)
                self.steps += [result]
                self.justifications += ['Right multiply line {lineNum} by '  + elemName]
                self.show()
            else:
                print('Proof Error', "The element " + elemName + " is not in the " + str(eq.group))
        else:
            print('Proof Error', f"Line {lineNum} is not an equation")

    def leftMultInverse (self, elemName, lineNum):
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq):
            if elemName in eq.group.elements:
                product = self.MultElem(inverse(elemName,eq.group), eq.LHS)
                result = Eq(product, self.MultElem(inverse(elemName,eq.group), eq.RHS), eq.group)
                self.steps += [result]
                self.justifications += ['Right multiply line {lineNum} by '  + elemName]
                self.show()
            else:
                print('Proof Error', "The element " + elemName + " is not in the " + str(eq.group))
        else:
            print('Proof Error', f"Line {lineNum} is not an equation")

    ##power methods 
    def breakPower(self,input):
        """
        Given an expression like e^a where a is a python integer, return a mult object equivalent to e^a
        :param power: the power to be converted to mult
        """  
        if isinstance(input,power):  
            exp=input.exponent   
            element = input.element 
            multList=[]
            for i in range(exp):
                multList.append(element)
            self.steps += [Mult(multList)]
            self.justifications += ['Convert power object to mult object'] 
            self.show()
        else:
            print('Proof Error',f"Expected a power object but received type {type(input)}")

    def combinePower(self, mult):
        """
        Given a mult object with a single element, convert it to a power object (for example turning e*e*e to e^3)
        :param mult: the mult object to be converted 
        """  
        if isinstance(mult,Mult): 
            multList=mult.elemList
            e=multList[0]
            singletonCheck = True
            for i in multList: 
                if i != e: 
                    singletonCheck = False
            if singletonCheck == False:
                print ('\n' +"Need a single element but given multiple")
            else:
                result=power(e,len(multList)) 
                self.steps += [result]
                self.justifications += ['Convert multiplications to equivalent powers'] 
                self.show()
        else:
            print('Proof Error',f"Expected a Mult object but received type {type(mult)}")

    def splitPowerAddition(self,input):
        """
        Simplify power objects: Given an expression e^a+b, convert to e^a*e^b. Given an expression e^a*b=(e^a)^b
        :param power: the power object with addition in exponent to be modified
        """  
        if isinstance(input, power):            
            element = input.element
            exp=input.exponent
            l=exp.split("+")
            if len(l)==1:
                print('Proof Error',"No power addition to be split apart")
            else:
                multList=[]
                for i in l: 
                    elem=power(element,i)
                    multList.append(elem)
                self.steps += [Mult(multList)]
                self.justifications += ["Split up power with addition in exponents"] 
                self.show()          
        else:
            print('Proof Error',f"Expected a power object but received type {type(input)}")     
             

    def splitPowerMult(self,input):
        """
        Simplify power objects: Given an expression e^a*b=(e^a)^b
        :param lineNum: the power object with mult in exponent to be modified
        """ 
        if isinstance(input, power) == False:       
            element = input.element
            exp=input.exponent
            l=exp.split("*")
            if len(l)==1:
                print('Proof Error',"No power multiplication to be split apart")
            else:
                elem=element
                for i in l: 
                    e=power(elem,i)
                    elem=e
                self.steps += [elem]
                self.justifications += ["Split up power with multiplication in exponents"] 
                self.show()
        else:
            print('Proof Error',f"Expected a power object but received type {type(input)}")
    
    ## Identity and equality elimination
    def rightSidesEq(self, lineNum1, lineNum2):
        """
        If two sides have the same right side, then set left sides to equal in a new line
        :param line1: the first line with same right side
        :param line2: the second line with the same right side
        """
        l1 = self.steps[lineNum1]
        l2 = self.steps[lineNum2]
        if l1.RHS == l2.RHS and l1.group == l2.group:
            self.steps += [Eq(l1.LHS,l2.LHS, l1.group)]
            self.justifications += [f"Equations with same right side on lines {str(lineNum1)}, {str(lineNum2)}"]
            self.show()
        else:
            print('Proof Error',f"The equations on lines {str(lineNum1)}, {str(lineNum2)} do not have the same right sides")

    def leftSidesEq(self, lineNum1, lineNum2):
        """
        If two sides have the same left side, then set right sides to equal in a new line
        :param line1: the first line with same left side
        :param line2: the second line with the same left side
        """
        l1 = self.steps[lineNum1]
        l2 = self.steps[lineNum2]
        if l1.LHS == l2.LHS and l1.group == l2.group:
            self.steps += [Eq(l1.RHS,l2.RHS, l1.group)]
            self.justifications += [f"Equations with same left side on lines {str(lineNum1)}, {str(lineNum2)}"]
            self.show()
        else:
            print('Proof Error',f"The equations on lines {str(lineNum1)}, {str(lineNum2)} do not have the same left sides")

    def identleft(self, lineNum):
        """
        Identity elimination: find the first pair of element and the group identity return an element 
        :param lineNum: the line of the proof to be modified 
        """
        evidence = self.steps[lineNum]
        if isinstance(evidence,Eq): 
            l = evidence.LHS.products
            l1=[]
            for i in range(len(l)-1):
                # deals with the case a*1
                # if isinstance(l[i],groupElement) and isinstance(l[i+1],ident):
                if isinstance(l[i+1],identity):
                    l1 = l[:i+1]+l[i+2:]
                    break
                # deals with the case 1*a
                # elif isinstance(l[i],ident) and isinstance(l[i+1],groupElement):
                elif isinstance(l[i],identity):
                    l1 = l[i+1:]
                    break
                # else we can't apply identity elimination 
            if l1==[]:
                print('Proof Error',"Identity can't be applied")
            else:
                newProduct = Mult(l1)
                ret = Eq(newProduct,evidence.RHS,evidence.group)
                self.steps += [ret]
                self.justifications += ["identity elimination "] 
                self.show() 
        else: 
            print('Proof Error',f"Expected an equation on line {lineNum} but received {type(evidence)}")

        
    def identright(self, lineNum):
        """
        Identity elimination: find the first pair of element and the group identity return an element 
        :param lineNum: the line of the proof to be modified 
        """
        evidence = self.steps[lineNum]
        if isinstance(evidence,Eq): 
            l = evidence.RHS.products
            l1=[]
            for i in range(len(l)-1):
                # deals with the case a*1
                # if isinstance(l[i],groupElement) and isinstance(l[i+1],ident):
                if isinstance(l[i+1],identity):
                    l1 = l[:i+1]+l[i+2:]
                    break
                # deals with the case 1*a
                # elif isinstance(l[i],ident) and isinstance(l[i+1],groupElement):
                elif isinstance(l[i],identity):
                    l1 = l[i+1:]
                    break
                # else we can't apply identity elimination 
            if l1==[]:
                print ('\n' + "Identity can't be applied")
            else:
                if len(l1) != 1:
                    newProduct = Mult(l1)
                else:
                    newProduct = l1[0]
                ret = Eq(evidence.LHS,newProduct,evidence.group)
                self.steps += [ret]
                self.justifications += ["identity elimination "] 
                self.show()
        else: 
            print('Proof Error', f"Expected an equation on line {lineNum} but received {type(evidence)}")

        

    def introReflexive(self,name,G):
        """
        Introduce a reflexive equality (like x=x)
        Necessary to show something equals something else when not given
        a starting equation
        :param eq: The equality you want to introduce
        """
        self.steps+=[Eq(name,name,G)]
        self.justifications += ["reflexive equality"] 
        self.show()
        # if eq.LHS == eq.RHS:
        #     self.steps+=[eq]
        #     self.justifications += ["reflexive equality"] 
        #     self.show()
        # else:
        #     print('Proof Error', "This is not reflexive")

    def reduceLogic(self, lineNum):
        """
        Recursively reduces a ND statement by pushing in the nots
        :param lineNum: the line of the proof to be modified 
        """
        evidence = self.steps[lineNum]
        if type(lineNum) in [And, Or, Implies, Not]:
            self.steps += [reduce(evidence)]
            self.justifications += ["logic reduction"] 
            self.show()
        else:
            print('Proof Error', "This is not a logic statement")

    def introCases(self, case):
        """
        Introduction of cases (law of excluded middle)
        :param case: the equation/logical statement of one case (the other is a not of that) 
        """
        case1 = case
        case2 = reduce(Not(case))
        self.steps += [Or(case1, case2)]
        self.justifications += ["Case introduction (LEM)"] 
        self.show()

    def introSubproof(self, assum):
        """
        WIP
        This one returns so the user has access to the new subproof
        We will have to make show recursive to make the subproof steps show
        :param assum: the assumption for the subproof
        """
        subproof = Proof(label="Subproof", assumption=assum, steps=copy.deepcopy(self.steps), justifications=copy.deepcopy(self.justifications), depth=self.depth+1, linestart=len(self.steps))
        self.show()
        self.steps+=[subproof]
        self.justifications+=["IntroSubproof"]
        return subproof

    def concludeSubproof(self, lineNum):
        """
        WIP
        You conclude a subproof from the parent subproof
        Work in progress, we should discuss how to do this.
        :param lineNum: the conclusion of the subproof to turn into an implies
        """
        evidence = self.steps[-1]
        if isinstance(evidence, Proof):
            conc = Implies(evidence.assumption,evidence.steps[lineNum])
            self.steps += [None]*(len(evidence.steps)-evidence.linestart-1)
            self.justifications += [None]*((len(evidence.steps))-evidence.linestart-1)
            self.steps += [conc]
            self.justifications += ["Conclusion of subproof"]
            self.show()
        else:
            print("You can only conclude a subproof right after one")
        

    def introElement(self,G, name):
        """
        Introduces an arbitrary element in G
        Can be used as evidence for a forall introduction
        :param G: the group the elemen is in
        :param name: the name of the new element
        """
        if G.contains(name):
            print('Proof Error', f"{name} is already in {G}")
        else:
            self.env[name] = G.newElement(name)
            self.steps += [In(name, G)]
            self.justifications += ["Introducing an arbitrary element"]
            self.show()
    
    def forAllIntroduction(self, equationLine, vars, elemIntroLines):
        '''
        Creates a for all from an equation with arbitrary variables
        :param equationLine: the equation
        :param vars: the names of the arbitrary variables
        :param elemIntroLines: the lines of the introductions of the variables (to show they are arbitrary)
        '''
        evidence = copy.deepcopy(self.steps[equationLine]) # Mo, do you need this?
        G = self.steps[elemIntroLines[0]].group
        #Checking that the lines introduce the arbitrary variables, and that the variables are all in the same group
        for i in range(len(vars)):
            v = vars[i]
            l = elemIntroLines[i]
            if self.steps[l].elem!=vars[i]:
                print('Proof Error', f'Line {l} does not introduce variable {v}')
            elif self.steps[l].group!=G:
                print('Proof Error', f'Element {v} is not in group {G}')
            else:
                #If you make it here, this is a valid for all intro
                self.steps+=[forall(vars,G,evidence)]
                self.justifications+=["For all introduction"]
                self.show()
                break

    def closure(self,G,a,b):
        '''
        Introduces ab as an element of G by closure
        :param G: the group a,b are in
        :param a: element a
        :param b: element b
        '''
        if G.contains(a) and G.contains(b):
            G.mulElements(a,b)
            self.steps+=[In(Mult([a,b]),G)]
            self.justifications+=["Closure"]
            self.show()
        else:
            if not G.contains(a):
                print('Proof Error',f"{a} is not in {G}")
            else:
                print('Proof Error',f"{b} is not in {G}")

    def cancelRight(self, lineNum, mult):
        '''
        Cancels element from right side of multiplication if it exists 
        :param lineNum: the line where the equation resides
        :param mult: the list of elements to eliminate
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, Eq):
            rhselems = evidence.RHS.products
            lhselems = evidence.LHS.products
            l = -1*len(mult)
            if rhselems[l:] == mult and lhselems[l:] == mult:
                self.steps += [Eq( Mult(lhselems[:l]), Mult(rhselems[:l]) , evidence.group )]
                self.justifications += [f"Right side cancellation of {mult} on line {lineNum}"]
                self.show()
            else:
                print('Proof Error',f"It seems like the right hand sides on line {lineNum} are not equal to {mult}")
        else:
            print('Proof Error',f"It doesn't seem like line {lineNum} contains an equation")

    def cancelLeft(self, lineNum, mult):
        '''
        Cancels element from left side of multiplication if it exists 
        :param lineNum: the line where the equation resides
        :param mult: the list of elements to eliminate
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, Eq):
            rhselems = evidence.RHS.products
            lhselems = evidence.LHS.products
            l = len(mult)
            if rhselems[:l] == mult and lhselems[:l] == mult:
                self.steps += [Eq( Mult(lhselems[l:]), Mult(rhselems[l:]) , evidence.group )]
                self.justifications += [f"Right side cancellation of {mult} on line {lineNum}"]
                self.show()
            else:
                print('Proof Error',f"It seems like the left hand sides on line {lineNum} are not equal to {mult}")
        else:
            print('Proof Error',f"It doesn't seem like line {lineNum} contains an equation")

    def switchSidesOfEqual(self, lineNum):
        '''
        Switches an equality like x=y to become y=x
        :param lineNum: the line where the equality to be flipped is on 
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, Eq):
            rhs = evidence.RHS
            lhs = evidence.LHS
            self.steps += [Eq(rhs , lhs , evidence.group )]
            self.justifications += [f"Switched sides of line {lineNum}"]
            self.show()
        else:
            print('Proof Error',f"Hmm, it doesn't look like line {lineNum} isn't an equality")
        
    def notElim(self, lineNum1, lineNum2):
        '''
        Eliminate a not into a contradiction
        :param lineNum1: the line containing the not statement
        :param lineNum2: the line which has the real statement
        '''
        evidence1 = self.steps[lineNum1]
        if isinstance(evidence1, Not):
            result = evidence1.elim(self.steps[lineNum2])
            self.steps += [result]
            self.justifications += [f'Contradiction from lines {lineNum1} and {lineNum2}']
            self.show()
        else:
            print('Proof Error',f"The statement on line {lineNum1} isn't a Not statement")

    def impliesIntroduction(self, lineNumsAssums, lineNumConc): # needs work, a lot of it
        '''
        Introduce an implication based on assumptions and a conclusion
        :param lineNumsAssums: the lines containing the assumptions
        :param lineNumConc: the line to conclude
        '''
        assums = []
        for line in lineNumsAssums:
            assums.append(self.steps[line])
        self.steps += [Implies(assums,self.steps[lineNumConc])]
        self.justifications += [f"Introduced implies based on assumptions on lines {lineNumsAssums} to conclude line {lineNumConc}"]
        self.show()

    def andElim(self, lineNum, n):
        '''
        Eliminate a not into a contradiction
        :param lineNum1: the line containing the not statement
        :param lineNum2: the line which has the real statement
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, And):
            if n==1:
                self.steps += [evidence.arg1]
                self.justifications += ["And elimination"]
                self.show()
            elif n==2:
                self.steps += [evidence.arg2]
                self.justifications += ["And elimination"]
                self.show()
            else:
                print('Proof Error',"You must choose argument 1 or 2")
        else:
            print('Proof Error',f"The statement on line {lineNum} isn't an And statement")
    
    def introInverse(self, G, name):
        if type(name) == str:
            if not G.contains(name):
                print('Proof Error', f"{name} is not defined")
                return
        else:
            for x in name.products:
                if not G.contains(x):
                   print('Proof Error', f"{x} is not defined")
                   return
                
        if type(name) == str:
            name_ = name
            lhs = self.MultElem(inverse(name_,G),G.elements[name_])
        else:
            name_ = Mult([G.elements[x] for x in name.products])
            lhs = self.MultElem(inverse(name_,G),name_)
        
        G.newElement(str(inverse(name_,G)))
        rhs = G.elements["e"]
        self.steps += [Eq(lhs,rhs,G)]
        self.justifications += ["Introducing the inverse of an element"]
        self.show()
        print(G.elements)