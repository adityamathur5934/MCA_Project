# Final Project Defense & Presentation Script: 4 Speaking Teammates

**Project Title:** Single-Cycle and 5-Stage Pipelined MIPS Processor with Memory Interface and Hazard Resolution  
**Evaluation:** Final Phase Academic Project Defense (100% Weighting)  
**Total Presentation Time:** 12 – 15 Minutes (approx. 3 – 4 minutes per speaker)  
**Target Slide Deck:** `presentation/final_presentation.pptx` (14 Slides, 16:9 Widescreen)  
**Verification Status:** 100% Verified (78/78 Assertions Passed across 6 Testbenches, 5 Benchmarks Validated)  

---

## Team Role & Responsibility Matrix

| Teammate | Academic / Architectural Role | Assigned Slides | Section Focus | Speaking Time |
| :--- | :--- | :--- | :--- | :--- |
| **Teammate 1** | **CPU Architecture & Integration Lead** | Slides 1 – 4 | Introduction, Scope Evolution, Harvard Memory Subsystem, Single-Cycle Baseline | 3:30 min |
| **Teammate 2** | **Pipelining & Microarchitecture Specialist** | Slides 5 – 8 | 5-Stage Pipeline Stages, Forwarding Unit, Hazard Detection Unit, ISA & Decoding | 3:45 min |
| **Teammate 3** | **Verification & Benchmark Lead** | Slides 9 – 11 | Verification Framework, Array Sum, Max Search, Factorial, Fibonacci, Bubble Sort | 3:45 min |
| **Teammate 4** | **Performance & Hardware Synthesis Lead** | Slides 12 – 14 | Performance Comparison (CPI/Speedup), FPGA Resource Utilization, Conclusion & Defense | 3:30 min |
| **Member 5** | **Technical Production & Live Demo Coordinator** | *All Slides* | **NON-SPEAKING ROLE:** Slide transitions, Terminal execution, GTKWave waveform navigation | 0:00 min |

---

## Detailed Scene-by-Scene Spoken Script

```
========================================================================================
PART 1: PROJECT INTRODUCTION, SCOPE EVOLUTION & BASELINE ARCHITECTURE
Speaker: TEAMMATE 1 (Slides 1 to 4 | Time: 0:00 – 3:30)
========================================================================================
```

### [SLIDE 1: Title & Team Introduction]
*(Visual: Slide 1 showing Title, Subtitle, and all 5 Team Members)*

**TEAMMATE 1:**  
"Respected evaluators and professors, good morning. We are presenting our final academic project: the **Design, Implementation, and Hardware Verification of Single-Cycle and 5-Stage Pipelined MIPS Processors with Memory Interface and Hazard Resolution**.

Our team consists of five members: myself, serving as the CPU Architecture and Integration Lead; Teammate 2, our Pipelining and Microarchitecture Specialist; Teammate 3, our Verification and Benchmark Lead; Teammate 4, our Performance and Hardware Synthesis Lead; and Member 5, who is serving as our technical production and demonstration coordinator.

In this project, we did not merely build a theoretical model. We developed synthesizable, cycle-accurate hardware in Verilog HDL, starting from a baseline single-cycle core and evolving it into a fully pipelined processor equipped with dedicated data forwarding and hazard detection units. Today, we will walk you through the architectural principles, hardware implementation, automated verification, and benchmark performance of our design."

---

### [SLIDE 2: Project Evolution: Phase I Baseline to Final Phase Pipelining]
*(Visual: Slide 2 showing the comparison cards between Phase I Single-Cycle and Final Phase Pipelining)*

**TEAMMATE 1:**  
"To appreciate the microarchitectural choices made in this project, we must examine the progression from our Phase I baseline to the final deliverable.

