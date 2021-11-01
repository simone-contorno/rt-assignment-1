from __future__ import print_function
import time
from sr.robot import *
import math

'''
    Robotics Engineering - Research Track 1 
    Assignment number 1

    by Simone Contorno
'''

'''
    ---------- GLOBAL VARIABLES ----------
                                            '''

a_th = 2 # Threshold for the control of the orientation
d_th = 0.4 # Threshold for the control of the linear distance

# max_speed = 100
straight_on_speed = 75 # Straight on speed
turn_speed = 12.5 # Turn speed
kp = 1 # Gain
margin_error = 1 # Spin precision

'''
Change these values if the map changes:
    1. max_angle_from_g : if the robot has an angle less than this one and more than
    min_angle_from_g, it turns to remain parallel to the borders.
    2. min_angle_from_g : if the robot has an angle less than this one and the distance
    from the golden token is less than dist_from_g, it turns of turn_from_g
'''
max_angle_from_g = 82.5 
min_angle_from_g = 10            
dist_from_g = 1
turn_from_g = 90

'''
Refresh rate: decrement this value to obtain a more precision with the robot's movements
'''
refresh_rate = 0.05 

'''
Memory system variables:
    - direction : signal the direction that the robot is going on:
        1 - Right
        2 - Up
        3 - Left
        4 - Down
    - memory : memorize the last direction (with the opposite value).
    - turn_value : the robot turns of this value if direction is equals to the memory
    - distance : update memory value only when the robot ran this value
'''
direction = 4 # Initial direction
memory = 2 # Initial memory
turn_value = 90 
distance = 0 # Initial distance
distance_to_run = 0.06 

old_direction = 0 # Just to manage how often print direction
print_flag = 0 # Just to manage printed strings

# Instance of the class Robot
R = Robot()

'''
    ---------- FUNCTIONS ----------
                                    '''

'''
Function to go on

Args: 
    speed (int): the speed of the wheels
	seconds (int): the time interval
'''
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

