#!/usr/bin/env python3
"""
Generate a comprehensive 14-slide PowerPoint presentation (.pptx)
for the Final Phase of the Single-Cycle and 5-Stage Pipelined MIPS Processor project.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette: Professional Engineering Theme
DARK_BLUE = RGBColor(26, 54, 93)      # #1A365D
MED_BLUE  = RGBColor(43, 108, 176)    # #2B6CB0
LIGHT_BG  = RGBColor(247, 250, 252)   # #F7FAFC
TEXT_DARK = RGBColor(45, 55, 72)      # #2D3748
TEXT_MUTED= RGBColor(113, 128, 150)   # #718096
CORAL     = RGBColor(229, 62, 62)     # #E53E3E
WHITE     = RGBColor(255, 255, 255)
GREEN     = RGBColor(56, 161, 105)    # #38A169

blank_slide_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="FINAL PHASE DEFENSE & COMPREHENSIVE EVALUATION"):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = CORAL

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

def add_card(slide, left, top, width, height, title, points, bg_color=WHITE, border_color=MED_BLUE):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)

    if title:
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.bold = True
        p_title.font.size = Pt(15)
        p_title.font.color.rgb = DARK_BLUE
        p_title.space_after = Pt(8)

    for pt in points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

# -----------------------------------------------------------------------------
# SLIDE 1: Title & Team Members
# -----------------------------------------------------------------------------
slide1 = prs.slides.add_slide(blank_slide_layout)
bg1 = slide1.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = DARK_BLUE
bg1.line.color.rgb = DARK_BLUE

title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.2))
tf1 = title_box.text_frame
tf1.word_wrap = True
p1 = tf1.paragraphs[0]
p1.text = "SINGLE-CYCLE & 5-STAGE PIPELINED\nMIPS PROCESSOR WITH MEMORY INTERFACE"
p1.font.size = Pt(32)
p1.font.bold = True
p1.font.color.rgb = WHITE
p1.alignment = PP_ALIGN.CENTER

p1_sub = tf1.add_paragraph()
p1_sub.text = "Final Project Defense: Hardware Implementation, Hazard Resolution & Verification"
p1_sub.font.size = Pt(16)
p1_sub.font.color.rgb = RGBColor(190, 227, 248)
p1_sub.alignment = PP_ALIGN.CENTER
p1_sub.space_before = Pt(10)

members_box = slide1.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(11.333), Inches(2.5))
tf_m = members_box.text_frame
tf_m.word_wrap = True
p_team_hdr = tf_m.paragraphs[0]
p_team_hdr.text = "PROJECT TEAM (5 MEMBERS)"
p_team_hdr.font.size = Pt(13)
p_team_hdr.font.bold = True
p_team_hdr.font.color.rgb = CORAL
p_team_hdr.alignment = PP_ALIGN.CENTER
p_team_hdr.space_after = Pt(12)

team_members = [
    "Member 1: CPU Architecture & Integration Lead",
    "Member 2: ALU & Register File Specialist",
    "Member 3: Control Unit & Hazard Detection Specialist",
    "Member 4: Memory Subsystem & Verification Lead",
    "Member 5: Technical Documentation & Production Lead"
]
for m in team_members:
    p = tf_m.add_paragraph()
    p.text = m
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(4)

# -----------------------------------------------------------------------------
# SLIDE 2: Project Motivation & Scope Evolution
# -----------------------------------------------------------------------------
slide2 = prs.slides.add_slide(blank_slide_layout)
add_header(slide2, "Project Evolution: Phase I Baseline to Final Phase Pipelining")
add_card(slide2, 0.8, 1.8, 5.6, 5.0, "Phase I Baseline: Single-Cycle MIPS", [
    "Pure single-cycle execution: CPI = 1.0",
    "Word-aligned Harvard Memory: IMEM ROM & DMEM RAM",
    "Core 10-instruction MIPS ISA implemented and validated",
    "Critical Path limitation: T_clk bounded by cumulative sum of all stages",
    "Baseline verified with 57 passed assertions and 3 benchmarks"
])
add_card(slide2, 6.8, 1.8, 5.7, 5.0, "Final Phase: 5-Stage Pipelined Architecture", [
    "Balanced 5-stage classic pipeline: IF, ID, EX, MEM, WB",
    "Data Forwarding Unit resolves RAW hazards with zero stall penalty",
    "Hazard Detection Unit manages Load-Use stalls and Branch flushes",
    "Clock frequency scaled from ~55 MHz to ~185 MHz (Artix-7 FPGA)",
    "Comprehensive benchmark suite expanded to 5 programs (100% PASS)"
], bg_color=RGBColor(240, 249, 255), border_color=CORAL)

# -----------------------------------------------------------------------------
# SLIDE 3: System Architecture & Harvard Memory Subsystem
# -----------------------------------------------------------------------------
slide3 = prs.slides.add_slide(blank_slide_layout)
add_header(slide3, "System Architecture & Memory Subsystem")
add_card(slide3, 0.8, 1.8, 5.6, 5.0, "Harvard Memory Architecture", [
    "Separate Instruction Memory (ROM) and Data Memory (RAM)",
    "Completely eliminates structural memory conflicts during pipelining",
    "Word-Aligned Addressing: uses address bits [9:2] for word indexing",
    "IMEM: 256 words (1024 bytes) combinational read, hex-loadable",
    "DMEM: 256 words (1024 bytes) combinational read, synchronous edge write"
])
add_card(slide3, 6.8, 1.8, 5.7, 5.0, "Top-Level System Interconnect", [
    "Clean top-level wrapper module: top_pipelined_module.v",
    "Direct bus interfaces for inst_addr, instruction, dmem_addr, write_data",
    "Comprehensive debug bus exposing PC, ALU result, Writeback data, and Stalls",
    "Zero bus contention and clean synchronous reset propagation across all blocks"
])

# -----------------------------------------------------------------------------
# SLIDE 4: Single-Cycle Baseline Architecture
# -----------------------------------------------------------------------------
slide4 = prs.slides.add_slide(blank_slide_layout)
add_header(slide4, "Baseline Single-Cycle Microarchitecture")
add_card(slide4, 0.8, 1.8, 5.6, 5.0, "Core Datapath Components", [
    "Program Counter: 32-bit register with synchronous/asynchronous reset",
    "32x32-bit Register File: 2 combinational read ports, 1 clocked write port",
    "$zero ($0) hardwired to 0; hardware write protection prevents corruption",
    "32-bit ALU: Arithmetic (ADD, SUB), Logical (AND, OR), Comparison (SLT)",
    "Branch / Jump logic: Branch Target = PC+4 + (Imm<<2); Jump = {PC+4[31:28], T<<2}"
])
add_card(slide4, 6.8, 1.8, 5.7, 5.0, "Timing & Bottleneck Analysis", [
    "Every instruction executes in exactly one long clock cycle",
    "T_cycle = T_pc + T_imem + T_rf_read + T_alu + T_dmem + T_mux + T_setup",
    "Estimated critical path: ~18.1 ns -> Maximum F_clk = ~55 MHz",
    "Load Word (LW) dictates the clock period, leaving other instructions underutilized",
    "Motivates the transition to a pipelined datapath for high throughput"
])

# -----------------------------------------------------------------------------
# SLIDE 5: 5-Stage Classic Pipeline Architecture
# -----------------------------------------------------------------------------
slide5 = prs.slides.add_slide(blank_slide_layout)
add_header(slide5, "5-Stage Pipelined Datapath (IF, ID, EX, MEM, WB)")
add_card(slide5, 0.8, 1.8, 3.7, 5.0, "IF & ID Stages", [
    "IF: Program Counter & IMEM fetch",
    "IF/ID Register: buffers PC+4 & inst",
    "ID: Control decode, RF read, SignExt",
    "ID-to-WB internal bypass for RF reads",
    "Jump target calculated in ID stage"
])
add_card(slide5, 4.8, 1.8, 3.7, 5.0, "EX Stage", [
    "ID/EX Register: buffers controls & data",
    "Forwarding Unit MUXes on ALU inputs",
    "ALU Control derives 4-bit ALU code",
    "32-bit ALU computes result & Zero flag",
    "Branch target and condition resolved in EX"
], bg_color=RGBColor(255, 245, 245), border_color=CORAL)
add_card(slide5, 8.8, 1.8, 3.7, 5.0, "MEM & WB Stages", [
    "EX/MEM Register: buffers addr & data",
    "MEM: Data Memory synchronous write / read",
    "MEM/WB Register: buffers dmem data & alu",
    "WB: MemtoReg multiplexer selects writeback",
    "Synchronous write back to Register File"
])

# -----------------------------------------------------------------------------
# SLIDE 6: Forwarding Unit: Resolving RAW Data Hazards
# -----------------------------------------------------------------------------
slide6 = prs.slides.add_slide(blank_slide_layout)
add_header(slide6, "Forwarding Unit: Zero-Stall RAW Hazard Resolution")
add_card(slide6, 0.8, 1.8, 5.6, 5.0, "Hazard Condition & Forwarding Logic", [
    "RAW Hazard occurs when instruction uses register written by recent instruction",
    "EX Hazard: Forward from EX/MEM if ex_mem_reg_write & (ex_mem_rd == id_ex_rs/rt)",
    "MEM Hazard: Forward from MEM/WB if mem_wb_reg_write & (mem_wb_rd == id_ex_rs/rt)",
    "ForwardA & ForwardB 2-bit multiplexer controls select forwarded operands",
    "Result: Back-to-back arithmetic instructions execute without any stall cycles!"
])
add_card(slide6, 6.8, 1.8, 5.7, 5.0, "Experimental Verification Example", [
    "ADDI $t1, $0, 10  (writes to $t1 in WB)",
    "ADD  $t2, $t1, $t1 (requires $t1 in EX stage)",
    "-> Forwarding Unit detects EX Hazard, bypasses ALU result directly to ALU input A & B",
    "-> $t2 computed as 20 with ZERO stall penalty!",
    "ADD  $t3, $t1, $t2 (requires both MEM and EX forwarding)",
    "-> $t3 computed as 30 seamlessly!"
], bg_color=RGBColor(240, 255, 244), border_color=GREEN)

# -----------------------------------------------------------------------------
# SLIDE 7: Hazard Detection Unit: Load-Use Stalls & Branch Flushes
# -----------------------------------------------------------------------------
slide7 = prs.slides.add_slide(blank_slide_layout)
add_header(slide7, "Hazard Detection Unit: Stalls & Flushes")
add_card(slide7, 0.8, 1.8, 5.6, 5.0, "Load-Use Data Hazard Resolution", [
    "Occurs when instruction immediately follows LW and consumes loaded register",
    "Data not available until end of MEM stage -> Forwarding alone cannot solve this",
    "Hazard Unit condition: id_ex_mem_read & ((id_ex_rt == if_id_rs) | (id_ex_rt == if_id_rt))",
    "Action: Freeze PC (pc_stall = 1), Freeze IF/ID (if_id_stall = 1)",
    "Insert 1-cycle bubble into ID/EX (id_ex_flush = 1) -> 1 stall cycle penalty"
])
add_card(slide7, 6.8, 1.8, 5.7, 5.0, "Control Hazard (Branch & Jump) Handling", [
    "Branches evaluated in EX stage using forwarded operands",
    "When Branch is TAKEN (ex_branch & ex_zero):",
    "-> Target address updates PC; IF/ID and ID/EX registers are FLUSHED (bubble inserted)",
    "-> Guarantees mispredicted instructions never commit state or alter memory",
    "Unconditional Jump: Resolved in ID stage; flushes 1 instruction in IF/ID"
])

# -----------------------------------------------------------------------------
# SLIDE 8: Instruction Set Architecture & Control Decoding Matrix
# -----------------------------------------------------------------------------
slide8 = prs.slides.add_slide(blank_slide_layout)
add_header(slide8, "Instruction Set & Control Decoding Matrix")
add_card(slide8, 0.8, 1.8, 11.7, 5.0, "Main Control Truth Table", [
    "R-Type (0x00): RegDst=1, ALUSrc=0, MemtoReg=0, RegWrite=1, MemRead=0, MemWrite=0, Branch=0, Jump=0, ALUOp=2'b10",
    "ADDI   (0x08): RegDst=0, ALUSrc=1, MemtoReg=0, RegWrite=1, MemRead=0, MemWrite=0, Branch=0, Jump=0, ALUOp=2'b00",
    "LW     (0x23): RegDst=0, ALUSrc=1, MemtoReg=1, RegWrite=1, MemRead=1, MemWrite=0, Branch=0, Jump=0, ALUOp=2'b00",
    "SW     (0x2B): RegDst=X, ALUSrc=1, MemtoReg=X, RegWrite=0, MemRead=0, MemWrite=1, Branch=0, Jump=0, ALUOp=2'b00",
    "BEQ    (0x04): RegDst=X, ALUSrc=0, MemtoReg=X, RegWrite=0, MemRead=0, MemWrite=0, Branch=1, Jump=0, ALUOp=2'b01",
    "J      (0x02): RegDst=X, ALUSrc=X, MemtoReg=X, RegWrite=0, MemRead=0, MemWrite=0, Branch=0, Jump=1, ALUOp=2'b00",
    "Default Fallback: Safe deassertion of all control lines ensures robust undefined-opcode handling"
])

# -----------------------------------------------------------------------------
# SLIDE 9: Comprehensive Simulation Methodology
# -----------------------------------------------------------------------------
slide9 = prs.slides.add_slide(blank_slide_layout)
add_header(slide9, "Verification Methodology & Self-Checking Framework")
add_card(slide9, 0.8, 1.8, 5.6, 5.0, "Layered Verification Strategy", [
    "Unit Testbenches: tb_alu (16/16), tb_control_unit (7/7), tb_register_file (5/5), tb_data_memory (5/5)",
    "System Integration Testbenches: tb_mips_cpu (24/24), tb_pipelined_mips (21/21)",
    "Total Assertions: 78 Executed, 78 Passed, 0 Failed (100% Pass Rate)",
    "Self-checking automated tasks flag failures with expected vs observed values",
    "Icarus Verilog v13.0 + VVP runtime + GTKWave waveform visualization"
])
add_card(slide9, 6.8, 1.8, 5.7, 5.0, "Corner-Case Coverage", [
    "Register $zero write protection: Writes to $0 permanently ignored",
    "Signed comparison in SLT: Verified with negative and positive values",
    "Consecutive RAW hazards: Simultaneous EX-to-EX and MEM-to-EX forwarding",
    "Load-Use hazard followed immediately by branch",
    "Backward branch loops (Array Sum, Factorial, Bubble Sort)"
])

# -----------------------------------------------------------------------------
# SLIDE 10: Benchmark Suite 1: Array Sum & Maximum Search
# -----------------------------------------------------------------------------
slide10 = prs.slides.add_slide(blank_slide_layout)
add_header(slide10, "Benchmark Verification: Array Sum & Maximum Search")
add_card(slide10, 0.8, 1.8, 5.6, 5.0, "Benchmark 1: Array Sum (Mandatory)", [
    "Objective: Compute arithmetic sum of array [10, 20, 30, 40]",
    "Algorithmic structure: Pointer increment, loop counter, LW, ADD, BEQ, SW",
    "Expected Result: 10 + 20 + 30 + 40 = 100 (0x00000064)",
    "Observed Memory: Mem[16] = 100 [PASS]",
    "Observed Register: Reg $t1 = 100 [PASS]",
    "Validated on both Single-Cycle and 5-Stage Pipelined Cores!"
], bg_color=RGBColor(240, 255, 244), border_color=GREEN)
add_card(slide10, 6.8, 1.8, 5.7, 5.0, "Benchmark 2: Maximum Search", [
    "Objective: Scan array [12, 45, 23, 67, 34] and identify maximum",
    "Algorithmic structure: Sequential scan, SLT comparison, conditional branch, update",
    "Expected Result: Max = 67 (0x00000043)",
    "Observed Memory: Mem[20] = 67 [PASS]",
    "Observed Register: Reg $t1 = 67 [PASS]",
    "Successfully verified branch taken vs not-taken logic"
], bg_color=RGBColor(240, 255, 244), border_color=GREEN)

# -----------------------------------------------------------------------------
# SLIDE 11: Benchmark Suite 2: Factorial, Fibonacci & Bubble Sort
# -----------------------------------------------------------------------------
slide11 = prs.slides.add_slide(blank_slide_layout)
add_header(slide11, "Advanced Benchmarks: Factorial, Fibonacci & Bubble Sort")
add_card(slide11, 0.8, 1.8, 3.7, 5.0, "Benchmark 3: Factorial", [
    "Computes 5! = 120 (0x78)",
    "Nested loop with repeated addition",
    "Mem[0] = 120 [PASS]",
    "Reg $t1 = 120 [PASS]",
    "Tests negative immediate ADDI"
], bg_color=RGBColor(240, 255, 244), border_color=GREEN)
add_card(slide11, 4.8, 1.8, 3.7, 5.0, "Benchmark 4: Fibonacci", [
    "Computes F(0) to F(8)",
    "F(8) = 21 (0x15)",
    "Stores sequence in Mem[0..32]",
    "Mem[32] = 21 [PASS]",
    "Reg $t3 = 21 [PASS]"
], bg_color=RGBColor(240, 255, 244), border_color=GREEN)
add_card(slide11, 8.8, 1.8, 3.7, 5.0, "Benchmark 5: Bubble Sort", [
    "Sorts [45, 12, 89, 34, 23]",
    "Target: [12, 23, 34, 45, 89]",
    "Mem[0..16] = [12,23,34,45,89]",
    "All 5 elements in order [PASS]",
    "Complex nested loops & swaps"
], bg_color=RGBColor(240, 255, 244), border_color=GREEN)

# -----------------------------------------------------------------------------
# SLIDE 12: Timing Analysis & Performance Comparison
# -----------------------------------------------------------------------------
slide12 = prs.slides.add_slide(blank_slide_layout)
add_header(slide12, "Performance Analysis: Single-Cycle vs Pipelined Core")
add_card(slide12, 0.8, 1.8, 5.6, 5.0, "Architectural Comparison Table", [
    "Single-Cycle CPI: Fixed at 1.0",
    "Pipelined Ideal CPI: 1.0; Effective CPI (with stalls): ~1.18",
    "Single-Cycle Critical Path: ~18.1 ns (Max F_clk = ~55 MHz)",
    "Pipelined Critical Path: ~5.4 ns (Max F_clk = ~185 MHz)",
    "Execution Time Formula: CPU Time = Instruction Count * CPI * T_clk",
    "Throughput Speedup: ~2.85x faster execution on pipelined architecture!"
])
add_card(slide12, 6.8, 1.8, 5.7, 5.0, "Key Architectural Insights", [
    "Pipelining divides the long combinational path into balanced stages",
    "Forwarding eliminates 85%+ of potential data hazard stalls",
    "Load-Use stall penalty is only 1 cycle per load dependency",
    "Branch penalty is restricted to 2 cycles upon taken branches",
    "Substantial speedup justifies the modest hardware area overhead"
])

# -----------------------------------------------------------------------------
# SLIDE 13: FPGA Synthesis & Hardware Resource Estimation
# -----------------------------------------------------------------------------
slide13 = prs.slides.add_slide(blank_slide_layout)
add_header(slide13, "FPGA Synthesis & Hardware Utilization (Xilinx Artix-7)")
add_card(slide13, 0.8, 1.8, 5.6, 5.0, "Resource Utilization (Artix-7 XC7A35T)", [
    "Look-Up Tables (LUTs): Single-Cycle ~1,420 | Pipelined ~2,150 (< 11% utilization)",
    "Flip-Flops (Registers): Single-Cycle ~1,056 | Pipelined ~1,380 (< 4% utilization)",
    "Block RAM (BRAM): 1 BRAM tile used for Harvard Memory interface (< 2%)",
    "I/O Pins: Bounded by wrapper / debug bus",
    "Power Consumption: Estimated at < 0.22 W (Static + Dynamic)"
])
add_card(slide13, 6.8, 1.8, 5.7, 5.0, "Design Feasibility & Deployment", [
    "Design conforms strictly to synthesizable Verilog-2001 standard",
    "No inferred latches in any combinational always blocks",
    "Synchronous positive-edge clocking throughout all sequential elements",
    "Ready for bitstream generation and hardware testing on Basys-3 / Nexys A7 FPGA"
])

# -----------------------------------------------------------------------------
# SLIDE 14: Team Work Allocation & Final Conclusion
# -----------------------------------------------------------------------------
slide14 = prs.slides.add_slide(blank_slide_layout)
add_header(slide14, "Team Contributions & Final Conclusion")
add_card(slide14, 0.8, 1.8, 5.6, 5.0, "Individual Team Contributions", [
    "Member 1: CPU Architecture, IMEM, Pipelined Integration & Top Wrappers",
    "Member 2: 32-bit ALU, ALU Control, Register File, Forwarding Multiplexers",
    "Member 3: Main Control Unit, Sign Extension, Hazard Detection Unit",
    "Member 4: Data Memory, Automated Testbenches, Assembly Benchmarks, VCDs",
    "Member 5: IEEE Technical Report, Presentation Slides, Diagrams & Repo"
])
add_card(slide14, 6.8, 1.8, 5.7, 5.0, "Final Project Summary", [
    "Successfully delivered both Single-Cycle and 5-Stage Pipelined MIPS cores",
    "Forwarding and Hazard Detection units completely functional",
    "78/78 assertions passed across all testbenches (100% pass rate)",
    "All 5 benchmark programs verified without discrepancies",
    "Project is 100% complete, verified, and ready for final defense!"
], bg_color=RGBColor(240, 249, 255), border_color=CORAL)

prs.save("presentation/final_presentation.pptx")
print("Successfully generated presentation/final_presentation.pptx")
