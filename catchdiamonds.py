#CATCHTHEDIAMONDS!!!!!!!


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Window 
W, H = 800, 1080
WINDOW_ID = None  

diamond = {
    'x': 0,
    'y': 400,
    'size': 12,
    'speed': 1.1,
}

catcher = {
    'x': 0,
    'y': -480,
    'width': 150,
    'height': 20
}

score = 0
game_over = False
paused = False
last_frame_time = time.time()

#Button bounds
RESTART_BTN = (-390, -310, 440, 500)
PAUSE_BTN   = (-40, 40, 440, 500)
EXIT_BTN    = (300, 380, 440, 500)

#button mouse function
def in_button(mx, my, rect):
    left, right, bottom, top = rect
    return left <= mx <= right and bottom <= my <= top

#Midpoint Line Drawing with Zone Conversion
def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: return 0
        elif dx >= 0 and dy < 0: return 7
        elif dx < 0 and dy >= 0: return 3
        else: return 4
    else:
        if dx >= 0 and dy >= 0: return 1
        elif dx >= 0 and dy < 0: return 6
        elif dx < 0 and dy >= 0: return 2
        else: return 5

def toZone0(x, y, zone):
    if zone == 0: return x, y
    elif zone == 1: return y, x
    elif zone == 2: return y, -x
    elif zone == 3: return -x, y
    elif zone == 4: return -x, -y
    elif zone == 5: return -y, -x
    elif zone == 6: return -y, x
    elif zone == 7: return x, -y

def fromZone0(x, y, zone):
    if zone == 0: return x, y
    elif zone == 1: return y, x
    elif zone == 2: return -y, x
    elif zone == 3: return -x, y
    elif zone == 4: return -x, -y
    elif zone == 5: return -y, -x
    elif zone == 6: return y, -x
    elif zone == 7: return x, -y
def drawPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def drawLine(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    x1, y1 = toZone0(x1, y1, zone)
    x2, y2 = toZone0(x2, y2, zone)

    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1

    dx, dy = x2 - x1, y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    while x1 <= x2:
        px, py = fromZone0(x1, y1, zone)
        drawPixel(px, py)
        if d > 0:
            y1 += 1
            d += incNE
        else:
            d += incE
        x1 += 1

#Drawing
def draw_diamond():
    cx, cy, s = diamond['x'], diamond['y'], diamond['size']
    glColor3f(*diamond['color'])
    drawLine(cx, cy + 2*s, cx - s, cy)
    drawLine(cx - s, cy, cx, cy - 2*s)
    drawLine(cx, cy - 2*s, cx + s, cy)
    drawLine(cx + s, cy, cx, cy + 2*s)

def draw_catcher():
    glColor3f(1, 1, 1) if not game_over else glColor3f(1, 0, 0)
    x, y = catcher['x'], catcher['y']
    w, h = catcher['width'] // 2, catcher['height'] // 2
    drawLine(x - w, y - h, x + w, y - h)
    drawLine(x + w, y - h, x + w + 10, y + h)
    drawLine(x + w + 10, y + h, x - w - 10, y + h)
    drawLine(x - w - 10, y + h, x - w, y - h)

def draw_buttons():
    # Restart
    glColor3f(0, 1, 1)
    drawLine(-380, 470, -320, 470)
    drawLine(-380, 470, -350, 500)  
    drawLine(-380, 470, -350, 440)
    # Pause/Play
    glColor3f(1, 0.6, 0)
    if paused:
        drawLine(-40, 440, -40, 500)    # left vertical line of pause
        drawLine(40, 470, -40, 440)     # diagonal bottom line of play triangle
        drawLine(40, 470, -40, 500)     # diagonal top line of play triangle
    else:
        drawLine(-30, 440, -30, 500)    # left vertical line
        drawLine(30, 440, 30, 500)      # right vertical line

    # Exit
    glColor3f(1, 0, 0)
    drawLine(300, 440, 380, 500)
    drawLine(380, 440, 300, 500)



#Game Logic
def reset_diamond():
    diamond['x'] = random.randint(-350, 350)
    diamond['y'] = 480
    diamond['color'] = [random.uniform(0.4, 1.0), random.uniform(0.4, 1.0), random.uniform(0.4, 1.0)]
    diamond['speed'] += 0.5

def check_collision(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

def update():
    global last_frame_time, score, game_over
    now = time.time()
    dt = now - last_frame_time
    last_frame_time = now

    if not paused and not game_over:
        diamond['y'] -= diamond['speed'] * 100*dt

        if check_collision(
            catcher['x'] - catcher['width']//2, catcher['y'] - catcher['height']//2, catcher['width'], catcher['height'],
            diamond['x'] - diamond['size']//2, diamond['y'] - diamond['size']//2, diamond['size'], diamond['size']
        ):
            score += 1
            print("Score:", score)
            reset_diamond()
        elif diamond['y'] < -500:
            print("Game Over! Final Score:", score)
            game_over = True

    glutPostRedisplay()

#Input Handling
def mouse_click(button, state, x, y):
    global paused, game_over, score
    if state == GLUT_DOWN:
        mx, my = x - W//2, H//2 - y
        if in_button(mx, my, RESTART_BTN):
            print("Starting Over")
            score = 0
            game_over = False
            paused = False
            catcher['x'] = 0
            diamond['speed'] = 1.5
            reset_diamond()
        elif in_button(mx, my, PAUSE_BTN):
            paused = not paused
            print("Paused" if paused else "Resumed")
        elif in_button(mx, my, EXIT_BTN):
            print("Goodbye. Final Score:", score)
            glutLeaveMainLoop()

def special_keys(key, x, y):
    if game_over or paused:
        return
    if key == GLUT_KEY_LEFT:
        catcher['x'] -= 20
        catcher['x'] = max(catcher['x'], (-W//2 + catcher['width']//2)+10)
    elif key == GLUT_KEY_RIGHT:
        catcher['x'] += 20
        catcher['x'] = min(catcher['x'], (W//2 - catcher['width']//2)-10)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_diamond()
    draw_catcher()
    draw_buttons()
    glFlush()

def idle():
    update()

def init():
    reset_diamond()
    glClearColor(0, 0, 0, 1)
    glColor3f(1, 1, 1)
    glPointSize(2)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-W//2, W//2, -H//2, H//2)


def main():
    global WINDOW_ID
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(W, H)
    glutInitWindowPosition(1110, 0)
    WINDOW_ID = glutCreateWindow(b"Catch the Diamond!")
    init()
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMouseFunc(mouse_click)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if __name__ == "__main__":
    main()