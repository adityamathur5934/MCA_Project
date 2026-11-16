# Single-Cycle MIPS Processor Architecture

## 1. Architectural Overview
The Single-Cycle MIPS Processor is a 32-bit Reduced Instruction Set Computer (RISC) implementing a subset of the MIPS32 Release 1 Instruction Set Architecture. In this microarchitecture, each instruction is fetched, decoded, executed, accesses memory, and completes write-back within a single clock cycle ($CPI = 1$).

### Key Architectural Specifications:
- **Datapath Width:** 32 bits
- **Register File:** 32 general-purpose 32-bit registers ($R0 - $R31)
  - Hardware constraint: Register `$zero` (`$0`) is permanently tied to `32'h00000000`.
- **Program Counter (PC):** 32-bit byte-addressed register with synchronous/asynchronous reset to `32'h00000000`.
- **Instruction Memory (Harvard Architecture):** 256 words (1024 bytes) read-only memory with combinational output.
- **Data Memory:** 256 words (1024 bytes) read/write RAM with synchronous writes and combinational reads.
- **Arithmetic Logic Unit (ALU):** 32-bit multi-function arithmetic and logic core with zero detection.
- **Control Unit:** Combinational single-level opcode decoder generating control lines for execution and memory routing.

---

## 2. Block Diagram and Signal Flow
The datapath separates the memory subsystems into Harvard architecture instruction and data memories to avoid resource conflicts during single-cycle operation:

```
+---------------+     PC[31:0]      +--------------------+
|Program Counter| ----------------> | Instruction Memory |
+---------------+                   +--------------------+
       |                                      |
     (PC+4)                         Instruction[31:0]
       |                            /      |      \
       |               [31:26]     /    [25:21]   [20:16]
       |                  v       /        v         v
       |         +--------------+   +-------------------+
       |         | Control Unit |   |   Register File   |
       |         +--------------+   +-------------------+
       |                 |                |         |
       v                 v           ReadData1  ReadData2
+--------------+   [Control Lines]        |         |
| Branch/Jump  |         |                v         v
| Address Mux  | <-------+------------> +---------------+
+--------------+                        |  32-bit ALU   |
       |                                +---------------+
       |                                  |           |
       |                              ALUResult    ZeroFlag
       |                                  |           |
       |                                  v           v
       |                        +-------------+   [Branch]
       |                        | Data Memory |       |
       |                        +-------------+       v
       |                               |         (PC Branch)
       |                            ReadData
       |                               |
       |        Write-Back Mux         v
       +----------------------------> [MemtoReg] --> RegFile WriteData
```

---

## 3. Subsystem Descriptions

### 3.1 Program Counter and Next-PC Logic
The Program Counter (PC) stores the byte address of the active instruction. The next PC calculation supports three modes:
1. **Sequential Increment:**
   $$\text{PC}_{\text{seq}} = \text{PC} + 4$$
2. **Branch on Equal (BEQ):**
   $$\text{PC}_{\text{branch}} = (\text{PC} + 4) + (\text{SignExtImm} \ll 2)$$
   Taken if $\text{Branch} = 1$ and $\text{Zero} = 1$.
3. **Unconditional Jump (J):**
   $$\text{PC}_{\text{jump}} = \{(\text{PC} + 4)[31:28], \text{Target}[25:0], 2'b00\}$$

### 3.2 Register File
- **Ports:** Two combinational read ports (`read_reg1`, `read_reg2`) and one synchronous write port (`write_reg`, `write_data`, `reg_write`).
- **Timing:** Internal register values are updated on the rising clock edge when `reg_write` is asserted. Read operations are asynchronous/combinational, presenting valid register contents within the same clock period.

### 3.3 Arithmetic Logic Unit (ALU) & ALU Control
- Supports operations: ADD, SUB, AND, OR, SLT.
- The `alu_control` module decodes the 2-bit `alu_op` from the Main Control Unit and the 6-bit `funct` field:
  - `alu_op == 2'b00`: Forces ADD (LW, SW, ADDI address calculation)
  - `alu_op == 2'b01`: Forces SUB (BEQ equality check)
  - `alu_op == 2'b10`: R-type decoding via `funct`

### 3.4 Memory Subsystems
- Both instruction and data memories employ word-aligned indexing using `addr[31:2]` (mapped to 256 words: `addr[9:2]`).
- Instruction Memory is read combinationally.
- Data Memory provides combinational reads on `mem_read` and performs synchronous writes on `posedge clk` when `mem_write` is asserted.
