# ============================================================================
# Program 2: Maximum Search
# Architecture: Single-Cycle MIPS (32-bit)
#
# Description:
#   Finds the maximum integer in a 5-element array stored in Data Memory:
#   Input Array: [12, 45, 23, 67, 34]
#   Expected Maximum: 67 (Hex: 0x43)
#   Result stored at Data Memory byte address 20 (0x00000014).
#
# Demonstrates:
#   LW, SLT, ADDI, BEQ, SW, J, ADD
#
# Register Allocation:
#   $t0 ($8):  Array base address (0x00000000)
#   $t1 ($9):  Current maximum value
#   $t2 ($10): Loop index i (starts at 1)
#   $t3 ($11): Array size limit N = 5
#   $t4 ($12): Current element array[i]
#   $t5 ($13): Memory byte pointer
#   $t6 ($14): Comparison flag ($t1 < $t4)
# ============================================================================

.data
    # Memory layout:
    # 0x00: 12
    # 0x04: 45
    # 0x08: 23
    # 0x0C: 67
    # 0x10: 34
    # 0x14: Result Maximum destination (67 = 0x00000043)

.text
main:
    # 1. Initialize base and load first element as initial max
    addi $t0, $zero, 0       # base = 0
    lw   $t1, 0($t0)         # max = array[0] = 12
    addi $t2, $zero, 1       # i = 1
    addi $t3, $zero, 5       # limit = 5
    addi $t5, $t0, 4         # pointer = address of array[1]

loop:
    # 2. Check if all elements checked
    beq  $t2, $t3, end       # if i == 5, finish

    # 3. Load next element and compare with current max
    lw   $t4, 0($t5)         # $t4 = array[i]
    slt  $t6, $t1, $t4       # $t6 = (max < array[i]) ? 1 : 0
    beq  $t6, $zero, skip    # if not smaller, skip update
    add  $t1, $t4, $zero     # max = array[i]

skip:
    # 4. Advance pointer and loop counter
    addi $t5, $t5, 4         # pointer += 4
    addi $t2, $t2, 1         # i += 1
    j    loop                # jump to loop

    # NOP padding
    add  $zero, $zero, $zero

end:
    # 5. Store result
    sw   $t1, 20($t0)        # Mem[20] = max (67)
halt:
    j    halt
