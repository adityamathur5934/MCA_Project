// ============================================================================
// Testbench: tb_data_memory
// Description: Self-checking unit testbench for Data Memory.
//              Verifies reset, word-aligned addressing, synchronous writes,
//              and combinational reads.
// ============================================================================

`timescale 1ns / 1ps

module tb_data_memory;

    reg         clk;
    reg         rst;
    reg         mem_read;
    reg         mem_write;
    reg  [31:0] addr;
    reg  [31:0] write_data;
    wire [31:0] read_data;

    integer tests_passed = 0;
    integer tests_failed = 0;
    integer test_id      = 0;

    data_memory #(
        .MEM_DEPTH (256)
    ) uut (
        .clk        (clk),
        .rst        (rst),
        .mem_read   (mem_read),
        .mem_write  (mem_write),
        .addr       (addr),
        .write_data (write_data),
        .read_data  (read_data)
    );

    // Clock generator: 10ns period
    always #5 clk = ~clk;

    task check_data;
        input [31:0]       exp_data;
        input [8*32-1:0]   name;
        begin
            #2; // Wait for combinational read
            test_id = test_id + 1;
            if (read_data === exp_data) begin
                $display("[PASS] Test %2d: %s | Addr=0x%08h, Data=0x%08h",
                         test_id, name, addr, read_data);
                tests_passed = tests_passed + 1;
            end else begin
                $display("[FAIL] Test %2d: %s | Addr=0x%08h | Got: 0x%08h | Expected: 0x%08h",
                         test_id, name, addr, read_data, exp_data);
                tests_failed = tests_failed + 1;
            end
        end
    endtask

    initial begin
        $dumpfile("simulation/waveforms/tb_data_memory.vcd");
        $dumpvars(0, tb_data_memory);

        clk        = 0;
        rst        = 1;
        mem_read   = 0;
        mem_write  = 0;
        addr       = 0;
        write_data = 0;

        $display("==================================================");
        $display("Starting Data Memory Verification");
        $display("==================================================");

        // 1. Reset check
        #10;
        rst = 0;
        mem_read = 1;
        addr = 32'h00000000;
        check_data(32'h00000000, "Reset clears word 0");

        // 2. Synchronous Write to Word 1 (Byte Address 0x00000004)
        @(negedge clk);
        mem_read   = 0;
        mem_write  = 1;
        addr       = 32'h00000004;
        write_data = 32'hCAFE1234;
        @(negedge clk);
        mem_write  = 0;
        mem_read   = 1;
        check_data(32'hCAFE1234, "Read Word 1 (0x04) with mem_read=1");

        // 3. Read with mem_read = 0 (Must return 0)
        mem_read = 0;
        check_data(32'h00000000, "Read Word 1 with mem_read=0 returns 0");

        // 4. Synchronous Write to Word 5 (Byte Address 0x00000014 = 20)
        @(negedge clk);
        mem_write  = 1;
        addr       = 32'h00000014;
        write_data = 32'h00000064; // 100 decimal
        @(negedge clk);
        mem_write  = 0;
        mem_read   = 1;
        check_data(32'h00000064, "Read Word 5 (0x14) stored value 100");

        // 5. Overwrite Word 1
        @(negedge clk);
        mem_write  = 1;
        addr       = 32'h00000004;
        write_data = 32'hDEADBEEF;
        @(negedge clk);
        mem_write  = 0;
        mem_read   = 1;
        check_data(32'hDEADBEEF, "Overwrite Word 1 with DEADBEEF");

        $display("==================================================");
        $display("Data Memory Verification Finished");
        $display("Total Tests : %0d", test_id);
        $display("Tests Passed: %0d", tests_passed);
        $display("Tests Failed: %0d", tests_failed);
        $display("==================================================");

        if (tests_failed == 0) begin
            $display(">>> ALL DATA MEMORY TESTS PASSED <<<");
        end else begin
            $display(">>> DATA MEMORY VERIFICATION FAILED <<<");
            $finish(1);
        end

        $finish;
    end

endmodule
