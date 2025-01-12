'''
Michael Yu

My 91906 Math game program;
Josad's Journey is a game about learning how to graph functions.

GUI made using Tkinter, Pillow and Matplotlib,
Computations made using Sympy and Numpy,
Music imported using Pygame Mixer.

Program created using VS Code,
Graphics designed using Adobe PS, 
Music composed using MuseScore 4.

Game by me,
Graphics by me,
Program by me,
Music by me.
'''


import matplotlib.pyplot as plt     # All the necessary modules.
import matplotlib.patheffects as pe     # This gives coordinate text a small white outline to improve visibility.
import numpy as np     # Numpy interprets input notation.
import sympy as sp     # Sympy solves equations to check collision with nodes.
from numpy import *
from sympy import *
import re     # Allows Regular expression when getting file location.
import random     # Randomness for RNG.
from tkinter import *     # GUI module.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # Let Matplotlib update graphs live.
import matplotlib.image as mpimg     # Import background images for graphs.
import json     # Json file to store player data.
import os     # Get relative paths for files. 
from pygame import mixer     # Play sfx and background music. Pygame is the easiest & most compatible method for doing this.
from matplotlib.patches import *     # Plot advanced shapes on Matplotlib.
from sympy import degree     # Detect degree of user function.
from sympy.abc import x, y, q     # Variables used to solve equations.
from PIL import Image, ImageTk     # Use Pillow to import images. Pillow is the best method for doing this.
import time     # Time.


#import ctypes
#ctypes.windll.shcore.SetProcessDpiAwareness(0)


plt.figure()     # For some reason I need to graph nothing then immediately close it otherwise matplotlib starts glitching.
plt.close()

with open("game_data.json","r") as f:     # Open up the json file containing player data.
    data=json.load(f)


'''
Variables below
'''
goal_accomplished_top=None     # Begin with no toplevel windows.
new_player_top=None     
delete_top=None
achievements_top=None
notification_top=None
draw_canvas=True     # These variables that don't show up often so don't need to be part of a class.


class tb:     # Make these things a class: Tubicle-Oasis so I don't have to global it everywhere.

    WINDOW_HORIZONTAL_OFFSET=400     # Constant: the horizontal shift of all non-canvas type graphics e.g., tkinter labels, will have this constant shift as different devices have different screen lengths. (height isn't of concern).
        
    function_curve=None   # The variable assigned to the user's function being drawn, used to reconfigure its colour. 
    points_intersection=0     # If the curve has passed through start point and greenzone, passing through both=2, coins not needed.
    text_coordinates=None     # Display coordinate text on graph.
    level=None     # Stores the current levels the player is on.

    redzone_rectangle=None     # These 2 variables used and set to the specific redzones/greenzones properties to be plotted as shapes.
    greenzone_rectangle=None

    show_coordinates=False     # Coordinates are OFF by default.   
    invalid_input=False     # Will turn true if player's function is not valid. 
    show_hint=0     # Do not display hint by default (this isn't a true/false as 0 indicates off, 1 indicates 1st hint, 2 indicates 2nd hint).
    
    coins_list0=None     # The list of coins to spawn in the modes.
    coins_list1=coins_list2=coins_list3=coins_list4=coins_list5=coins_list6=coins_list7=coins_list8=coins_list9=coins_list10=None
    coins_list11=coins_list12=coins_list13=coins_list14=coins_list15=coins_list16=coins_list17=coins_list18=None

    levels_list=None     # List of levels
   
    music_toggle=True     # Music plays by default.

    name=data["Player"][0]["name"]     # Name of the player, from the json file.

    cumulative_L0_score=data["Zen"][0]["score"]     # Keep track of the previous zen mode score so that current,new score can be added to it to find cumulative score. 
    L0_round=data["Zen"][0]["round"]     # Keep track of the round / no. of completed rounds on zen mode. 

    previous_score=None     # Keep track of player's previous score on that level so that the game only saves the highscore, not the current one if it's lower.
    score_no_penalty=None     # Note down player's score if they didn't cross redzone for calculation later on. 

    weights_true=None     # The weights of chance of coin spawning, which varies depending on the difficulty setting. 
    weights_false=None
    game_difficulty=data["Player"][0]["difficulty"]     # Game difficulty, taken from json file.

    diamond=False     # If player has collected diamond or not (default False).
    graph_master=True     # If player has completed all 18 journey levels. 
    ace=True     # If place has gotten A+ on all 18 journey levels. 
    linear=True   # If all player's functions are linear. 

    current_music=None     # Get which soundtrack is currently playing. 

    tip_text=None      # Generate random tip in home menu. 

    buttons_list1=levels_list1=images_list1=None    # create list of levels to place level images quickly in the 3 journey menus later in the program. 
    buttons_list2=levels_list2=images_list2=None
    buttons_list3=levels_list3=images_list3=None
    
    achievement_1=data["Achievements"][0]["1"]     # Achievement 1, graph master.
    achievement_2=data["Achievements"][0]["2"]     # Achievement 2, finding peace.
    achievement_3=data["Achievements"][0]["3"]     # Achievement 3, functions expert.
    achievement_4=data["Achievements"][0]["4"]     # Achievement 4, achieving peace. 
    achievement_5=data["Achievements"][0]["5"]     # Achievement 5, ace.
    achievement_6=data["Achievements"][0]["6"]     # Achievement 6, diamond discovery.
    achievement_7=data["Achievements"][0]["7"]     # Achievement 7, eternal peace.
    achievement_8=data["Achievements"][0]["8"]     # Achievement 8, minimalist.
    achievement_9=data["Achievements"][0]["9"]     # Achievement 9, dirty cheater. 

'''
All music code below:
2 soundtracks: Josad OST for main background music,
Zen OST for zen mode.
Music can be toggled on/off in settings. 
'''
mixer.init()    # Initiate mixer.

time.sleep(0.6)     # Wait a little bit so the music plays on time as the game loads.


def play_josadost_music():     # Quick function to play background music, (-1) makes it loop. 
    mixer.music.load(os.getcwd()+r'\Sounds\Josad ost.wav')
    mixer.music.play(-1)
    tb.current_music="Josad ost"


def play_zenost_music():
    mixer.music.load(os.getcwd()+r'\Sounds\Zen ost.wav')     # Second background music, plays in zen mode. 
    mixer.music.play(-1)
    tb.current_music="Zen ost"


clicked_sfx = mixer.Sound(os.getcwd()+r"\Sounds\button click sfx.wav")     # Sound effect when button is clicked. 
clicked_sfx.set_volume(0.5)     # Adjust volume. 
error_sfx = mixer.Sound(os.getcwd()+r"\Sounds\error sfx.wav")     # Error sound effect when player makes invalid input. 
error_sfx.set_volume(0.4)      # Adjust volume. 
level_complete_sfx = mixer.Sound(os.getcwd()+r"\Sounds\level complete sfx.wav")     # Level complete sound effect when player completes level.
level_complete_sfx.set_volume(0.45)      # Adjust volume. 


def stop_background_music():     # Stop background music. 
    mixer.music.stop()


play_josadost_music()     # Start the game by having josad OST play.


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


'''zen mode seed'''
def spawn_zen_seed():     # randomly generate the zen mode seed configurations. This is put into a function to use later on to re-randomly generate a new seed each time user starts up zen mode. 
    global S0,offset,flip2,domain_midpoint
    S0=Seed(round(random.randint(-200,0),-1),round(random.randint(0,200),-1),None,None)     # Seed 1, for zen mode.
    flip2=bool(random.getrandbits(1))     # Randomly generate either True or False.

    domain_midpoint=int((abs(S0.domain_lower)+S0.domain_upper)/2)     # Get the midpoint coordinate for the seed.

    try:
        offset=random.randint(0,domain_midpoint-10)     # Stop nodes spawning on the edges of graph.
    except Exception:
        offset=0     # Sometimes seed can get unlucky and will spawn origin off the grid, in this case, make offset 0 to prevent axis from going out of view.

    S0.range_lower=-domain_midpoint;S0.range_upper=domain_midpoint     # Get the lower range of the seed.

    if flip2==True:     # offset y axis for more randomness.
        S0.range_lower-=offset;S0.range_upper-=offset
    else:
        S0.range_lower+=offset;S0.range_upper+=offset


spawn_zen_seed()     # Spawn the zen seed, RNG.

'''journey mode seed'''
S1=Seed(0,10,0,10)     # Seed 1, for journey mode level 1. 
S2=Seed(-10,10,0,20)    # Seed 2 for journey mode level 2 etc.
S3=Seed(-8,16,-10,14)
S4=Seed(-12,10,-10,12)
S5=Seed(-15,15,-5,25)
S6=Seed(-20,20,-20,20)
S7=Seed(-5,50,-5,50)
S8=Seed(-16,14,-15,15)
S9=Seed(-85,15,-60,40)
S10=Seed(-45,45,-5,85)
S11=Seed(-170,30,-90,110)
S12=Seed(-26,44,-35,35)
S13=Seed(-120,120,-90,160)
S14=Seed(-90,70,-85,75)
S15=Seed(-100,220,-120,200)
S16=Seed(-100,60,-100,60)
S17=Seed(-450,120,-180,390)
S18=Seed(-140,145,-65,220)


'''
Class: Node generates random points on the graph.
generates P nodes: the start and end points,
generates C nodes: the 'coins' to be collected,
the graph is divided vertically into 7 even sections, each node having its own area to randomly spawn in. 
left end of graph is 0th section, right end is 7th section.
'''
class Node:    # Randomly generate nodes.
    def __init__(self,x_point,y_point,chance):
        self.x_point=x_point
        self.y_point=y_point
        self.chance=chance


def area(section):     # generate the area for node to randomly spawn based of the nth section of the graph.
    return round(int(S0.domain_lower+int(section)*(abs(S0.domain_lower)+S0.domain_upper)/7))


boolean=[True,False]     # Spawn node? -> yes/no (66% chance yes, 33% no)


def spawn_node(start,end):     # Function to generate 2 points, 5 coins in their dedicated sections of the graph. e.g., 1/7th section is first section, 7/7th is last.
    return Node(random.randint(area(start),area(end)),random.randint(S0.range_lower,S0.range_upper),(random.choices(boolean,weights=[tb.weights_true,tb.weights_false]))[0])     # 'weights' adjusts the probability of a coin spawning. currently is set to 2/3.


def journey_coins_chance(level):
    """Respawn the coins for journey mode, their positions remain fixed/not randomly generated, but their chances of spawning are.

    Args:
        level (Class): Configures the level based on the current level.
    """    
    
    for obj in level.coins:
        obj.chance=random.choices(boolean,weights=[tb.weights_true,tb.weights_false])[0]     # Respawn the chances of coins spawning for all coins in this specific level.
    if level==L12:
        C12_diamond.chance=random.choices(boolean,weights=[2,5+tb.weights_false*5])[0]     # Respawn chances of diamond spawning in level 12. 
        if C12_diamond.chance==True:     # If diamond has spawned, add it to the list. 
            tb.coins_list12.append(C12_diamond)


if data["Player"][0]["difficulty"]=="Novice":    # The weights for chances that coin spawns in journey level, default is set to STANDARD so 2/3 chance. 
    tb.weights_true=3;tb.weights_false=0     # 3/3 chance of spawning coins.
elif data["Player"][0]["difficulty"]=="Standard":
    tb.weights_true=2;tb.weights_false=1     # 2/3 chance of spawning coins.
elif data["Player"][0]["difficulty"]=="Expert":
    tb.weights_true=1;tb.weights_false=2     # 1/3 chance of spawning coins.
 

'''zen mode nodes''' 
def spawn_zen_nodes():     # This has been made into a function to be called again whenever user enters zen mode because these will randomly be generated each time user does so.
    global P0,C0_1,C0_2,C0_3,C0_4,C0_5
 
    P0=spawn_node(0,1);P0.chance=True;P0.x_point+=1  # start and end points: P0, must spawn.
    C0_1=spawn_node(1,2)     # These are all the coins, 'C' to spawn in zen mode, denoted with the following '0'. Number proceeding '_'is the nth coin of the mode. e.g., C1_5 -> 5th coin of journey level 1.
    C0_2=spawn_node(2,3)
    C0_3=spawn_node(3,4)
    C0_4=spawn_node(4,5)
    C0_5=spawn_node(5,6)     # Spawn_nodes function used to randomly spawn within the horizontal areas of the arguments, for coordinate spawning, directly make a Node object.
    tb.coins_list0=[C0_1,C0_2,C0_3,C0_4,C0_5]     # Make these coins a list to put as an attribute for class: Level.
spawn_zen_nodes()     # Randomly spawn start point and coins.


'''journey level nodes'''  
P1=Node(1,1,True)     # Start node for journey level 1.
C1_1=Node(6,6,None)     # 2/3 chance of spawning a coin, max. 2 coins possible.
tb.coins_list1=[C1_1]     # Make coins into list for easier use later in program.

P2=Node(-8,19,True)
C2_1=Node(-2,12,None)    
C2_2=Node(5,7,None)
tb.coins_list2=[C2_1,C2_2] 

P3=Node(-6,-8,True)
C3_1=Node(-3,-5,None)    
C3_2=Node(12,5,None)
tb.coins_list3=[C3_1,C3_2] 

P4=Node(-10,11,True)
C4_1=Node(-5,-5,None)    
C4_2=Node(0,-9,None)
C4_3=Node(5,-4,None)
tb.coins_list4=[C4_1,C4_2,C4_3] 

P5=Node(-14,0,True)
C5_1=Node(0,1,None)    
C5_2=Node(4,2,None)
C5_3=Node(12,10,None)
tb.coins_list5=[C5_1,C5_2,C5_3] 

P6=Node(-17,-1,True)
C6_1=Node(-1,-17,None)    
C6_2=Node(1,17,None)
tb.coins_list6=[C6_1,C6_2] 

P7=Node(0,0,True)
C7_1=Node(36,28,None)    
C7_2=Node(13,16,None)
C7_3=Node(4,11,None)
tb.coins_list7=[C7_1,C7_2,C7_3] 

P8=Node(-15,14,True)
C8_1=Node(-7,-10,None)    
C8_2=Node(0,0,None)
C8_3=Node(5,9,None)
tb.coins_list8=[C8_1,C8_2,C8_3] 

P9=Node(-80,-16,True)
C9_1=Node(-75,14,None)    
C9_2=Node(5,30,None)
C9_3=Node(-15,21,None)
C9_4=Node(-50,24,None)
tb.coins_list9=[C9_1,C9_2,C9_3,C9_4] 

P10=Node(-40,1,True)
C10_1=Node(4,76,None)    
C10_2=Node(15,43,None)
C10_3=Node(30,5,None)
C10_4=Node(-15,30,None)
tb.coins_list10=[C10_1,C10_2,C10_3,C10_4] 

P11=Node(-160,28,True)
C11_1=Node(-116,100,None)    
C11_2=Node(-80,-45,None)
C11_3=Node(-44,-16,None)
C11_4=Node(-10,-47,None)
tb.coins_list11=[C11_1,C11_2,C11_3,C11_4] 

P12=Node(-22,0,True)
C12_1=Node(-3,28,None)    
C12_2=Node(9,-28,None)
C12_3=Node(22,28,None)
C12_4=Node(35,-28,None)
C12_diamond=Node(-17,-30,random.choices(boolean,weights=[2,5+tb.weights_false*5])[0])     # Small chance of diamond spawning in level 12.
tb.coins_list12=[C12_1,C12_2,C12_3,C12_4] 
if C12_diamond.chance==True:     # If diamond has spawned, add it to the list. 
    tb.coins_list12.append(C12_diamond)

P13=Node(-110,140,True)
C13_1=Node(-80,80,None)    
C13_2=Node(-20,-40,None)
C13_3=Node(20,-70,None)
C13_4=Node(41,5,None)
C13_5=Node(90,100,None)
tb.coins_list13=[C13_1,C13_2,C13_3,C13_4,C13_5] 

P14=Node(-76,60,True)
C14_1=Node(-50,-77,None)    
C14_2=Node(30,-25,None)
C14_3=Node(51,-6,None)
C14_4=Node(-25,-33,None)
C14_5=Node(-60,-42,None)
tb.coins_list14=[C14_1,C14_2,C14_3,C14_4,C14_5] 

P15=Node(-90,110,True)
C15_1=Node(-50,141,None)    
C15_2=Node(15,170,None)
C15_3=Node(60,-100,None)
C15_4=Node(100,170,None)
C15_5=Node(170,140,None)
tb.coins_list15=[C15_1,C15_2,C15_3,C15_4,C15_5] 

P16=Node(-85,-26,True)
C16_1=Node(-27,13,None)    
C16_2=Node(26,-48,None)
C16_3=Node(0,-20,None)
C16_4=Node(19,20,None)
C16_5=Node(-19,-60,None)
tb.coins_list16=[C16_1,C16_2,C16_3,C16_4,C16_5] 

