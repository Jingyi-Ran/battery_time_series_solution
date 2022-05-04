import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def get_t(path):
    return int(path[:-4].split("_")[-1])

def read_and_clean_data(path):
    
    df = pd.read_csv(path)
    t = int(path[:-4].split("_")[-1])
    time = np.arange(0, len(df)*t, t).tolist()
    df['Time'] = time
    
    return df["Time"], df["0.0"]

def visualize_data(xpoints_list, ypoints_list, files):
    
    figure(figsize = (13.5, 4.5), dpi = 100)
    for i in range(len(files)):
        plt.plot(xpoints_list[i], ypoints_list[i], label = files[i], linewidth = '1.5')

    plt.legend(bbox_to_anchor = (1.16, 1.0), loc = 'upper right')
    plt.xlabel("Time (Sec)", fontsize = 12);
    plt.ylabel("Signal", fontsize = 12);

    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)

    plt.show()

def extract_metrics(xpoints, ypoints):
    
    xs, ys = find_zero(xpoints, ypoints)
    visualize_find_zero(xs, ys, xpoints, ypoints, color = "tab:blue", label = "Sample")
    freq = frequency(xs[0], xs[1])
    xs, ys = find_local_max(xpoints, ypoints)
    visualize_local_max(xs, ys, xpoints, ypoints, color = "tab:blue", label = "Sample")
    max_idx, xs_max, ys_max = find_global_max(xs,ys)
    decay = decay_time(xs, ys, ys_max)
    
    return freq, decay

def visualize_metrics(x1, x2, freq_list, decay_list, files):
    
    visualize_distribution_of_frequency_values(x1)
    visualize_distribution_of_decay_times(x2)
    visualize_scatter(freq_list, decay_list, files)
    
    plt.show()

#.........................................................................................

def find_zero(xpoints, ypoints):
    xs = []
    ys = []
    for i in range(len(ypoints)-1):
        if ypoints[i] == 0 and ypoints[i+1] == 0:
            break
        if ypoints[i] >= 0 and ypoints[i+1] <= 0:
            print(xpoints[i], ypoints[i], ypoints[i+1])
            xs.append(xpoints[i])
            ys.append(ypoints[i]) 
    return xs, ys

def visualize_find_zero(xs, ys, xpoints, ypoints, color = "tab:blue", label = "Sample"):
    plt.figure(figsize = (8, 4.5), dpi = 100)

    plt.plot(xpoints, ypoints, label = label, mec = color, 
             mfc = color, color = color, linewidth = '1')
    plt.scatter(xs, ys, color = "black")
    plt.legend(loc = "upper right")
    plt.xlabel("Time (Sec)", fontsize = 12);
    plt.ylabel("Signal", fontsize = 12);

    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)

    plt.show()
    
def frequency(a, b):
    
    return 1/(b - a)

def find_local_max(xpoints, ypoints):
    xs = []
    ys = []
    for i in range(len(ypoints)-1):
        if ypoints[i] > ypoints[i+1] and ypoints[i] > ypoints[i-1] :
            print(xpoints[i], ypoints[i], ypoints[i+1])
            xs.append(xpoints[i])
            ys.append(ypoints[i])
    return xs, ys

def visualize_local_max(xs, ys, xpoints, ypoints, color = "tab:blue", label = "Sample"):
    plt.figure(figsize = (8, 4.5), dpi = 100)

    plt.plot(xpoints, ypoints, label = label, mec = color, 
             mfc = color, color = color, linewidth = '1')
    plt.scatter(xs, ys, color = "black")
    plt.legend(loc = "upper right")
    plt.xlabel("Time (Sec)", fontsize = 12);
    plt.ylabel("Signal", fontsize = 12);

    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)

    plt.show()
    
def find_global_max(xs, ys):
    # initialize max with first element   
    max_val = ys[0]
    max_idx = 0

    # loop
    for i in range(1, len(xs)):    
        # compare elements with max    
        if(ys[i] > max_val):    
            max_val = ys[i]
            max_idx = i  

    return max_idx, xs[max_idx], ys[max_idx]   


def decay_time(xs, ys, max_val):
    # threshold    
    thr = max_val*0.8
    idx = -1

    for i in range(1, len(xs)):    
        # scan the list from the last point instead of the first!
        # find the first point > thr
        if(ys[len(xs)-i] > thr):    
            idx = len(xs) - (i-1)
            break
    if idx != len(xs):       
        return xs[idx]   
    else:
        return np.nan

def visualize_distribution_of_frequency_values(x1):
    plt.figure(figsize = (9, 4.5), dpi = 100)

    plt.hist(x = x1, bins = 'auto', 
         color = 'indianred', alpha = 0.7, rwidth = 0.99)

    plt.title('Distribution of Frequency Values', fontsize = 14)
    plt.xlabel('Frequency (Hz)', fontsize = 12)
    plt.ylabel('Number of Samples', fontsize = 12)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.grid(axis = 'y', alpha = 0.75)

    plt.show()
    
def visualize_distribution_of_decay_times(x2):
    plt.figure(figsize = (9, 4.5), dpi = 100)

    plt.hist(x = x2, bins = 10, 
         color = 'navy', alpha = 0.7, rwidth = 0.99)

    plt.title('Distribution of Decay Times', fontsize = 14)
    plt.xlabel('Decay Time (sec)', fontsize = 12)
    plt.ylabel('Number of Samples', fontsize = 12)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.grid(axis = 'y', alpha = 0.75)

    plt.show()
    
def visualize_scatter(freq_list, decay_list, files):
    figure(figsize = (7, 7), dpi = 100)

    for i in range(len(files)):
        plt.scatter(x = freq_list[i], y = decay_list[i], label = files[i])

    plt.legend(loc = 'upper right')

    plt.xlabel('Frequency (Hz)', fontsize = 12)
    plt.ylabel('Decay Time (sec)', fontsize = 12)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    
    plt.show()