from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
import random
from GLFW import *

# Window dimensions
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 900
CELL_SIZE = 75  # Each cell in the grid is 75x75 pixels
CELL_SIZE_2 = 55
BOARD_OFFSET_Y = -10  # Move the board upwards by 10 pixels

player_number_printed = False
can_move_coins = False

# Game state variables
current_dice_value = 1
current_player = 0  # 0 for Yellow, 1 for Red, 2 for Green, 3 for Blue
consecutive_sixes = 0
blinking = True  # Start with blinking to indicate the player's turn
blink_state = True  # To toggle the blinking effect
blink_timer = 0  # Timer for blinking

dx1 = 54
dx2 = 55
dx3 = 50
dy1 = 54
dy2 = 55
dy3 = 50

player_yellow=[]
player_red=[]
player_green=[]
player_blue=[]



# Coins
coins = [

    # Yellow coins

    {"x": 135, "y": BOARD_OFFSET_Y + 135, "size": 20, "color": (0.8, 0.8, 0)},
    {"x": 205, "y": BOARD_OFFSET_Y + 135, "size": 20, "color": (0.8, 0.8, 0)},
    {"x": 135, "y": BOARD_OFFSET_Y + 205, "size": 20, "color": (0.8, 0.8, 0)},
    {"x": 205, "y": BOARD_OFFSET_Y + 205, "size": 20, "color": (0.8, 0.8, 0)},

    # Red coins

    {"x": 625, "y": BOARD_OFFSET_Y + 135, "size": 20, "color": (0.8, 0, 0)},
    {"x": 695, "y": BOARD_OFFSET_Y + 135, "size": 20, "color": (0.8, 0, 0)},
    {"x": 625, "y": BOARD_OFFSET_Y + 205, "size": 20, "color": (0.8, 0, 0)},
    {"x": 695, "y": BOARD_OFFSET_Y + 205, "size": 20, "color": (0.8, 0, 0)},

    # Green coins

    {"x": 625, "y": BOARD_OFFSET_Y + 625, "size": 20, "color": (0, 0.8, 0)},
    {"x": 695, "y": BOARD_OFFSET_Y + 625, "size": 20, "color": (0, 0.8, 0)},
    {"x": 625, "y": BOARD_OFFSET_Y + 695, "size": 20, "color": (0, 0.8, 0)},
    {"x": 695, "y": BOARD_OFFSET_Y + 695, "size": 20, "color": (0, 0.8, 0)},

    # Blue coins

    {"x": 135, "y": BOARD_OFFSET_Y + 625, "size": 20, "color": (0, 0, 0.8)},
    {"x": 205, "y": BOARD_OFFSET_Y + 625, "size": 20, "color": (0, 0, 0.8)},
    {"x": 135, "y": BOARD_OFFSET_Y + 695, "size": 20, "color": (0, 0, 0.8)},
    {"x": 205, "y": BOARD_OFFSET_Y + 695, "size": 20, "color": (0, 0, 0.8)},

]


# New starting positions for each player's coins
STARTING_POSITIONS = {
    "yellow": [[135, BOARD_OFFSET_Y + 135], [205, BOARD_OFFSET_Y + 135], [135, BOARD_OFFSET_Y + 205], [205, BOARD_OFFSET_Y + 205]],
    "red": [[625, BOARD_OFFSET_Y + 135], [695, BOARD_OFFSET_Y + 135], [625, BOARD_OFFSET_Y + 205], [695, BOARD_OFFSET_Y + 205]],
    "green": [[625, BOARD_OFFSET_Y + 625], [695, BOARD_OFFSET_Y + 625], [625, BOARD_OFFSET_Y + 695], [695, BOARD_OFFSET_Y + 695]],
    "blue": [[135, BOARD_OFFSET_Y + 625], [205, BOARD_OFFSET_Y + 625], [135, BOARD_OFFSET_Y + 695], [205, BOARD_OFFSET_Y + 695]]
}

