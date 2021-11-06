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

rt_assigment_1 uses the library sr.robot to get information about the robot and to control it.<br>
In particular, the robot:
    <ol>
        <li>Follows a path.</li>
        <li>Avoids the golden tokens which rappresent the borders.</li>
        <li>Grabs a silver token when it is near to it and move it behind itself.</li>
    </ol>
<br>
At the begin it looks like:

![map](https://github.com/simone-contorno/rt_assignment_1/blob/main/map.png)

<a name="how"></a>
### How it works

Let's analyze each case:
    <ul>
        <li>If there is an angle too small between the robot and a golden token, the robot turns away to be almost parallel to the borders.</li>
        <li>If there is a distance too small between the robot and a silver token, the robot starts a check to identify where the path is free;
            to do this, it checks the distance from the wall on the right and from the wall on the left (walls are represented by golden token)
            and go to the furthest one.</li>
        <li>If there is not any golden token between the robot and a silver token and the distance between them is little enough (less than the
            distance between the robot and the closest golden token), the robot turns against the silver token and go on.</li>
        <li>When the robot is close enough to the silver token, it grabs this one, move it behind itself and turns again to continue the path.</li>
    </ul>
Look the pseudocode file for more details.<br>

<a name="installation"></a>
### Installation and Execution

First of all install the simulated environment from github opening the terminal and typing:

<pre>
    <code>
        git clone https://github.com/CarmineD8/python_simulator.git
    </code>
</pre>

After, go in the folder 'python_simulator', afterwards into 'robot-sim', where there is the file 'run.py',
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

You can also change some parameters into the code to modify the robot performance (e.g. straight_on_speed and refresh_rate).<br>
You will find all the information about functions and variables in the file thanks to the comments.

<a name="improve"></a>
### Improvements

Let's notice some possible and very well improvements:<br>
    <ul>
        <li>The robot could turn better with a better check about the golden tokens around it.</li>
        <li>The robot could identify better the silver token, for instance it could go to reach it
            only when there is not any golden token between them, without the second check about the
            distance between the robot and the closest golden token.</li>
    </ul>
Thanks to have read this file, i hope it was clear and interesting.<br>
<br>
Bye.    :slightly_smiling_face:
