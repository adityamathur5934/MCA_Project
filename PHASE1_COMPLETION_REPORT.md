# Phase I Completion Report: Single-Cycle MIPS Processor with Memory Interface

## Final Status: COMPLETE (100% Verified)

- **Project Title:** Single-Cycle MIPS Processor with Memory Interface
- **Course / Phase:** Phase I Evaluation (30% Weighting)
- **Evaluation Status:** **COMPLETE** (All 10 instructions, Harvard memory interface, 3 benchmark programs, IEEE report, presentation, video script, diagrams, and repository deliverables 100% finished and verified).
- **Date of Verification:** 2026-11-16

---

## 1. What Was Implemented

### 1.1 Microarchitecture and Core Datapath
- **Word Width:** 32-bit datapath width throughout.
- **Register File:** 32 general-purpose 32-bit registers ($0 - $31) with two combinational read ports and one synchronous positive-edge write port. Register `$zero` (`$0`) is permanently hardwired to `32'h00000000` and protected against writes.
- **Program Counter:** 32-bit byte-addressed register with active-high synchronous/asynchronous reset to `32'h00000000`.
- **Memory Interface (Harvard Architecture):**
  - **Instruction Memory (ROM):** 256 words (1024 bytes) combinational memory supporting preloading via `.hex` machine-code files.
  - **Data Memory (RAM):** 256 words (1024 bytes) word-aligned memory with combinational read and synchronous edge-triggered write.
