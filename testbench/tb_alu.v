// ============================================================================
// Testbench: tb_alu
// Description: Comprehensive self-checking unit testbench for 32-bit ALU.
//              Verifies ADD, SUB, AND, OR, SLT, signed comparisons, and Zero flag.
// ============================================================================

`timescale 1ns / 1ps

module tb_alu;

    reg  [31:0] a;
    reg  [31:0] b;
    reg  [3:0]  alu_ctrl;
    wire [31:0] result;
    wire        zero;

    integer tests_passed = 0;
    integer tests_failed = 0;
    integer test_id      = 0;

    // Instantiate ALU under test
    alu uut (
        .a        (a),
        .b        (b),
        .alu_ctrl (alu_ctrl),
        .result   (result),
        .zero     (zero)
    );

    // ALU control codes
    localparam ALU_AND = 4'b0000;
    localparam ALU_OR  = 4'b0001;
    localparam ALU_ADD = 4'b0010;
    localparam ALU_SUB = 4'b0110;
    localparam ALU_SLT = 4'b0111;

    task check_alu;
        input [31:0]       expected_result;
        input              expected_zero;
        input [8*32-1:0]   test_name;
        begin
            #1; // Wait for combinational logic propagation
            test_id = test_id + 1;
            if (result === expected_result && zero === expected_zero) begin
                $display("[PASS] Test %2d: %s | Result = 0x%08h, Zero = %b",
                         test_id, test_name, result, zero);
                tests_passed = tests_passed + 1;
            end else begin
                $display("[FAIL] Test %2d: %s | Got: Result = 0x%08h, Zero = %b | Expected: Result = 0x%08h, Zero = %b",
                         test_id, test_name, result, zero, expected_result, expected_zero);
                tests_failed = tests_failed + 1;
            end
        end
    endtask

    initial begin
        $dumpfile("simulation/waveforms/tb_alu.vcd");
        $dumpvars(0, tb_alu);

        $display("==================================================");
        $display("Starting ALU Unit Verification");
        $display("==================================================");

        // 1. ADD Tests
        a = 32'd25; b = 32'd15; alu_ctrl = ALU_ADD;
        check_alu(32'd40, 1'b0, "ADD positive numbers");

        a = 32'd100; b = -32'd40; alu_ctrl = ALU_ADD;
        check_alu(32'd60, 1'b0, "ADD with negative number");

        a = 32'd50; b = -32'd50; alu_ctrl = ALU_ADD;
        check_alu(32'd0, 1'b1, "ADD producing Zero");

        // 2. SUB Tests
        a = 32'd85; b = 32'd35; alu_ctrl = ALU_SUB;
        check_alu(32'd50, 1'b0, "SUB positive numbers");

        a = 32'd120; b = 32'd120; alu_ctrl = ALU_SUB;
        check_alu(32'd0, 1'b1, "SUB equal numbers (Zero flag)");

        a = 32'd10; b = 32'd25; alu_ctrl = ALU_SUB;
        check_alu(-32'd15, 1'b0, "SUB yielding negative result");

        // 3. AND Tests
        a = 32'hF0F0AA55; b = 32'hFFFF0000; alu_ctrl = ALU_AND;
        check_alu(32'hF0F00000, 1'b0, "AND bitwise operation");

        a = 32'hAAAA5555; b = 32'h5555AAAA; alu_ctrl = ALU_AND;
        check_alu(32'h00000000, 1'b1, "AND bitwise producing zero");

        // 4. OR Tests
        a = 32'hF0F00000; b = 32'h000F55AA; alu_ctrl = ALU_OR;
        check_alu(32'hF0FF55AA, 1'b0, "OR bitwise operation");

        a = 32'h00000000; b = 32'h00000000; alu_ctrl = ALU_OR;
        check_alu(32'h00000000, 1'b1, "OR zero inputs");

        // 5. SLT Tests (Signed Comparisons)
        a = 32'd10; b = 32'd20; alu_ctrl = ALU_SLT;
        check_alu(32'd1, 1'b0, "SLT (10 < 20)");

        a = 32'd20; b = 32'd10; alu_ctrl = ALU_SLT;
        check_alu(32'd0, 1'b1, "SLT (20 < 10)");

        a = 32'd15; b = 32'd15; alu_ctrl = ALU_SLT;
        check_alu(32'd0, 1'b1, "SLT (15 < 15)");

        // Signed comparison: negative vs positive
        a = -32'd10; b = 32'd5; alu_ctrl = ALU_SLT;
        check_alu(32'd1, 1'b0, "SLT (-10 < 5 signed)");

        a = 32'd5; b = -32'd10; alu_ctrl = ALU_SLT;
        check_alu(32'd0, 1'b1, "SLT (5 < -10 signed)");

        a = -32'd20; b = -32'd10; alu_ctrl = ALU_SLT;
        check_alu(32'd1, 1'b0, "SLT (-20 < -10 signed)");

        $display("==================================================");
        $display("ALU Verification Finished");
        $display("Total Tests : %0d", test_id);
        $display("Tests Passed: %0d", tests_passed);
        $display("Tests Failed: %0d", tests_failed);
        $display("==================================================");

        if (tests_failed == 0) begin
            $display(">>> ALL ALU TESTS PASSED <<<");
        end else begin
            $display(">>> ALU VERIFICATION FAILED <<<");
            $finish(1);
        end

        $finish;
    end

endmodule
