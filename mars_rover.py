
import sys
import os


class Plateau:
    """
    class to set the Plateau object coordinates
    """
    def __init__(self):
        """
        initialize variables
        """
        self.__bottom_left_x = 0
        self.__bottom_left_y = 0
        self.__upper_right_x = None
        self.__upper_right_y = None

    def set_upper_coordinates(self, upper_coordinates):
        """
        function to set Plateau upper right coordinates
        :param upper_coordinates: Plateau coordinates from input
        """
        try:
            upper_coordinates = upper_coordinates.strip().split(' ')

            # check to make sure user entered only x and y coordinates
            if len(upper_coordinates) != 2:
                raise ValueError
            self.__upper_right_x = int(upper_coordinates[0])
            self.__upper_right_y = int(upper_coordinates[1])

            # check upper right coordinates to make sure we have a proper Plateau
            if self.__upper_right_x < 0 or self.__upper_right_y < 0:
                raise ValueError

        except ValueError:  # catch exception if user didn't enter integers for coordinates and only two
            raise ValueError('You must enter x and y for Plateau upper-right coordinates e.g. 5 5. Please try again!\n')

    def get_coordinates(self) -> list:
        """
        function to return Plateau coordinates to be used in Rover object
        :return: array of Plateau coordinates -> [bottom left x, bottom left y, upper right x, upper right y]
        """
        return [self.__bottom_left_x, self.__bottom_left_y, self.__upper_right_x, self.__upper_right_y]


class Rover:
    """
    class to set Rover object -> landing, instructions and apply instructions to the Rover on the Plateau
    """
    def __init__(self):
        """
        initialize variables
        """
        self.__orientations = ['N', 'E', 'S', 'W']  # allowed orientation
        self.__controls = ['L', 'R', 'M']   # allowed instructions
        self.__plateau_bottom_left_x = None
        self.__plateau_bottom_left_y = None
        self.__plateau_upper_right_x = None
        self.__plateau_upper_right_y = None
        self.__rover_x = None
        self.__rover_y = None
        self.__rover_orientation = None
        self.__rover_instruction = None

    def set_plateau_coordinates(self, coordinates):
        """
        function to set Plateau coordinates to Rover object
        :param coordinates: coordinates from Plateau objects
        """
        self.__plateau_bottom_left_x = coordinates[0]
        self.__plateau_bottom_left_y = coordinates[1]
        self.__plateau_upper_right_x = coordinates[2]
        self.__plateau_upper_right_y = coordinates[3]

    def set_landing(self, landing):
        """
        function to set the Rover landing coordinates and its orientation
        :param landing: Rover landing coordinates and orientation from input
        """
        try:
            landing = landing.strip().split(' ')

            # check to make sure user entered x and y coordinates and also orientation
            if len(landing) != 3:
                raise ValueError

            self.__rover_x = int(landing[0])
            self.__rover_y = int(landing[1])
            self.__rover_orientation = landing[2].upper()

            # check the orientation to see if it is a allowed orientation
            if self.__rover_orientation not in self.__orientations:
                raise ValueError

            # check the Rover landing x coordinates to see if it falls into the Plateau x coordinates
            if not self.__plateau_bottom_left_x <= self.__rover_x <= self.__plateau_upper_right_x:
                raise ValueError

            # check the Rover landing y coordinates to see if it falls into the Plateau y coordinates
            if not self.__plateau_bottom_left_y <= self.__rover_y <= self.__plateau_upper_right_y:
                raise ValueError
        except ValueError:  # capture exception if user didn't enter right information for landing
            raise ValueError(
                'You must enter Rover landing coordinates and orientation. coordinates must fall into Plateau ' +
                'coordinates and orientation can be ["N", "E", "S", "W"]. N= North, E=East, S=South, W=West. ' +
                'e.g. 1 2 N for Plateau (5,5) and North facing. Please try again!\n'
            )

    def get_landing(self) -> list:
        """
        function to get the Rover landing information
        :return: array of landing info -> [rover x coordinate, rover y coordinate, rover orientation]
        """
        return [self.__rover_x, self.__rover_y, self.__rover_orientation]

    def set_instructions(self, instruction):
        """
        function to set the instructions that needs to be applied to the Rover
        :param instruction: Rover instruction from input
        """
        try:
            self.__rover_instruction = instruction.strip().upper()

            # check instructions to make sure they are valid instructions
            for instruction in self.__rover_instruction:
                if instruction not in self.__controls:
                    raise ValueError
        except ValueError:  # capture exception if user didn't enter right information for the instruction
            raise ValueError(
                'Navigation instructions can be in ["L", "R", "M"] e.g. LMLMLMLMRRM. ' +
                'L=Left, R=Right, M=Move. Please try again!\n'
            )

    def get_instruction(self) -> str:
        """
        function to return navigation instruction
        :return: navigation instruction string
        """
        return self.__rover_instruction

    def _new_orientation(self, current_orientation, navigate_to) -> str:
        """
        function to find the new orientation after 90 degrees left or right spin
        :param current_orientation: current orientation of the Rover
        :param navigate_to: spin 90 to left or right
        :return: desired orientation of the Rover
        """
        # spin 90 degrees to left
        if navigate_to == 'L':
            # used mod to return to end of the orientation array after the pointer reached to head
            return self.__orientations[(self.__orientations.index(current_orientation) - 1) % 4]
        # spin 90 degrees to right
        else:
            # used mod to return to head of the orientation array after the pointer reached to end
            return self.__orientations[(self.__orientations.index(current_orientation) + 1) % 4]

    def _move(self, orientation, x, y) -> tuple:
        """
        function to move Rover to desired location
        :param orientation: current facing of the Rover
        :param x: current x coordinate of the Rover
        :param y: current y coordinate of the Rover
        :return: new x and y coordinates or no change if hit the Plateau boundaries
        """
        # if the Rover is facing North and it didn't hit the Plateau upper right y coordinate
        if orientation == 'N' and y < self.__plateau_upper_right_y:
            return x, y + 1
        # if the Rover is facing South and it didn't hit the Plateau bottom left y coordinate
        elif orientation == 'S' and y > self.__plateau_bottom_left_y:
            return x, y - 1
        # if the Rover is facing East and it didn't hit the Plateau upper right x coordinate
        elif orientation == 'E' and x < self.__plateau_upper_right_x:
            return x + 1, y
        # if the Rover is facing West and Rover didn't hit the Plateau bottom left x coordinate
        elif orientation == 'W' and x > self.__plateau_bottom_left_x:
            return x - 1, y
        return x, y

    def apply_instructions(self) -> tuple:
        """
        apply instruction to the Rover
        :return: the Rover final x and y and also its orientation -> x coordinate, y coordinate, orientation
        """
        for instruction in self.__rover_instruction:
            if instruction == 'M':
                self.__rover_x, self.__rover_y = self._move(self.__rover_orientation, self.__rover_x, self.__rover_y)
            else:
                self.__rover_orientation = self._new_orientation(self.__rover_orientation, instruction)
        return self.__rover_x, self.__rover_y, self.__rover_orientation