# Starting points for each player's coins
starting_points = {

    "red": [[716, 900 - 513], [716, 900 - 562], [770, 900 - 513], [770, 900 - 562]],
    "yellow": [[350, 900 - 780], [350, 900 - 834], [400, 900 - 780], [400, 900 - 834]],
    "blue": [[76, 900 - 413], [76, 900 - 463], [130, 900 - 413], [130, 900 - 463]],
    "green": [[450, 900 - 141], [450, 900 - 194], [497, 900 - 141], [497, 900 - 194]]
}

player_capture_zone =[
    [[0],[0]],    [[0],[0]],    [[0],[0]],    [[0],[0]],
    [[0],[0]],    [[0],[0]],    [[0],[0]],    [[0],[0]],
    [[0],[0]],    [[0],[0]],    [[0],[0]],    [[0],[0]],
    [[0],[0]],    [[0],[0]],    [[0],[0]],    [[0],[0]],
]

# Drawing Functions
def plot_point(x, y):

    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_filled_rectangle(x, y, width, height, color):

    glColor3f(*color)
    # Draw the outline of the rectangle

    draw_rectangle_outline(x, y, width, height, color)
    # Fill the rectangle using points
    # for i in range(int(width)):
    #     for j in range(int(height)):
    #         plot_point(x + i, y + j)


# Function to draw the center home area with diagonal lines
def draw_center_home():

    glColor3f(0.65, 0.65, 0.65)  # Grey color for the lines

    midpoint_line(350, BOARD_OFFSET_Y + 350, 500, BOARD_OFFSET_Y + 500)
    midpoint_line(350, BOARD_OFFSET_Y + 500, 500, BOARD_OFFSET_Y + 350)

    draw_rectangle_outline(375, BOARD_OFFSET_Y + 375, 100, 100, (0, 0, 0))


# Function to draw the grid lines
def draw_grid_lines():
    glColor3f(0.65, 0.65, 0.65)  # Grey grid lines

    # Vertical lines for the center paths
    for i in range(4):

        midpoint_line(350 + i * CELL_SIZE / 1.5, BOARD_OFFSET_Y + 20,
                      350 + i * CELL_SIZE / 1.5, BOARD_OFFSET_Y + 825)

    # Horizontal lines for the center paths
    for i in range(4):

        midpoint_line(20, BOARD_OFFSET_Y + 350 + i * CELL_SIZE / 1.5,
                      825, BOARD_OFFSET_Y + 350 + i * CELL_SIZE / 1.5)

    # Vertical lines for the left side grid
    for i in range(7):

        midpoint_line(350 - i * CELL_SIZE_2, BOARD_OFFSET_Y + 350,
                      350 - i * CELL_SIZE_2, BOARD_OFFSET_Y + 500)

    # Horizontal lines for the bottom side grid
    for i in range(7):

        midpoint_line(350, BOARD_OFFSET_Y + 350 - i * CELL_SIZE_2,
                      500, BOARD_OFFSET_Y + 350 - i * CELL_SIZE_2)

    # Vertical lines for the right side grid
    for i in range(6):

        midpoint_line(550 + i * CELL_SIZE_2, BOARD_OFFSET_Y + 350,
                      550 + i * CELL_SIZE_2, BOARD_OFFSET_Y + 500)

    # Horizontal lines for the upper side grid
    for i in range(6):

        midpoint_line(350, BOARD_OFFSET_Y + 550 + i * CELL_SIZE_2,
                      500, BOARD_OFFSET_Y + 550 + i * CELL_SIZE_2)

    glPointSize(5.0)

    # Yellow color

    glColor3f(1, 1, 0)

    midpoint_line(350, 120, 450, 120)
    midpoint_line(350, 66, 450, 66)
    midpoint_line(400, 120, 400, 66)
    midpoint_line(350, 120, 350, 66)
    midpoint_line(400, 120, 400, 380)
    midpoint_line(450, 66, 450, 380)

    midpoint_line(400, 389, 450, 389)

    midpoint_line(351, 338, 425, 408)
    midpoint_line(499, 338, 425, 408)

    midpoint_line(351, 338, 499, 338)

    # Blue color

    glColor3f(0, 0, 1)

    midpoint_line(75, 490, 128, 490)  # 1-2
    midpoint_line(75, 490, 75, 389)  # 1-3
    midpoint_line(75, 390, 399, 390)  # 3-4
    midpoint_line(75, 440, 397, 440)  # 4-9
    midpoint_line(130, 490, 130, 390)

    midpoint_line(400, 440, 400, 390)

    midpoint_line(349, 340, 422, 412)
    midpoint_line(349, 488, 422, 412)

    midpoint_line(350, 340, 350, 488)

    # Green color

    glColor3f(0, 1, 0)

    midpoint_line(496, 705, 400, 705)  # 1-2
    midpoint_line(496, 760, 400, 760)  # 1-3
    midpoint_line(400, 760, 400, 445)  # 3-4
    midpoint_line(450, 760, 450, 445)  # 4-9
    midpoint_line(498, 705, 498, 760)

    midpoint_line(401, 440, 450, 440)
    midpoint_line(352, 489, 424, 413)
    midpoint_line(498, 489, 424, 413)

    midpoint_line(352, 489, 498, 489)

    # Red color

    glColor3f(1, 0, 0)  # Red color

    midpoint_line(711, 390, 770, 390)  # 1 &2
    midpoint_line(715, 385, 715, 340)  # 1 &3
    midpoint_line(770, 385, 770, 340)  # 2 &4
    midpoint_line(711, 340, 770, 340)  # 3 &4

    midpoint_line(711, 390, 452, 390)  # 1 &6

    midpoint_line(770, 440, 452, 440)  # 4 &12

    midpoint_line(450, 389, 450, 437)

    midpoint_line(715, 360, 715, 445)
    midpoint_line(770, 360, 770, 445)  # 4 &4

    midpoint_line(501, 485, 428, 413)  # triangle part
    midpoint_line(501, 345, 428, 413)

    midpoint_line(500, 485, 500, 345)


