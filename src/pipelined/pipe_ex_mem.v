// ============================================================================
// Module Name: pipe_ex_mem
// Description: EX/MEM Pipeline Register (Execute to Memory Stage).
// ============================================================================

`timescale 1ns / 1ps

module pipe_ex_mem (
    input  wire        clk,
    input  wire        rst,

    // Control Inputs from EX stage
    input  wire        ex_mem_to_reg,
    input  wire        ex_reg_write,
    input  wire        ex_mem_read,
    input  wire        ex_mem_write,

    // Data Inputs from EX stage
    input  wire [31:0] ex_alu_result,
    input  wire [31:0] ex_write_data,
    input  wire [4:0]  ex_write_reg,

    // Control Outputs to MEM stage
    output reg         mem_mem_to_reg,
    output reg         mem_reg_write,
    output reg         mem_mem_read,
    output reg         mem_mem_write,

    // Data Outputs to MEM stage
    output reg  [31:0] mem_alu_result,
    output reg  [31:0] mem_write_data,
    output reg  [4:0]  mem_write_reg
);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            mem_mem_to_reg <= 1'b0;
            mem_reg_write  <= 1'b0;
            mem_mem_read   <= 1'b0;
            mem_mem_write  <= 1'b0;
            mem_alu_result <= 32'h00000000;
            mem_write_data <= 32'h00000000;
            mem_write_reg  <= 5'd0;
        end else begin
            mem_mem_to_reg <= ex_mem_to_reg;
            mem_reg_write  <= ex_reg_write;
            mem_mem_read   <= ex_mem_read;
            mem_mem_write  <= ex_mem_write;
            mem_alu_result <= ex_alu_result;
            mem_write_data <= ex_write_data;
            mem_write_reg  <= ex_write_reg;
        end
    end

endmodule
