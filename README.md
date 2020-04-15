## Mars Rover

A squad of robotic rovers are to be landed by NASA on a plateau on Mars.

This plateau, which is curiously rectangular, must be navigated by the rovers so that their on board cameras can get a complete view of the surrounding terrain to send back to Earth.

A rover's position is represented by a combination of an x and y co-ordinates and a letter representing one of the four cardinal compass points. The plateau is divided up into a grid to simplify navigation. An example position might be 0, 0, N, which means the rover is in the bottom left corner and facing North.

In order to control a rover, NASA sends a simple string of letters. The possible letters are 'L', 'R' and 'M'. 'L' and 'R' makes the rover spin 90 degrees left or right respectively, without moving from its current spot.

'M' means move forward one grid point, and maintain the same heading.

Assume that the square directly North from (x, y) is (x, y+1).

Input:

Configuration Input: The first line of input is the upper-right coordinates of the plateau, the lower-left coordinates are assumed to be 0,0.

Per Rover Input:

Input 1: Landing co-ordinates for the named Rover. The position is made up of two integers and a letter separated by spaces, corresponding to the x and y co-ordinates and the rover's orientation.

Input 2: Navigation instructions for the named rover. i.e a string containing ('L', 'R', 'M').

### How to run the app
To run the application you need to have **Python3.7+**.

#### Test input from command line:
```
$ python mars_rover.py "Plateau:5 5
Rover1 Landing:1 2 N
Rover1 Instructions:LMLMLMLMM
Rover2 Landing:3 3 E
Rover2 Instructions:MMRMMRMRRM"
```

#### Test input from a file:
```
$ python mars_rover.py input.txt
```

#### Expected Output:
```
Rover1:1 3 N
Rover2:5 1 E
```

#### Unit Test:
```
$ python mars_rover_unittest.py
```
### Assumptions:

- ``Rovers`` can land in the same grid as they can have different instructions.
- One Rover can move at a time and finishes its instructions and then next Rover starts its instructions.
- Collision is acceptable which means if Rover1 is in 1,3 grid, Rover2 can come to the same grid or pass the grid.

### Other possible scenarios:

- ``Rovers`` cannot land in the same grid.
- ``Rovers`` can move at the same time.
- Each ``Rover`` moves once at a time and then the next Rover moves.
- Apply one instruction at a time for each Rover (then apply one instruction for the next Rover).
- If a ``Rover`` cannot end at a grid that already have a ``Rover`` in it.
 
#### Changes that are needed for the above scenarios:

- If collision is **acceptable**, there won't be any changes in the main ``Rover`` class functions however ``apply_instructions`` function needs to be updated in order to apply instruction in the desired format.
- If collision is **NOT acceptable**, there needs to be a change in ``Rover`` class especially ``move`` function to prevent collision and add check for each move to avoid collision (if we do have simultaneous move, each move needs to be checked to make sure that there is no collision) or in some scenarios a Rover can be blocked completely if there is already another Rover in a grid that the other Rover wants to move (like if ``Rover`` cannot end at the same grid, the last ``move`` needs to be checked). Also there needs to be a change in ``apply_instructions`` like above. 
- If ``Rovers`` cannot land at the same spot, then there needs to be a check in ``set_landing`` method in the ``Rover`` class.