P17=Node(-400,-75,True)
C17_1=Node(-360,50,None)    
C17_2=Node(-230,115,None)
C17_3=Node(-100,130,None)
C17_4=Node(0,210,None)
C17_5=Node(60,290,None)
tb.coins_list17=[C17_1,C17_2,C17_3,C17_4,C17_5] 

P18=Node(-129,210,True)
C18_1=Node(-66,-14,None)    
C18_2=Node(-26,66,None)
C18_3=Node(22,-50,None)
C18_4=Node(76,114,None)
C18_5=Node(50,35,None)
tb.coins_list18=[C18_1,C18_2,C18_3,C18_4,C18_5] 


def plot_all():     # Quick function that plots all nodes. 
    plot_nodes(P0,"right",1,'x',"blue","Start",15,5,L0)    # Plot points and coins.
    #plot_nodes(P1,"left",-1,'x',"blue","End",15,5)     # With Size set to 15, 675/32 (approx. 21.1) Points lined up horizontally fits the horizontal length of graph. '''
    
    for obj in tb.coins_list0:    # plot all the coins, if the coin's spawn is false ie. doesn't spawn, then ignore this code.
        if obj.chance==True:
            plot_nodes(obj,"center",0,'o',"yellow","",30,1,L0)     # With Size set to 30, 13.5 coins lined up horizontally fits the horizontal length of graph. 


def plot_nodes(node,alignment,offset,marker,colour,label,size,width,level):     # Quick function which plots and labels all nodes, and is fully customizable using its arguments. 
    plt.plot(node.x_point,node.y_point,marker=marker,markersize=size,color=colour,markeredgewidth=width,path_effects=[pe.Stroke(linewidth=5, foreground='#ffff6e'), pe.Normal()],zorder=20)      #zorder makes nodes go in front of graph axis, pe.stroke gives a small cutout outline to coordinate text to make it readable.
    
    if tb.show_coordinates==True:     # If coordinates are on, print them. 
        tb.text_coordinates=plt.text(node.x_point+int(offset),node.y_point+horizontal_segment(20,level.seed),label+' ('+str(node.x_point)+','+str(node.y_point)+')',color='orange',fontsize='9',horizontalalignment=alignment,fontname="Arial",zorder=50).set_path_effects([pe.withStroke(linewidth=2, foreground='white')])
    
    else:     # If coordinates are off, only label the start and end nodes.
        tb.text_coordinates=plt.text(level.point.x_point,level.point.y_point+horizontal_segment(30,level.seed),"Start",color='orange',fontsize='9',horizontalalignment="right",fontname="Arial",zorder=50).set_path_effects([pe.withStroke(linewidth=2, foreground='white')])


'''
Class: Score
Used to keep track of all the player's score information.
'''
class Score:    
    def __init__(self,coins,goal,tries,score,penalty,grade):
        self.coins=coins      # Keep track of player's coins.
        self.goal=goal     # Keep track of player's goal.
        self.tries=tries     # Keep track of player's tries.
        self.score=score     # Keep track of player's score.
        self.penalty=penalty     # Keep track of player's penalty.
        self.grade=grade     # Keep track of player's grade.

'''Setup score objects, taking into account the saved data from json file. '''
Sc0=Score(0,"",0,0,"","")     # The score information for zen mode, updated by the below calculate_score function.
Sc0.score=data["Zen"][0]["score"]     # Update the zen mode grade and score to the saved data in json file. 
Sc0.grade=data["Zen"][0]["grade"]

Sc1=Score(0,"",0,0,"","")      # Initiate score information for all journey levels. 
Sc2=Score(0,"",0,0,"","")
Sc3=Score(0,"",0,0,"","")
Sc4=Score(0,"",0,0,"","")
Sc5=Score(0,"",0,0,"","")
Sc6=Score(0,"",0,0,"","")
Sc7=Score(0,"",0,0,"","")
Sc8=Score(0,"",0,0,"","")
Sc9=Score(0,"",0,0,"","")
Sc10=Score(0,"",0,0,"","")
Sc11=Score(0,"",0,0,"","")
Sc12=Score(0,"",0,0,"","")
Sc13=Score(0,"",0,0,"","")
Sc14=Score(0,"",0,0,"","")
Sc15=Score(0,"",0,0,"","")
Sc16=Score(0,"",0,0,"","")
Sc17=Score(0,"",0,0,"","")
Sc18=Score(0,"",0,0,"","")

score_list=[Sc1,Sc2,Sc3,Sc4,Sc5,Sc6,Sc7,Sc8,Sc9,Sc10,Sc11,Sc12,Sc13,Sc14,Sc15,Sc16,Sc17,Sc18]     # Put these score information in a list for later use.
for obj in score_list:      # Update all journey mode levels grade and score to the saved data in json file. 
    obj.score=data["Journey - Level "+str(score_list.index(obj)+1)][0]["score"]
    obj.grade=data["Journey - Level "+str(score_list.index(obj)+1)][0]["grade"]


def calculate_score(level):    
    """Calculate the player's score for that level.

    Args:
        level (Class): Calculates the score based on the current level.

    Returns:
        int: The player score.
    """    

    if level.score_info.goal=="Goal: Not accomplished":     # If player's function doesn't meet start/end points, score is 0.
        return 0
    
    else:     # Calculate score,default 100 points by completing goal, every coin is + 35 Tries is divided from sum; the more the worse.
        level.score_info.score=100+35*level.score_info.coins+round(50/level.score_info.tries)

        if level.score_info.penalty=="Penalty for Crossing Redzone":     # If player crosses redzone, score halves.
            tb.score_no_penalty=level.score_info.score     # Store score on the class variable.
            level.score_info.score=round(level.score_info.score/2)     # Halve score.
            return level.score_info.score
        
        else:
           
            return level.score_info.score     # If there is no penalty, return the original score.


def calculate_grade(level):    
    """ Calculate the player's grade based on his score for that level.

    Args:
        level (Class): Finds the grade based on the current level. 
    """    

    max_score=100+35*len(level.coins)+50     # The maximum score player can get to get A+ grade is 100(default bonus) + 35*total possible coins + 50(get it on 1st try) + 0(no redzone penalty).
    
    if 52+4*(max_score-52)/5 <= level.score_info.score <= 52+5*(max_score-52)/5:     # If the user's score reaches this max possible score, he gets A+.
        level.score_info.grade="A+"
      
    elif 52+3*(max_score-52)/5 <= level.score_info.score < 52+4*(max_score-52)/5:     # If user's score is within this range, he gets A.
        level.score_info.grade="A"
     
    elif 52+2*(max_score-52)/5 <= level.score_info.score < 52+3*(max_score-52)/5:     # If user's score is within this range, he gets B.
        level.score_info.grade="B"
    
    elif 52+1*(max_score-52)/5 <= level.score_info.score < 52+2*(max_score-52)/5:     # If user's score is within this range, he gets C.
        level.score_info.grade="C"
      
    elif 52 <= level.score_info.score < 52+1*(max_score-52)/5:     # If user's score is within this range, he gets D.
        level.score_info.grade="D"
    
    elif 0 <= level.score_info.score < 52:    # Technically the lowest possible score, gets no coins, takes ~infinite tries, crosses redzone (score halves) but still crosses greenzone to complete level. 
        level.score_info.grade="F"


def horizontal_segment(division,seed):     # Gives the length of the width of the graph when divided into specific segments. 
    return (abs(seed.domain_upper)+abs(seed.domain_lower))/division


'''
Class: Redzone generates a red area randomly on the graph.
picks a random point where a coin has not spawned as a potential redzone area.
x-y point is bottom left corner of rectangle; x_point is the corresponding x_point of unspawned coin,
width is randomly chosen 
y_point is randomly chosen between the lowest range of graph to vertical midpoint,
height is randomly chosen between 1 to half the height of the graph.

UPDATE: greenzone, denoted with G is the safe area at the right end of graph which as long as the user function passes through this, is valid. 
They're both under the same class: Redzone because they have the same object properties so wouldn't be appropriate to create an entire new class with the same code, just different name.
Greenzone appears at the very right of graph of 'x-width of seed / 20' thickness covering the edges. 
'''

class Redzone:     # Class: Redzone which penalises player if function passes through its area.
    def __init__(self,x0,y0,x1,y1,x2,y2,x3,y3,width,height,spawn):
        self.x0=x0;self.x1=x1;self.x2=x2;self.x3=x3
        self.y0=y0;self.y1=y1;self.y2=y2;self.y3=y3
        self.width=width;self.height=height
        self.spawn=spawn


'''
Spawns greenzone, this area is generalised based on the size of seed unlike redzones, for additional info on how this is generated, refer above.
'''
def greenzone(seed):     # Function which automatically sets up dimensions of greenzone based off the current level's seed.
    return Redzone(seed.domain_upper-int(horizontal_segment(20,seed)),seed.range_lower,seed.domain_upper,seed.range_lower,seed.domain_upper-int(horizontal_segment(20,seed)),seed.range_upper,seed.domain_upper,seed.range_upper,int(horizontal_segment(20,seed)),seed.range_upper-seed.range_lower,True)     # Redzone1 and Greenzone1 is for zen mode. 


'''Zen mode green/redzones'''
R0=Redzone(None,None,None,None,None,None,None,None,None,None,True)      # Corners: 0=bottom left, 1=bottom right, 2=top left, 3=top right. R0 starts off as all none as these properties will be randomly generated later on. 
def spawn_zen_greenzone():     # Make the greenzone for zen mode into a function to be used again later in the code to refit the new randomly generated graph's seed.
    global G0
    G0=greenzone(S0)     # Red/greenzone 0 is for zen mode.


spawn_zen_greenzone()     # Spawn the greenzone for zen.

'''Journey level green/redzones'''
R1=Redzone(5,1,6,1,5,2,6,2,1,1,False)     # Red/greenzone 1 is for journey mode level 1, where redzone coordinates are not randomly generated. For level 1 there is no redzone
G1=Redzone(9,0,11,0,9,11,11,11,2,11,True)     # G1 directly defined as class rather than using greenzone(seed) function because level 1 has a thicker greenzone.

R2=Redzone(1,1,5,1,1,3,5,3,2,2,False)     # No redzone yet in level 2.
G2=greenzone(S2)     # Quickly automatically spawn greenzone based off size of seed 2.

R3=Redzone(0,-1,4,-1,0,6,4,6,4,7,True)   # First appearance of redzone.    
G3=greenzone(S3)   

R4=Redzone(-3,-6,3,-6,-3,1,3,1,6,7,True)      
G4=greenzone(S4) 

R5=Redzone(-14,4,6,4,-14,6,6,6,20,2,True)      
G5=greenzone(S5)  

R6=Redzone(-4,-4,4,-4,-4,4,4,4,8,8,True)      
G6=greenzone(S6)  

R7=Redzone(24,-2,30,-2,24,24,30,24,6,26,True)      
G7=greenzone(S7) 

R8=Redzone(-12,3,1,3,-12,7,1,7,13,4,True)      
G8=greenzone(S8)   

R9=Redzone(-75,-11,-55,-11,-75,9,-55,9,20,20,True)      
G9=greenzone(S9)   

R10=Redzone(-10,5,10,5,-10,55,10,55,20,50,True)      
G10=greenzone(S10) 

R11=Redzone(-97,-3,-15,-3,-97,90,-15,90,82,93,True)      
G11=greenzone(S11) 

R12=Redzone(-18,-20,-14,-20,-18,30,-14,30,4,50,True)      
G12=greenzone(S12)

R13=Redzone(-5,-200,5,-200,-5,200,5,200,10,400,True)      
G13=greenzone(S13)

R14=Redzone(-2,-82,8,-82,-2,8,11,8,13,90,True)      
G14=greenzone(S14)

R15=Redzone(50,-50,70,-50,50,195,70,195,20,245,True)      
G15=greenzone(S15)

R16=Redzone(-100,-10,15,-10,100,5,15,5,115,15,True)      
G16=greenzone(S16)

R17=Redzone(-440,-170,-360,-170,-440,-101,-360,-101,80,69,True)      
G17=greenzone(S17)

R18=Redzone(100,83,117,83,100,215,117,215,17,132,True)      
G18=greenzone(S18)


def spawn_redzone():     # Randomly spawns the redzone, randomly generates the coordinates for all 4 points of the rectangle.
    R0.x0=random.randint(area(1),area(6))     # Spawn x point of redzone between the start/end points.
    R0.y0=random.randint(S0.range_lower,S0.range_upper)     # Spawn y point anywhere in the y-range of graph.

    R0.x1=R0.x0+random.randint(int(horizontal_segment(8,S0)),int(horizontal_segment(3,S0)))     # Make width/height range from 1/3rd of graph to 1/8th.
    R0.y1=R0.y0

    R0.x2=R0.x0
    R0.y2=R0.y0+random.randint(int(horizontal_segment(8,S0)),int(horizontal_segment(3,S0)))     # Make width/height range from 1/3rd of graph to 1/8th.

    R0.x3=R0.x1
    R0.y3=R0.y2

    R0.width=R0.x1-R0.x0      # Obtain rectangle width.
    R0.height=R0.y2-R0.y0     # Obtain rectangle height.


'''
Class: Level
All the previous classes were responsible for generating properties e.g., redzones, seeds...  
this class now organises all the previous objects into levels, L0=zen, L1 = journey level 1 etc.
this way I can refer to these simple objects later when the program actually generates these levels which is more efficient 
'''
class Level:
    def __init__(self,seed,point,redzone,greenzone,coins,score_info,title,hint,hint2,solution):
        self.seed=seed
        self.point=point
        self.redzone=redzone
        self.greenzone=greenzone
        self.coins=coins
        self.score_info=score_info
        self.title=title
        self.hint=hint
        self.hint2=hint2
        self.solution=solution


'''Declaration of levels'''
L0=Level(S0,P0,R0,G0,tb.coins_list0,Sc0,"Zen","(Hint unavailable)",None,None)                                                               # Note that these functions aren't the only answers, the levels were created from these original equations and alternatives may exist.
L1=Level(S1,P1,R1,G1,tb.coins_list1,Sc1,"Journey - Level 1","linear","ax",None)                                                             # x                                     linear
L2=Level(S2,P2,R2,G2,tb.coins_list2,Sc2,"Journey - Level 2","linear","a-bx",None)                                                           # -x+11                                 linear
L3=Level(S3,P3,R3,G3,tb.coins_list3,Sc3,"Journey - Level 3","linear","ax-b",None)                                                           # 2/3x-4                                linear
L4=Level(S4,P4,R4,G4,tb.coins_list4,Sc4,"Journey - Level 4","parabolic","x^2/b-a",None)                                                     # 1/5x^2-9                              parabolic
L5=Level(S5,P5,R5,G5,tb.coins_list5,Sc5,"Journey - Level 5","exponential","a^x",None)                                                       # 1.2^x                                 exponential
L6=Level(S6,P6,R6,G6,tb.coins_list6,Sc6,"Journey - Level 6","hyperbola","a/x",None)                                                         # 20/x                                  hyperbola
L7=Level(S7,P7,R7,G7,tb.coins_list7,Sc7,"Journey - Level 7","radical","a*sqrt(x)",None)                                                     # 5sqrt(x)                              radical
L8=Level(S8,P8,R8,G8,tb.coins_list8,Sc8,"Journey - Level 8","cubic","ax-x^3/b",None)                                                        # -x^3/72+2x                            cubic
L9=Level(S9,P9,R9,G9,tb.coins_list9,Sc9,"Journey - Level 9","logarithmic","a*ln(x+b)",None)                                                 # 6ln(x+80)                             logarithmic
L10=Level(S10,P10,R10,G10,tb.coins_list10,Sc10,"Journey - Level 10","exponential & parabolic","a*b^(-x^2/c)",None)                          # 80(1.1)^(-x^2/30)                     exponential
L11=Level(S11,P11,R11,G11,tb.coins_list11,Sc11,"Journey - Level 11","rational & parabolic","a*x^2/((x+b)*(x+c))",None)                      # 10x^2/((x+100)(x+10))                 rational
L12=Level(S12,P12,R12,G12,tb.coins_list12,Sc12,"Journey - Level 12","sinusoidal","a*cos((x+pi)/b)",None)                                    # 28cos((x+pi)/4)                       sinusoidal
L13=Level(S13,P13,R13,G13,tb.coins_list13,Sc13,"Journey - Level 13","radical & parabolic","a*sqrt(x^2-b)-c",None)                           # 2sqrt(x^2-100)-80                     radical
L14=Level(S14,P14,R14,G14,tb.coins_list14,Sc14,"Journey - Level 14","quartic","(x+a)*(x+b)*(c-x)*(d-x)/e",None)                             # (x+70)(x+10)(x-20)(x-60)/80000        quartic
L15=Level(S15,P15,R15,G15,tb.coins_list15,Sc15,"Journey - Level 15","sinusoidal & rational","a*sin(b-x/c)/(d-x)+e",None)                    # 2300sin(x/10-6)/(60-x)+120            sinusoidal
L16=Level(S16,P16,R16,G16,tb.coins_list16,Sc16,"Journey - Level 16","rational & cubic & quartic","a*x^3/((x+b)*(x+c)*(d-x)*(e-x))-f",None)  # 400x^3/((x-20)(x+20)(x-40)(x+40))-20 rational
L17=Level(S17,P17,R17,G17,tb.coins_list17,Sc17,"Journey - Level 17","cubic & radical","sqrt(b^3+(x+c)^3)/d-a",None)                         # sqrt(200^3+(x+200)^3)/13-100          radical
L18=Level(S18,P18,R18,G18,tb.coins_list18,Sc18,"Journey - Level 18","parabolic & sinusoidal","x^2/c-a*sin(x/b)",None)                       # x^2/100-60sin(x/15)                   sinusoidal

