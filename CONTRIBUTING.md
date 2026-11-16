# Contribution Guidelines (5-Member Team)

Welcome to the **Single-Cycle MIPS Processor with Memory Interface** project repository. This guide defines the Git branching model, coding conventions, verification rules, and pull-request procedures for all five team members.

---

## 1. Team Allocation and Branching Model

Each team member is assigned a dedicated Git feature branch corresponding to their architectural domain:

| Member | Domain | Feature Branch | Assigned Ownership |
|:---|:---|:---|:---|
| **Member 1** | CPU Architecture & Integration | `feature/cpu-datapath-integration` | `src/program_counter.v`, `src/instruction_memory.v`, `src/mips_cpu.v`, `src/top_module.v` |
| **Member 2** | ALU & Register File | `feature/alu-regfile-unit` | `src/alu.v`, `src/alu_control.v`, `src/register_file.v`, `testbench/tb_alu.v`, `testbench/tb_register_file.v` |
| **Member 3** | Control & Decoding | `feature/control-decoding-unit` | `src/control_unit.v`, `src/sign_extend.v`, `testbench/tb_control_unit.v` |
| **Member 4** | Memory & Verification | `feature/memory-verification-suite` | `src/data_memory.v`, `testbench/tb_data_memory.v`, `testbench/tb_mips_cpu.v`, `programs/*` |
| **Member 5** | Documentation & Presentation | `feature/documentation-presentation` | `report/*`, `presentation/*`, `demo/*`, `diagrams/*`, `docs/*` |

---

## 2. Git Workflow & Semantic Commits

### Step-by-Step Branch & Commit Instructions:

1. **Clone & Switch to Branch:**
   ```bash
   git checkout -b feature/<your-assigned-branch>
   ```

2. **Commit with Clear Semantic Messages:**
   Use the conventional commit format:
   - `feat: <description>` for new modules or tests
   - `fix: <description>` for bug fixes or timing corrections
   - `docs: <description>` for documentation or report updates
   - `test: <description>` for testbenches and simulations

   Example:
   ```bash
   git add src/alu.v testbench/tb_alu.v
   git commit -m "feat(alu): implement signed SLT comparison and Zero flag generation"
   ```

3. **Mandatory Pre-Commit Verification:**
   Before staging any changes to RTL or testbenches, run the test suite to verify 0 failures:
   ```bash
   iverilog -g2001 -o simulation/tb_mips_cpu src/*.v testbench/tb_mips_cpu.v && vvp simulation/tb_mips_cpu
   ```

4. **Pull Request & Peer Review:**
   - Push your branch to the remote repository.
   - Open a Pull Request targeting `main`.
   - Each PR requires at least **one peer review approval** (Member 1 or Member 4) before merging.
   - No direct pushes to `main`.

---

## 3. Verilog RTL Coding Standards
- **Standard:** Synthesizable Verilog 2001 (`-g2001`).
- **Timing:** Always declare `` `timescale 1ns / 1ps `` at the top of each file.
- **Naming Conventions:**
  - Modules and ports: lower snake_case (`program_counter`, `alu_ctrl`, `read_data1`).
  - Constants and parameters: upper snake_case (`ALU_ADD`, `MEM_DEPTH`).
- **Latches:** Ensure all combinational `always @(*)` blocks assign all outputs across every branch to prevent unintentional latches.
- **Reset:** Synchronous or asynchronous active-high reset (`rst`).

---

## 4. Verification & Testing Requirements
- Every new feature must be accompanied by an automated self-checking testbench.
- Testbenches must produce explicit `[PASS]` or `[FAIL]` console messages and exit with code 0 on success.
- Value Change Dump (`$dumpfile`, `$dumpvars`) must be maintained in `simulation/waveforms/`.
