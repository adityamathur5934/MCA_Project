// ============================================================================
// Testbench: tb_mips_cpu
// Description: Comprehensive Integration and ISA Verification Testbench for
//              Single-Cycle MIPS Processor with Memory Interface.
//
//              Verifies:
//              1. All 10 supported instructions (ADD, SUB, AND, OR, SLT,
//                 ADDI, LW, SW, BEQ, J) with individual PASS/FAIL checks.
//              2. PC progression (+4), branch target, jump target.
//              3. Register $0 hardwired zero protection.
//              4. Reset behavior.
//              5. Complete execution of Sample Programs:
//                 - Program 1: Array Sum -> Verifies Mem[16] == 100
//                 - Program 2: Maximum Search -> Verifies Mem[20] == 67
//                 - Program 3: Factorial -> Verifies Mem[0] == 120
// ============================================================================

`timescale 1ns / 1ps

module tb_mips_cpu;

    reg         clk;
    reg         rst;

    // Observable outputs from top_module
    wire [31:0] pc;
    wire [31:0] instruction;
    wire [31:0] alu_result;
    wire [31:0] mem_write_data;
    wire [31:0] mem_read_data;
    wire [31:0] reg_write_data;
    wire [4:0]  write_reg;
    wire        reg_write;
    wire        mem_read;
    wire        mem_write;
    wire        zero;
    wire        branch;
    wire        jump;

    // Test tracking counters
    integer tests_passed = 0;
    integer tests_failed = 0;
    integer test_id      = 0;
    integer cycle_count  = 0;

    // Instantiate Top Module
    top_module #(
        .IMEM_DEPTH (256),
        .DMEM_DEPTH (256)
    ) uut (
        .clk            (clk),
        .rst            (rst),
        .pc             (pc),
        .instruction    (instruction),
        .alu_result     (alu_result),
        .mem_write_data (mem_write_data),
        .mem_read_data  (mem_read_data),
        .reg_write_data (reg_write_data),
        .write_reg      (write_reg),
        .reg_write      (reg_write),
        .mem_read       (mem_read),
        .mem_write      (mem_write),
        .zero           (zero),
        .branch         (branch),
        .jump           (jump)
    );

    // Clock generator: 100 MHz (10ns period)
    always #5 clk = ~clk;

    // Track clock cycles
    always @(posedge clk) begin
        if (!rst) cycle_count = cycle_count + 1;
    end

    // Helper task to report PASS/FAIL
    task assert_test;
        input              condition;
        input [8*40-1:0]   test_name;
        input [31:0]       observed;
        input [31:0]       expected;
        begin
            test_id = test_id + 1;
            if (condition) begin
                $display("[PASS] Test %2d: %s | Observed: 0x%08h (%0d)",
                         test_id, test_name, observed, observed);
                tests_passed = tests_passed + 1;
            end else begin
                $display("[FAIL] Test %2d: %s | Got: 0x%08h (%0d) | Expected: 0x%08h (%0d)",
                         test_id, test_name, observed, observed, expected, expected);
                tests_failed = tests_failed + 1;
            end
        end
    endtask

    // Task to reset processor
    task reset_cpu;
        begin
            rst = 1;
            @(negedge clk);
            @(negedge clk);
            rst = 0;
            #1; // Allow combinational logic to settle while at PC = 0x00
        end
    endtask

    // ------------------------------------------------------------------------
    // Test Suite Execution
    // ------------------------------------------------------------------------
    initial begin
        $dumpfile("simulation/waveforms/tb_mips_cpu.vcd");
        $dumpvars(0, tb_mips_cpu);

        clk = 0;
        rst = 1;

        $display("================================================================");
        $display("   SINGLE-CYCLE MIPS PROCESSOR: FULL SYSTEM VERIFICATION");
        $display("================================================================");

        // ====================================================================
        // SECTION A: INDIVIDUAL INSTRUCTION-SET VERIFICATION (10 INSTRUCTIONS)
        // ====================================================================
        $display("\n--- PART 1: ISA Verification (10 Instructions & Core Logic) ---");

        // Preload micro-test instructions directly into IMEM:
        // Word 0  (0x00): ADDI $t1, $zero, 25   -> 0x20090019
        // Word 1  (0x04): ADDI $t2, $zero, 15   -> 0x200A000F
        // Word 2  (0x08): ADD  $t3, $t1, $t2    -> 0x012A5820 (25 + 15 = 40)
        // Word 3  (0x0C): SUB  $t4, $t1, $t2    -> 0x012A6022 (25 - 15 = 10)
        // Word 4  (0x10): AND  $t5, $t1, $t2    -> 0x012A6824 (25 & 15 = 9)
        // Word 5  (0x14): OR   $t6, $t1, $t2    -> 0x012A7025 (25 | 15 = 31)
        // Word 6  (0x18): SLT  $t7, $t2, $t1    -> 0x0149782A (15 < 25 -> 1)
        // Word 7  (0x1C): ADDI $s0, $zero, -5   -> 0x2010FFFB (negative immediate)
        // Word 8  (0x20): SW   $t3, 8($zero)    -> 0xAC0B0008 (store 40 at Mem[8])
        // Word 9  (0x24): LW   $s1, 8($zero)    -> 0x8C110008 (load from Mem[8])
        // Word 10 (0x28): BEQ  $t1, $t2, +2     -> 0x112A0002 (not taken: 25 != 15)
        // Word 11 (0x2C): ADDI $s2, $zero, 99   -> 0x20120063 (executed because BEQ not taken)
        // Word 12 (0x30): BEQ  $t1, $t1, +2     -> 0x11290002 (taken: 25 == 25, jumps to 0x3C)
        // Word 13 (0x34): ADDI $s3, $zero, 88   -> 0x20130058 (skipped!)
        // Word 14 (0x38): ADDI $s3, $zero, 77   -> 0x2013004D (skipped!)
        // Word 15 (0x3C): J    0x48             -> 0x08000012 (jumps to Word 18 = 0x48)
        // Word 16 (0x40): ADDI $s4, $zero, 66   -> 0x20140042 (skipped!)
        // Word 17 (0x44): ADDI $s4, $zero, 55   -> 0x20140037 (skipped!)
        // Word 18 (0x48): ADDI $0, $zero, 111   -> 0x2000006F (attempt write to $zero)

        uut.u_instruction_memory.mem[0]  = 32'h20090019; // ADDI $t1, $zero, 25
        uut.u_instruction_memory.mem[1]  = 32'h200A000F; // ADDI $t2, $zero, 15
        uut.u_instruction_memory.mem[2]  = 32'h012A5820; // ADD  $t3, $t1, $t2
        uut.u_instruction_memory.mem[3]  = 32'h012A6022; // SUB  $t4, $t1, $t2
        uut.u_instruction_memory.mem[4]  = 32'h012A6824; // AND  $t5, $t1, $t2
        uut.u_instruction_memory.mem[5]  = 32'h012A7025; // OR   $t6, $t1, $t2
        uut.u_instruction_memory.mem[6]  = 32'h0149782A; // SLT  $t7, $t2, $t1
        uut.u_instruction_memory.mem[7]  = 32'h2010FFFB; // ADDI $s0, $zero, -5
        uut.u_instruction_memory.mem[8]  = 32'hAC0B0008; // SW   $t3, 8($zero)
        uut.u_instruction_memory.mem[9]  = 32'h8C110008; // LW   $s1, 8($zero)
        uut.u_instruction_memory.mem[10] = 32'h112A0002; // BEQ  $t1, $t2, +2 (not taken)
        uut.u_instruction_memory.mem[11] = 32'h20120063; // ADDI $s2, $zero, 99
        uut.u_instruction_memory.mem[12] = 32'h11290002; // BEQ  $t1, $t1, +2 (taken)
        uut.u_instruction_memory.mem[13] = 32'h20130058; // ADDI $s3, $zero, 88
        uut.u_instruction_memory.mem[14] = 32'h2013004D; // ADDI $s3, $zero, 77
        uut.u_instruction_memory.mem[15] = 32'h08000012; // J    0x48 (Word 18)
        uut.u_instruction_memory.mem[16] = 32'h20140042; // ADDI $s4, $zero, 66
        uut.u_instruction_memory.mem[17] = 32'h20140037; // ADDI $s4, $zero, 55
        uut.u_instruction_memory.mem[18] = 32'h2000006F; // ADDI $0, $zero, 111

        // Clear CPU state
        reset_cpu();

        // 1. Reset check: PC must be 0x00000000
        assert_test((pc === 32'h00000000), "Reset PC initialization", pc, 32'h00000000);

        // Execute Word 0: ADDI $t1, $zero, 25
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[9] === 32'd25),
                    "ADDI positive immediate ($t1=25)", uut.u_mips_cpu.u_register_file.registers[9], 32'd25);

        // Execute Word 1: ADDI $t2, $zero, 15
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[10] === 32'd15),
                    "ADDI second operand ($t2=15)", uut.u_mips_cpu.u_register_file.registers[10], 32'd15);

        // Execute Word 2: ADD $t3, $t1, $t2 (25 + 15 = 40)
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[11] === 32'd40),
                    "ADD instruction ($t3=40)", uut.u_mips_cpu.u_register_file.registers[11], 32'd40);

        // Execute Word 3: SUB $t4, $t1, $t2 (25 - 15 = 10)
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[12] === 32'd10),
                    "SUB instruction ($t4=10)", uut.u_mips_cpu.u_register_file.registers[12], 32'd10);

        // Execute Word 4: AND $t5, $t1, $t2 (25 & 15 = 9)
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[13] === 32'd9),
                    "AND instruction ($t5=9)", uut.u_mips_cpu.u_register_file.registers[13], 32'd9);

        // Execute Word 5: OR $t6, $t1, $t2 (25 | 15 = 31)
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[14] === 32'd31),
                    "OR instruction ($t6=31)", uut.u_mips_cpu.u_register_file.registers[14], 32'd31);

        // Execute Word 6: SLT $t7, $t2, $t1 (15 < 25 -> 1)
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[15] === 32'd1),
                    "SLT instruction ($t7=1)", uut.u_mips_cpu.u_register_file.registers[15], 32'd1);

        // Execute Word 7: ADDI $s0, $zero, -5
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[16] === -32'd5),
                    "ADDI negative immediate ($s0=-5)", uut.u_mips_cpu.u_register_file.registers[16], -32'd5);

        // Execute Word 8: SW $t3, 8($zero) (stores 40 at Mem[8])
        @(negedge clk);
        assert_test((uut.u_data_memory.mem[2] === 32'd40),
                    "SW instruction (Mem[8]=40)", uut.u_data_memory.mem[2], 32'd40);

        // Execute Word 9: LW $s1, 8($zero) (loads 40 into $s1)
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[17] === 32'd40),
                    "LW instruction ($s1=40)", uut.u_mips_cpu.u_register_file.registers[17], 32'd40);

        // Execute Word 10: BEQ $t1, $t2, +2 (Not taken, PC advances to 0x2C)
        @(negedge clk);
        assert_test((pc === 32'h0000002C),
                    "BEQ not taken (PC advances to 0x2C)", pc, 32'h0000002C);

        // Execute Word 11: ADDI $s2, $zero, 99
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[18] === 32'd99),
                    "Fall-through instruction ($s2=99)", uut.u_mips_cpu.u_register_file.registers[18], 32'd99);

        // Execute Word 12: BEQ $t1, $t1, +2 (Taken, branch target = 0x30 + 4 + (2<<2) = 0x3C)
        @(negedge clk);
        assert_test((pc === 32'h0000003C),
                    "BEQ taken (Branch target PC=0x3C)", pc, 32'h0000003C);

        // Check that skipped instructions (Words 13 & 14) did not execute
        assert_test((uut.u_mips_cpu.u_register_file.registers[19] === 32'd0),
                    "Skipped instruction branch safety ($s3=0)", uut.u_mips_cpu.u_register_file.registers[19], 32'd0);

        // Execute Word 15 (at 0x3C): J 0x48 (Jump target = 0x00000048)
        @(negedge clk);
        assert_test((pc === 32'h00000048),
                    "J instruction (Jump target PC=0x48)", pc, 32'h00000048);

        // Check that skipped instructions (Words 16 & 17) did not execute
        assert_test((uut.u_mips_cpu.u_register_file.registers[20] === 32'd0),
                    "Skipped instruction jump safety ($s4=0)", uut.u_mips_cpu.u_register_file.registers[20], 32'd0);

        // Execute Word 18 (at 0x48): ADDI $0, $zero, 111 (Attempt write to $0)
        @(negedge clk);
        assert_test((uut.u_mips_cpu.u_register_file.registers[0] === 32'd0),
                    "Register $zero write protection ($0 remains 0)", uut.u_mips_cpu.u_register_file.registers[0], 32'd0);


        // ====================================================================
        // SECTION B: SAMPLE PROGRAM 1 — ARRAY SUM (MANDATORY)
        // ====================================================================
        $display("\n--- PART 2: Sample Program 1 — Array Sum (10, 20, 30, 40) ---");
        reset_cpu();

        // Load array_sum.hex into Instruction Memory
        $readmemh("programs/array_sum.hex", uut.u_instruction_memory.mem);

        // Prepopulate Data Memory with input array: 10, 20, 30, 40 at bytes 0, 4, 8, 12
        uut.u_data_memory.mem[0] = 32'd10;
        uut.u_data_memory.mem[1] = 32'd20;
        uut.u_data_memory.mem[2] = 32'd30;
        uut.u_data_memory.mem[3] = 32'd40;
        uut.u_data_memory.mem[4] = 32'd0;  // Result location at byte 16 (Word 4)

        // Run processor for 40 cycles to execute the entire summation loop
        repeat (40) @(negedge clk);

        // Check that final sum stored in Data Memory at byte 16 (word 4) is 100
        assert_test((uut.u_data_memory.mem[4] === 32'd100),
                    "Array Sum Program: Mem[16] == 100", uut.u_data_memory.mem[4], 32'd100);

        // Also verify register $t1 holds 100
        assert_test((uut.u_mips_cpu.u_register_file.registers[9] === 32'd100),
                    "Array Sum Program: Reg $t1 == 100", uut.u_mips_cpu.u_register_file.registers[9], 32'd100);


        // ====================================================================
        // SECTION C: SAMPLE PROGRAM 2 — MAXIMUM SEARCH
        // ====================================================================
        $display("\n--- PART 3: Sample Program 2 — Maximum Search (12, 45, 23, 67, 34) ---");
        reset_cpu();

        // Load maximum_search.hex into Instruction Memory
        $readmemh("programs/maximum_search.hex", uut.u_instruction_memory.mem);

        // Prepopulate Data Memory with input array at bytes 0, 4, 8, 12, 16
        uut.u_data_memory.mem[0] = 32'd12;
        uut.u_data_memory.mem[1] = 32'd45;
        uut.u_data_memory.mem[2] = 32'd23;
        uut.u_data_memory.mem[3] = 32'd67;
        uut.u_data_memory.mem[4] = 32'd34;
        uut.u_data_memory.mem[5] = 32'd0;  // Result location at byte 20 (Word 5)

        // Run processor for 50 cycles to complete search loop
        repeat (50) @(negedge clk);

        // Check that maximum stored in Data Memory at byte 20 (word 5) is 67
        assert_test((uut.u_data_memory.mem[5] === 32'd67),
                    "Maximum Search Program: Mem[20] == 67", uut.u_data_memory.mem[5], 32'd67);

        // Verify register $t1 holds 67
        assert_test((uut.u_mips_cpu.u_register_file.registers[9] === 32'd67),
                    "Maximum Search Program: Reg $t1 == 67", uut.u_mips_cpu.u_register_file.registers[9], 32'd67);


        // ====================================================================
        // SECTION D: SAMPLE PROGRAM 3 — FACTORIAL (N = 5 -> 120)
        // ====================================================================
        $display("\n--- PART 4: Sample Program 3 — Factorial (5! = 120) ---");
        reset_cpu();

        // Load factorial.hex into Instruction Memory
        $readmemh("programs/factorial.hex", uut.u_instruction_memory.mem);
        uut.u_data_memory.mem[0] = 32'd0; // Result destination at byte 0

        // Run processor for 120 cycles to complete iterative factorial multiplication
        repeat (120) @(negedge clk);

        // Check that factorial result stored in Data Memory at byte 0 is 120
        assert_test((uut.u_data_memory.mem[0] === 32'd120),
                    "Factorial Program: Mem[0] == 120", uut.u_data_memory.mem[0], 32'd120);

        // Verify register $t1 holds 120
        assert_test((uut.u_mips_cpu.u_register_file.registers[9] === 32'd120),
                    "Factorial Program: Reg $t1 == 120", uut.u_mips_cpu.u_register_file.registers[9], 32'd120);


        // ====================================================================
        // SUMMARY
        // ====================================================================
        $display("\n================================================================");
        $display("   PROCESSOR INTEGRATION VERIFICATION SUMMARY");
        $display("================================================================");
        $display("Total Assertions Executed : %0d", test_id);
        $display("Total Assertions Passed   : %0d", tests_passed);
        $display("Total Assertions Failed   : %0d", tests_failed);
        $display("Total Simulation Cycles   : %0d", cycle_count);
        $display("================================================================");

        if (tests_failed == 0) begin
            $display(">>> ALL SYSTEM & PROGRAM VERIFICATION TESTS PASSED SUCCESSFULLY <<<");
        end else begin
            $display(">>> CRITICAL FAILURE: VERIFICATION TESTS FAILED <<<");
            $finish(1);
        end

        $finish;
    end

endmodule
