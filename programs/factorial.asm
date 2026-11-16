# ============================================================================
# Program 3: Factorial
# Architecture: Single-Cycle MIPS (32-bit)
#
# Description:
#   Computes the factorial of N = 5:
#   5! = 5 * 4 * 3 * 2 * 1 = 120 (Hex: 0x78)
#   Uses repeated addition for multiplication on the single-cycle core.
#   Result stored at Data Memory byte address 0 (0x00000000).
#
# Demonstrates:
#   ADDI (with negative immediate for decrement), ADD, BEQ, SW, J
#
# Register Allocation:
#   $t0 ($8):  Input N = 5
#   $t1 ($9):  Accumulated factorial result (initially 1)
#   $t2 ($10): Multiplier counter n (counts 5 down to 2)
#   $t3 ($11): Constant 1 for termination comparison
#   $t4 ($12): Product accumulator for inner multiplication loop
#   $t5 ($13): Inner loop counter j
#   $t6 ($14): Memory base address pointer (0)
# ============================================================================

.text
main:
    # 1. Initialize variables
    addi $t0, $zero, 5       # N = 5
    addi $t1, $zero, 1       # result = 1
    addi $t2, $t0, 0         # n = 5
    addi $t3, $zero, 1       # const 1

outer_loop:
    # 2. If n <= 1 (i.e. n == 1), calculation complete
    beq  $t2, $t3, end       # if n == 1, branch to end

    # 3. Multiply result by n using repeated addition:
    #    product = 0; for (j = 0; j < n; j++) product += result;
    addi $t4, $zero, 0       # product = 0
    addi $t5, $zero, 0       # j = 0

inner_loop:
    beq  $t5, $t2, inner_end # if j == n, inner multiplication done
    add  $t4, $t4, $t1       # product += result
    addi $t5, $t5, 1         # j++
    j    inner_loop

inner_end:
    add  $t1, $t4, $zero     # result = product
    addi $t2, $t2, -1        # n = n - 1 (demonstrates negative immediate)
    j    outer_loop

end:
    # 4. Store factorial result (120) into Data Memory
    addi $t6, $zero, 0       # base = 0
    sw   $t1, 0($t6)         # Mem[0] = 120
halt:
    j    halt                # Halt execution
