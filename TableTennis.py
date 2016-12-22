import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [1,0]
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = HALF_PAD_HEIGHT
paddle2_pos = HALF_PAD_HEIGHT
score1, score2 = 0, 1
counter = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT the ball's velocity is upper right, else upper left
def spawn_ball():
    global ball_pos, ball_vel, RIGHT, LEFT # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if RIGHT:
        ball_vel[0] = random.randrange(240, 480) / 120 
        ball_vel[1] = random.randrange(60, 180) / 80 * -1
    elif LEFT:
        ball_vel[0] = random.randrange(240, 480) / 120 * -1
        ball_vel[1] = random.randrange(60, 180) / 120 * -1
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball()
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, RIGHT, LEFT
 
    if(ball_pos[0] - BALL_RADIUS <= PAD_WIDTH):
        ball_vel[0] = -ball_vel[0]
    elif(ball_pos[0] + BALL_RADIUS >= WIDTH - 1 - PAD_WIDTH):
        ball_vel[0] = -ball_vel[0]
    elif(ball_pos[1] - BALL_RADIUS <= 0):
        ball_vel[1] = -ball_vel[1]
    elif(ball_pos[1] + BALL_RADIUS >= HEIGHT -1):
        ball_vel[1] = -ball_vel[1]
   
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]       
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    # update paddle's vertical position, keep paddle on the screen
    if(paddle1_pos - HALF_PAD_HEIGHT <= 0 ):
        paddle1_pos = HALF_PAD_HEIGHT
    elif(paddle1_pos + HALF_PAD_HEIGHT >= HEIGHT -1):
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT -1
    if(paddle2_pos - HALF_PAD_HEIGHT <= 0):
        paddle2_pos = HALF_PAD_HEIGHT
    elif(paddle2_pos + HALF_PAD_HEIGHT >= HEIGHT -1):
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT -1
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    # draw paddles
    canvas.draw_polygon([[PAD_WIDTH / 2, paddle1_pos - HALF_PAD_HEIGHT],  [PAD_WIDTH / 2, paddle1_pos],[PAD_WIDTH / 2, paddle1_pos + HALF_PAD_HEIGHT], ], PAD_WIDTH, 'White', 'White')
    canvas.draw_polygon([[(WIDTH - 1) - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],  [(WIDTH - 1) - HALF_PAD_WIDTH, paddle2_pos],[(WIDTH - 1) - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], ], PAD_WIDTH, 'White', 'White')
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 2 - 50, 80), 40, 'White')
    canvas.draw_text(str(score2), (WIDTH / 2 + 30, 80), 40, 'White')
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if math.sqrt((ball_pos[0] - 4) ** 2 + (ball_pos[1] - paddle1_pos) ** 2) > math.sqrt(40 ** 2 + 24 ** 2):
            score2 += 1
            RIGHT = True
            LEFT = False
            spawn_ball()
            
            
    if WIDTH - ball_pos[0] - PAD_WIDTH <= BALL_RADIUS:
        if math.sqrt((WIDTH - 5 - ball_pos[0]) **2 + (paddle2_pos - ball_pos[1])  ** 2) > math.sqrt(40 ** 2 + 24 ** 2):
            score1 += 1
            LEFT = True
            RIGHT = False
            spawn_ball()
            
            

def ball_vel_incre():
    global counter, ball_vel
    counter = counter + 1
    ball_vel[0] *= (counter % 10) * 1.1
    ball_vel[1] *= (counter % 10) * 1.1
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 10
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Reset', new_game)
timer = simplegui.create_timer(10000, ball_vel_incre)



# start frame
new_game()
frame.start()
timer.start()