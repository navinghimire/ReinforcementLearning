class State:
    def __init__(self,y,x,b):
        self.x = x
        self.y = y
        self.b = b
    def get(self):
        return [self.y,self.x,self.b]