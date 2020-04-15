
import unittest

import mars_rover


class TestPlateau(unittest.TestCase):

    def setUp(self):
        self.plateau = mars_rover.Plateau()

    def test_invalid_get_coordinates(self):
        self.plateau.set_upper_coordinates('7 7')
        self.assertNotEqual(self.plateau.get_coordinates(), [0, 0, 5, 5])

    def test_coordinates_input_not_equal_to_two(self):
        self.assertRaises(ValueError, self.plateau.set_upper_coordinates, '5 5 3')

    def test_coordinates_less_than_zero(self):
        self.assertRaises(ValueError, self.plateau.set_upper_coordinates, '-1 -1')

    def test_coordinates_not_integer(self):
        self.assertRaises(ValueError, self.plateau.set_upper_coordinates, 'S a')

    def test_valid_coordinates(self):
        self.plateau.set_upper_coordinates('6 6')
        self.assertEqual(self.plateau.get_coordinates(), [0, 0, 6, 6])

    def test_invalid_coordinates(self):
        self.assertRaises(ValueError, self.plateau.set_upper_coordinates, '-1 -1')


class TestRover(unittest.TestCase):

    def setUp(self):
        self.rover = mars_rover.Rover()
        self.rover.set_plateau_coordinates([0, 0, 5, 5])

    def test_valid_landing(self):
        self.rover.set_landing('1 2 N')
        self.assertEqual(self.rover.get_landing(), [1, 2, 'N'])

    def test_invalid_landing_from_file(self):
        self.assertRaises(ValueError, self.rover.set_landing, '5 5')

    def test_landing_input_not_equal_to_three(self):
        self.assertRaises(ValueError, self.rover.set_landing, '1 N')

    def test_landing_coordinates_not_integer(self):
        self.assertRaises(ValueError, self.rover.set_landing, '1 W N')

    def test_landing_not_valid_orientation(self):
        self.assertRaises(ValueError, self.rover.set_landing, '1 2 Q')

    def test_landing_x_coordinates_out_of_plateau(self):
        self.assertRaises(ValueError, self.rover.set_landing, '6 2 N')

    def test_landing_y_coordinates_out_of_plateau(self):
        self.assertRaises(ValueError, self.rover.set_landing, '1 6 N')

    def test_valid_instruction(self):
        self.rover.set_instructions('LMLMLMLMM')
        self.assertEqual(self.rover.get_instruction(), 'LMLMLMLMM')

    def test_invalid_instruction_control(self):
        self.assertRaises(ValueError, self.rover.set_instructions, 'LMLMLMLMQ')

    def test_valid_navigation(self):
        self.assertEqual(self.rover._new_orientation('N', 'L'), 'W')
        self.assertEqual(self.rover._new_orientation('N', 'R'), 'E')
        self.assertEqual(self.rover._new_orientation('W', 'L'), 'S')
        self.assertEqual(self.rover._new_orientation('W', 'R'), 'N')
        self.assertEqual(self.rover._new_orientation('S', 'L'), 'E')
        self.assertEqual(self.rover._new_orientation('S', 'R'), 'W')
        self.assertEqual(self.rover._new_orientation('E', 'L'), 'N')
        self.assertEqual(self.rover._new_orientation('E', 'R'), 'S')

    def test_invalid_navigation(self):
        self.assertNotEqual(self.rover._new_orientation('N', 'L'), 'N')
        self.assertNotEqual(self.rover._new_orientation('N', 'R'), 'S')
        self.assertNotEqual(self.rover._new_orientation('W', 'L'), 'W')
        self.assertNotEqual(self.rover._new_orientation('W', 'R'), 'E')
        self.assertNotEqual(self.rover._new_orientation('S', 'L'), 'N')
        self.assertNotEqual(self.rover._new_orientation('S', 'R'), 'S')
        self.assertNotEqual(self.rover._new_orientation('E', 'L'), 'W')
        self.assertNotEqual(self.rover._new_orientation('E', 'R'), 'E')

    def test_navigation_return_type(self):
        self.assertIsInstance(self.rover._new_orientation('N', 'L'), str)

    def test_valid_move(self):
        self.assertEqual(self.rover._move('N', 1, 2), (1, 3))
        self.assertEqual(self.rover._move('N', 1, 5), (1, 5))
        self.assertEqual(self.rover._move('S', 1, 2), (1, 1))
        self.assertEqual(self.rover._move('S', 1, 0), (1, 0))
        self.assertEqual(self.rover._move('E', 1, 2), (2, 2))
        self.assertEqual(self.rover._move('E', 5, 1), (5, 1))
        self.assertEqual(self.rover._move('W', 1, 2), (0, 2))
        self.assertEqual(self.rover._move('W', 0, 2), (0, 2))

    def test_invalid_move(self):
        self.assertNotEqual(self.rover._move('N', 1, 2), (1, 2))
        self.assertNotEqual(self.rover._move('N', 1, 5), (1, 6))
        self.assertNotEqual(self.rover._move('S', 1, 2), (1, 2))
        self.assertNotEqual(self.rover._move('S', 1, 0), (1, 1))
        self.assertNotEqual(self.rover._move('E', 1, 2), (1, 2))
        self.assertNotEqual(self.rover._move('E', 5, 1), (4, 1))
        self.assertNotEqual(self.rover._move('W', 1, 2), (1, 2))
        self.assertNotEqual(self.rover._move('W', 0, 2), (1, 2))

    def test_apply_instruction(self):
        self.rover.set_landing('1 2 N')
        self.rover.set_instructions('LMLMLMLMM')
        self.assertEqual(self.rover.apply_instructions(), (1, 3, 'N'))


class MarsRover(unittest.TestCase):

    def test_valid_result_from_problem(self):
        input_data = ['MMRMMRMRRM', '3 3 E', 'LMLMLMLMM', '1 2 N', '5 5']
        expected_output = ['Rover1:1 3 N', 'Rover2:5 1 E']
        self.assertEqual(mars_rover.run_mars_rover(input_data), expected_output)

    def test_invalid_result(self):
        input_data = ['MMRMMRMRRM', '3 3 E', 'LMLMLMLMM', '1 2 N', '5 5']
        unexpected_output = ['Rover1:1 2 N', 'Rover2:5 0 E']
        self.assertNotEqual(mars_rover.run_mars_rover(input_data), unexpected_output)

    def test_valid_case_1(self):
        input_data = ['M', '3 3 E', 'L', '1 2 N', '5 5']
        expected_output = ['Rover1:1 2 W', 'Rover2:4 3 E']
        self.assertEqual(mars_rover.run_mars_rover(input_data), expected_output)

    def test_valid_case_2(self):
        input_data = ['MR', '3 3 E', 'LM', '1 2 N', '5 5']
        expected_output = ['Rover1:0 2 W', 'Rover2:4 3 S']
        self.assertEqual(mars_rover.run_mars_rover(input_data), expected_output)

    def test_valid_case_3(self):
        input_data = ['LR', '3 3 N', 'RL', '1 2 S', '5 5']
        expected_output = ['Rover1:1 2 S', 'Rover2:3 3 N']
        self.assertEqual(mars_rover.run_mars_rover(input_data), expected_output)


if __name__ == '__main__':
    unittest.main()
