// ============================================================================
// Module Name: register_file
// Description: 32x32-bit General Purpose Register File for MIPS Processor.
//              Features two combinational read ports and one synchronous write port.
//              Register $zero ($0) is hardwired to 32'h00000000.
// ============================================================================

`timescale 1ns / 1ps

module register_file (
    input  wire        clk,
    input  wire        rst,
    input  wire        reg_write,
    input  wire [4:0]  read_reg1,
    input  wire [4:0]  read_reg2,
    input  wire [4:0]  write_reg,
    input  wire [31:0] write_data,
    output wire [31:0] read_data1,
    output wire [31:0] read_data2
);

    // 32 registers of 32 bits each
    reg [31:0] registers [0:31];

    // Combinational read ports: Register 0 permanently returns 0
    assign read_data1 = (read_reg1 == 5'd0) ? 32'h00000000 : registers[read_reg1];
    assign read_data2 = (read_reg2 == 5'd0) ? 32'h00000000 : registers[read_reg2];

    integer i;
    // Synchronous write port on rising edge of clock
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < 32; i = i + 1) begin
                registers[i] <= 32'h00000000;
            end
        end else if (reg_write && (write_reg != 5'd0)) begin
            registers[write_reg] <= write_data;
        end
    end

endmodule