- **Arithmetic Logic Unit (ALU):** 32-bit execution unit supporting ADD, SUB, AND, OR, and SLT (signed comparison via `$signed()`), plus an equality Zero flag output.
- **Control Unit & ALU Control:** Combinational decoders converting 6-bit opcodes and 6-bit funct fields into 9 control lines (`RegDst`, `ALUSrc`, `MemtoReg`, `RegWrite`, `MemRead`, `MemWrite`, `Branch`, `Jump`, `ALUOp[1:0]`).
- **Branch and Jump Logic:** Combinational calculation of sequential PC+4, branch target $(PC+4) + (\text{SignExtImm} \ll 2)$, and jump target $\{PC+4[31:28], \text{Target}[25:0], 2'b00\}$.

### 1.2 Instruction Set Implemented (10 Instructions)
- **R-Type:** `ADD`, `SUB`, `AND`, `OR`, `SLT`
- **I-Type:** `ADDI`, `LW`, `SW`, `BEQ`
- **J-Type:** `J`

---

## 2. Inventory of Generated Files

### 2.1 Verilog RTL Modules (`src/`)
1. `src/program_counter.v` — 32-bit Program Counter register.
2. `src/instruction_memory.v` — 256-word instruction memory ROM.
3. `src/control_unit.v` — Main Control Unit 6-bit opcode decoder.
4. `src/register_file.v` — 32x32-bit general purpose register file.
5. `src/sign_extend.v` — 16-to-32 bit sign-extension module.
6. `src/alu.v` — 32-bit multi-function Arithmetic Logic Unit.
7. `src/alu_control.v` — 4-bit ALU operation control decoder.
8. `src/data_memory.v` — 256-word word-aligned data RAM.
9. `src/mips_cpu.v` — Core processor datapath and control integration.
10. `src/top_module.v` — Top-level system wrapper integrating CPU, IMEM, and DMEM.

### 2.2 Self-Checking Testbenches (`testbench/`)
1. `testbench/tb_alu.v` — Unit testbench for 32-bit ALU.
2. `testbench/tb_control_unit.v` — Unit testbench for Main Control Unit.
3. `testbench/tb_register_file.v` — Unit testbench for 32x32-bit Register File.
4. `testbench/tb_data_memory.v` — Unit testbench for Data Memory.
5. `testbench/tb_mips_cpu.v` — Full CPU integration and benchmark execution testbench.

### 2.3 Sample Programs (`programs/`)
1. `programs/assemble.py` — Python assembler script for ISA encoding and validation.
2. `programs/array_sum.asm` — Assembly source for 4-element summation.
3. `programs/array_sum.hex` — Verified machine code for Array Sum.
4. `programs/maximum_search.asm` — Assembly source for 5-element maximum search.
5. `programs/maximum_search.hex` — Verified machine code for Maximum Search.
6. `programs/factorial.asm` — Assembly source for iterative 5! calculation.
7. `programs/factorial.hex` — Verified machine code for Factorial.

### 2.4 Simulation Outputs & Waveforms (`simulation/`)
1. `simulation/results/alu_test.log` — Log for ALU unit test (16/16 PASS).
2. `simulation/results/control_unit_test.log` — Log for Control Unit unit test (7/7 PASS).
3. `simulation/results/register_file_test.log` — Log for Register File unit test (5/5 PASS).
4. `simulation/results/data_memory_test.log` — Log for Data Memory unit test (5/5 PASS).
5. `simulation/results/mips_cpu_test.log` — Log for CPU integration test (24/24 PASS).
6. `simulation/waveforms/tb_alu.vcd` — Waveform trace for ALU.
7. `simulation/waveforms/tb_control_unit.vcd` — Waveform trace for Control Unit.
8. `simulation/waveforms/tb_register_file.vcd` — Waveform trace for Register File.
9. `simulation/waveforms/tb_data_memory.vcd` — Waveform trace for Data Memory.
10. `simulation/waveforms/tb_mips_cpu.vcd` — Full system 225-cycle waveform trace.
11. `simulation/simulation_summary.md` — Formal verification report.

### 2.5 Architecture Diagrams (`diagrams/`)
1. `diagrams/generate_diagrams.py` — Python script generating vector-quality diagrams.
2. `diagrams/datapath_architecture.png` — Complete single-cycle MIPS datapath.
3. `diagrams/control_unit_flow.png` — Main Control Unit signal flow.
4. `diagrams/alu_architecture.png` — 32-bit ALU architecture.
5. `diagrams/register_file_architecture.png` — Register File architecture.
6. `diagrams/instruction_flow.png` — 5-stage conceptual execution in single cycle.
7. `diagrams/memory_interface.png` — CPU core and Harvard memory interface.

### 2.6 Academic Deliverables (`report/`, `presentation/`, `demo/`, `docs/`)
1. `report/project_report.tex` — Complete IEEE conference paper source.
2. `report/project_report.pdf` — Compiled IEEE two-column conference paper PDF.
3. `report/generate_pdf_report.py` — PDF compilation script.
4. `presentation/prototype_presentation.pptx` — 9-slide demonstration presentation.
5. `presentation/generate_presentation.py` — Presentation generation script.
6. `demo/video_script.md` — 4m:30s scene-by-scene 5-member video narration script.
7. `demo/video_link.txt` — Video submission placeholder & recording checklist.
8. `docs/architecture.md` — Comprehensive microarchitectural specification.
9. `docs/instruction_set.md` — Full ISA reference & control signal truth table.
10. `docs/module_documentation.md` — Verilog module port specifications.
11. `docs/testing_strategy.md` — Verification strategy & assertion guide.
12. `docs/team_work_allocation.md` — 5-member role and git branch allocation.
13. `README.md` — Master repository README.
14. `CONTRIBUTING.md` — Team Git branching and contribution guidelines.
15. `LICENSE` — MIT License.
16. `.gitignore` — Ignore patterns for simulation binaries.
17. `PROJECT_STATUS.md` — Milestone tracking document.

---

## 3. Verification Evidence & Test Statistics

### 3.1 Pass/Fail Metrics
| Test Scope | Assertions Executed | Assertions Passed | Assertions Failed | Success Rate |
|:---|:---:|:---:|:---:|:---:|
| `tb_alu.v` | 16 | 16 | 0 | 100.0% |
| `tb_control_unit.v` | 7 | 7 | 0 | 100.0% |
| `tb_register_file.v` | 5 | 5 | 0 | 100.0% |
| `tb_data_memory.v` | 5 | 5 | 0 | 100.0% |
| `tb_mips_cpu.v` (ISA + Programs) | 24 | 24 | 0 | 100.0% |
| **Overall Total** | **57** | **57** | **0** | **100.0%** |

### 3.2 Benchmark Program Execution
1. **Array Sum (Mandatory):**
   - Input Array: `[10, 20, 30, 40]`
   - Observed Output: `Mem[16] == 100` (`0x00000064`), `Reg $t1 == 100` -> **PASS**
2. **Maximum Search:**
   - Input Array: `[12, 45, 23, 67, 34]`
   - Observed Output: `Mem[20] == 67` (`0x00000043`), `Reg $t1 == 67` -> **PASS**
3. **Factorial (5!):**
   - Input: `5`
   - Observed Output: `Mem[0] == 120` (`0x00000078`), `Reg $t1 == 120` -> **PASS**

---

## 4. Deliverables Completed vs. Requiring Manual Action

### Completed (100% Ready):
- [x] All 10 Verilog RTL modules.
- [x] All 5 self-checking testbenches.
- [x] All 3 benchmark programs (assembly + hex).
- [x] Simulation logs and VCD waveforms.
- [x] 6 High-resolution architectural diagrams.
- [x] IEEE Project Report PDF (`report/project_report.pdf`).
- [x] IEEE Project Report LaTeX source (`report/project_report.tex`).
- [x] 9-Slide Presentation (`presentation/prototype_presentation.pptx`).
- [x] 5-Member Video Script (`demo/video_script.md`).
- [x] Complete `README.md`, `CONTRIBUTING.md`, `LICENSE`, `.gitignore`.
- [x] Team work allocation and documentation in `docs/`.

### Requiring Manual Action by Team:
1. **Video Recording:** Team members must record the actual 4m:30s prototype demonstration video following the dialogue and visual cues in `demo/video_script.md`.
2. **Video Upload:** Upload recorded video to YouTube or university portal, and paste the final URL into `demo/video_link.txt` and `README.md`.
3. **GitHub Push:** When authorized, initialize git remote and push the repository branches using individual GitHub student accounts according to `CONTRIBUTING.md`.

---

## 5. Exact Commands to Reproduce Verification

Run these commands directly in the repository root:

```bash
# 1. Execute all 4 unit testbenches
iverilog -g2001 -o simulation/tb_alu src/alu.v testbench/tb_alu.v && vvp simulation/tb_alu
iverilog -g2001 -o simulation/tb_control_unit src/control_unit.v testbench/tb_control_unit.v && vvp simulation/tb_control_unit
iverilog -g2001 -o simulation/tb_register_file src/register_file.v testbench/tb_register_file.v && vvp simulation/tb_register_file
iverilog -g2001 -o simulation/tb_data_memory src/data_memory.v testbench/tb_data_memory.v && vvp simulation/tb_data_memory

# 2. Execute full CPU integration and benchmark programs
iverilog -g2001 -o simulation/tb_mips_cpu src/*.v testbench/tb_mips_cpu.v && vvp simulation/tb_mips_cpu

# 3. Inspect waveforms in GTKWave
gtkwave simulation/waveforms/tb_mips_cpu.vcd
```