def draw_rectangle_outline(x, y, width, height, color):

    glColor3f(*color)
    midpoint_line(x, y, x + width, y)
    midpoint_line(x + width, y, x + width, y + height)
    midpoint_line(x + width, y + height, x, y + height)
    midpoint_line(x, y + height, x, y)

def move_coin(current_X, current_Y, coin_color):
    # Define conditions for each method (A to R)

    global  dx1, dx2, dx3, dy1, dy2, dy3, current_player, player_yellow, player_red, player_green, player_blue

    if 350 < current_X < 400 and 285 < current_Y < 338:  # Method A
        current_X -= dx3
        current_Y += dy3

    elif 350 < current_X < 400 and 759 < current_Y < 813:  # Method B
        current_X += dx3

    elif 295 < current_X < 350 and 438 < current_Y < 489:  # Method C
        current_X += dx3
        current_Y += dy1

    elif 770 < current_X < 825 and 440 < current_Y < 488:  # Method D
        current_Y -= dy3

    elif 450 < current_X < 500 and 489 < current_Y < 538:  # Method E
        current_X += dx1
        current_Y -= dy3

    elif 450 < current_X < 500 and 9 < current_Y < 65:  # Method F
        current_X -= dx3

    elif 500 < current_X < 550 and 339 < current_Y < 387:  # Method G
        current_X -= dx3
        current_Y -= dy2

    elif 21 < current_X < 76 and 339 < current_Y < 389:  # Method H
        current_Y += dy3

    elif 20 < current_X < 295 and 438 < current_Y < 489:  # Method I
        current_X += dx2

    elif 450 < current_X < 500 and 537 < current_Y < 812:  # Method J
        current_Y -= dy1

    elif 500 < current_X < 825 and 339 < current_Y < 388:  # Method K
        current_X -= dx1

    elif 350 < current_X < 400 and 10 < current_Y < 285:  # Method L
        current_Y += dy2

    elif 75 < current_X < 350 and 339 < current_Y < 389:  # Method M
        current_X -= dx2

    elif 350 < current_X < 400 and 488 < current_Y < 759:  # Method N
        current_Y += dy1

    elif 501 < current_X < 770 and 437 < current_Y < 487:  # Method O
        current_X += dx1

    elif 450 < current_X < 500 and 63 < current_Y < 337:  # Method P
        current_Y -= dy2

    elif 400 < current_X < 450:  # Method Q

        if current_player == 2 and not(11 < current_Y < 65 ):
            current_Y -= dy1

            if 397 < current_X < 450 and 438 < current_Y < 492:
                player_green.append(1)
                if len(player_green) == 4:
                    print("Player", current_player + 1, "wins the game")

        elif current_player == 0 and not(759 < current_Y < 813):
            current_Y += dy2

            if 399 < current_X < 450 and 335 < current_Y < 390:
                player_yellow.append(1)
                if len(player_yellow) == 4:
                    print("Player", current_player + 1, "wins the game")

        else:

            if 759 < current_Y < 813:
                current_X+=dx3
            elif 11 < current_Y < 65:
                current_X-=dx3

    elif 387 < current_Y < 439:  # Method R

        if current_player == 3 and not(770 < current_X < 824):
            current_X += dx2

            if 350 < current_X < 400 and 383 < current_Y < 440:
                player_blue.append(1)
                if len(player_blue) == 4:
                    print("Player", current_player + 1, "wins the game")

        elif current_player == 1 and not(21 < current_X < 76):
            current_X -= dx1

            if 450 < current_X < 502 and 385 < current_Y < 440:
                player_red.append(1)
                if len(player_red) == 4:
                    print("Player", current_player + 1, "wins the game")

        else:

            if 21 < current_X < 76:
                current_Y+=dy3

            elif 770 < current_X < 824:
                current_Y-=dy3

    return current_X, current_Y

