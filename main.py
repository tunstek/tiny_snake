import random
import curses
from config import *

def main():

    board = [[BOARD_CHAR for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    snake = [(random.randint(0,BOARD_SIZE-1), random.randint(0,BOARD_SIZE-1))]
    food = (random.randint(0,BOARD_SIZE-1), random.randint(0,BOARD_SIZE-1))

    direction = 0
    points = 0
    speed = STARTING_SPEED

    stdscr = curses.initscr()

    while True:
        stdscr.timeout(1000 - speed)

        key = stdscr.getch()
        if key == ord('q'): break

        # change direction based on key press and disable reverse movement
        direction = UP if key==W_KEY and direction!=DOWN else DOWN if key==S_KEY and direction!=UP else RIGHT if key==D_KEY and direction!=LEFT else LEFT if key==A_KEY and direction!=RIGHT else direction

        # Update snake
        insert = (snake[0][0], snake[0][1]+1) if direction==0 else (snake[0][0], snake[0][1]-1) if direction==1 else (snake[0][0]+1, snake[0][1]) if direction==2 else (snake[0][0]-1, snake[0][1])
        if WRAP_AROUND:
            insert = (insert[0] % BOARD_SIZE, insert[1] % BOARD_SIZE)
        snake.insert(0,insert)

        # we will end game if !WRAP_AROUND and we go outside the board
        if not ((snake[0][0] < BOARD_SIZE) and (snake[0][0] >= 0) and (snake[0][1] < BOARD_SIZE) and (snake[0][1] >= 0)): break

        # detect food collision
        if snake[0] == food:
            points = points + 20
            speed = speed + INCREMENT_SPEED if speed < MAX_SPEED-INCREMENT_SPEED else MAX_SPEED
            while food in snake: food = (random.randint(0,BOARD_SIZE-1), random.randint(0,BOARD_SIZE-1))
        else:
            snake.pop()

        # detect self collision
        if snake[0] in snake[1:]: break

        # update board
        board = [[FOOD_CHAR if (i,j)==food else SNAKE_CHAR if (i,j) in snake else BOARD_CHAR for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

        # Draw
        stdscr.clear()
        stdscr.addstr("Press 'q' to quit\n")
        stdscr.addstr("Points: {}\n".format(points))
        for l in board: stdscr.addstr(str(l)+"\n")
        stdscr.refresh()


    curses.endwin()
    print("Game Over\nScore: {}".format(points))




if __name__ == "__main__":
    main()
