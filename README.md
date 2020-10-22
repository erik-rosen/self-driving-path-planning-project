# CarND-Path-Planning-Project
This project contains a working highway path planner implementation, which was built as part of the Self-Driving Car Engineer Nanodegree Program
  
![alt text](path_planning.gif "Path Planner in Action")


### Project Goals
In this project the goal is to safely navigate around a virtual highway with other traffic that is driving +-10 MPH of the 50 MPH speed limit. The simulator provides us with the car's localization and sensor fusion data and there is also a sparse map list of waypoints around the highway. The goal is for the car should to go as close as possible to the 50 MPH speed limit, which means passing slower traffic when possible. Other cars will try to change lanes too, adding further complexity to the problem. 

The car uses a finite state machine with 6 different states to successfully avoid hitting other cars at all cost as well as driving inside of the marked road lanes at all times, unless when switching lanes. The car is able to make more than one complete loop around the 6946m highway without incident. The car should not experience total acceleration over 10 m/s^2 and jerk that is greater than 10 m/s^3.

#### Path genereration

Lorem ipsum dolor amet.

### Simulator.
You can download the Term3 Simulator which contains the Path Planning Project from the [releases tab (https://github.com/udacity/self-driving-car-sim/releases/tag/T3_v1.2).  

To run the simulator on Mac/Linux, first make the binary file executable with the following command:
```shell
sudo chmod u+x {simulator_file_name}
```

## Basic Build Instructions

1. Clone this repo.
2. Make a build directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./path_planning`.


## Dependencies

* cmake >= 3.5
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools]((https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)
* [uWebSockets](https://github.com/uWebSockets/uWebSockets)
  * Run either `install-mac.sh` or `install-ubuntu.sh`.
  * If you install from source, checkout to commit `e94b6e1`, i.e.
    ```
    git clone https://github.com/uWebSockets/uWebSockets 
    cd uWebSockets
    git checkout e94b6e1
    ```