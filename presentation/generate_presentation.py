#!/usr/bin/env python3
"""
Generate a professional 9-slide PowerPoint presentation (.pptx)
for the Single-Cycle MIPS Processor with Memory Interface project.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette: Professional Engineering Theme (Navy Blue, Slate Grey, Coral Accent)
DARK_BLUE = RGBColor(26, 54, 93)      # #1A365D
MED_BLUE  = RGBColor(43, 108, 176)    # #2B6CB0
LIGHT_BG  = RGBColor(247, 250, 252)   # #F7FAFC
TEXT_DARK = RGBColor(45, 55, 72)      # #2D3748
TEXT_MUTED= RGBColor(113, 128, 150)   # #718096
CORAL     = RGBColor(229, 62, 62)     # #E53E3E
WHITE     = RGBColor(255, 255, 255)

blank_slide_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="PHASE I DEMONSTRATION & EVALUATION"):
    # Category / Super-title
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = CORAL

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

# -----------------------------------------------------------------------------
# SLIDE 1: Title & Team Members
# -----------------------------------------------------------------------------
slide1 = prs.slides.add_slide(blank_slide_layout)

# Main Title Box
title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(2.2))
tf = title_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Single-Cycle MIPS Processor\nwith Memory Interface"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = DARK_BLUE

p2 = tf.add_paragraph()
p2.text = "Hardware Design, Verilog Implementation, and Full System Verification (Phase I)"
p2.font.size = Pt(18)
p2.font.color.rgb = MED_BLUE
p2.space_before = Pt(10)

# Team Members Box
team_box = slide1.shapes.add_textbox(Inches(1.0), Inches(3.8), Inches(11.3), Inches(3.0))
tf_team = team_box.text_frame
p_th = tf_team.paragraphs[0]
p_th.text = "Project Team Members & Responsibilities:"
p_th.font.size = Pt(14)
p_th.font.bold = True
p_th.font.color.rgb = DARK_BLUE

members = [
    ("Member 1 [Name Placeholder]", "CPU Architecture & Datapath Integration Lead"),
    ("Member 2 [Name Placeholder]", "ALU, ALU Control & Register File Specialist"),
    ("Member 3 [Name Placeholder]", "Main Control Unit & Instruction Decoding"),
    ("Member 4 [Name Placeholder]", "Memory Subsystems & Verification Lead"),
    ("Member 5 [Name Placeholder]", "Technical Documentation, Report & Presentation Lead")
]

for name, role in members:
    pm = tf_team.add_paragraph()
    pm.text = f"• {name}  —  {role}"
    pm.font.size = Pt(13)
    pm.font.color.rgb = TEXT_DARK
    pm.space_before = Pt(6)

# -----------------------------------------------------------------------------
# SLIDE 2: Problem Statement & Objectives
# -----------------------------------------------------------------------------
slide2 = prs.slides.add_slide(blank_slide_layout)
add_header(slide2, "Problem Statement & Project Objectives")

box2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf2 = box2.text_frame
tf2.word_wrap = True

def add_bullet(tf, heading, body):
    p = tf.add_paragraph()
    p.text = heading + ": "
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_BLUE
    p.space_before = Pt(12)
    
    run = p.add_run()
    run.text = body
    run.font.bold = False
    run.font.color.rgb = TEXT_DARK

add_bullet(tf2, "Context & Challenge", 
           "Modern computer architecture requires deep understanding of hardware-software boundary. Designing an operational 32-bit processor in synthesizable Verilog demonstrates core microarchitectural principles, including single-cycle datapath timing, control flow decoding, and memory interfaces.")

add_bullet(tf2, "Primary Objectives", 
           "Design, implement, verify, and document a 32-bit single-cycle MIPS processor in Verilog 2001 RTL supporting 10 essential instructions spanning R, I, and J formats.")

add_bullet(tf2, "Key Architectural Requirements", 
           "Full 32 general-purpose registers with $zero write-protection, 32-bit Program Counter with reset, Harvard architecture instruction and data memory interfaces, combinational branch/jump target calculation, and zero latches.")

add_bullet(tf2, "Phase I Verification Target", 
           "100% self-checking verification pass rate across unit testbenches and execution of 3 complete benchmark programs: Array Sum (producing 100), Maximum Search (producing 67), and Factorial (producing 120).")

# -----------------------------------------------------------------------------
# SLIDE 3: MIPS Architecture & Datapath
# -----------------------------------------------------------------------------
slide3 = prs.slides.add_slide(blank_slide_layout)
add_header(slide3, "Single-Cycle MIPS Architecture & Datapath")

box3_text = slide3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.0), Inches(5.2))
tf3 = box3_text.text_frame
tf3.word_wrap = True

add_bullet(tf3, "Harvard Subsystem", "Separate Instruction Memory (IMEM) and Data Memory (DMEM) prevent structural memory hazards during the single clock cycle.")
add_bullet(tf3, "Next-PC Calculation", "Sequential PC + 4, Branch Target PC + 4 + (Imm << 2), and Jump Target {PC+4[31:28], Target, 2'b00} resolved via multiplexers.")
add_bullet(tf3, "Write-Back Multiplexing", "MemtoReg multiplexer selects between Data Memory read data and ALU result for register writeback.")

if os.path.exists("diagrams/datapath_architecture.png"):
    slide3.shapes.add_picture("diagrams/datapath_architecture.png", 
                              Inches(5.9), Inches(1.5), width=Inches(6.8))

# -----------------------------------------------------------------------------
# SLIDE 4: Verilog Module Architecture
# -----------------------------------------------------------------------------
slide4 = prs.slides.add_slide(blank_slide_layout)
add_header(slide4, "Modular Verilog RTL Hierarchy")

box4_text = slide4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
tf4 = box4_text.text_frame
tf4.word_wrap = True

modules_info = [
    ("program_counter.v", "32-bit PC register, synchronous reset to 0x00000000"),
    ("instruction_memory.v", "256-word (1024B) ROM, combinational read, hex load"),
    ("control_unit.v", "6-bit opcode combinational decoder for all 9 control lines"),
    ("register_file.v", "32x32-bit dual-read, sync-write, $0 hardwired to zero"),
    ("sign_extend.v", "Two's complement 16-to-32 bit immediate sign extension"),
    ("alu.v", "32-bit core (ADD, SUB, AND, OR, SLT, Zero flag generation)"),
    ("alu_control.v", "Decodes 2-bit ALUOp and 6-bit funct to 4-bit ALU control"),
    ("data_memory.v", "256-word RAM, word-aligned, combinational read, sync write"),
    ("mips_cpu.v", "Core processor integrating datapath, control, and muxes"),
    ("top_module.v", "Clean top wrapper integrating CPU, IMEM, and DMEM with debug buses")
]

for mod, desc in modules_info:
    p = tf4.add_paragraph()
    p.text = f"• {mod:22s} : {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(4)

if os.path.exists("diagrams/memory_interface.png"):
    slide4.shapes.add_picture("diagrams/memory_interface.png", 
                              Inches(7.0), Inches(1.8), width=Inches(5.6))

# -----------------------------------------------------------------------------
# SLIDE 5: Instruction Execution & Control Signals
# -----------------------------------------------------------------------------
slide5 = prs.slides.add_slide(blank_slide_layout)
add_header(slide5, "Supported ISA & Control Unit Decoding Matrix")

box5_text = slide5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.2))
tf5 = box5_text.text_frame
tf5.word_wrap = True

add_bullet(tf5, "Complete 10-Instruction Scope", "Supports 5 R-Type (ADD, SUB, AND, OR, SLT), 4 I-Type (ADDI, LW, SW, BEQ), and 1 J-Type (J).")
add_bullet(tf5, "Single-Level Decoding", "Control unit extracts 6-bit opcode inst[31:26] to produce RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, Jump, ALUOp[1:0].")
add_bullet(tf5, "Safe Default Guarantees", "All unspecified opcodes default to 0 to prevent accidental bus contention, invalid memory writes, or latch generation.")

if os.path.exists("diagrams/control_unit_flow.png"):
    slide5.shapes.add_picture("diagrams/control_unit_flow.png", 
                              Inches(6.2), Inches(1.5), width=Inches(6.5))

# -----------------------------------------------------------------------------
# SLIDE 6: Simulation Demonstration & Verification Methodology
# -----------------------------------------------------------------------------
slide6 = prs.slides.add_slide(blank_slide_layout)
add_header(slide6, "Simulation Methodology & Automated Testbenches")

box6 = slide6.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf6 = box6.text_frame
tf6.word_wrap = True

add_bullet(tf6, "Verification Environment", "Simulated using Icarus Verilog (v13.0) and GTKWave. Fully automated, self-checking testbenches with programmatic assertions.")
add_bullet(tf6, "Hierarchical Testing", "Bottom-up testing strategy: Unit testbenches (ALU, Control, RegFile, DMEM) followed by full CPU integration testbench.")
add_bullet(tf6, "100% Verification Coverage", "57 total assertions executed across unit and system tests. 57 passed, 0 failed. Full cycle-by-cycle VCD traces generated.")
add_bullet(tf6, "Robust Corner-Case Validation", "Tested negative signed comparisons (-10 < 5), zero-flag assertion upon equal operand subtraction, $zero write blocking, and branch take/not-take logic.")

# -----------------------------------------------------------------------------
# SLIDE 7: Sample Program 1 — Array Sum & Actual Output
# -----------------------------------------------------------------------------
slide7 = prs.slides.add_slide(blank_slide_layout)
add_header(slide7, "Benchmark Program: Array Summation (Mandatory)")

box7_left = slide7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))
tf7_l = box7_left.text_frame
tf7_l.word_wrap = True

add_bullet(tf7_l, "Program Objective", "Compute sum of 4 integers: 10, 20, 30, 40 preloaded into Data Memory at addresses 0x00, 0x04, 0x08, 0x0C.")
add_bullet(tf7_l, "Instructions Used", "Demonstrates LW (load element), ADD (accumulate sum), ADDI (loop increment and pointer advance), BEQ (loop boundary check), SW (store result), J (loop jump).")
add_bullet(tf7_l, "Execution Performance", "Loop executes 4 iterations over 40 clock cycles. Results stored in Data Memory address 16 (0x00000010).")

box7_right = slide7.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.8), Inches(5.2))
tf7_r = box7_right.text_frame
tf7_r.word_wrap = True

add_bullet(tf7_r, "Expected Result", "10 + 20 + 30 + 40 = 100 (Hex: 0x00000064)")
add_bullet(tf7_r, "Observed Simulation Output", 
           "Data Memory[16] = 0x00000064 (100) -> PASS\nRegister $t1 ($9) = 0x00000064 (100) -> PASS\nZero errors, verified by automated testbench.")
add_bullet(tf7_r, "Additional Benchmark Programs", 
           "• Maximum Search (12, 45, 23, 67, 34) -> Result: Mem[20] = 67 (PASS)\n• Factorial Calculation (5!) -> Result: Mem[0] = 120 (PASS)")

# -----------------------------------------------------------------------------
# SLIDE 8: Waveform & Verification Results
# -----------------------------------------------------------------------------
slide8 = prs.slides.add_slide(blank_slide_layout)
add_header(slide8, "Waveform Analysis & Hardware Verification")

box8_text = slide8.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.2))
tf8 = box8_text.text_frame
tf8.word_wrap = True

add_bullet(tf8, "Waveform Evidence", "VCD files generated for all testbenches. tb_mips_cpu.vcd captures 225 simulation cycles showing PC increment, memory writes, and register writebacks.")
add_bullet(tf8, "Signal Timing Analysis", "PC updates synchronously on posedge clk; combinational instruction read yields valid instruction within clock high; ALU and memory reads settle cleanly before active clock edge.")
add_bullet(tf8, "Glitch & Hazard Free", "No unintended write pulses on mem_write or reg_write; no unknown (X/Z) values observed on critical datapath buses.")

if os.path.exists("diagrams/instruction_flow.png"):
    slide8.shapes.add_picture("diagrams/instruction_flow.png", 
                              Inches(6.5), Inches(1.6), width=Inches(6.2))

# -----------------------------------------------------------------------------
# SLIDE 9: Conclusion & Phase II Roadmap
# -----------------------------------------------------------------------------
slide9 = prs.slides.add_slide(blank_slide_layout)
add_header(slide9, "Conclusion & Phase II Future Scope")

box9 = slide9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
tf9 = box9.text_frame
tf9.word_wrap = True

add_bullet(tf9, "Phase I Achievements", 
           "Successfully delivered a fully functional, verified 32-bit single-cycle MIPS processor in synthesizable Verilog. All 10 instructions, Harvard memory interface, and 3 benchmark programs fully verified with 100% test pass rate.")

add_bullet(tf9, "Phase I Evaluation Deliverables Completed", 
           "IEEE Project Report (PDF & LaTeX), 9-slide demonstration presentation, 5-member video demonstration script, architecture diagrams, simulation logs, and structured GitHub repository.")

add_bullet(tf9, "Phase II Roadmap & Enhancements", 
           "• Pipelined Architecture: Transition to classic 5-stage pipeline (IF, ID, EX, MEM, WB) with hazard detection and forwarding units.\n• Memory Hierarchy: Add L1 direct-mapped instruction and data caches.\n• ISA Expansion: Implement Shift operations (SLL, SRL), JAL/JR for function call support, and LUI.\n• FPGA Prototyping: Synthesis and deployment onto Xilinx Artix-7 / Cyclone IV FPGA board with seven-segment display output.")

prs.save("presentation/prototype_presentation.pptx")
print("Presentation successfully saved to presentation/prototype_presentation.pptx")