In Phase I, our objective was to establish a functionally verified, 32-bit single-cycle MIPS core. That architecture achieved an ideal Cycles Per Instruction—or CPI—of 1.0. Every instruction, from fetch to write-back, completed within a single clock cycle. However, as computer architecture theory dictates, the clock period in a single-cycle machine is strictly bounded by the cumulative propagation delay of its slowest instruction—specifically the Load Word path.

For the Final Phase, our engineering goal was to break this critical path limitation. We evolved the core into a balanced **5-stage classic pipeline** consisting of Instruction Fetch, Decode, Execute, Memory Access, and Write-Back. To maintain correctness without degrading throughput, we incorporated a **Data Forwarding Unit** that eliminates stalls for back-to-back arithmetic instructions, and a **Hazard Detection Unit** that handles Load-Use dependencies and branch penalties. This evolutionary design scaled our estimated operating frequency from approximately 55 MHz to over 185 MHz on a Xilinx Artix-7 FPGA."

---

### [SLIDE 3: System Architecture & Harvard Memory Subsystem]
*(Visual: Slide 3 showing the Harvard Memory Architecture cards and bus interconnect details)*

**TEAMMATE 1:**  
"A fundamental design requirement of our system is the memory hierarchy. We implemented a strict **Harvard Architecture**, separating Instruction Memory from Data Memory.

In a pipelined processor, an instruction fetch occurs in the IF stage simultaneously with a memory read or write occurring in the MEM stage. If a unified Von Neumann memory were used, this would create an unavoidable structural hazard, stalling the processor every time a Load or Store executed. By employing independent Instruction ROM and Data RAM, both memories can be accessed concurrently on every clock cycle.

Both memories are 256 words—or 1024 bytes—deep and enforce strict **32-bit word alignment**. Addressing uses bits [9:2] of the byte address, discarding the lower two bits. The Instruction Memory is combinational and supports preloading assembled machine code via `$readmemh`. The Data Memory features combinational read ports and synchronous, edge-triggered write ports, ensuring glitch-free memory transactions.

Our top-level wrapper cleanly encapsulates the CPU core and memories while exposing a comprehensive debug bus for real-time observability."

---

### [SLIDE 4: Single-Cycle Baseline Architecture & Critical Path Bottleneck]
*(Visual: Slide 4 showing the Single-Cycle datapath breakdown and critical path timing analysis)*

**TEAMMATE 1:**  
"Here we see the baseline single-cycle datapath. It consists of the Program Counter, the 32-by-32-bit Register File with hardware write protection on Register `$zero`, the 32-bit ALU supporting addition, subtraction, logical operations, and signed set-on-less-than, the combinational Control Unit, and the branch and jump multiplexers.

While conceptually straightforward, timing analysis reveals its fatal flaw. The clock period $T_{clk}$ must accommodate:
$$T_{clk} \ge T_{PC} + T_{IMEM} + T_{RF\_read} + T_{ALU} + T_{DMEM} + T_{MUX} + T_{setup}$$

In our RTL synthesis estimation, this path totals approximately 18.1 nanoseconds, capping the maximum clock frequency at around 55 MHz. Most instructions, such as ADD or BEQ, complete long before the clock period ends, leaving the datapath idle and wasting valuable time.

To eliminate this inefficiency, we segmented this monolithic path into five discrete pipeline stages. I will now hand over to **Teammate 2** to explain our 5-stage pipelined architecture and hazard resolution mechanisms."

```
[VERBAL HANDOVER: Teammate 1 nods to Teammate 2; Teammate 2 takes the floor]
```

---

```
========================================================================================
PART 2: 5-STAGE PIPELINING & HAZARD RESOLUTION MECHANISMS
Speaker: TEAMMATE 2 (Slides 5 to 8 | Time: 3:30 – 7:15)
========================================================================================
```

### [SLIDE 5: 5-Stage Classic Pipeline Datapath]
*(Visual: Slide 5 showing the 5 pipeline stages: IF, ID, EX, MEM, WB and the pipeline registers)*

