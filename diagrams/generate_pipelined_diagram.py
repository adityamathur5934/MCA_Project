#!/usr/bin/env python3
"""
Generate professional architectural diagram for the 5-Stage Pipelined MIPS Processor.
Generates: diagrams/pipelined_architecture.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_pipelined_diagram():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 90)
    ax.axis('off')

    # Title
    ax.text(80, 86, "5-Stage Pipelined MIPS Processor Architecture (Final Phase)", 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1A365D')
    ax.text(80, 82.5, "Integrated with Data Forwarding Unit, Hazard Detection Unit, and Harvard Memory Interface", 
            ha='center', va='center', fontsize=11, fontstyle='italic', color='#4A5568')

    def draw_box(x, y, w, h, text, color='#E2E8F0', edge='#2B6CB0', text_color='#1A202C', fsize=9):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", 
                                      facecolor=color, edgecolor=edge, linewidth=1.6)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                fontsize=fsize, fontweight='bold', color=text_color, multialignment='center')

    def draw_pipe_reg(x, y, w, h, text):
        rect = patches.Rectangle((x, y), w, h, facecolor='#2D3748', edgecolor='#1A202C', linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                fontsize=11, fontweight='bold', color='#FFFFFF', rotation=90)

    # 5 Stages Background Bands
    stage_colors = ['#EBF8FF', '#FEFCBF', '#FED7D7', '#C6F6D5', '#E9D8FD']
    stage_names = ['1. FETCH (IF)', '2. DECODE (ID)', '3. EXECUTE (EX)', '4. MEMORY (MEM)', '5. WRITE-BACK (WB)']
    stage_x = [4, 34, 68, 102, 134]
    stage_w = [24, 28, 28, 26, 22]

    for i in range(5):
        rect = patches.Rectangle((stage_x[i], 12), stage_w[i], 66, facecolor=stage_colors[i], alpha=0.35, edgecolor='#CBD5E0', linestyle='--')
        ax.add_patch(rect)
        ax.text(stage_x[i] + stage_w[i]/2, 75, stage_names[i], ha='center', va='center', fontsize=10, fontweight='bold', color='#2D3748')

    # IF Stage
    draw_box(6, 42, 8, 18, "PC\nRegister", color='#BEE3F8', edge='#2B6CB0')
    draw_box(16, 36, 10, 28, "Instruction\nMemory\n(IMEM)", color='#EBF8FF', edge='#3182CE')

    # IF/ID Register
    draw_pipe_reg(29.5, 14, 3, 62, "IF / ID")

    # ID Stage
    draw_box(36, 54, 12, 16, "Main\nControl\nUnit", color='#FEFCBF', edge='#D69E2E')
    draw_box(36, 26, 14, 24, "Register\nFile\n(32x32-bit)", color='#EDF2F7', edge='#4A5568')
    draw_box(36, 14, 12, 9, "Sign\nExtend", color='#EDF2F7', edge='#718096')

    # ID/EX Register
    draw_pipe_reg(63.5, 14, 3, 62, "ID / EX")

    # EX Stage
    draw_box(70, 56, 12, 14, "ALU\nControl", color='#FEEBC8', edge='#DD6B20')
    draw_box(74, 30, 16, 22, "32-bit\nALU", color='#FED7D7', edge='#E53E3E')
    draw_box(70, 14, 22, 12, "Forwarding\nUnit (Muxes)", color='#FEFCBF', edge='#B7791F')

    # EX/MEM Register
    draw_pipe_reg(97.5, 14, 3, 62, "EX / MEM")

    # MEM Stage
    draw_box(106, 28, 16, 26, "Data\nMemory\n(DMEM)", color='#C6F6D5', edge='#38A169')

    # MEM/WB Register
    draw_pipe_reg(129.5, 14, 3, 62, "MEM / WB")

    # WB Stage
    draw_box(136, 34, 14, 18, "MemtoReg\nMultiplexer", color='#E9D8FD', edge='#805AD5')

    # Top Units: Hazard Detection Unit
    draw_box(48, 70, 32, 7, "Hazard Detection Unit (Load-Use Stall & Branch Flush)", color='#FED7D7', edge='#C53030', text_color='#9B2C2C', fsize=8.5)

    # Connections and Arrows
    def draw_arrow(x1, y1, x2, y2, color='#2D3748', label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.4))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 1.2, label, fontsize=7.5, color=color, fontweight='bold', ha='center')

    draw_arrow(14, 50, 16, 50, color='#2B6CB0')
    draw_arrow(26, 50, 29.5, 50, color='#3182CE')
    draw_arrow(32.5, 50, 36, 50, color='#3182CE')
    draw_arrow(50, 38, 63.5, 38, color='#4A5568')
    draw_arrow(66.5, 41, 74, 41, color='#E53E3E')
    draw_arrow(90, 41, 97.5, 41, color='#E53E3E')
    draw_arrow(100.5, 41, 106, 41, color='#38A169')
    draw_arrow(122, 41, 129.5, 41, color='#38A169')
    draw_arrow(132.5, 41, 136, 41, color='#805AD5')

    # Write-Back Feedback loop to RegFile
    ax.annotate('', xy=(42, 26), xytext=(143, 34),
                arrowprops=dict(arrowstyle="->", color='#805AD5', lw=1.6, connectionstyle="arc3,rad=-0.25"))
    ax.text(90, 6, "Write-Back Data Bus (WB -> Register File)", fontsize=9, color='#805AD5', fontweight='bold', ha='center')

    # Forwarding paths
    ax.annotate('', xy=(78, 14), xytext=(102, 35),
                arrowprops=dict(arrowstyle="->", color='#D69E2E', lw=1.4, linestyle=':'))
    ax.annotate('', xy=(84, 14), xytext=(134, 38),
                arrowprops=dict(arrowstyle="->", color='#D69E2E', lw=1.4, linestyle=':'))

    plt.tight_layout()
    plt.savefig("diagrams/pipelined_architecture.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated diagrams/pipelined_architecture.png")

if __name__ == '__main__':
    create_pipelined_diagram()
