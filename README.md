# Quantum circuit tensor network simulation challenge

This repository contains the results from public tier participants in Quantinuum's challenge for Tensor Network simulations.

The files originally sent to the participants can be downloaded from Zenodo at [https://doi.org/10.5281/zenodo.15878875](https://doi.org/10.5281/zenodo.15878875). These include the suite of quantum circuits provided by Quantinuum.

The file `report.pdf` contains the conclusions drawn from the results.

The following scripts generate the figures included in `report.pdf`:

- `python expval_diff_heatmap.py` generates the heat maps comparing expectation values.
- `python ranking.py <mirror_fidelity>` generates the rankings for the different circuit families according to runtime, only including simulations where the mirror fidelity is greater or equal to the argument provided.


## Continued improvements

Current public tier participants, as well as new ones, are welcome to contribute with PRs to this repository, adding new submissions following the format specified in the `Instructions.pdf` file.
Please contact `pablo.andresmartinez@quantinuum.com` if you wish to contribute with a new submission.


