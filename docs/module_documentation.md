# Verilog RTL Module Documentation

This document describes each Verilog module in `src/`, detailing its interface ports, internal architecture, and design rationale.

---

## 1. `program_counter.v`
- **Purpose:** Tracks the byte address of the instruction being executed.
- **Port Interface:**
  - `input wire clk`: System clock.
  - `input wire rst`: Synchronous/Asynchronous active-high reset.
  - `input wire [31:0] next_pc`: Computed next PC value from branch/jump multiplexers.
  - `output reg [31:0] pc`: Current program counter address.
- **Implementation Note:** On reset, `pc` is driven to `32'h00000000`. On each active clock edge, `pc` latches `next_pc`.

---

## 2. `instruction_memory.v`
- **Purpose:** Read-only storage for program machine instructions.
- **Parameters:**
  - `MEM_DEPTH`: Number of words (default: 256 words = 1024 bytes).
  - `MEM_FILE`: Optional `.hex` filename to load at initialization.
- **Port Interface:**
  - `input wire [31:0] addr`: Byte address from Program Counter.
  - `output wire [31:0] instruction`: 32-bit fetched machine instruction.
- **Implementation Note:** Address is word-aligned using `addr[$clog2(MEM_DEPTH)+1 : 2]`. Reads are purely combinational to support single-cycle fetch and execute.

---

## 3. `control_unit.v`
- **Purpose:** Decodes instruction opcode `inst[31:26]` into control signals for datapath multiplexers, register file, and memories.
- **Port Interface:**
  - `input wire [5:0] opcode`: 6-bit instruction opcode.
  - `output reg reg_dst, alu_src, mem_to_reg, reg_write, mem_read, mem_write, branch, jump`: Single-bit control lines.
  - `output reg [1:0] alu_op`: 2-bit ALU operation selector.
- **Implementation Note:** Synthesized as pure combinational logic with safe zero-defaults for unassigned opcodes to prevent latch inference.

---

## 4. `register_file.v`
- **Purpose:** General-Purpose Register File (32 registers, 32-bit width).
- **Port Interface:**
  - `input wire clk, rst, reg_write`
  - `input wire [4:0] read_reg1, read_reg2, write_reg`
  - `input wire [31:0] write_data`
  - `output wire [31:0] read_data1, read_data2`
- **Implementation Note:** Reads from address `5'd0` continuously return `32'h00000000`. Writes to register 0 are ignored in hardware (`if (reg_write && write_reg != 5'd0)`).

---

## 5. `sign_extend.v`
- **Purpose:** Replicates the sign bit (bit 15) across the upper 16 bits of a 16-bit immediate value.
- **Port Interface:**
  - `input wire [15:0] in`: 16-bit signed immediate from instruction.
  - `output wire [31:0] out`: 32-bit sign-extended immediate.
- **Implementation Note:** Implemented with Verilog replication operator: `{{16{in[15]}}, in}`.

---

## 6. `alu.v`
- **Purpose:** Performs 32-bit arithmetic and bitwise logic operations.
- **Port Interface:**
  - `input wire [31:0] a, b`
  - `input wire [3:0] alu_ctrl`
  - `output reg [31:0] result`
  - `output wire zero`
- **Supported Operations:**
  - `4'b0000`: Bitwise AND
  - `4'b0001`: Bitwise OR
  - `4'b0010`: ADD (Signed / Unsigned two's complement addition)
  - `4'b0110`: SUB (Subtraction)
  - `4'b0111`: SLT (Set Less Than, signed comparison using `$signed()`)
- **Zero Flag:** Asserted when `result === 32'h00000000`.

---

## 7. `alu_control.v`
- **Purpose:** Decodes the 2-bit `alu_op` from the Main Control Unit and the 6-bit `funct` field `inst[5:0]`.
- **Port Interface:**
  - `input wire [1:0] alu_op`
  - `input wire [5:0] funct`
  - `output reg [3:0] alu_ctrl`

---

## 8. `data_memory.v`
- **Purpose:** Word-aligned data memory for `LW` and `SW` instructions.
- **Parameters:**
  - `MEM_DEPTH`: Number of words (default: 256 words).
- **Port Interface:**
  - `input wire clk, rst, mem_read, mem_write`
  - `input wire [31:0] addr, write_data`
  - `output wire [31:0] read_data`
- **Implementation Note:** Writes take effect on `posedge clk`. Reads are combinational, presenting data when `mem_read` is asserted and isolating to 0 when deasserted.

---

## 9. `mips_cpu.v`
- **Purpose:** Core datapath module integrating Program Counter, Register File, ALU, Control Units, and Branch/Jump Multiplexers.
- **Port Interface:**
  - Clock and reset.
  - Instruction memory bus: `inst_addr`, `instruction`.
  - Data memory bus: `mem_addr`, `mem_write_data`, `mem_read_data`, `mem_read`, `mem_write`.
  - Comprehensive debug lines for testbench probing.

---

## 10. `top_module.v`
- **Purpose:** Top-level integration module instantiating `mips_cpu`, `instruction_memory`, and `data_memory`.
- **Port Interface:**
  - Provides system inputs (`clk`, `rst`) and brings all internal datapath signals to module boundary for GTKWave waveform visualization.