**TEAMMATE 2:**  
"Thank you, Teammate 1. I am Teammate 2, and I will walk you through the microarchitecture of our 5-stage pipelined processor.

To achieve high clock frequencies, we inserted four synchronous pipeline registers between the execution stages:
1. **IF/ID Register:** Captures the fetched 32-bit instruction and the sequential $PC+4$. It supports synchronous stall and flush controls.
2. **ID/EX Register:** Buffers decoded control signals, register read data, sign-extended immediates, and operand register addresses. It features an active-high flush input to insert pipeline bubbles.
3. **EX/MEM Register:** Holds the ALU execution result, the write-data operand for Store instructions, the destination register address, and memory control lines.
4. **MEM/WB Register:** Buffers memory read data and the ALU result, delivering them to the Write-Back stage.

In the Write-Back stage, a multiplexer selects between memory data and the ALU result, committing the value to the Register File on the next rising clock edge. To eliminate half-cycle structural register stalls, we implemented an internal write-before-read bypass inside the register file, allowing an instruction in Decode to read data being written back by an instruction in Write-Back during the exact same clock cycle."

---

### [SLIDE 6: Forwarding Unit: Resolving RAW Hazards without Stalls]
*(Visual: Slide 6 showing the Forwarding Unit truth table, multiplexer paths, and example)*

**TEAMMATE 2:**  
"The primary challenge in pipelining is handling hazards. The most frequent data hazard is Read-After-Write, or RAW, where an instruction requires the result of a preceding instruction that has not yet committed to the register file.

Without hardware intervention, the processor would need to stall for two full cycles between dependent instructions. To solve this, we implemented a dedicated **Data Forwarding Unit**.

The Forwarding Unit continuously monitors register write-enable signals and destination register numbers from both the EX/MEM and MEM/WB pipeline stages, comparing them against the source registers `rs` and `rt` in the Execute stage:
- **EX Hazard:** If an instruction in EX requires data produced by the instruction immediately ahead in EX/MEM, the unit sets the forward multiplexer to `2'b10`, routing the ALU result directly back to the ALU input.
- **MEM Hazard:** If the dependency is with an instruction two cycles ahead in MEM/WB, the forward multiplexer is set to `2'b01`, routing write-back data to the ALU input.

As demonstrated on the slide, in a sequence like `ADDI $t1, $0, 10` followed immediately by `ADD $t2, $t1, $t1`, the Forwarding Unit supplies the value 10 to both ALU inputs with **zero stall penalty**, preserving a perfect 1.0 CPI for arithmetic sequences."

---

### [SLIDE 7: Hazard Detection Unit: Load-Use Stalls & Branch Flushes]
*(Visual: Slide 7 showing the Load-Use stall condition, bubble insertion, and branch flush logic)*

**TEAMMATE 2:**  
"However, forwarding alone cannot resolve every dependency. Specifically, during a **Load-Use Data Hazard**, an instruction attempts to consume a register loaded by an immediately preceding `LW` instruction. Because memory read data is not valid until the end of the MEM stage, the data simply does not exist in time for the EX stage of the following instruction.

Our **Hazard Detection Unit** detects this specific condition in the Decode stage:
$$\text{id\_ex\_mem\_read} \land ((\text{id\_ex\_rt} == \text{if\_id\_rs}) \lor (\text{id\_ex\_rt} == \text{if\_id\_rt}))$$

When this condition evaluates to true, the unit takes three coordinated actions:
1. It disables the Program Counter update (`pc_stall = 1`), holding the current fetch address.
2. It disables the IF/ID pipeline register (`if_id_stall = 1`), preserving the dependent instruction in Decode.
3. It asserts `id_ex_flush = 1`, inserting a bubble—equivalent to a NOP—into the ID/EX register.

After this single stall cycle, the loaded data reaches the MEM/WB stage, where our Forwarding Unit forwards it directly into the ALU.

