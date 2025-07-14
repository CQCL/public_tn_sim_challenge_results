This document summarizes the hardware, simulation algorithms, and benchmarking methodology used in this submission

1. Hardware Specifications
- CPU: Intel® Xeon® w5-2545
    - Cores/Threads: 12/24
    - Max Turbo Frequency: 4.5 GHz (base frequency 800 MHz)
    - Architecture: 64-bit
- RAM: 128 GiB DDR4
- Operating System: NixOS 25.05 (Warbler)
- GPU: Not used (code is CPU only for now)

2. Simulation Algorithm Description
MIMIQ employs a highly optimized quantum circuit emulator based on the Matrix Product State (MPS) formalism, featuring advanced circuit preconditioning and Matrix Product Operator (MPO) compression to efficiently simulate large and moderately entangled quantum systems.
- Efficient handling of 2-qubit gates and n-qubit gates via decomposition.
- In-house tensor library designed to minimize computational and memory overheads
- Expectation value computation and sampling directly from the MPS representation.
- Other key features include: native OpenQASM 2.0 support; fidelity estimation, mid-circuit measurements; conditional gates; parametric gates; three different MPO compression methods, user adjustable bond dimension, entanglement dimension, and cutoffs; automatic qubit ordering, and more.

3. Circuit Format and Gate Support
- Input Format: All simulations use the provided QASM files, imported using MIMIQ's OpenQASM parser
- Multicontrol gates are supported natively. Other n-qubit gates (n > 2) are decomposed into sequences of 1- and 2-qubit gates.

4. Trade-off Description
For each benchmark circuit we tuned the emulator hyperparameters (e.g., bond dimension, entanglement dimension, cutoff) to achieve the lowest runtime while ensuring the mirror fidelity remains above the highest achievable threshold. Global optimality is not guaranteed. Mirror circuit fidelity was calculated by first simulating the forward circuit to obtain the final MPS, then applying the inverse (dagger) circuit to this state (no gate cancellation possible). For certain circuits, higher fidelities may be achievable without a substantial increase in runtime; alternatively, reducing fidelity can lead to faster runtimes. 

5. Algorithm Parameters
- Emulator hyperparameters were optimized per circuit to minimize runtime while maintaining fidelity above the required threshold.

6. Additional Sources of Inaccuracy
- Precompilation and CPU variability: Timing is based on the minimum of three executions to reduce these effects, except for simulations exceeding 1,000 seconds.
- Fidelity estimates are calculated on the basis of the MPS truncations. These are lower bounds for the forward circuit only.
- We note that many of the requested expectation values are below machine precision
- Expectation values and shots follow the qubit ordering defined by the QASM file, which is increasing lexicographic order if registers are alphabetically ordered.

7. Access to Simulation Algorithm
- Mimiq is a proprietary simulation framework. It is currently available to users as a cloud-based SaaS platform with an on-premise version planned to be released in 2025. 
- For further information please see our documentation at docs.qperfect.io or contact shannon.whitlock@qperfect.io

8. Additional Notes
- Timing: All times are reported in seconds.
- Memory: All memory usage is reported in megabytes (MB).
- Timing Method: Minimum of three executions is used for timing, except for runs exceeding 1,000 seconds, where only one execution is performed.
- Data Source: All simulations use only the data from the provided QASM files.
- Missing Entries indicate that fidelity > 0.2 was not achieved within the allocated time.
- Fidelity: Estimates are lower bounds for the forward circuit only.
- Parameter Optimization: Emulator hyperparameters were independently optimized for each benchmark circuit to minimize runtime while maintaining mirror fidelity above threshold. Global optimality is not guaranteed.
- All chemistry_uccsd circuits were infeasible within the allocated time using the provided QASM files. This may be rectified in the near future as we are developing an efficient MPS implementation of PauliExpBox.
- QEC Circuits: The logical qubit encoding for qec_non_ft circuits in the "hard" category was unfamiliar to us. Further study is needed to determine if a more efficient MPS representation might be suitable.
- Qubit Ordering: Expectation values and shots follow the qubit ordering defined by the QASM file.

