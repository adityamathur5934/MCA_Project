// ============================================================================
// Module Name: top_module
// Description: Top-level integration module for Single-Cycle MIPS Processor
//              with Memory Interface.
//              Integrates MIPS CPU Core, Instruction Memory, and Data Memory.
//              Exposes status and debug signals for simulation and verification.
// ============================================================================

`timescale 1ns / 1ps

module top_module #(
    parameter IMEM_DEPTH = 256,
    parameter DMEM_DEPTH = 256,
    parameter IMEM_FILE  = ""
)(
    input  wire        clk,
    input  wire        rst,

    // Observability and Debug Outputs
    output wire [31:0] pc,
    output wire [31:0] instruction,
    output wire [31:0] alu_result,
    output wire [31:0] mem_write_data,
    output wire [31:0] mem_read_data,
    output wire [31:0] reg_write_data,
    output wire [4:0]  write_reg,
    output wire        reg_write,
    output wire        mem_read,
    output wire        mem_write,
    output wire        zero,
    output wire        branch,
    output wire        jump
);

    // ------------------------------------------------------------------------
    // Internal Interconnects
    // ------------------------------------------------------------------------
    wire [31:0] inst_addr;
    wire [31:0] inst_data;
    wire [31:0] dmem_addr;
    wire [31:0] dmem_wdata;
    wire [31:0] dmem_rdata;
    wire        dmem_read;
    wire        dmem_write;

    // ------------------------------------------------------------------------
    // Instruction Memory Instantiation
    // ------------------------------------------------------------------------
    instruction_memory #(
        .MEM_DEPTH (IMEM_DEPTH),
        .MEM_FILE  (IMEM_FILE)
    ) u_instruction_memory (
        .addr        (inst_addr),
        .instruction (inst_data)
    );

    // ------------------------------------------------------------------------
    // Data Memory Instantiation
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

    // ------------------------------------------------------------------------
    // MIPS CPU Core Instantiation
    // ------------------------------------------------------------------------
    mips_cpu u_mips_cpu (
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
        .debug_alu_result     (alu_result),
        .debug_reg_write_data (reg_write_data),
        .debug_write_reg      (write_reg),
        .debug_reg_write      (reg_write),
        .debug_zero           (zero),
        .debug_branch         (branch),
        .debug_jump           (jump)
    );

    // ------------------------------------------------------------------------
    // Output Assignments
    // ------------------------------------------------------------------------
    assign instruction    = inst_data;
    assign mem_write_data = dmem_wdata;
    assign mem_read_data  = dmem_rdata;
    assign mem_read       = dmem_read;
    assign mem_write      = dmem_write;

endmodule
