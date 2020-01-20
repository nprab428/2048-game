from constants import *
from collections import namedtuple


def relative_coords(coords1, coords2):
    return (coords1[0] - coords2[0], coords1[1] - coords2[1])


def compute_board_pixels(loc_x, loc_y):
    # compute top_left coord of the cell with coords (loc_x, loc_y)
    top_left_x = BOARD_MARGIN + (loc_x+1)*PADDING + loc_x*CELL_LENGTH
    top_left_y = BOARD_MARGIN + (loc_y + 1) * PADDING + loc_y * CELL_LENGTH
    return top_left_x, top_left_y


def center_text(text, background):
    background_rect = background.get_rect()
    text_pos = text.get_rect(center=background_rect.center)
    background.blit(text, relative_coords(
        text_pos.topleft, background_rect.topleft))


# TODO better formatted comments
# Single move instruction executed by a tile
# holds a tile-sprite, its destination coords, and a nullable absorbing tile
# that's used if the current tile combines with another
Move = namedtuple('Move', ['tile', 'dest_x', 'dest_y', 'absorbing_tile'])
