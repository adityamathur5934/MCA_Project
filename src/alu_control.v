// ============================================================================
// Module Name: alu_control
// Description: ALU Control Decoder for Single-Cycle MIPS.
//              Combines 2-bit ALUOp from Main Control Unit and 6-bit funct
//              field from instruction to generate 4-bit ALU control code.
// ============================================================================

`timescale 1ns / 1ps

module alu_control (
    input  wire [1:0] alu_op,
    input  wire [5:0] funct,
    output reg  [3:0] alu_ctrl
);

    // ALU Operation Codes
    localparam ALU_AND = 4'b0000;
    localparam ALU_OR  = 4'b0001;
    localparam ALU_ADD = 4'b0010;
    localparam ALU_SUB = 4'b0110;
    localparam ALU_SLT = 4'b0111;

    // MIPS R-Type Function Codes
    localparam FUNCT_ADD = 6'b100000; // 0x20
    localparam FUNCT_SUB = 6'b100010; // 0x22
    localparam FUNCT_AND = 6'b100100; // 0x24
    localparam FUNCT_OR  = 6'b100101; // 0x25
    localparam FUNCT_SLT = 6'b101010; // 0x2A

    always @(*) begin
        case (alu_op)
            2'b00: alu_ctrl = ALU_ADD; // LW, SW, ADDI
            2'b01: alu_ctrl = ALU_SUB; // BEQ
            2'b10: begin // R-Type instructions
                case (funct)
                    FUNCT_ADD: alu_ctrl = ALU_ADD;
                    FUNCT_SUB: alu_ctrl = ALU_SUB;
                    FUNCT_AND: alu_ctrl = ALU_AND;
                    FUNCT_OR:  alu_ctrl = ALU_OR;
                    FUNCT_SLT: alu_ctrl = ALU_SLT;
                    default:   alu_ctrl = ALU_ADD;
                endcase
            end
            default: alu_ctrl = ALU_ADD;
        endcase
    end

endmodule
