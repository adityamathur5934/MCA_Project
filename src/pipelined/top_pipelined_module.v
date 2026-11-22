// ============================================================================
// Module Name: top_pipelined_module
// Description: Top-Level Integration Wrapper for 5-Stage Pipelined MIPS Core
//              with Instruction Memory (ROM) and Data Memory (RAM).
// ============================================================================

`timescale 1ns / 1ps

module top_pipelined_module #(
    parameter IMEM_FILE  = "programs/array_sum.hex",
    parameter IMEM_DEPTH = 256,
    parameter DMEM_DEPTH = 256
)(
    input  wire        clk,
    input  wire        rst,

    // Debug and Verification Ports
    output wire [31:0] pc,
    output wire [31:0] instruction,
    output wire [31:0] alu_result,
    output wire [31:0] reg_write_data,
    output wire [4:0]  write_reg,
    output wire        reg_write,
    output wire [31:0] mem_write_data,
    output wire [31:0] mem_read_data,
    output wire        mem_read,
    output wire        mem_write,
    output wire        pipeline_stall,
    output wire        branch_taken
);

    // Interconnect wires
    wire [31:0] inst_addr;
    wire [31:0] inst_data;
    wire [31:0] dmem_addr;
    wire [31:0] dmem_wdata;
    wire [31:0] dmem_rdata;
    wire        dmem_read;
    wire        dmem_write;

    // ------------------------------------------------------------------------
    // Pipelined CPU Core
    // ------------------------------------------------------------------------
    pipelined_mips_cpu u_pipelined_cpu (
        .clk                  (clk),
        .rst                  (rst),
        .inst_addr            (inst_addr),
        .instruction          (inst_data),
        .mem_addr             (dmem_addr),
        .mem_write_data       (dmem_wdata),
        .mem_read             (dmem_read),
        .mem_write            (dmem_write),
        .mem_read_data        (dmem_rdata),
        .debug_pc             (pc),
        .debug_wb_data        (reg_write_data),
        .debug_wb_reg         (write_reg),
        .debug_wb_reg_write   (reg_write),
        .debug_pipeline_stall (pipeline_stall),
        .debug_branch_taken   (branch_taken)
    );

    // ------------------------------------------------------------------------
    // Instruction Memory (ROM)
    // ------------------------------------------------------------------------
    instruction_memory #(
        .MEM_DEPTH (IMEM_DEPTH),
        .MEM_FILE  (IMEM_FILE)
    ) u_instruction_memory (
        .addr        (inst_addr),
        .instruction (inst_data)
    );

    // ------------------------------------------------------------------------
    // Data Memory (RAM)
    // ------------------------------------------------------------------------
    data_memory #(
        .MEM_DEPTH (DMEM_DEPTH)
    ) u_data_memory (
        .clk        (clk),
        .rst        (rst),
        .mem_read   (dmem_read),
        .mem_write  (dmem_write),
        .addr       (dmem_addr),
        .write_data (dmem_wdata),
        .read_data  (dmem_rdata)
    );

    // Export Observability Signals
    assign instruction    = inst_data;
    assign alu_result     = dmem_addr;
    assign mem_write_data = dmem_wdata;
    assign mem_read_data  = dmem_rdata;
    assign mem_read       = dmem_read;
    assign mem_write      = dmem_write;

endmodule
