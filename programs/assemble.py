#!/usr/bin/env python3
"""
MIPS Assembler and Instruction Encoder for Single-Cycle MIPS.
Encodes assembly programs to machine code hex files for the 10 supported instructions.
"""
import sys

# Supported ISA Opcodes & Funct codes
OPCODES = {
    'R':    0x00, # 6'b000000
    'ADDI': 0x08, # 6'b001000
    'LW':   0x23, # 6'b100011
    'SW':   0x2B, # 6'b101011
    'BEQ':  0x04, # 6'b000100
    'J':    0x02, # 6'b000010
}

FUNCT = {
    'ADD': 0x20, # 6'b100000
    'SUB': 0x22, # 6'b100010
    'AND': 0x24, # 6'b100100
    'OR':  0x25, # 6'b100101
    'SLT': 0x2A, # 6'b101010
}

REGISTERS = {
    '$zero': 0, '$0': 0,
    '$at': 1,   '$1': 1,
    '$v0': 2,   '$v1': 3,
    '$a0': 4,   '$a1': 5,   '$a2': 6,   '$a3': 7,
    '$t0': 8,   '$t1': 9,   '$t2': 10,  '$t3': 11,
    '$t4': 12,  '$t5': 13,  '$t6': 14,  '$t7': 15,
    '$s0': 16,  '$s1': 17,  '$s2': 18,  '$s3': 19,
    '$s4': 20,  '$s5': 21,  '$s6': 22,  '$s7': 23,
    '$t8': 24,  '$t9': 25,
    '$k0': 26,  '$k1': 27,
    '$gp': 28,  '$sp': 29,  '$fp': 30,  '$ra': 31
}

def parse_reg(r):
    r = r.strip().rstrip(',')
    if r in REGISTERS:
        return REGISTERS[r]
    if r.startswith('$'):
        return int(r[1:])
    raise ValueError(f"Unknown register: {r}")