tb.levels_list=[L0,L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,L13,L14,L15,L16,L17,L18]     # Get the list of all levels, for use later.

for obj in tb.levels_list:     # Get player's solution function for all levels, taken from json file. 
    obj.solution=data[obj.title][0]["solution"]



def graph_configurations(seed):
    """ Graph configurations function, called before starting each level/zen mode to set up the graph the same way  
    e.g., setup x/y axis, grid the graph etc.

    Args:
        seed (Class): Configures the graph creation based on the given seed.
    """    

    global canvas,ax,fig

    fig, ax = plt.subplots(figsize=(7, 7))    # Adjust the figure size to fit the screen well.

    img = mpimg.imread(os.getcwd() +r"\Images\level header.png")     # Reopen background image for the matplotlib canvas because canvases can't be transparent for whatever reason.
    fig.figimage(img,xo=-1,yo=-170,alpha=1,zorder=-10)     # Place the image, x coord is negative as image for whatever reason is offset a bit to the right. zorder to send background to back. 
    
    ax.set_aspect(aspect=1)     # Aspect ratio, larger number -> longer y axis.
    ax.grid(True, which='both')
    ax.spines['left'].set_position('zero')     # Set the ticks for x and y axis.
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()
    ax.spines['bottom'].set_position('zero')     # Center the spines.
    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()
    ax.minorticks_on()     # Give the minor axis. 
    ax.set_axisbelow(True)
    ax.set_xlabel('x', loc='right')     # Label x axis.
    ax.set_ylabel('y', loc='top')     # Label y axis.
    #ax.set_facecolor("lightblue")

    #plt.grid(visible=True, which='major', color='b', linestyle='-')     # Set gridlines. 
    plt.xlim(seed.domain_lower-0.2, seed.domain_upper+0.2)     # Domain and range of graph.
    plt.ylim(seed.range_lower-0.2,seed.range_upper+0.2)     # Additional offsets is so first and last gridlines won't get cutoff.
    plt.grid(visible=True, which='minor', color='#aeaeae', linestyle='-',linewidth=0.2)

    

def spawn_level_zen(event=None):
    """ Starts the zen mode by randomly generating the nodes -> coins, start/end points, redzone
    then updates the canvas

    Args:
        event (None): Defaults to None.
    """    

    global canvas,ax,fig,level

    if tb.music_toggle==True:     # Play music only if music is switched on in settings. 
        play_zenost_music()     # Play zen background music, stop josad ost soundtrack. 

    level=L0     # Zen level is L0. 
    
    spawn_zen_seed()     # Reespawn zen mode seed to generate new, different graph seed whenever user enters zen mode.
    spawn_zen_nodes()     # Respawn all nodes to generate new, different random positions whenever user enters zen mode. 
    spawn_zen_greenzone()     # Respawn greenzone for the newly randomly generated seed. (there is no spawn_zen_redzone as this line of code is right below, needs to specifically be programed so it doesn't spawn in the way of any of these already generated nodes/zones)
    L0.seed=S0;L0.coins=tb.coins_list0;L0.point=P0;L0.greenzone=G0       # Update L0 with these new configurations.

    graph_configurations(L0.seed)     # Go set the graph configurations for a typical math graph format with class: Seed 1 for zen mode.

    plot_all()     # Plot all the randomly generated nodes.

    '''
    Redzone 
    calling the spawn_redzone() function randomly spawns redzone
    while loop is true, it will check if any nodes are within the redzone, if it is, then keep looping until redzone spawns away from all nodes
    This section is specifically under the zen mode and not generalised for all modes including journey since journey won't have randomly spawning redzones so isn't worth bringing outside this function.
    '''
    global pointio;pointio=[L0.point] # temporary make the start node into a list to be able to combine it with coin list to be included for the calculation below.
    if R0.spawn==True:     
        loop=True
        while loop==True:     # Continuously spawn redzone randomly until it doesn't spawn on top of any nodes.
            loop=False
            spawn_redzone()     # Spawn redzone. 
            
            for obj in (L0.coins+pointio):     # If redzone crosses into coins or start node, then keep spawning new redzone. 
        
                if (R0.x0 <= obj.x_point <= R0.x1 and R0.y0 <= obj.y_point <= R0.y2) or (R0.y2 >= S0.range_upper) or (R0.x1 >= S0.domain_upper-horizontal_segment(20,S0)):     # If any coins or start point or greenzone are within the redzone area or redzone goes off the graph, respawn it.
                    loop=True
  
    
    '''
    Draw the red/greenzones onto graph, alpha is the opacity of the colours
    higher alpha (0.6) shows it has been crossed by user function,
    lower alpha (0.3) shows it hasn't
    '''
    tb.redzone_rectangle = Rectangle((R0.x0,R0.y0), R0.width, R0.height, linewidth=2,color='red', alpha=0.3)     # Draw the Redzone onto graph.
    ax.add_patch(tb.redzone_rectangle)    

    tb.greenzone_rectangle = Rectangle((G0.x0,G0.y0), G0.width, G0.height, linewidth=2,color='green', alpha=0.3)     # Draw the Greenzone onto graph.
    ax.add_patch(tb.greenzone_rectangle)    

    canvas = FigureCanvasTkAgg(fig, master=root)    # Create a canvas and add the plot to it.'
    canvas.get_tk_widget().place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=0)     # Place the graph canvas accordingly.
    
    canvas.draw()     # Draw the canvas.

    main(level)     # Initiate the level. 


def spawn_level(initial_level):     
    """ Spawn the levels for journey mode.

    Args:
        initial_level (Class): Spawns the level from the given level class.
    """    
    global canvas,ax,fig,level

    level=initial_level     # Set the level to the initial level.

    graph_configurations(level.seed)     # Go set the graph configurations for a typical math graph format with class: Seed n for journey mode level n.

    plot_nodes(level.point,"right",1,'x',"blue","Start",15,5,level)  # Plot start node of journey level n.

    journey_coins_chance(level)     # Respawn the chances of the coins spawning. 

    if level == L1 or level == L2:     # First 2 levels don't have redzones, so don't spawn any. 
        pass
    else:
      
        tb.redzone_rectangle = Rectangle((level.redzone.x0,level.redzone.y0), level.redzone.width, level.redzone.height, linewidth=2,color='red', alpha=0.3)    # Draw redzone onto graph.
        ax.add_patch(tb.redzone_rectangle)  

    tb.greenzone_rectangle = Rectangle((level.greenzone.x0,level.greenzone.y0), level.greenzone.width, level.greenzone.height, linewidth=2,color='green', alpha=0.3)     # Draw the Greenzone onto graph.
    ax.add_patch(tb.greenzone_rectangle)    

    canvas = FigureCanvasTkAgg(fig, master=root)    # Create a canvas and add the plot to it.
    canvas.get_tk_widget().place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=0)     # Place the graph canvas accordingly. 
    canvas.draw()

    main(level)     # Take player to main, where they interact with the graph.


def tutorial_popup(level):
    """ Gives player an instructions page on the side of level 1 or 2."""   
    global tutorial_top

    tutorial_top=Toplevel()   # Details for the tutorial window. 
    tutorial_top.geometry("575x990+"+str(tb.WINDOW_HORIZONTAL_OFFSET+870)+"+60")     # Make this window open next to the main one.
    tutorial_top.resizable(0,0)
    tutorial_top.overrideredirect(True)     # Stop player from manipulating this window.
    tutorial_top.attributes('-topmost', True)     # Make this window appear in front.

    tutorial_top_canvas=Canvas(tutorial_top,bg="#f8eeda",height=1000,width=700, bd=0, highlightthickness=0)     # Canvas frame over tutorial window.
    tutorial_top_canvas.place(x=0,y=0)

    if level==L1:       # Background for tutorial 1 if player is on level 1. 
        tutorial_image=tutorial1_background
    elif level==L2:      # Background for tutorial 2 if player is on level 2. 
        tutorial_image=tutorial2_background
    elif level==L3:      # Background for tutorial 3 if player is on level 3. 
        tutorial_image=tutorial3_background
    
    tutorial_top_canvas.create_image(0,0,image=tutorial_image,anchor='nw')   # display the tutorial instructions beside the main levels of 1, 2 and 3.



def graph_function(level): 
    """ Graph function, after calling the main where user does his inputs, this graphs the user function
    then calculates if graph has passed through start/end points, coins, redzones etc. colours the curve accordingly e.g., crossing redzone makes curve red
    updates and calculates user score and info, along with updating the title of f(x)
    first argument is on the seed specific to the mode/level chosen as drawing np.linespace needs to fit within the domain of this specific seed.
    *first part of this function also reconfigures necessary information back to inital e.g., coins collected resets to 0 before being recalculated, colours of red/greenzones get reset before being recalculated.

    Args:
        level (Class): Graphs the user function from the given level.

    Returns:
        Class: Returns the level class if player has accomplshed the level.
    """    
    
    global fig,goal_accomplished_top,canvas,user_function,draw_canvas,ax,hint_button,hint_icon,coordinates_icon,background_canvas


    for text in ax.texts:     # Remove coordinate text before reconfiguring them only the updated text appears. 
        text.remove()
   
    if goal_accomplished_top:     # Make sure only one of this top window apepars.
        goal_accomplished_top.destroy()

    
    if level==L1 or level==L2 or level==L3:     # If player is on level 1 or 2 of Journey, give them the tutorial page popup.
        tutorial_popup(level)



    
    if level==L0:     # If the mode is zen, then plot all the preset randomly generated nodes, including start and coin nodes.
        plot_all()     # Replot the nodes that way they get set back to their original colour and calculations recheck if user function passes through these nodes still. 
    else:     # If mode is journey, then plot the start node based off that level.
        plot_nodes(level.point,"right",1,'x',"blue","Start",15,5,level)   # Plot the start node for journey mode.

        for obj in level.coins:     # Plot the coins for journey mode, if its spawn is set to false, ignore this code.
            if obj.chance==True:
                plot_nodes(obj,"center",0,'o',"yellow","",30,1,level)     # Plot the coin.

        if level==L12 and C12_diamond.chance==True:     # If level is lvl 12 and chance of diamond spawning is true, plot it. 
            plot_nodes(C12_diamond,"center",0,'*',"#1e81b0","",40,1,level) 
           

    if level.redzone.spawn==True:     # If the level has no redzone, ignore this line of code. 
        tb.redzone_rectangle.set_alpha(0.3)     # Reconfigure zone rectangles to their original, more transparent colours. 
    tb.greenzone_rectangle.set_alpha(0.3)

    level.score_info.coins=0     # Update score by initially reconfiguring it back to 0.
    tb.points_intersection=0

    x = np.linspace(level.seed.domain_lower, level.seed.domain_upper, 300)     # Domain.
    
    if tb.invalid_input==True and (tb.show_hint==1 or tb.show_hint==2 or tb.show_coordinates==True):    
        user_function="987651"     # Exception for Specific case: Player makes invalid input and forces it and tries to display hint or coordinates, let player toggle hint/coords, but don't let the function pass through. 

   
    if 'x' not in user_function:     # Check if 'x' is in the user's function.
        y = [float(user_function) for _ in x]     # Create a constant function.
    else:
        y = eval(user_function)

        if level==L16 or level==L11 or level==L6:  # This line of code is specific to lvl 16 where dumbass matplotlib keeps graphing points of discontinuities for rational functions, this code says if the function's range exceeds the seed's vertical range by too much, then those values are replaced with +/-infinity which won't be plotted at all. 
            y[y>3*level.seed.range_upper] = np.inf;y[y<3*level.seed.range_lower] = -np.inf   


    if user_function !=str(987651):     # If the player hasn't inputted a function but this graph_function was called, it means he has either toggled coordinates or asked for hint, in which case don't increase tries by 1.
        level.score_info.tries+=1


    def function(input):     # treat user's function as a python function, brackets have been forced in because numpy cannot do bedmas. 
       return user_function.replace("x","("+input+")")
    
    
    def find_points_intersection(node,alignment,offset,label):
        '''
        This function checks to see if the curve of f(x) passes through the start and end points.
        Finds f(x), where x will range from the left-edge X-coordinate of point to the right-edge X-coordinate of point, increasing in 0.1 every time for increased accuracy.
        If at any point, f(x) falls between the lower Y-coordinate of point and upper Y-coordinate of point, then f(X) has 'passed through' this point.
        The division constant for horizontal_segment(division) is 675/32 which gives the relative width/height of the point. input here is 675/16 to get the halfway length from centre. 
        '''

        for i in range(int(round(-horizontal_segment(675/16,level.seed)*10)),int(round(horizontal_segment(675/16,level.seed)*10))):    # Check if the curve is in the vicinity of the x width of node.  
                
            try:
                if node.y_point-horizontal_segment(675/16,level.seed) <= eval(function(str(node.x_point+i/10))) <= node.y_point+horizontal_segment(675/16,level.seed):     # if curve passes through start and end points, make it green. 
                 
                    plot_nodes(node,str(alignment),offset,'x',"green",str(label),15,5,level)    # Plot start/end nodes, green.
            
                    tb.points_intersection+=1 
                    break
            except Exception:    # This occurs when e.g., f(x)=5/x, as function checks the value of f(0) will lead to division by zero. In this case, pass it.
                pass

            # Remember to put brackets around function argument because numpy doesn't do BEDMAS and will treat e.g.,  f(-x)=--x^2, not f(-x)=-(-x)^2.
    
               
    find_points_intersection(level.point,"right",1,"Start")

    
    def greenzone_intersection():
        '''
        sees if function passes through greenzone
        takes a range of inputs between the x-width of greenzone, inputs it into user function and sees if f(x) is between the greenzone's y-height
        if it is, the curve has 'crossed' the greenzone. 
        '''

        for i in range(0,int(round(horizontal_segment(20,level.seed)*10))):     # Check if the curve is in the vicinity of the x width of greenzone. 
            try:
                if level.seed.range_lower <=  eval(function(str(level.greenzone.x0+i/10))) <= level.seed.range_upper:
                    tb.greenzone_rectangle.set_alpha(0.6)     # Change greenzone colour to darker green once passed through.
                    tb.points_intersection+=1 
                    break
            except Exception:      # This occurs when e.g., f(x)=5/x, as function checks the value of f(0) will lead to division by zero. In this case, pass it.
                pass
            # Remember to put brackets around function argument because numpy doesn't do BEDMAS and will treat e.g.,  f(-x)=--x^2, not f(-x)=-(-x)^2.
    
    greenzone_intersection()


    def coins_intersection():    # Calculates to see if curve passes through any coins, description on how is in docstring below. 
        for obj in level.coins:     # If the coordinates of the coins pass through the function, the user has 'collected' it.
            
            if obj.chance==True:     # Only do this calculation if the coin has actually spawned. If it hasn't, then ignore this function. 
            
                for i in range(int(round(-horizontal_segment(26,level.seed)*10)),int(round(horizontal_segment(26,level.seed)*10))):    # Check if the curve is in the vicinity of the x width of coin. 
                    

                    '''
                    This function checks to see if the curve of f(x) passes through any coins.
                    Finds f(x), where x will range from the left-edge X-coordinate of coin to the right-edge X-coordinate of coin, increasing in 0.1 every time for increased accuracy.
                    If at any point, f(x) falls between the lower Y-coordinate of coin and upper Y-coordinate of coin, then f(X) has 'passed through' this coin.
                    The division constant for horizontal_segment(division) is 13.5 which gives the relative width/height of the point. input here is 26 to get the halfway length from centre. 
                    '''

                    try:   
                        if obj.y_point-horizontal_segment(26,level.seed) <= eval(function(str(obj.x_point+i/10))) <= obj.y_point+horizontal_segment(26,level.seed):
                            level.score_info.coins+=1      # Incease the coins counter by 1.
                            plot_nodes(obj,"center",0,'o',"green","",30,5,level)     # Make coin green to show its been picked up.
                            
                            if obj==C12_diamond and C12_diamond.chance==True and level==L12:     # If level is lvl12 and chance of diamond spawning is true and curve has crossed it, plot it. 
                        
                                tb.diamond=True     # Keep track that player has collected diamond.
                                plot_nodes(C12_diamond,"center",0,'*',"yellow","",40,0,level) 
                                
                            break
                        
                    except Exception:     # This occurs when e.g., f(x)=5/x, as function checks the value of f(0) will lead to division by zero. In this case, pass it. 
                        pass   #28cos((x+pi)/4)

                    # Remember to put brackets around function argument because numpy doesn't do BEDMAS and will treat e.g.,  f(-x)=--x^2, not f(-x)=-(-x)^2.
                    

    coins_intersection()
    
    try:     # Remove previous curve such that only the current one is showing on graph.
        tb.function_curve.pop(0).remove()
    except Exception:
        pass
    
    '''
    Redzone_intersection, functions similarly to previous greenzone_intersection
    '''
    def redzone_intersection():     # Check if function crosses redzone.
        
        for i in range(level.redzone.x0*10,level.redzone.x1*10):     # Checks for x values within the width of redzone.
            try:
                if level.redzone.y0 <= eval(function(str(i/10))) <= level.redzone.y2:     # If f(x-values) is between the height of the redzone, it means f(x) has crossed it.
                    tb.redzone_rectangle.set_alpha(0.6)     # Change redzone colour to darker green once passed through.
                    level.score_info.penalty="Penalty for Crossing Redzone"     # Player gets penalised.
                    break
                else:
                    level.score_info.penalty="No Penalty!"     # If f(x) doesn't cross redzone, he doesn't get penalised. 
            except Exception:     # Try statement occurs when function divided by 0 for inputs, in this case, ignore it and continue the calculation.
                pass

    if level.redzone.spawn==True:     # If this level has a redzone, then call this calculation function otherwise ignore it.
     
        redzone_intersection()

    if tb.points_intersection==2:     # Determines the colour of the curve based off the conditions.
        colour="green"
        level.score_info.goal="Goal: Accomplished!"     # Goal accomplished.
    elif level.score_info.penalty!="Penalty for Crossing Redzone":   
        colour="orange"
        level.score_info.goal="Goal: Not accomplished"     # Goal not accomplished.
    else:
        colour="red"  # Crossed redzone. 
            
    tb.function_curve=ax.plot(x, y, color=colour)      # Plot the function.
    
    tb.previous_score=data[level.title][0]["score"]      # Keep track of the player's previous score for use later on.

    tb.previous_score=level.score_info.score    # Store and keep track of the previous score for that level. 
    calculate_score(level)

    
    if tb.show_hint==1:     # If hint 1 is toggled on, display a small eye icon to show hint has been revealed.
        main_canvas.itemconfig(hint_icon,image=hint1_image)
    elif tb.show_hint==2:     # If hint 2 is toggled, display a small eye icon with a plus sign to show hint 2 has been revealed.
        main_canvas.itemconfig(hint_icon,image=hint2_image)
    else:      # If hint is off, remove this image. 
        main_canvas.itemconfig(hint_icon,image='')

    if tb.show_coordinates==True:     # If coordeinates if toggled on, display a small eye icon to show coordinates have been revealed.
        main_canvas.itemconfig(coordinates_icon,image=hint1_image)
    else:     # If coordinates are turned off, remove this image.
         main_canvas.itemconfig(coordinates_icon,image='')
        

    if level.title!="Zen":
        level_name=str(level.title)     # If the current level is a journey level, it's level name is just its level title e.g., Journey - level 5.
    else:
        level_name=str(level.title)+" - Round "+str(tb.L0_round)     # Otherwise if it's the zen mode, it's level name will be: Zen - Round {round number}.
   
    try:
        latex_expression="$"+latex(sympify(str(original_entry)))+"$"     # Converts user input to LaTeX expression.
        plt.title(str(level_name+'\nf(x) = '+latex_expression).replace("log","ln") ,pad=20)   # Add title and labels.    numpy treats log(x) as ln(x) ie. log_e(x), so replace this with ln(x) for proper notation.
    except Exception:
        plt.title(level_name+'\n',pad=20)      # If there is no function, make it blank.
    
    if tb.show_hint == 1:
        plt.title(level_name+'\nf(x) = '+level.hint,pad=20)     # If toggle hint is turned on, display it. 
    if tb.show_hint == 2:
        if level.title == "Zen":
            plt.title(str(level_name+'\nf(x) = (Hint unavailable)') ,pad=20)    # If it's zen mode, make 2nd hint just say 'hint unavailable' otherwise sympy tries to convert this string into an expression.
        else:
            plt.title(str(level_name+'\nf(x) = '+"$"+latex(sympify(str(level.hint2)))+"$").replace("log","ln") ,pad=20)     # If toggle 2nd hint is turned on, display it. 

    
    title_obj = plt.gca().title      # Change configurations of title to make it more aesthetically pleasing.
    title_obj.set_fontname('Comic Sans MS')
    title_obj.set_color('white')
    title_obj.set_fontweight("bold")

    if user_function == "987651" and tb.show_hint == 0:     # If player has just started the level ie. no function is showing in header (user function becomes 987651), make the level name larger.
        title_obj.set_fontsize(17)
    else:
        title_obj.set_fontsize(13)     # After player input, make the header smaller so as to make room to display user function in header.

    canvas.draw()

    if level.score_info.goal == "Goal: Accomplished!":     # If the player has won the round, take him to the won round window. 
        return goal_accomplished_window(level)