def draw_coins(coins):
    global blink_state, blink_timer, player_number_printed

    for index, coin in enumerate(coins):
        if index // 4 == current_player and blinking:
            if blink_state:
                draw_filled_rectangle(coin["x"], coin["y"], coin["size"], coin["size"], coin["color"])
                if not player_number_printed:
                    print("Player : ", current_player + 1)
                    player_number_printed = True

        else:
            draw_filled_rectangle(coin["x"], coin["y"], coin["size"], coin["size"], coin["color"])

    blink_timer += 1
    if blink_timer % 10 == 0:
        blink_state = not blink_state


def draw_dice(x, y, size):

    glPointSize(5.0)
    glColor3f(1, 1, 1)
    draw_rectangle_outline(x, y, size, size, (0, 0, 0))
    draw_filled_rectangle(x, y, size, size, (1, 1, 1))

    glPointSize(7.0)
    glColor3f(1, 1, 1)
    half_size = size // 2
    quarter_size = size // 4

    if current_dice_value == 1:
        plot_point(x + half_size, y + half_size)

    elif current_dice_value == 2:
        plot_point(x + quarter_size, y + quarter_size)
        plot_point(x + 3 * quarter_size, y + 3 * quarter_size)

    elif current_dice_value == 3:
        plot_point(x + quarter_size, y + quarter_size)
        plot_point(x + half_size, y + half_size)
        plot_point(x + 3 * quarter_size, y + 3 * quarter_size)

    elif current_dice_value == 4:
        plot_point(x + quarter_size, y + quarter_size)
        plot_point(x + quarter_size, y + 3 * quarter_size)
        plot_point(x + 3 * quarter_size, y + quarter_size)
        plot_point(x + 3 * quarter_size, y + 3 * quarter_size)

    elif current_dice_value == 5:
        plot_point(x + quarter_size, y + quarter_size)
        plot_point(x + quarter_size, y + 3 * quarter_size)
        plot_point(x + half_size, y + half_size)
        plot_point(x + 3 * quarter_size, y + quarter_size)
        plot_point(x + 3 * quarter_size, y + 3 * quarter_size)

    elif current_dice_value == 6:
        plot_point(x + quarter_size, y + quarter_size)
        plot_point(x + quarter_size, y + 3 * quarter_size)
        plot_point(x + quarter_size, y + half_size)
        plot_point(x + 3 * quarter_size, y + quarter_size)
        plot_point(x + 3 * quarter_size, y + 3 * quarter_size)
        plot_point(x + 3 * quarter_size, y + half_size)

    glPointSize(3.0)


