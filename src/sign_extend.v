// ============================================================================
// Module Name: sign_extend
// Description: Sign-extension unit for MIPS I-Type instructions.
//              Converts a 16-bit signed immediate to a 32-bit signed value.
// ============================================================================

`timescale 1ns / 1ps

module sign_extend (
    input  wire [15:0] in,
    output wire [31:0] out
);

    assign out = {{16{in[15]}}, in};

endmodule
