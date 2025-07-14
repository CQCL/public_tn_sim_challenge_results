
## Disclaimer

The package `pytket-cutensornet` is an open sourced library developed by Quantinuum (see repository [here](https://github.com/CQCL/pytket-cutensornet)) that is used to simulate pytket circuits using NVIDIA's [CuTensorNet](https://docs.nvidia.com/cuda/cuquantum/latest/cutensornet/index.html) library.

However, the MPS algorithm tested here is _not_ the implementation available in CuTensorNet. It is a custom implementation developed using CuTensorNet's lower level primitives `contract` and `decompose`. Consequently, the performance of the MPS algorithm in `pytket-cutensornet` may differ from that of the MPS offered by CuTensorNet.

## Submission data

You can find all submission data and scripts used to generate these in the following [public repository](https://github.com/CQCL/benchmarking_pytket_cutensornet/). **Note:** The `main` branch does not contain any data.
The repository contains two submissions. Each is included in a separate branch of the repository:

- [high_fidelity](https://github.com/CQCL/benchmarking_pytket_cutensornet/tree/faster_runtime) contains the simulation data of the circuits from the challenge that could be simulated. This submission corresponds to the attempt to reach the highest possible fidelity band for each circuit.
- [faster_runtime](https://github.com/CQCL/benchmarking_pytket_cutensornet/tree/faster_runtime) contains the simulation data of a subset of the circuits that were run in the previous submission, targeting a lower fidelity band and, hence, lower runtime and memory used.

Within each branch, you can find the filled in `METRICS.csv`, `EXP_VALS.json` and `SHOTS.json` files as described in the instructions of the challenge.
Furthermore, there is a `*_settings.txt` file at the root of the directory, including information of the parameter configuration used for each of the circuits.
Within the `settings/` folder you can find data for each of the runs. In the cases where the final MPS occupied less than 50MB, it has been included as a pickle file.

#### Reproducibility

All scripts used to generate the data are included in the repository linked above. The most important one is `run.py` that produces all of the data for a single circuit simulation and populates the data in the `settings/` directory. Files `main.sh` and `script.sh` are the scripts used to issue the job for each circuit; each job corresponds to a single execution of `run.py`. Finally, `prepare_submission.py` reads the contents of `settings/` and produces the submission files `METRICS.csv`, `EXP_VALS.json` and `SHOTS.json`.

## Hardware used

All simulations reported in this repository were run on Perlmutter with nodes of the following specifications:
- GPUs NVIDIA A100 (80GB VRAM)
- CPU AMD EPYC 7763
Each job was run on a single GPU. Since each compute node of Perlmutter contains 4 GPUs, four jobs were run in parallel per node.

This research used resources of the National Energy Research Scientific Computing Center (NERSC), a Department of Energy Office of Science User Facility using NERSC award DDR-ERCAP0032628.

## Brief description of the simulation algorithm

**Note**: this is _not_ the same algorithm as the MPS provided by NVIDIA's CuTensorNet library. See the disclaimer section above.

The state of the quantum circuit is stored as an MPS and evolved throughout the circuit by applying gates directly to it. After a two-qubit gate is applied, the bonds between the two qubits are truncated according to the policy selected in the `config.json` file (found inside each of the `settings/` subdirectories). There are two possible mutually exclusive configurations:
- **chi**. Sets the maximum value allowed for the dimension of the virtual bonds. Higher implies better approximation but more computational resources. If not provided, chi will be unbounded.
- **truncation_fidelity**. The virtual bond will be truncated to the minimum dimension that satisfies `|<psi|phi>|^2 >= trucantion_fidelity`, where `|psi>` and `|phi>` are the states before and after truncation (both normalised). If not provided, it will default to its maximum value 1.

#### Calculation of the fidelity estimate

Other than the mirror fidelity, which is calculated as described in the instructions for the challenge, we also provide a fidelity estimate _lower bound_.
This fidelity estimate is calculated as `Prod_i f_g` where `f_g` is the relative drop of fidelity after the truncation following gate `g`. This `f_g` is calculated as the sum of the squares of all of the singular values that were kept after truncation (before normalisation). When the error per truncation is low enough, this provides a lower bound of the actual fidelity of the state.
We observe that, for high fidelity circuits, the mirror fidelity and the fidelity estimate have similar values. There are also cases where the fidelity estimate is essentially zero, but the mirror fidelity is above `0.2` (an example of this is `XZ_square_PBC_J=1_dt=0.3_n_trotter_steps=16_Lx=8_Ly=7` in the `high_fidelity` submission); this is likely due to the product of small gate fidelities leads to the fidelity estimate quickly vanishing for deep circuits, while the real fidelity (better captured by the mirror fidelity) is higher.
The fidelity estimate only considers the application of the gates in the original circuit, whereas the mirror fidelity includes the application of the additional gates from the dagger of the circuit; consequently, in some rare cases the fidelity estimate may be higher than the mirror fidelity (an example of this is `mvsp_cauchy2d_fourier_d10_n40` from the `faster_runtime` submission).

#### Special features of the algorithm

A couple of features that deviate from standard MPS algorithms:
- _Two-qubit gates may be applied between distant qubits_. Rather than applying SWAPs to bring the qubits close, the two-qubit gate is first decomposed into two tensors connected by a bond, both of these tensors are contracted with the site tensor for the corresponding qubit, resulting in an MPS with an additional non-local virtual bond. The non-local virtual bond on one of the qubit sites is then separated from the site tensor using QR decomposition, and the `R` tensor is contracted with the next qubit in the MPS. This is repeated, each time reducing the distance of the non-local bond by one, until the `R` tensor reaches the site of the other qubit where the gate was applied. At this point, contracting the tensors gets rid of the non-local virtual bond introduced by the two-qubit gate, returning the tensor network to its MPS form. Truncation is applied across all of the bonds between the two qubits as discussed above; in the case of `truncation_fidelity`, we still guarantee that `|<psi|phi>|^2 >= trucantion_fidelity`, where `|psi>` is the state immediately after gate application (before truncation) and `|phi>` is the state after truncating the bonds between the two qubits where the gate was applied.
- _Multi qubit CnX gates, as well as Pauli gadgets are applied natively_. Rather than decomposing these into the two-qubit and single-qubit gates, they can be applied at once exploiting the fact that the MPO describing them has virtual bond dimension 2. The algorithm used is similar to the zip-up algorithm described [here](https://arxiv.org/abs/1901.05824). Truncation policies are applied in the same manner as for non-local two-qubit gates, where we truncate all bonds between the leftmost and rightmost qubits that were affected by the operation.

A shortcoming of the algorithm:
- The assignment of circuit qubits to MPS sites is direct, following the order in the circuit. It is likely that smarter ordering of the qubits would lead to better performance, but this has not been explored.

## Other details

Here we indicate other details requested from the README file by the instructions from the challenge.

- The circuits from `circuit_suite/pytket_orig` directory from the challenge were used. These contain multi-qubit CnX gates as well as Pauli gadgets, which were handled as discussed in the section above.
- The trade-offs explored by the two submissions are described in the "Submission data" section from this file.
- The parameters the algorithm admits are described in the previous section; these are `chi` and `truncation_fidelity`. Only one of the two can be set to a non-default value. The values for each of the simulations appear in the `*_settings.txt` file in the corresponding branch of the submission.
- There are no additional source of inaccuracies not accounted for by the fidelity metrics.
- The library is open sourced, including the custom MPS implementation (see repository [here](https://github.com/CQCL/pytket-cutensornet)). It uses NVIDIA's CuTensorNet as a dependecy, which is not open sourced (although it's Python interface is) but does not require a license to use.
