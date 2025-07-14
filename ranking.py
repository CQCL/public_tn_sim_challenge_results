from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import sys

if len(sys.argv) != 2:
    raise Exception("Usage: python runtime_bands <min_fidelity>")
min_fid = float(sys.argv[1])

family_circs = defaultdict(list)
with open("metadata.csv", "r") as f:
    for l in f.readlines()[1:]:  # Ignore the header
        circname = l.split(",")[0]
        family = l.split(",")[1]
        if "t_injections" not in circname:  # Ignore t_injections bonus circuits
            family_circs[family].append(circname)
participants = list()

all_circs = sum(family_circs.values(), [])
runtime_per_circ = dict()
for subdir in Path(".").iterdir():
    if subdir.is_dir() and ".git" not in str(subdir):
        this_participant = str(subdir)
        participants.append(this_participant)
        runtime_per_circ[this_participant] = {c: float("inf") for c in all_circs}
        for subsubdir in subdir.iterdir():
            if subsubdir.is_dir():
                df = pd.read_csv(subsubdir / "METRICS.csv")
                for index, row in df.iterrows():
                    circname = row["circuit_name"]
                    mirror_fid = row["mirror_fidelity"]
                    # Computing total_time = simulation_time + preprocessing_time + shot_time
                    # as defined in the instructions. Some participants added expectation_value_time
                    # to their total_runtime column, which is why we are calculating it here explicitly
                    sim_time = float(row["simulation_time"])
                    pre_time = float(row["preprocessing_time"])
                    shot_time = float(row["shot_time"])
                    total_time = sim_time + pre_time + shot_time
                    # Include it if it satisfies the threshold for this fidelity band
                    if mirror_fid != "" and float(mirror_fid) >= min_fid:
                        prev_time = runtime_per_circ[this_participant][circname]
                        runtime_per_circ[this_participant][circname] = min(prev_time, total_time)

# Create one figure per family of circuits
participant_color = {p: col for p, col in zip(participants, plt.cm.Set1.colors)}
for family, circs in family_circs.items():
    # Sort the circs so that fastest goes first
    circ_best_time = list()
    for c in circs:
        best_time = float("inf")
        for p in participants:
            best_time = min(best_time, runtime_per_circ[p][c])
        circ_best_time.append((c, best_time))
    circ_best_time.sort(key=lambda tup: tup[1], reverse=True)
    sorted_circs = [c for c, _ in circ_best_time]

    plt.plot([0.0]*len(sorted_circs), sorted_circs, color="black")

    for participant in participants:
        times = [runtime_per_circ[participant][c] for c in sorted_circs]
        plt.plot(times, sorted_circs, color=participant_color[participant], label=participant, marker="o")

    plt.legend()
    plt.grid(visible=True, which="both", linewidth=0.3)
    plt.xlabel('Runtime (seconds)')
    plt.xscale("log")
    plt.ylabel('Circuit')
    plt.title(family)
    plt.show()
