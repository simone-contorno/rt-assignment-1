from __future__ import print_function
import time
from sr.robot import *

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
straight_on_speed = 50 # Straight on speed
turn_speed = 10 # Turn speed

'''
Refresh rate: decrement this value to obtain a more precision with the robot's movements
but pay attention to don't break out your PC... :)
'''
refresh_rate = 0.05 

'''
Memory system variables:
- Orientation: check how the robot is oriented.
- Direction: signal the direction that the robot is going on:
    1 - Right
    2 - Up
    3 - Left
    4 - Down
- Memory: memorize the last direction (with the opposite value).
- Distance: update memory value only when the robot ran this distance value.
'''
orientation = 270 # Initial orientation
direction = 4 # Initial direction
memory = 2 # Initial memory
distance = 0 # Initial runned distance

temp_rot_s = 0 # Initial value of rotation about a silver token (when the spin starts)
temp_rot_g = 0 # Initial value of rotation about a golden token (when the spin starts)
current_rot_s = 0 # Final value of rotation about a silver token (when the spin ends)
current_rot_g = 0 # Final value of rotation about a golden token (when the spin ends)

old_direction = 0 # Just to manage how often print direction
print_flag = 0 # Just to manage printed strings
error_flag = 1 # Flag to signal if the error can be reduced
rot_flag = 0 # Flag to signal rotation

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
        if token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < dist:
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
    turn(60, 1)
    time.sleep(0.1)
    R.release()
    time.sleep(0.1)
    turn(-60, 1)
    drive(straight_on_speed, 0.5)

'''
Function to update the robot's orientation while it is turning against a silver token

Arguments:
    - orientation (explained above)
    - direction (explained above)
    - rot: started orientation (before the spin starts)
    - current_rot: ended orientation (when the spin finish)
    - way: left or right
'''
def rotate(orientation, direction, rot, current_rot, way) :

    # Difference value
    if current_rot > 0 and rot < 0 :
        difference = current_rot - rot
    elif current_rot < 0 and rot > 0 :
        difference = rot - current_rot
    else :
        current_rot = module(current_rot)
        rot = module(rot)
        if rot > current_rot :
            difference = rot - current_rot
        else :
            difference = current_rot - rot 

    # Update orientation
    if difference < 135 : # To avoid the case when the robot change the token reference when it finishes to spin
        if way == "left" :
            orientation += difference
        else :
            orientation -= difference

    orientation, direction = update(orientation, direction) # Call update function
    
    return orientation, direction
        