# Game Logic Functions
def switch_turn():

    global current_player, consecutive_sixes, player_number_printed, can_move_coins
    if consecutive_sixes < 3:
        current_player = (current_player + 1) % 4
        player_number_printed = False
        can_move_coins = False


def player_capture(coin_index, x, y):
    global current_player, player_capture_zone, coins, STARTING_POSITIONS
    coin = coins[coin_index]
    if current_player > 0:
        var = (current_player - 1) * 4
    else:
        var = (3) * 4
    print("condition current player:", current_player)
    print("coin index: ", coin_index)
    for i in range(16):
        if not (i == var + 0 or i == var + 1 or i == var + 2 or i == var + 3):
            if (((coin["x"] - 15 < player_capture_zone[i][0][0] < coin["x"] + 15 and
                  coin["y"] - 15 < player_capture_zone[i][1][0] < coin["y"] + 15)) and

                    ((not (449 < x < 500 and 703 < y < 761)) or
                     (not (349 < x < 402 and 647 < y < 705)) or
                     (not (75 < x < 132 and 437 < y < 489)) or
                     (not (129 < x < 187 and 338 < y < 391)) or
                     (not (348 < x < 402 and 64 < y < 121)) or
                     (not (448 < x < 502 and 117 < y < 177)) or
                     (not (714 < x < 772 and 337 < y < 390)) or
                     (not (658 < x < 717 and 436 < y < 489)))):

                if i == 0 or 0 < i < 4:
                    coins[i]["x"] = STARTING_POSITIONS["yellow"][i][0]
                    coins[i]["y"] = STARTING_POSITIONS["yellow"][i][1]

                    player_capture_zone[i][0][0] = STARTING_POSITIONS["yellow"][i][0]
                    player_capture_zone[i][1][0] = STARTING_POSITIONS["yellow"][i][1]


                elif 3 < i < 8:
                    coins[i]["x"] = STARTING_POSITIONS["red"][i - 4][0]
                    coins[i]["y"] = STARTING_POSITIONS["red"][i - 4][1]

                    player_capture_zone[i][0][0] = STARTING_POSITIONS["red"][i - 4][0]
                    player_capture_zone[i][1][0] = STARTING_POSITIONS["red"][i - 4][1]


                elif 7 < i < 12:
                    coins[i]["x"] = STARTING_POSITIONS["green"][i - 8][0]
                    coins[i]["y"] = STARTING_POSITIONS["green"][i - 8][1]

                    player_capture_zone[i][0][0] = STARTING_POSITIONS["green"][i - 8][0]
                    player_capture_zone[i][1][0] = STARTING_POSITIONS["green"][i - 8][1]



                elif 11 < i < 16:
                    coins[i]["x"] = STARTING_POSITIONS["blue"][i - 12][0]
                    coins[i]["y"] = STARTING_POSITIONS["blue"][i - 12][1]

                    player_capture_zone[i][0][0] = STARTING_POSITIONS["blue"][i - 12][0]
                    player_capture_zone[i][1][0] = STARTING_POSITIONS["blue"][i - 12][1]  #############################################################################

    return

