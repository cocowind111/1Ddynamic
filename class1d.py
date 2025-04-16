import numpy as np

class river:
    def __init__(self, N,L,T,dt,alpha,u):
        self.length=N
        self.river=np.ones(N)
        self.dx=L/N
        self.d=alpha*dt/self.dx**2
        self.nt=int(T/dt)
        self.c=u*dt/self.dx
        if self.d < 0.5:
            print(self.d)
            print("条件满足")
        else:
            print("d不满足要求")
            exit()
        if self.c <1:
            print(self.c)
            print("条件满足")
        else:
            print("c不满足要求")
            exit()