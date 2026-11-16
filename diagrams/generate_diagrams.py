#!/usr/bin/env python3
"""
Generate professional architectural diagrams for the Single-Cycle MIPS Processor.
Generates:
1. diagrams/datapath_architecture.png
2. diagrams/control_unit_flow.png
3. diagrams/alu_architecture.png
4. diagrams/register_file_architecture.png
5. diagrams/instruction_flow.png
6. diagrams/memory_interface.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_datapath_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    # Title
    ax.text(70, 77, "Single-Cycle MIPS 32-Bit Processor Datapath", 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1A365D')

    def draw_box(x, y, w, h, text, color='#E2E8F0', edge='#2B6CB0', text_color='#1A202C', fsize=10):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5", 
                                      facecolor=color, edgecolor=edge, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                fontsize=fsize, fontweight='bold', color=text_color, multialignment='center')

    # Sub-blocks
    draw_box(4, 30, 12, 20, "Program\nCounter\n(PC)", color='#BEE3F8', edge='#2B6CB0')
    draw_box(22, 25, 18, 30, "Instruction\nMemory\n(IMEM)\n32-bit Words", color='#EBF8FF', edge='#3182CE')
    draw_box(48, 48, 16, 22, "Main\nControl\nUnit", color='#FEFCBF', edge='#D69E2E')
    draw_box(48, 15, 20, 28, "Register\nFile\n(32x32-bit)\nRead/Write", color='#E2E8F0', edge='#4A5568')
    draw_box(74, 5, 14, 12, "Sign\nExtend\n16 to 32", color='#EDF2F7', edge='#718096')
    draw_box(92, 16, 18, 24, "32-bit\nALU", color='#FED7D7', edge='#E53E3E')
    draw_box(92, 45, 16, 12, "ALU\nControl", color='#FEEBC8', edge='#DD6B20')
    draw_box(116, 16, 18, 26, "Data\nMemory\n(DMEM)\n1024 Bytes", color='#C6F6D5', edge='#38A169')

    # Arrows and interconnects
    def draw_arrow(x1, y1, x2, y2, label="", color='#2D3748', lpos='mid'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
        if label:
            lx = (x1 + x2)/2
            ly = (y1 + y2)/2 + 1.2
            ax.text(lx, ly, label, fontsize=8, color=color, fontweight='bold', ha='center')

    # PC -> IMEM
    draw_arrow(16, 40, 22, 40, "PC[31:0]")
    # IMEM -> Control Unit & RegFile & SignExtend
    draw_arrow(40, 48, 48, 55, "Op[31:26]")
    draw_arrow(40, 35, 48, 35, "rs, rt")
    draw_arrow(40, 15, 74, 11, "Imm[15:0]")
    # Control Unit -> ALU Control & Datapath
    draw_arrow(64, 55, 92, 51, "ALUOp[1:0]", color='#C53030')
    # RegFile -> ALU
    draw_arrow(68, 32, 92, 32, "ReadData1")
    draw_arrow(68, 22, 92, 22, "ReadData2")
    # ALU -> DMEM
    draw_arrow(110, 28, 116, 28, "ALUResult")
    # DMEM -> Write-Back
    draw_arrow(125, 16, 125, 2)
    draw_arrow(125, 2, 58, 2)
    draw_arrow(58, 2, 58, 15, "WriteBack Data", color='#2B6CB0')

    plt.tight_layout()
    plt.savefig("diagrams/datapath_architecture.png", dpi=300)
    plt.close()

def create_control_unit_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis('off')

    ax.text(50, 65, "MIPS Main Control Unit Signal Flow", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1A365D')

    # Opcode input
    rect = patches.FancyBboxPatch((5, 25), 18, 15, boxstyle="round,pad=0.5", 
                                  facecolor='#BEE3F8', edgecolor='#2B6CB0', linewidth=1.8)
    ax.add_patch(rect)
    ax.text(14, 32.5, "Instruction\nOpcode\n[31:26]", ha='center', va='center', 
            fontsize=10, fontweight='bold')

    # Control Decoder
    rect = patches.FancyBboxPatch((32, 10), 30, 45, boxstyle="round,pad=0.5", 
                                  facecolor='#FEFCBF', edgecolor='#D69E2E', linewidth=2)
    ax.add_patch(rect)
    ax.text(47, 32.5, "Main Control\nDecoder Logic\n\n(Combinational)", ha='center', va='center', 
            fontsize=12, fontweight='bold', color='#744210')

    # Arrow from Opcode to Decoder
    ax.annotate('', xy=(32, 32.5), xytext=(23, 32.5),
                arrowprops=dict(arrowstyle="->", color='#2D3748', lw=2))

    # Control outputs
    outputs = [
        ("RegDst", 52, "Selects rd vs rt for write register"),
        ("ALUSrc", 47, "Selects Register vs Sign-Ext Immediate"),
        ("MemtoReg", 42, "Selects ALU result vs Data Memory"),
        ("RegWrite", 37, "Enables Register File write on posedge"),
        ("MemRead", 32, "Enables Data Memory combinational read"),
        ("MemWrite", 27, "Enables Data Memory write on posedge"),
        ("Branch", 22, "Enables BEQ target PC branch logic"),
        ("Jump", 17, "Selects 26-bit Jump target address"),
        ("ALUOp[1:0]", 12, "2-bit operation category to ALU Control")
    ]

    for name, y, desc in outputs:
        ax.annotate('', xy=(72, y), xytext=(62, y),
                    arrowprops=dict(arrowstyle="->", color='#C53030', lw=1.5))
        ax.text(73, y, f"{name:11s} - {desc}", fontsize=9, fontweight='bold', 
                color='#1A202C', va='center')

    plt.tight_layout()
    plt.savefig("diagrams/control_unit_flow.png", dpi=300)
    plt.close()

def create_alu_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis('off')

    ax.text(50, 65, "32-Bit Arithmetic Logic Unit (ALU) Architecture", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1A365D')

    # ALU Block (symbolic shape)
    alu_poly = patches.Polygon([[40, 52], [65, 42], [65, 18], [40, 8], [40, 24], [46, 30], [40, 36]],
                               closed=True, facecolor='#FED7D7', edgecolor='#E53E3E', linewidth=2)
    ax.add_patch(alu_poly)
    ax.text(53, 30, "32-bit\nALU", ha='center', va='center', fontsize=12, fontweight='bold', color='#9B2C2C')

    # Inputs A & B
    ax.annotate('', xy=(40, 44), xytext=(20, 44), arrowprops=dict(arrowstyle="->", color='#2D3748', lw=2))
    ax.text(18, 44, "Operand A [31:0]", ha='right', va='center', fontsize=10, fontweight='bold')

    ax.annotate('', xy=(40, 16), xytext=(20, 16), arrowprops=dict(arrowstyle="->", color='#2D3748', lw=2))
    ax.text(18, 16, "Operand B [31:0]", ha='right', va='center', fontsize=10, fontweight='bold')

    # ALU Control input
    ax.annotate('', xy=(52.5, 47), xytext=(52.5, 58), arrowprops=dict(arrowstyle="->", color='#C53030', lw=2))
    ax.text(52.5, 60, "ALU_Ctrl [3:0]", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#C53030')

    # Outputs Result & Zero
    ax.annotate('', xy=(85, 36), xytext=(65, 36), arrowprops=dict(arrowstyle="->", color='#2D3748', lw=2))
    ax.text(87, 36, "ALU Result [31:0]", ha='left', va='center', fontsize=10, fontweight='bold')

    ax.annotate('', xy=(85, 24), xytext=(65, 24), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2))
    ax.text(87, 24, "Zero Flag (Result == 0)", ha='left', va='center', fontsize=10, fontweight='bold', color='#2B6CB0')

    # Internal operations list
    ax.text(12, 30, "Supported Operations:\n• ADD  (0010)\n• SUB  (0110)\n• AND  (0000)\n• OR   (0001)\n• SLT  (0111)", 
            fontsize=9, va='center', bbox=dict(boxstyle='square,pad=0.5', facecolor='#F7FAFC', edgecolor='#CBD5E0'))

    plt.tight_layout()
    plt.savefig("diagrams/alu_architecture.png", dpi=300)
    plt.close()

def create_register_file_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis('off')

    ax.text(50, 65, "32x32-bit Register File Architecture", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1A365D')

    rect = patches.FancyBboxPatch((35, 12), 32, 45, boxstyle="round,pad=0.5", 
                                  facecolor='#E2E8F0', edgecolor='#4A5568', linewidth=2)
    ax.add_patch(rect)
    ax.text(51, 35, "Register Array\n[31:0] x 32\n\n$zero hardwired\nto 32'h00000000", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#2D3748')

    # Inputs on the left
    ax.annotate('', xy=(35, 50), xytext=(15, 50), arrowprops=dict(arrowstyle="->", color='#2D3748', lw=1.5))
    ax.text(14, 50, "read_reg1 [4:0] (rs)", ha='right', va='center', fontsize=9, fontweight='bold')

    ax.annotate('', xy=(35, 40), xytext=(15, 40), arrowprops=dict(arrowstyle="->", color='#2D3748', lw=1.5))
    ax.text(14, 40, "read_reg2 [4:0] (rt)", ha='right', va='center', fontsize=9, fontweight='bold')

    ax.annotate('', xy=(35, 30), xytext=(15, 30), arrowprops=dict(arrowstyle="->", color='#2D3748', lw=1.5))
    ax.text(14, 30, "write_reg [4:0] (rd/rt)", ha='right', va='center', fontsize=9, fontweight='bold')

    ax.annotate('', xy=(35, 20), xytext=(15, 20), arrowprops=dict(arrowstyle="->", color='#2D3748', lw=1.5))
    ax.text(14, 20, "write_data [31:0]", ha='right', va='center', fontsize=9, fontweight='bold')

    ax.annotate('', xy=(51, 12), xytext=(51, 3), arrowprops=dict(arrowstyle="->", color='#C53030', lw=1.5))
    ax.text(51, 1, "clk, rst, reg_write", ha='center', va='top', fontsize=9, fontweight='bold', color='#C53030')

    # Outputs on the right
    ax.annotate('', xy=(85, 45), xytext=(67, 45), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=1.5))
    ax.text(87, 45, "read_data1 [31:0] (Combinational)", ha='left', va='center', fontsize=9, fontweight='bold')

    ax.annotate('', xy=(85, 25), xytext=(67, 25), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=1.5))
    ax.text(87, 25, "read_data2 [31:0] (Combinational)", ha='left', va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig("diagrams/register_file_architecture.png", dpi=300)
    plt.close()

def create_instruction_flow_diagram():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 60)
    ax.axis('off')

    ax.text(60, 54, "Single-Cycle MIPS Instruction Execution Flow", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1A365D')

    stages = [
        ("1. Instruction Fetch (IF)", "PC -> IMEM\nFetch 32-bit Inst\nCompute PC + 4", 10, '#BEE3F8', '#2B6CB0'),
        ("2. Decode & Reg Read (ID)", "Decode Opcode\nRead rs, rt registers\nSign-extend Imm16", 34, '#FEFCBF', '#D69E2E'),
        ("3. Execute (EX)", "ALU Operation\nBranch target calc\nZero flag generation", 58, '#FED7D7', '#E53E3E'),
        ("4. Memory Access (MEM)", "LW read data\nSW write data\nWord-aligned address", 82, '#C6F6D5', '#38A169'),
        ("5. Write Back (WB)", "Select ALU or Mem\nWrite to rd/rt\nUpdate PC for next cycle", 106, '#E2E8F0', '#4A5568')
    ]

    for title, desc, cx, bg, border in stages:
        rect = patches.FancyBboxPatch((cx-10, 15), 20, 28, boxstyle="round,pad=0.5",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(cx, 38, title, ha='center', va='center', fontsize=9, fontweight='bold', color='#1A202C')
        ax.text(cx, 25, desc, ha='center', va='center', fontsize=8, color='#4A5568', multialignment='center')

        if cx < 100:
            ax.annotate('', xy=(cx+14, 29), xytext=(cx+10, 29),
                        arrowprops=dict(arrowstyle="->", color='#2D3748', lw=2))

    ax.text(60, 6, "Single-Cycle Execution: All 5 conceptual stages complete within ONE clock period (10 ns / 100 MHz)", 
            ha='center', va='center', fontsize=10, style='italic', color='#4A5568')

    plt.tight_layout()
    plt.savefig("diagrams/instruction_flow.png", dpi=300)
    plt.close()

def create_memory_interface_diagram():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 70)
    ax.axis('off')

    ax.text(55, 65, "MIPS CPU Core and Memory Subsystem Interface", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1A365D')

    # CPU Core
    rect_cpu = patches.FancyBboxPatch((10, 12), 35, 45, boxstyle="round,pad=0.5",
                                      facecolor='#EBF8FF', edgecolor='#3182CE', linewidth=2)
    ax.add_patch(rect_cpu)
    ax.text(27.5, 34.5, "MIPS CPU Core\n(Datapath &\nControl Unit)", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#2B6CB0')

    # Instruction Memory
    rect_imem = patches.FancyBboxPatch((65, 40), 35, 20, boxstyle="round,pad=0.5",
                                       facecolor='#EDF2F7', edgecolor='#4A5568', linewidth=1.8)
    ax.add_patch(rect_imem)
    ax.text(82.5, 50, "Instruction Memory\n(IMEM - ROM)\n256 Words (1024 Bytes)", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#2D3748')

    # Data Memory
    rect_dmem = patches.FancyBboxPatch((65, 10), 35, 22, boxstyle="round,pad=0.5",
                                       facecolor='#C6F6D5', edgecolor='#38A169', linewidth=1.8)
    ax.add_patch(rect_dmem)
    ax.text(82.5, 21, "Data Memory\n(DMEM - RAM)\n256 Words (1024 Bytes)", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#22543D')

    # IMEM connections
    ax.annotate('', xy=(65, 53), xytext=(45, 53), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=1.8))
    ax.text(55, 55, "pc [31:0]", ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.annotate('', xy=(45, 45), xytext=(65, 45), arrowprops=dict(arrowstyle="->", color='#4A5568', lw=1.8))
    ax.text(55, 43, "inst [31:0]", ha='center', va='top', fontsize=8, fontweight='bold')

    # DMEM connections
    ax.annotate('', xy=(65, 27), xytext=(45, 27), arrowprops=dict(arrowstyle="->", color='#C53030', lw=1.8))
    ax.text(55, 29, "mem_addr [31:0]", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#C53030')

    ax.annotate('', xy=(65, 21), xytext=(45, 21), arrowprops=dict(arrowstyle="->", color='#C53030', lw=1.8))
    ax.text(55, 22.5, "mem_write_data", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#C53030')

    ax.annotate('', xy=(45, 14), xytext=(65, 14), arrowprops=dict(arrowstyle="->", color='#276749', lw=1.8))
    ax.text(55, 12, "mem_read_data", ha='center', va='top', fontsize=8, fontweight='bold', color='#276749')

    plt.tight_layout()
    plt.savefig("diagrams/memory_interface.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    create_datapath_diagram()
    create_control_unit_diagram()
    create_alu_diagram()
    create_register_file_diagram()
    create_instruction_flow_diagram()
    create_memory_interface_diagram()
    print("All architecture diagrams generated successfully in diagrams/")
