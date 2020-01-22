import pygame as pg
from constants import *
from utils import *


class Tile(pg.sprite.Sprite):
    def __init__(self, coords_x, coords_y, board, num=2):
        pg.sprite.Sprite.__init__(self)
        # (coords_x, coord_y) reflect tile coords on board
        self.coords_x, self.coords_y = coords_x, coords_y
        self.board = board
        self.num = num
        self.speed = 0
        self.moving = False
        # (target_x, target_y) and (cur_x, cur_y) are the top-left pixels of coords
        self.target_x, self.target_y = compute_board_pixels(coords_x, coords_y)
        # since tile is initially stationary, (cur_x, cur_y) = (target_x, target_y)
        self.cur_x, self.cur_y = self.target_x, self.target_y

        self.image = pg.Surface((CELL_LENGTH, CELL_LENGTH))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.cur_x, self.cur_y
        self.update()

    def double_value(self):
        self.num *= 2

    def is_moving(self):
        return self.cur_x != self.target_x or self.cur_y != self.target_y

    def _set_font(self):
        if len(str(self.num)) < 4:
            self.font = pg.font.Font(None, TILE_LARGE_FONT_SIZE)
        else:
            self.font = pg.font.Font(None, TILE_SMALL_FONT_SIZE)

    def _color_tile(self):
        self.image.fill(TILE_COLORS[self.num]['fill'])
        self._set_font()
        self.text = self.font.render(
            str(self.num), True, TILE_COLORS[self.num]['text'])
        center_text(self.text, self.image)

    def handle_move(self, move):
        self.coords_x, self.coords_y = move.dest_x, move.dest_y
        self.target_x, self.target_y = compute_board_pixels(
            move.dest_x, move.dest_y)
        self.speed = max(abs(self.target_x - self.cur_x),
                         abs(self.target_y-self.cur_y))/TILE_MOVE_TIME
        self.absorbing_tile = move.absorbing_tile

    def update(self):
        if self.is_moving():
            # compute direction
            if self.cur_x == self.target_x:
                if self.cur_y < self.target_y:
                    # move down
                    dx, dy = 0, self.speed
                    has_finished = self.cur_y + self.speed >= self.target_y
                else:
                    # move up
                    dx, dy = 0, -self.speed
                    has_finished = self.cur_y - self.speed <= self.target_y
            else:
                if self.cur_x < self.target_x:
                    # move right
                    dx, dy = self.speed, 0
                    has_finished = self.cur_x + self.speed >= self.target_x
                else:
                    # move left
                    dx, dy = -self.speed, 0
                    has_finished = self.cur_x - self.speed <= self.target_x

            # perform move
            if not has_finished:
                self.rect.move_ip((dx, dy))
                self.cur_x += dx
                self.cur_y += dy
            else:
                if self.absorbing_tile:
                    self.absorbing_tile.double_value()
                    self.kill()
                else:
                    self.rect.clamp_ip(
                        self.board[self.coords_x][self.coords_y])
                    self.cur_x = self.target_x
                    self.cur_y = self.target_y

        # color tile according to number value
        self._color_tile()
