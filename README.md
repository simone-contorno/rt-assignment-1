# rt_assignment_1
## Research Track 1 - Assignment 1

<br><br><br>
Robotics Engineering - Simone Contorno<br>
Control of a robot in a simulated environment.

### Introduction
An overview of this program function.<br>
[Go to Introduction](#intro)

### How it works
A rapid description of how the program works (pseudo-code).<br>
[Go to How it works](#how)

### Installation and Execution
How install and run rt_assignment_1 on Linux.<br>
[Go to Installation and Execution](#installation)

### Improvements
How this program could be improved.<br>
[Go to Improvements](#improve)

<a name="intro"></a>
### Introduction

rt_assigment_1 uses the library sr.robot to obtain information about the robot and to control it.<br>
In particular, the robot:
    <ol>
        <li>Follows a path.</li>
        <li>Avoids the golden tokens which rappresent the borders.</li>
        <li>Grabs a silver token when it is near to them and move it behind itself.</li>
    </ol>
<br>
At the start it looks like this:

![map](https://github.com/simone-contorno/rt_assignment_1/blob/main/map.png)

<a name="how"></a>
### How it works

The program use principally 2 parameters:
    <ol>
        <li>Direction: signal the direction where the robot is going on.</li>
            <ul>
                <li>1 - Right</li>
                <li>2 - Up</li>
                <li>3 - Left</li>
                <li>4 - Right</li>
            </ul>
        <li>Memory: memorize the last direction (with the opposite direction value).</li>
    </ol>
Using these variables the robot can follow the path without worrying about the next silver token and adjusting the direction to remain almost parallel to the borders.<br>
When it is too close to a golden token (in front of it), the robot turns, searching a new free direction.<br>
When it is close enough to a silver token, the robot starts to align itself with the token and reaches it to grab and move it behind itself.<br>
Look the pseudo-code file for more details.<br>

<a name="installation"></a>
### Installation and Execution

First of all install the simulated environment from github opening the terminal and typing:

<pre>
    <code>
        git clone https://github.com/CarmineD8/python_simulator.git
    </code>
</pre>

After, go in the folder 'python_simulator' and afterwards into 'robot-sim', where there is the file 'run.py',
and download rt_assignment_1 typing:

<pre>
    <code>
        https://github.com/simone-contorno/rt_assignment_1
    </code>
</pre>

Now, to run 'assignment.py' type:

<pre>
    <code>
        python2 run.py rt_assignment_1/assignment.py
    </code>
</pre>

You can also change some parameters into the code to modify the robot performance (e.g. straight_on_speed, turn_speed and refresh_rate).<br>
You will find all the information about functions and variables in the file thanks to the comments.

<a name="improve"></a>
### Improvements

The robot view could be improved to a better performance: <br>
instead of turn when it is against a wall, it can turns following better rules, like checking the distance of more than one golden token and computing the path direction to follow it.
<br>
Bye.    :slightly_smiling_face: