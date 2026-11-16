// ============================================================================
// Module Name: program_counter
// Description: 32-bit Program Counter for Single-Cycle MIPS Processor.
//              Holds the current instruction byte address.
//              Synchronously updates to next_pc on the rising clock edge.
//              Synchronously/Asynchronously resets to 32'h00000000.
// ============================================================================

`timescale 1ns / 1ps

module program_counter (
    input  wire        clk,
    input  wire        rst,
    input  wire [31:0] next_pc,
    output reg  [31:0] pc
);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            pc <= 32'h00000000;
        end else begin
            pc <= next_pc;
        end
    end

endmodule
