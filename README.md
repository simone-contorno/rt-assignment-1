# Research Track 2 - Robotics Engineering
## Statistical Analysis
### Author: Simone Contorno

<br>

### Introduction
An overview of this program function.<br>
[Go to Introduction](#intro)

### How it works
A rapid description of how the program works (pseudo-code).<br>
[Go to How it works](#how)

### Installation and Execution
How install and run this program in Linux.<br>
[Go to Installation and Execution](#installation)

<a name="intro"></a>
### Introduction

The main aim of this branch is to provide a statistical analysis based on the comparison between the program of this repository and a another one.<br>
The performance are evaluated on the base of the average time to compute a race, and different map configuration are used.<br>

Read the file statistical_analysis.pdf for more details.

<a name="how"></a>
### How it works

Read the README.md of the main branch.

<a name="installation"></a>
### Installation and Execution

Download this repository:

<pre><code>git clone https://github.com/simone-contorno/rt-assignment-1</code></pre>

Go into the downloaded folder and change the branch:

<pre><code>git checkout rt2-statistical-analysis</code></pre>

Go into the folder robot-sim and run 'my_robot.py' and/or 'prof_robot':

<pre><code>python2 run.py my_robot.py</code></pre>
<pre><code>python2 run.py prof_robot.py</code></pre>

The robots will write the expired time for each race into two files, respectively 'my_time.txt' and 'prof_time.txt'.<br>
You will find all the information about functions and variables in the file thanks to the comments.
