import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

SERIAL_PORT = 'COM10'  
BAUD_RATE = 9600
DATA_POINTS = 200
Y_LOWER_LIM = 0
Y_UPPER_LIM = 4096

# DATA_POINTS = 2000
# Y_LOWER_LIM = -2
# Y_UPPER_LIM = 2

data_buffer_0 = deque(maxlen=DATA_POINTS)
data_buffer_1 = deque(maxlen=DATA_POINTS)
data_buffer_2 = deque(maxlen=DATA_POINTS)

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0)
print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

fig, ax = plt.subplots()
ax.set_title("Real-Time Serial Data Plot")
ax.set_xlabel("Data Points")
ax.set_ylabel("Value")

line0, = ax.plot([], [], lw=2)
line1, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)
ax.legend()

text0 = ax.text(0.3, 0.95, '', transform=ax.transAxes, ha='center', color='blue', fontsize=12)
text1 = ax.text(0.5, 0.95, '', transform=ax.transAxes, ha='center', color='orange', fontsize=12)
text2 = ax.text(0.7, 0.95, '', transform=ax.transAxes, ha='center', color='green', fontsize=12)

def init():
    # ax.set_xlim(0, DATA_POINTS * 2 - 1)
    ax.set_xlim(0, DATA_POINTS  + 10)
    ax.set_ylim(Y_LOWER_LIM, Y_UPPER_LIM)  
    line0.set_data([], [])
    line1.set_data([], [])
    line2.set_data([], [])

    text0.set_text("")
    text1.set_text("")
    text2.set_text("")
    return line0, line1, line2, text0, text1, text2

def update(frame):
    global data_buffer_1, data_buffer_2
    
    try:
        while ser.in_waiting > 0:
            line_data = ser.readline().decode('utf-8').strip()
            print(line_data, end=" ")
            if line_data:
                if "L" in line_data or "H" in line_data:
                    if line_data[1] == "0":
                        text0.set_text(line_data)
                    elif line_data[1] == "1":
                        text1.set_text(line_data)
                    else:
                        text2.set_text(line_data)
                else:
                    channel, data = line_data.split(":")
                    value = float(data)
                    if int(channel) == 0:
                        data_buffer_0.append(value)
                    elif int(channel) == 1:
                        data_buffer_1.append(value)
                    elif int(channel) == 2: 
                        data_buffer_2.append(value)
                    else:
                        print("Unknown channel")
        print()

    except serial.SerialException as e:
        print(f"Serial error: {e}")

    line0.set_data(range(len(data_buffer_0)), data_buffer_0)
    line1.set_data(range(len(data_buffer_1)), data_buffer_1)
    line2.set_data(range(len(data_buffer_2)), data_buffer_2)
    return line0, line1, line2, text0, text1, text2


ani = animation.FuncAnimation(fig, update, init_func=init, blit=False, interval=1)

try:
    plt.show()
except KeyboardInterrupt:
    print("Plotting stopped.")

ser.close()
