# prototype1.py
#
# This is the first racecar coding
#

from Panda import *

items = [boost, charge, defense, glide, hp, offense, questionBlock, speed, turn, weight]

# create the scene
#grassScene()

# create the vehicle
car = jeep(size = 0.25)

# create the racetrack
track = Racetrack("maze2.txt", model = car)
text(format("Time: %i", (60-time)*step(60-time)))
text(format("Score: %i", track.score))
'''
for i in range(20):
    for j in range(20):
        #track.item(items[int(randomRange(0,9))], P3(int(randomRange(5,track.w-5)),int(randomRange(5,track.h-5)),0))
        track.placeObj(items[int(randomRange(0,len(items)-1))], position = P3(int(randomRange(5,track.w-5)),int(randomRange(5,track.h-5)),0))
'''
#track.placeObj(items[int(randomRange(0,len(items)-1))], position = P3(randomRange(5,track.w-5),randomRange(5,track.h-5),0), score = 1, reaction = spin, sound = "good.mp3")

# set camera
#camera.position = P3(0,5,1)
#camera.hpr = HPR(pi,0,0)
camera.rod(car, distance = 2)
#camera.position = P3(20,20,75)
#camera.hpr = HPR(0,-pi/2,0)

# force constant
#fK = slider(label = "Force constant", min = 0, max = 5, init = 2)
fK = 2
# friction constant
#fcK = slider(label = "Friction", min = 0, max = 10, init = 0.5)
fcK = 0.5
# centripetal force threshold
#thresh = slider(label = "Centripetal threshold", min = 0.01, max = 2, init = 1.5)
thresh = 1.5
# velocity variable
setType(car.vel, P3Type)
#text(format("Velocity: %f", abs(car.vel)*abs(car.vel)))

# driving state
def driving(model, p0 = P3(0,0,0), hpr0 = HPR(0,0,0)):
    # vehicle movement variable
    # steering wheel angle
    a = getX(mouse)
    # the force on the vehicle
    f = fK * (getY(mouse)-1)
    # velocity
    #velocity = abs(car.vel)
    velocity = abs(car.vel)*abs(car.vel)
    # friction on vehicle
    fcK = track.getFriction(car.position)
    fc = -fcK * velocity
    # speed
    s = integral(f - fc)
    # heading
    h = getH(hpr0) + integral(s * a)
    car.hpr = HPR(h,0,0)
    # velocity
    car.vel = P3C(s,h+pi/2,0)
    # position
    car.position = p0 + integral(car.vel)
    # centripetal force
    cK = track.getCent(car.position)
    cent = cK * velocity*velocity * a

    # spin out the vehicle
    car.when1(cent > thresh, spin)
    car.when1(track.inWall(car), burn)
    car.when1(track.getCent(car.position) == 0, burn)

# drive reaction
def drive(model, var):
    # preserve state
    p = now(model.position)
    hpr = now(model.hpr)

    # drive!
    driving(model, p, hpr)


# spinning state
def spinning(model, p0, hpr0, v0):
    # spinning
    p = p0 + integral(v0 * (1 - localTime / 3))
    model.position = p
    hpr = hpr0 + HPR(integral(20 * (1 - localTime / 3)),0,0)
    model.hpr = hpr

    # drive away
    model.react1(localTimeIs(3), drive)


# spin reaction
def spin(model, var):
    # preserve state
    p = now(model.position)
    hpr = now(model.hpr)
    v = now(model.vel)

    # spin out!
    spinning(model, p, hpr, v)

# burning state
def burning(model, p0, hpr0):
    # burning
    p = p0*step(1-localTime) + step(localTime-1)*startPos
    model.position = p
    model.hpr = hpr0*step(1-localTime) + step(localTime-1)*startHPR
    s = fireish(position = p0)
    s.react1(localTimeIs(1), stopIt)

    # reset the model
    model.react1(localTimeIs(1), drive)

# burning reaction
def burn(model, var):
    # preserve state
    p = now(model.position)
    hpr = now(model.hpr)
    
    # burning!
    burning(model, p, hpr)

def powerUp(model, var):
    p = now(model.position)
    s = shakenSparkles(position = p)
    s.react1(localTimeIs(1), stopIt)

def explosion(model, var):
    p = now(model.position)
    s = fireish(position = p)
    s.react1(localTimeIs(1), stopIt)

def generateObj(model, var):
    num = random01()
    if num > 0.5:
        track.placeObj(hp if random01() > 0.5 else questionBlock, position = P3(randomRange(5,track.w-5),randomRange(5,track.h-5),0), score = 1, reaction = powerUp, duration = 30)
    else:
        track.placeObj(offense if random01() > 0.5 else questionBlock, position = P3(randomRange(5,track.w-5),randomRange(5,track.h-5),0), score = -1, reaction = explosion, duration = 30)


a = alarm(step = 2)
react(a, generateObj)


# go for a drive!
startPos = P3(20,15,0)
startHPR = HPR(pi/2,0,0)
driving(car, startPos, startHPR)

# run loop
start()
