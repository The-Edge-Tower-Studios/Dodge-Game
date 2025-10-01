from tkinter import *
from time import *
from keyboard import *
from math import *
from random import *
windows = Tk()
windows.title('dodge game')


canvas = Canvas(windows, width=700, height=500)
canvas.pack()
label = Label(windows, width=100, height=2, text='')
label.pack()
blockx = []
blocky = []
blocklen = []
blockwid = []
blocktype = []
blockname = []
lvbl = [] #[level time, type, direction, speed, ready?]
currentlv = 1
locbn = 0 # location blockname
Bounce = True
col_ = True


def line(x1, y1, x2, y2, Fill):
    if Fill == '':
        canvas.create_line(x1, y1, x2, y2, fill='#000000')
    else:
        canvas.create_line(x1, y1, x2, y2, fill=f'{Fill}')

def square(x1, y1, x2, y2, num, fill):
    for i in range(num):
        line(x1, y1, x1, y2, fill)
        line(x1, y2, x2, y2, fill)
        line(x2, y2, x2, y1, fill)
        line(x2, y1, x1, y1, fill)

def border(minx, miny, maxx, maxy, bounce):
    global x, y, xmove, ymove
    if x < minx:
        x = minx
        if bounce:
            xmove = -xmove
    if y < miny:
        y = miny
        if bounce:
            ymove = -ymove
    if x > maxx:
        x = maxx
        if bounce:
            xmove = -xmove
    if y > maxy:
        y = maxy
        if bounce:
         ymove = -ymove
def collision(x1, y1, x2, y2, length, width):
    if x < x2 and x + length > x1:
        if y < y2 and y + width > y1:
            return(True)
        else: 
            return(False)
    else: 
        return(False)
    
def col(type):
    if len(blockx) == 0 or not col_:
        return False
    else:
        for i in range(len(blockx)):
            if collision(blockx[i], blocky[i], blockx[i] + blocklen[i], blocky[i] + blockwid[i], 50, 50):
                if blocktype[i] == type:
                    return True
        return False


def update():
    canvas.update()

def clear():
    canvas.delete("all")

def createblock(x, y, len, wid, type, name):
    blockx.append(x)
    blocky.append(y)
    blocklen.append(len)
    blockwid.append(wid)
    blocktype.append(type)
    blockname.append(name)


x = 325
y = 225
game = 1
friction = 0.9
xmove = 0
ymove = 0
maxspeed = 5
changespeed = 1
lvfi = 0 # level finish (lvfi/len(lvbl))
tela = f'level {currentlv}' # text label
telaed = 0 # text label edit

def resetlv():
    global lvfi, blockx, blocky, blocklen, blockwid, blocktype, blockname, lvbl
    lvfi = 0
    x=325
    y=225
    blockx.clear()
    blocky.clear()
    blocklen.clear()
    blockwid.clear()
    blocktype.clear()
    blockname.clear()
    lvbl.clear()
    for i in range(randint(9, 15) * currentlv):
        lvbl.append([((randint(0, 10) / currentlv) * (i + 1) + time()), '!', choice(['left', 'right', 'up', 'down']), abs(randint(1, 5) * currentlv), False])
    # if currentlv == 3:
    #     lvbl.append([((randint(0, 10) / currentlv) * (i + 1) + time()), '!', choice(['left', 'right', 'up', 'down']), abs(randint(1, 5) * currentlv), 'Boss'])


