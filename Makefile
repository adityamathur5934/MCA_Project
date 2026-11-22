# Makefile for Single‑Cycle MIPS Processor (Project 2)
# -------------------------------------------------------
# Usage:
#   make          # compile testbench and all RTL
#   make run      # execute simulation (generates VCD)
#   make wave     # open GTKWave with prepared configuration
#   make clean    # remove generated binaries and VCD files

SIM_DIR = simulation
SRC_DIR = src
TB_DIR  = testbench

# List of all RTL sources (single‑cycle only)
SRC = $(wildcard $(SRC_DIR)/*.v)

# Testbench source
TB = $(TB_DIR)/tb_mips_cpu.v

# Output files
OUT_EXE = $(SIM_DIR)/tb_mips_cpu.out
VCD    = $(SIM_DIR)/waveforms/tb_mips_cpu.vcd
GTKW   = $(SIM_DIR)/waveforms/mips_demo.gtkw

.PHONY: all run wave clean

all: $(OUT_EXE)

$(OUT_EXE): $(TB) $(SRC)
	@echo "Compiling single‑cycle MIPS testbench..."
	iverilog -g2005 -o $@ $^ || (echo "Compilation failed"; exit 1)

run: $(OUT_EXE)
	@echo "Running simulation..."
	vvp $< || (echo "Simulation failed"; exit 1)

wave: run
	@echo "Launching GTKWave..."
	gtkwave $(VCD) $(GTKW) || echo "GTKWave not available in this environment"

clean:
	rm -f $(OUT_EXE) $(VCD)
	echo "Cleaned generated files"
