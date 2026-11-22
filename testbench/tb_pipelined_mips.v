// ============================================================================
// Testbench: tb_pipelined_mips
// Description: Comprehensive Verification Testbench for 5-Stage Pipelined
//              MIPS Processor with Forwarding and Hazard Detection.
//              Verifies:
//              - Pipeline execution & throughput
//              - RAW Data Hazard resolution via Forwarding Unit (EX & MEM paths)
//              - Load-Use Data Hazard resolution via 1-cycle Stall Bubble
//              - Control Hazard resolution via Branch Flush
//              - Benchmark 1: Array Sum (Mem[16] == 100)
//              - Benchmark 2: Maximum Search (Mem[20] == 67)
//              - Benchmark 3: Factorial (Mem[0] == 120)
//              - Benchmark 4: Fibonacci Sequence (Mem[32] == 21)
//              - Benchmark 5: Bubble Sort ([45, 12, 89, 34, 23] -> [12, 23, 34, 45, 89])
// ============================================================================

`timescale 1ns / 1ps

module tb_pipelined_mips;

    reg clk;
    reg rst;

    // Observability signals
    wire [31:0] pc;
    wire [31:0] instruction;
    wire [31:0] alu_result;
    wire [31:0] reg_write_data;
    wire [4:0]  write_reg;
    wire        reg_write;
    wire [31:0] mem_write_data;
    wire [31:0] mem_read_data;
    wire        mem_read;
    wire        mem_write;
    wire        pipeline_stall;
    wire        branch_taken;

    integer tests_passed = 0;
    integer tests_failed = 0;
    integer test_id      = 0;
    integer cycle_count  = 0;

    // Instantiate Top-Level Pipelined System
    top_pipelined_module #(
        .IMEM_DEPTH (256),
        .DMEM_DEPTH (256),
        .IMEM_FILE  ("programs/array_sum.hex")
    ) uut (
        .clk            (clk),
        .rst            (rst),
        .pc             (pc),
        .instruction    (instruction),
        .alu_result     (alu_result),
        .reg_write_data (reg_write_data),
        .write_reg      (write_reg),
        .reg_write      (reg_write),
        .mem_write_data (mem_write_data),
        .mem_read_data  (mem_read_data),
        .mem_read       (mem_read),
        .mem_write      (mem_write),
        .pipeline_stall (pipeline_stall),
        .branch_taken   (branch_taken)
    );

    // Clock Generation: 100 MHz (10 ns period)
    always #5 clk = ~clk;

    // Cycle counter
    always @(posedge clk) begin
        if (!rst) cycle_count = cycle_count + 1;
    end

    // Assert test task
    task assert_test;
        input              condition;
        input [8*48-1:0]   test_name;
        input [31:0]       observed;
        input [31:0]       expected;
        begin
            test_id = test_id + 1;
            if (condition) begin
                $display("[PASS] Test %2d: %s | Observed: 0x%08h (%0d)",
                         test_id, test_name, observed, observed);
                tests_passed = tests_passed + 1;
            end else begin
                $display("[FAIL] Test %2d: %s | Observed: 0x%08h (%0d) | Expected: 0x%08h (%0d)",
                         test_id, test_name, observed, observed, expected, expected);
                tests_failed = tests_failed + 1;
            end
        end
    endtask

    // Reset CPU
    task reset_cpu;
        begin
            rst = 1'b1;
            repeat (3) @(negedge clk);
            rst = 1'b0;
            @(negedge clk);
        end
    endtask

    initial begin
        $dumpfile("simulation/waveforms/tb_pipelined_mips.vcd");
        $dumpvars(0, tb_pipelined_mips);

        clk = 0;
        rst = 1;

        $display("================================================================");
        $display("   FINAL PHASE: 5-STAGE PIPELINED MIPS PROCESSOR VERIFICATION   ");
        $display("================================================================");

        // ====================================================================
        // SECTION 1: PIPELINE HAZARDS & FORWARDING UNIT VERIFICATION
        // ====================================================================
        $display("\n--- PART 1: Forwarding & Hazard Unit Test Sequence ---");

        // Load custom hazard test program into IMEM:
        uut.u_instruction_memory.mem[0] = 32'h2009000a; // addi $t1, $0, 10
        uut.u_instruction_memory.mem[1] = 32'h01295020; // add  $t2, $t1, $t1
        uut.u_instruction_memory.mem[2] = 32'h012a5820; // add  $t3, $t1, $t2
        uut.u_instruction_memory.mem[3] = 32'hac0b0000; // sw   $t3, 0($0)
        uut.u_instruction_memory.mem[4] = 32'h8c0c0000; // lw   $t4, 0($0)
        uut.u_instruction_memory.mem[5] = 32'h01896820; // add  $t5, $t4, $t1
        uut.u_instruction_memory.mem[6] = 32'h11290002; // beq  $t1, $t1, 2 (target PC = 0x24)
        uut.u_instruction_memory.mem[7] = 32'h20100063; // addi $s0, $0, 99
        uut.u_instruction_memory.mem[8] = 32'h20110063; // addi $s1, $0, 99
        uut.u_instruction_memory.mem[9] = 32'h2012004d; // addi $s2, $0, 77

        reset_cpu();

        // Run 25 cycles through pipeline
        repeat (25) @(negedge clk);

        // Verify Register Results
        assert_test((uut.u_pipelined_cpu.u_register_file.registers[9] === 32'd10),
                    "ADDI writeback to $t1 == 10", uut.u_pipelined_cpu.u_register_file.registers[9], 32'd10);

        assert_test((uut.u_pipelined_cpu.u_register_file.registers[10] === 32'd20),
                    "EX-to-EX Forwarding: $t2 == 20", uut.u_pipelined_cpu.u_register_file.registers[10], 32'd20);

        assert_test((uut.u_pipelined_cpu.u_register_file.registers[11] === 32'd30),
                    "MEM-to-EX Forwarding: $t3 == 30", uut.u_pipelined_cpu.u_register_file.registers[11], 32'd30);

        assert_test((uut.u_data_memory.mem[0] === 32'd30),
                    "SW from forwarded register: Mem[0] == 30", uut.u_data_memory.mem[0], 32'd30);

        assert_test((uut.u_pipelined_cpu.u_register_file.registers[12] === 32'd30),
                    "LW writeback: $t4 == 30", uut.u_pipelined_cpu.u_register_file.registers[12], 32'd30);

        assert_test((uut.u_pipelined_cpu.u_register_file.registers[13] === 32'd40),
                    "Load-Use Stall + Forwarding: $t5 == 40", uut.u_pipelined_cpu.u_register_file.registers[13], 32'd40);

        assert_test((uut.u_pipelined_cpu.u_register_file.registers[16] === 32'd0),
                    "Branch Flush Safety: $s0 remains 0 (not 99)", uut.u_pipelined_cpu.u_register_file.registers[16], 32'd0);

        assert_test((uut.u_pipelined_cpu.u_register_file.registers[18] === 32'd77),
                    "Branch Target Executed: $s2 == 77", uut.u_pipelined_cpu.u_register_file.registers[18], 32'd77);

        // ====================================================================
        // SECTION 2: BENCHMARK 1 — ARRAY SUM ON PIPELINED CORE
        // ====================================================================
        $display("\n--- PART 2: Benchmark 1 — Array Sum (10, 20, 30, 40) ---");
        $readmemh("programs/array_sum.hex", uut.u_instruction_memory.mem);
        reset_cpu();

        // Prepopulate Data Memory AFTER reset so reset doesn't clear them!
        uut.u_data_memory.mem[0] = 32'd10;
        uut.u_data_memory.mem[1] = 32'd20;
        uut.u_data_memory.mem[2] = 32'd30;
        uut.u_data_memory.mem[3] = 32'd40;
        uut.u_data_memory.mem[4] = 32'd0;

        repeat (80) @(negedge clk);

        assert_test((uut.u_data_memory.mem[4] === 32'd100),
                    "Pipelined Array Sum: Mem[16] == 100", uut.u_data_memory.mem[4], 32'd100);
        assert_test((uut.u_pipelined_cpu.u_register_file.registers[9] === 32'd100),
                    "Pipelined Array Sum: Reg $t1 == 100", uut.u_pipelined_cpu.u_register_file.registers[9], 32'd100);

        // ====================================================================
        // SECTION 3: BENCHMARK 2 — MAXIMUM SEARCH ON PIPELINED CORE
        // ====================================================================
        $display("\n--- PART 3: Benchmark 2 — Maximum Search (12, 45, 23, 67, 34) ---");
        $readmemh("programs/maximum_search.hex", uut.u_instruction_memory.mem);
        reset_cpu();

        // Prepopulate Data Memory AFTER reset
        uut.u_data_memory.mem[0] = 32'd12;
        uut.u_data_memory.mem[1] = 32'd45;
        uut.u_data_memory.mem[2] = 32'd23;
        uut.u_data_memory.mem[3] = 32'd67;
        uut.u_data_memory.mem[4] = 32'd34;
        uut.u_data_memory.mem[5] = 32'd0;

        repeat (90) @(negedge clk);

        assert_test((uut.u_data_memory.mem[5] === 32'd67),
                    "Pipelined Max Search: Mem[20] == 67", uut.u_data_memory.mem[5], 32'd67);
        assert_test((uut.u_pipelined_cpu.u_register_file.registers[9] === 32'd67),
                    "Pipelined Max Search: Reg $t1 == 67", uut.u_pipelined_cpu.u_register_file.registers[9], 32'd67);

        // ====================================================================
        // SECTION 4: BENCHMARK 3 — FACTORIAL (5! = 120)
        // ====================================================================
        $display("\n--- PART 4: Benchmark 3 — Factorial (5! = 120) ---");
        $readmemh("programs/factorial.hex", uut.u_instruction_memory.mem);
        reset_cpu();

        repeat (650) @(negedge clk);

        assert_test((uut.u_data_memory.mem[0] === 32'd120),
                    "Pipelined Factorial: Mem[0] == 120", uut.u_data_memory.mem[0], 32'd120);
        assert_test((uut.u_pipelined_cpu.u_register_file.registers[9] === 32'd120),
                    "Pipelined Factorial: Reg $t1 == 120", uut.u_pipelined_cpu.u_register_file.registers[9], 32'd120);

        // ====================================================================
        // SECTION 5: BENCHMARK 4 — FIBONACCI (F8 = 21)
        // ====================================================================
        $display("\n--- PART 5: Benchmark 4 — Fibonacci Sequence (F(8) = 21) ---");
        $readmemh("programs/fibonacci.hex", uut.u_instruction_memory.mem);
        reset_cpu();

        repeat (120) @(negedge clk);

        assert_test((uut.u_data_memory.mem[8] === 32'd21),
                    "Pipelined Fibonacci: Mem[32] == 21 (0x15)", uut.u_data_memory.mem[8], 32'd21);
        assert_test((uut.u_pipelined_cpu.u_register_file.registers[11] === 32'd21),
                    "Pipelined Fibonacci: Reg $t3 == 21", uut.u_pipelined_cpu.u_register_file.registers[11], 32'd21);

        // ====================================================================
        // SECTION 6: BENCHMARK 5 — BUBBLE SORT ([45,12,89,34,23] -> [12,23,34,45,89])
        // ====================================================================
        $display("\n--- PART 6: Benchmark 5 — Bubble Sort ---");
        $readmemh("programs/bubble_sort.hex", uut.u_instruction_memory.mem);
        reset_cpu();

        // Prepopulate Data Memory AFTER reset
        uut.u_data_memory.mem[0] = 32'd45;
        uut.u_data_memory.mem[1] = 32'd12;
        uut.u_data_memory.mem[2] = 32'd89;
        uut.u_data_memory.mem[3] = 32'd34;
        uut.u_data_memory.mem[4] = 32'd23;

        repeat (500) @(negedge clk);

        assert_test((uut.u_data_memory.mem[0] === 32'd12),
                    "Bubble Sort: Mem[0] == 12", uut.u_data_memory.mem[0], 32'd12);
        assert_test((uut.u_data_memory.mem[1] === 32'd23),
                    "Bubble Sort: Mem[4] == 23", uut.u_data_memory.mem[1], 32'd23);
        assert_test((uut.u_data_memory.mem[2] === 32'd34),
                    "Bubble Sort: Mem[8] == 34", uut.u_data_memory.mem[2], 32'd34);
        assert_test((uut.u_data_memory.mem[3] === 32'd45),
                    "Bubble Sort: Mem[12] == 45", uut.u_data_memory.mem[3], 32'd45);
        assert_test((uut.u_data_memory.mem[4] === 32'd89),
                    "Bubble Sort: Mem[16] == 89", uut.u_data_memory.mem[4], 32'd89);

        // ====================================================================
        // SUMMARY
        // ====================================================================
        $display("\n================================================================");
        $display("   PIPELINED PROCESSOR VERIFICATION SUMMARY");
        $display("================================================================");
        $display("Total Assertions Executed : %0d", test_id);
        $display("Total Assertions Passed   : %0d", tests_passed);
        $display("Total Assertions Failed   : %0d", tests_failed);
        $display("Total Simulation Cycles   : %0d", cycle_count);
        $display("================================================================");

        if (tests_failed == 0) begin
            $display(">>> ALL PIPELINED PROCESSOR TESTS PASSED WITH 100%% SUCCESS <<<\n");
        end else begin
            $display(">>> ERROR: SOME PIPELINED TESTS FAILED <<<\n");
        end

        $finish;
    end

endmodule