def error_check(event=None):
    """ Error check,
    when user graphs the function by clicking graph, this first converts user math notation to numpy notation e.g., 2^3 becomes 2**3
    then goes through error checking process of seeing if user function is valid for plotting before calling the graph_function() part

    Args:
        event (None): Defaults to None.

    Returns:
        Class: Returns the current level class.
    """    
    global user_function,ax,x,y,error_label,original_entry

    
    user_function = function_entry.get()      # Get user input as a function expression.
    original_entry = function_entry.get()     # Get a copy of the user's original input. 

    try:
       
        if not user_function:      # If input is blank, use for later as error.
            user_function="Tubicl-Oasis"
       
        user_function = re.sub(r'(\d+)([a-zA-Z_]+)', r'\1*\2', user_function)      # Substitute multiplication with * symbols for use in numpy.
        

        for i in [0,1,2,3,4,5,6,7,8,9,pi,e,"x"]:     # Ease of notation, e.g., 2*(x+3) -> 2(x+3)
            
            user_function=(
                user_function
                    .replace(str(i)+"(",str(i)+"*(")
                    .replace(")(",")*(")     # Ease of notation, e.g., (x+2)*(x-4) -> (x+2)(x-4)
            )


        original_entry=user_function     # obtains original entry by adding in necessary multiplicative operators.

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
                .replace("log","np.log")
                .replace("ln","np.log")
                .replace("pi", str(np.pi))     # Constants.
                .replace("e", str(np.e))
       )
        
        
        x = np.linspace(0,0,0)     # Test to see if user function is plottable for error checking before actually graphing it. 
        if 'x' not in user_function:  
            float(eval(user_function))     # Test to see if an unrecognised variable ie. variable other than x, is in user_function.     LINE STILL UNDER TESTING PRONE TO ERRORS
            y = [float(user_function) for _ in x]
            user_function=str(eval(user_function));original_entry=str(eval(original_entry))     # Occurs when user inputs e.g., 2+3, some reason this needs to be simplified first using eval(), then back to str().

        else:
            y = eval(user_function)


        error_label.config(text="")     # Clear error label, no error present. 

        tb.show_hint=0     # Reset hint counter back to 0 so user function gets displayed on header rather than the hint. 

        mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

        tb.invalid_input=False     # If code has passed all these calculations,  it means the user's function is valid. 
       
        return graph_function(level)     # Graph the function.
    

    except Exception:

        mixer.Sound.play(error_sfx)     # Error sound effect when user makes invalid input.  
        tb.invalid_input=True
       
        if user_function.count("(") != user_function.count(")"):
            error_label.config(text="Check all brackets have been closed.")     # Inform user their brackets have not been closed. 
        elif 'y' in str(user_function):
            error_label.config(text="Remember f(x) is a function of x.")     # Inform user they used y as their variable.
        elif user_function=="Tubicl-Oasis":
            error_label.config(text="f(x) has not been defined!")     # Inform user they haven't defined f(x).
        else:
            error_label.config(text="Invalid function, check notation.")     # Inform user they have not inputted a valid function.


def coordinates(event=None):
    """ When coordinate button is clicked, if it was shown, then hide it, vice versa.

    Args:
        event (None): Defaults to None.

    Returns:
        Class: Gives the current level class.
    """    
    
    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    if tb.show_coordinates==True:     # If coordinates was on, toggle it back off.
        tb.show_coordinates=False
    else:
        tb.show_coordinates=True     # If coordinates was off, toggle it on.

    return graph_function(level)     # Graph the function again.
    
 
def music(event=None):     
    """ When music button is toggled in settings, turn music on/off. 
    
    Args:
        event (None): Defaults to None.
    """

    global music_button,settings_menu_canvas

    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    if tb.music_toggle==True:     # If music was previously playing, turn it off.
        tb.music_toggle=False
       
        settings_menu_canvas.itemconfig(music_button,image=music_off_image)
        stop_background_music()     # Stop background music.
    else:
        tb.music_toggle=True     # If music was previously off, turn it on.
       
        settings_menu_canvas.itemconfig(music_button,image=music_on_image)
        play_josadost_music()     # Play background music.


def hint(event=None):
    """ When hint button is toggled: display hint1, hint2 or hide hint.
    
    Args:
        event (None): Defaults to None.

    Returns:
        Class: Gives the current level class.
    """
    global hint_button

    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    if tb.show_hint==0:
        tb.show_hint=1     # Hint button has been clicked, so display hint. 
    elif tb.show_hint==1:
        tb.show_hint=2     # If Hint button was clicked again, reveal the 2nd hint. 
    elif tb.show_hint==2:
        tb.show_hint=0     # If hint was previously displayed and player clicks for hint button, remove the hint.
    
    return graph_function(level)     # Graph the function again.
   

def difficulty(event=None):
    """ When player toggles difficulty in settings, switch from: Novice, Standard, Expert.
    
    Args:
        event (None): Defaults to None.
    """
    global difficulty_button,settings_menu_canvas

    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 
   
    if tb.game_difficulty=="Standard":     # Toggle through the 3 difficulties: NOVICE, STANDARD, EXPERT.
        settings_menu_canvas.itemconfig(difficulty_button,image=expert_image)
        tb.game_difficulty="Expert"
        data["Player"][0]["difficulty"]     # Game difficulty, taken from json file.
        tb.weights_true=1;tb.weights_false=2     # EXPERT mode: 1/3 chance coin spawns.

    elif tb.game_difficulty=="Expert":
        settings_menu_canvas.itemconfig(difficulty_button,image=novice_image)
        tb.game_difficulty="Novice"
        tb.weights_true=3;tb.weights_false=0     # NOVICE mode: 100% chance coin spawns.

    elif tb.game_difficulty=="Novice":
        settings_menu_canvas.itemconfig(difficulty_button,image=standard_image)
        tb.game_difficulty="Standard"
        tb.weights_true=2;tb.weights_false=1    # STANDARD mode: 2/3 chance coin spawns.
    
    data["Player"][0]["difficulty"]=tb.game_difficulty     # Update the game data for game difficulty.
    with open("game_data.json", "w") as f:     # Update this back to the original json file.
        json.dump(data, f, indent=4)
    

def new_player_window():     
    """ Have this window appear first to ask for player name in new game. """
   
    global name_entry,name_error,greet_label,new_player_top

    new_player_top=Toplevel()   # Details for the new player  window. 
    new_player_top.title("Greetings")
    new_player_top.geometry("918x430+"+str(tb.WINDOW_HORIZONTAL_OFFSET+00)+"+580")     # Make this window open next to the main one.
    new_player_top.resizable(0,0)
    new_player_top.overrideredirect(True)     # Stop player from manipulating this window.
    new_player_top.attributes('-topmost', True)     # Make this window appear in front.
    new_player_top.bind('<Return>',enter_name)     # When user presses enter, it automatically checks the name. 
   
    new_player_canvas=Canvas(new_player_top,height=440,width=918, bd=0, highlightthickness=0)     # Frame for top window.
    new_player_canvas.place(x=0,y=0)

    new_player_canvas.create_image(0,0,image=new_player_background,anchor='nw')     # Place the background image, grid pattern.

    name_entry=Entry(new_player_top,width=31,font=("Comic Sans MS", 23),fg="red",insertbackground='red',highlightthickness=0, borderwidth=0)     # Entry for player to enter their name. 
    name_entry.place(x=80,y=292)
    
    confirm_button=new_player_canvas.create_image(852,326,image=confirm_image,anchor="center")     # Button to 'sign up' new player. 
    new_player_canvas.tag_bind(confirm_button,"<Button-1>",enter_name)

    name_error=Label(new_player_top,text="",font=("Comic Sans MS", 10),fg="orange",bg="white")
    name_error.place(x=77,y=353)

    new_player_top.after(100, lambda: name_entry.focus_set())     # Automatically make player's cursor default onto the name entry. 
    

