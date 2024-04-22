import matplotlib.pyplot as plt     # All the necessary modules, some are dehighlighted in VS Code but they will be used. 
import numpy as np
import sympy as sp
from numpy import *
from sympy import *
import re  
import time
import random
from tkinter import *
from threading import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from playsound import playsound
import os

top=None



'''
Class: Seed generates a graph at a random location on the x/y-plane, of random size. 
Begins by generating the upper and lower domains (x axis length) ranging from -200 to 200.
Then generates the upper and lower ranges (y axis length) initially equal to its domain, this is so the graph is to scale.
var.offset generates a random value from 0 to the midpoint of the y axis length.
This value is used to offset the new upper and lower ranges by a difference of var.offset, producing a randomly generated seed.
'''

class Seed:   # Randomly generate blank graph.
    def __init__(self,domain_lower,domain_upper,range_lower,range_upper):
        self.domain_lower=domain_lower
        self.domain_upper=domain_upper
        self.range_lower=range_lower
        self.range_upper=range_upper

S1=Seed(round(random.randint(-200,0),-1),round(random.randint(0,200),-1),None,None)     # Seed 1.

flip1=bool(random.getrandbits(1));flip2=bool(random.getrandbits(1))   

#if flip1==True:     # Flip graph for more randomness.
#    S1.range_lower=S1.domain_lower;S1.range_upper=S1.domain_upper
#else:
#    S1.range_lower=-S1.domain_upper;S1.range_upper=-S1.domain_lower

domain_midpoint=int((abs(S1.domain_lower)+S1.domain_upper)/2)
offset=random.randint(0,domain_midpoint-10)
S1.range_lower=-domain_midpoint;S1.range_upper=domain_midpoint

if flip2==True:     # offset y axis for more randomness.
    S1.range_lower-=offset;S1.range_upper-=offset
else:
    S1.range_lower+=offset;S1.range_upper+=offset



print(vars(S1))
print(offset)


'''
Class: Node generates random points on the graph.
generates P0: starting point of the curve,
P1: end point of the curve,

'''
class Node:    # Randomly generate nodes.
    def __init__(self,x_point,y_point):
        self.x_point=x_point
        self.y_point=y_point

P0=Node(random.randint(S1.domain_lower,round(int(S1.domain_lower+(abs(S1.domain_lower)+S1.domain_upper)/7))),random.randint(S1.range_lower,S1.range_upper))     # Point 0, the starting position, ranges from 1/7th of the left side of graph.
P1=Node(random.randint(round(int(S1.domain_upper-(abs(S1.domain_lower)+S1.domain_upper)/7)),S1.domain_upper),random.randint(S1.range_lower,S1.range_upper))     # Point 1, the end position, ranges from 1/7th of right side of graph.

print(vars(P0))
print(vars(P1))






def music():
    while True:
        playsound(os.getcwd()+'/Sounds/Josad ost.mp3')



def graph_function(): 
    global fig,top

    x = np.linspace(S1.domain_lower, S1.domain_upper, 300)     # Domain.
    fig, ax = plt.subplots(figsize=(10, 10))     # X by Y graph size.

    if 'x' not in user_function:     # Check if 'x' is in the user's function.
        y = [float(user_function) for _ in x]     # Create a constant function.
    else:
        y = eval(user_function)

    plt.xlim(S1.domain_lower-0.2, S1.domain_upper+0.2)     # Domain and range of graph.
    plt.ylim(S1.range_lower-0.2,S1.range_upper+0.2)     # Additional offsets is so first and last gridlines won't get cutoff.
    
    plt.plot(P0.x_point,P0.y_point,marker='x',markeredgewidth=2,color="blue")     # Plot and label nodes.
    plt.text(P0.x_point-2,P0.y_point+3,'Start ('+str(P0.x_point)+','+str(P0.y_point)+')',color='orange',fontsize='11',fontname="Helvetica")
    plt.plot(P1.x_point,P1.y_point,marker='x',markeredgewidth=2,color="blue")
    plt.text(P1.x_point+2,P1.y_point+3,'End ('+str(P1.x_point)+','+str(P1.y_point)+')',color='orange',fontsize='11',horizontalalignment='right',fontname="Helvetica")

    
    
    ax.plot(x, y)
    ax.set_aspect(aspect=1)     # Aspect ratio, larger number -> longer y axis.

    ax.grid(True, which='both')

    
    ax.spines['left'].set_position('zero')     # Set the ticks for x and y axis.
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()
    ax.minorticks_on()
    
    #plt.grid(visible=True, which='major', color='b', linestyle='-')     # Set gridlines. 
    plt.grid(visible=True, which='minor', color='grey', linestyle='-',linewidth=0.2)

    
    plt.title('f(x) = '+str(original_entry))     # Add title and labels.
    ax.set_xlabel('x', loc='right')
    ax.set_ylabel('y', loc='top')
    

    
    if top:     # Update toplevel window if it exists.
        top.destroy()
        top.update()
    top = Toplevel()     # Create toplevel window.
    top.title("Graph")
    top.geometry("800x800+0+0")  # Set the position of the window.
    top.resizable(0,0)

    
    canvas = FigureCanvasTkAgg(fig, master=top)    # Create a canvas and add the plot to it.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


def error_check():
    global user_function,ax,x,y,error_label,original_entry

   
    user_function = function_entry.get()      # Get user input as a function expression.
    original_entry = function_entry.get()     # Get a copy of the user's original input. 

    try:
       
        if not user_function:      # If the user didn't input anything, plot nothing.
            user_function=str(9999)
       
        user_function = re.sub(r'(\d+)([a-zA-Z_]+)', r'\1*\2', user_function)      # Substitute multiplication with * symbols for use in numpy.
        
        user_function=(
           user_function     # Make notation substitutions for use in numpy.
                .replace("^","**")
                .replace("sin","np.sin")     # Trig functions.
                .replace("cos","np.cos")
                .replace("tan","np.tan")
                .replace("sec","np.sec")
                .replace("csc","np.csc")
                .replace("cot","np.cot")
                .replace("sqrt","np.sqrt")
                .replace("abs","np.abs")
                .replace("pi", str(np.pi))     # Constants.
                .replace("e", str(np.e))
       )

        print(user_function)
        

        x = np.linspace(0,0,0)     # Test to see if user function is plottable for error checking before actually graphing it. 
        if 'x' not in user_function:     
            y = [float(user_function) for _ in x]     
        else:
            y = eval(user_function)


        error_label.config(text="")     # Clear error label, no error present. 

        return graph_function()     # Graph the function.

    except Exception:

        if user_function.count("(") != user_function.count(")"):
            error_label.config(text="Check all brackets have been closed.")     # Inform user their brackets have not been closed. 
        else:
            error_label.config(text="Unrecognized function, check notation.")     # Inform user they have not inputted a valid function.



def main():

    global function_entry,error_label,user_function,original_entry,top

    Thread(target=music).start()
    

    function_label=Label(root,text='f(x)=')
    function_label.place(x=0,y=0)

    function_entry=Entry(root,width=20)
    function_entry.place(x=30,y=0)

    graph_button=Button(root,text='Graph',command=error_check)
    graph_button.place(x=165,y=0)

    error_label=Label(root,text="",fg="red") 
    error_label.place(x=220,y=0)

    user_function=str(9999)
    original_entry=""
    graph_function()

    root.title("Input a function")
    root.geometry("800x100+0+836")
    root.resizable(0,0)
    root.mainloop()


root = Tk()
main()