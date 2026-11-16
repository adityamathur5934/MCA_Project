// ============================================================================
// Testbench: tb_control_unit
// Description: Self-checking unit testbench for Main Control Unit.
//              Verifies all 9 control outputs across all supported opcodes.
// ============================================================================

`timescale 1ns / 1ps

module tb_control_unit;

    reg  [5:0] opcode;
    wire       reg_dst;
    wire       alu_src;
    wire       mem_to_reg;
    wire       reg_write;
    wire       mem_read;
    wire       mem_write;
    wire       branch;
    wire       jump;
    wire [1:0] alu_op;

    integer tests_passed = 0;
    integer tests_failed = 0;
    integer test_id      = 0;

    control_unit uut (
        .opcode     (opcode),
        .reg_dst    (reg_dst),
        .alu_src    (alu_src),
        .mem_to_reg (mem_to_reg),
        .reg_write  (reg_write),
        .mem_read   (mem_read),
        .mem_write  (mem_write),
        .branch     (branch),
        .jump       (jump),
        .alu_op     (alu_op)
    );

    task check_controls;
        input       exp_reg_dst;
        input       exp_alu_src;
        input       exp_mem_to_reg;
        input       exp_reg_write;
        input       exp_mem_read;
        input       exp_mem_write;
        input       exp_branch;
        input       exp_jump;
        input [1:0] exp_alu_op;
        input [8*24-1:0] name;
        begin
            #1;
            test_id = test_id + 1;
            if (reg_dst === exp_reg_dst &&
                alu_src === exp_alu_src &&
                mem_to_reg === exp_mem_to_reg &&
                reg_write === exp_reg_write &&
                mem_read === exp_mem_read &&
                mem_write === exp_mem_write &&
                branch === exp_branch &&
                jump === exp_jump &&
                alu_op === exp_alu_op) begin
                $display("[PASS] Test %2d: %s (Opcode: 6'b%06b)", test_id, name, opcode);
                tests_passed = tests_passed + 1;
            end else begin
                $display("[FAIL] Test %2d: %s (Opcode: 6'b%06b)", test_id, name, opcode);
                $display("       Got:      RegDst=%b ALUSrc=%b MemToReg=%b RegWrite=%b MemRead=%b MemWrite=%b Branch=%b Jump=%b ALUOp=%b",
                         reg_dst, alu_src, mem_to_reg, reg_write, mem_read, mem_write, branch, jump, alu_op);
                $display("       Expected: RegDst=%b ALUSrc=%b MemToReg=%b RegWrite=%b MemRead=%b MemWrite=%b Branch=%b Jump=%b ALUOp=%b",
                         exp_reg_dst, exp_alu_src, exp_mem_to_reg, exp_reg_write, exp_mem_read, exp_mem_write, exp_branch, exp_jump, exp_alu_op);
                tests_failed = tests_failed + 1;
            end
        end
    endtask

    initial begin
        $dumpfile("simulation/waveforms/tb_control_unit.vcd");
        $dumpvars(0, tb_control_unit);

        $display("==================================================");
        $display("Starting Control Unit Verification");
        $display("==================================================");

        // 1. R-Type (Opcode 6'b000000)
        opcode = 6'b000000;
        check_controls(1'b1, 1'b0, 1'b0, 1'b1, 1'b0, 1'b0, 1'b0, 1'b0, 2'b10, "R-Type (ADD/SUB/etc)");

        // 2. ADDI (Opcode 6'b001000)
        opcode = 6'b001000;
        check_controls(1'b0, 1'b1, 1'b0, 1'b1, 1'b0, 1'b0, 1'b0, 1'b0, 2'b00, "ADDI");

        // 3. LW (Opcode 6'b100011)
        opcode = 6'b100011;
        check_controls(1'b0, 1'b1, 1'b1, 1'b1, 1'b1, 1'b0, 1'b0, 1'b0, 2'b00, "LW");

        // 4. SW (Opcode 6'b101011)
        opcode = 6'b101011;
        check_controls(1'b0, 1'b1, 1'b0, 1'b0, 1'b0, 1'b1, 1'b0, 1'b0, 2'b00, "SW");

        // 5. BEQ (Opcode 6'b000100)
        opcode = 6'b000100;
        check_controls(1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b1, 1'b0, 2'b01, "BEQ");

        // 6. J (Opcode 6'b000010)
        opcode = 6'b000010;
        check_controls(1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b1, 2'b00, "J");

        // 7. Unsupported / Default (Opcode 6'b111111)
        opcode = 6'b111111;
        check_controls(1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 2'b00, "Unsupported/Default");

        $display("==================================================");
        $display("Control Unit Verification Finished");
        $display("Total Tests : %0d", test_id);
        $display("Tests Passed: %0d", tests_passed);
        $display("Tests Failed: %0d", tests_failed);
        $display("==================================================");

        if (tests_failed == 0) begin
            $display(">>> ALL CONTROL UNIT TESTS PASSED <<<");
        end else begin
            $display(">>> CONTROL UNIT VERIFICATION FAILED <<<");
            $finish(1);
        end

        $finish;
    end

endmodule
