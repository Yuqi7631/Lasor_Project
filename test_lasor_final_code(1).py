import unittest
from lasor_final_code import (
    grid_info,
    Laser,
    Block,
    Grid,
    move_lasers,
    check_solution,
)


class TestLazorGame(unittest.TestCase):
    def setUp(self):

        self.grid_content = [
            ["x", "x", "x", "x"],
            ["x", "A", " ", "x"],
            ["x", " ", "C", "x"],
            ["x", "x", "x", "x"],
        ]
        self.grid = Grid(self.grid_content, 4, 4)
        self.laser = Laser(1, 1, 1, 0)
        self.block = Block("A", 2, 1)

    def test_grid_info(self):
        (
            grid_content,
            A_value,
            B_value,
            C_value,
            L_value,
            P_value,
            column,
            row,
        ) = grid_info("yarn_5.bff")
        self.assertTrue(len(grid_content) > 0)
        self.assertEqual(A_value, 8)

    def test_laser_move(self):
        self.laser.move()
        self.assertEqual(self.laser.x, 2)
        self.assertEqual(self.laser.y, 1)

    def test_block_interaction(self):
        reflected_laser = self.block.interact_with_laser(self.laser)
        self.assertIsNone(reflected_laser)
        self.assertEqual(self.laser.vx, -1)

    def test_grid_creation(self):

        self.grid.place_block("A", 1, 1)
        self.assertIsInstance(self.grid.grid_blocks[3][3], Block)
        self.assertEqual(self.grid.grid_blocks[3][3].type, "A")
        self.assertIsNone(self.grid.grid_blocks[1][2])

    def test_move_lasers(self):
        lasers = [Laser(1, 1, 1, 0)]
        paths = move_lasers(self.grid.grid_blocks, lasers)
        self.assertIn((2, 1), paths)

    def test_check_solution(self):
        lasers = [Laser(1, 1, 1, 0)]
        targets = {(2, 1)}
        is_solved, paths = check_solution(
            self.grid.grid_blocks, lasers, targets
        )
        self.assertTrue(is_solved)


if __name__ == "__main__":
    unittest.main()
