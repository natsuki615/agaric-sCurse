import random
#from the physics mini lecture 
class Gravity:
    def falling(y, v, g, dt): 
        v += g * dt 
        y += (v * dt)/2
        return (y, v)
    
    def jumping(y, v, f, g, dt): #asked chatgpt to help with calculating v with f and g
        v += f * dt 
        y += (v * dt)*4
        return (y, v)
    
    def flying(y, v, f, g, dt):
        v += f * dt 
        y += (v * dt)*2
        return (y, v)

    def moveXDir(x, v, dt):
        x += v * dt
        return x

