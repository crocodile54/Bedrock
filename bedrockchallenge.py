from gpiozero import LED
from mcpi.minecraft import Minecraft
import time, sys, random, threading
import pyautogui as pag
led = LED(13)
mc = Minecraft.create()
running = True

def make_holes(num, x, y, z): #make the holes
    for I in range(num):        
        rx = random.randint(2,49)
        rz = random.randint(2,49)
        mc.setBlocks(x+rx, y+20, z+rz, x+rx, y+22, z+rz, 0)
        
def monitor(starting_pos):
    global running    
    LED = [(-1, -1, 1), (-1, -1, 0), (-1, -1, -1), (0, -1, -1), (1, -1, -1), (1, -1, 0), (1, -1, 1), (0, -1, 1)]
    y_start = starting_pos.y
    while running:
        pag.keyUp('shift')
        pos = mc.player.getTilePos()
        for p in LED:
            boss = mc.getBlock(pos.x+p[0], pos.y+p[1], pos.z+p[2])
            if boss==0:
                led.on() #LED on 
            else:
                led.off() #LED off   
        if pos.y > y_start:
            mc.postToChat ('cheat')
            mc.player.setPos(starting_pos.x, pos.y, starting_pos.z)#teleport after cheating
            time.sleep(1)
        if pos.y < y_start:
            mc.postToChat ('Uh-oh')
            time.sleep(3)
            mc.player.setPos(starting_pos.x, starting_pos.y, starting_pos.z)#teleport after cheating
        if pos.z==starting_pos.z+51:
            mc.postToChat('Well Done')
            running = False 
        
try:
    pos = mc.player.getTilePos()        
    mc.postToChat('get ready for the bedrock challenge')
    time.sleep(1)
    mc.postToChat('get to the other side without falling down the holes!')
    time.sleep(3)
    mc.setBlocks(pos.x+1, pos.y+20, pos.z, pos.x+53, pos.y+22, pos.z+53, 35) #wool
    mc.setBlocks(pos.x+2, pos.y+20, pos.z+1, pos.x+52, pos.y+20, pos.z+52, 95) #bedrock
    mc.setBlocks(pos.x+1, pos.y+30, pos.z, pos.x+53, pos.y+30, pos.z+53, 17)#wood roof
    mc.setBlocks(pos.x+2, pos.y+21, pos.z+1, pos.x+52, pos.y+22, pos.z+52, 0)#air gap so you don't start in wool
    mc.setBlocks(pos.x+25, pos.y+21, pos.z+1, pos.x+25, pos.y+22, pos.z+1, 0) #air for steve starting pos
    mc.player.setPos(pos.x+25, pos.y+21, pos.z+1)# teleport to start
    newpos = mc.player.getTilePos() #get newpos
    t1 = threading.Thread(target = monitor, args = (newpos, ))
    t1.start()
    make_holes(250, pos.x, pos.y, pos.z)
    time_start = time.time()
    counter = 80 #setting the timer
    while time.time()<time_start+80: #starting the timer
        time.sleep(1)
        counter-=1
        if counter%10==0:
            mc.postToChat(str(counter))
    mc.setBlocks(pos.x+2, pos.y+20, pos.z+1, pos.x+52, pos.y+20, pos.z+52, 0)
    mc.postToChat('GAME OVER')
    running = False
except KeyboardInterrupt: #type Ctrl+C
    print('bye')
    running = False
    sys.exit()
