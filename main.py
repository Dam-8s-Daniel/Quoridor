#Author: Daniel Dam
#Last Updated: 9/18/21
#Description: This file executes Quoridor with an UI using pygame.

import Quoridor as q
import pygame, sys
from pygame.locals import *


FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 630 # size of window's width in pixels
WINDOWHEIGHT = 630 # size of windows' height in pixels
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels (where fences will be placed)
BOARDWIDTH = 9 # number of columns of boxes
BOARDHEIGHT = 9 # number of rows of boxes
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
distance_between_corners = WINDOWWIDTH / BOARDWIDTH
vertical_fences = []
horizontal_fences = []



GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (220,   48,   48)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
TEAL     = (  0, 128, 128)
BLACK    = (  0,   0,   0)



def main():
    """Main game loop that initializes pygame and Quoridor."""
    global FPSCLOCK, DISPLAYSURF, FONT

    pygame.init()
    Quoridor = q.QuoridorGame()
    mainBoard = mainBoardRepresentation(Quoridor.get_squares())

    FPSCLOCK = pygame.time.Clock()
    FONT = pygame.font.Font('freesansbold.ttf', 17)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(TEAL)
    pygame.display.set_caption("Quoridor")

    mouseX = 0
    mouseY = 0


    while True:
        mouseClicked = False
        add_vertical_fence = False
        add_horizontal_fence = False
        DISPLAYSURF.fill(TEAL)
        drawBoard(mainBoard)
        draw_vertical_fences(Quoridor)
        draw_horizontal_fences(Quoridor)
        show_fences(Quoridor)
        show_player_turn(Quoridor)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True

        vertical_fence_wanted, vfence = vertical_fence_pressed(mouseX, mouseY)
        horizontal_fence_wanted, hfence = horizontal_fence_pressed(mouseX, mouseY)
        player = Quoridor.get_player_turn()
        box_coordinates = getBoxAtPixel(mouseX, mouseY)
        v_fence_coordinates = getBoxAtPixel_for_vertical_grid(mouseX, mouseY)
        h_fence_coordinates = getBoxAtPixel_for_horizontal_grid(mouseX, mouseY)

        if mouseClicked and vertical_fence_wanted != None:
            if Quoridor.place_fence(player, vertical_fence_wanted, v_fence_coordinates):
                pygame.draw.rect(DISPLAYSURF, BLACK, vfence)
                mouseClicked = False


        if mouseClicked and horizontal_fence_wanted != None:
            if Quoridor.place_fence(player, horizontal_fence_wanted, h_fence_coordinates):
                pygame.draw.rect(DISPLAYSURF, BLACK, hfence)
                mouseClicked = False


        elif mouseClicked and Quoridor.move_pawn(player, box_coordinates):
            drawBoard(mainBoard)
            mouseClicked = False


        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainBoardRepresentation(squares:list):
    """
    Creates an internal representation of the board as a list of 9x9 lists containing the class Square, which
    represents a square in Quoridor.
    p1: squares -- list of all the Square objects made when Quoridor was initialized.
    """
    count = 0
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(squares[y+count])
        board.append(column)
        count += BOARDWIDTH
    return board


def drawBoard(mainBoard):
    """
    Draws all the boxes in the game based on board made from mainBoardRepresentation.
    """
    for boxX in range(BOARDWIDTH):
        for boxY in range(BOARDHEIGHT):
            x, y = leftTopCoordsOfBox(boxX, boxY)
            if mainBoard[boxY][boxX].get_pawn() == 1:
                pygame.draw.rect(DISPLAYSURF, RED, (x, y, BOXSIZE, BOXSIZE))
            elif mainBoard[boxY][boxX].get_pawn() == 2:
                pygame.draw.rect(DISPLAYSURF, BLUE, (x, y, BOXSIZE, BOXSIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, BOXSIZE, BOXSIZE))


def vertical_fence_pressed(mouseX, mouseY):
    """
    Determines if the user pressed a space that can contain a vertical fence.
    """
    for fence in vertical_fences:
        if fence.collidepoint(mouseX, mouseY):
            return 'v', fence
    return None, None


def horizontal_fence_pressed(mouseX, mouseY):
    """
    Determines if the user pressed a space that can contain a horizontal fence.
    """
    for fence in horizontal_fences:
        if fence.collidepoint(mouseX, mouseY):
            return 'h', fence
    return None, None