def mouseListener(button, state, x, y):
    global current_dice_value, consecutive_sixes, blinking, can_move_coins, starting_points, current_player, player_capture_zone, coins
    # print("current player" ,current_player)
    print("Cordinate X : ", x, "Cordinate Y : ", y)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        converted_x, converted_y = convert_coordinate(x, y)

        # Check if the player is clicking the dice to roll
        if -30 <= converted_x <= 30 and 380 <= converted_y <= 438:
            current_dice_value = random.randint(3, 5)
            print("Dice point : ", current_dice_value)
            # glutPostRedisplay()

            if current_dice_value == 6:
                consecutive_sixes += 1
                if consecutive_sixes >= 3:
                    print("Three consecutive sixes! Turn lost.")
                    consecutive_sixes = 0
                    switch_turn()
                else:
                    print("Roll again!")
                    can_move_coins = True  # Allow moving coins
            else:
                consecutive_sixes = 0
                can_move_coins = True  # Allow moving coins

            blinking = True
            print("Player : ", current_player +1)
            glutPostRedisplay()

        # Check if the player is clicking on their coins to move
        if can_move_coins:
            player_colors = ["yellow", "red", "green", "blue"]
            color = player_colors[current_player]
            for i in range(4):
                coin_index = current_player * 4 + i
                coin = coins[coin_index]
                if (coin["x"] - 15 <= x <= coin["x"] + 15 and
                        coin["y"] - 15 <= 900 - y <= coin["y"] + 15):
                    print(f"Coin {coin_index} clicked for player {current_player +1 }")

                    # Move the coin to the starting point
                    if ((121< x <240 and 674< y <790) or                        ##############################       six     ###################
                            (121< x <240 and 183< y <302) or
                            (611< x <730 and 184< y <302) or
                            (611< x <730 and 673< y <791)):
                        coin["x"] = starting_points[color][0][0] + 15
                        coin["y"] = starting_points[color][1][1] +15
                        print(coin["x"], coin["y"])
                        can_move_coins = False
                        switch_turn()
                        glutPostRedisplay()
                        break
                    else:

                        if ((397 < x < 451 and 283 < y < 339) or         # Yellow
                                (397 < x < 450 and 489 < y < 543) or     # Green
                                (293 < x < 351 and 388 < y < 438) or     # Blue
                                (499 < x < 551  and 385 < y < 439)):     # Red

                            if (current_dice_value <= 1):

                                for i in range(current_dice_value):
                                    coin["x"], coin["y"] = move_coin(coin["x"], coin["y"], coins[coin_index])
                                    glutPostRedisplay()

                                print(coin["x"], coin["y"])
                                can_move_coins = False
                                switch_turn()
                                glutPostRedisplay()

                        if ((399 < x < 450 and 229 < y < 285) or        # Yellow
                                (398 < x < 451 and 540 < y < 597) or    # Green
                                (239 < x < 297 and 388 < y < 440) or    # Blue
                                (549 < x < 606 and 386 < y < 439)):     # Red

                            if (current_dice_value <= 2):

                                for i in range(current_dice_value):
                                    coin["x"], coin["y"] = move_coin(coin["x"], coin["y"], coins[coin_index])
                                    glutPostRedisplay()

                                print(coin["x"], coin["y"])
                                can_move_coins = False
                                switch_turn()
                                glutPostRedisplay()

                        if ((398 < x < 450 and 173 < y < 231) or        # Yellow
                                (398 < x < 451 and 594 < y < 652) or    # Green
                                (183 < x < 242 and 387 < y < 440) or    # Blue
                                (604 < x < 661 and 386 < y < 439)):     # Red

                            if (current_dice_value <= 3):

                                for i in range(current_dice_value):
                                    coin["x"], coin["y"] = move_coin(coin["x"], coin["y"], coins[coin_index])
                                    glutPostRedisplay()

                                print(coin["x"], coin["y"])
                                can_move_coins = False
                                switch_turn()
                                glutPostRedisplay()

                        if ((398 < x < 451 and 120 < y < 176) or         # Yellow
                                (399 < x < 451 and 647 < y < 708) or     # Green
                                (128 < x < 186 and 386 < y < 438) or     # Blue
                                (659 < x < 716 and 386 < y < 439)):      # Red
                            if (current_dice_value <= 4):

                                for i in range(current_dice_value):
                                    coin["x"], coin["y"] = move_coin(coin["x"], coin["y"], coins[coin_index])
                                    glutPostRedisplay()

                                print(coin["x"], coin["y"])
                                can_move_coins = False
                                switch_turn()
                                glutPostRedisplay()

                        if ((398 < x < 450 and 64 < y < 123) or           # Yellow
                                (399 < x < 451 and 704 < y < 761) or      # Green
                                (74 < x < 132 and 387 < y < 438) or       # Blue
                                (714 < x < 771 and 387 < y < 440)):       # Red

                            if (current_dice_value <= 5):
                                for i in range(current_dice_value):
                                    coin["x"], coin["y"] = move_coin(coin["x"], coin["y"], coins[coin_index])
                                    glutPostRedisplay()

                                print(coin["x"], coin["y"])
                                can_move_coins = False
                                switch_turn()
                                glutPostRedisplay()
                        else:
                            for i in range(current_dice_value):
                                coin["x"], coin["y"] = move_coin(coin["x"], coin["y"], coins[coin_index])
                                glutPostRedisplay()
                            player_capture_zone[coin_index][0][0] = coin["x"]
                            player_capture_zone[coin_index][1][0] = coin["y"]
                            print(coin["x"], coin["y"])
                            can_move_coins = False
                            switch_turn()
                            player_capture(coin_index, x, y)
                            glutPostRedisplay()


