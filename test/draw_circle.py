##Bresenham画圆
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random as rd

# ==========================================
# 圆的基本信息
# 1.圆半径
r = 6.0
# 2.圆心坐标
a, b = (0., 0.)
Ary = []
Aryd = []


# ==========================================
##Bresenham计算点的方法
##画点方向 只有右下L点或者正右H点
##计算D(H) D(L） 计算公式为D(p)=px*px+py*py-r*r
##计算di=D(H)+D(L) di>0则画L，di<=0则画H
##考虑圆的对称性根据L点坐标依次画出(x,y),(-x,y),(-x,-y),(x,-y),(y,x),(-y,x),(-y,-x),(y,-x)八个点
##起止位置(0,r)到(r-1,y)，因为终点没有好的方法可以判断到底划分到那里
##为了适合大多数半径还是使用上面的终点，虽然会多画几个点，不过消耗很少
##def init():
##    plt.set_xlim(Ary[

def getPoint():
    R = int(r)
    st = [0, R]
    Ary.append(st)
    plt.scatter(0, R, color='b')
    plt.scatter(0, -R, color='b')
    plt.scatter(-R, 0, color='b')
    plt.scatter(R, 0, color='b')
    for i in range(0, R - 1):
        H = [st[0] + 1, st[1]]
        L = [st[0] + 1, st[1] - 1]
        DH = H[0] * H[0] + H[1] * H[1] - R * R
        DL = L[0] * L[0] + L[1] * L[1] - R * R
        di = DH + DL
        Aryd.append(di)
        if (di > 0):
            H = L
        st = H
        Ary.append(st)
        DrawPoint(st[0], st[1], 'b')


def DrawPoint(x, y, cr):
    plt.scatter(x, y, color=cr)
    plt.scatter(-x, y, color=cr)
    plt.scatter(-x, -y, color=cr)
    plt.scatter(x, -y, color=cr)
    plt.scatter(y, x, color=cr)
    plt.scatter(-y, x, color=cr)
    plt.scatter(-y, -x, color=cr)
    plt.scatter(y, -x, color=cr)


def setAxis():
    lent = range(-15, 15, 1)
    plt.xticks(lent)
    plt.yticks(lent)
    plt.plot([-18, 18], [0, 0], 'k')
    plt.plot([0, 0], [-18, 18], 'k')


##参数方程画圆
def drawCle():
    theta = np.arange(0, 2 * np.pi, 0.01)
    x = a + r * np.cos(theta)
    y = b + r * np.sin(theta)
    plt.plot(x, y, 'r')
    plt.axis('equal')


##plt.show()

if __name__ == "__main__":
    ##    r=float(input("r:"))
    r = int(rd.uniform(3, 15) + 0.5)
    ##    r=8
    setAxis()
    getPoint()
    drawCle()
    print(Ary)
    print(Aryd)
    plt.show()
