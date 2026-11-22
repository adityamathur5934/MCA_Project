// ============================================================================
// Module Name: pipe_mem_wb
// Description: MEM/WB Pipeline Register (Memory to Write-Back Stage).
// ============================================================================

`timescale 1ns / 1ps

module pipe_mem_wb (
    input  wire        clk,
    input  wire        rst,

    // Control Inputs from MEM stage
    input  wire        mem_mem_to_reg,
    input  wire        mem_reg_write,

    // Data Inputs from MEM stage
    input  wire [31:0] mem_read_data,
    input  wire [31:0] mem_alu_result,
    input  wire [4:0]  mem_write_reg,

    // Control Outputs to WB stage
    output reg         wb_mem_to_reg,
    output reg         wb_reg_write,

    // Data Outputs to WB stage
    output reg  [31:0] wb_read_data,
    output reg  [31:0] wb_alu_result,
    output reg  [4:0]  wb_write_reg
);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            wb_mem_to_reg <= 1'b0;
            wb_reg_write  <= 1'b0;
            wb_read_data  <= 32'h00000000;
            wb_alu_result <= 32'h00000000;
            wb_write_reg  <= 5'd0;
        end else begin
            wb_mem_to_reg <= mem_mem_to_reg;
            wb_reg_write  <= mem_reg_write;
            wb_read_data  <= mem_read_data;
            wb_alu_result <= mem_alu_result;
            wb_write_reg  <= mem_write_reg;
        end
    end

endmodule
