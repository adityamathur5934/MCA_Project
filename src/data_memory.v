// ============================================================================
// Module Name: data_memory
// Description: Word-aligned Data Memory for Single-Cycle MIPS Processor.
//              Provides combinational read output on mem_read and
//              synchronous write on rising clock edge when mem_write is active.
// ============================================================================

`timescale 1ns / 1ps

module data_memory #(
    parameter MEM_DEPTH = 256
)(
    input  wire        clk,
    input  wire        rst,
    input  wire        mem_read,
    input  wire        mem_write,
    input  wire [31:0] addr,
    input  wire [31:0] write_data,
    output wire [31:0] read_data
);

    // Memory array storing 32-bit words
    reg [31:0] mem [0:MEM_DEPTH-1];

    // Word-aligned addressing: addr[31:2]
    wire [$clog2(MEM_DEPTH)-1:0] word_addr;
    assign word_addr = addr[$clog2(MEM_DEPTH)+1 : 2];

    // Combinational read port: returns memory data if mem_read is high, otherwise 0
    assign read_data = (mem_read) ? mem[word_addr] : 32'h00000000;

    integer i;
    // Synchronous write on rising clock edge
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < MEM_DEPTH; i = i + 1) begin
                mem[i] <= 32'h00000000;
            end
        end else if (mem_write) begin
            mem[word_addr] <= write_data;
        end
    end

endmodule
