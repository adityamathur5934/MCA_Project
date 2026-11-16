# Supported Instruction Set Architecture (ISA)

The processor implements 10 instructions spanning R-Type, I-Type, and J-Type formats of the standard MIPS32 ISA.

---

## 1. Instruction Encoding Formats

### R-Type (Register Format)
```
 31      26 25      21 20      16 15      11 10       6 5        0
+----------+----------+----------+----------+----------+----------+
|  opcode  |    rs    |    rt    |    rd    |  shamt   |  funct   |
|  6 bits  |  5 bits  |  5 bits  |  5 bits  |  5 bits  |  6 bits  |
+----------+----------+----------+----------+----------+----------+
```

### I-Type (Immediate Format)
```
 31      26 25      21 20      16 15                             0
+----------+----------+----------+--------------------------------+
|  opcode  |    rs    |    rt    |           immediate            |
|  6 bits  |  5 bits  |  5 bits  |            16 bits             |
+----------+----------+----------+--------------------------------+
```

### J-Type (Jump Format)
```
 31      26 25                                                   0
+----------+------------------------------------------------------+
|  opcode  |                    target address                    |
|  6 bits  |                       26 bits                        |
+----------+------------------------------------------------------+
```

---

## 2. Supported Instructions Summary Table

| Instruction | Type | Opcode | Funct | Syntax | Semantics |
|-------------|:----:|:------:|:-----:|--------|-----------|
| **ADD** | R | `000000` | `100000` | `add $rd, $rs, $rt` | $R[rd] \leftarrow R[rs] + R[rt]$ |
| **SUB** | R | `000000` | `100010` | `sub $rd, $rs, $rt` | $R[rd] \leftarrow R[rs] - R[rt]$ |
| **AND** | R | `000000` | `100100` | `and $rd, $rs, $rt` | $R[rd] \leftarrow R[rs] \ \& \ R[rt]$ |
| **OR** | R | `000000` | `100101` | `or $rd, $rs, $rt` | $R[rd] \leftarrow R[rs] \ \| \ R[rt]$ |
| **SLT** | R | `000000` | `101010` | `slt $rd, $rs, $rt` | $R[rd] \leftarrow (R[rs] <_{\text{signed}} R[rt]) \ ? \ 1 : 0$ |
| **ADDI** | I | `001000` | — | `addi $rt, $rs, imm` | $R[rt] \leftarrow R[rs] + \text{SignExt}(imm)$ |
| **LW** | I | `100011` | — | `lw $rt, offset($rs)` | $R[rt] \leftarrow \text{Mem}[R[rs] + \text{SignExt}(offset)]$ |
| **SW** | I | `101011` | — | `sw $rt, offset($rs)` | $\text{Mem}[R[rs] + \text{SignExt}(offset)] \leftarrow R[rt]$ |
| **BEQ** | I | `000100` | — | `beq $rs, $rt, label` | $\text{if } R[rs] == R[rt] \implies \text{PC} \leftarrow (\text{PC}+4) + (\text{SignExt}(imm) \ll 2)$ |
| **J** | J | `000010` | — | `j target` | $\text{PC} \leftarrow \{(\text{PC}+4)[31:28], target[25:0], 2'b00\}$ |

---

## 3. Control Signal Matrix

| Instruction | RegDst | ALUSrc | MemtoReg | RegWrite | MemRead | MemWrite | Branch | Jump | ALUOp | ALU Ctrl |
|-------------|:------:|:------:|:--------:|:--------:|:-------:|:--------:|:------:|:----:|:-----:|:--------:|
| **ADD** | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | `10` | `0010` (ADD) |
| **SUB** | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | `10` | `0110` (SUB) |
| **AND** | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | `10` | `0000` (AND) |
| **OR** | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | `10` | `0001` (OR) |
| **SLT** | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | `10` | `0111` (SLT) |
| **ADDI** | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | `00` | `0010` (ADD) |
| **LW** | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | `00` | `0010` (ADD) |
| **SW** | X | 1 | X | 0 | 0 | 1 | 0 | 0 | `00` | `0010` (ADD) |
| **BEQ** | X | 0 | X | 0 | 0 | 0 | 1 | 0 | `01` | `0110` (SUB) |
| **J** | X | X | X | 0 | 0 | 0 | 0 | 1 | `00` | `XXXX` |