def convert_coordinate(x, y):

    global WINDOW_WIDTH, WINDOW_HEIGHT
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b


# Drawing Algorithms
def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = originalzone(x, y, zone)
    plot_point(x0, y0)

    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = originalzone(x, y, zone)
        plot_point(x0, y0)


def convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)


def originalzone(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)


# Circle Drawing Algorithm
def midpointcircle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, - y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()


# Board Drawing Functions
def draw_player_zones():
    # Yellow zone (bottom-left)

    glPointSize(4.0)

    glColor3f(0.8, 0.8, 0)
    midpointcircle(135, 180, BOARD_OFFSET_Y + 180)

    glColor3f(0.8, 0.8, 0)
    midpointcircle(90, 180, BOARD_OFFSET_Y + 180)

    glPointSize(3.0)

    draw_filled_rectangle(80, BOARD_OFFSET_Y + 80, 200, 200, (0.65, 0.65, 0.65))
    draw_filled_rectangle(120, BOARD_OFFSET_Y + 120, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(190, BOARD_OFFSET_Y + 120, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(120, BOARD_OFFSET_Y + 190, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(190, BOARD_OFFSET_Y + 190, 50, 50, (0.65, 0.65, 0.65))

    # Yellow Coins

    # draw_filled_rectangle(135, BOARD_OFFSET_Y + 625, 20, 20, (0, 0, 0.8))
    # draw_filled_rectangle(205, BOARD_OFFSET_Y + 625, 20, 20, (0, 0, 0.8))
    # draw_filled_rectangle(135, BOARD_OFFSET_Y + 695, 20, 20, (0, 0, 0.8))
    # draw_filled_rectangle(205, BOARD_OFFSET_Y + 695, 20, 20, (0, 0, 0.8))

    glPointSize(4.0)

    glColor3f(0.8, 0, 0)
    midpointcircle(90, 670, BOARD_OFFSET_Y + 180)

    glColor3f(0.8, 0, 0)
    midpointcircle(135, 670, BOARD_OFFSET_Y + 180)

    glPointSize(3.0)

    # Red zone (bottom-right)
    draw_filled_rectangle(570, BOARD_OFFSET_Y + 80, 200, 200, (0.65, 0.65, 0.65))
    draw_filled_rectangle(610, BOARD_OFFSET_Y + 120, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(680, BOARD_OFFSET_Y + 120, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(610, BOARD_OFFSET_Y + 190, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(680, BOARD_OFFSET_Y + 190, 50, 50, (0.65, 0.65, 0.65))

    # Red coins

    # draw_filled_rectangle(625, BOARD_OFFSET_Y + 135, 20, 20, (0.8, 0, 0))
    # draw_filled_rectangle(695, BOARD_OFFSET_Y + 135, 20, 20, (0.8, 0, 0))
    # draw_filled_rectangle(625, BOARD_OFFSET_Y + 205, 20, 20, (0.8, 0, 0))
    # draw_filled_rectangle(695, BOARD_OFFSET_Y + 205, 20, 20, (0.8, 0, 0))

    glPointSize(4.0)

    glColor3f(0, 0.8, 0)
    midpointcircle(135, 670, BOARD_OFFSET_Y + 670)

    glColor3f(0, 0.8, 0)
    midpointcircle(90, 670, BOARD_OFFSET_Y + 670)

    glPointSize(3.0)

    # Green zone (top-right)
    draw_filled_rectangle(570, BOARD_OFFSET_Y + 570, 200, 200, (0.65, 0.65, 0.65))
    draw_filled_rectangle(610, BOARD_OFFSET_Y + 610, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(680, BOARD_OFFSET_Y + 610, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(610, BOARD_OFFSET_Y + 680, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(680, BOARD_OFFSET_Y + 680, 50, 50, (0.65, 0.65, 0.65))

    # Green Coins

    # draw_filled_rectangle(625, BOARD_OFFSET_Y + 625, 20, 20, (0, 0.8, 0))
    # draw_filled_rectangle(695, BOARD_OFFSET_Y + 625, 20, 20, (0, 0.8, 0))
    # draw_filled_rectangle(625, BOARD_OFFSET_Y + 695, 20, 20, (0, 0.8, 0))
    # draw_filled_rectangle(695, BOARD_OFFSET_Y + 695, 20, 20, (0, 0.8, 0))

    glPointSize(4.0)

    glColor3f(0, 0, 0.8)
    midpointcircle(135, 180, BOARD_OFFSET_Y + 670)

    glColor3f(0, 0, 0.8)
    midpointcircle(90, 180, BOARD_OFFSET_Y + 670)

    glPointSize(3.0)

    # Blue zone (top-left)
    draw_filled_rectangle(80, BOARD_OFFSET_Y + 570, 200, 200, (0.65, 0.65, 0.65))
    draw_filled_rectangle(120, BOARD_OFFSET_Y + 610, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(190, BOARD_OFFSET_Y + 610, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(120, BOARD_OFFSET_Y + 680, 50, 50, (0.65, 0.65, 0.65))
    draw_filled_rectangle(190, BOARD_OFFSET_Y + 680, 50, 50, (0.65, 0.65, 0.65))

    # Blue Coins

    # draw_filled_rectangle(135, BOARD_OFFSET_Y + 135, 20, 20, (0.8, 0.8, 0))
    # draw_filled_rectangle(205, BOARD_OFFSET_Y + 135, 20, 20, (0.8, 0.8, 0))
    # draw_filled_rectangle(135, BOARD_OFFSET_Y + 205, 20, 20, (0.8, 0.8, 0))
    # draw_filled_rectangle(205, BOARD_OFFSET_Y + 205, 20, 20, (0.8, 0.8, 0))


    glPointSize(4.0)


# Function to draw the bounding box around the entire board
def draw_board_box():
    glColor3f(0.65, 0.65, 0.65)  # Grey color for the outline
    draw_rectangle_outline(15, BOARD_OFFSET_Y + 15, 815, 815, (0.65, 0.65, 0.65))  # Outer rectangle


# Function to draw the box for the dice
def draw_dice_box():
    draw_rectangle_outline(395, BOARD_OFFSET_Y + 840, 60, 60, (0.65, 0.65, 0.65))  # Dice box


# Timer function to update the blinking state
def update_blinking_state(value):
    global blink_state, player_number_printed
    blink_state = not blink_state  # Toggle blink state
    # glutPostRedisplay()  # Request a redraw
    glutTimerFunc(500, update_blinking_state, 0)  # Call this function again after 500 ms
    glutPostRedisplay()

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1)  # Dark background (dark gray)

    draw_board_box()  # Draw the box around the board
    draw_player_zones()
    draw_center_home()
    draw_dice(405, 840, 40)
    draw_grid_lines()
    draw_dice_box()  # Draw the dice box

    draw_coins(coins)  # Draw the updated coin positions

    glutSwapBuffers()


# Initialization function
def init():
    glClearColor(0, 0, 0, 1)  # Dark background (dark gray)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glPointSize(3.0)  # Set the size of GL points
    glutMouseFunc(mouseListener)
    glutTimerFunc(500, update_blinking_state, 0)  # Start the blinking timer


# Main function
def main():
    glutInit()
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow(b"Ludo Board Game Using GL_POINTS")
    init()
    glutDisplayFunc(display)
    glutMainLoop()


if __name__ == "__main__":
    main()