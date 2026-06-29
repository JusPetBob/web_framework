from test import Display
from math import copysign
import time

d = Display(400,400,400)


def sgn(x) -> int:
    return int(copysign(1,x))

def Bresenham3D(x1, y1, z1, x2, y2, z2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    
    xs = 1 if x2 > x1 else -1
    ys = 1 if y2 > y1 else -1
    zs = 1 if z2 > z1 else -1
    
    
    print((x1, y1, z1), (x2, y2, z2))
    print(xs, ys, zs)

    # X
    if (dx >= dy and dx >= dz):        
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while (x1 != x2):
            yield "x",xs
            x1 += xs
            if (p1 >= 0):
                yield "y",ys
                y1 += ys
                p1 -= 2 * dx
            if (p2 >= 0):
                yield "z",zs
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz

    # Y
    elif (dy >= dx and dy >= dz):       
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while (y1 != y2):
            yield "y",ys
            y1 += ys
            if (p1 >= 0):
                yield "x",xs
                x1 += xs
                p1 -= 2 * dy
            if (p2 >= 0):
                yield "z",zs
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz

    # Z
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while (z1 != z2):
            yield "z",zs
            z1 += zs
            if (p1 >= 0):
                yield "y",ys
                y1 += ys
                p1 -= 2 * dz
            if (p2 >= 0):
                yield "x",xs
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
    
    return x2,y2,z2


def Bresenham2D(s_x,s_y,e_x,e_y):
    global d
    
    dx = e_x-s_x
    dy = e_y-s_y
    
    adx, ady = abs(dx), abs(dy)
    sdx, sdy = sgn(dx), sgn(dy)
    
    if adx > ady:
        pdx, pdy = sdx, 0
        
        dslowdir = ady
        dfastdir = adx
    else:
        pdx, pdy = 0, sdy
        
        dslowdir = adx
        dfastdir = ady
    
    x = s_x
    y = s_y
    
    d.set_pos(x,y,0)
    
    print(dx,dy, sdx, sdy)
    f = dfastdir//2
    
    for i in range(1,dfastdir+1):
        if dfastdir == adx:
            d.step_x(sdx)
        else:
            d.step_y(sdy)
            
        f -= dslowdir
        if f < 0:
            if dfastdir == adx:
                d.step_y(sdy)
            else:
                d.step_x(sdx)
                
            f += dfastdir

            x += sdx
            y += sdy
        else:
            x += pdx
            y += pdy

    print(x,y)



if __name__ == "__main__":
    x1,y1,z1 = 0,0,0
    x2,y2,z2 = 400,0,0
    
    d.set_pos(x1,y1,z1)
    
    # chat_gpt
    steps_per_mm = 80
    feed_mm_min = 1200

    steps_per_sec = feed_mm_min * steps_per_mm / 60
    step_delay = 1.0 / steps_per_sec
    
    ####
    
    
    #Bresenham2D(200,0,100,400)
    for a,direc in Bresenham3D(x1,y1,z1,x2,y2,z2):
        if a == "x":
            d.step_x(direc)
        elif a == "y":
            d.step_y(direc)
        else:
            d.step_z(direc)
        
        time.sleep(step_delay)
    
    input()