'''
Function to check orientation and update direct values 
'''
def update(orientation, direction) :

    # Check orientation inconsistencies
    if orientation > 360 :
        orientation -= 360
    elif orientation < 0 :
        orientation += 360

    # Update direction 
    if 0 <= orientation <= 45 :
        direction = 1
    elif 45 < orientation <= 135 :
        direction = 2
    elif 135 < orientation <= 225 :
        direction = 3
    elif 225 < orientation <= 315 :
        direction = 4
    elif 315 < orientation <= 360 :
        direction = 1

    return orientation, direction

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

    # Orientation error correction
    if 89 < rot_g_m < 91 and error_flag == 1:
        if 0 <= orientation <= 45 :
            orientation = 0
            direction = 1
        elif 45 < orientation <= 135 :
            orientation = 90
            direction = 2
        elif 135 < orientation <= 225 :
            orientation = 180
            direction = 3
        elif 225 < orientation <= 315 :
            orientation = 270
            direction = 4
        elif 315 < orientation <= 360 :
            orientation = 0
            direction = 1

    '''
    Check if the robot has not any golden token between it and the silver token; 
    in this case it turns against the silver token iff the angle with this one
    is not too much, otherwise it go on to reach its.
    '''
    if dist_s < dist_g and rot_s_m < 90 :
        
        # Aligned with the silver token
        if rot_s_m < a_th : 

            # Reach the silver token
            while dist_s > d_th : 
                dist_s, rot_s = find_token_silver()
                drive(+straight_on_speed, refresh_rate)
        
        # Align with the silver token
        else : 
            error_flag = 0

            # Memorize starting orientation
            if temp_rot_s == 0 :
                temp_rot_s = rot_s
                current_rot_s = rot_s

            # Check if at the end the robot did not change the reference silver token, otherwise use the last value of current_rot_s
            if temp_rot_s != 0 and ((0 < rot_s_m - module(current_rot_s) < 15) or (0 < module(current_rot_s) - rot_s_m < 15)) :
                current_rot_s = rot_s

            if rot_s < 0 : # Turn left
                rot_flag = 1
                turn(-turn_speed, refresh_rate)

            else : # Turn right
                rot_flag = 2
                turn(+turn_speed, refresh_rate)
                
            continue
    
    '''
    Check if the robot is oriented too close to a golden token (the angle between them is too small)
    '''
    if 10 <= rot_g_m < 85 :
        error_flag = 0

        # Memorize starting orientation
        if temp_rot_g == 0 :
            temp_rot_g = rot_g
            current_rot_g = rot_g
        
        # Check if at the end the robot did not change the reference golden token, otherwise use the last value of current_rot_g
        if temp_rot_g != 0 and ((0 < rot_g_m - module(current_rot_g) < 15) or (0 < module(current_rot_g) - rot_g_m < 15)) :
            current_rot_g = rot_g

        if rot_g < 0 : # Turn right
            rot_flag = 3
            turn(+turn_speed, refresh_rate)
            
        else : # Turn left
            rot_flag = 4
            turn(-turn_speed, refresh_rate)
            
        continue

    '''
    Check if the robot is too close to a golden token (almost in front of its)
    '''
    if dist_g < 1 and rot_g_m < 10 :
        turn(-60, 0.5) # Turn left of 90 grades
        distance = 0
        orientation += 90
        orientation, direction = update(orientation, direction)

    '''
    Check 
    
    If the direction is not equals to the memory:
        1. The robot go on and the memory value will be update after a distance value.
        2. If some spin was done, so update orientation and direction values.
        3. Print new values.
    
    If the direction is equals to the memory:
        1. The robot turns left of 90 grades.
        2. Update orientation and direction.
    '''
    if direction != memory : 

        # 1. Compute the distance
        temp_dist_g, NULL = find_token_gold()
        drive(straight_on_speed, refresh_rate)
        dist_g, NULL = find_token_gold()

        # The difference must be small (otherwise it does mean that the robot changed the reference token)
        if dist_g > temp_dist_g and dist_g - temp_dist_g < 0.05 :
            distance += (dist_g - temp_dist_g)

        elif dist_g <= temp_dist_g and temp_dist_g - dist_g < 0.05 : 
            distance += (temp_dist_g - dist_g)
            
        # Update the memory
        if distance >= 0.075 : 
            distance = 0
            error_flag = 1

            if direction == 1 :
                memory = 3
            elif direction == 2 :
                memory = 4
            elif direction == 3 :
                memory = 1
            else :
                memory = 2

            if print_flag == 1 and old_direction != direction :
                print("New memory: " + str(memory))
                print_flag = 0
        
        # 2. Check if some spin was done
        if rot_flag == 1 :
            orientation, direction = rotate(orientation, direction, temp_rot_s, current_rot_s, "left")
        elif rot_flag == 2 :
            orientation, direction = rotate(orientation, direction, temp_rot_s, current_rot_s, "right")
        elif rot_flag == 3 :
            orientation, direction = rotate(orientation, direction, temp_rot_g, current_rot_g, "right")
        elif rot_flag == 4 :
            orientation, direction = rotate(orientation, direction, temp_rot_g, current_rot_g, "left")
        
        # 3. Print new orientation and direction values
        if rot_flag == 1 or rot_flag == 2 or rot_flag == 3 or rot_flag == 4 :
            if print_flag == 0 and old_direction != direction :
                # print("New orientation = " + str(orientation))
                print("New direction = " + str(direction) + "\n")
                old_direction = direction
                print_flag = 1

        rot_flag = 0
        temp_rot_s = 0
        temp_rot_g = 0
        current_rot_temp_s = 0
        current_rot_temp_g = 0
        
    else : # direction == memory
        turn(-60, 0.5) # Turn left of 90 grades
        distance = 0
        orientation += 90
        orientation, direction = update(orientation, direction)