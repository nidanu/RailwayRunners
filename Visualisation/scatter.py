#!/usr/bin/env python # 
"""
Plots results into a scatter plot.
"""
import matplotlib.pyplot as plt
from typing import Any
import sys
sys.path.append('..')
from Code.Classes.station import Station

def scatter_plot(filename: str) -> None:
    """
    Creates scatter plot for scores of all results, with mean & best score
    """
    x = []
    trajectories = []

    with open(filename, "r") as f:
        next(f)
        num_lines = len(f.readlines())

    with open(filename, "r") as f:
        next(f)
        for i in range(num_lines):
            line = f.readline().rstrip('\n')

            if line[1].isdigit():
                scores = line.split(',')
                scores = [float(score) for score in scores]
                x = scores
            else:
                station = line.split(',')
                trajectories.append(station)


    minimum = min(x)
    maximum = max(x)
    mean = sum(x) / len(x)
    y = x

    caption = "Scores"
    text = "Best route:\n"
    for i in range(len(trajectories)):
        text += f" {i+1}: {', '.join(trajectories[i])}\n"    

    plt.scatter(x, y, s=8)

    # Plot minimum, maximum, and mean
    plt.scatter(x[scores.index(minimum)], minimum, color='red', label='Lowest',s=30)
    plt.scatter(x[scores.index(maximum)], maximum, color='darkorange', label='Maximum',s=30)
    plt.scatter(x[int(len(scores) / 2)], mean, color='deeppink', label='Mean', marker ="^",s=60)

    # Create legend
    plt.legend()

    # Add space to bottom to fit text
    plt.subplots_adjust(bottom=0.4, top=0.8)

    # Add title & textbox
    plt.title(caption)
    textbox_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='black')
    
    # Add the textbox to the plot
    plt.text(0.005, 0.07, text, fontsize=10, bbox=textbox_props, transform=plt.gcf().transFigure)

    plt.show()