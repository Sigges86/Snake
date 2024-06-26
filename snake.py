import random
import curses

# Initialize the screen
s = curses.initscr()
curses.curs_set(0) # Hide the cursor
sh, sw = s.getmaxyx() # Get screen height and width
w = curses.newwin(sh, sw, 0, 0) # Create a new window
w.keypad(1) # Accept keypad input
w.timeout(100) # Refresh the screen every 100ms

# Initialize the snake
snk_x = sw//4
snk_y = sh//2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Initialize the food
food = [sh//2, sw//2]
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

# Initial direction
key = curses.KEY_RIGHT
last_key = None # Track the last key pressed

while True:
    next_key = w.getch()
    if next_key != -1:
        if next_key == last_key:
            # If the same button is pressed twice, display an error message
            curses.endwin()
            print("You found the bug!")
            quit()
        else:
            key = next_key
            last_key = next_key # Update the last key pressed
    
    # Check for collision with borders or self
    if snake[0][0] in [0, sh] or snake[0][1]  in [0, sw] or snake[0] in snake[1:]:
        curses.endwin()
        quit()

    # Calculate new head position
    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Insert the new head
    snake.insert(0, new_head)

    # Check if snake gets the food
    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(int(food[0]), int(food[1]), curses.ACS_PI)
    else:
        # Move the snake
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Draw the snake
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
