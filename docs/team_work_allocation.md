# Team Work Allocation & Responsibilities (5-Member Team)

## 1. Team Allocation Matrix

| Team Member | Primary Architectural Role | Core RTL Modules & Artefacts Owned | Suggested Git Branch |
|:---|:---|:---|:---|
| **Member 1** [Name Placeholder] | **CPU Architecture & Integration Lead** | `program_counter.v`, `instruction_memory.v`, `mips_cpu.v`, `top_module.v`, Branch/Jump multiplexers | `feature/cpu-datapath-integration` |
| **Member 2** [Name Placeholder] | **ALU & Register File Specialist** | `alu.v`, `alu_control.v`, `register_file.v`, `tb_alu.v`, `tb_register_file.v` | `feature/alu-regfile-unit` |
| **Member 3** [Name Placeholder] | **Control Unit & Instruction Decoding** | `control_unit.v`, `sign_extend.v`, `tb_control_unit.v`, ISA opcode mapping | `feature/control-decoding-unit` |
| **Member 4** [Name Placeholder] | **Memory Subsystem & Verification Lead** | `data_memory.v`, `tb_data_memory.v`, `tb_mips_cpu.v`, `programs/*.asm`, `programs/*.hex` | `feature/memory-verification-suite` |
| **Member 5** [Name Placeholder] | **Technical Documentation & Presentation Lead** | `report/project_report.tex`, `report/project_report.pdf`, `presentation/prototype_presentation.pptx`, `demo/video_script.md`, `README.md` | `feature/documentation-presentation` |

---

## 2. Detailed Technical Responsibilities

### Member 1: CPU Architecture & Integration Lead
- **RTL Ownership:**
  - `src/program_counter.v`: PC register with reset and PC update logic.
  - `src/instruction_memory.v`: Harvard instruction ROM with hex loading capability.
  - `src/mips_cpu.v`: Top CPU core connecting datapath, control, and execution logic.
  - `src/top_module.v`: Top-level wrapper integrating CPU, IMEM, and DMEM.
- **Dependencies:**
  - Consumes ALU from Member 2, Control Unit from Member 3, and Data Memory from Member 4.
- **Key Deliverables:** Top-level integration compiling cleanly in Icarus Verilog.

### Member 2: ALU & Register File Specialist
- **RTL Ownership:**
  - `src/alu.v`: 32-bit ALU supporting ADD, SUB, AND, OR, SLT, and Zero flag.
  - `src/alu_control.v`: 4-bit ALU control decoder from `alu_op` and `funct`.
  - `src/register_file.v`: 32x32-bit dual-read synchronous-write register file with `$zero` write protection.
- **Verification Ownership:**
  - `testbench/tb_alu.v`: Unit testbench covering 16 corner cases.
  - `testbench/tb_register_file.v`: Dual read, reset, and $0 protection testbench.

### Member 3: Control Unit & Instruction Decoding Specialist
- **RTL Ownership:**
  - `src/control_unit.v`: Combinational 6-bit opcode decoder.
  - `src/sign_extend.v`: 16-to-32 bit two's complement sign extender.
- **Verification Ownership:**
  - `testbench/tb_control_unit.v`: Verification of all 9 control lines across all 10 opcodes and default fallbacks.
  - Documentation of ISA control matrix.

### Member 4: Memory Subsystem & Verification Lead
- **RTL Ownership:**
  - `src/data_memory.v`: Word-aligned 256-word data RAM.
- **Verification & Assembly Ownership:**
  - `testbench/tb_data_memory.v`: Memory unit testbench.
  - `testbench/tb_mips_cpu.v`: System integration testbench for all 10 instructions.
  - Sample assembly programs: `array_sum.asm`, `maximum_search.asm`, `factorial.asm`.
  - Machine code generation and validation (`programs/assemble.py`).
  - Simulation waveform generation and logging (`simulation/waveforms/`, `simulation/results/`).

### Member 5: Technical Documentation & Presentation Lead
- **Deliverables Ownership:**
  - IEEE-format Conference Report (`report/project_report.tex` and compiled `report/project_report.pdf`).
  - Architecture Diagrams (`diagrams/*.png`).
  - Slide Presentation (`presentation/prototype_presentation.pptx`).
  - Video Recording Script (`demo/video_script.md`) and video link placeholder (`demo/video_link.txt`).
  - Repository documentation (`README.md`, `CONTRIBUTING.md`, `PROJECT_STATUS.md`, `PHASE1_COMPLETION_REPORT.md`).

---

## 3. Integration & Review Workflow
1. **Branching Strategy:** Each member develops on their designated feature branch branched from `main`.
2. **Unit Test Requirement:** No pull request is merged into `main` without 100% passing self-checking testbench logs.
3. **Integration Gate:** Member 1 and Member 4 review and sign off on all merged pull requests.
4. **Git Hygiene:** Clean commit history with clear semantic messages. Never push secrets or large temporary files.
