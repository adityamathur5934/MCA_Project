# Single-Cycle MIPS Processor with Memory Interface
## Prototype Demonstration Video Script & Recording Plan

- **Target Duration:** 4 minutes 30 seconds (Hard maximum: 5 minutes)
- **Target Audience:** Academic Evaluation Panel / University Engineering Faculty
- **Team Size:** 5 Members (All 5 members have active speaking roles and introductions)
- **Resolution:** 1080p (1920x1080) at 60 fps
- **Tooling Used:** VS Code / Text Editor, Terminal (Icarus Verilog), GTKWave

---

## Scene-by-Scene Production Plan

| Scene # | Time Window | Duration | Topic | Speaker | Visual Display / On-Screen Content |
|:---:|:---:|:---:|:---|:---|:---|
| **Scene 1** | 0:00 – 0:35 | 35 sec | Title, Team Introductions & Project Overview | **Member 1** (Lead) | Slide 1 (Title & Team Members), webcam/team intro |
| **Scene 2** | 0:35 – 1:15 | 40 sec | Problem Statement, Objectives & Specifications | **Member 2** | Slide 2 (Objectives) & Slide 3 (Datapath Architecture) |
| **Scene 3** | 1:15 – 1:55 | 40 sec | Verilog RTL Implementation & Module Hierarchy | **Member 3** | VS Code: `src/` directory, highlighting `top_module.v`, `mips_cpu.v`, `control_unit.v` |
| **Scene 4** | 1:55 – 2:40 | 45 sec | Control Unit Decoding & ALU Operations | **Member 2** | Slide 5 (Control Matrix) & `src/control_unit.v`, `src/alu.v` |
| **Scene 5** | 2:40 – 3:35 | 55 sec | Live Simulation Demo & Benchmark Execution | **Member 4** | Terminal: Running `vvp simulation/tb_mips_cpu`, highlighting Array Sum = 100 |
| **Scene 6** | 3:35 – 4:10 | 35 sec | GTKWave Waveform Analysis & Signal Timing | **Member 4** & **Member 5** | GTKWave: Inspecting `pc`, `instruction`, `alu_result`, `mem_write`, `zero` |
| **Scene 7** | 4:10 – 4:35 | 25 sec | Phase I Summary, Deliverables & Phase II Roadmap | **Member 5** | Slide 9 (Conclusion & Roadmap), Final team sign-off |

---

## Detailed Script & Dialogue

### Scene 1: Introduction & Project Overview (0:00 – 0:35)
**Visual:** Display **Slide 1** (`presentation/prototype_presentation.pptx`). Camera on speakers or team panel.

> **Member 1 (Spoken):**
> "Good morning, respected professors and evaluation committee. Welcome to our Phase I prototype demonstration of the **Single-Cycle 32-Bit MIPS Processor with Memory Interface**.
> 
> My name is **[Member 1 Name]**, serving as the CPU Architecture and Integration Lead. Joining me today are my colleagues:
> - **[Member 2 Name]**, our ALU and Register File Specialist;
> - **[Member 3 Name]**, our Control Unit and Instruction Decoding Specialist;
> - **[Member 4 Name]**, our Memory and Verification Lead;
> - and **[Member 5 Name]**, our Technical Documentation and Reporting Lead.
> 
> Today, we will walk you through our complete hardware design, from synthesizable Verilog RTL to automated simulation benchmarks and GTKWave waveform analysis."

---

### Scene 2: Problem Statement & System Architecture (0:35 – 1:15)
**Visual:** Transition to **Slide 2** and **Slide 3** (Datapath Diagram `diagrams/datapath_architecture.png`).

> **Member 2 (Spoken):**
> "The primary objective of this project is to implement a robust, fully synthesizable 32-bit single-cycle processor adhering to the MIPS32 architecture with a separate Harvard memory interface.
> 
> Every instruction in our processor executes from start to finish within a single clock cycle—achieving a theoretical Cycles Per Instruction (CPI) of exactly one.
> 
> Our processor datapath features 32 general-purpose registers where register `$zero` is permanently hardwired to zero, a 32-bit byte-addressed Program Counter with synchronous reset, a combinational 256-word Instruction Memory, and a word-aligned 256-word Data Memory.
> 
> The processor supports ten core MIPS instructions: five R-Type instructions—ADD, SUB, AND, OR, SLT; four I-Type instructions—ADDI, LW, SW, BEQ; and the J-Type unconditional Jump instruction."

---

### Scene 3: Verilog RTL Architecture & Code Walkthrough (1:15 – 1:55)
**Visual:** Switch screen capture to **VS Code**, showing the file explorer under `src/` and opening `src/top_module.v` and `src/mips_cpu.v`.

> **Member 3 (Spoken):**
> "Moving to our hardware implementation, our RTL codebase is structured into ten modular, synthesizable Verilog modules in `src/`.
> 
> Here in `top_module.v`, we see a clean structural integration connecting our `mips_cpu` core directly with `instruction_memory` and `data_memory`. 
> 
> Inside `mips_cpu.v`, the datapath cleanly decouples the combinational instruction decode from the execution and memory stages. Notice how our PC increment logic computes PC plus 4, while the branch target adder computes PC plus 4 plus sign-extended immediate shifted left by two. 
> 
> The jump target is formed by concatenating the top 4 bits of PC plus 4 with the 26-bit target field shifted left by two. Multiplexers select the appropriate next PC without creating any combinational latches."

---

