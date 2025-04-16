import numpy as np
import class1d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#数据输入
N=20
L=1
T=4
dt=0.0005
alpha=0.01
u=0.5
#
river=class1d.river(N,L,T,dt,alpha,u)
nt=int(T/dt)

h=np.ones(N+1)
h[:]=5
# h[int(N/2)]=7
h[0]=7
results = [h.copy()[:N+1]]

for n in range(nt):
    h_new=h.copy()
    for j in range(1,N):
        # h_new[j]=h[j]+river.d*(h[j+1]-2*h[j]+h[j-1])-river.c*(h[j+1]-h[j-1])/2
        h_new[j]=h[j]-river.c*(h[j+1]-h[j-1])/2
        h_new[-1] = h[-1]-river.c*(h[-1]-h[-2])
    # h_new[0] = h_new[1]


    h=h_new
    if n % 10== 0:
        print(n)
        results.append(h.copy()[:N+1])
x = np.linspace(0, L, N+1)
for i, u_i in enumerate(results):
    plt.plot(x, u_i, label=f"step {i}")
plt.xlabel("x")
plt.ylabel("u")
plt.title("1D Diffusion Equation (FTCS)")
plt.legend()
plt.grid(True)
plt.show()

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# 设置坐标轴范围（根据你的物理量调整）
ax.set_xlim(x[0], x[-1])
ax.set_ylim(0, max([h.max() for h in results]) * 1.1)
ax.set_xlabel("x")
ax.set_ylabel("h")
ax.set_title("水深随时间变化")

# 初始化函数：空线
def init():
    line.set_data([], [])
    return line,

# 每一帧更新函数
def update(frame):
    y = results[frame]
    line.set_data(x, y)
    ax.set_title(f"t = {frame * 50} Δt")  # 显示时间
    return line,

# 创建动画（interval 控制帧率，blit=True 可加速）
ani = animation.FuncAnimation(fig, update, frames=len(results),
                              init_func=init, interval=100, blit=True)

plt.show()
ani.save("diffusionreflect.gif", writer='pillow', fps=20)


print(1)
# river.river[0]=1




