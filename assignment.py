from __future__ import print_function
import time
from sr.robot import *

""" 
Robotics Engineering - Research Track 1 
Assignment number 1

by Simone Contorno
"""

# Threshold for the control of the orientation
a_th = 5

# Threshold for the control of the linear distance
d_th = 0.4

# Instance of the class Robot
R = Robot()

"""
Function for setting a linear velocity

Args: 
    speed (int): the speed of the wheels
	seconds (int): the time interval
"""
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

"""
Function for setting an angular velocity
    
Args: 
    speed (int): the speed of the wheels
	seconds (int): the time interval
"""
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

"""
Function to find the closest silver-token

Returns:
    dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
"""
def find_token_silver():
    print("Searching a silver token...")
    dist = 100
    for token in R.see():
        #print(token)
        if token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < dist:
            dist = token.dist
	    rot_y = token.rot_y
    if dist == 100:
	    return -1, -1
    else:
   	    return dist, rot_y

"""
Function to find the closest golden-token

Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
"""
def find_token_gold():
    dist=100
    for token in R.see():
        if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < dist :
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	    return -1, -1
    else:
   	    return dist, rot_y

def move_behind() :
    turn(60, 1)
    R.release()
    turn(-60,1)

'''
Function to return module value
'''
def module(rot) :
    if rot < 0 :
        return rot * -1
    else :
        return rot
    
'''
Start program
'''
while 1:
    # Search the closest silver token
    dist_s, rot_s = find_token_silver()

    # Search the closest gold token
    dist_g, rot_g = find_token_gold()

    # Check error
    if dist_s == -1:
        print("I don't see any silver token...")

    # Check if it is close enough to grab
    elif dist_s < d_th: 
        print("Found it!")
        R.grab() # If the robot is close to the token, it grabs it.
        print("Gotcha!") 
        move_behind() # Move the block behind it

    elif -a_th <= rot_s <= a_th : # Ff the robot is well aligned with the token,it goes forward
        print("Go on!")
        drive(50, 0.5)
        continue
    
    # Take absolute value of rot_s
    rot_s_m = module(rot_s)
    
    #Take absolute value of rot_g
    rot_g_m = module(rot_g)

    '''
    IF: 
    Check if the robot can turn against the silver token.
    The third condition is to avoid that the robot turns
    against a silver token bihind him (i manage its movements
    in order to have the next silver token within this limit).

    ELSE: 
    Check if the robot is too close to a golden token.
    In this case it evaluates two ways:
        1. If it is almost in front of a golden token it goes back 
        a little and after turns to go to the next silver token.
        2. If the condition above is satisfy so it also turns away from
        the golden token until it is more or less align with the next 
        silver token or the angle with the golden token is more then 90.
        3. If the above condition is not satisfy the robot turns away
        the golden token until the angle with it is more then 88
    '''
    if rot_s_m < rot_g_m and dist_s < dist_g and rot_s_m < 105: # IF
        print("Turning against silver token...")
        while rot_s_m > a_th and rot_s_m < 105:
            if rot_s < -a_th : # Turning left
                turn(-1, 0.5)
            elif rot_s > a_th : # Turning right
                turn(+1, 0.5)
            dist_s, rot_s = find_token_silver()
            rot_s_m = module(rot_s)
            print(rot_s_m)
    else : # ELSE
        while rot_g_m < 88 :
            print("Turning away golden token...")
            # Condition
            if rot_g_m < a_th * 3 and dist_g < 0.9 : # If the robot is almost in front of a golden token
                print("Turning away golden token and against silver token...")
                # 1.
                while rot_s_m > 91 and dist_g < 0.9 :
                    print("1.")
                    drive(-10, 0.5) 
                    dist_g, rot_g = find_token_gold()
                    #print(dist_g)
                    dist_s, rot_s = find_token_silver()
                    rot_s_m = module(rot_s)
                # 2.
                while rot_s_m > a_th and rot_g_m < 90 :
                    print("2.")
                    if rot_s < -a_th :
                        turn(-10, 1)
                    elif rot_s > a_th :
                        turn(+10, 1)
                    dist_s, rot_s = find_token_silver()
                    dist_g, rot_g = find_token_gold()
                    rot_g_m = module(rot_g)
                    rot_s_m = module(rot_s)
            # 3.
            elif rot_g <= 0 :  
                print("Turning right")
                turn(+1, 0.5)
            elif rot_g > 0 :
                print("Turning left")
                turn(-1, 0.5)
            #elif -a_th < rot_g < a_th :
                
            dist_g, rot_g = find_token_gold()
            rot_g_m = module(rot_g)
            print(rot_g_m)
            print(dist_g)

    # Go on
    drive(25, 1)