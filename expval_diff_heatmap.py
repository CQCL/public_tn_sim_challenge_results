from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

family_circs = defaultdict(list)
with open("metadata.csv", "r") as f:
    for l in f.readlines()[1:]:  # Ignore the header
        circname = l.split(",")[0]
        family = l.split(",")[1]
        family_circs[family].append(circname)

all_circs = sum(family_circs.values(), [])
accurate_circs_per_submission = {c: list() for c in all_circs}
for subdir in Path(".").iterdir():
    if subdir.is_dir() and ".git" not in str(subdir):
        for subsubdir in subdir.iterdir():
            if subsubdir.is_dir():
                df = pd.read_csv(subsubdir / "METRICS.csv")
                for index, row in df.iterrows():
                    circname = row["circuit_name"]
                    mirror_fid = row["mirror_fidelity"]
                    if mirror_fid != "" and float(mirror_fid) >= 0.9:
                        accurate_circs_per_submission[circname].append(subsubdir)

for family, circs in family_circs.items():
    for c in circs:
        this_expvals = dict()
        submission_path = list()
        for i, submission in enumerate(accurate_circs_per_submission[c]):
            with open(submission / "EXP_VAL.json", "r") as f:
                expvals = json.load(f)
            this_expvals[i] = expvals[c]
            submission_path.append(str(submission))

        # Create the matrix of differences for the heat map
        n_submissions = len(this_expvals)
        if n_submissions == 0: continue
        diff_matrix = np.zeros((n_submissions, n_submissions))
        for sub1, expvals1 in this_expvals.items():
            for sub2, expvals2 in this_expvals.items():
                max_diff = 0.0
                for pstr, v in expvals1.items():
                    max_diff = max(max_diff, abs(complex(expvals2[pstr]) - complex(v)))
                diff_matrix[sub1][sub2] = max_diff

        # Display the heat map
        fig, ax = plt.subplots()
        im = ax.imshow(diff_matrix, vmin=0.0, vmax=0.15)
        cbar = plt.colorbar(im)
        cbar.ax.set_ylabel("Max exp_val diff", rotation=-90, va="bottom")

        # Show all ticks and label them with the respective list entries
        ax.set_xticks(range(len(submission_path)), labels=submission_path,
                    rotation=45, ha="right", rotation_mode="anchor")
        ax.set_yticks(range(len(submission_path)), labels=submission_path)

        ax.set_title(c)
        plt.tight_layout()
        plt.show()


