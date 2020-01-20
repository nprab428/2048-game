import pygame as pg
from collections import namedtuple

from constants import *
from utils import *
from tile import Tile
from game import *


def create_board(screen):
    board = pg.Surface((BOARD_LENGTH, BOARD_LENGTH))
    board.fill(BOARD_COLORS['background'])
    # create cells in COLUMN MAJOR order
    board_cells = [[None]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            x = i*CELL_LENGTH + (i+1)*PADDING
            y = j * CELL_LENGTH + (j + 1) * PADDING
            empty_cell = pg.Surface((CELL_LENGTH, CELL_LENGTH))
            empty_cell.fill(BOARD_COLORS['empty'])
            board.blit(empty_cell, (x, y))
            # store rect of the empty cell in board_cells
            board_cells[i][j] = empty_cell.get_rect()
            board_cells[i][j].topleft = BOARD_MARGIN+x, BOARD_MARGIN+y
    screen.blit(board, (BOARD_MARGIN, BOARD_MARGIN))
    return board, board_cells


def create_menu(screen):
    menu_font = pg.font.Font(None, MENU_FONT_SIZE)

    def create_menu_button(text):
        button = pg.Surface(
            (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT))
        button.fill(MENU_BUTTON_COLOR)
        menu_text = menu_font.render(text, True, MENU_TEXT_COLOR)
        center_text(menu_text, button)
        return button

    # create New Game button
    new_game_button = create_menu_button('New Game')
    new_game_button_pos = new_game_button.get_rect(
        center=(NEW_GAME_BUTTON_POS_X, NEW_GAME_BUTTON_POS_Y))
    screen.blit(new_game_button, new_game_button_pos.topleft)

    # create AI Mode button
    AI_mode_button = create_menu_button('AI Mode')
    AI_mode_button_pos = AI_mode_button.get_rect(
        center=(AI_MODE_BUTTON_POS_X, AI_MODE_BUTTON_POS_Y))
    screen.blit(AI_mode_button, AI_mode_button_pos.topleft)

    # return rects for each button
    return new_game_button_pos, AI_mode_button_pos


def create_game_over_message(screen):
    background = pg.Surface(
        (GAME_OVER_BACKGROUND_WIDTH, GAME_OVER_BACKGROUND_HEIGHT))
    background.fill(GAME_OVER_BACKGROUND_COLOR)
    game_over_font = pg.font.Font(None, GAME_OVER_FONT_SIZE)
    game_over_str = 'Game over :( would you like to play again?'
    game_over_text = game_over_font.render(
        game_over_str, True, GAME_OVER_TEXT_COLOR)
    center_text(game_over_text, background)

    game_over_pos = background.get_rect(
        center=((GAME_OVER_POS_X, GAME_OVER_POS_Y)))
    return background, game_over_pos.topleft


def main():
    # init pygame
    pg.init()
    pg.display.set_caption('2048')

    # create background
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    # create board
    board, board_cells = create_board(screen)
    # create menu
    new_game, AI_mode = create_menu(screen)
    game_over, game_over_pos = create_game_over_message(screen)

    # initialize Game
    all_sprites = pg.sprite.RenderUpdates()
    game = Game(board_cells, all_sprites)

    running = True
    arrow_keys = [pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT, pg.K_UP]
    moves = []
    should_insert = False
    while running:
        # determine if new tile insert is required
        any_moving = any(s.is_moving() for s in all_sprites)
        if should_insert and not any_moving:
            game.insert_new_tile()
            should_insert = False

        # process event keys
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if new_game.collidepoint(mouse_pos):
                    game.new_game()

            if event.type == pg.KEYDOWN and event.key in arrow_keys and not any_moving:
                if event.key == pg.K_DOWN:
                    dir = 'D'
                if event.key == pg.K_RIGHT:
                    dir = 'R'
                if event.key == pg.K_UP:
                    dir = 'U'
                if event.key == pg.K_LEFT:
                    dir = 'L'

                moves = game.handle_move(dir)
                for move in moves:
                    should_insert = True
                    tile = move.tile
                    tile.handle_move(move)

        # update tiles
        all_sprites.update()

        # redraw board
        screen.blit(board, (BOARD_MARGIN, BOARD_MARGIN))
        all_sprites.draw(screen)

        if game.is_game_over():
            screen.blit(game_over, game_over_pos)
        pg.display.update()


if __name__ == "__main__":
    main()