def draw_vertical_fences(Quoridor):
    """Draws all the vertical fences that are placed on the board."""
    for boxX in range(BOARDWIDTH):
        for boxY in range(BOARDHEIGHT):
            x, y = leftTopCoordsOfBox_for_vertical_grid(boxX, boxY)
            fenceRect = pygame.Rect(x, y, GAPSIZE, BOXSIZE)
            if (boxX, boxY) in Quoridor.get_vFences():
                pygame.draw.rect(DISPLAYSURF, BLACK, fenceRect)
            else:
                vertical_fences.append(fenceRect)


def draw_horizontal_fences(Quoridor):
    """Draws all the horizontal fences that are placed on the board."""
    for boxX in range(BOARDWIDTH):
        for boxY in range(BOARDHEIGHT):
            x, y = leftTopCoordsOfBox_for_horizonal_grid(boxX, boxY)
            fenceRect = pygame.Rect(x, y, BOXSIZE, GAPSIZE)
            if (boxX, boxY) in Quoridor.get_hFences():
                pygame.draw.rect(DISPLAYSURF, BLACK, fenceRect)
            else:
                horizontal_fences.append(fenceRect)


def leftTopCoordsOfBox_for_vertical_grid(boxx, boxy):
    """Converts board coordinates to pixel coordinates for vertical fences."""
    x = boxx * (BOXSIZE + GAPSIZE) + XMARGIN - GAPSIZE
    y = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return x, y


def leftTopCoordsOfBox_for_horizonal_grid(boxx, boxy):
    """Converts board coordinates to pixel coordinates for horizontal fences."""
    x = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    y = boxy * (BOXSIZE + GAPSIZE) + YMARGIN - GAPSIZE
    return x, y


def getBoxAtPixel_for_vertical_grid(x, y):
    """Function returns the vertical fence coordinates corresponding to the pixels that were clicked, if any."""
    #returns box coordinates (not pixel coordinates!)
    #uses leftTopCoordsofBox
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            x_pixel, y_pixel = leftTopCoordsOfBox_for_vertical_grid(boxx, boxy)
            boxRect = pygame.Rect(x_pixel, y_pixel, GAPSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def getBoxAtPixel_for_horizontal_grid(x, y):
    """Function returns the horizontal fence coordinates corresponding to the pixels that were clicked, if any."""
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            x_pixel, y_pixel = leftTopCoordsOfBox_for_horizonal_grid(boxx, boxy)
            boxRect = pygame.Rect(x_pixel, y_pixel, BOXSIZE, GAPSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def leftTopCoordsOfBox(boxx, boxy):
    """Converts board coordinates of boxes to pixel coordinates"""
    x = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    y = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return x, y


def getBoxAtPixel(x, y):
    """Returns box coordinates"""
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            x_pixel, y_pixel = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(x_pixel, y_pixel, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def show_fences(Quoridor_game_object):
    """Displays the number of fences each player has in the game."""
    p1_score = FONT.render("P1 Fences:" + str(Quoridor_game_object.get_fence_inventory(1)), True, RED)
    p2_score = FONT.render("P2 Fences:" + str(Quoridor_game_object.get_fence_inventory(2)), True, BLUE)
    DISPLAYSURF.blit(p1_score, (BOXSIZE + WINDOWWIDTH/100, BOXSIZE + BOXSIZE/3))
    DISPLAYSURF.blit(p2_score, ((WINDOWWIDTH * .80) - BOXSIZE, BOXSIZE + BOXSIZE/3))


def show_player_turn(Quoridor_game_object):
    """Displays which player is moving or who won the game."""
    player = str(Quoridor_game_object.get_player_turn())
    game_won = Quoridor_game_object.get_game_won()
    color = None
    if game_won is False:
        if player == "1":
            color = RED
        elif player == "2":
            color = BLUE
        display_turn = FONT.render("Player Turn: P" + player, True, color)
        DISPLAYSURF.blit(display_turn, (WINDOWWIDTH * .4, WINDOWHEIGHT *.9))
    elif game_won:
        if Quoridor_game_object.is_winner(1):
            winner_prompt = FONT.render("Player 1 won!", True, RED)
            DISPLAYSURF.blit(winner_prompt, (WINDOWWIDTH * .4, WINDOWHEIGHT *.9))
        elif Quoridor_game_object.is_winner(2):
            winner_prompt = FONT.render("Player 2 won!", True, BLUE)
            DISPLAYSURF.blit(winner_prompt, (WINDOWWIDTH * .4, WINDOWHEIGHT *.9))



if __name__ == '__main__':
    main()