For control hazards, branches are evaluated in the Execute stage using forwarded operands. When a branch is taken, the Hazard Detection Unit flushes the misfetched instructions in IF/ID and ID/EX, ensuring that incorrect path instructions never alter processor or memory state."

---

### [SLIDE 8: Instruction Set & Control Decoding Matrix]
*(Visual: Slide 8 showing the Main Control Unit truth table across all 10 supported opcodes)*

**TEAMMATE 2:**  
"On Slide 8, you can see our comprehensive Control Decoding Matrix. The Main Control Unit is purely combinational, decoding the 6-bit instruction opcode to produce nine distinct control signals.

For R-type instructions, `RegDst` routes the destination address to `rd`, `ALUSrc` selects the register operand, `RegWrite` is asserted, and `ALUOp` is set to `2'b10`, directing the ALU Control unit to decode the 6-bit `funct` field. For Load Word, `MemRead`, `ALUSrc`, `MemtoReg`, and `RegWrite` are asserted. For Store Word, `MemWrite` and `ALUSrc` are active while register writes are disabled. Branch Equal asserts the `Branch` line and selects ALU subtraction to generate the Zero flag.

Crucially, our control unit incorporates a safe default state: any unsupported or illegal opcode deasserts all control lines, ensuring predictable behavior and avoiding spurious register or memory writes.

I will now pass the floor to **Teammate 3** to present our verification framework and benchmark results."

```
[VERBAL HANDOVER: Teammate 2 nods to Teammate 3; Teammate 3 takes the floor]
```

---

```
========================================================================================
PART 3: VERIFICATION FRAMEWORK & BENCHMARK DEMONSTRATION
Speaker: TEAMMATE 3 (Slides 9 to 11 | Time: 7:15 – 11:00)
========================================================================================
```

### [SLIDE 9: Comprehensive Simulation Methodology & Testbench Architecture]
*(Visual: Slide 9 showing the layered testbench hierarchy and 78/78 test pass summary)*

**TEAMMATE 3:**  
"Thank you, Teammate 2. I am Teammate 3, and I will present our verification methodology and benchmark results.

Hardware design is only as credible as its verification suite. To ensure absolute correctness, we adopted a multi-tiered, automated self-checking verification strategy using Icarus Verilog and GTKWave.

Our test hierarchy consists of:
- **Unit Testbenches:** Dedicated test harnesses for the ALU (16 corner cases tested), the Control Unit (7 opcodes and fallbacks), the Register File (dual reads, reset, and Register `$zero` protection), and Data Memory (word boundary read/writes). All 33 unit assertions passed with 100% success.
- **Single-Cycle System Testbench (`tb_mips_cpu.v`):** 24 end-to-end assertions verifying complete ISA execution and memory interactions.
- **Pipelined System Testbench (`tb_pipelined_mips.v`):** 21 complex assertions validating pipeline flow, simultaneous EX and MEM hazard forwarding, 1-cycle Load-Use stalls, branch flushing, and full program execution.

Across the entire project, **78 individual hardware assertions were executed, and 78 passed with zero failures**. Every assertion is self-checking, comparing observed signal buses against gold architectural values on specific clock edges."

---

### [SLIDE 10: Benchmark Suite 1: Array Sum & Maximum Search]
*(Visual: Slide 10 showing the green verification cards for Array Sum = 100 and Max Search = 67)*

**TEAMMATE 3:**  
"To prove real-world capability, we assembled and executed five complete assembly programs on both processor cores.

**Benchmark 1 is the mandatory Array Sum application.**  
The processor is tasked with summing four 32-bit integers stored in Data Memory: 10, 20, 30, and 40. The assembly routine initializes memory pointers, traverses the array using `LW`, accumulates the sum in register `$t1`, tests termination via `BEQ`, and stores the final result into Data Memory address 16 using `SW`.  
- **Expected Result:** $10 + 20 + 30 + 40 = 100$ (`0x00000064`).  
- **Observed Result:** Data Memory location `Mem[16]` contains exactly `100`, and register `$t1` contains `100`. Both the single-cycle and pipelined cores executed this program with 100% precision.

