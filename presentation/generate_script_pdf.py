#!/usr/bin/env python3
"""
Generate a printable PDF copy of the 4-Teammate Final Presentation Script
for the Single-Cycle & 5-Stage Pipelined MIPS Processor project.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

pdf_filename = "presentation/Final_Presentation_Script_4_Teammates.pdf"

doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=0.5*inch,
    rightMargin=0.5*inch,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch
)

styles = getSampleStyleSheet()

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

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#2B6CB0'),
    spaceAfter=10
)

speaker_hdr_style = ParagraphStyle(
    'SpeakerHdr',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    alignment=TA_LEFT,
    textColor=colors.HexColor('#C53030'),
    spaceBefore=8,
    spaceAfter=4
)

slide_cue_style = ParagraphStyle(
    'SlideCue',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=12,
    alignment=TA_LEFT,
    textColor=colors.HexColor('#2B6CB0'),
    spaceBefore=6,
    spaceAfter=2
)

dialogue_style = ParagraphStyle(
    'Dialogue',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=8.5,
    leading=11.5,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor('#1A202C'),
    spaceAfter=6,
    firstLineIndent=10
)

qa_q_style = ParagraphStyle(
    'QA_Q',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor('#1A365D'),
    spaceBefore=4,
    spaceAfter=2
)

qa_a_style = ParagraphStyle(
    'QA_A',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#2D3748'),
    spaceAfter=6,
    firstLineIndent=8
)

th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.white)
tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, alignment=TA_CENTER, textColor=colors.HexColor('#1A202C'))

story = []

story.append(Paragraph("Final Project Defense & Presentation Script: 4 Speaking Teammates", title_style))
story.append(Paragraph("Single-Cycle & 5-Stage Pipelined MIPS Processor with Memory Interface and Hazard Resolution", subtitle_style))

# Role allocation table
table_data = [
    [Paragraph("Teammate", th_style), Paragraph("Role", th_style), Paragraph("Slides", th_style), Paragraph("Topic Focus", th_style), Paragraph("Duration", th_style)],
    [Paragraph("Teammate 1", tc_style), Paragraph("CPU Architecture Lead", tc_style), Paragraph("1 – 4", tc_style), Paragraph("Introduction, Scope, Harvard Memory, Single-Cycle Base", tc_style), Paragraph("3:30 min", tc_style)],
    [Paragraph("Teammate 2", tc_style), Paragraph("Pipelining Specialist", tc_style), Paragraph("5 – 8", tc_style), Paragraph("5-Stage Stages, Forwarding Unit, Hazard Detection, ISA", tc_style), Paragraph("3:45 min", tc_style)],
    [Paragraph("Teammate 3", tc_style), Paragraph("Verification Lead", tc_style), Paragraph("9 – 11", tc_style), Paragraph("Verification Framework, 5 Benchmarks (100% Pass)", tc_style), Paragraph("3:45 min", tc_style)],
    [Paragraph("Teammate 4", tc_style), Paragraph("Performance & FPGA Lead", tc_style), Paragraph("12 – 14", tc_style), Paragraph("Performance Speedup (2.85x), Artix-7 Synthesis, Summary", tc_style), Paragraph("3:30 min", tc_style)],
    [Paragraph("Member 5", tc_style), Paragraph("Production Coordinator", tc_style), Paragraph("All", tc_style), Paragraph("NON-SPEAKING: Slides, Terminal, GTKWave demo", tc_style), Paragraph("0:00 min", tc_style)]
]
t = Table(table_data, colWidths=[1.1*inch, 1.4*inch, 0.7*inch, 3.1*inch, 0.9*inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t)
story.append(Spacer(1, 10))

# Teammate 1
story.append(Paragraph("PART 1: TEAMMATE 1 (Slides 1 – 4 | 0:00 – 3:30)", speaker_hdr_style))
story.append(Paragraph("[SLIDE 1: Title & Team Introduction]", slide_cue_style))
story.append(Paragraph('"Respected evaluators and professors, good morning. We are presenting our final academic project: the Design, Implementation, and Hardware Verification of Single-Cycle and 5-Stage Pipelined MIPS Processors with Memory Interface and Hazard Resolution. Our team consists of five members: myself, serving as the CPU Architecture Lead; Teammate 2, our Pipelining Specialist; Teammate 3, our Verification Lead; Teammate 4, our Performance & Hardware Synthesis Lead; and Member 5, our technical production coordinator. We developed synthesizable, cycle-accurate hardware in Verilog HDL, progressing from a baseline single-cycle core to a fully pipelined processor with dedicated data forwarding and hazard detection units."', dialogue_style))

story.append(Paragraph("[SLIDE 2: Scope Evolution]", slide_cue_style))
story.append(Paragraph('"In Phase I, our single-cycle core achieved an ideal CPI of 1.0, but its clock period was bounded by the cumulative delay of the longest instruction (~18.1 ns, or 55 MHz). In the Final Phase, we segmented the core into a balanced 5-stage classic pipeline (IF, ID, EX, MEM, WB), incorporating a Data Forwarding Unit and a Hazard Detection Unit. This scaled our estimated clock frequency to 185 MHz on a Xilinx Artix-7 FPGA."', dialogue_style))

story.append(Paragraph("[SLIDE 3: Harvard Memory Subsystem]", slide_cue_style))
story.append(Paragraph('"We implemented a strict Harvard Architecture with separate 256-word Instruction ROM and Data RAM. This prevents structural memory hazards between simultaneous instruction fetch in IF and data access in MEM. Addressing uses word alignment on bits [9:2], discarding the lower two byte offsets."', dialogue_style))

story.append(Paragraph("[SLIDE 4: Single-Cycle Bottleneck & Handover]", slide_cue_style))
story.append(Paragraph('"The single-cycle critical path totals 18.1 ns, dominated by the Load Word path. To overcome this limitation, we introduced pipelining. I will now hand over to Teammate 2 to explain our pipelined microarchitecture."', dialogue_style))

# Teammate 2
story.append(Paragraph("PART 2: TEAMMATE 2 (Slides 5 – 8 | 3:30 – 7:15)", speaker_hdr_style))
story.append(Paragraph("[SLIDE 5: 5-Stage Pipelined Datapath]", slide_cue_style))
story.append(Paragraph('"Thank you, Teammate 1. I am Teammate 2. We inserted four synchronous pipeline registers: IF/ID, ID/EX, EX/MEM, and MEM/WB. In Write-Back, a multiplexer selects memory data or the ALU result. To prevent half-cycle register read stalls, we built an internal write-before-read bypass into the Register File, allowing Decode to read data updated in Write-Back during the exact same clock cycle."', dialogue_style))

story.append(Paragraph("[SLIDE 6: Forwarding Unit]", slide_cue_style))
story.append(Paragraph('"To resolve RAW data hazards without stalling, our Data Forwarding Unit continuously compares destination registers from EX/MEM and MEM/WB against source registers in Execute. In back-to-back arithmetic instructions such as ADDI followed by ADD, operands are forwarded directly into the ALU inputs with zero stall penalty, preserving a 1.0 CPI for compute workloads."', dialogue_style))

story.append(Paragraph("[SLIDE 7: Hazard Detection Unit]", slide_cue_style))
story.append(Paragraph('"When an instruction immediately follows a Load Word and requires the loaded register, forwarding alone is impossible because data has not yet arrived from memory. Our Hazard Detection Unit detects this in Decode, freezes the PC and IF/ID register, and injects a 1-cycle bubble into ID/EX. Branches are evaluated in Execute using forwarded operands; when a branch is taken, misfetched instructions in IF/ID and ID/EX are flushed."', dialogue_style))

story.append(Paragraph("[SLIDE 8: Control Decoding Matrix & Handover]", slide_cue_style))
story.append(Paragraph('"Our Main Control Unit decodes the 6-bit opcode to generate nine control signals, with safe defaults deasserting all lines for illegal opcodes. I now pass the floor to Teammate 3 for our verification suite."', dialogue_style))

# Teammate 3
story.append(Paragraph("PART 3: TEAMMATE 3 (Slides 9 – 11 | 7:15 – 11:00)", speaker_hdr_style))
story.append(Paragraph("[SLIDE 9: Automated Verification Framework]", slide_cue_style))
story.append(Paragraph('"Thank you, Teammate 2. I am Teammate 3. We implemented an automated, multi-tiered self-checking verification suite across six testbenches. All 78 assertions executed and passed with 100% success and zero errors, covering corner cases including Register $zero write protection and simultaneous EX/MEM hazard forwarding."', dialogue_style))

story.append(Paragraph("[SLIDE 10: Benchmarks 1 & 2: Array Sum and Max Search]", slide_cue_style))
story.append(Paragraph('"Benchmark 1 is Array Sum: it sums [10, 20, 30, 40] in memory. The observed result in Mem[16] and register $t1 is exactly 100 (0x64). Benchmark 2 is Maximum Search: scanning [12, 45, 23, 67, 34], it correctly finds max = 67 in Mem[20], validating signed SLT comparison."', dialogue_style))

story.append(Paragraph("[SLIDE 11: Benchmarks 3, 4 & 5: Factorial, Fibonacci, Bubble Sort & Handover]", slide_cue_style))
story.append(Paragraph('"Benchmark 3 computes 5! = 120 via repeated addition, verified at Mem[0] = 120. Benchmark 4 computes Fibonacci F(8) = 21, verified at Mem[32] = 21. Benchmark 5 sorts [45, 12, 89, 34, 23] into [12, 23, 34, 45, 89] via double-nested loops in memory. All passed on our pipelined core. I now hand over to Teammate 4."', dialogue_style))

# Teammate 4
story.append(Paragraph("PART 4: TEAMMATE 4 (Slides 12 – 14 | 11:00 – 14:30)", speaker_hdr_style))
story.append(Paragraph("[SLIDE 12: Timing Analysis & Speedup]", slide_cue_style))
story.append(Paragraph('"Thank you, Teammate 3. I am Teammate 4. Pipelining reduces the critical path from 18.1 ns (55 MHz) to 5.4 ns (185 MHz). With an effective CPI of ~1.18 accounting for stalls and branch penalties, our pipelined processor achieves a 2.85x overall throughput speedup over the single-cycle baseline."', dialogue_style))

story.append(Paragraph("[SLIDE 13: FPGA Synthesis on Xilinx Artix-7]", slide_cue_style))
story.append(Paragraph('"Synthesis on Artix-7 XC7A35T indicates approximately 2,150 LUTs (< 11% capacity), 1,380 Flip-Flops (< 4%), 1 BRAM tile (< 2%), and total power under 0.22 W. The RTL strictly adheres to synthesizable Verilog-2001 with no inferred latches."', dialogue_style))

story.append(Paragraph("[SLIDE 14: Team Allocation, Conclusion & Viva Defense]", slide_cue_style))
story.append(Paragraph('"Every member owned critical deliverables. In conclusion, the project fulfills 100% of Final Phase requirements: verified single-cycle and pipelined cores, hazard forwarding, automated testing with 78/78 passed assertions, 5 verified benchmarks, and complete IEEE documentation. Thank you, and we welcome your questions."', dialogue_style))

# Viva Q&A
story.append(Spacer(1, 10))
story.append(Paragraph("VIVA DEFENSE & PANEL Q&A MODEL ANSWERS", speaker_hdr_style))
story.append(Paragraph("Q1 (Teammate 1): Why Harvard architecture over Von Neumann?", qa_q_style))
story.append(Paragraph("A: Harvard provides independent memory buses for IF and MEM stages, eliminating structural hazards when fetching instructions while reading/writing memory data in the same cycle.", qa_a_style))

story.append(Paragraph("Q2 (Teammate 2): How does the Forwarding Unit handle double RAW hazards to the same register?", qa_q_style))
story.append(Paragraph("A: The EX hazard condition is checked first, taking precedence over MEM hazards in an if-else hierarchy. This ensures the most recent ALU result from EX/MEM always overrides older data.", qa_a_style))

story.append(Paragraph("Q3 (Teammate 2): Why can't forwarding resolve Load-Use hazards without stalling?", qa_q_style))
story.append(Paragraph("A: Data is only available at the end of the MEM stage. The subsequent instruction needs it at the start of EX. Time travel is impossible; hence, 1 stall cycle is mandatory.", qa_a_style))

story.append(Paragraph("Q4 (Teammate 3): How was Register $zero write protection verified?", qa_q_style))
story.append(Paragraph("A: Test 18 executed ADDI $0, $0, 111. Subsequent assertion confirmed register $0 remained strictly zero, verified by both RTL hardware clamps and self-checking testbenches.", qa_a_style))

story.append(Paragraph("Q5 (Teammate 4): Why is speedup 2.85x rather than the theoretical 5x?", qa_q_style))
story.append(Paragraph("A: Stage delays are not perfectly equal (Execute stage is 5.4 ns), pipeline register overhead exists, and CPI is ~1.18 due to load-use stalls and branch flushes. (18.1 / (1.18 * 5.4)) = 2.85x.", qa_a_style))

doc.build(story)
print(f"Successfully compiled {pdf_filename}")
