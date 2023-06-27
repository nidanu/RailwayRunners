"""
name: sample.py

By: RailwayRunners

Does: extracting and primary testing algorithm data 
"""
import statistics
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import random
import csv

number_of_scores = int(input("Amount of random samples per dataset: "))
datasets = ["greedy_scores.txt", "all_scores_n.txt", "all_scores_m.txt"]
for dataset in datasets: 
    
    # Prints progress with names and lenght of documents
    with open(dataset, "r") as f:
        length = len(f.readlines())
        print(f"{dataset}: {length}")
    
    # Creates list of x random sample results
    with open(dataset, "r") as f:
        i = 0
        all_scores = []
        for line in f.readlines():
            all_scores.append(float(line.strip()))
        subsection_scores = []
        while i < number_of_scores:
            random_line_number = random.randint(0, length - 1)
            subsection_scores.append(all_scores[random_line_number])
            i += 1
        
    average = statistics.mean(all_scores)
    median = statistics.median(all_scores)

    print(f"Avarage: {average}")
    print(f"Median: {median}")
    print(f"Maximum: {max(all_scores)}")
    all_scores.remove(max(all_scores))
    print(f"Maximum: {max(all_scores)}")
    all_scores.remove(max(all_scores))
    print(f"Maximum: {max(all_scores)}")

    
    
    # creates csv with x random sample  results of all algorithms 
    with open("all_results_"+ str(number_of_scores) +".csv", "a", newline="") as f:
        writer = csv.writer(f)
        for score in subsection_scores:
            writer.writerow([dataset, score])
    
    """
    # Function that draws a histogram
    def draw_histogram(data, bins):
        plt.hist(data, bins=bins, edgecolor='black', color='darkblue', alpha=1)
        plt.xlabel("Scores", fontsize=15, weight="bold")
        plt.ylabel("Frequency", fontsize=15, weight="bold")
        
        # Set the background color
        plt.gca().set_facecolor('yellow')
        plt.gca().set_alpha(0.1)
        
        if dataset == datasets[0]:
            plt.title("Greedy " + str(number_of_scores) + " Runs", fontsize=20)
        if dataset == datasets[1]:
            plt.title("GRandom " + str(number_of_scores) + " Runs", fontsize=20)
        if dataset == datasets[2]:
            plt.title("GRandom Max " + str(number_of_scores) + " Runs", fontsize=20)
            
        plt.savefig("hist_" + dataset[:-4] + "_" + str(number_of_scores) + ".png", dpi=300)
        plt.close()

    # Set hist variables 
    my_data = subsection_scores
    num_bins = 16
    draw_histogram(my_data, num_bins)
    """
    """
    # Shapiro-Wilk Test
    shapiro_test = stats.shapiro(subsection_scores)
    print("Shapiro-Wilk Test:")
    print(f"Statistic: {shapiro_test.statistic}")
    print(f"P-value: {shapiro_test.pvalue}")
    """