while 1:
    label.config(text=tela)
    clear()
    square(2, 2, 700, 501, 1, "#000000")
    tela = f'level {currentlv}'
    if game == 2:
        square(x, y, x + 50, y + 50, 10, "#0008ff")
        for i in range(len(blockx)):
            try:
                if lvbl[int(blockname[i])][4] == 1:
                    square(blockx[i], blocky[i], blockx[i] + blocklen[i], blocky[i] + blockwid[i], 1, "#ff1100")
            except:
                pass

    elif game == 1:
        canvas.create_text(300,100,fill="darkblue",font="Arial 30 bold",text="dodge")
        canvas.create_text(300, 200, fill='black', font='arial 15 bold', text='press space to start game')

    elif game == 3:
        canvas.create_text(300, 200, fill='red', font='arial 20 bold', text='GAME OVER')
        if round(time()) % 2 > 0:
            canvas.create_text(300, 300, fill='black', font='arial 15 bold', text='press space to try again')
            canvas.create_text(300, 350, fill='black', font='arial 15 bold', text='press q to to go to menu')
    elif game == 4:
        canvas.create_text(300, 200, fill='green', font='arial 20 bold', text='LEVEL COMPLETE!')
        if round(time()) % 2 > 0:
            canvas.create_text(300, 300, fill='black', font='arial 15 bold', text='press space to continue')
            canvas.create_text(300, 350, fill='black', font='arial 15 bold', text='press q to to go to menu')
    update()

    if game == 2:
        tela = f'level {currentlv}, {lvfi}/{len(lvbl)}'
        if lvfi >= len(lvbl):
            currentlv += 1
            lvfi = 0
            game = 4
        try:
            if is_pressed('w'):
                if col('block'):
                    if Bounce:
                        ymove = -ymove
                    else:
                        ymove = -ymove
                        y += ymove
                        ymove = 0
                elif col('!'):
                    game = 3
                else:
                    ymove -= changespeed
                
            elif is_pressed('s'):
                if col('block'):
                    if Bounce:
                        ymove = -ymove
                    else:
                        ymove = -ymove
                        y += ymove
                        ymove = 0
                elif col('!'):
                    game = 3
                else:
                    ymove += changespeed
            
            else: 
                if col('block'):
                    if Bounce:
                        ymove = -ymove
                    else:
                        ymove = -ymove
                        y += ymove
                        ymove = 0
                elif col('!'):
                    game = 3
                else:
                    ymove = ymove * friction

            if abs(ymove) > maxspeed:
                if abs(ymove) == ymove:
                    ymove = maxspeed
                else:
                    ymove = -maxspeed
            
            y += ymove
            
                
            if is_pressed('a'):
                print('a', end='')
                if col('block'):
                    if Bounce:
                        xmove = -xmove
                    else:
                        xmove = -xmove
                        x += xmove
                        xmove = 0
                elif col('!'):
                    game = 3
                else:
                    xmove -= changespeed
            elif is_pressed('d'):
                print('d', end='')
                if col('block'):
                    if Bounce:
                        xmove = -xmove
                    else:
                        xmove = -xmove
                        x += xmove
                        xmove = 0
                elif col('!'):
                    game = 3
                else:
                    xmove += changespeed
            else:
                if col('block'):
                    if Bounce:
                        xmove = -xmove
                    else:
                        xmove = -xmove
                        x += xmove
                        xmove = 0
                elif col('!'):
                    game = 3
                else:
                    xmove = xmove * friction

            if abs(xmove) > maxspeed:
                if abs(xmove) == xmove:
                    xmove = maxspeed
                else:
                    xmove = -maxspeed
            x += xmove
        except:
            pass

        border(0, 0, 650, 450, Bounce)

        for i in range(len(lvbl)):
            # Spawn enemy only when its time is reached and not yet spawned
            if lvbl[i][0] <= time() and lvbl[i][4] == 0:
                if lvbl[i][2] == 'up':
                    createblock(randint(20, 630), 460, 50, 50, '!', f'{i}')
                elif lvbl[i][2] == 'down':
                    createblock(randint(20, 630), -10, 50, 50, '!', f'{i}')
                elif lvbl[i][2] == 'left':
                    createblock(660, randint(20, 430), 50, 50, '!', f'{i}')
                elif lvbl[i][2] == 'right':
                    createblock(-10, randint(20, 430), 50, 50, '!', f'{i}')
                lvbl[i][4] = 1  # Mark as created so it doesn't duplicate
                lvbl[i].append(len(blockx) - 1)  # Store block index
            # Move only spawned enemies
            elif lvbl[i][4] == 1 and len(lvbl[i]) > 5:
                locbn = lvbl[i][5]  # Get stored block index
                if lvbl[i][2] == 'up':
                    blocky[locbn] -= lvbl[i][3]
                elif lvbl[i][2] == 'down':
                    blocky[locbn] += lvbl[i][3]
                elif lvbl[i][2] == 'left':
                    blockx[locbn] -= lvbl[i][3]
                elif lvbl[i][2] == 'right':
                    blockx[locbn] += lvbl[i][3]

                if (blockx[locbn] < -70 or blockx[locbn] > 700 or blocky[locbn] < -70 or blocky[locbn] > 520):
                    lvfi += 1
                    lvbl[i][4] = 2


    elif game == 1:
        try:
            if is_pressed('space'):
                resetlv()
                game = 2
        except:
            pass
    elif game == 3:
        x=325
        y=225
        xmove=0
        ymove=0
        try:
            if is_pressed('space'):
                resetlv()
                game = 2
            if is_pressed('q'):
                game = 1
        except:
            pass
    elif game == 4:
        try:
            if is_pressed('space'):
                resetlv()
                game = 2
            if is_pressed('q'):
                game = 1
        except:
            pass
    sleep(0.01)

    try:
        if is_pressed('/'):
                if is_pressed('!'):
                    windows.destroy()
                if is_pressed('"') and game == 2:
                    currentlv += 1
                    resetlv()
                    sleep(0.3)
                if is_pressed('|') and game == 2 and currentlv > 1:
                    currentlv -= 1
                    resetlv()
                    sleep(0.3)
                if is_pressed('.'):
                    pass
                if is_pressed('<'):
                    if True:
                        if col_:
                            col_ = False
                        else:
                            col_ = True
                        sleep(1)
    except:
        pass
    if not col_:
        tela = f'level {currentlv}, {lvfi}/{len(lvbl)} (spectating)'
    



windows.mainloop()