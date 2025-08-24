import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# uploading data (replaced the "****" with mean of immediate above and below readings)
data = [
101327.401, 101327.401, 101326.2005, 101331.0025, 101327.401,
101328.6015, 101327.401, 101328.6015, 101329.802, 101329.802,
101328.6015, 101331.0025, 101331.0025, 101329.802, 101328.6015,
101331.0025, 101329.802, 101328.6015, 101329.802, 101331.0025,
101331.0025, 101331.0025, 101331.0025, 101331.0025, 101331.0025,
101328.6015, 101332.203, 101228.96, 100635.913, 99525.4505,
99273.3455, 98231.3115, 97460.5905, 96849.536, 96488.1855,
96303.3085, 96183.2585, 96159.2485, 96237.281, 96707.877,
96561.416, 96782.308, 97000.799, 97252.904, 97505.009, 97748.7105,
97996.0135, 98243.3165, 98501.424, 98775.138, 99017.639,
99299.7565, 99797.964, 100321.382, 100585.492, 100815.988,
101058.489
]

df = pd.DataFrame({"Pressure": data})
df["Pressure"] = pd.to_numeric(df["Pressure"], errors="coerce")

time = np.arange(len(df))

# removing irrational data using oulier detection method
Q1, Q3 = df["Pressure"].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
mask = (df["Pressure"] >= lower) & (df["Pressure"] <= upper)
df_clean = df[mask].reset_index(drop=True)
time_clean = np.arange(len(df_clean))

# to make it look fancy 
print(f"Original points: {len(df)}")
print(f"After cleaning: {len(df_clean)}")

# defining altitude and velocity 
R, T, M, g, P0 = 8.314, 288.15, 0.029, 9.81, 101325
alt = (R*T)/(M*g) * np.log(P0 / df_clean["Pressure"].to_numpy())
vel = np.gradient(alt, time_clean)

# smoothing the values by taking average
def smooth(x, w=4):
    return pd.Series(x).rolling(window=w, min_periods=1).mean().to_numpy()

alt_s = smooth(alt, 4)
vel_s = smooth(vel, 4)

# to see if the data is correct or not (boxplots)
plt.figure(figsize=(10,5))
plt.subplot(1,2,1); plt.boxplot(df["Pressure"], vert=False); plt.title("Raw Pressure")
plt.subplot(1,2,2); plt.boxplot(df_clean["Pressure"], vert=False); plt.title("Cleaned Pressure")
plt.tight_layout(); plt.show(block=False)

# altitude vs time and velocity vs time graphs
plt.figure(figsize=(10,5))
plt.plot(time_clean, alt, alpha=0.5, label="raw altitude")
plt.plot(time_clean, alt_s, linewidth=2, label="smoothed altitude")
plt.legend(); plt.xlabel("Time (s)"); plt.ylabel("Altitude (m)"); plt.title("Altitude vs Time")
plt.grid(True) 
plt.show(block=False)

plt.figure(figsize=(10,5))
plt.plot(time_clean, vel, alpha=0.5, label="raw velocity")
plt.plot(time_clean, vel_s, linewidth=2, label="smoothed velocity")
plt.legend(); plt.xlabel("Time (s)"); plt.ylabel("Velocity (m/s)"); plt.title("Velocity vs Time")
plt.grid(True)
plt.show(block=False)

# animation
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, max(time_clean))
ax.set_ylim(0, max(alt_s)*1.1)
ax.set_xlabel("Time (s)"); ax.set_ylabel("Altitude (m)")
ax.set_title("Altitude")

xdata, ydata = [], []
def update(frame):
    xdata.append(time_clean[frame])
    ydata.append(alt_s[frame])
    line.set_data(xdata, ydata)
    return line,

ani = animation.FuncAnimation(fig, update, frames=len(time_clean),
                              blit=True, interval=500, repeat=False)
plt.grid(True)
plt.show()