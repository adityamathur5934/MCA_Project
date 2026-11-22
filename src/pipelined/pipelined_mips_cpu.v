// ============================================================================
// Module Name: pipelined_mips_cpu
// Description: Complete 5-Stage Pipelined 32-bit MIPS Processor Core.
//              Features:
//              - IF, ID, EX, MEM, WB Pipeline Stages
//              - Data Forwarding Unit (resolves EX and MEM hazards)
//              - Hazard Detection Unit (resolves Load-Use stalls & Branch flushes)
//              - Branch resolution in EX stage with full operand forwarding
//              - Register File write-before-read internal bypass
// ============================================================================

`timescale 1ns / 1ps

module pipelined_mips_cpu (
    input  wire        clk,
    input  wire        rst,

    // Instruction Memory Interface (Fetch Stage)
    output wire [31:0] inst_addr,
    input  wire [31:0] instruction,

    // Data Memory Interface (Memory Stage)
    output wire [31:0] mem_addr,
    output wire [31:0] mem_write_data,
    output wire        mem_read,
    output wire        mem_write,
    input  wire [31:0] mem_read_data,

    // Observability / Debug Outputs
    output wire [31:0] debug_pc,
    output wire [31:0] debug_wb_data,
    output wire [4:0]  debug_wb_reg,
    output wire        debug_wb_reg_write,
    output wire        debug_pipeline_stall,
    output wire        debug_branch_taken
);

    // ========================================================================
    // 1. INSTRUCTION FETCH (IF) STAGE
    // ========================================================================
    wire [31:0] if_pc_current;
    reg  [31:0] if_pc_next;
    wire [31:0] if_pc_plus_4;
    wire        pc_stall;
    wire        if_id_stall;
    wire        if_id_flush;
    wire        id_ex_flush;

    // Branch signals from EX stage
    wire [31:0] ex_branch_target;
    wire        ex_branch_taken;

    // Jump signals from ID stage
    wire [31:0] id_jump_target;
    wire        id_jump;

    assign if_pc_plus_4 = if_pc_current + 32'd4;
    assign inst_addr    = if_pc_current;

    // Next PC selection logic: Branch taken in EX has highest priority
    always @(*) begin
        if (ex_branch_taken)
            if_pc_next = ex_branch_target;
        else if (id_jump)
            if_pc_next = id_jump_target;
        else
            if_pc_next = if_pc_plus_4;
    end

    // Program Counter register with stall capability
    reg [31:0] pc_reg;
    always @(posedge clk or posedge rst) begin
        if (rst)
            pc_reg <= 32'h00000000;
        else if (!pc_stall)
            pc_reg <= if_pc_next;
    end
    assign if_pc_current = pc_reg;

    // ------------------------------------------------------------------------
    // IF/ID Pipeline Register
    // ------------------------------------------------------------------------
    wire [31:0] id_pc_plus_4;
    wire [31:0] id_instruction;

    pipe_if_id u_pipe_if_id (
        .clk            (clk),
        .rst            (rst),
        .stall          (if_id_stall),
        .flush          (if_id_flush),
        .if_pc_plus_4   (if_pc_plus_4),
        .if_instruction (instruction),
        .id_pc_plus_4   (id_pc_plus_4),
        .id_instruction (id_instruction)
    );

    // ========================================================================
    // 2. INSTRUCTION DECODE (ID) STAGE
    // ========================================================================
    wire [5:0]  id_opcode = id_instruction[31:26];
    wire [4:0]  id_rs     = id_instruction[25:21];
    wire [4:0]  id_rt     = id_instruction[20:16];
    wire [4:0]  id_rd     = id_instruction[15:11];
    wire [5:0]  id_funct  = id_instruction[5:0];

    // Control signals from Main Control Unit
    wire        id_reg_dst;
    wire        id_alu_src;
    wire        id_mem_to_reg;
    wire        id_reg_write;
    wire        id_mem_read;
    wire        id_mem_write;
    wire        id_branch;
    wire [1:0]  id_alu_op;

    control_unit u_control_unit (
        .opcode     (id_opcode),
        .reg_dst    (id_reg_dst),
        .alu_src    (id_alu_src),
        .mem_to_reg (id_mem_to_reg),
        .reg_write  (id_reg_write),
        .mem_read   (id_mem_read),
        .mem_write  (id_mem_write),
        .branch     (id_branch),
        .jump       (id_jump),
        .alu_op     (id_alu_op)
    );

    // Register File connections
    wire [31:0] id_rf_read1;
    wire [31:0] id_rf_read2;
    wire [31:0] wb_write_data;
    wire [4:0]  wb_write_reg;
    wire        wb_reg_write;

    register_file u_register_file (
        .clk        (clk),
        .rst        (rst),
        .reg_write  (wb_reg_write),
        .read_reg1  (id_rs),
        .read_reg2  (id_rt),
        .write_reg  (wb_write_reg),
        .write_data (wb_write_data),
        .read_data1 (id_rf_read1),
        .read_data2 (id_rf_read2)
    );

    // Sign extension
    wire [31:0] id_sign_ext_imm;
    sign_extend u_sign_extend (
        .in  (id_instruction[15:0]),
        .out (id_sign_ext_imm)
    );

    // Internal Register File WB-to-ID bypass (write-before-read in same cycle)
    wire [31:0] id_read_data1 = (wb_reg_write && (wb_write_reg != 5'd0) && (wb_write_reg == id_rs)) ?
                                 wb_write_data : id_rf_read1;
    wire [31:0] id_read_data2 = (wb_reg_write && (wb_write_reg != 5'd0) && (wb_write_reg == id_rt)) ?
                                 wb_write_data : id_rf_read2;

    // Jump target calculation
    assign id_jump_target = {id_pc_plus_4[31:28], id_instruction[25:0], 2'b00};

    // Hazard Detection Unit instance
    wire ex_mem_read;
    wire [4:0] ex_rt;

    hazard_detection_unit u_hazard_unit (
        .id_ex_mem_read  (ex_mem_read),
        .id_ex_rt        (ex_rt),
        .if_id_rs        (id_rs),
        .if_id_rt        (id_rt),
        .ex_branch_taken (ex_branch_taken),
        .id_jump         (id_jump),
        .pc_stall        (pc_stall),
        .if_id_stall     (if_id_stall),
        .if_id_flush     (if_id_flush),
        .id_ex_flush     (id_ex_flush)
    );

    // ------------------------------------------------------------------------
    // ID/EX Pipeline Register
    // ------------------------------------------------------------------------
    wire        ex_reg_dst;
    wire        ex_alu_src;
    wire        ex_mem_to_reg;
    wire        ex_reg_write;
    wire        ex_mem_write;
    wire        ex_branch;
    wire [1:0]  ex_alu_op;
    wire [31:0] ex_pc_plus_4;
    wire [31:0] ex_read_data1;
    wire [31:0] ex_read_data2;
    wire [31:0] ex_sign_ext_imm;
    wire [4:0]  ex_rs;
    wire [4:0]  ex_rd;
    wire [5:0]  ex_funct;

    pipe_id_ex u_pipe_id_ex (
        .clk            (clk),
        .rst            (rst),
        .flush          (id_ex_flush),
        .id_reg_dst     (id_reg_dst),
        .id_alu_src     (id_alu_src),
        .id_mem_to_reg  (id_mem_to_reg),
        .id_reg_write   (id_reg_write),
        .id_mem_read    (id_mem_read),
        .id_mem_write   (id_mem_write),
        .id_branch      (id_branch),
        .id_alu_op      (id_alu_op),
        .id_pc_plus_4   (id_pc_plus_4),
        .id_read_data1  (id_read_data1),
        .id_read_data2  (id_read_data2),
        .id_sign_ext_imm(id_sign_ext_imm),
        .id_rs          (id_rs),
        .id_rt          (id_rt),
        .id_rd          (id_rd),
        .id_funct       (id_funct),
        .ex_reg_dst     (ex_reg_dst),
        .ex_alu_src     (ex_alu_src),
        .ex_mem_to_reg  (ex_mem_to_reg),
        .ex_reg_write   (ex_reg_write),
        .ex_mem_read    (ex_mem_read),
        .ex_mem_write   (ex_mem_write),
        .ex_branch      (ex_branch),
        .ex_alu_op      (ex_alu_op),
        .ex_pc_plus_4   (ex_pc_plus_4),
        .ex_read_data1  (ex_read_data1),
        .ex_read_data2  (ex_read_data2),
        .ex_sign_ext_imm(ex_sign_ext_imm),
        .ex_rs          (ex_rs),
        .ex_rt          (ex_rt),
        .ex_rd          (ex_rd),
        .ex_funct       (ex_funct)
    );

    // ========================================================================
    // 3. EXECUTE (EX) STAGE
    // ========================================================================
    wire [4:0]  ex_write_reg = (ex_reg_dst) ? ex_rd : ex_rt;
    wire [3:0]  ex_alu_ctrl;

    alu_control u_alu_control (
        .alu_op   (ex_alu_op),
        .funct    (ex_funct),
        .alu_ctrl (ex_alu_ctrl)
    );

    // Forwarding Unit
    wire [1:0]  forward_a;
    wire [1:0]  forward_b;
    wire [4:0]  mem_write_reg;
    wire        mem_reg_write;
    wire [31:0] mem_alu_result;

    forwarding_unit u_forwarding_unit (
        .id_ex_rs          (ex_rs),
        .id_ex_rt          (ex_rt),
        .ex_mem_write_reg  (mem_write_reg),
        .ex_mem_reg_write  (mem_reg_write),
        .mem_wb_write_reg  (wb_write_reg),
        .mem_wb_reg_write  (wb_reg_write),
        .forward_a         (forward_a),
        .forward_b         (forward_b)
    );

    // Operand A Forwarding Mux
    reg [31:0] ex_alu_in_a;
    always @(*) begin
        case (forward_a)
            2'b10:   ex_alu_in_a = mem_alu_result; // Forwarded from EX/MEM
            2'b01:   ex_alu_in_a = wb_write_data;  // Forwarded from MEM/WB
            default: ex_alu_in_a = ex_read_data1;  // Register value
        endcase
    end

    // Operand B Forwarding Mux (pre-ALUSrc)
    reg [31:0] ex_forwarded_b;
    always @(*) begin
        case (forward_b)
            2'b10:   ex_forwarded_b = mem_alu_result;
            2'b01:   ex_forwarded_b = wb_write_data;
            default: ex_forwarded_b = ex_read_data2;
        endcase
    end

    // ALU Input B Selection: ALUSrc MUX
    wire [31:0] ex_alu_in_b = (ex_alu_src) ? ex_sign_ext_imm : ex_forwarded_b;
    wire [31:0] ex_alu_result;
    wire        ex_zero;

    alu u_alu (
        .a        (ex_alu_in_a),
        .b        (ex_alu_in_b),
        .alu_ctrl (ex_alu_ctrl),
        .result   (ex_alu_result),
        .zero     (ex_zero)
    );

    // Branch Target and Evaluation in EX stage
    assign ex_branch_target = ex_pc_plus_4 + (ex_sign_ext_imm << 2);
    assign ex_branch_taken  = ex_branch && ex_zero;

    // ------------------------------------------------------------------------
    // EX/MEM Pipeline Register
    // ------------------------------------------------------------------------
    wire        mem_mem_to_reg;
    wire        mem_mem_read;
    wire        mem_mem_write;
    wire [31:0] mem_write_data_bus;

    pipe_ex_mem u_pipe_ex_mem (
        .clk            (clk),
        .rst            (rst),
        .ex_mem_to_reg  (ex_mem_to_reg),
        .ex_reg_write   (ex_reg_write),
        .ex_mem_read    (ex_mem_read),
        .ex_mem_write   (ex_mem_write),
        .ex_alu_result  (ex_alu_result),
        .ex_write_data  (ex_forwarded_b), // for SW instructions
        .ex_write_reg   (ex_write_reg),
        .mem_mem_to_reg (mem_mem_to_reg),
        .mem_reg_write  (mem_reg_write),
        .mem_mem_read   (mem_mem_read),
        .mem_mem_write  (mem_mem_write),
        .mem_alu_result (mem_alu_result),
        .mem_write_data (mem_write_data_bus),
        .mem_write_reg  (mem_write_reg)
    );

    // ========================================================================
    // 4. MEMORY (MEM) STAGE
    // ========================================================================
    assign mem_addr       = mem_alu_result;
    assign mem_write_data = mem_write_data_bus;
    assign mem_read       = mem_mem_read;
    assign mem_write      = mem_mem_write;

    // ------------------------------------------------------------------------
    // MEM/WB Pipeline Register
    // ------------------------------------------------------------------------
    wire        wb_mem_to_reg;
    wire [31:0] wb_read_data;
    wire [31:0] wb_alu_result;

    pipe_mem_wb u_pipe_mem_wb (
        .clk            (clk),
        .rst            (rst),
        .mem_mem_to_reg (mem_mem_to_reg),
        .mem_reg_write  (mem_reg_write),
        .mem_read_data  (mem_read_data),
        .mem_alu_result (mem_alu_result),
        .mem_write_reg  (mem_write_reg),
        .wb_mem_to_reg  (wb_mem_to_reg),
        .wb_reg_write   (wb_reg_write),
        .wb_read_data   (wb_read_data),
        .wb_alu_result  (wb_alu_result),
        .wb_write_reg   (wb_write_reg)
    );

    // ========================================================================
    // 5. WRITE-BACK (WB) STAGE
    // ========================================================================
    assign wb_write_data = (wb_mem_to_reg) ? wb_read_data : wb_alu_result;

    // Debug Observability
    assign debug_pc             = if_pc_current;
    assign debug_wb_data        = wb_write_data;
    assign debug_wb_reg         = wb_write_reg;
    assign debug_wb_reg_write   = wb_reg_write;
    assign debug_pipeline_stall = pc_stall;
    assign debug_branch_taken   = ex_branch_taken;

endmodule
