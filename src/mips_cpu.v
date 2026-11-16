// ============================================================================
// Module Name: mips_cpu
// Description: Single-Cycle 32-bit MIPS Processor Core.
//              Integrates Program Counter, Register File, ALU, ALU Control,
//              Sign Extension, Main Control Unit, and Branch/Jump Multiplexers.
// ============================================================================

`timescale 1ns / 1ps

module mips_cpu (
    input  wire        clk,
    input  wire        rst,

    // Instruction Memory Interface
    output wire [31:0] inst_addr,
    input  wire [31:0] instruction,

    // Data Memory Interface
    output wire [31:0] mem_addr,
    output wire [31:0] mem_write_data,
    output wire        mem_read,
    output wire        mem_write,
    input  wire [31:0] mem_read_data,

    // Debug / Observability Outputs
    output wire [31:0] debug_pc,
    output wire [31:0] debug_alu_result,
    output wire [31:0] debug_reg_write_data,
    output wire [4:0]  debug_write_reg,
    output wire        debug_reg_write,
    output wire        debug_zero,
    output wire        debug_branch,
    output wire        debug_jump
);

    // ------------------------------------------------------------------------
    // Internal Wires and Buses
    // ------------------------------------------------------------------------
    wire [31:0] pc_current;
    wire [31:0] pc_next;
    wire [31:0] pc_plus_4;
    wire [31:0] branch_target;
    wire [31:0] jump_target;
    wire [31:0] pc_branch_mux;

    // Control signals
    wire        reg_dst;
    wire        alu_src;
    wire        mem_to_reg;
    wire        reg_write;
    wire        branch;
    wire        jump;
    wire [1:0]  alu_op;
    wire [3:0]  alu_ctrl;

    // Register File signals
    wire [4:0]  write_reg;
    wire [31:0] reg_write_data;
    wire [31:0] reg_read_data1;
    wire [31:0] reg_read_data2;

    // ALU and Immediate signals
    wire [31:0] sign_ext_imm;
    wire [31:0] alu_operand_b;
    wire [31:0] alu_result;
    wire        zero;
    wire        branch_taken;

    // ------------------------------------------------------------------------
    // Program Counter (PC) and Next-PC Logic
    // ------------------------------------------------------------------------
    program_counter u_pc (
        .clk     (clk),
        .rst     (rst),
        .next_pc (pc_next),
        .pc      (pc_current)
    );

    // Sequential PC increment (word alignment: +4 bytes)
    assign pc_plus_4 = pc_current + 32'd4;

    // Sign extension of 16-bit immediate field (inst[15:0])
    sign_extend u_sign_extend (
        .in  (instruction[15:0]),
        .out (sign_ext_imm)
    );

    // Branch Target = (PC + 4) + (SignExtImm << 2)
    assign branch_target = pc_plus_4 + (sign_ext_imm << 2);

    // Jump Target = { (PC + 4)[31:28], instruction[25:0], 2'b00 }
    assign jump_target = {pc_plus_4[31:28], instruction[25:0], 2'b00};

    // Branch condition: BEQ branches when branch control is high and ALU zero flag is set
    assign branch_taken = branch & zero;

    // PC multiplexers: branch decision followed by jump decision
    assign pc_branch_mux = (branch_taken) ? branch_target : pc_plus_4;
    assign pc_next       = (jump)         ? jump_target   : pc_branch_mux;

    // Instruction address to external Instruction Memory
    assign inst_addr = pc_current;

    // ------------------------------------------------------------------------
    // Control Unit
    // ------------------------------------------------------------------------
    control_unit u_control_unit (
        .opcode     (instruction[31:26]),
        .reg_dst    (reg_dst),
        .alu_src    (alu_src),
        .mem_to_reg (mem_to_reg),
        .reg_write  (reg_write),
        .mem_read   (mem_read),
        .mem_write  (mem_write),
        .branch     (branch),
        .jump       (jump),
        .alu_op     (alu_op)
    );

    // ------------------------------------------------------------------------
    // Register File and Write-Back Logic
    // ------------------------------------------------------------------------
    // RegDst MUX: 0 -> rt (inst[20:16]), 1 -> rd (inst[15:11])
    assign write_reg = (reg_dst) ? instruction[15:11] : instruction[20:16];

    // MemtoReg MUX: 0 -> ALU Result, 1 -> Data Memory read_data
    assign reg_write_data = (mem_to_reg) ? mem_read_data : alu_result;

    register_file u_register_file (
        .clk        (clk),
        .rst        (rst),
        .reg_write  (reg_write),
        .read_reg1  (instruction[25:21]), // rs
        .read_reg2  (instruction[20:16]), // rt
        .write_reg  (write_reg),
        .write_data (reg_write_data),
        .read_data1 (reg_read_data1),
        .read_data2 (reg_read_data2)
    );

    // ------------------------------------------------------------------------
    // ALU and ALU Control
    // ------------------------------------------------------------------------
    alu_control u_alu_control (
        .alu_op   (alu_op),
        .funct    (instruction[5:0]),
        .alu_ctrl (alu_ctrl)
    );

    // ALUSrc MUX: 0 -> Read Data 2, 1 -> Sign Extended Immediate
    assign alu_operand_b = (alu_src) ? sign_ext_imm : reg_read_data2;

    alu u_alu (
        .a        (reg_read_data1),
        .b        (alu_operand_b),
        .alu_ctrl (alu_ctrl),
        .result   (alu_result),
        .zero     (zero)
    );

    // ------------------------------------------------------------------------
    // Data Memory Interface Connections
    // ------------------------------------------------------------------------
    assign mem_addr       = alu_result;
    assign mem_write_data = reg_read_data2;

    // ------------------------------------------------------------------------
    // Debug & Observability Outputs
    // ------------------------------------------------------------------------
    assign debug_pc             = pc_current;
    assign debug_alu_result     = alu_result;
    assign debug_reg_write_data = reg_write_data;
    assign debug_write_reg      = write_reg;
    assign debug_reg_write      = reg_write;
    assign debug_zero           = zero;
    assign debug_branch         = branch;
    assign debug_jump           = jump;

endmodule
