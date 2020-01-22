import unittest
from game import *
from main import *


class TestGame(unittest.TestCase):
    def _create_game(self, map):
        pg.init()
        screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        board, board_cells = create_board(screen)
        all_sprites = pg.sprite.RenderUpdates()
        return Game(board_cells, all_sprites, map)

    def test_game_over(self):
        game = self._create_game('test_maps/test_game_over.csv')
        game.handle_move('L')
        game.insert_new_tile()
        self.assertTrue(game.is_game_over())

    def test_combine_cells_1(self):
        game = self._create_game('test_maps/test_combine_cells_1.csv')
        game.handle_move('U')
        expected = [
            ['_', '_', '_', '4'],
            ['_', '_', '_', '4'],
            ['_', '_', '_', '_'],
            ['_', '_', '_', '_'],
        ]
        self.assertEqual(game.print_board(), expected)

    def test_combine_cells_2(self):
        game = self._create_game('test_maps/test_combine_cells_2.csv')
        game.handle_move('U')
        expected = [
            ['_', '_', '_', '8'],
            ['_', '_', '_', '4'],
            ['_', '_', '_', '_'],
            ['_', '_', '_', '_'],
        ]
        self.assertEqual(game.print_board(), expected)

    def test_combine_cells_3(self):
        game = self._create_game('test_maps/test_combine_cells_3.csv')
        game.handle_move('U')
        expected = [
            ['_', '_', '_', '4'],
            ['_', '_', '_', '4'],
            ['_', '_', '_', '_'],
            ['_', '_', '_', '_'],
        ]
        self.assertEqual(game.print_board(), expected)


if __name__ == "__main__":
    unittest.main()