**Benchmark 2 is the Maximum Search application.**  
The program scans an unsorted array of five elements: 12, 45, 23, 67, and 34. In each iteration, it loads the current element, executes the `SLT` instruction to perform a signed comparison against the running maximum, conditionally updates the maximum, and writes the result to memory address 20.  
- **Expected Result:** Maximum value = 67 (`0x00000043`).  
- **Observed Result:** `Mem[20]` contains exactly `67`, proving that signed comparison and forward-branching logic function flawlessly."

---

### [SLIDE 11: Advanced Benchmarks: Factorial, Fibonacci & Bubble Sort]
*(Visual: Slide 11 showing verification cards for Factorial = 120, Fibonacci = 21, and Bubble Sort)*

**TEAMMATE 3:**  
"To stress-test nested loops, tight register dependencies, and sorting algorithms, we developed three additional benchmarks for the Final Phase:

**Benchmark 3: Factorial Calculation.**  
Computes $5! = 5 \times 4 \times 3 \times 2 \times 1 = 120$. Because the core implements a pure RISC integer datapath without a hardware multiplier, multiplication is performed via repeated addition using nested loops and negative immediate decrements (`ADDI $t2, $t2, -1`).  
- **Observed Result:** Memory location `Mem[0]` contains `120` (`0x00000078`).

**Benchmark 4: Fibonacci Sequence Generation.**  
Iteratively generates the first eight numbers of the Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, and 21. Each value is computed by adding the two previous terms and written to successive memory words.  
- **Observed Result:** Memory location `Mem[32]` contains `21` (`0x00000015`), and register `$t3` holds `21`.

**Benchmark 5: In-Place Bubble Sort.**  
We initialized memory with five unsorted integers: `[45, 12, 89, 34, 23]`. The program implements a classic double-nested loop, loading adjacent elements, comparing them with `SLT`, and swapping them in memory using `SW` when out of order.  
- **Observed Result:** Memory locations `Mem[0]` through `Mem[16]` contain the sorted sequence: `[12, 23, 34, 45, 89]` in perfect ascending order.

All five benchmarks verified successfully under active pipelined execution. I will now hand over to **Teammate 4** to present our performance analysis, FPGA synthesis estimates, and project conclusion."

```
[VERBAL HANDOVER: Teammate 3 nods to Teammate 4; Teammate 4 takes the floor]
```

---

```
========================================================================================
PART 4: PERFORMANCE EVALUATION, HARDWARE SYNTHESIS & CONCLUSION
Speaker: TEAMMATE 4 (Slides 12 to 14 | Time: 11:00 – 14:30)
========================================================================================
```

### [SLIDE 12: Timing Analysis & Performance Comparison]
*(Visual: Slide 12 showing the CPI, Clock Frequency, and Throughput Speedup comparison)*

**TEAMMATE 4:**  
"Thank you, Teammate 3. I am Teammate 4, and I will present our performance evaluation, hardware resource synthesis, and project conclusion.

Slide 12 quantifies the architectural speedup gained by transitioning from our single-cycle baseline to the 5-stage pipelined design. According to the fundamental processor performance equation:
$$\text{CPU Execution Time} = \text{Instruction Count} \times \text{CPI} \times T_{clk}$$

In the **Single-Cycle core**, CPI is strictly 1.0. However, the clock period $T_{clk}$ is approximately 18.1 nanoseconds, yielding an operating frequency of roughly 55 MHz.

In the **5-Stage Pipelined core**, the critical path is segmented into five balanced stages. The longest single stage delay—the Execute stage comprising the forwarding mux, ALU, and latch setup—is approximately 5.4 nanoseconds. This enables an estimated operating frequency of **185 MHz**—more than a 3.3x increase in clock speed.