def goal_accomplished_window(level): 
    """ When the user wins the round ie. goal: accomplished, take him to this window.

    Args:
        level (Class): Gives the current level class. 
    """    
    global goal_accomplished_top,graph_button,main_canvas,coordinates_button,back_button,hint_button,tutorial_top
   
    mixer.Sound.play(level_complete_sfx)     # Sound effect when button is clicked. 

    main_canvas.tag_unbind(graph_button,"<Button-1>")
    main_canvas.tag_unbind(coordinates_button,"<Button-1>")
    #main_canvas.tag_unbind(back_button,"<Button-1>")
    function_entry["state"]="disabled"
    function_entry.configure(disabledbackground='white', disabledforeground='red')
    main_canvas.tag_unbind(hint_button,"<Button-1>")

    root.unbind('<Return>')     # Temporarily unbind user pressing enter to graph function, this will be rebinded when user leaves level.
  
    if level==L1 or level==L2 or level==L3:     # If the tutorial insrtuctions page image is showing, remove it. 
        destroy_all_top()      # Close the tutorial page.


    goal_accomplished_top=Toplevel()   # Details for the win window. 
    goal_accomplished_top.title("You won!")
    goal_accomplished_top.geometry("500x700+"+str(tb.WINDOW_HORIZONTAL_OFFSET+900)+"+50")     # Make this window open next to the main one.
    goal_accomplished_top.resizable(0,0)
    goal_accomplished_top.overrideredirect(True)     # Stop player from manipulating this window.
    goal_accomplished_top.attributes('-topmost', True)     # Make this window appear in front.
    
    top_canvas=Canvas(goal_accomplished_top,bg="#f8eeda",height=700,width=500, bd=0, highlightthickness=0)     # Canvas for level complete toplevel window. 
    top_canvas.place(x=0,y=0)

    top_canvas.create_image(0,0,image=level_complete_background,anchor='nw')     # Place the background image, grid pattern.

    close_button=top_canvas.create_image(127,665,image=close_image,anchor="center")      # Click this button to close level complete window.
    top_canvas.tag_bind(close_button,"<Button-1>",menu)

    if level != L0:
        if level in tb.levels_list1:      # If the player is in zen mode, then 'close' takes user back to home menu, if player is in journey mode, 'close' takes user back to journeys menu.
            top_canvas.tag_bind(close_button,"<Button-1>",journey_menu1)     # Specific journey mode menus e.g., if player has completed level 12 and hits close, he will be taken to journey menu 2.
        elif level in tb.levels_list2:
            top_canvas.tag_bind(close_button,"<Button-1>",journey_menu2)
        else:
            top_canvas.tag_bind(close_button,"<Button-1>",journey_menu3)


    top_canvas.create_text(395,270,text="+100",font=("Comic Sans MS", 22),anchor="w",fill="#97ff6c")     # Pass bonus text.
    top_canvas.create_text(395,340,text="+"+str(int(round(50/level.score_info.tries))),font=("Comic Sans MS", 22),anchor="w",fill="#97ff6c")     # Tries taken bonus text.
    top_canvas.create_text(395,407,text="+"+str(int(35*level.score_info.coins)),font=("Comic Sans MS", 22),anchor="w",fill="#97ff6c")     # Coins collected bonus text.
    
    top_canvas.create_text(280,340,text=str(level.score_info.tries),font=("Comic Sans MS", 22),anchor="w")     # Tries taken text.
    top_canvas.create_text(330,405,text=str(level.score_info.coins),font=("Comic Sans MS", 22))     # Coins collected text.

    penalty_label_text=top_canvas.create_text(220,473,text="none!",font=("Comic Sans MS", 22),anchor="w")     # Penalty label text.

    penalty_text=top_canvas.create_text(395,470,text="-0",font=("Comic Sans MS", 22),anchor="w",fill="orange")     # Penalty deduction text. 

    if level.score_info.penalty=="Penalty for Crossing Redzone":     # If user has crossed redzone, deduct points.
        
        top_canvas.itemconfig(penalty_text, text="-"+str(tb.score_no_penalty-level.score_info.score))     # Update penalty text if crossed redzone. 
        top_canvas.itemconfig(penalty_label_text, text="redzone")     

    final_score=calculate_score(level)

    if level==L12 and tb.diamond==True:     # If its lvl 12 and player has collected diamond, add bonus. 
        
        diamond_label=Label(goal_accomplished_top,text="Diamond: Collected!    +500",bg="white",fg="purple",font=("Comic Sans MS", 20))
        diamond_label.place(x=70,y=165)
        #diamond_bonus_label=Label(goal_accomplished_top,text="+555")
        #diamond_bonus_label.place(x=250,y=170)
        final_score+=555     # +555 points bonus.
        level.score_info.score+=555    # Update this to the score info for level 12.
        data["Achievements"][0]["6"]=True;tb.achievement_6=True     # Update this on json file, also locally.   

        if tb.achievement_6==False:     # Only notify user's new achievement unlocked if they haven't already unlocked it previously, if player's already found diamond, ignore this popup. 
            achievement_notification()     # popup notification notifying player he's unlocked achievement. 


    score_label=Label(goal_accomplished_top,text="FINAL SCORE: ")
    score_label.place(x=1400,y=200)
    score_label_bonus=Label(goal_accomplished_top,text=str(final_score))
    score_label_bonus.place(x=2500,y=200)

    top_canvas.create_text(418,540,text=str(final_score),font=("Comic Sans MS", 22,"bold"))     # Display final score.

    calculate_grade(level)

    grade_label=Label(goal_accomplished_top,text=level.score_info.grade,font='Helvetica 18 bold',fg="red")
    grade_label.place(x=2500,y=230)

    top_canvas.create_text(415,630,text=level.score_info.grade,font=("Comic Sans MS", 50),angle=30,fill="red")     # Display the grade. 
   
    close_button=Button(goal_accomplished_top,text="Save & close",command=menu)
    close_button.place(x=0,y=4000)
    
   
    if level==L0:      # If mode is zen, since it is infinite it calculates cumulative score, so first add the new score to the current cumulative score for the total.
       
        tb.L0_round+=1     # Increase zen mode rounds by +1. 
        tb.cumulative_L0_score=calculate_score(level)+tb.cumulative_L0_score 
      
        level.score_info.score=tb.cumulative_L0_score

        data["Zen"][0]["round"]=tb.L0_round     # Update the zen rounds count on the json file. 


    if level.score_info.score >= tb.previous_score:     # If the player's current score is larger than his previous score for that level, then store it (only keeps track of highscore, lower scores aren't kept).
        data[str(level.title)][0]["score"]=level.score_info.score     # Update the game data for the file.
        data[str(level.title)][0]["grade"]=level.score_info.grade    
        with open("game_data.json", "w") as f:     # Update this back to the original json file.
            json.dump(data, f, indent=4)
    else:     # If player's new score is not the highscore, then don't store it in json file, instead replace the data in json file (stored highscore) as the current score. 
        level.score_info.score=data[str(level.title)][0]["score"]
        level.score_info.grade=data[str(level.title)][0]["grade"]

    
    '''Achievement 2: finding peace'''
    if level==L0 and data["Zen"][0]["score"]>=1000 and tb.achievement_2==False:     # If cumulative score of zen mode passes 1000 and player has not previously unlocked it already, player unlocks Finding Peace achievement.
        tb.achievement_2=True     # Update achievement 2 to unlocked. 
        data["Achievements"][0]["2"]=True
        achievement_notification()     # popup notification notifying player he's unlocked achievement. 

    '''Achievement 4: achieving peace'''
    if level==L0 and data["Zen"][0]["score"]>=5000 and tb.achievement_4==False:     # If cumulative score of zen mode passes 5000 and player has not previously unlocked it already,  player unlocks Achieving Peace achievement. 
        tb.achievement_4=True     # Update achievement 4 to unlocked. 
        data["Achievements"][0]["4"]=True
        achievement_notification()     # popup notification notifying player he's unlocked achievement. 
    
    '''Achievement 7: eternal peace'''
    if level==L0 and data["Zen"][0]["score"]>=10000 and tb.achievement_7==False:     # If cumulative score of zen mode passes 10000 and player has not previously unlocked it already,  player unlocks Achieving Peace achievement. 
        tb.achievement_7=True     # Update achievement 7 to unlocked. 
        data["Achievements"][0]["7"]=True
        achievement_notification()     # popup notification notifying player he's unlocked achievement. 

    '''Achievement 1: Graph Master'''
    global key
    tb.graph_master=True
    if tb.achievement_1==False:     # Only check if eligible for graph master achievement if player hasn't previous unlocked it already.
        for key, value in data.items():
            if key.startswith("Journey - Level"):     # (excludes zen mode.) 
                for item in value:     # Checks all "score" values from all 18 journey levels, if one of them is 0 ie. player hasn't tried it, then tb.graph_master=False (not eligible).
                    if "score" in item and item["score"]==0:
                        tb.graph_master=False

        if tb.graph_master==True:     # If none of player's scores are 0 ie. player's tried all levels, give him achievement 1. 
            tb.achievement_1=True
            data["Achievements"][0]["1"]=True
            achievement_notification()
    
    '''Achievement 5: Ace'''
    tb.ace=True
    if tb.achievement_5==False:     # Only check if eligible for graph master achievement if player hasn't previous unlocked it already.
        for key, value in data.items():
            if key.startswith("Journey - Level"):     # (excludes zen mode.) 
                for item in value:     # Checks all "grade" values from all 18 journey levels, if one of them is not A+, then tb.ace=False (not eligible).
                    if item["grade"]!="A+":
                        tb.ace=False

        if tb.ace==True:     # If all of player's grades are A+, give him achievement 5. 
            tb.achievement_5=True
            data["Achievements"][0]["5"]=True
            achievement_notification()
    
    '''Achievement 3: Functions Expert'''
    total_score=0
    if tb.achievement_3==False:     # Only check if eligible for graph master achievement if player hasn't previous unlocked it already.
        for key, value in data.items():
            if key.startswith("Journey"):
                total_score += value[0]["score"]     # Sum up all scores from all 18 journey levels.

        if total_score > 3000:     # If sum of score exceeds 3000, give him achievement 3. 
           tb.achievement_3=True
           data["Achievements"][0]["3"]=True
           achievement_notification()
    
    '''Achievement 8: Minimalist'''
    level.solution=str(user_function)     # Store user's solution function into level's solution attribute. 
    data[str(level.title)][0]["solution"]=level.solution     # Store this in json file.

    tb.linear=True
    for key, value in data.items():
        if key.startswith("Journey - Level"):     # (excludes zen mode.) 
            for item in value:    
                try:      # First sympifies all solution strings in journey mode so it can be used in sympy, replaces variable 'x' with variable 'y' as x already exists previously as a list of floats. then the sympy degree function is used to check the degree of the function. If degree isn't 1 or 0, it's not linear. 
                    if degree(sp.sympify(item["solution"].replace("x","q")),gen=q)!=1 and degree(sp.sympify(item["solution"].replace("x","q")),gen=q)!=0 and degree(sp.sympify(item["solution"].replace("x","q")),gen=q)!=-oo:     # For some reason degree of f(x)=0 is -infinity using sympy, so have to account for that.
                        tb.linear=False
                except Exception:     # Not all functions returns a degree e.g., sin(x), which produces an error, if this happens the function is also not linear. 
                    tb.linear=False
    
    if tb.achievement_1==True and tb.linear==True and tb.achievement_8==False:     # If player has tried all levels and has only used linear functions and hasn't previously unlocked achievement 8 already, give him achievement 8.
        tb.achievement_8=True
        data["Achievements"][0]["8"]=True
        achievement_notification()    
    
    with open("game_data.json", "w") as f:     # Update this back to the original json file.
        json.dump(data, f, indent=4)

    
def quit_game(event=None):     # Quit game.
    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 
    time.sleep(0.2)
    root.destroy()


def enter_name(event=None):
    """When player enters the game for the first time/without an account, they will be asked to give their name.

    Args:
        event (None): Defaults to None.
    """    
    global name_entry,name_error,greet_label,journey_button,zen_button,menu_canvas
   
    tb.name=name_entry.get()     # Extract user name as a variable.

    if not tb.name or tb.name.isspace()==True:     # If player inputs blank spaces, it's not allowed.
        name_error.config(text="Blank names aren't allowed!")

        mixer.Sound.play(error_sfx)     # Error sound effect when player makes an invalid name (no entry). 

    else:
        mixer.Sound.play(clicked_sfx)     # Error sound effect when player makes an invalid name (no entry). 

        if tb.name=="I am a cheater" and tb.achievement_9==False:     # If player inputs 'cheat code' and hasn't already unlocked achievement 9, unlock achievement 9.
            tb.achievement_9=True
            data["Achievements"][0]["9"]=True
            achievement_notification()
            with open("game_data.json", "w") as f:     # Update this back to the original json file.
                json.dump(data, f, indent=4)

        tb.name=tb.name.title()[:30]
        menu_canvas.tag_bind(journey_button,"<Button-1>",journey_menu1)     # Let player interact with the game modes now. 
        menu_canvas.tag_bind(zen_button,"<Button-1>",spawn_level_zen)

        if tb.achievement_9==True:
            max_save_data()     # If player has just inputted the 'cheat code', give him max save data. 

        data["Player"][0]["name"]=tb.name     # Update the game data to include player name.
        with open("game_data.json", "w") as f:     # Update this back to the original json file.
            json.dump(data, f, indent=4)

        menu()     # Go back to home menu. 
        
        
def reset_data_window(event=None):    
    """ Confirmation window for resetting data.

    Args:
        event (None): Defaults to None.
    """    
    global delete_top,music_button,delete_account_button,settings_menu_canvas
    
    settings_menu_canvas.tag_unbind(music_button,"<Button-1>")     # Disable these settings buttons to stop player from pressing these buttons when confirming data delete. 
    settings_menu_canvas.tag_unbind(delete_account_button, "<Button-1>")
    settings_menu_canvas.tag_unbind(difficulty_button, "<Button-1>")
    settings_menu_canvas.tag_unbind(difficulty_button, "<Escape>")
    
    delete_top=Toplevel()   # Details for the win window. 
    delete_top.title("DELETE ACCOUNT")
    delete_top.geometry("918x550+"+str(tb.WINDOW_HORIZONTAL_OFFSET+00)+"+300")     # Make this window open next to the main one.
    delete_top.resizable(0,0)
    delete_top.overrideredirect(True)     # Stop player from manipulating this window.
    delete_top.attributes('-topmost', True)     # Make this window appear in front.

    delete_canvas=Canvas(delete_top,bg="#f8eeda",height=630,width=918, bd=0, highlightthickness=0)     # Canvas for delete account window. 
    delete_canvas.place(x=0,y=0)
    
    delete_canvas.create_image(0,0,image=delete_account_background,anchor='nw')     # Place the background image.

    delete_button=delete_canvas.create_image(200,450,image=delete_image,anchor="center")      # Click this button tdelete account, reset data.
    delete_canvas.tag_bind(delete_button,"<Button-1>",reset_data)

    cancel_button=delete_canvas.create_image(735,450,image=cancel_image,anchor="center")      # Click this button cancel action and go back to settings.
    delete_canvas.tag_bind(cancel_button,"<Button-1>",settings_menu)


def max_save_data():     # Give player max save file in json.
    # Replace current json file storing player info with this default info.
    max_data ={
        "Player": [
            {
                "name": "Cheater 🤡",
                "difficulty": "Expert"
            }
        ],
        "Achievements": [
            {
                "1": True,
                "2": True,
                "3": True,
                "4": True,
                "5": True,
                "6": True,
                "7": True,
                "8": True,
                "9": True
            }
        ],
        "Zen": [
            {
                "score": 999999,
                "grade": "A+",
                "solution": "x",
                "round": 9999
            }
        ],
        "Journey - Level 1": [
            {
                "score": 185,
                "grade": "A+",
                "solution": "x"
            }
        ],
        "Journey - Level 2": [
            {
                "score": 220,
                "grade": "A+",
                "solution": "-x+11"
            }
        ],
        "Journey - Level 3": [
            {
                "score": 220,
                "grade": "A+",
                "solution": "2/3*x-4"
            }
        ],
        "Journey - Level 4": [
            {
                "score": 255,
                "grade": "A+",
                "solution": "1/5*x**2-9"
            }
        ],
        "Journey - Level 5": [
            {
                "score": 255,
                "grade": "A+",
                "solution": "1.2**x"
            }
        ],
        "Journey - Level 6": [
            {
                "score": 220,
                "grade": "A+",
                "solution": "20/x"
            }
        ],
        "Journey - Level 7": [
            {
                "score": 255,
                "grade": "A+",
                "solution": "5*np.sqrt(x)"
            }
        ],
        "Journey - Level 8": [
            {
                "score": 255,
                "grade": "A+",
                "solution": " -x**3/72+2*x"
            }
        ],
        "Journey - Level 9": [
            {
                "score": 290,
                "grade": "A+",
                "solution": "6*np.log(x+80)"
            }
        ],
        "Journey - Level 10": [
            {
                "score": 290,
                "grade": "A+",
                "solution": "80*(1.1)**(-x**2/30)"
            }
        ],
        "Journey - Level 11": [
            {
                "score": 290,
                "grade": "A+",
                "solution": "10*x**2/((x+100)*(x+10))"
            }
        ],
        "Journey - Level 12": [
            {
                "score": 915,
                "grade": "A+",
                "solution": " 28*np.cos((x+np.pi)/4"
            }
        ],
        "Journey - Level 13": [
            {
                "score": 325,
                "grade": "A+",
                "solution": "2*np.sqrt(x**2-100)-80"
            }
        ],
        "Journey - Level 14": [
            {
                "score": 325,
                "grade": "A+",
                "solution": "(x+70)*(x+10)*(x-20)*(x-60)/80000"
            }
        ],
        "Journey - Level 15": [
            {
                "score": 325,
                "grade": "A+",
                "solution": "2300*np.sin(x/10-6)/(60-x)+120"
            }
        ],
        "Journey - Level 16": [
            {
                "score": 325,
                "grade": "A+",
                "solution": "400*x**3/((x-20)*(x+20)*(x-40)*(x+40))-20"
            }
        ],
        "Journey - Level 17": [
            {
                "score": 325,
                "grade": "A+",
                "solution": "np.sqrt(200**3+(x+200)**3)/13-100"
            }
        ],
        "Journey - Level 18": [
            {
                "score": 325,
                "grade": "A+",
                "solution": "x**2/100-60*np.sin(x/15)"
            }
        ]
    }

    with open("game_data.json","w") as f_write:     # Open up the json file containing player data.
       
        f_write.truncate(0)     # Clear current player data.
        json.dump(max_data,f_write,indent=4)     # Replace with max player data. 
   
    root.destroy()     # Close program.
    exit()
  


def reset_data(event=None):     # Reset game data by resetting json file back to original. 
    # Replace current json file storing player info with this default info.
    default_data ={    
        "Player": [
            {
                "name": "",
                "difficulty": "Standard"
            }
        ],
        "Achievements": [
            {
                "1": False,
                "2": False,
                "3": False,
                "4": False,
                "5": False,
                "6": False,
                "7": False,
                "8": False,
                "9": False
            }
        ],  
        "Zen": [
            {
                "score": 0,
                "grade": "",
                "solution": "",
                "round": 1
            }
        ],
        "Journey - Level 1": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 2": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 3": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 4": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 5": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 6": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 7": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 8": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 9": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 10": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 11": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 12": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 13": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 14": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 15": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 16": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 17": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ],
        "Journey - Level 18": [
            {
                "score": 0,
                "grade": "",
                "solution": ""
            }
        ]
    }

    with open("game_data.json","w") as f_write:     # Open up the json file containing player data.
       
        f_write.truncate(0)     # Clear current player data.
        json.dump(default_data,f_write,indent=4)     # Replace with original, empty new fresh data.


    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 
    time.sleep(0.2)
    root.destroy()     # Close program.


def destroy_all_top():     # Quick function call when necessary. 

    for widget in root.winfo_children():     # Destroy previous top windows to ensure only 1 appears at once.
        if isinstance(widget,Toplevel):
            widget.destroy()


