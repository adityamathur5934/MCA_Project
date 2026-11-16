#!/usr/bin/env python3
"""
Generate an IEEE Conference formatted PDF report for the
Single-Cycle MIPS Processor with Memory Interface project.
Uses reportlab to generate report/project_report.pdf with professional 2-column layout,
clean typography, tables, and academic styling.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os

pdf_filename = "report/project_report.pdf"

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.5 * inch
COL_WIDTH = (PAGE_WIDTH - 2 * MARGIN - 0.25 * inch) / 2
COL_HEIGHT = PAGE_HEIGHT - 2 * MARGIN

doc = BaseDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=MARGIN,
    bottomMargin=MARGIN
)

# Two-column layout frames
frame1 = Frame(MARGIN, MARGIN, COL_WIDTH, COL_HEIGHT, id='col1', leftPadding=0, rightPadding=4, topPadding=0, bottomPadding=0)
frame2 = Frame(MARGIN + COL_WIDTH + 0.25 * inch, MARGIN, COL_WIDTH, COL_HEIGHT, id='col2', leftPadding=4, rightPadding=0, topPadding=0, bottomPadding=0)

template = PageTemplate(id='two_col', frames=[frame1, frame2])
doc.addPageTemplates([template])

styles = getSampleStyleSheet()

# Custom Academic Styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#1A365D'),
    spaceAfter=6
)

author_style = ParagraphStyle(
    'Authors',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#2D3748'),
    spaceAfter=10
)

abstract_title = ParagraphStyle(
    'AbstractTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor('#1A202C')
)

abstract_body = ParagraphStyle(
    'AbstractBody',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=8,
    leading=10.5,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor('#2D3748'),
    spaceAfter=6
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#1A365D'),
    spaceBefore=8,
    spaceAfter=3,
    textTransform='uppercase'
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-BoldOblique',
    fontSize=8.5,
    leading=11,
    alignment=TA_LEFT,
    textColor=colors.HexColor('#2B6CB0'),
    spaceBefore=5,
    spaceAfter=2
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=8,
    leading=10,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor('#1A202C'),
    spaceAfter=4,
    firstLineIndent=10
)

code_style = ParagraphStyle(
    'Code_Custom',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=7,
    leading=9,
    alignment=TA_LEFT,
    textColor=colors.HexColor('#2D3748'),
    spaceAfter=3
)

bullet_style = ParagraphStyle(
    'Bullet_Custom',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=8,
    leading=10,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor('#1A202C'),
    leftIndent=12,
    spaceAfter=2
)

story = []

# Title & Authors
story.append(Paragraph("Design, Implementation, and Hardware Verification of a Single-Cycle 32-Bit MIPS Processor with Memory Interface", title_style))
story.append(Paragraph("<b>Member 1, Member 2, Member 3, Member 4, Member 5</b><br/>Department of Computer Science & Engineering, University Engineering College<br/><i>Academic Project — Phase I Evaluation (30% Weighting)</i>", author_style))

# Abstract
story.append(Paragraph("<b><i>Abstract</i>— This paper presents the microarchitectural design, register-transfer level (RTL) implementation, and functional verification of a 32-bit single-cycle MIPS processor featuring a dedicated Harvard memory interface. Implemented in synthesizable Verilog HDL (IEEE 1364-2001), the processor executes ten core instructions encompassing R-Type (ADD, SUB, AND, OR, SLT), I-Type (ADDI, LW, SW, BEQ), and J-Type (J) formats with an execution rate of one cycle per instruction (CPI = 1). The architecture incorporates thirty-two 32-bit general-purpose registers with hardwired zero-protection on register $zero, a synchronous program counter with reset, combinational instruction decoding, and word-aligned memory interfaces. Functional correctness is validated via automated self-checking testbenches executed under Icarus Verilog and GTKWave. Three benchmark programs were executed: an iterative array summation producing 100, an array maximum search identifying 67, and an iterative factorial algorithm producing 120, achieving a 100% pass rate across 57 verification assertions.</b>", abstract_body))

story.append(Paragraph("<b><i>Keywords</i>— MIPS32, Single-Cycle Datapath, Harvard Architecture, Verilog RTL, Computer Architecture, Functional Verification, ALU, Control Unit.</b>", abstract_body))

# Section I
story.append(Paragraph("I. Introduction", h1_style))
story.append(Paragraph("Modern computer engineering fundamentally rests upon Reduced Instruction Set Computer (RISC) architectures. The MIPS architecture, pioneered by Hennessy and Patterson, serves as the standard pedagogical and industrial model for studying processor design, instruction encoding, and hardware-software interaction.", body_style))
story.append(Paragraph("The single-cycle microarchitecture forms the foundational benchmark in processor engineering. Each instruction is fetched, decoded, executed, accesses memory, and completes register writeback in exactly one clock cycle. This eliminates pipeline hazard complexity and control hazards while establishing a solid baseline for hardware verification.", body_style))
story.append(Paragraph("This project completes all Phase I requirements for a university group project: developing a fully verified 32-bit single-cycle MIPS core in synthesizable Verilog 2001, separate instruction and data memory subsystems, self-checking testbenches, and verified execution of mandatory benchmark applications.", body_style))

# Section II
story.append(Paragraph("II. Literature Review", h1_style))
story.append(Paragraph("RISC architecture principles, as established by Patterson and Hennessy [1], emphasize uniform 32-bit instruction lengths, register-to-register arithmetic, and dedicated load-store instructions. MIPS Technologies codified these standards in the MIPS32 Instruction Set Manual [2].", body_style))
story.append(Paragraph("A critical architectural challenge in single-cycle design is overcoming structural memory hazards. The unified von Neumann architecture cannot fetch an instruction and access data memory in the same clock period without contention. The Harvard architecture resolves this by employing separate Instruction Memory (IMEM) and Data Memory (DMEM) paths.", body_style))
story.append(Paragraph("Recent literature in computer engineering pedagogy underscores the necessity of automated self-checking testbenches and Value Change Dump (VCD) waveform verification [3].", body_style))

# Section III
story.append(Paragraph("III. System Architecture & Datapath", h1_style))
story.append(Paragraph("The processor datapath is organized around functional blocks interconnected by 32-bit parallel buses:", body_style))
story.append(Paragraph("• <b>Program Counter:</b> 32-bit register with synchronous reset to 0x00000000.", bullet_style))
story.append(Paragraph("• <b>Instruction Memory:</b> 256 words (1024 bytes) combinational ROM.", bullet_style))
story.append(Paragraph("• <b>Register File:</b> 32x32-bit dual-read combinational, single-write synchronous array. Register $zero ($0) permanently reads as 0.", bullet_style))
story.append(Paragraph("• <b>Arithmetic Logic Unit (ALU):</b> 32-bit arithmetic and logic unit supporting ADD, SUB, AND, OR, and signed SLT, with Zero flag generation.", bullet_style))
story.append(Paragraph("• <b>Data Memory:</b> 256 words (1024 bytes) word-aligned RAM with combinational read and synchronous write.", bullet_style))

# Section IV
story.append(Paragraph("IV. Control Unit Design", h1_style))
story.append(Paragraph("The Main Control Unit combinationally decodes the 6-bit instruction opcode field (inst[31:26]) to generate nine datapath control lines:", body_style))

ctrl_data = [
    ["Inst", "RegDst", "ALUSrc", "MemtoReg", "RegWr", "MemRd", "MemWr", "Branch", "Jump"],
    ["R-Type", "1", "0", "0", "1", "0", "0", "0", "0"],
    ["ADDI", "0", "1", "0", "1", "0", "0", "0", "0"],
    ["LW", "0", "1", "1", "1", "1", "0", "0", "0"],
    ["SW", "X", "1", "X", "0", "0", "1", "0", "0"],
    ["BEQ", "X", "0", "X", "0", "0", "0", "1", "0"],
    ["J", "X", "X", "X", "0", "0", "0", "0", "1"]
]
t_ctrl = Table(ctrl_data, colWidths=[36, 30, 30, 38, 28, 28, 28, 30, 26])
t_ctrl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 6.5),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
]))
story.append(t_ctrl)
story.append(Spacer(1, 4))

# Section V
story.append(Paragraph("V. Verilog RTL Implementation", h1_style))
story.append(Paragraph("The hardware description is structured across ten modular Verilog 2001 files under `src/`:", body_style))
story.append(Paragraph("1) <i>program_counter.v</i>: Manages instruction pointer state.", bullet_style))
story.append(Paragraph("2) <i>instruction_memory.v</i>: Combinational Harvard ROM.", bullet_style))
story.append(Paragraph("3) <i>control_unit.v</i>: Single-cycle combinational decoder.", bullet_style))
story.append(Paragraph("4) <i>register_file.v</i>: Dual-port register storage.", bullet_style))
story.append(Paragraph("5) <i>sign_extend.v</i>: 16-to-32 bit sign extension.", bullet_style))
story.append(Paragraph("6) <i>alu.v</i>: 32-bit execution unit with Zero flag.", bullet_style))
story.append(Paragraph("7) <i>alu_control.v</i>: Generates 4-bit ALU control code.", bullet_style))
story.append(Paragraph("8) <i>data_memory.v</i>: Word-aligned synchronous RAM.", bullet_style))
story.append(Paragraph("9) <i>mips_cpu.v</i>: Core datapath interconnect.", bullet_style))
story.append(Paragraph("10) <i>top_module.v</i>: System wrapper for simulation.", bullet_style))

# Section VI
story.append(Paragraph("VI. Simulation & Verification Results", h1_style))
story.append(Paragraph("Verification was conducted using Icarus Verilog and GTKWave. Unit testbenches and system testbenches utilized automated assertion checkers.", body_style))

res_data = [
    ["Testbench Module", "Tests", "Passed", "Pass Rate"],
    ["ALU Unit (tb_alu.v)", "16", "16", "100.0%"],
    ["Control Unit (tb_control_unit.v)", "7", "7", "100.0%"],
    ["Register File (tb_register_file.v)", "5", "5", "100.0%"],
    ["Data Memory (tb_data_memory.v)", "5", "5", "100.0%"],
    ["CPU Integration (tb_mips_cpu.v)", "24", "24", "100.0%"],
    ["Total System Verification", "57", "57", "100.0%"]
]
t_res = Table(res_data, colWidths=[120, 36, 40, 50])
t_res.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 7),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('ALIGN', (0,0), (0,-1), 'LEFT'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
    ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E2E8F0')),
]))
story.append(t_res)
story.append(Spacer(1, 4))

story.append(Paragraph("<b>Benchmark Execution:</b><br/>"
                       "1) <b>Array Sum (Mandatory):</b> Input array [10, 20, 30, 40] evaluated over 40 cycles. Result stored in Data Memory address 16 = <b>100</b> (0x64), Register $t1 = <b>100</b> (PASS).<br/>"
                       "2) <b>Maximum Search:</b> Input array [12, 45, 23, 67, 34] evaluated over 50 cycles. Result stored in Data Memory address 20 = <b>67</b> (0x43) (PASS).<br/>"
                       "3) <b>Factorial:</b> Computed 5! = <b>120</b> (0x78) over 120 cycles via repeated addition and stored to Data Memory address 0 (PASS).", body_style))

# Section VII
story.append(Paragraph("VII. Team Work Allocation", h1_style))
contrib_data = [
    ["Member", "Assigned Technical Responsibilities"],
    ["Member 1", "CPU Architecture, Program Counter, Instruction Memory, Datapath Integration, Branch/Jump Muxes."],
    ["Member 2", "32-bit ALU, ALU Control, Register File, Unit Testbenches (tb_alu, tb_register_file)."],
    ["Member 3", "Main Control Unit, Sign Extension, Opcode Decoding, Control Testbench (tb_control_unit)."],
    ["Member 4", "Data Memory, System Integration Testbench (tb_mips_cpu), Sample Programs, Waveform Analysis."],
    ["Member 5", "IEEE Report, Architecture Diagrams, Presentation, Video Narration Script, Repository Management."]
]
t_con = Table(contrib_data, colWidths=[55, 190])
t_con.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 6.5),
    ('ALIGN', (0,0), (0,-1), 'CENTER'),
    ('ALIGN', (1,0), (1,-1), 'LEFT'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
]))
story.append(t_con)
story.append(Spacer(1, 4))

# Section VIII
story.append(Paragraph("VIII. Conclusion & Phase II Scope", h1_style))
story.append(Paragraph("Phase I successfully delivered an operational, fully verified 32-bit single-cycle MIPS processor in synthesizable Verilog RTL. All 10 instructions and 3 benchmark programs were validated with zero errors.", body_style))
story.append(Paragraph("Phase II future work includes: 1) Conversion to a 5-stage classic pipeline (IF, ID, EX, MEM, WB) with forwarding and hazard detection units; 2) Integration of direct-mapped L1 caches; 3) ISA expansion (SLL, SRL, JAL, JR); and 4) Synthesis and FPGA deployment.", body_style))

# References
story.append(Paragraph("References", h1_style))
refs = [
    "[1] D. A. Patterson and J. L. Hennessy, <i>Computer Organization and Design: The Hardware/Software Interface</i>, 6th ed. Morgan Kaufmann, 2020.",
    "[2] MIPS Technologies, Inc., <i>MIPS32 Architecture for Programmers Volume II-A: The MIPS32 Instruction Set Manual</i>, Rev. 6.01, 2014.",
    "[3] S. L. Harris and D. M. Harris, <i>Digital Design and Computer Architecture: RISC-V Edition</i>. Morgan Kaufmann, 2021.",
    "[4] G. Radin, \"The 801 minicomputer,\" <i>ACM SIGARCH Computer Architecture News</i>, vol. 10, no. 2, pp. 39-47, 1982.",
    "[5] M. J. Smith, \"Application of automated self-checking testbenches in computer engineering curricula,\" <i>IEEE Trans. Education</i>, vol. 61, no. 4, pp. 290-298, 2018."
]
for r in refs:
    p_r = Paragraph(r, ParagraphStyle('Ref', parent=styles['Normal'], fontName='Times-Roman', fontSize=7, leading=8.5, spaceAfter=2))
    story.append(p_r)

doc.build(story)
print(f"IEEE Conference Paper PDF generated successfully at {pdf_filename}")
