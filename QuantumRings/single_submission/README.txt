– The specifications of the hardware used to run the simulation.
8x H100 (80 GB SXM5)
208 vCPUs, 1800 GiB RAM, 22 TiB SSD

– A brief description of the simulation algorithm used and the features
that may distinguish it from others

QuantumRings SDK implements the Schmidt basis using a tensorized representation.
The SDK works in a CPU only mode, GPU enabled mode, and a hybrid mode. The users
can select the operational mode depending upon the hardware and the circuit being used.

– Which of the circuit formats listed in section 2.6 was used, or if you
had to do some conversion. Indicate if your algorithm supports n-
qubit gates with n > 2 and, if not, how did you deal with them.

We used the circuits provided in the circuit suite/pytket_orig folder and its correspondng
dagger circuits. We flattened these circuits using PYTKET's unboxer functions and transpiled using
qiskit. The SDK supports multi-controlled gates such as mcp, mcrx, mcry, mcrz, mct, mcx. These are converted
into simpler gates internally.

– A brief description of the trade-off explored in this solution: e.g.
maximise fidelity or minimise resources.

We tried to maximize fidelity with in a reasonable compute time.

– Information about the parameters the algorithm admits and which
values were chosen for this submission (which may be different for
different circuits).

The SDK's run method takes in a threhold parameter which adjusts the execution space.
For each circuit, we experimented which value works best.

– Information on any additional source of inaccuracies that may not
be accounted for in the fidelity metrics from section 3.

SVD decomposition inaccuracies.

– Information on how we may access your simulation algorithm in the
future, e.g. open sourced, licensed, cloud, on-prem, etc.

Licensed as Quantum Rings SDK: https://www.quantumrings.com
Scripts to reproduce results here: https://github.com/Quantum-Rings/quantinuum-benchmark
to use these scripts you need version 0.11 from the Quantum Rings SDK which will be made publicly available soon.
