// ============================================================================
// Module Name: pipe_if_id
// Description: IF/ID Pipeline Register (Fetch to Decode Stage).
// ============================================================================

`timescale 1ns / 1ps

module pipe_if_id (
    input  wire        clk,
    input  wire        rst,
    input  wire        stall,
    input  wire        flush,
    input  wire [31:0] if_pc_plus_4,
    input  wire [31:0] if_instruction,
    output reg  [31:0] id_pc_plus_4,
    output reg  [31:0] id_instruction
);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            id_pc_plus_4    <= 32'h00000000;
            id_instruction  <= 32'h00000000; // NOP (sll $0, $0, 0)
        end else if (flush) begin
            id_pc_plus_4    <= 32'h00000000;
            id_instruction  <= 32'h00000000; // NOP bubble
        end else if (!stall) begin
            id_pc_plus_4    <= if_pc_plus_4;
            id_instruction  <= if_instruction;
        end
    end

endmodule
