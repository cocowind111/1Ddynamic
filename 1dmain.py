import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter  # PillowWriter 用于保存 gif

# 参数
g = 9.81
L = 1000
Nx = 200
dx = L / Nx
T = 120
CFL = 0.9
h_min = 1e-6

# 初始条件
h = np.ones(Nx)
h[Nx // 2 - 5: Nx // 2 + 5] += 1
u = np.zeros(Nx)
U = np.vstack((h, h * u))

# 准备保存每一帧的数据
h_frames = []

def compute_flux(h, u):
    hu = h * u
    return np.array([hu, hu * u + 0.5 * g * h ** 2])

def rusanov_flux(U_L, U_R):
    h_L, hu_L = U_L
    h_R, hu_R = U_R

    u_L = hu_L / h_L if h_L > h_min else 0.0
    u_R = hu_R / h_R if h_R > h_min else 0.0

    F_L = compute_flux(h_L, u_L)
    F_R = compute_flux(h_R, u_R)

    c_L = abs(u_L) + np.sqrt(g * h_L)
    c_R = abs(u_R) + np.sqrt(g * h_R)
    a = max(c_L, c_R)

    return 0.5 * (F_L + F_R) - 0.5 * a * (U_R - U_L)

# 模拟主循环并保存帧数据
t = 0
step = 0

while t < T:
    h = U[0]
    u = np.where(h > h_min, U[1] / h, 0.0)
    max_wave_speed = np.max(np.abs(u) + np.sqrt(g * h))
    dt = CFL * dx / max_wave_speed
    dt = min(dt, T - t)

    # 保存每隔10步的水深快照
    if step % 10 == 0:
        h_frames.append(U[0].copy())

    # 更新
    F_half = np.zeros((2, Nx + 1))
    for i in range(1, Nx):
        F_half[:, i] = rusanov_flux(U[:, i - 1], U[:, i])
    for i in range(1, Nx - 1):
        U[:, i] = U[:, i] - dt / dx * (F_half[:, i + 1] - F_half[:, i])
    U[:, 0] = U[:, 1]
    U[:, -1] = U[:, -2]

    if np.isnan(U).any():
        print(f"[警告] 时间 {t:.2f} s 出现 NaN，模拟终止")
        break

    t += dt
    step += 1

# -------------------------------
# 🎞️ 动图生成
# -------------------------------
fig, ax = plt.subplots()
line, = ax.plot(h_frames[0])
ax.set_ylim(0, 2)
ax.set_title("一维浅水波传播")

def animate(i):
    line.set_ydata(h_frames[i])
    ax.set_title(f"t ≈ {i * dt * 10:.1f} s")
    return line,

ani = FuncAnimation(fig, animate, frames=len(h_frames), interval=100)

# 保存为 GIF（需要 pillow）
ani.save("shallow_water.gif", writer=PillowWriter(fps=10))

# 或保存为 MP4（需要 ffmpeg）
# ani.save("shallow_water.mp4", fps=10, dpi=200)

plt.show()
