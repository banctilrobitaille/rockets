# Club RockETS base station <img src="/image/logo.png" width="60" vertical-align="bottom">

>This project is a python project developped for a student club called RockETS at ETS (École de Technologie Supérieure).
RockETS participate anually to the IREC (Intercollegiate Rocket Engineering Competition). 
The goal of the competition is to develop, build and launch a sounding rocket, reach a precise altitude,
perform a scientific experience during the flight and recover the rocket in good shape. To do so, tracking the 
rocket is essential. This project is the base station that will be used to track the rocket during the flight, 
send command to the rocket, get telemetry data, review the logs, etc., using different serial devices such as 
RFD900 and xbee.

## Libraries
* PyQt4
* PyQwt
* Basemap
* Matplotlib

## Contributing

#### How to contribute ?
- [X] Install Python 2.7.x
- [X] Install the libs
- [X] Create a branch by feature and/or bug fix
- [X] Get the code
- [X] Commit and push
- [X] Create a pull request

#### Branch naming

##### Feature branch
> feature/ [Short feature description] [Issue number]

##### Bug branch
> bugfix/ [Short fix description] [Issue number]

#### Commits syntax:

##### Adding code:
> \+ Added [Short Description] [Issue Number]

##### Deleting code:
> \- Deleted [Short Description] [Issue Number]

##### Modifying code:
> \* Changed [Short Description] [Issue Number]

## Look and feel

#### Rockets BaseStation V1.0
##### Overview
![GitHub Logo](/image/overview.PNG)

## Features
- [X] Live rocket and basestation tracking
- [X] Live baseStation GPS satellites and fix status
- [X] Multi rockets support
- [X] Remote 360 Camera start
- [X] Remote telemetry stream start
- [X] Custom animated error messaging system
- [X] Live graphs and dials
- [X] Robust multithreaded communication protocol
- [X] Live rocket state monitoring
- [ ] Live motherboard temperature sensor monitoring
- [ ] Live payload data monitoring
- [ ] Flight report creation
- [ ] 3D flight data representation
