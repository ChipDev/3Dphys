import math
import numpy as np
import tkinter as tk
import cexprtk

window = tk.Tk()
canvasframe = tk.Frame(window, width=1300, height=800)
canvas = tk.Canvas(canvasframe, width=1300, height=800)
originx = 650
originy = 400
global rotation; rotation = 0
global zoom; zoom = 130
st = cexprtk.Symbol_Table({'x' : 0.0}, add_constants=True)
expression = cexprtk.Expression("sin(x)", st)

def init():
    window.geometry('1600x800')
    window.title("3DPhys")

    canvas.pack(side=tk.TOP, anchor=tk.NW)
    canvasframe.pack(side='left', anchor=tk.NW)
    canvas.create_rectangle(0, 0, 1300, 800, fill='#18466b')

    buttonsframe = tk.Frame(window, width=300, height=800)
    buttonsframe.pack(side='right')
    #Y = ENTRY#
    label1 = tk.Label(buttonsframe, text="y = ", width=10)
    label1.grid(column="1", row="0")
    entry1 = tk.Entry(buttonsframe, text="sin(x)", width=10)
    entry1.grid(column="2", row = "0", ipadx=50)
    blank1 = tk.Label(buttonsframe, text=" ", width=5)
    blank1.grid(column="3", row="0")

    #CONFIRM BUTTON#

def change_function(expstr):
    global expression
    expression = cexprtk.Expression(expstr, st)

def rot_x(rotrad):
    return np.array(
        [
            [1, 0, 0],
            [0, math.cos(rotrad), -1 * math.sin(rotrad)],
            [0, math.sin(rotrad), math.cos(rotrad)]
        ]
    )

def rot_y(rotrad):
    return np.array(
        [
            [math.cos(rotrad), 0, math.sin(rotrad)],
            [0, 1, 0],
            [-1 * math.sin(rotrad), 0, math.cos(rotrad)]
        ]
    )

def rot_z(rotrad):
    return np.array(
        [
            [math.cos(rotrad), -1 * math.sin(rotrad), 0],
            [math.sin(rotrad), math.cos(rotrad), 0],
            [0, 0, 1]
        ]
    )

def cross():
    canvas.create_line(0, 400, 1300, 400, fill='#234764')
    canvas.create_line(650, 0, 650, 800, fill='#234764')

def nBit(num, k):
    return num & (1 << (k-1))

def _from_rgb(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def display_native_pixel(x, y, color, width):
    canvas.create_oval(x-(width/2), y-(width/2), x+(width/2), y+(width/2), fill=color, width=1, outline="", tags="graph")

def display_pixel(x, y, color, width):
    display_native_pixel(x, 800-y, color, width)

def display(x, y, color, width):
    display_pixel(originx + x*zoom, originy + y*zoom, color, width)

def display3d(x, y, z, color, width):
    if(z > 0):
        display_pixel(originx + float((x / z) * zoom), originy + (y / z) * zoom, color, width)
        #print("-> " + str(float((x/z)*zoom)))

def graphsin3d(start, end):
    for xpix in range(start,end):
        xpixtranslated = xpix - (end / 2)
        x = xpixtranslated / zoom
        #print(float(x))
        pos = np.array([[x],[math.sin(x)],[0]])
        rotrad = rotation * math.pi / 180
        posrotated = np.dot(rot_y(rotrad), pos)
        finx = posrotated.item(0)
        finy = posrotated.item(1)
        orgz = posrotated.item(2)
        finz = orgz + 8
        #print(str(finx) + ", " + str(finy) + ", " + str(finz))
        display3d(finx, finy, finz, _from_rgb(0, 0, int(sorted((0, min(max(0,finz*10), 255), 255))[1])), 3)

def graphsin3d_fast(rangex, resolution):
    for xres in range(-(rangex * resolution)//2 , (rangex * resolution)//2):
        x = xres / resolution
        st.variables['x'] = x;
        y = expression()
        #print(str(x) + ", " + str(y))
        pos = np.array([
            [x], [y], [0]
        ])
        rotrad = rotation * math.pi / 180
        posrotated = np.dot(rot_y(rotrad), pos)
        dist = 15
        k = int(sorted((0, min(max(0,(posrotated.item(2) + dist)*8), 255), 255))[1])
        display3d(posrotated.item(0),posrotated.item(1),posrotated.item(2) + dist, _from_rgb(k,0,0), 3)

def graphcube():
    pos = [None] * 8
    for i in range(0, len(pos)):
        pos[i] = np.array([
            [5 if nBit(i, 1) == 1 else -5],
            [5 if nBit(i, 2) == 2 else -5],
            [5 if nBit(i, 3) == 4 else -5]
        ])

        rotrad = rotation * math.pi / 180
        posrotated = np.dot(rot_y(rotrad), pos[i])
        finx = posrotated.item(0)
        finy = posrotated.item(1)
        orgz = posrotated.item(2)
        finz = orgz + 20

        display3d(finx, finy, finz, _from_rgb(255, 0, 255), 3)

def update():
    #INSERT updating funtions
    canvas.delete("graph")
    global rotation
    rotation = rotation + 5
    #graphsin3d(0, 1300)
    graphcube()
    graphsin3d_fast(15, 15)
    window.after(20, update)

init()
cross()
#graphsin3d(0,1300)
graphcube()
graphsin3d_fast(10, 7)
window.after(1, update)
window.mainloop()