### Scene 4: Control Unit & ALU Implementation (1:55 – 2:40)
**Visual:** Display `src/control_unit.v` and `diagrams/control_unit_flow.png`, then switch to `src/alu.v`.

> **Member 2 (Spoken):**
> "Our Main Control Unit in `control_unit.v` decodes the 6-bit instruction opcode to drive nine essential control lines: `RegDst`, `ALUSrc`, `MemtoReg`, `RegWrite`, `MemRead`, `MemWrite`, `Branch`, `Jump`, and a 2-bit `ALUOp`.
> 
> In `alu_control.v`, we decode the 2-bit `ALUOp` alongside the 6-bit `funct` field for R-type instructions to generate a 4-bit ALU control code.
> 
> In `alu.v`, our 32-bit ALU performs addition, subtraction, bitwise AND, bitwise OR, and signed comparison with `slt` using Verilog signed arithmetic. Crucially, it generates a high-speed `zero` flag that directly gates the branch multiplexer for the `BEQ` instruction."

---

### Scene 5: Live Simulation & Benchmark Execution (2:40 – 3:35)
**Visual:** Switch to **Terminal**. Run compile and simulation commands on screen.

```bash
iverilog -g2001 -o simulation/tb_mips_cpu src/*.v testbench/tb_mips_cpu.v
vvp simulation/tb_mips_cpu
```

> **Member 4 (Spoken):**
> "Now, let us demonstrate the live simulation using Icarus Verilog.
> 
> We run our comprehensive system testbench, `tb_mips_cpu.v`.
> 
> As you can see in the terminal output:
> - In Part 1, all ten individual instructions are sequentially verified: ADD, SUB, AND, OR, SLT, ADDI with positive and negative immediates, SW, LW, BEQ taken and not taken, J, and the register `$zero` write protection. Every single check returns PASS.
> 
> - Next, in Part 2, we execute our mandatory **Array Sum benchmark**. An array of four integers—10, 20, 30, and 40—is loaded into Data Memory. Our MIPS program executes an iterative loop using `LW`, `ADD`, `ADDI`, and `BEQ`, and stores the final accumulated sum back to memory address 16 using `SW`.
> 
> Notice the output: Memory at address 16 equals **100**, and register `$t1` equals **100**—verifying a 100% correct loop execution!
> 
> - Furthermore, Part 3 executes our **Maximum Search** program on 5 elements, correctly finding **67**; and Part 4 executes our **Factorial** program computing 5 factorial, producing **120** in memory!
> 
> Across all tests, we have 24 out of 24 system assertions passing with zero errors."

---

### Scene 6: Waveform Analysis in GTKWave (3:35 – 4:10)
**Visual:** Launch GTKWave displaying `simulation/waveforms/tb_mips_cpu.vcd`. Zoom in on signals `clk`, `pc[31:0]`, `instruction[31:0]`, `alu_result[31:0]`, `zero`, `mem_write`, `reg_write_data[31:0]`.

> **Member 4 (Spoken):**
> "Let us inspect the physical timing in GTKWave.
> 
> Here, we observe the clock running at 100 MHz. On each positive clock edge, the Program Counter increments from `0x00` to `0x04`, `0x08`, and so on.
> 
> Notice cycle 12: when two equal values are compared during `BEQ`, the ALU zero flag asserts high. In the very next clock edge, the PC jumps directly to target address `0x3C`, cleanly skipping the unexecuted instructions.
> 
> The write-back data bus and memory write enable signals show sharp, glitch-free transitions, validating that our single-cycle datapath achieves full timing closure within the clock period."

---

### Scene 7: Conclusion & Phase II Roadmap (4:10 – 4:35)
**Visual:** Display **Slide 9** (`presentation/prototype_presentation.pptx`).

> **Member 5 (Spoken):**
> "In conclusion, our team has satisfied all Phase I requirements:
> - A fully operational, synthesizable 32-bit single-cycle MIPS processor in Verilog RTL;
> - Harvard instruction and data memory interfaces;
> - Full verification of 10 instructions and three benchmark programs with 100% test pass rate;
> - And complete IEEE documentation, architecture diagrams, and GitHub repository preparation.
> 
> For Phase II, our roadmap includes migrating to a 5-stage pipelined architecture with hazard detection and forwarding, implementing L1 caches, and deploying onto an FPGA board.
> 
> Thank you for your time, and we welcome any questions from the panel."

---

## Technical Setup Instructions for Recording

1. **Terminal Setup:**
   - Window size: 120 x 30 characters.
   - Font: JetBrains Mono or Menlo, size 16pt.
   - Command ready to execute:
     ```bash
     iverilog -g2001 -o simulation/tb_mips_cpu src/*.v testbench/tb_mips_cpu.v && vvp simulation/tb_mips_cpu
     ```

2. **GTKWave Setup:**
   - Open: `gtkwave simulation/waveforms/tb_mips_cpu.vcd`
   - Insert Signals:
     - `tb_mips_cpu/clk`
     - `tb_mips_cpu/rst`
     - `tb_mips_cpu/pc[31:0]`
     - `tb_mips_cpu/instruction[31:0]`
     - `tb_mips_cpu/alu_result[31:0]`
     - `tb_mips_cpu/zero`
     - `tb_mips_cpu/branch`
     - `tb_mips_cpu/jump`
     - `tb_mips_cpu/mem_write`
     - `tb_mips_cpu/reg_write_data[31:0]`

3. **Presentation Setup:**
   - Open `presentation/prototype_presentation.pptx` in Full Screen Slide Show mode.
