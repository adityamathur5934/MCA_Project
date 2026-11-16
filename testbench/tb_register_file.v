// ============================================================================
// Testbench: tb_register_file
// Description: Self-checking unit testbench for 32x32-bit Register File.
//              Verifies reset, $zero hardwired protection, synchronous writes,
//              and dual combinational read ports.
// ============================================================================

`timescale 1ns / 1ps

module tb_register_file;

    reg         clk;
    reg         rst;
    reg         reg_write;
    reg  [4:0]  read_reg1;
    reg  [4:0]  read_reg2;
    reg  [4:0]  write_reg;
    reg  [31:0] write_data;
    wire [31:0] read_data1;
    wire [31:0] read_data2;

    integer tests_passed = 0;
    integer tests_failed = 0;
    integer test_id      = 0;

    register_file uut (
        .clk        (clk),
        .rst        (rst),
        .reg_write  (reg_write),
        .read_reg1  (read_reg1),
        .read_reg2  (read_reg2),
        .write_reg  (write_reg),
        .write_data (write_data),
        .read_data1 (read_data1),
        .read_data2 (read_data2)
    );

    // Clock generator: 10ns period (100 MHz)
    always #5 clk = ~clk;

    task check_read;
        input [4:0]        reg_idx1;
        input [4:0]        reg_idx2;
        input [31:0]       exp_val1;
        input [31:0]       exp_val2;
        input [8*32-1:0]   name;
        begin
            read_reg1 = reg_idx1;
            read_reg2 = reg_idx2;
            #2; // Wait for combinational read
            test_id = test_id + 1;
            if (read_data1 === exp_val1 && read_data2 === exp_val2) begin
                $display("[PASS] Test %2d: %s | R[%0d]=0x%08h, R[%0d]=0x%08h",
                         test_id, name, reg_idx1, read_data1, reg_idx2, read_data2);
                tests_passed = tests_passed + 1;
            end else begin
                $display("[FAIL] Test %2d: %s | Got: R[%0d]=0x%08h, R[%0d]=0x%08h | Expected: 0x%08h, 0x%08h",
                         test_id, name, reg_idx1, read_data1, reg_idx2, read_data2, exp_val1, exp_val2);
                tests_failed = tests_failed + 1;
            end
        end
    endtask

    initial begin
        $dumpfile("simulation/waveforms/tb_register_file.vcd");
        $dumpvars(0, tb_register_file);

        clk        = 0;
        rst        = 1;
        reg_write  = 0;
        read_reg1  = 0;
        read_reg2  = 0;
        write_reg  = 0;
        write_data = 0;

        $display("==================================================");
        $display("Starting Register File Verification");
        $display("==================================================");

        // 1. Reset check
        #10;
        rst = 0;
        check_read(5'd1, 5'd2, 32'h00000000, 32'h00000000, "Reset clears registers");

        // 2. Write to R[1] and read back
        @(negedge clk);
        reg_write  = 1;
        write_reg  = 5'd1;
        write_data = 32'h12345678;
        @(negedge clk);
        reg_write  = 0;
        check_read(5'd1, 5'd0, 32'h12345678, 32'h00000000, "Write to R[1] and read R[0]");

        // 3. Register $zero write protection: Attempt to write 0xDEADBEEF to R[0]
        @(negedge clk);
        reg_write  = 1;
        write_reg  = 5'd0;
        write_data = 32'hDEADBEEF;
        @(negedge clk);
        reg_write  = 0;
        check_read(5'd0, 5'd0, 32'h00000000, 32'h00000000, "$zero hardwired zero protection");

        // 4. Write to R[10] and R[20], verify simultaneous dual read
        @(negedge clk);
        reg_write  = 1;
        write_reg  = 5'd10;
        write_data = 32'hAABBCCDD;
        @(negedge clk);
        write_reg  = 5'd20;
        write_data = 32'h55667788;
        @(negedge clk);
        reg_write  = 0;
        check_read(5'd10, 5'd20, 32'hAABBCCDD, 32'h55667788, "Dual port simultaneous read");

        // 5. Verify no write occurs when reg_write is low
        @(negedge clk);
        reg_write  = 0;
        write_reg  = 5'd10;
        write_data = 32'hFFFFFFFF;
        @(negedge clk);
        check_read(5'd10, 5'd1, 32'hAABBCCDD, 32'h12345678, "No write when reg_write=0");

        $display("==================================================");
        $display("Register File Verification Finished");
        $display("Total Tests : %0d", test_id);
        $display("Tests Passed: %0d", tests_passed);
        $display("Tests Failed: %0d", tests_failed);
        $display("==================================================");

        if (tests_failed == 0) begin
            $display(">>> ALL REGISTER FILE TESTS PASSED <<<");
        end else begin
            $display(">>> REGISTER FILE VERIFICATION FAILED <<<");
            $finish(1);
        end

        $finish;
    end

endmodule
