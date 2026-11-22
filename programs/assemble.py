#!/usr/bin/env python3
"""
MIPS Assembler and Instruction Encoder for MIPS Processor (Final Phase).
Encodes assembly programs to machine code hex files for all benchmark suites:
1. Array Sum (10, 20, 30, 40 -> 100)
2. Maximum Search (12, 45, 23, 67, 34 -> 67)
3. Factorial (5! = 120)
4. Bubble Sort ([45, 12, 89, 34, 23] -> [12, 23, 34, 45, 89])
5. Fibonacci Sequence (F(0..8) -> F(8) = 21)
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
array_sum_instructions = [
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$zero'), 0),
    encode_i('ADDI', parse_reg('$t1'), parse_reg('$zero'), 0),
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$zero'), 0),
    encode_i('ADDI', parse_reg('$t3'), parse_reg('$zero'), 4),
    encode_r('ADD', parse_reg('$t5'), parse_reg('$t0'), parse_reg('$zero')),
    encode_i('BEQ', parse_reg('$t3'), parse_reg('$t2'), 6),
    encode_i('LW', parse_reg('$t4'), parse_reg('$t5'), 0),
    encode_r('ADD', parse_reg('$t1'), parse_reg('$t1'), parse_reg('$t4')),
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t5'), 4),
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$t2'), 1),
    encode_j(0x14),
    encode_r('ADD', 0, 0, 0),
    encode_i('SW', parse_reg('$t1'), parse_reg('$t0'), 16),
    encode_j(0x34),
]

# -----------------------------------------------------------------------------
# Program 2: Maximum Search
# -----------------------------------------------------------------------------
maximum_search_instructions = [
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$zero'), 0),
    encode_i('LW', parse_reg('$t1'), parse_reg('$t0'), 0),
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$zero'), 1),
    encode_i('ADDI', parse_reg('$t3'), parse_reg('$zero'), 5),
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t0'), 4),
    encode_i('BEQ', parse_reg('$t3'), parse_reg('$t2'), 8),
    encode_i('LW', parse_reg('$t4'), parse_reg('$t5'), 0),
    encode_r('SLT', parse_reg('$t6'), parse_reg('$t1'), parse_reg('$t4')),
    encode_i('BEQ', parse_reg('$zero'), parse_reg('$t6'), 1),
    encode_r('ADD', parse_reg('$t1'), parse_reg('$t4'), parse_reg('$zero')),
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t5'), 4),
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$t2'), 1),
    encode_j(0x14),
    encode_r('ADD', 0, 0, 0),
    encode_i('SW', parse_reg('$t1'), parse_reg('$t0'), 20),
    encode_j(0x3C),
]

# -----------------------------------------------------------------------------
# Program 3: Factorial (5! = 120)
# -----------------------------------------------------------------------------
factorial_instructions = [
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$zero'), 5),
    encode_i('ADDI', parse_reg('$t1'), parse_reg('$zero'), 1),
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$t0'), 0),
    encode_i('ADDI', parse_reg('$t3'), parse_reg('$zero'), 1),
    encode_i('BEQ', parse_reg('$t3'), parse_reg('$t2'), 9),
    encode_i('ADDI', parse_reg('$t4'), parse_reg('$zero'), 0),
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$zero'), 0),
    encode_i('BEQ', parse_reg('$t2'), parse_reg('$t5'), 3),
    encode_r('ADD', parse_reg('$t4'), parse_reg('$t4'), parse_reg('$t1')),
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t5'), 1),
    encode_j(0x1C),
    encode_r('ADD', parse_reg('$t1'), parse_reg('$t4'), parse_reg('$zero')),
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$t2'), -1),
    encode_j(0x10),
    encode_i('ADDI', parse_reg('$t6'), parse_reg('$zero'), 0),
    encode_i('SW', parse_reg('$t1'), parse_reg('$t6'), 0),
    encode_j(0x40),
]

# -----------------------------------------------------------------------------
# Program 4: Bubble Sort Benchmark
# -----------------------------------------------------------------------------
# Sorts 5 numbers: [45, 12, 89, 34, 23] -> [12, 23, 34, 45, 89]
bubble_sort_instructions = [
    # PC = 0x00: addi $t0, $zero, 0   (base = 0)
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$zero'), 0),
    # PC = 0x04: addi $t1, $zero, 0   (i = 0)
    encode_i('ADDI', parse_reg('$t1'), parse_reg('$zero'), 0),
    # PC = 0x08: addi $t2, $zero, 5   (n = 5)
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$zero'), 5),
    # PC = 0x0C: addi $t4, $zero, 4   (inner_limit = 4)
    encode_i('ADDI', parse_reg('$t4'), parse_reg('$zero'), 4),
    # outer_loop: (PC = 0x10)
    # PC = 0x10: beq $t1, $t2, end (PC = 0x4C) -> offset = (0x4C - 0x14)/4 = 14
    encode_i('BEQ', parse_reg('$t2'), parse_reg('$t1'), 14),
    # PC = 0x14: addi $t3, $zero, 0   (j = 0)
    encode_i('ADDI', parse_reg('$t3'), parse_reg('$zero'), 0),
    # PC = 0x18: addi $t5, $t0, 0     (ptr = base)
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t0'), 0),
    # inner_loop: (PC = 0x1C)
    # PC = 0x1C: beq $t3, $t4, inner_end (PC = 0x44) -> offset = (0x44 - 0x20)/4 = 9
    encode_i('BEQ', parse_reg('$t4'), parse_reg('$t3'), 9),
    # PC = 0x20: lw $t6, 0($t5)       (A = array[j])
    encode_i('LW', parse_reg('$t6'), parse_reg('$t5'), 0),
    # PC = 0x24: lw $t7, 4($t5)       (B = array[j+1])
    encode_i('LW', parse_reg('$t7'), parse_reg('$t5'), 4),
    # PC = 0x28: slt $s0, $t7, $t6    (s0 = B < A)
    encode_r('SLT', parse_reg('$s0'), parse_reg('$t7'), parse_reg('$t6')),
    # PC = 0x2C: beq $s0, $zero, no_swap (PC = 0x38) -> offset = (0x38 - 0x30)/4 = 2
    encode_i('BEQ', parse_reg('$zero'), parse_reg('$s0'), 2),
    # PC = 0x30: sw $t7, 0($t5)       (array[j] = B)
    encode_i('SW', parse_reg('$t7'), parse_reg('$t5'), 0),
    # PC = 0x34: sw $t6, 4($t5)       (array[j+1] = A)
    encode_i('SW', parse_reg('$t6'), parse_reg('$t5'), 4),
    # no_swap: (PC = 0x38)
    # PC = 0x38: addi $t5, $t5, 4     (ptr += 4)
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$t5'), 4),
    # PC = 0x3C: addi $t3, $t3, 1     (j++)
    encode_i('ADDI', parse_reg('$t3'), parse_reg('$t3'), 1),
    # PC = 0x40: j inner_loop (PC = 0x1C)
    encode_j(0x1C),
    # inner_end: (PC = 0x44)
    # PC = 0x44: addi $t1, $t1, 1     (i++)
    encode_i('ADDI', parse_reg('$t1'), parse_reg('$t1'), 1),
    # PC = 0x48: j outer_loop (PC = 0x10)
    encode_j(0x10),
    # end: (PC = 0x4C)
    # PC = 0x4C: j 0x4C (halt)
    encode_j(0x4C),
]

# -----------------------------------------------------------------------------
# Program 5: Fibonacci Sequence Generator (F0..F8)
# -----------------------------------------------------------------------------
fibonacci_instructions = [
    # PC = 0x00: addi $t0, $zero, 0   (base = 0)
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$zero'), 0),
    # PC = 0x04: addi $t1, $zero, 0   (F0 = 0)
    encode_i('ADDI', parse_reg('$t1'), parse_reg('$zero'), 0),
    # PC = 0x08: addi $t2, $zero, 1   (F1 = 1)
    encode_i('ADDI', parse_reg('$t2'), parse_reg('$zero'), 1),
    # PC = 0x0C: sw $t1, 0($t0)       (Mem[0] = 0)
    encode_i('SW', parse_reg('$t1'), parse_reg('$t0'), 0),
    # PC = 0x10: sw $t2, 4($t0)       (Mem[4] = 1)
    encode_i('SW', parse_reg('$t2'), parse_reg('$t0'), 4),
    # PC = 0x14: addi $t0, $t0, 8     (ptr = 8)
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$t0'), 8),
    # PC = 0x18: addi $t4, $zero, 2   (i = 2)
    encode_i('ADDI', parse_reg('$t4'), parse_reg('$zero'), 2),
    # PC = 0x1C: addi $t5, $zero, 8   (N = 8)
    encode_i('ADDI', parse_reg('$t5'), parse_reg('$zero'), 8),
    # fib_loop: (PC = 0x20)
    # PC = 0x20: beq $t4, $t5, fib_done (PC = 0x40) -> offset = (0x40 - 0x24)/4 = 7
    encode_i('BEQ', parse_reg('$t5'), parse_reg('$t4'), 7),
    # PC = 0x24: add $t3, $t1, $t2   (Fn = F(n-1) + F(n-2))
    encode_r('ADD', parse_reg('$t3'), parse_reg('$t1'), parse_reg('$t2')),
    # PC = 0x28: sw $t3, 0($t0)       (Mem[ptr] = Fn)
    encode_i('SW', parse_reg('$t3'), parse_reg('$t0'), 0),
    # PC = 0x2C: add $t1, $t2, $zero (F(n-2) = F(n-1))
    encode_r('ADD', parse_reg('$t1'), parse_reg('$t2'), parse_reg('$zero')),
    # PC = 0x30: add $t2, $t3, $zero (F(n-1) = Fn)
    encode_r('ADD', parse_reg('$t2'), parse_reg('$t3'), parse_reg('$zero')),
    # PC = 0x34: addi $t0, $t0, 4     (ptr += 4)
    encode_i('ADDI', parse_reg('$t0'), parse_reg('$t0'), 4),
    # PC = 0x38: addi $t4, $t4, 1     (i++)
    encode_i('ADDI', parse_reg('$t4'), parse_reg('$t4'), 1),
    # PC = 0x3C: j fib_loop (PC = 0x20)
    encode_j(0x20),
    # fib_done: (PC = 0x40)
    # PC = 0x40: add $t3, $t1, $t2   (F8 = F6 + F7 = 8 + 13 = 21)
    encode_r('ADD', parse_reg('$t3'), parse_reg('$t1'), parse_reg('$t2')),
    # PC = 0x44: sw $t3, 0($t0)       (Mem[28] = 21 = 0x15)
    encode_i('SW', parse_reg('$t3'), parse_reg('$t0'), 0),
    # PC = 0x48: j 0x48 (halt)
    encode_j(0x48),
]

def write_hex(filename, instructions):
    with open(filename, 'w') as f:
        for inst in instructions:
            f.write(f"{inst:08x}\n")

write_hex("programs/array_sum.hex", array_sum_instructions)
write_hex("programs/maximum_search.hex", maximum_search_instructions)
write_hex("programs/factorial.hex", factorial_instructions)
write_hex("programs/bubble_sort.hex", bubble_sort_instructions)
write_hex("programs/fibonacci.hex", fibonacci_instructions)
print("All 5 Hex files successfully generated for Final Phase.")