def main(level):    
    """main, where the main user inputs are done here including buttons, info e.g., tries, points, and input box for user to enter function

    Args:
        level (Class): Gives the current level class.
    """    
    global function_entry,error_label,user_function,original_entry,hint_icon,coordinates_icon,graph_button,back_button,hint_button,coordinates_button,main_canvas

    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 
    
    tb.invalid_input=False     # Set the variable back to false; player hasn't inputted anything initially. 

    ex=860     # Constant too keep vertical coordinate of widgets in line.


    main_canvas=Canvas(root,bg="#f8eeda",height=400,width=880, bd=0, highlightthickness=0)     # Canvas for main window in levels.
    main_canvas.place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=798)
    #(x=0,y=800)
    
    main_canvas.create_image(0,0,image=level_background,anchor='nw')     # Place the background image.

    back_button=main_canvas.create_image(772,208,image=back_image,anchor="center")      # Click this button to initiate the journey level.
    main_canvas.tag_bind(back_button,"<Button-1>",menu)

    hint_button=main_canvas.create_image(500,206,image=hint_image,anchor="center")      # Click this button to give a hint.
    main_canvas.tag_bind(hint_button,"<Button-1>",hint)
    root.bind('<Control-h>', hint)     # Keyboard shortcut; when player clicks ctrl+h, it toggles the hint button.
   
    hint_icon=main_canvas.create_image(560,190,image=None,anchor="center")     # Hint 1 on icon.
    coordinates_icon=main_canvas.create_image(367,190,image=None,anchor="center")     # Hint 1 on coordinates icon.
    

    coordinates_button=main_canvas.create_image(300,206,image=coordinates_image,anchor="center")      # Click this button to go back to journey menu.
    main_canvas.tag_bind(coordinates_button,"<Button-1>",coordinates)
    root.bind('<Control-c>', coordinates)     # Keyboard shortcut; when player clicks ctrl+escape, it toggles the coordinates


    graph_button=main_canvas.create_image(745,140,image=graph_image,anchor="center")      # Click this button to graph function.
    main_canvas.tag_bind(graph_button,"<Button-1>",error_check)

    action=menu
    if level != L0:
        if level in tb.levels_list1:      # If the player is in zen mode, then 'back' takes user back to home menu, if player is in journey mode, 'back' takes user back to journeys menu.
            action=journey_menu1
            main_canvas.tag_bind(back_button,"<Button-1>",journey_menu1)     # Specific journey mode menus e.g., if player was in level 12 and hits back, he will be taken to journey menu 2.
        elif level in tb.levels_list2:
            action=journey_menu2
            main_canvas.tag_bind(back_button,"<Button-1>",journey_menu2)
        else:
            action=journey_menu3
            main_canvas.tag_bind(back_button,"<Button-1>",journey_menu3)


    function_entry=Entry(root,width=16,font=("Comic Sans MS", 25),fg="red",insertbackground='red',highlightthickness=0, borderwidth=0)     # Insert background makes the cursor red by defualt.
    function_entry.place(x=240+tb.WINDOW_HORIZONTAL_OFFSET,y=898)
    function_entry.focus_set()     # Have cursor automatically be placed in this entry box.


    if level.title=="Zen":     # zen mdoe is randomly generated levels so has no predetermined hint.
        #hint_button["state"]="disabled"
        pass

    error_label=Label(root,text="",fg="orange",font=("Comic Sans MS",10),bg="white") 
    error_label.place(x=135+tb.WINDOW_HORIZONTAL_OFFSET,y=880)
    

    user_function=str(987651)     # make the original user function 'blank' to draw the grpah but avoid math errors for undefined function.
    original_entry=""     
    
    graph_function(level)    

    root.bind('<Return>',error_check)     # When user presses enter, it automatically graphs the function (graph button).
    root.bind('<Escape>', action)     # When user presses escape, it returns him back to the previous menu (back button).
    root.unbind('<Left>')
    root.unbind('<Right>')


def journey_level_info(level):     # Quick function to simplify writing level infos on journey menus 1 and 2 e.g., level 1, highscore: 180, A+ etc.
    return "\nhighscore: "+str(level.score_info.score)+"\n"+str(level.score_info.grade)


def get_grade_image(level):     # Give the canvas image for the grade the player got for that level.
    if level.score_info.grade=="A+":     # If player got this grade, display A+.
        return Amax_image
    elif level.score_info.grade=="A":     # If player got this grade, display A.
        return A_image
    elif level.score_info.grade=="B":     # If player got this grade, display B.
        return B_image 
    elif level.score_info.grade=="C":     # If player got this grade, display C.
        return C_image 
    elif level.score_info.grade=="D":     # If player got this grade, display D.
        return D_image 
    elif level.score_info.grade=="F":     # If player got this grade, display F.
        return F_image 
    else:
        return None     # It there is no grade, don't display any image. 


'''Quick function to place the journey buttons in journey menus and their highscores and grade all at once.'''
def place_journey_level(level,canvas,button):

    canvas.tag_bind(button,"<Button-1>",lambda event:spawn_level(level))      # Bind it to command to its corresponding level. 
    canvas.create_text(canvas.coords(button)[0]-2,canvas.coords(button)[1]+49,text=level.score_info.score,anchor="w",font=("Comic Sans MS",15),fill="orange")      # Create the highscore label, placed in coordinates relative to the button. 
    canvas.create_image(canvas.coords(button)[0]+103,canvas.coords(button)[1]+70,image=get_grade_image(level),anchor="center")     # Place the grade image the player got as an image. 
   

'''Level Lock/Unlock System for 3 journey menus.'''
def level_lock_system(canvas,buttons_list,levels_list,images_list,first_level,last_level,cl_first_level,d):

    for i in buttons_list:     # Start with making all buttons disabled.
        canvas.tag_unbind(i,"<Button-1>")
        canvas.itemconfig(i,image=locked_image)     # Replace the image with a locked level. 

    if first_level!=1:     # Only do this part of code if menu is in 2 or 3, since there is no previous level before level 1 in menu 1. 
        if data["Journey - Level "+str(first_level-1)][0]["score"]!=0:     # If previous level has been tried (back in previous journey level menu), then unlock the first level of this journey level menu. 
            canvas.tag_bind(buttons_list[0],"<Button-1>", lambda event: spawn_level(cl_first_level))
            canvas.itemconfig(buttons_list[0],image=images_list[0])
    if first_level==1:
        canvas.tag_bind(buttons_list[0],"<Button-1>", lambda event: spawn_level(cl_first_level))
        canvas.itemconfig(buttons_list[0],image=level1_image)     # If player is on menu 1, always make level 1 unlocked by default, replace it with the normal, unlocked image. 
       
    for i in range(first_level,last_level):     # Go through all journey levels, if score for this level isn't 0 ie. player has tried the level, 'unlock' the next 2 proceeding levels for the player. 
        if data["Journey - Level "+str(i)][0]["score"]!=0:
            try:
                for j in range(0,2):     # Unlock the proceeding 2 levels after the level the player has just unlocked. 
                    canvas.tag_bind(buttons_list[i-d+j],"<Button-1>",lambda event,level=levels_list[i-d+j]: spawn_level(level))
                    canvas.itemconfig(buttons_list[i-d+j],image=images_list[i-d+j])     # Replace image with the corresponding unlocked, normal image.
            except IndexError:     # When player gets up to e.g., level 17, then: level 18 and 'level 19' will be unlocked. There is no level 19 so index error, which is fine.  
                pass


def toggle_tools_off():     # If player had previously turned tools on in a level and left, then these tools should be reset back to default (off).
    tb.show_coordinates=False     # Turn show coordinates and show hint back off when player leaves level.
    tb.show_hint=0
    

def journey_menu1(event=None):
    """ Mennu 1 to select journey levels

    Args:
        event (None): Defaults to None.
    """    
    
    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    plt.close()     # Close previous graph. 


    for obj in tb.levels_list:      # Reset tries counter back to 0 when user finishes level and returns to menu.
        obj.score_info.tries=0

    toggle_tools_off()     # Turn all tools back off.
    
    destroy_all_top()      # Destroys all previous toplevel windows if opened, such as achievement notifications etc.


    journey_menu_canvas1=Canvas(root,bg="#f8eeda",height=1040,width=880, bd=0, highlightthickness=0)     # New frame over the original menu frame.
    journey_menu_canvas1.place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=0)

    journey_menu_canvas1.create_image(0,0,image=level_menu_background,anchor="nw")     # Place the background image, grid pattern.


    '''Declare and spawn all journey levels in menu 1.'''
    level1=journey_menu_canvas1.create_image(281,268,image=level1_image,anchor="center")
    level2=journey_menu_canvas1.create_image(632,268,image=level2_image,anchor="center")  
    level3=journey_menu_canvas1.create_image(281,463,image=level3_image,anchor="center")  
    level4=journey_menu_canvas1.create_image(632,463,image=level4_image,anchor="center")  
    level5=journey_menu_canvas1.create_image(281,658,image=level5_image,anchor="center")  
    level6=journey_menu_canvas1.create_image(632,658,image=level6_image,anchor="center")  

    place_journey_level(L1,journey_menu_canvas1,level1)
    place_journey_level(L2,journey_menu_canvas1,level2)
    place_journey_level(L3,journey_menu_canvas1,level3)
    place_journey_level(L4,journey_menu_canvas1,level4)
    place_journey_level(L5,journey_menu_canvas1,level5)
    place_journey_level(L6,journey_menu_canvas1,level6)

    
    next_button=journey_menu_canvas1.create_image(710,842,image=next_image,anchor="center")     # Button to take player to next level selection menu. 
    journey_menu_canvas1.tag_bind(next_button,"<Button-1>",journey_menu2)
    root.bind('<Right>', journey_menu2)     # Keyboard shortcut; when player presses right arrow key, it navigates to next selection menu. 

    back_button=journey_menu_canvas1.create_image(770,970,image=back_image,anchor="center")     # Button to take player back to main menu. 
    journey_menu_canvas1.tag_bind(back_button,"<Button-1>",menu)
    root.bind('<Escape>', menu)     # Keyboard shortcut; when player clicks escape, it returns them back to the previous menu (back button).


    '''Level Lock/Unlock for journey menu 1'''
    tb.buttons_list1=[level1,level2,level3,level4,level5,level6]
    tb.levels_list1=[L1,L2,L3,L4,L5,L6]
    tb.images_list1=[level1_image,level2_image,level3_image,level4_image,level5_image,level6_image]
    level_lock_system(journey_menu_canvas1,tb.buttons_list1,tb.levels_list1,tb.images_list1,1,6,L1,0)    



def journey_menu2(event=None):
    """ Mennu 2 to select journey levels

    Args:
        event (None): Defaults to None.
    """    
   
    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    plt.close()     # Close previous graph. 

    for obj in tb.levels_list:      # Reset tries counter back to 0 when user finishes level and returns to menu. 
        obj.score_info.tries=0

    toggle_tools_off()     # Turn all tools back off.
    
    destroy_all_top()      # Destroys all previous toplevel windows if opened, such as achievement notifications etc.
    
    
    journey_menu_canvas2=Canvas(root,bg="#f8eeda",height=1040,width=880, bd=0, highlightthickness=0)     # New frame over the original menu frame.
    journey_menu_canvas2.place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=0)

    journey_menu_canvas2.create_image(0,0,image=level_menu_background,anchor='nw')     # Place the background image, grid pattern.
    

    '''Declare and spawn all journey levels in menu 2.'''
    level7=journey_menu_canvas2.create_image(281,268,image=level7_image,anchor="center")
    level8=journey_menu_canvas2.create_image(632,268,image=level8_image,anchor="center")  
    level9=journey_menu_canvas2.create_image(281,463,image=level9_image,anchor="center")  
    level10=journey_menu_canvas2.create_image(632,463,image=level10_image,anchor="center")  
    level11=journey_menu_canvas2.create_image(281,658,image=level11_image,anchor="center")  
    level12=journey_menu_canvas2.create_image(632,658,image=level12_image,anchor="center")  

    place_journey_level(L7,journey_menu_canvas2,level7)
    place_journey_level(L8,journey_menu_canvas2,level8)
    place_journey_level(L9,journey_menu_canvas2,level9)
    place_journey_level(L10,journey_menu_canvas2,level10)
    place_journey_level(L11,journey_menu_canvas2,level11)
    place_journey_level(L12,journey_menu_canvas2,level12)


    previous_button=journey_menu_canvas2.create_image(213,842,image=previous_image,anchor="center")     # Button to take player to previous level selection menu (2). 
    journey_menu_canvas2.tag_bind(previous_button,"<Button-1>",journey_menu1)
    root.bind('<Left>', journey_menu1)     # Keyboard shortcut; when player presses left arrow key, it navigates to previous selection menu. 


    next_button=journey_menu_canvas2.create_image(710,842,image=next_image,anchor="center")     # Button to take player to next level selection menu (3). 
    journey_menu_canvas2.tag_bind(next_button,"<Button-1>",journey_menu3)
    root.bind('<Right>', journey_menu3)     # Keyboard shortcut; when player presses right arrow key, it navigates to next selection menu. 


    back_button=journey_menu_canvas2.create_image(770,970,image=back_image,anchor="center")     # Button to take player back to main menu. 
    journey_menu_canvas2.tag_bind(back_button,"<Button-1>",menu)
    root.bind('<Escape>', menu)     # Keyboard shortcut; when player clicks escape, it returns them back to the previous menu (back button).


    '''Level Lock/Unlock System for journey menu 2'''
    tb.buttons_list2=[level7,level8,level9,level10,level11,level12]
    tb.levels_list2=[L7,L8,L9,L10,L11,L12]
    tb.images_list2=[level7_image,level8_image,level9_image,level10_image,level11_image,level12_image]
    level_lock_system(journey_menu_canvas2,tb.buttons_list2,tb.levels_list2,tb.images_list2,7,12,L7,6)



def journey_menu3(event=None):
    """ Mennu 3 to select journey levels

    Args:
        event (None): Defaults to None.
    """    
   
    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    plt.close()     # Close previous graph. 


    for obj in tb.levels_list:      # Reset tries counter back to 0 when user finishes level and returns to menu.
        obj.score_info.tries=0
   
    toggle_tools_off()     # Turn all tools back off.
    
    destroy_all_top()      # Destroys all previous toplevel windows if opened, such as achievement notifications etc.


    journey_menu_canvas3=Canvas(root,bg="#f8eeda",height=1040,width=880, bd=0, highlightthickness=0)     # New frame over the original menu frame.
    journey_menu_canvas3.place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=0)

    journey_menu_canvas3.create_image(0,0,image=level_menu_background,anchor="nw")     # Place the background image, grid pattern.


    '''Declare and spawn all journey levels in menu 3.'''
    level13=journey_menu_canvas3.create_image(281,268,image=level13_image,anchor="center")
    level14=journey_menu_canvas3.create_image(632,268,image=level14_image,anchor="center")  
    level15=journey_menu_canvas3.create_image(281,463,image=level15_image,anchor="center")  
    level16=journey_menu_canvas3.create_image(632,463,image=level16_image,anchor="center")  
    level17=journey_menu_canvas3.create_image(281,658,image=level17_image,anchor="center")  
    level18=journey_menu_canvas3.create_image(632,658,image=level18_image,anchor="center")  

    place_journey_level(L13,journey_menu_canvas3,level13)
    place_journey_level(L14,journey_menu_canvas3,level14)
    place_journey_level(L15,journey_menu_canvas3,level15)
    place_journey_level(L16,journey_menu_canvas3,level16)
    place_journey_level(L17,journey_menu_canvas3,level17)
    place_journey_level(L18,journey_menu_canvas3,level18)


    previous_button=journey_menu_canvas3.create_image(213,842,image=previous_image,anchor="center")     # Button to take player to previous level selection menu (2). 
    journey_menu_canvas3.tag_bind(previous_button,"<Button-1>",journey_menu2)
    root.bind('<Left>', journey_menu2)     # Keyboard shortcut; when player presses left arrow key, it navigates to previous selection menu. 


    back_button=journey_menu_canvas3.create_image(770,970,image=back_image,anchor="center")     # Button to take player back to main menu. 
    journey_menu_canvas3.tag_bind(back_button,"<Button-1>",menu)
    root.bind('<Escape>', menu)     # Keyboard shortcut; when player clicks escape, it returns them back to the previous menu (back button).

    '''Level Lock/Unlock System for journey menu 3'''
    tb.buttons_list3=[level13,level14,level15,level16,level17,level18]
    tb.levels_list3=[L13,L14,L15,L16,L17,L18]
    tb.images_list3=[level13_image,level14_image,level15_image,level16_image,level17_image,level18_image]
    level_lock_system(journey_menu_canvas3,tb.buttons_list3,tb.levels_list3,tb.images_list3,13,18,L13,12)
   
   

def settings_menu(event=None):
    """ Settings menu where player configures their: music, difficulty, account.

    Args:
        event (None): Defaults to None.
    """    
    global delete_top,music_button,delete_account_button,music_button,difficulty_button,settings_menu_canvas

    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    tb.game_difficulty=data["Player"][0]["difficulty"]     # Get game difficulty from json file. 

    if delete_top:     # Close delete account confirm window if previously opened and cancelled by player. 
        delete_top.destroy()

    settings_menu_canvas=Canvas(root,bg="#f8eeda",height=1040,width=880, bd=0, highlightthickness=0)     # Frame over settings menu window.
    settings_menu_canvas.place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=0)

    settings_menu_canvas.create_image(0,0,image=settings_menu_background,anchor='nw')     # Place the background image, grid pattern.

    music_button=settings_menu_canvas.create_image(442,260,image=music_on_image,anchor="center")     # Toggle music on/off, on by default. 
    settings_menu_canvas.tag_bind(music_button,"<Button-1>",music)

    difficulty_button=settings_menu_canvas.create_image(442,452,image=standard_image,anchor="center")     # Game difficulty, standard by default. 
    settings_menu_canvas.tag_bind(difficulty_button,"<Button-1>",difficulty)

    if tb.game_difficulty=="Novice":     # If the game difficulty is novice, change the button image to novice. 
        settings_menu_canvas.itemconfig(difficulty_button,image=novice_image)
    elif tb.game_difficulty=="Expert":     # If the game difficulty is expert, change the button image to expert. 
        settings_menu_canvas.itemconfig(difficulty_button,image=expert_image)

    delete_account_button=settings_menu_canvas.create_image(442,650,image=delete_account_image,anchor="center")    # Delete player's game info, reset json file back to default.  
    settings_menu_canvas.tag_bind(delete_account_button,"<Button-1>",reset_data_window)


    back_button=settings_menu_canvas.create_image(770,970,image=back_image,anchor="center")     # Button to take player back to main menu. 
    settings_menu_canvas.tag_bind(back_button,"<Button-1>",menu)
    root.bind('<Escape>', menu)     # Keyboard shortcut; when player clicks escape, it returns them back to the previous menu (back button).


    if tb.music_toggle==False:     # If music is currently off, update it to off on the button. 
        settings_menu_canvas.itemconfig(music_button,image=music_off_image)


