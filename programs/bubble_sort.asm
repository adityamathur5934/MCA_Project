# ============================================================================
# Program 4: Bubble Sort Benchmark
# Architecture: MIPS (Single-Cycle & 5-Stage Pipelined Core)
#
# Description:
#   Sorts an array of 5 integers in ascending order:
#   Initial Array in Data Memory [Mem[0..16]]:
#     Mem[0]  = 45
#     Mem[4]  = 12
#     Mem[8]  = 89
#     Mem[12] = 34
#     Mem[16] = 23
#   Expected Sorted Array:
#     Mem[0]  = 12
#     Mem[4]  = 23
#     Mem[8]  = 34
#     Mem[12] = 45
#     Mem[16] = 89
#
# Register Allocation:
#   $t0 ($8):  Array base pointer (0)
#   $t1 ($9):  Outer loop counter i (0 to 4)
#   $t2 ($10): Outer loop limit n = 5
#   $t3 ($11): Inner loop counter j
#   $t4 ($12): Inner loop limit (n - 1 = 4)
#   $t5 ($13): Current element pointer
#   $t6 ($14): Element A = array[j]
#   $t7 ($15): Element B = array[j+1]
#   $s0 ($16): Comparison flag ($t7 < $t6)
# ============================================================================

.text
main:
    addi $t0, $zero, 0       # base address = 0
    addi $t1, $zero, 0       # i = 0
    addi $t2, $zero, 5       # n = 5
    addi $t4, $zero, 4       # inner_limit = 4

outer_loop:
    beq  $t1, $t2, end       # if i == n, sorting complete
    addi $t3, $zero, 0       # j = 0
    addi $t5, $t0, 0         # ptr = base address

inner_loop:
    beq  $t3, $t4, inner_end # if j == 4, outer pass finished
    lw   $t6, 0($t5)         # A = array[j]
    lw   $t7, 4($t5)         # B = array[j+1]
    slt  $s0, $t7, $t6       # if B < A, s0 = 1 (swap needed)
    beq  $s0, $zero, no_swap # if not less, skip swap
    sw   $t7, 0($t5)         # array[j] = B
    sw   $t6, 4($t5)         # array[j+1] = A

no_swap:
    addi $t5, $t5, 4         # ptr += 4
    addi $t3, $t3, 1         # j++
    j    inner_loop

inner_end:
    addi $t1, $t1, 1         # i++
    j    outer_loop

end:
    j    end                 # halt
