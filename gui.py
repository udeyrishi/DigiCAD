#!/usr/bin/python3
# Currently in beta stage
"""
A GUI for Boolean functions; a Boolean function toolbox. It contains some minor glitches, but it
demonstrates many of the methods in the Boolean function class. There is some functionality 
missing from this GUI, such as printing out truth tables and comparing functions to each other.

If you input a function with more than 5 variables, there the list of minterms and/or maxterms will 
become long, and the GUI window will stretch. You may not be able to clear the text; if this occurs,
simply exit the GUI and re-enter.

After every input, the output function is stored in the clipboard. The restore button will restore
previous functions (to the clipboard) that were used in the GUI in that particular session.

Using the GUI, you can do the following with a Boolean function:
-Find the minterms (numerical values where the function is true)
-Find the maxterms (numerical values where the function is false)
-Find the minterm expansion
-Find the maxterm expansion
-Find the simplest expression in SOP form
-Find the negation of the function
-Manipulate two functions at the same time (there are two input boxes)
-Restore previous functions

Examples (these can be typed directly into the input boxes):

--> a+b
--> f(a, b) = a + b
--> a % b
--> a * b + c | d

Source for the GUI outline:
http://www.tkdocs.com/tutorial/firstexample.html

Developed by: Raghav Vamaraju, 2014
"""

# Import modules from Tkinter and the Boolean Function module.
from tkinter import *
from tkinter import ttk
from boolfunc import *

# Define the Tk instance, the window size, and the window title.
root = Tk()
root.geometry("1200x500+300+300")
root.title("Boolean Function Toolbox")
root.clipboard_clear()

# Define the frame which will be used for the GUI.
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# Variable definitions. 
# There are two sides to the GUI, and each side can handle different inputs simultaneously.
# Each variable must be defined twice (once for each side).
user_input0 = StringVar()
user_input1 = StringVar()

original0, original1 = StringVar(), StringVar()
minterms0, minterms1 = StringVar(), StringVar()
min_expansion0, min_expansion1 = StringVar(), StringVar()
maxterms0, maxterms1 = StringVar(), StringVar()
max_expansion0, max_expansion1 = StringVar(), StringVar()
simplify_sop0, simplify_sop1 = StringVar(), StringVar()
simplify_pos0, simplify_pos1 = StringVar(), StringVar()
negate0, negate1 = StringVar(), StringVar()
restore0, restore1 = StringVar(), StringVar()

# A list of variables and a record of the inputs will be global variables.
variable_list = [[original0, minterms0, min_expansion0, maxterms0, \
                 max_expansion0, simplify_sop0, simplify_pos0, negate0, restore0], \
                 [original1, minterms1, min_expansion1, maxterms1, \
                 max_expansion1, simplify_sop1, simplify_pos1, negate1, restore1]]
input = [None, None]
function = [[], []]                 
counter = [-1, -1]
 
def calculate(side=None, mode=None, clear=0):
    """
    Function which does the Boolean calculations. It assigns the results 
    to the appropriate variables in the GUI.
    """

    global variable_list, input, function, counter
    
    # Increment the counter of the number of functions entered.
    # This will be used to retrace previous entries.
    if not clear:
        counter[side] += 1    
    
    # If no side and mode is given, do nothing.
    if side == None and mode == None:
        pass
        
    elif clear:
        variable_list[side][mode].set('')
        
    else:
        try:
            # Inputs can occur on side 0 or side 1. Set variables accordingly.
            if side == 0:
                input[side] = str(user_input0.get())
            elif side == 1:
                input[side] = str(user_input1.get())

            # Append the latest user input to the resevoir of user inputs.
            function[side].append(BF(input[side]))
            
            # Mode 0: Display the original function.
            if mode == 0:
                variable_list[side][mode].set(function[side][counter[side]])

            # Mode 1: Display the minterms.
            elif mode == 1:
                variable_list[side][mode].set(function[side][counter[side]].minterms())
                
            # Mode 2: Display the minterm expansion.
            elif mode == 2:
                variable_list[side][mode].set(function[side][counter[side]].min_expand())
         
            # Mode 3: Display the maxterms.
            elif mode == 3:
                variable_list[side][mode].set(function[side][counter[side]].maxterms())
         
            # Mode 4: Display the maxterm expansion.
            elif mode == 4:
                variable_list[side][mode].set(function[side][counter[side]].max_expand())
                
            # Mode 5: Display the simplified function in SOP form.
            elif mode == 5:
                variable_list[side][mode].set(function[side][counter[side]].min_sop())
         
            # Mode 6: Display the simplified function in POS form.
            elif mode == 6:
                variable_list[side][mode].set("Still under development. Try SOP form instead.")
         
            # Mode 7: Display the function negated.
            elif mode == 7:
                variable_list[side][mode].set(function[side][counter[side]].bf_not())
         
            # Mode 8: Copy the previous function to the clipboard and display it.
            elif mode == 8:
                if counter[side] > 0:
                    counter[side] -= 1
                else:
                    counter[side] = 0
                variable_list[side][mode].set(function[side][counter[side]])
                counter[side] -= 1
            
            root.clipboard_clear()
            root.clipboard_append(function[side][counter[side]])            
              
        except SyntaxError:
            variable_list[side][mode].set("Invalid syntax! Try enclosing terms with brackets.")
     
        except IndexError:
            counter[side] = 0
            variable_list[side][mode].set("Index Error! Please try again. Otherwise, reset program.")

        
user_entry0 = ttk.Entry(mainframe, width=30, textvariable=user_input0)
user_entry0.grid(column=2, row=1, sticky=(W, E))
user_entry1 = ttk.Entry(mainframe, width=30, textvariable=user_input1)
user_entry1.grid(column=5, row=1, sticky=(W, E))