def get_input() -> list:
    """
    function to get input data either from command line or file
    :return: array of input data
    """
    if len(sys.argv) != 2:
        raise ValueError('Missing input data. To run: python mars_rover.py <arg1>. arg1 is a file or input data')

    # read the Plateau and Rover data from file if file exists otherwise read the input from command line
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], 'r') as input_file:
            plateau_rover_data = [line.strip().split(':')[1] for line in input_file.readlines() if line.strip()]
    else:
        plateau_rover_data = [line.strip().split(':')[1] for line in sys.argv[1].split('\n') if line.strip()]

    # reverse the plateau_rover_data array to be able to use pop() function
    plateau_rover_data.reverse()

    return plateau_rover_data


def run_mars_rover(plateau_rover_data):
    """
    function to read rovers' data and apply the instruction
    assumptions:
        - one Rover can move at a time and finishes its instructions and then next Rover starts its instructions.
        - collision is acceptable which means if Rover1 is in 1,3 grid, Rover2 can come to the same grid or pass
            the grid.
    possible scenarios that we can change the above behavior:
        - Rovers can move at the same time.
        - each Rover moves once at a time and then the next Rover moves
        - apply one instruction at a time for a Rover then apply one instruction for the next Rover
    possible changes for above scenarios
        - If collision is acceptable, there won't be any changes in the main Rover class functions however
            ``apply_instructions`` function needs to be updated in order to apply instruction in the desired format.
        - If collision is NOT acceptable, there needs to be a change in Rover class especially ``move`` function
            to prevent collision or in some scenarios a Rover can be blocked completely if there is already another
            Rover in a grid that the other Rover wants to surfs. Also there needs to be a change in
            ``apply_instructions`` like above.

    :param plateau_rover_data: input data
    """

    results = []

    # set Plateau coordinates - get the first element from plateau_rover_data which is plateau coordinates
    plateau = Plateau()
    plateau.set_upper_coordinates(plateau_rover_data.pop())
    plateau_coordinates = plateau.get_coordinates()

    # for loop to run for each Rover. For each Rover, there is two lines of input hence divide by 2
    for i in range(0, int(len(plateau_rover_data) / 2)):
        rover = Rover()
        rover.set_plateau_coordinates(plateau_coordinates)
        rover.set_landing(plateau_rover_data.pop())
        rover.set_instructions(plateau_rover_data.pop())
        rover_x, rover_y, rover_orientation = rover.apply_instructions()
        results.append(
            'Rover{i}:{x} {y} {orientation}'.format(i=i + 1, x=rover_x, y=rover_y, orientation=rover_orientation)
        )
    return results


if __name__ == '__main__':

    try:
        res = run_mars_rover(get_input())
        print(*res, sep="\n")
    except Exception as e:
        raise