"""
Function to turn
    
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

'''
Function to find the closest silver-token

Returns:
    dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
'''
def find_token_silver():
    dist = 100
    for token in R.see():
        if token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < dist :
            dist = token.dist
	    rot_y = token.rot_y
    if dist == 100:
	    return -1, -1
    else:
   	    return dist, rot_y

'''
Function to find the closest golden-token

Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
'''
def find_token_gold():
    dist = 100
    for token in R.see():
        if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < dist :
            dist = token.dist
	    rot_y = token.rot_y
    if dist == 100:
	    return -1, -1
    else:
   	    return dist, rot_y

'''
Function to move behind the silver token when the robot grabs it
'''
def move_behind() :
    turn_P(180)
    R.release()
    turn_P(180)

'''
Function to check orientation and update direct values 
'''
def update(direction) :

    # Update direction 
    heading = R.heading * 180 / math.pi

    if -45 <= heading < 45 :
        direction = 1
    elif -135 <= heading < -45 :
        direction = 2
    elif -180 <= heading < -135 :
        direction = 3
    elif 45 <= heading < 135 :
        direction = 4
    elif 135 <= heading <= 180 :
        direction = 3

    return direction


'''
Function to turn the robot of a grades value :
    1. Take current orientation
    2. Compute final orientation
    3. Turn until the orientation is equals to the computed final orientation
'''
def turn_P(grades) :

    # 1. Take current orientation
    heading = R.heading * 180 / math.pi
    if -180 <= heading < 0 :
        heading = module(heading)
    elif 0 <= heading <= 180 :
        heading = 360 - heading
    
    # 2. Compute final orientation
    final = heading + grades

    final_flag = 0

    if final > 360 :
        final -= 360
        error = 360 - heading + final
        final_flag = 1
    else : 
        error = final - heading
        error = module(error)
    
    # 3. Turn until the error is more than max error set
    while error > margin_error :
        turn(-error * kp, refresh_rate)

        heading = R.heading * 180 / math.pi
        if -180 <= heading < 0 :
            heading = module(heading)
        elif 0 <= heading <= 180 :
            heading = 360 - heading

        if final_flag == 1 and heading > final :
            error = 360 - heading + final
        else :
            error = final - heading
            error = module(error)

'''
Function to return the module value
'''
def module(rot) :
    if rot < 0 :
        return rot * -1
    else :
        return rot

'''
    ---------- PROGRAM STARTS ----------
                                        '''

print("\nTurning on the robot...")
time.sleep(3)
print("GO!\n")

while 1:
    # Update direction value
    direction = update(direction)

    # Search the closest silver token
    dist_s, rot_s = find_token_silver()

    # Search the closest golden token
    dist_g, rot_g = find_token_gold()

    # Take the absolute value of rot_s
    rot_s_m = module(rot_s)
    
    # Take the absolute value of rot_g
    rot_g_m = module(rot_g)

    # Check error
    if dist_s == -1:
        print("I don't see any silver token... :(")
    else :
        # Check if it is close enough to grab
        if dist_s < d_th and rot_s_m < a_th : 
            R.grab() # If the robot is close to the token, it grabs it
            print("Gotcha!\n") 
            move_behind() # Move the block behind it

    '''
    Check if the robot has not any golden token between it and the silver token; 
    in this case it turns against the silver token iff the angle with this one
    is not too much, otherwise it go on to reach it.
    '''
    if (dist_s < dist_g and rot_s_m < 90) or 0 <= rot_s_m < 10 and direction != memory :
        
        # Aligned with the silver token
        if rot_s_m < a_th : 
            drive(+straight_on_speed, refresh_rate)
     
        # Align with the silver token
        else : 
            if rot_s < 0 : # Turn left
                turn(-turn_speed, refresh_rate)

            else : # Turn right
                turn(+turn_speed, refresh_rate)
                
            NULL, rot_s = find_token_silver()
            rot_s_m = module(rot_s)

        continue
    
    '''
    Check if the robot is oriented too close to a golden token (the angle between them is too small)
    '''
    if min_angle_from_g <= rot_g_m < max_angle_from_g :

        if rot_g < 0 : # Turn right
            turn(+turn_speed, refresh_rate)   

        else : # Turn left
            turn(-turn_speed, refresh_rate) 

        continue

    '''
    Check if the robot is too close to a golden token (almost in front of it)
    '''
    if dist_g < dist_from_g and rot_g_m < min_angle_from_g :
        turn_P(turn_from_g)
        distance = 0

    '''
    Check 
    
    If the direction is not equals to the memory:
        1. The robot go 
        2. The memory value will be update after a distance value.
        3. Print new values.
    
    If the direction is equals to the memory the robot turns left of 90 grades.
    '''
    if direction != memory : 

        # 1. Compute the distance
        temp_dist_g, NULL = find_token_gold()
        drive(straight_on_speed, refresh_rate)
        dist_g, NULL = find_token_gold()

        # The difference must be small (otherwise it means that the robot changed the reference token)
        if dist_g > temp_dist_g and dist_g - temp_dist_g < 0.05 :
            distance += (dist_g - temp_dist_g)

        elif dist_g <= temp_dist_g and temp_dist_g - dist_g < 0.05 : 
            distance += (temp_dist_g - dist_g)
            
        # 2. Update the memory
        if distance >= distance_to_run : 
            distance = 0

            if direction == 1 :
                memory = 3
            elif direction == 2 :
                memory = 4
            elif direction == 3 :
                memory = 1
            else :
                memory = 2

            if print_flag == 1 :
                print("New memory: " + str(memory))
                print_flag = 0
        
        # 3. Print direction value
        if old_direction != direction :
            print("New direction = " + str(direction))
            old_direction = direction
            distance = 0
            print_flag = 1

    else : # direction == memory
        turn_P(turn_value) 
        distance = 0