def achievements_menu(event=None):
    """Achievements menu to display all 9 achievements and will open their corresponding toplevel windows when clicked.

    Args:
        event (None): Defaults to None.
    """    

    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    achievements_menu_canvas=Canvas(root,bg="#f8eeda",height=1040,width=880, bd=0, highlightthickness=0)     # Frame over achievements menu window.
    achievements_menu_canvas.place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=0)

    achievements_menu_canvas.create_image(0,0,image=achievements_menu_background,anchor='nw')     # Place the background image, grid pattern.

    back_button=achievements_menu_canvas.create_image(770,970,image=back_image,anchor="center")     # Button to take player back to main menu. 
    achievements_menu_canvas.tag_bind(back_button,"<Button-1>",menu)
    root.bind('<Escape>', menu)     # Keyboard shortcut; when player clicks escape, it returns them back to the previous menu (back button).


    #achievement0=achievements_menu_canvas.create_image(100,100,image=achievement0_image,anchor="center")     # When player hasn't unlocked this achievement, make it locked with this image..

    achievement1=achievements_menu_canvas.create_image(250,320,image=achievement1_image,anchor="center")     # All achievements, clickable to open new window giving description and image.
    achievements_menu_canvas.tag_bind(achievement1,"<Button-1>",achievement_1)

    achievement2=achievements_menu_canvas.create_image(465,320,image=achievement2_image,anchor="center")    
    achievements_menu_canvas.tag_bind(achievement2,"<Button-1>",achievement_2)

    achievement3=achievements_menu_canvas.create_image(680,320,image=achievement3_image,anchor="center")    
    achievements_menu_canvas.tag_bind(achievement3,"<Button-1>",achievement_3)

    achievement4=achievements_menu_canvas.create_image(250,540,image=achievement4_image,anchor="center")    
    achievements_menu_canvas.tag_bind(achievement4,"<Button-1>",achievement_4)

    achievement5=achievements_menu_canvas.create_image(465,540,image=achievement5_image,anchor="center")    
    achievements_menu_canvas.tag_bind(achievement5,"<Button-1>",achievement_5)

    achievement6=achievements_menu_canvas.create_image(680,540,image=achievement6_image,anchor="center")    
    achievements_menu_canvas.tag_bind(achievement6,"<Button-1>",achievement_6)

    achievement7=achievements_menu_canvas.create_image(250,760,image=achievement7_image,anchor="center")    
    achievements_menu_canvas.tag_bind(achievement7,"<Button-1>",achievement_7)

    achievement8=achievements_menu_canvas.create_image(465,760,image=achievement8_image,anchor="center")    
    achievements_menu_canvas.tag_bind(achievement8,"<Button-1>",achievement_8)

    achievement9=achievements_menu_canvas.create_image(680,760,image=achievement9_image,anchor="center")    
    achievements_menu_canvas.tag_bind(achievement9,"<Button-1>",achievement_9)


    if tb.achievement_1==False:     # If achievements haven't been unlocked, disable the corresponding achievement button. 
        achievements_menu_canvas.itemconfig(achievement1,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement1,"<Button-1>")

    if tb.achievement_2==False:
        achievements_menu_canvas.itemconfig(achievement2,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement2,"<Button-1>")

    if tb.achievement_3==False:
        achievements_menu_canvas.itemconfig(achievement3,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement3,"<Button-1>")

    if tb.achievement_4==False:
        achievements_menu_canvas.itemconfig(achievement4,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement4,"<Button-1>")

    if tb.achievement_5==False:
        achievements_menu_canvas.itemconfig(achievement5,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement5,"<Button-1>")

    if tb.achievement_6==False:
        achievements_menu_canvas.itemconfig(achievement6,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement6,"<Button-1>")

    if tb.achievement_7==False:
        achievements_menu_canvas.itemconfig(achievement7,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement7,"<Button-1>")

    if tb.achievement_8==False:
        achievements_menu_canvas.itemconfig(achievement8,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement8,"<Button-1>")

    if tb.achievement_9==False:
        achievements_menu_canvas.itemconfig(achievement9,image=achievement0_image)
        achievements_menu_canvas.tag_unbind(achievement9,"<Button-1>")
   

def achievement_notification():
    """Achievement notification window pops up when achievement is unlocked. """   
    global notification_top

    notification_top=Toplevel()   # Details for the win window. 
    notification_top.title("Achievement Unlocked!")
    notification_top.geometry("655x299+"+str(tb.WINDOW_HORIZONTAL_OFFSET+850)+"+780")     # Make this window open next to the main one.
    notification_top.resizable(0,0)
    notification_top.overrideredirect(True)     # Stop player from manipulating this window.
    notification_top.attributes('-topmost', True)     # Make this window appear in front.

    notification_top_canvas=Canvas(notification_top,bg="#f8eeda",height=1040,width=880, bd=0, highlightthickness=0)     # Canvas frame over notification window.
    notification_top_canvas.place(x=0,y=0)

    notification_top_canvas.create_image(0,0,image=achievement_notification_background,anchor='nw')    # Background for achievmeent notification. 


def achievement_config(popup):
    """ Toplevel window appears when player clicks on the corresponding achievement, giving its badge and description.

    Args:
        popup (Image): The corresponding achievement image.
    """    

    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    destroy_all_top()     # Ensure only 1 achievement info window is opened at once. 

    def close_top(event=None):     # When player clicks 'close', it will close this popup window. 
        mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 
        achievements_top.destroy()
    
    achievements_top=Toplevel()   # Details for the win window. 
    achievements_top.title("Achievement")
    achievements_top.geometry("650x924+"+str(tb.WINDOW_HORIZONTAL_OFFSET+855)+"+100")     # Make this window open next to the main one.
    achievements_top.resizable(0,0)
    achievements_top.overrideredirect(True)     # Stop player from manipulating this window.
    achievements_top.attributes('-topmost', True)     # Make this window appear in front.

    achievements_top_canvas=Canvas(achievements_top,bg="#f8eeda",height=925,width=650, bd=0, highlightthickness=0)     # Canvas frame over achievements popup window.
    achievements_top_canvas.place(x=0,y=0)

    achievements_top_canvas.create_image(0,0,image=popup,anchor='nw')     # Place the achievement popup image as the background on the canvas. 

    close_button=achievements_top_canvas.create_image(127,865,image=close_image,anchor="center")      # Click this button to close achievement popup window.
    achievements_top_canvas.tag_bind(close_button,"<Button-1>",close_top)


def achievement_1(event=None):     # produce the achievement 1 toplevel window for this achievement.
    achievement_config(achievement1_popup)

def achievement_2(event=None):      # produce the achievement 2 toplevel window for this achievement.
   achievement_config(achievement2_popup)

def achievement_3(event=None):     # produce the achievement 3 toplevel window for this achievement.
    achievement_config(achievement3_popup)

def achievement_4(event=None):      # produce the achievement 4 toplevel window for this achievement.             
    achievement_config(achievement4_popup)

def achievement_5(event=None):     # produce the achievement 5 toplevel window for this achievement.
    achievement_config(achievement5_popup)

def achievement_6(event=None):      # produce the achievement 6 toplevel window for this achievement.           
    achievement_config(achievement6_popup)

def achievement_7(event=None):      # produce the achievement 7 toplevel window for this achievement.            
    achievement_config(achievement7_popup)

def achievement_8(event=None):     # produce the achievement 8 toplevel window for this achievement.
    achievement_config(achievement8_popup)

def achievement_9(event=None):     # produce the achievement 9 toplevel window for this achievement.
    achievement_config(achievement9_popup)
  

def generate_tip():
    """ Function which randomly generates tip at bottom of home menu for player. """
    global tip_label,menu_canvas

    tips_list= [
        "Need help graphing? Use the 'Hint' button to reveal the answer function's type.",
        "Click the 'Hint' button twice to reveal the answer function's format.",
        "Use the 'Coordinates' button for exact positions of coins and the start point.",
        "Game difficulty can be adjusted to suit your graphing skills under game settings.",
        "Legend has it there's an ultra-rare Diamond which may appear in a level...",
        "Levels in the Journey gamemode start easy but get progressively more difficult.",
        "The more tries you take, the less points you'll get which may affect your grade!",
        "Collecting coins gives you bonus points, but are not necessary.",
        "The game autosaves so you can reopen it without losing any progress.",
        "The highest possible grade you can receive is A+, with the lowest being F.",
        "Once completed all levels, you'll be awarded the 'Graph Master' achievement.",
        "The is always more than one way to graph the 'correct' function.",
        "To collect coins, your function doesn't need to cross their exact coordinates.",
        "Josad's Journey offers a range of functions; from logarithms to trigonometry.",
        "You must first complete the easier levels before giving the harder ones a try.",
        "Background music can be turned on or off under game settings.",
        "Play this game with headphones for the full immersive experience!",
        "Use '*' for multiplication, '/' for division and '^' for exponentiation.",
        "Use 'sqrt()' to denote the radical and 'ln()' to denote the natural logarithm.",
        "Your points for Zen mode are added together and stored as the Cumulative Score.",
        "Make sure all your brackets are closed in your function before graphing!",
        "Journey is an 18-level gamemode, whilst Zen is an unending, casual gamemode.",
        "Use 'Esc' to navigate to the previous menu, and 'Enter' to graph functions. ",
        "Use 'ctrl+C' to reveal coordinates, and 'ctrl+H' to reveal hints.",
        "Click me to refresh a new tip!"
    ]

    tb.tip_text=tips_list[random.randint(0,len(tips_list)-1)]     # Randomly generate tip text.
    #tip_label.config(text=tb.tip_text)     
    menu_canvas.itemconfig(tip_label,text=tb.tip_text)# Update this on the label in home menu. 


def menu(event=None):     # Main menu window, user selects levels etc. 
    """ The window that first pops up when user opens up game, gives option to choose zen or journey mode and settings and achievements.

    Args:
        event (None): Defaults to None.
    """    
    global name_entry,menu_canvas,name_error,greet_label,journey_button,zen_button,new_player_top,notification_top,tip_label,background_canvas

    background_canvas=Canvas(root,bg="#f8eeda",height=1100,width=3000, bd=0, highlightthickness=0)     # Have The grid background placed here. This will remain visible at all times (background) and is unchanged. 
    background_canvas.place(x=0,y=0)
    background_canvas.create_image(tb.WINDOW_HORIZONTAL_OFFSET+670,0,image=grid_background,anchor='n')    

    root.unbind('<Escape>')     # Escape key is shortcut to go back to previous menu, but home menu is already the first menu, so unbind this action. 

    mixer.Sound.play(clicked_sfx)     # Sound effect when button is clicked. 

    if mixer.music.get_busy() and tb.music_toggle==True:     # If music is currently playing, check if josad or zen is playing. 
        if tb.current_music=="Zen ost":     # If Zen is currently playing but player is in main menu, it shouldn't be playing, instead play josad ost.
            play_josadost_music()
    
    plt.close()     # Close previous graph. 

  
    toggle_tools_off()     # Turn all tools back off.

    for obj in tb.levels_list:      # Reset tries counter back to 0 when user finishes level and returns to menu. 
        obj.score_info.tries=0

    destroy_all_top()      # Destroys all previous toplevel windows if opened, such as achievement notifications etc.


    dy=100

    menu_canvas=Canvas(root,bg="#f8eeda",height=1100,width=883, bd=0, highlightthickness=0)     # First frame to appear on main menu.
    menu_canvas.place(x=tb.WINDOW_HORIZONTAL_OFFSET,y=0)
    
    #menu_canvas.create_image(0,0,image=grid_background,anchor='nw')     # Get the grid background. 

    menu_canvas.create_image(0,0,image=menu_background,anchor='nw')     # Place the background image, grid pattern.

    menu_canvas.create_image(390,160,image=logo,anchor="center")     # Logo.
    

    journey_button=menu_canvas.create_image(455,dy+472,image=journey_image,anchor="center")      # Click this button to initiate the journey level.
    menu_canvas.tag_bind(journey_button,"<Button-1>",journey_menu1)

    menu_canvas.create_text(455,610,font=("Comic Sans MS",12),text="Difficulty: "+str(tb.game_difficulty),anchor="center",fill="orange")    # Display the game difficulty for Journey.  

   
    zen_button=menu_canvas.create_image(455,dy+594,image=zen_image,anchor="center")      # Click this button to initiate the zen level, also display the score.
    menu_canvas.tag_bind(zen_button,"<Button-1>",spawn_level_zen)

    menu_canvas.create_text(455,736,font=("Comic Sans MS",12),text="Cumulative Score: "+str(L0.score_info.score),anchor="center",fill="orange")    # Display the cumulative score for zen. 

    achievements_button=menu_canvas.create_image(455,dy+726,image=achievements_image,anchor="center")      # Game achievements. 
    menu_canvas.tag_bind(achievements_button,"<Button-1>",achievements_menu)

    settings_button=menu_canvas.create_image(455,dy+854,image=settings_image,anchor="center")      # Game settings. 
    menu_canvas.tag_bind(settings_button,"<Button-1>",settings_menu)

    quit_button=menu_canvas.create_image(770,dy+910,image=quit_image,anchor="center")      # Quit game. 
    menu_canvas.tag_bind(quit_button,"<Button-1>",quit_game)

    greet_label=Label(root,text="New player detected.",fg="orange",bg="white",font=("Comic Sans MS",16))     # Greet the play on the home menu. 
    greet_label.place(x=805+tb.WINDOW_HORIZONTAL_OFFSET,y=400,anchor="e")

    tip_heading_label=menu_canvas.create_text(93,515,text="Tip:",fill="#050478",font=("Comic Sans MS",11,"bold","italic"),anchor="w")  # Tip for player, randomly generated at home menu. 
    menu_canvas.tag_bind(tip_heading_label,"<Button-1>",menu)     # Change the tip when player clicks on it. 
    tip_label=menu_canvas.create_text(135,515,text=tb.tip_text,fill="#050478",font=("Comic Sans MS",10,"italic"),anchor="w") 
    menu_canvas.tag_bind(tip_label,"<Button-1>",menu)

    #top_canvas.create_text(428,405,text="+"+str(int(35*level.score_info.coins)),font=("Comic Sans MS", 22))     # Coins collected bonus text.
    
    generate_tip()     # Function to randomly generate tip. 

    if tb.name =="":     # If the player name is blank ie. new player, go to the new player window.

        menu_canvas.tag_unbind(journey_button,"<Button-1>")
        menu_canvas.tag_unbind(zen_button,"<Button-1>")
        menu_canvas.tag_unbind(settings_button,"<Button-1>")
        menu_canvas.tag_unbind(achievements_button,"<Button-1>")
        new_player_window()
        root.unbind('<Return>')     # Unbind the name enter button as player has already entered his name and is not needed anymore. 

    else:
        greet_label.config(text="Greetings, "+tb.name+".",fg="#050478")     # When player name has been entered, greet him. 


    root.title("Josad's Journey")     # Main window configurations.
    root.geometry("880x1040+0+0")
    #root.resizable(0,0)
    root.state('zoomed')
    root.focus_force()
    root.iconbitmap(os.getcwd()+r"\Icons\Josad's Journey Icon.ico")   # Josad's Journey logo for icon. 
   
    root.mainloop()
    

root = Tk()
#root.tk.call('tk','scaling',2)
print(root.winfo_fpixels("1i"))

'''Load and setup all images''' 
# These are at the end of the program because tkinter root window needs to be created first.
# Using Image.LANCZOS does anti-aliasing on images.
menu_background_image=Image.open(os.getcwd()+r"\Images\home menu.png").convert("RGBA")     # Background for menu screens.
#menu_background_image=menu_background_image.resize((880,1040),Image.LANCZOS)     # Resize dimensions to fit main window exactly.
menu_background=ImageTk.PhotoImage(menu_background_image)