def encode_r(funct_name, rd, rs, rt, shamt=0):
    opcode = OPCODES['R']
    funct = FUNCT[funct_name]
    inst = (opcode << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct
    return inst

def encode_i(op_name, rt, rs, imm):
    opcode = OPCODES[op_name]
    imm = imm & 0xFFFF # 16-bit mask
    inst = (opcode << 26) | (rs << 21) | (rt << 16) | imm
    return inst

def encode_j(target_byte_addr):
    opcode = OPCODES['J']
    target_field = (target_byte_addr >> 2) & 0x03FFFFFF
    inst = (opcode << 26) | target_field
    return inst

# -----------------------------------------------------------------------------
# Program 1: Array Sum
# -----------------------------------------------------------------------------
# Computes 10 + 20 + 30 + 40 = 100
# Mem[0..3] holds the array; Mem[4] (addr 16) holds sum.
array_sum_instructions = [
    # PC = 0x00: addi $t0, $zero, 0     (base addr = 0)
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$zero'), 0),
    # PC = 0x04: addi $t1, $zero, 0     (sum = 0)
    encode_i('ADDI', parse_reg('$t1'), parse_reg('$zero'), 0),
    # PC = 0x08: addi $t2, $zero, 0     (i = 0)
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$zero'), 0),
    # PC = 0x0C: addi $t3, $zero, 4     (limit = 4)
    encode_i('ADDI', parse_reg('$t3'), parse_reg('$zero'), 4),
    # PC = 0x10: add  $t5, $t0, $zero   (current pointer = $t0)
    encode_r('ADD', parse_reg('$t5'), parse_reg('$t0'), parse_reg('$zero')),
    # Loop:
    # PC = 0x14: beq  $t2, $t3, end (PC=0x30) -> offset = (0x30 - 0x18)/4 = 6
    encode_i('BEQ', parse_reg('$t3'), parse_reg('$t2'), 6),
    # PC = 0x18: lw   $t4, 0($t5)       (load array[i])
    encode_i('LW', parse_reg('$t4'), parse_reg('$t5'), 0),
    # PC = 0x1C: add  $t1, $t1, $t4     (sum += array[i])
    encode_r('ADD', parse_reg('$t1'), parse_reg('$t1'), parse_reg('$t4')),
    # PC = 0x20: addi $t5, $t5, 4       (ptr += 4)
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t5'), 4),
    # PC = 0x24: addi $t2, $t2, 1       (i += 1)
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$t2'), 1),
    # PC = 0x28: j    loop (PC=0x14)
    encode_j(0x14),
    # PC = 0x2C: add $zero, $zero, $zero (NOP)
    encode_r('ADD', 0, 0, 0),
    # End:
    # PC = 0x30: sw   $t1, 16($t0)      (store sum at address 16)
    encode_i('SW', parse_reg('$t1'), parse_reg('$t0'), 16),
    # PC = 0x34: j    0x34              (halt / loop forever)
    encode_j(0x34),
]

# -----------------------------------------------------------------------------
# Program 2: Maximum Search
# -----------------------------------------------------------------------------
# Array: 12, 45, 23, 67, 34 -> Max = 67
# Mem[0..4] holds array; Mem[5] (addr 20) holds max.
maximum_search_instructions = [
    # PC = 0x00: addi $t0, $zero, 0     (base = 0)
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$zero'), 0),
    # PC = 0x04: lw   $t1, 0($t0)       (max = array[0])
    encode_i('LW', parse_reg('$t1'), parse_reg('$t0'), 0),
    # PC = 0x08: addi $t2, $zero, 1     (i = 1)
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$zero'), 1),
    # PC = 0x0C: addi $t3, $zero, 5     (limit = 5)
    encode_i('ADDI', parse_reg('$t3'), parse_reg('$zero'), 5),
    # PC = 0x10: addi $t5, $t0, 4       (ptr = 4)
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t0'), 4),
    # Loop:
    # PC = 0x14: beq  $t2, $t3, end (PC=0x38) -> offset = (0x38 - 0x18)/4 = 8
    encode_i('BEQ', parse_reg('$t3'), parse_reg('$t2'), 8),
    # PC = 0x18: lw   $t4, 0($t5)       (load array[i])
    encode_i('LW', parse_reg('$t4'), parse_reg('$t5'), 0),
    # PC = 0x1C: slt  $t6, $t1, $t4     ($t6 = max < array[i])
    encode_r('SLT', parse_reg('$t6'), parse_reg('$t1'), parse_reg('$t4')),
    # PC = 0x20: beq  $t6, $zero, skip (PC=0x28) -> offset = (0x28 - 0x24)/4 = 1
    encode_i('BEQ', parse_reg('$zero'), parse_reg('$t6'), 1),
    # PC = 0x24: add  $t1, $t4, $zero   (max = array[i])
    encode_r('ADD', parse_reg('$t1'), parse_reg('$t4'), parse_reg('$zero')),
    # Skip:
    # PC = 0x28: addi $t5, $t5, 4       (ptr += 4)
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t5'), 4),
    # PC = 0x2C: addi $t2, $t2, 1       (i += 1)
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$t2'), 1),
    # PC = 0x30: j    loop (PC=0x14)
    encode_j(0x14),
    # PC = 0x34: add $zero, $zero, $zero
    encode_r('ADD', 0, 0, 0),
    # End:
    # PC = 0x38: sw   $t1, 20($t0)      (store max at address 20)
    encode_i('SW', parse_reg('$t1'), parse_reg('$t0'), 20),
    # PC = 0x3C: j    0x3C              (halt)
    encode_j(0x3C),
]

# -----------------------------------------------------------------------------
# Program 3: Factorial
# -----------------------------------------------------------------------------
# Computes 5! = 120.
# Registers:
#   $t0: N = 5
#   $t1: result = 1
#   $t2: current multiplier n = N
#   $t3: one = 1
#   $t4: temp accumulator for product
#   $t5: inner loop counter j
#   $t6: base address pointer = 0
factorial_instructions = [
    # PC = 0x00: addi $t0, $zero, 5     (N = 5)
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$zero'), 5),
    # PC = 0x04: addi $t1, $zero, 1     (result = 1)
    encode_i('ADDI', parse_reg('$t1'), parse_reg('$zero'), 1),
    # PC = 0x08: addi $t2, $t0, 0       (n = N = 5)
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$t0'), 0),
    # PC = 0x0C: addi $t3, $zero, 1     (const 1)
    encode_i('ADDI', parse_reg('$t3'), parse_reg('$zero'), 1),
    # Outer Loop: (PC = 0x10)
    # PC = 0x10: beq  $t2, $t3, end (PC=0x38) -> offset = (0x38 - 0x14)/4 = 9
    encode_i('BEQ', parse_reg('$t3'), parse_reg('$t2'), 9),
    # PC = 0x14: addi $t4, $zero, 0     (product = 0)
    encode_i('ADDI', parse_reg('$t4'), parse_reg('$zero'), 0),
    # PC = 0x18: addi $t5, $zero, 0     (j = 0)
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$zero'), 0),
    # Inner Loop: (PC = 0x1C)
    # PC = 0x1C: beq  $t5, $t2, inner_end (PC=0x2C) -> offset = (0x2C - 0x20)/4 = 3
    encode_i('BEQ', parse_reg('$t2'), parse_reg('$t5'), 3),
    # PC = 0x20: add  $t4, $t4, $t1     (product += result)
    encode_r('ADD', parse_reg('$t4'), parse_reg('$t4'), parse_reg('$t1')),
    # PC = 0x24: addi $t5, $t5, 1       (j += 1)
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t5'), 1),
    # PC = 0x28: j    inner_loop (PC=0x1C)
    encode_j(0x1C),
    # Inner End: (PC = 0x2C)
    # PC = 0x2C: add  $t1, $t4, $zero   (result = product)
    encode_r('ADD', parse_reg('$t1'), parse_reg('$t4'), parse_reg('$zero')),
    # PC = 0x30: addi $t2, $t2, -1      (n = n - 1)
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$t2'), -1),
    # PC = 0x34: j    outer_loop (PC=0x10)
    encode_j(0x10),
    # End: (PC = 0x38)
    # PC = 0x38: addi $t6, $zero, 0     (base = 0)
    encode_i('ADDI', parse_reg('$t6'), parse_reg('$zero'), 0),
    # PC = 0x3C: sw   $t1, 0($t6)       (store 120 at Mem[0])
    encode_i('SW', parse_reg('$t1'), parse_reg('$t6'), 0),
    # PC = 0x40: j    0x40              (halt)
    encode_j(0x40),
]

def write_hex(filename, instructions):
    with open(filename, 'w') as f:
        for inst in instructions:
            f.write(f"{inst:08x}\n")

write_hex("programs/array_sum.hex", array_sum_instructions)
write_hex("programs/maximum_search.hex", maximum_search_instructions)
write_hex("programs/factorial.hex", factorial_instructions)
print("Hex files successfully generated.")
