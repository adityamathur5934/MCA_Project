// ============================================================================
// Module Name: pipe_id_ex
// Description: ID/EX Pipeline Register (Decode to Execute Stage).
// ============================================================================

`timescale 1ns / 1ps

module pipe_id_ex (
    input  wire        clk,
    input  wire        rst,
    input  wire        flush,

    // Control Inputs from ID stage
    input  wire        id_reg_dst,
    input  wire        id_alu_src,
    input  wire        id_mem_to_reg,
    input  wire        id_reg_write,
    input  wire        id_mem_read,
    input  wire        id_mem_write,
    input  wire        id_branch,
    input  wire [1:0]  id_alu_op,

    // Data Inputs from ID stage
    input  wire [31:0] id_pc_plus_4,
    input  wire [31:0] id_read_data1,
    input  wire [31:0] id_read_data2,
    input  wire [31:0] id_sign_ext_imm,
    input  wire [4:0]  id_rs,
    input  wire [4:0]  id_rt,
    input  wire [4:0]  id_rd,
    input  wire [5:0]  id_funct,

    // Control Outputs to EX stage
    output reg         ex_reg_dst,
    output reg         ex_alu_src,
    output reg         ex_mem_to_reg,
    output reg         ex_reg_write,
    output reg         ex_mem_read,
    output reg         ex_mem_write,
    output reg         ex_branch,
    output reg  [1:0]  ex_alu_op,

    // Data Outputs to EX stage
    output reg  [31:0] ex_pc_plus_4,
    output reg  [31:0] ex_read_data1,
    output reg  [31:0] ex_read_data2,
    output reg  [31:0] ex_sign_ext_imm,
    output reg  [4:0]  ex_rs,
    output reg  [4:0]  ex_rt,
    output reg  [4:0]  ex_rd,
    output reg  [5:0]  ex_funct
);

    always @(posedge clk or posedge rst) begin
        if (rst || flush) begin
            ex_reg_dst      <= 1'b0;
            ex_alu_src      <= 1'b0;
            ex_mem_to_reg   <= 1'b0;
            ex_reg_write    <= 1'b0;
            ex_mem_read     <= 1'b0;
            ex_mem_write    <= 1'b0;
            ex_branch       <= 1'b0;
            ex_alu_op       <= 2'b00;
            ex_pc_plus_4    <= 32'h00000000;
            ex_read_data1   <= 32'h00000000;
            ex_read_data2   <= 32'h00000000;
            ex_sign_ext_imm <= 32'h00000000;
            ex_rs           <= 5'd0;
            ex_rt           <= 5'd0;
            ex_rd           <= 5'd0;
            ex_funct        <= 6'd0;
        end else begin
            ex_reg_dst      <= id_reg_dst;
            ex_alu_src      <= id_alu_src;
            ex_mem_to_reg   <= id_mem_to_reg;
            ex_reg_write    <= id_reg_write;
            ex_mem_read     <= id_mem_read;
            ex_mem_write    <= id_mem_write;
            ex_branch       <= id_branch;
            ex_alu_op       <= id_alu_op;
            ex_pc_plus_4    <= id_pc_plus_4;
            ex_read_data1   <= id_read_data1;
            ex_read_data2   <= id_read_data2;
            ex_sign_ext_imm <= id_sign_ext_imm;
            ex_rs           <= id_rs;
            ex_rt           <= id_rt;
            ex_rd           <= id_rd;
            ex_funct        <= id_funct;
        end
    end

endmodule
