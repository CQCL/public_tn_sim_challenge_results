from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

family_circs = defaultdict(list)
with open("metadata.csv", "r") as f:
    for l in f.readlines()[1:]:  # Ignore the header
        circname = l.split(",")[1]
        family = l.split(",")[2]
        if "t_injections" not in circname:  # Ignore t_injections bonus circuits
            family_circs[family].append(circname)
participants = list()

all_circs = sum(family_circs.values(), [])
mirror_fidelities = dict()
for subdir in Path(".").iterdir():
    if subdir.is_dir() and ".git" not in str(subdir):
        this_participant = str(subdir)
        participants.append(this_participant)
        mirror_fidelities[this_participant] = dict()
        for subsubdir in subdir.iterdir():
            if subsubdir.is_dir():
                df = pd.read_csv(subsubdir / "METRICS.csv")
                for index, row in df.iterrows():
                    circname = row["circuit_name"]
                    mirror_fid = row["mirror_fidelity"]
                    # Include it if it satisfies the threshold for the 0.9 fidelity band
                    if mirror_fid != "" and float(mirror_fid) >= 0.9:
                        mirror_fidelities[this_participant][circname] = max(mirror_fid, mirror_fidelities[this_participant].get(circname, 0.0))

# Create one figure per family of circuits
for family, circs in family_circs.items():

    for i, participant in enumerate(participants):
        data = list()
        for c in circs:
            if c in mirror_fidelities[participant].keys():
                data.append(mirror_fidelities[participant][c])
        jitter_x_axis = [i + (1 - 2*np.random.rand())*0.2 for _ in data]
        plt.scatter(jitter_x_axis, data, color="blue", marker="x")

    # Create boxplot
    plt.plot([-0.5, 3.5], [0.9, 0.9], color="gray", linewidth=2, linestyle="--")
    plt.title(family)
    plt.ylabel('Mirror fidelity')
    plt.xticks(ticks=[0,1,2,3], labels=participants, rotation=45)
    plt.ylim([0.87, 1.0])
    plt.tight_layout()
    plt.show()
