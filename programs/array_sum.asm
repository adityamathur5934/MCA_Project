# ============================================================================
# Program 1: Array Sum (Mandatory)
# Architecture: Single-Cycle MIPS (32-bit)
#
# Description:
#   Computes the arithmetic sum of a 4-element array stored in Data Memory:
#   Input Array: [10, 20, 30, 40]  (Hex: 0x0A, 0x14, 0x1E, 0x28)
#   Expected Sum: 100               (Hex: 0x64)
#   Result stored at Data Memory byte address 16 (0x00000010).
#
# Demonstrates:
#   LW, ADD, ADDI, BEQ, SW, J
#
# Register Allocation:
#   $t0 ($8):  Array base address (0x00000000)
#   $t1 ($9):  Accumulator / Sum
#   $t2 ($10): Loop index counter i (0 .. 4)
#   $t3 ($11): Array size limit N = 4
#   $t4 ($12): Current element value array[i]
#   $t5 ($13): Pointer to current element in Data Memory
# ============================================================================

.data
    # Memory layout:
    # 0x00: 10 (0x0000000A)
    # 0x04: 20 (0x00000014)
    # 0x08: 30 (0x0000001E)
    # 0x0C: 40 (0x00000028)
    # 0x10: Result Sum destination (100 = 0x00000064)

.text
main:
    # 1. Initialize pointers and accumulators
    addi $t0, $zero, 0       # $t0 = base address 0x00000000
    addi $t1, $zero, 0       # $t1 = sum = 0
    addi $t2, $zero, 0       # $t2 = loop index i = 0
    addi $t3, $zero, 4       # $t3 = loop limit N = 4
    add  $t5, $t0, $zero     # $t5 = current element pointer = $t0

loop:
    # 2. Loop termination check
    beq  $t2, $t3, end       # If i == 4, branch to end (PC = 0x30)

    # 3. Load element and accumulate
    lw   $t4, 0($t5)         # Load array[i] from memory into $t4
    add  $t1, $t1, $t4       # sum = sum + array[i]

    # 4. Advance pointer and loop counter
    addi $t5, $t5, 4         # Advance memory pointer by 4 bytes
    addi $t2, $t2, 1         # i = i + 1
    j    loop                # Repeat loop (Jump to 0x14)

    # Padding / Alignment NOP
    add  $zero, $zero, $zero

end:
    # 5. Store final sum into Data Memory
    sw   $t1, 16($t0)        # Mem[16] = sum (100)
halt:
    j    halt                # Infinite loop to halt execution
