class State:
    def __init__(self,y,x,b):
        self.x = x
        self.y = y
        self.b = b
        self.qValue = 0
    def get(self):
        return [self.y,self.x,self.b]
    def indx(self):
        return self.y*5+self.x + (self.b * 25)