While data hazards introduce occasional stalls—specifically 1 cycle for Load-Use dependencies and 2 cycles for taken branches—our forwarding unit resolves over 85% of potential hazards without stalling. Across our benchmark workloads, the effective CPI of the pipelined core is approximately **1.18**.

Combining the higher clock rate with this effective CPI:
$$\text{Speedup} = \frac{\text{Time}_{\text{Single-Cycle}}}{\text{Time}_{\text{Pipelined}}} = \frac{\text{CPI}_{\text{Single}} \times T_{\text{clk, Single}}}{\text{CPI}_{\text{Pipe}} \times T_{\text{clk, Pipe}}} = \frac{1.0 \times 18.1\,\text{ns}}{1.18 \times 5.4\,\text{ns}} \approx \mathbf{2.85\times}$$

Our 5-stage pipelined processor achieves an overall **2.85-fold throughput improvement** over the baseline."

---

### [SLIDE 13: FPGA Synthesis & Hardware Resource Estimation]
*(Visual: Slide 13 showing the Xilinx Artix-7 resource utilization table)*

**TEAMMATE 4:**  
"To assess physical realizability, we synthesized both designs targeting a popular university FPGA platform: the **Xilinx Artix-7 (XC7A35T)**.

Our RTL code strictly adheres to the synthesizable Verilog-2001 standard. All combinational blocks have fully specified defaults to prevent inferred latches, and all sequential elements use positive-edge clocking.

The resource utilization metrics are highly favorable:
- **Look-Up Tables (LUTs):** The single-cycle core requires approximately 1,420 LUTs. The pipelined core requires roughly 2,150 LUTs—an increase of only about 730 LUTs to implement the Forwarding Unit, Hazard Detection Unit, and pipeline multiplexers. This represents less than 11% of the total FPGA capacity.
- **Flip-Flops:** The single-cycle core utilizes approximately 1,056 flip-flops (dominated by the 32x32 register file). The pipelined core utilizes approximately 1,380 flip-flops, accounting for the four pipeline registers. This represents under 4% of available slice registers.
- **Block RAM:** The Harvard memory subsystem utilizes one Block RAM tile, consuming under 2% of on-chip memory.
- **Power Consumption:** Estimated total on-chip power is under 0.22 Watts at 100 MHz.

These metrics prove that the architecture is exceptionally lightweight and ready for immediate physical bitstream deployment on Basys-3 or Nexys A7 development boards."

---

### [SLIDE 14: Team Contributions & Final Conclusion]
*(Visual: Slide 14 showing Team Work Allocation Breakdown and Final Summary Cards)*

**TEAMMATE 4:**  
"On Slide 14, we present our team work breakdown. Every member of our five-person group owned critical modules:
- **Member 1:** Program Counter, Instruction ROM, Top wrappers, and Pipelined Core integration.
- **Member 2:** 32-bit ALU, ALU Control Decoder, Register File with `$zero` protection, and Forwarding multiplexers.
- **Member 3:** Main Control Unit, Sign Extender, and Hazard Detection Unit.
- **Member 4:** Data RAM, Automated Testbenches, Assembly Benchmarks, and Waveform validation.
- **Member 5:** IEEE Technical Documentation, Slide Presentation Deck, High-Resolution Architecture Diagrams, and demonstration coordination.

In summary, this project has successfully fulfilled 100% of the requirements for the Final Phase academic evaluation:
1. We designed, integrated, and verified both a Single-Cycle MIPS baseline and a high-performance 5-Stage Pipelined core in synthesizable Verilog.
2. We designed and proved dedicated hardware units for Data Forwarding and Load-Use Hazard Detection.
3. We established an automated, self-checking verification suite with 78 passed assertions and zero failures.
4. We validated five real-world assembly benchmarks: Array Sum, Maximum Search, Factorial, Fibonacci, and Bubble Sort.
5. We delivered complete IEEE documentation, architecture diagrams, and hardware resource analysis.

