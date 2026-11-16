// ============================================================================
// Module Name: control_unit
// Description: Main Control Unit for Single-Cycle MIPS Processor.
//              Decodes the 6-bit instruction opcode and generates all major
//              datapath and memory control signals.
// ============================================================================

`timescale 1ns / 1ps

module control_unit (
    input  wire [5:0] opcode,
    output reg        reg_dst,
    output reg        alu_src,
    output reg        mem_to_reg,
    output reg        reg_write,
    output reg        mem_read,
    output reg        mem_write,
    output reg        branch,
    output reg        jump,
    output reg  [1:0] alu_op
);

    // MIPS Opcode definitions
    localparam OP_R_TYPE = 6'b000000; // 0x00: R-Type instructions (ADD, SUB, AND, OR, SLT)
    localparam OP_ADDI   = 6'b001000; // 0x08: Add Immediate
    localparam OP_LW     = 6'b100011; // 0x23: Load Word
    localparam OP_SW     = 6'b101011; // 0x2B: Store Word
    localparam OP_BEQ    = 6'b000100; // 0x04: Branch on Equal
    localparam OP_J      = 6'b000010; // 0x02: Jump

    always @(*) begin
        // Safe default values: all control signals deasserted
        reg_dst    = 1'b0;
        alu_src    = 1'b0;
        mem_to_reg = 1'b0;
        reg_write  = 1'b0;
        mem_read   = 1'b0;
        mem_write  = 1'b0;
        branch     = 1'b0;
        jump       = 1'b0;
        alu_op     = 2'b00;

        case (opcode)
            OP_R_TYPE: begin
                reg_dst    = 1'b1; // Destination register is rd
                alu_src    = 1'b0; // Second ALU operand is rt register
                mem_to_reg = 1'b0; // Write ALU result back to register
                reg_write  = 1'b1; // Write to register file
                mem_read   = 1'b0;
                mem_write  = 1'b0;
                branch     = 1'b0;
                jump       = 1'b0;
                alu_op     = 2'b10; // Function field determines operation
            end

            OP_ADDI: begin
                reg_dst    = 1'b0; // Destination register is rt
                alu_src    = 1'b1; // Second ALU operand is sign-extended immediate
                mem_to_reg = 1'b0; // Write ALU result back to register
                reg_write  = 1'b1; // Write to register file
                mem_read   = 1'b0;
                mem_write  = 1'b0;
                branch     = 1'b0;
                jump       = 1'b0;
                alu_op     = 2'b00; // Addition
            end

            OP_LW: begin
                reg_dst    = 1'b0; // Destination register is rt
                alu_src    = 1'b1; // Second ALU operand is sign-extended immediate
                mem_to_reg = 1'b1; // Write Data Memory read_data back to register
                reg_write  = 1'b1; // Write to register file
                mem_read   = 1'b1; // Read from Data Memory
                mem_write  = 1'b0;
                branch     = 1'b0;
                jump       = 1'b0;
                alu_op     = 2'b00; // Address calculation (Base + Offset)
            end

            OP_SW: begin
                reg_dst    = 1'b0; // Don't care
                alu_src    = 1'b1; // Second ALU operand is sign-extended immediate
                mem_to_reg = 1'b0; // Don't care
                reg_write  = 1'b0; // No register write
                mem_read   = 1'b0;
                mem_write  = 1'b1; // Write to Data Memory
                branch     = 1'b0;
                jump       = 1'b0;
                alu_op     = 2'b00; // Address calculation (Base + Offset)
            end

            OP_BEQ: begin
                reg_dst    = 1'b0; // Don't care
                alu_src    = 1'b0; // Second ALU operand is rt register
                mem_to_reg = 1'b0; // Don't care
                reg_write  = 1'b0; // No register write
                mem_read   = 1'b0;
                mem_write  = 1'b0;
                branch     = 1'b1; // Branch enabled
                jump       = 1'b0;
                alu_op     = 2'b01; // Subtraction for equality comparison
            end

            OP_J: begin
                reg_dst    = 1'b0; // Don't care
                alu_src    = 1'b0; // Don't care
                mem_to_reg = 1'b0; // Don't care
                reg_write  = 1'b0; // No register write
                mem_read   = 1'b0;
                mem_write  = 1'b0;
                branch     = 1'b0;
                jump       = 1'b1; // Unconditional jump
                alu_op     = 2'b00;
            end

            default: begin
                // All signals remain 0 (safe default / NOP)
                reg_dst    = 1'b0;
                alu_src    = 1'b0;
                mem_to_reg = 1'b0;
                reg_write  = 1'b0;
                mem_read   = 1'b0;
                mem_write  = 1'b0;
                branch     = 1'b0;
                jump       = 1'b0;
                alu_op     = 2'b00;
            end
        endcase
    end

endmodule