logo_image=Image.open(os.getcwd()+r"\Images\josad's journey logo.png").convert("RGBA")    # Game logo.
lw,lh=logo_image.size   
logo_image=logo_image.resize((int(lw/3.8),int(lh/3.8)),Image.LANCZOS)       # scale down size of logo image because it's too big.
logo=ImageTk.PhotoImage(logo_image)

journey_button_image=Image.open(os.getcwd()+r"\Images\Journey button.png").convert("RGBA")    # Button image.   
journey_image=ImageTk.PhotoImage(journey_button_image)

zen_button_image=Image.open(os.getcwd()+r"\Images\Zen button.png").convert("RGBA")    # Button image.   
zen_image=ImageTk.PhotoImage(zen_button_image)

achievements_button_image=Image.open(os.getcwd()+r"\Images\Achievements button.png").convert("RGBA")    # Button image.   
achievements_image=ImageTk.PhotoImage(achievements_button_image)

settings_button_image=Image.open(os.getcwd()+r"\Images\Settings button.png").convert("RGBA")    # Button image.   
settings_image=ImageTk.PhotoImage(settings_button_image)

quit_button_image=Image.open(os.getcwd()+r"\Images\Quit button.png").convert("RGBA")    # Quit image.   
quit_image=ImageTk.PhotoImage(quit_button_image)


level_background_image=Image.open(os.getcwd()+r"\Images\level background.png").convert("RGBA")     # Background for levels.
#level_background_image=level_background_image.resize((880,1040),Image.LANCZOS)     # Resize dimensions to fit main window exactly.
level_background=ImageTk.PhotoImage(level_background_image)

back_button_image=Image.open(os.getcwd()+r"\Images\Back button.png").convert("RGBA")    # back image.   
back_image=ImageTk.PhotoImage(back_button_image)

hint_button_image=Image.open(os.getcwd()+r"\Images\Hint button.png").convert("RGBA")    # Button image.   
hint_image=ImageTk.PhotoImage(hint_button_image)

coordinates_button_image=Image.open(os.getcwd()+r"\Images\Coordinates button.png").convert("RGBA")    # Button image.   
coordinates_image=ImageTk.PhotoImage(coordinates_button_image)

graph_button_image=Image.open(os.getcwd()+r"\Images\Graph button.png").convert("RGBA")    # Button image.   
graph_image=ImageTk.PhotoImage(graph_button_image)

hint1_icon_image=Image.open(os.getcwd()+r"\Images\Hint1 icon.png").convert("RGBA")    # Button image.   
hint1_icon_image=hint1_icon_image.resize((int(hint1_icon_image.width//1.5),int(hint1_icon_image.height//1.5)),Image.LANCZOS)     # Resize the image to 2/3x its original size.
hint1_image=ImageTk.PhotoImage(hint1_icon_image)

hint2_icon_image=Image.open(os.getcwd()+r"\Images\Hint2 icon.png").convert("RGBA")    # Button image.   
hint2_icon_image=hint2_icon_image.resize((int(hint2_icon_image.width//1.5),int(hint2_icon_image.height//1.5)),Image.LANCZOS)     # Resize the image to 2/3x its original size.
hint2_image=ImageTk.PhotoImage(hint2_icon_image)


level_complete_background_image=Image.open(os.getcwd()+r"\Images\level complete background.png").convert("RGBA")     # Background for level complete small window.
level_complete_background=ImageTk.PhotoImage(level_complete_background_image)

close_button_image=Image.open(os.getcwd()+r"\Images\Close button.png").convert("RGBA")     # Button image.
close_image=ImageTk.PhotoImage(close_button_image)


level_menu_background_image=Image.open(os.getcwd()+r"\Images\level menu background.png").convert("RGBA")     # Home menu background.  
level_menu_background=ImageTk.PhotoImage(level_menu_background_image)

grid_background_image=Image.open(os.getcwd()+r"\Images\home menu background.png").convert("RGBA")     # Home menu background.  
grid_background=ImageTk.PhotoImage(grid_background_image)

level1_button_image=Image.open(os.getcwd()+r"\Images\level 1.png").convert("RGBA")    # Button image.   
level1_image=ImageTk.PhotoImage(level1_button_image)
level2_button_image=Image.open(os.getcwd()+r"\Images\level 2.png").convert("RGBA")    # Button image.   
level2_image=ImageTk.PhotoImage(level2_button_image)
level3_button_image=Image.open(os.getcwd()+r"\Images\level 3.png").convert("RGBA")    # Button image.   
level3_image=ImageTk.PhotoImage(level3_button_image)
level4_button_image=Image.open(os.getcwd()+r"\Images\level 4.png").convert("RGBA")    # Button image.   
level4_image=ImageTk.PhotoImage(level4_button_image)
level5_button_image=Image.open(os.getcwd()+r"\Images\level 5.png").convert("RGBA")    # Button image.   
level5_image=ImageTk.PhotoImage(level5_button_image)
level6_button_image=Image.open(os.getcwd()+r"\Images\level 6.png").convert("RGBA")    # Button image.   
level6_image=ImageTk.PhotoImage(level6_button_image)

level7_button_image=Image.open(os.getcwd()+r"\Images\level 7.png").convert("RGBA")    # Button image.   
level7_image=ImageTk.PhotoImage(level7_button_image)
level8_button_image=Image.open(os.getcwd()+r"\Images\level 8.png").convert("RGBA")    # Button image.   
level8_image=ImageTk.PhotoImage(level8_button_image)
level9_button_image=Image.open(os.getcwd()+r"\Images\level 9.png").convert("RGBA")    # Button image.   
level9_image=ImageTk.PhotoImage(level9_button_image)
level10_button_image=Image.open(os.getcwd()+r"\Images\level 10.png").convert("RGBA")    # Button image.   
level10_image=ImageTk.PhotoImage(level10_button_image)
level11_button_image=Image.open(os.getcwd()+r"\Images\level 11.png").convert("RGBA")    # Button image.   
level11_image=ImageTk.PhotoImage(level11_button_image)
level12_button_image=Image.open(os.getcwd()+r"\Images\level 12.png").convert("RGBA")    # Button image.   
level12_image=ImageTk.PhotoImage(level12_button_image)

level13_button_image=Image.open(os.getcwd()+r"\Images\level 13.png").convert("RGBA")    # Button image.   
level13_image=ImageTk.PhotoImage(level13_button_image)
level14_button_image=Image.open(os.getcwd()+r"\Images\level 14.png").convert("RGBA")    # Button image.   
level14_image=ImageTk.PhotoImage(level14_button_image)
level15_button_image=Image.open(os.getcwd()+r"\Images\level 15.png").convert("RGBA")    # Button image.   
level15_image=ImageTk.PhotoImage(level15_button_image)
level16_button_image=Image.open(os.getcwd()+r"\Images\level 16.png").convert("RGBA")    # Button image.   
level16_image=ImageTk.PhotoImage(level16_button_image)
level17_button_image=Image.open(os.getcwd()+r"\Images\level 17.png").convert("RGBA")    # Button image.   
level17_image=ImageTk.PhotoImage(level17_button_image)
level18_button_image=Image.open(os.getcwd()+r"\Images\level 18.png").convert("RGBA")    # Button image.   
level18_image=ImageTk.PhotoImage(level18_button_image)

locked_button_image=Image.open(os.getcwd()+r"\Images\level locked.png").convert("RGBA")    # Button image.   
locked_image=ImageTk.PhotoImage(locked_button_image)

Amax_grade_image=Image.open(os.getcwd()+r"\Images\A+.png").convert("RGBA")     # Grade Image.   
Amax_image=ImageTk.PhotoImage(Amax_grade_image)
A_grade_image=Image.open(os.getcwd()+r"\Images\A.png").convert("RGBA")     # Grade Image.   
A_image=ImageTk.PhotoImage(A_grade_image)
B_grade_image=Image.open(os.getcwd()+r"\Images\B.png").convert("RGBA")     # Grade Image.   
B_image=ImageTk.PhotoImage(B_grade_image)
C_grade_image=Image.open(os.getcwd()+r"\Images\C.png").convert("RGBA")     # Grade Image.   
C_image=ImageTk.PhotoImage(C_grade_image)
D_grade_image=Image.open(os.getcwd()+r"\Images\D.png").convert("RGBA")     # Grade Image.   
D_image=ImageTk.PhotoImage(D_grade_image)
F_grade_image=Image.open(os.getcwd()+r"\Images\F.png").convert("RGBA")     # Grade Image.  
F_image=ImageTk.PhotoImage(F_grade_image)


previous_button_image=Image.open(os.getcwd()+r"\Images\Previous button.png").convert("RGBA")    # Button image.   
previous_image=ImageTk.PhotoImage(previous_button_image)
next_button_image=Image.open(os.getcwd()+r"\Images\Next button.png").convert("RGBA")    # Button image.   
next_image=ImageTk.PhotoImage(next_button_image)


settings_menu_background_image=Image.open(os.getcwd()+r"\Images\settings menu background.png").convert("RGBA")    # Settings menu background.   
settings_menu_background=ImageTk.PhotoImage(settings_menu_background_image)

delete_account_button_image=Image.open(os.getcwd()+r"\Images\Delete account button.png").convert("RGBA")    # Button image.   
delete_account_image=ImageTk.PhotoImage(delete_account_button_image)

novice_button_image=Image.open(os.getcwd()+r"\Images\Novice button.png").convert("RGBA")    # Button image.   
novice_image=ImageTk.PhotoImage(novice_button_image)

standard_button_image=Image.open(os.getcwd()+r"\Images\Standard button.png").convert("RGBA")    # Button image.   
standard_image=ImageTk.PhotoImage(standard_button_image)

expert_button_image=Image.open(os.getcwd()+r"\Images\Expert button.png").convert("RGBA")    # Button image.   
expert_image=ImageTk.PhotoImage(expert_button_image)

music_on_button_image=Image.open(os.getcwd()+r"\Images\Music on button.png").convert("RGBA")    # Button image.   
music_on_image=ImageTk.PhotoImage(music_on_button_image)

music_off_button_image=Image.open(os.getcwd()+r"\Images\Music off button.png").convert("RGBA")    # Button image.   
music_off_image=ImageTk.PhotoImage(music_off_button_image)


achievements_menu_background_image=Image.open(os.getcwd()+r"\Images\achievements menu background.png").convert("RGBA")    # Achievements menu background.   
achievements_menu_background=ImageTk.PhotoImage(achievements_menu_background_image)

achievement0_image=Image.open(os.getcwd()+r"\Images\achievement 0.png").convert("RGBA")    # All 10 achievements images (including the default, locked image).
achievement0_image=ImageTk.PhotoImage(achievement0_image)
achievement1_image=Image.open(os.getcwd()+r"\Images\achievement 1.png").convert("RGBA")   
achievement1_image=ImageTk.PhotoImage(achievement1_image)
achievement2_image=Image.open(os.getcwd()+r"\Images\achievement 2.png").convert("RGBA")    
achievement2_image=ImageTk.PhotoImage(achievement2_image)
achievement3_image=Image.open(os.getcwd()+r"\Images\achievement 3.png").convert("RGBA")    
achievement3_image=ImageTk.PhotoImage(achievement3_image)
achievement4_image=Image.open(os.getcwd()+r"\Images\achievement 4.png").convert("RGBA")  
achievement4_image=ImageTk.PhotoImage(achievement4_image)
achievement5_image=Image.open(os.getcwd()+r"\Images\achievement 5.png").convert("RGBA")      
achievement5_image=ImageTk.PhotoImage(achievement5_image)
achievement6_image=Image.open(os.getcwd()+r"\Images\achievement 6.png").convert("RGBA")     
achievement6_image=ImageTk.PhotoImage(achievement6_image)
achievement7_image=Image.open(os.getcwd()+r"\Images\achievement 7.png").convert("RGBA")       
achievement7_image=ImageTk.PhotoImage(achievement7_image)
achievement8_image=Image.open(os.getcwd()+r"\Images\achievement 8.png").convert("RGBA")       
achievement8_image=ImageTk.PhotoImage(achievement8_image)
achievement9_image=Image.open(os.getcwd()+r"\Images\achievement 9.png").convert("RGBA")       
achievement9_image=ImageTk.PhotoImage(achievement9_image)

achievement1_popup_image=Image.open(os.getcwd()+r"\Images\achievement 1 popup.png").convert("RGBA")      # Popup window for these achievements when player selects them.
achievement1_popup=ImageTk.PhotoImage(achievement1_popup_image)
achievement2_popup_image=Image.open(os.getcwd()+r"\Images\achievement 2 popup.png").convert("RGBA")        
achievement2_popup=ImageTk.PhotoImage(achievement2_popup_image)
achievement3_popup_image=Image.open(os.getcwd()+r"\Images\achievement 3 popup.png").convert("RGBA")        
achievement3_popup=ImageTk.PhotoImage(achievement3_popup_image)
achievement4_popup_image=Image.open(os.getcwd()+r"\Images\achievement 4 popup.png").convert("RGBA")        
achievement4_popup=ImageTk.PhotoImage(achievement4_popup_image)
achievement5_popup_image=Image.open(os.getcwd()+r"\Images\achievement 5 popup.png").convert("RGBA")        
achievement5_popup=ImageTk.PhotoImage(achievement5_popup_image)
achievement6_popup_image=Image.open(os.getcwd()+r"\Images\achievement 6 popup.png").convert("RGBA")        
achievement6_popup=ImageTk.PhotoImage(achievement6_popup_image)
achievement7_popup_image=Image.open(os.getcwd()+r"\Images\achievement 7 popup.png").convert("RGBA")        
achievement7_popup=ImageTk.PhotoImage(achievement7_popup_image)
achievement8_popup_image=Image.open(os.getcwd()+r"\Images\achievement 8 popup.png").convert("RGBA")        
achievement8_popup=ImageTk.PhotoImage(achievement8_popup_image)
achievement9_popup_image=Image.open(os.getcwd()+r"\Images\achievement 9 popup.png").convert("RGBA")       
achievement9_popup=ImageTk.PhotoImage(achievement9_popup_image)

#     make a list of all achievements to scale them all down at once.
achievements=[
    r"\Images\achievement 0.png",
    r"\Images\achievement 1.png",
    r"\Images\achievement 2.png",
    r"\Images\achievement 3.png",
    r"\Images\achievement 4.png",
    r"\Images\achievement 5.png",
    r"\Images\achievement 6.png",
    r"\Images\achievement 7.png",
    r"\Images\achievement 8.png",
    r"\Images\achievement 9.png"
]

def scale_image(image_path,scale_factor):     # Function to scale images.
    image=Image.open(os.getcwd()+"\\"+image_path).convert("RGBA")     # RGBA accounts for transparency.
    width,height=image.size     # Obtain the corresponding widths and heights of the image.
    image=image.resize((width//scale_factor,height//scale_factor),Image.LANCZOS)     # Scale image down, LANCZOS prevents jagged images when resizing.
    return ImageTk.PhotoImage(image) 
achievement_images=scaled_images=[scale_image(path,6) for path in achievements]     # Scale all images by 5x, save these over the original variable names. 
achievement0_image,achievement1_image, achievement2_image, achievement3_image, achievement4_image, achievement5_image, achievement6_image, achievement7_image, achievement8_image, achievement9_image = achievement_images


new_player_background_image=Image.open(os.getcwd()+r"\Images\new player background.png").convert("RGBA")     # Background image.        
new_player_background=ImageTk.PhotoImage(new_player_background_image)

confirm_button_image=Image.open(os.getcwd()+r"\Images\Confirm button.png").convert("RGBA")       # Button image. 
confirm_image=ImageTk.PhotoImage(confirm_button_image)


achievement_notification_background_image=Image.open(os.getcwd()+r"\Images\achievement notification background.png").convert("RGBA")    # Background image.    
achievement_notification_background=ImageTk.PhotoImage(achievement_notification_background_image)

delete_account_background_image=Image.open(os.getcwd()+r"\Images\delete account background.png").convert("RGBA")        # Background image.
delete_account_background=ImageTk.PhotoImage(delete_account_background_image)

delete_button_image=Image.open(os.getcwd()+r"\Images\Delete button.png").convert("RGBA")    # Button image.     
delete_image=ImageTk.PhotoImage(delete_button_image)

cancel_button_image=Image.open(os.getcwd()+r"\Images\Cancel button.png").convert("RGBA")     # Button image.    
cancel_image=ImageTk.PhotoImage(cancel_button_image)


tutorial1_background_image=Image.open(os.getcwd()+r"\Images\tutorial1 background.png").convert("RGBA")        # Tutorial 1 background image.
tutorial1_background=ImageTk.PhotoImage(tutorial1_background_image)

tutorial2_background_image=Image.open(os.getcwd()+r"\Images\tutorial2 background.png").convert("RGBA")        # Tutorial 2 background image.
tutorial2_background=ImageTk.PhotoImage(tutorial2_background_image)

tutorial3_background_image=Image.open(os.getcwd()+r"\Images\tutorial3 background.png").convert("RGBA")        # Tutorial 2 background image.
tutorial3_background=ImageTk.PhotoImage(tutorial3_background_image)


menu()
