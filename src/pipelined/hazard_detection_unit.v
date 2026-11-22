// ============================================================================
// Module Name: hazard_detection_unit
// Description: Hazard Detection Unit for 5-Stage Pipelined MIPS.
//              Detects Load-Use data hazards and handles branch/jump flushes.
// ============================================================================

`timescale 1ns / 1ps

module hazard_detection_unit (
    input  wire       id_ex_mem_read,
    input  wire [4:0] id_ex_rt,
    input  wire [4:0] if_id_rs,
    input  wire [4:0] if_id_rt,
    input  wire       ex_branch_taken,
    input  wire       id_jump,
    output reg        pc_stall,
    output reg        if_id_stall,
    output reg        if_id_flush,
    output reg        id_ex_flush
);

    always @(*) begin
        pc_stall    = 1'b0;
        if_id_stall = 1'b0;
        if_id_flush = 1'b0;
        id_ex_flush = 1'b0;

        // 1. Control Hazard (Branch taken in EX stage has highest priority)
        if (ex_branch_taken) begin
            if_id_flush = 1'b1;
            id_ex_flush = 1'b1;
        end
        // 2. Control Hazard (Unconditional Jump in ID stage)
        else if (id_jump) begin
            if_id_flush = 1'b1;
        end
        // 3. Load-Use Data Hazard
        else if (id_ex_mem_read && (id_ex_rt != 5'd0) &&
                 ((id_ex_rt == if_id_rs) || (id_ex_rt == if_id_rt))) begin
            pc_stall    = 1'b1;
            if_id_stall = 1'b1;
            id_ex_flush = 1'b1;
        end
    end

endmodule
