// ============================================================================
// Module Name: alu
// Description: 32-bit Arithmetic Logic Unit (ALU) for Single-Cycle MIPS.
//              Supports ADD, SUB, AND, OR, and SLT operations.
//              Produces 32-bit result and 1-bit Zero flag.
// ============================================================================

`timescale 1ns / 1ps

module alu (
    input  wire [31:0] a,
    input  wire [31:0] b,
    input  wire [3:0]  alu_ctrl,
    output reg  [31:0] result,
    output wire        zero
);

    // ALU Operation Codes
    localparam ALU_AND = 4'b0000;
    localparam ALU_OR  = 4'b0001;
    localparam ALU_ADD = 4'b0010;
    localparam ALU_SUB = 4'b0110;
    localparam ALU_SLT = 4'b0111;

    always @(*) begin
        case (alu_ctrl)
            ALU_AND: result = a & b;
            ALU_OR:  result = a | b;
            ALU_ADD: result = a + b;
            ALU_SUB: result = a - b;
            ALU_SLT: result = ($signed(a) < $signed(b)) ? 32'd1 : 32'd0;
            default: result = 32'h00000000;
        endcase
    end

    // Zero flag generation: asserted when result equals 0
    assign zero = (result == 32'h00000000);

endmodule
