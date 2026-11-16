// ============================================================================
// Module Name: instruction_memory
// Description: Word-aligned instruction memory for Single-Cycle MIPS Processor.
//              Provides combinational read output based on byte-addressed PC.
//              Supports preloading from a hex file using $readmemh.
// ============================================================================

`timescale 1ns / 1ps

module instruction_memory #(
    parameter MEM_DEPTH = 256,
    parameter MEM_FILE  = ""
)(
    input  wire [31:0] addr,
    output wire [31:0] instruction
);

    // Memory array storing 32-bit instructions (MEM_DEPTH words)
    reg [31:0] mem [0:MEM_DEPTH-1];

    integer i;
    initial begin
        // Initialize memory with NOPs (sll $zero, $zero, 0 = 32'h00000000)
        for (i = 0; i < MEM_DEPTH; i = i + 1) begin
            mem[i] = 32'h00000000;
        end
        if (MEM_FILE != "") begin
            $readmemh(MEM_FILE, mem);
        end
    end

    // Word-aligned addressing: addr[31:2] indexes the 32-bit word.
    // Address is wrapped within MEM_DEPTH words (e.g. addr[9:2] for 256 words).
    wire [$clog2(MEM_DEPTH)-1:0] word_addr;
    assign word_addr = addr[$clog2(MEM_DEPTH)+1 : 2];

    assign instruction = mem[word_addr];

endmodule
