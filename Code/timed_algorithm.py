#!/usr/bin/env python 
"""
Runs an algorithm for up to an hour. Every run times out after one minute.
Writes scores to scores.csv.
"""
import subprocess
import time
import csv
from typing import List

def run_algorithm(algorithm: str):
    start = time.time()
    n_runs = 0

    # Path to the CSV file
    csv_file_path = '../Results/%s.csv' % (algorithm + "_results")

    scores = []
    while time.time() - start < 3600:
        print(f"run: {n_runs}")

        # Times out after 60 seconds
        score = subprocess.call(["timeout", "60", "python3", "Algorithms/greedy.py"])
        n_runs += 1
        scores.append(score)

        # Writes to file after every 1000 runs
        if (n_runs % 1000) == 0:
            save_results(csv_file_path, scores)
            scores = []
    
def save_results(csv_file_path: str, scores: List[int]) -> None:
    # Write results to scores.csv
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(scores)



run_algorithm('greedy.py')