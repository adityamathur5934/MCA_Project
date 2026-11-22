# Final Project Completion Report: Single-Cycle and 5-Stage Pipelined MIPS Processor with Memory Interface and Hazard Resolution

## Final Status: COMPLETE (100% Verified)

- **Project Title:** Single-Cycle & 5-Stage Pipelined MIPS Processor with Memory Interface and Hazard Resolution
- **Evaluation Status:** **FINAL PHASE COMPLETED (100% Full Project Evaluation)**
- **Verification Result:** **78/78 Assertions Passed (100% Pass Rate across 6 Testbenches)**
- **Benchmarks Validated:** 5 Benchmarks (Array Sum, Maximum Search, Factorial, Fibonacci Sequence, Bubble Sort)
- **Target FPGA Platform:** Xilinx Artix-7 (XC7A35T)
- **Date of Final Verification:** 2026-11-22

---

## 1. Executive Summary & Architectural Scope Evolution

This project successfully fulfills all academic requirements for the **Final Phase Evaluation**. Building upon the baseline Single-Cycle MIPS processor developed in Phase I, the project achieved full microarchitectural evolution to an advanced **5-Stage Pipelined RISC Processor** in synthesizable Verilog 2001.

| Architectural Parameter | Phase I Baseline (Single-Cycle) | Final Phase (5-Stage Pipelined Core) |
| :--- | :--- | :--- |
| **Pipeline Stages** | Monolithic (1 stage) | 5 stages: IF, ID, EX, MEM, WB |
| **CPI (Cycles Per Instruction)** | Fixed 1.0 | Ideal 1.0; Effective ~1.18 (with stalls) |
| **Critical Path Delay** | ~18.1 ns (dominated by LW path) | ~5.4 ns (Execute stage ALU + MUX) |
| **Max Clock Frequency (Artix-7)**| ~55 MHz | ~185 MHz (3.36x clock frequency scaling) |
| **Data Hazard Resolution** | Not applicable | Dedicated **Data Forwarding Unit** (EX & MEM paths) |
| **Load-Use Hazard Resolution**| Not applicable | Dedicated **Hazard Detection Unit** (1-cycle bubble stall) |
| **Control Hazard Resolution** | Combinational branch / jump | Branch resolution in EX stage with 2-cycle flush |
| **Throughput Speedup** | Baseline (1.0x) | **~2.85x faster execution** over baseline |
| **Hardware Resource (LUTs)** | ~1,420 LUTs (< 7% Artix-7) | ~2,150 LUTs (< 11% Artix-7) |
| **Hardware Resource (FFs)** | ~1,056 FFs (< 3% Artix-7) | ~1,380 FFs (< 4% Artix-7) |
| **Memory Architecture** | Harvard Architecture (1024B ROM, 1024B RAM) | Harvard Architecture (Concurrent IF & MEM access) |

---

## 2. Inventory of RTL Modules & Deliverables

### 2.1 Baseline RTL Modules (`src/`)
1. `src/program_counter.v`: 32-bit Program Counter with synchronous/asynchronous active-high reset.
2. `src/instruction_memory.v`: 256-word Harvard ROM with word alignment and hex loading.
3. `src/control_unit.v`: Combinational 6-bit opcode decoder producing 9 primary control signals.
4. `src/register_file.v`: 32x32-bit register file with dual read ports and `$zero` write protection.
5. `src/sign_extend.v`: 16-to-32 bit sign extender for two's complement immediates.
6. `src/alu.v`: 32-bit multi-function ALU (ADD, SUB, AND, OR, SLT, NOR, shifts).
7. `src/alu_control.v`: 4-bit ALU control decoder from `alu_op` and instruction `funct`.
8. `src/data_memory.v`: 256-word Harvard RAM with word alignment and edge-triggered writes.
9. `src/mips_cpu.v`: Top-level CPU core connecting datapath and control for single-cycle execution.
10. `src/top_module.v`: Top-level integration wrapper encapsulating CPU, IMEM, and DMEM.

