// ============================================================================
// Module Name: forwarding_unit
// Description: Data Forwarding / Bypassing Unit for 5-Stage Pipelined MIPS.
//              Resolves RAW (Read-After-Write) data hazards from EX/MEM and
//              MEM/WB stages to the EX stage ALU inputs without stalling.
// ============================================================================

`timescale 1ns / 1ps

module forwarding_unit (
    input  wire [4:0] id_ex_rs,
    input  wire [4:0] id_ex_rt,
    input  wire [4:0] ex_mem_write_reg,
    input  wire       ex_mem_reg_write,
    input  wire [4:0] mem_wb_write_reg,
    input  wire       mem_wb_reg_write,
    output reg  [1:0] forward_a,
    output reg  [1:0] forward_b
);

    // Forwarding codes:
    // 2'b00: No forwarding (use operand from ID/EX pipeline register)
    // 2'b10: Forward from EX/MEM pipeline register (prior instruction)
    // 2'b01: Forward from MEM/WB pipeline register (two instructions prior)

    always @(*) begin
        // Forward A logic (ALU input A: rs operand)
        if (ex_mem_reg_write && (ex_mem_write_reg != 5'd0) && (ex_mem_write_reg == id_ex_rs)) begin
            forward_a = 2'b10;
        end else if (mem_wb_reg_write && (mem_wb_write_reg != 5'd0) && (mem_wb_write_reg == id_ex_rs)) begin
            forward_a = 2'b01;
        end else begin
            forward_a = 2'b00;
        end

        // Forward B logic (ALU input B: rt operand)
        if (ex_mem_reg_write && (ex_mem_write_reg != 5'd0) && (ex_mem_write_reg == id_ex_rt)) begin
            forward_b = 2'b10;
        end else if (mem_wb_reg_write && (mem_wb_write_reg != 5'd0) && (mem_wb_write_reg == id_ex_rt)) begin
            forward_b = 2'b01;
        end else begin
            forward_b = 2'b00;
        end
    end

endmodule