Thank you very much for your time and attention. We now welcome any questions from the examination panel."

```
[END OF SPOKEN PRESENTATION — TOTAL TIME: ~14 MINUTES]
```

---

## Panel Defense & Viva Q&A Guide (Anticipated Examination Questions)

This section prepares the four teammates to defend technical questions from professors and evaluators:

### Q1 (Directed to Teammate 1): "Why did you choose a Harvard architecture instead of Von Neumann?"
**Model Answer (Teammate 1):**  
"In a single-cycle or pipelined processor, an instruction fetch occurs on every single clock cycle. If we used a unified Von Neumann memory with a single read/write port, a structural hazard would occur whenever an instruction in the MEM stage needed to load or store data, forcing the processor to stall the Fetch stage. The Harvard architecture provides two completely separate memory interfaces—one for instructions and one for data—enabling simultaneous fetch and memory access in the same clock cycle without structural conflicts."

### Q2 (Directed to Teammate 2): "How does your Forwarding Unit distinguish between an EX hazard and a MEM hazard when both write to the same register?"
**Model Answer (Teammate 2):**  
"This is the classic double-RAW hazard condition. For example, if instruction 1 writes to `$s0`, instruction 2 also writes to `$s0`, and instruction 3 reads `$s0`, instruction 3 must receive the *most recent* value produced by instruction 2. In our Verilog implementation inside `forwarding_unit.v`, we prioritize the EX hazard check ahead of the MEM hazard check. The MEM forwarding condition is evaluated in an `else if` branch that only activates if the EX hazard condition is false. This guarantees that the newer ALU result from EX/MEM always overrides older values from MEM/WB."

### Q3 (Directed to Teammate 2): "Why can't forwarding resolve a Load-Use hazard without a stall cycle?"
**Model Answer (Teammate 2):**  
"A Load Word instruction does not obtain its read data from Data Memory until the very end of its Memory Access (MEM) stage. The following instruction requires its operands at the beginning of its Execute (EX) stage. In time, the data simply has not been retrieved from memory yet. Therefore, forwarding backwards in time is physically impossible. Our Hazard Detection Unit detects this dependency in Decode and inserts exactly one bubble cycle into the pipeline, allowing the loaded data to reach the MEM/WB boundary, where it can then be forwarded directly into the ALU."

### Q4 (Directed to Teammate 3): "How did you verify that Register `$zero` cannot be overwritten?"
**Model Answer (Teammate 3):**  
"In `register_file.v`, Register `$0` is permanently tied to ground (`32'h00000000`), and writes where `write_reg == 5'd0` are explicitly ignored. In test `tb_mips_cpu.v` (Test 18), we executed `ADDI $0, $0, 111`—an explicit attempt to write non-zero data to register `$0`. In the subsequent cycle, an assertion checked that Register `$0` remained strictly zero. Furthermore, in our ALU and datapath, all operations referencing `$zero` consistently observe 0."

### Q5 (Directed to Teammate 4): "Why is your estimated speedup 2.85x instead of the theoretical 5x for a 5-stage pipeline?"
**Model Answer (Teammate 4):**  
"The theoretical speedup of an $N$-stage pipeline equals $N$ only under ideal conditions: perfectly balanced stage delays, infinite instruction streams, and zero hazards. In practice:
1. Stage delays are not perfectly equal; the Execute and Memory stages take longer than Write-Back, bounding $T_{clk}$ to the slowest stage (~5.4 ns) plus pipeline register overhead.
2. Stalls from Load-Use hazards and flushes from taken branches increase our CPI from 1.0 to approximately 1.18.
When you evaluate $\frac{18.1\,\text{ns}}{1.18 \times 5.4\,\text{ns}}$, you obtain 2.85x. This is a realistic, academically rigorous result that matches commercial RISC pipeline implementations."
