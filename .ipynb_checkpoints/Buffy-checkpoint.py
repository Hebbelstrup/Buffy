from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import numpy as np
import os
import subprocess

root = Tk()
style = ttk.Style()
style.theme_use('aqua')
root.title("Buffer calc 9000")
root.geometry('240x550')

############################ IMPORT ############################################
with open('reagents.txt','r') as inf:
    reagents = eval(inf.read()) # Open reagents.txt and loads them as a dict now contained in reagents. No idea why this works.


############################ FUNCTIONS ############################################

store = [] # Array to store input
increment = 2
final = []
labels = []

def get_values():  
    
    global store
    global increment # defines that i want to use the global variable, increment.
    global reagents
    global final
    global labels
    
    reagent = c1.get() # Gets text from Entry 1
    concentration = c2.get() # Gets text from Entry 2
    
    try:
        if reagents[reagent]: # if reagents dict contains the key for reagent input, continue
        
            if not reagent or not concentration: # If reagent or concentration is false ( not filled in ), pass. Else increment by 1 and add label.
                pass
            else:
                display = Label(root, text= concentration + 'M ' + reagent, background='white')
                display.grid(column=1,row=increment, columnspan=3) # Displays a label at column one, and increments by one row each click. 
                increment = increment + 1
                store.append([reagent, concentration]) # Saves component and concetration as a list. Accessible by store[x][y] - where x is the iteration of component, and y = 0 is comp_txt and y = 1 is [c]
                labels.append(display)
                
            c1.delete('0', END) # Deletes text in entry 1
            c2.delete('0', END) # Deletes text in entry 2
            c1.focus()   
        
        
    except:
        messagebox.showerror('Error','Reagent not in reagent list. Try again') # Creates Errorbox if reagents dict does not match reagent input
        c1.delete('0',END)
        c2.delete('0',END)
        c1.focus
    
    
    
def calculate(): 
    volume = Volume.get()
    
    if not volume:
        messagebox.showerror('Error','No volume detected')
    else:
        
        for i in range (0,len(store)):
                    global final
                    grams = float(reagents[str(store[i][0])]) * float(store[i][1]) * float(volume) # Calculates the grams needed to make the desired buffer. g/mol * mol/L * L
                    final.append([str(round(grams,2)) +'g ' + str(store[i][0])])
    
      
        buffer = Tk()
        style = ttk.Style()
        style.theme_use('aqua')
        buffer.title("Buffer")
        
        Label(buffer, text= "Buffer ingredients: \n\n", background='white',font=("Ariel Bold",13)).pack(fill=tk.BOTH, expand=True)
        for i in range(0, len(final)):
            
                Label(buffer, text= " ".join(final[i]), background='white', font=("Arial Bold", 13)).pack(fill=tk.BOTH, expand=True)
                
        Label(buffer, text="\n\nIn %s L MQ" % float(volume), background='white',font=("Ariel Bold",13)).pack(fill=tk.BOTH, expand=True)
        buffer.focus_force()
        buffer.mainloop()

        
        
def reset():
    global labels
    global final
    global store
    global increment
    global Volume
    
    final = [] # Simply resets counters and list that store, so that everything is wiped
    store = []
    increment = 2 # need to set counter back, or new reagents positions will be off
    
    
    for label in labels: label.destroy()
    c1.focus()
    Volume.delete('0',END)

    
    
def open_reagent():
    subprocess.call(['open', 'reagents.txt'])

############################ BUTTONS AND INITIALIZE ############################################

#### reagent entry ####
Label(root, text="Reagent", background='white', font=("Arial Bold", 13)).grid(column=1, row=0, sticky=N)
c1 = Entry(root, width=10) # Molar weight
c1.grid(column=1, row=1)

#### Concentration entry ####
Label(root, text="[C] in M", background='white', font=("Arial Bold", 13)).grid(column=2, row=0, sticky=N)
c2 = Entry(root, width=10) # Molar weight
c2.grid(column=2, row=1)

#### Add button ####
add = Button(root, text='Add', command= get_values) 
add.grid(column=3, row=1)

#### Volume button ###

Vol_label = Label(root, text= "Volume in L", background='white', font=("Arial Bold", 13)).place(relx=0.5, rely=0.6, anchor=CENTER)
Volume = Entry(root, width = 10)
Volume.place(relx=0.5, rely=0.65, anchor=CENTER)

#### Calculate button ####
Calc = Button(root, text='Calculate', command= calculate)
Calc.place(relx=0.5, rely=0.73, anchor=CENTER)

#### RESET BUTTON ####
reset_button = Button(root, text='  Reset ', command= reset)
reset_button.place(relx=0.33, rely=0.85, anchor=CENTER)

##### Reagent button ####

reagent_button = Button(root, text='Reagents', command= open_reagent)
reagent_button.place(relx=0.68, rely=0.85, anchor= CENTER)



def Enter(Enter): # neccesary for root.bind('Return') to work - get_values does not take a positional arguement, but the bind gives it one. 
    get_values() 

root.bind('<Return>', Enter) # Binds return key to the get_values function
c1.focus()
root.focus_force()
root.resizable(width=False, height=False)
root.mainloop()