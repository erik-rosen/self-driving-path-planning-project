# CarND-Path-Planning-Project
This project contains a working highway path planner implementation, which was built as part of the Self-Driving Car Engineer Nanodegree Program
  
![alt text](path_planning.gif "Path Planner in Action")

_Fig 1: Output of path planner - safely navigating a trafficated highway._

## Project Goals
In this project the goal is to safely navigate around a virtual highway with other traffic that is driving +-10 MPH of the 50 MPH speed limit. The simulator provides us with the car's localization and sensor fusion data and there is also a sparse map list of waypoints around the highway. The goal is for the car should to go as close as possible to the 50 MPH speed limit, which means passing slower traffic when possible. Other cars will try to change lanes too, adding further complexity to the problem. 


## Path Planning

On a high level, the path planner uses a finite state machine with 6 different states to successfully avoid hitting other cars and adhering to traffic laws, while still working to minimize the travel time.

### State machine

 Each state can be split up into two components, where one governs the velocity of the vehicle, and the other governs whether or not to switch lane. The velocity control component of the state machine can take 3 different values: 
 
 #### Velocity

* Keep speed limit: Match own vehicle reference velocity to something close to the speed limit.
* Track: Match the reference velocity of the closest vehicle in front in the same lane.
* Slow down: Slow down - reduces the reference velocity of the own vehicle by 1 meter per second every second.

As long as the closest vehicle in front in the same lane is further than 35 meters away, the ego vehicles will assume state *Keep speed limit*, if the distance to the closest vehicle in front in the same lane is between 20-35 meters, we will try to *track* and match the ego vehicles velocity to the vehicle in front of it. If the distance is less than 20 meters to the closest vehicle in front in the same lane, the ego vehicle will *slow down* to increase the distance to the vehicle in front.

The reference velocity is used to compute the trajectory - see *Trajectory Generation*

#### Lane switch

The second part of the state machine governs lane switching. This takes on two different values:

* Keeping lane
* Switching lane

The car will enter the *switch lane* state if both of the below are true: 

* It is currently not in a state where the velocity control state component is *Keep speed limit*  
* Either of the adjacent lanes are safe to switch to

Upon entering a state where the late switch component becomes: *Switching lane*, the target lane is either decreased by one (switch to lane left of the car), or increased by one (switch to lane right of the car). This is used by the *trajectory generation* - see below.

The car will enter the *keeping lane* state if the target lane center is the most proximate lane center to the car.

#### Safe lane checking

The path planner uses a simple bounding box in frenet space to determine whether a lane is safe to switch to or not. If the lane is empty 35 meters ahead of the own vehicle and 15 meters behind the own vehicle, the lane is determined safe to change to. 

I attempted several more sophisticated approaches to determine whether or not a lane is safe to switch to - including more advanced prediction of other vehicles future position: 
 * A gaussian naive bayes classifier with a motion model to predict the future position of cars
 * A neural net which predicted the position of other cars 1-10 seconds in the future
 * A motion model assuming constant velocity and no lane changes
 
The above predictions would be compared to generated ego vehicle lane switching trajectories to check for collisions/unsafe distances. The more sophisticated approaches introduced a lot of complexity and it turned out that for this scenario, the simplest bounding box checking approach was good enough.
 

### Trajectory generation

Lorem ipsum dolor amet

## Simulator.
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