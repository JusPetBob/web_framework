import time
from math import sqrt
from test import Display

offset = 25000
t = time.time_ns()
dt = 0.000025
acceleration = 600
step_per_mm = 200

step_accumulator = 0

x,y,z = 20,20,20
x2,y2,z2 = 20,400,200

current_block = {
    "ax":0,
    "ay":0,
    "az":0,
    "curr_step":0,
    "target_speed":1200/60,
    "speed":0,
    "type":"line",
    "done":False
}

current_block["dx"],current_block["dy"],current_block["dz"] = dx, dy, dz = abs(x2-x),abs(y2-y),abs(z2-z)

current_block["step"] = max(dx, dy, dz)

current_block["length"] = ((dx/step_per_mm)**2+(dy/step_per_mm)**2+(dz/step_per_mm)**2)**0.5
current_block["step_length"] = current_block["length"] / current_block["step"]
current_block["accel_end"] = current_block["target_speed"]**2 / (2*acceleration)
current_block["decel_start"] = current_block["length"] - (current_block["target_speed"]**2 / (2*acceleration))

if current_block["accel_end"] > current_block["decel_start"]:
    current_block["target_speed"] = sqrt(acceleration * current_block["length"])

    current_block["accel_end"] = current_block["decel_start"] = current_block["length"] / 2
    
current_block["xs"] = 1 if x2 > x else -1
current_block["ys"] = 1 if y2 > y else -1
current_block["zs"] = 1 if z2 > z else -1


#current_block = {"type":"delay","time":2000,"t":0,"done":False}

print(current_block)

def dda():
    x_step = y_step = z_step = 0
    
    current_block["ax"] += current_block["dx"]
    current_block["ay"] += current_block["dy"]
    current_block["az"] += current_block["dz"]

    if current_block["ax"] >= current_block["step"]:
        x_step = current_block["xs"]
        current_block["ax"] -= current_block["step"]
        
    if current_block["ay"] >= current_block["step"]:
        y_step = current_block["ys"]
        current_block["ay"] -= current_block["step"]
        
    if current_block["az"] >= current_block["step"]:
        z_step = current_block["zs"]
        current_block["az"] -= current_block["step"]

    return x_step,y_step,z_step

def isr():
    global current_block,x,y,z,step_accumulator,d
    
    if current_block["type"] == "line":
        if current_block["curr_step"] >= current_block["step"]:
            current_block["speed"] = 0
            current_block["done"] = True
        
        s = min((current_block["curr_step"]+0.5) * current_block["step_length"], current_block["length"])
        
        if s < current_block["accel_end"]:
            current_block["speed"] = min(sqrt(acceleration*2*s), current_block["target_speed"])
        elif s < current_block["decel_start"]:
            current_block["speed"] = current_block["target_speed"]
        else:
            r = current_block["length"] - s
            current_block["speed"] = min(sqrt(acceleration*2*r),current_block["target_speed"])
        
        step_rate = current_block["speed"] * step_per_mm
        
        if step_rate <= 0:
            return
        
        step_interval = 1.0 / step_rate
        
        step_accumulator += dt
        
        while step_accumulator >= step_interval:
            step_accumulator -= step_interval
            
            _x,_y,_z = dda()
            
            current_block["curr_step"] += 1
            
            #step(_x,_y,_z)
            
            d.step_all(_x,_y,_z)
            
            #print(d.x,d.y,d.z)
            
            x += _x
            y += _y
            z += _z
            
            #print(x,y,z,_x,_y,_z)
            
            #print("step")
            
            #print(current_block["speed"], current_block["curr_step"])
    
    elif current_block["type"] == "delay":
        current_block["t"] += dt*1000
        if current_block["t"] >= current_block["time"]:
            current_block["done"] = True

if __name__ == "__main__":
    d = Display(500,500,500)
    d.set_pos(x,y,z)
    
    while True:
        now = time.time_ns()
        if now >= t+offset:
            isr()
            
            t=now
        
        if current_block["done"]:
            print(current_block,x,y,z)
            break
    
    input()