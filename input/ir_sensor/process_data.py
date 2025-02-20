import pandas as pd
import matplotlib.pyplot as plt

file_path = "sample_data.csv"
df = pd.read_csv(file_path, header=None)

# Change num groups to see the effects of number of samples we do for smoothing the signal
# Setting num_groups to 1 shows the original data
num_groups = 1
df['group'] = df.index // num_groups
min_df = df.groupby('group')[0].min().reset_index(drop=True)

plt.figure(figsize=(10, 5))
plt.plot(min_df.index, min_df, marker='o', linestyle='-')  

plt.xlabel("Grouped Index")
plt.ylabel("Min Values")
plt.title("Min CSV Data Plot")
plt.ylim([0, 600])  
plt.grid()
plt.legend()
plt.show()