# Buttons for the left-hand side (side 0).
ttk.Button(mainframe, text="Original", command=lambda:calculate(0,0,0), width=20).grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, textvariable=original0).grid(column=2, row=3, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,0,1)).grid(column=4, row=3, sticky=W)

ttk.Button(mainframe, text="Minterms", command=lambda:calculate(0,1,0), width=20).grid(column=3, row=4, sticky=W)
ttk.Label(mainframe, textvariable=minterms0).grid(column=2, row=4, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,1,1)).grid(column=4, row=4, sticky=W)

ttk.Button(mainframe, text="Minterm Expansion", command=lambda:calculate(0,2,0), width=20).grid(column=3, row=5, sticky=W)
ttk.Label(mainframe, textvariable=min_expansion0).grid(column=2, row=5, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,2,1)).grid(column=4, row=5, sticky=W)

ttk.Button(mainframe, text="Maxterms", command=lambda:calculate(0,3,0), width=20).grid(column=3, row=6, sticky=W)
ttk.Label(mainframe, textvariable=maxterms0).grid(column=2, row=6, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,3,1)).grid(column=4, row=6, sticky=W)

ttk.Button(mainframe, text="Maxterm Expansion", command=lambda:calculate(0,4,0), width=20).grid(column=3, row=7, sticky=W)
ttk.Label(mainframe, textvariable=max_expansion0).grid(column=2, row=7, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,4,1)).grid(column=4, row=7, sticky=W)

ttk.Button(mainframe, text="Simplify to SOP", command=lambda:calculate(0,5,0), width=20).grid(column=3, row=8, sticky=W)
ttk.Label(mainframe, textvariable=simplify_sop0).grid(column=2, row=8, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,5,1)).grid(column=4, row=8, sticky=W)

ttk.Button(mainframe, text="Simplify to POS", command=lambda:calculate(0,6,0), width=20).grid(column=3, row=9, sticky=W)
ttk.Label(mainframe, textvariable=simplify_pos0).grid(column=2, row=9, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,6,1)).grid(column=4, row=9, sticky=W)

ttk.Button(mainframe, text="Negate", command=lambda:calculate(0,7,0), width=20).grid(column=3, row=10, sticky=W)
ttk.Label(mainframe, textvariable=negate0).grid(column=2, row=10, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,7,1)).grid(column=4, row=10, sticky=W)

ttk.Button(mainframe, text="Restore", command=lambda:calculate(0,8,0), width=20).grid(column=3, row=11, sticky=W)
ttk.Label(mainframe, textvariable=restore0).grid(column=2, row=11, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(0,8,1)).grid(column=4, row=11, sticky=W)


# Buttons for the right-hand side (side 1).
ttk.Button(mainframe, text="Original", command=lambda:calculate(1,0,0), width=20).grid(column=6, row=3, sticky=W)
ttk.Label(mainframe, textvariable=original1).grid(column=5, row=3, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,0,1)).grid(column=7, row=3, sticky=W)

ttk.Button(mainframe, text="Minterms", command=lambda:calculate(1,1,0), width=20).grid(column=6, row=4, sticky=W)
ttk.Label(mainframe, textvariable=minterms1).grid(column=5, row=4, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,1,1)).grid(column=7, row=4, sticky=W)

ttk.Button(mainframe, text="Minterm Expansion", command=lambda:calculate(1,2,0), width=20).grid(column=6, row=5, sticky=W)
ttk.Label(mainframe, textvariable=min_expansion1).grid(column=5, row=5, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,2,1)).grid(column=7, row=5, sticky=W)

ttk.Button(mainframe, text="Maxterms", command=lambda:calculate(1,3,0), width=20).grid(column=6, row=6, sticky=W)
ttk.Label(mainframe, textvariable=maxterms1).grid(column=5, row=6, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,3,1)).grid(column=7, row=6, sticky=W)

ttk.Button(mainframe, text="Maxterm Expansion", command=lambda:calculate(1,4,0), width=20).grid(column=6, row=7, sticky=W)
ttk.Label(mainframe, textvariable=max_expansion1).grid(column=5, row=7, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,4,1)).grid(column=7, row=7, sticky=W)

ttk.Button(mainframe, text="Simplify to SOP", command=lambda:calculate(1,5,0), width=20).grid(column=6, row=8, sticky=W)
ttk.Label(mainframe, textvariable=simplify_sop1).grid(column=5, row=8, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,5,1)).grid(column=7, row=8, sticky=W)

ttk.Button(mainframe, text="Simplify to POS", command=lambda:calculate(1,6,0), width=20).grid(column=6, row=9, sticky=W)
ttk.Label(mainframe, textvariable=simplify_pos1).grid(column=5, row=9, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,6,1)).grid(column=7, row=9, sticky=W)

ttk.Button(mainframe, text="Negate", command=lambda:calculate(1,7,0), width=20).grid(column=6, row=10, sticky=W)
ttk.Label(mainframe, textvariable=negate1).grid(column=5, row=10, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,7,1)).grid(column=7, row=10, sticky=W)

ttk.Button(mainframe, text="Restore", command=lambda:calculate(1,8,0), width=20).grid(column=6, row=11, sticky=W)
ttk.Label(mainframe, textvariable=restore1).grid(column=5, row=11, sticky=(W, E))
ttk.Button(mainframe, text="Clear", command=lambda:calculate(1,8,1)).grid(column=7, row=11, sticky=W)


ttk.Label(mainframe, text="Enter a Boolean function in the form:\nf(a,...,n) = a+b*c%d").grid(column=1, row=1, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

user_entry0.focus()
root.bind('<Return>', calculate)

root.mainloop()