### 2.2 Pipelined RTL Modules (`src/pipelined/`)
1. `src/pipelined/pipe_if_id.v`: IF/ID pipeline register with stall and flush controls.
2. `src/pipelined/pipe_id_ex.v`: ID/EX pipeline register buffering control lines, operands, and immediates.
3. `src/pipelined/pipe_ex_mem.v`: EX/MEM pipeline register buffering ALU results and memory write data.
4. `src/pipelined/pipe_mem_wb.v`: MEM/WB pipeline register buffering memory data and ALU writeback values.
5. `src/pipelined/forwarding_unit.v`: Data Forwarding / Bypassing Unit resolving RAW hazards without stalls.
6. `src/pipelined/hazard_detection_unit.v`: Hazard Detection Unit handling Load-Use stalls and branch flushes.
7. `src/pipelined/pipelined_mips_cpu.v`: Complete 5-stage pipelined MIPS core.
8. `src/pipelined/top_pipelined_module.v`: Top-level integration wrapper for the pipelined system.

---

## 3. Comprehensive Verification & Benchmark Audit

Across the multi-tiered self-checking verification framework, **78 assertions were executed and 78 passed with 0 failures (100% pass rate)**:

| Testbench | Focus | Assertions Executed | Assertions Passed | Status |
| :--- | :--- | :--- | :--- | :--- |
| `testbench/tb_alu.v` | 32-bit ALU operations & Zero flag | 16 | 16 | **PASS (100%)** |
| `testbench/tb_control_unit.v` | Opcode decoding & safe defaults | 7 | 7 | **PASS (100%)** |
| `testbench/tb_register_file.v` | Dual read, clocked write, $0 clamp | 5 | 5 | **PASS (100%)** |
| `testbench/tb_data_memory.v` | RAM word boundary reads & writes | 5 | 5 | **PASS (100%)** |
| `testbench/tb_mips_cpu.v` | Single-cycle ISA & memory integration | 24 | 24 | **PASS (100%)** |
| `testbench/tb_pipelined_mips.v`| Pipelined hazards, stalls, benchmarks | 21 | 21 | **PASS (100%)** |
| **TOTAL** | **Full System Regression Suite** | **78** | **78** | **100% PASS** |

### Benchmark Execution Audit:
1. **Array Sum:** Sums [10, 20, 30, 40] -> `Mem[16] = 100` (`0x00000064`) [VERIFIED]
2. **Maximum Search:** Scans [12, 45, 23, 67, 34] -> `Mem[20] = 67` (`0x00000043`) [VERIFIED]
3. **Factorial:** Computes 5! = 120 -> `Mem[0] = 120` (`0x00000078`) [VERIFIED]
4. **Fibonacci Sequence:** Computes F(0..8) -> `Mem[32] = 21` (`0x00000015`) [VERIFIED]
5. **Bubble Sort:** Sorts [45, 12, 89, 34, 23] -> `Mem[0..16] = [12, 23, 34, 45, 89]` [VERIFIED]

---

## 4. Final Submission Artefacts

| Artefact | Location | Description |
| :--- | :--- | :--- |
| **Final IEEE Report (PDF)** | `report/final_project_report.pdf` | Comprehensive 2-column IEEE Conference technical report. |
| **Final Presentation Slides** | `presentation/final_presentation.pptx`| Professional 14-slide widescreen (16:9) engineering slide deck. |
| **4-Teammate Spoken Script** | `presentation/FINAL_PRESENTATION_SCRIPT.md` | Word-for-word spoken dialogue and Q&A defense for 4 speakers. |
| **Printable Script (PDF)** | `presentation/Final_Presentation_Script_4_Teammates.pdf` | Formatted printable speaking script with timing and cues. |
| **Pipelined Architecture Diagram**| `diagrams/pipelined_architecture.png` | High-resolution diagram showing 5 stages, forwarding & hazards. |
| **Single-Cycle Diagram** | `diagrams/datapath_architecture.png` | Architecture diagram for baseline single-cycle datapath. |
| **Pipelined Waveforms** | `simulation/waveforms/tb_pipelined_mips.vcd` | Full cycle-accurate VCD trace for pipelined processor. |
| **Single-Cycle Waveforms** | `simulation/waveforms/tb_mips_cpu.vcd` | Full cycle-accurate VCD trace for baseline processor. |
| **GTKWave Setup** | `simulation/waveforms/mips_demo.gtkw` | Pre-configured GTKWave signal layout. |
