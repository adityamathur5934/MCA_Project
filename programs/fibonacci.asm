# ============================================================================
# Program 5: Fibonacci Sequence Generator
# Architecture: MIPS (Single-Cycle & 5-Stage Pipelined Core)
#
# Description:
#   Computes the first 8 Fibonacci numbers iteratively:
#   F(0) = 0, F(1) = 1, F(2) = 1, F(3) = 2, F(4) = 3,
#   F(5) = 5, F(6) = 8, F(7) = 13, F(8) = 21 (0x15).
#   Stores results in Data Memory Mem[0] to Mem[28].
#   Target verification: Mem[28] == 21.
#
# Register Allocation:
#   $t0 ($8):  Base memory address pointer
#   $t1 ($9):  F(n-2), initially 0
#   $t2 ($10): F(n-1), initially 1
#   $t3 ($11): F(n) = F(n-1) + F(n-2)
#   $t4 ($12): Loop counter i (starts at 2)
#   $t5 ($13): Limit N = 8
# ============================================================================

.text
main:
    addi $t0, $zero, 0       # base = 0
    addi $t1, $zero, 0       # F0 = 0
    addi $t2, $zero, 1       # F1 = 1
    sw   $t1, 0($t0)         # Mem[0] = 0
    sw   $t2, 4($t0)         # Mem[4] = 1
    addi $t0, $t0, 8         # ptr = 8
    addi $t4, $zero, 2       # i = 2
    addi $t5, $zero, 8       # N = 8

fib_loop:
    beq  $t4, $t5, fib_done  # if i == 8, done (computes F2 through F7, then F8)
    add  $t3, $t1, $t2       # F(n) = F(n-1) + F(n-2)
    sw   $t3, 0($t0)         # Mem[ptr] = F(n)
    add  $t1, $t2, $zero     # F(n-2) = F(n-1)
    add  $t2, $t3, $zero     # F(n-1) = F(n)
    addi $t0, $t0, 4         # ptr += 4
    addi $t4, $t4, 1         # i++
    j    fib_loop

fib_done:
    # Compute 8th Fibonacci number
    add  $t3, $t1, $t2       # F(8) = 8 + 13 = 21
    sw   $t3, 0($t0)         # Mem[28] = 21 (0x15)
halt:
    j    halt                # halt
