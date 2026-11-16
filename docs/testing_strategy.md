# Testing and Verification Strategy

## 1. Verification Philosophy
The verification framework follows a hierarchical, bottom-up methodology:
1. **Unit-Level Testing:** Isolated unit testbenches for critical blocks (`alu`, `control_unit`, `register_file`, `data_memory`).
2. **Instruction-Level Verification:** Automated sequential testing of all 10 supported instructions with deterministic expected results.
3. **Application-Level System Testing:** Execution of real algorithmic workloads (`array_sum`, `maximum_search`, `factorial`) running on the complete CPU with Harvard memory interface.

---

## 2. Testbench Architecture

### Self-Checking Mechanism
Every testbench utilizes automated assertion tasks:
```verilog
task assert_test;
    input              condition;
    input [8*40-1:0]   test_name;
    input [31:0]       observed;
    input [31:0]       expected;
    begin
        test_id = test_id + 1;
        if (condition) begin
            $display("[PASS] Test %2d: %s | Observed: 0x%08h (%0d)",
                     test_id, test_name, observed, observed);
            tests_passed = tests_passed + 1;
        end else begin
            $display("[FAIL] Test %2d: %s | Got: 0x%08h (%0d) | Expected: 0x%08h (%0d)",
                     test_id, test_name, observed, observed, expected, expected);
            tests_failed = tests_failed + 1;
        end
    end
endtask
```
Any mismatch immediately logs an error, increments the failure counter, and causes non-zero exit codes.

---

## 3. Waveform Generation and Inspection
All testbenches automatically generate IEEE standard Value Change Dump (`.vcd`) files:
- `simulation/waveforms/tb_alu.vcd`
- `simulation/waveforms/tb_control_unit.vcd`
- `simulation/waveforms/tb_register_file.vcd`
- `simulation/waveforms/tb_data_memory.vcd`
- `simulation/waveforms/tb_mips_cpu.vcd`

### Key Signals Probed in GTKWave:
1. `pc[31:0]`: Verifies sequential +4 increment, branch offsets, and jump targets.
2. `instruction[31:0]`: Decoded machine instruction.
3. `alu_result[31:0]`: Arithmetic result and computed memory addresses.
4. `read_data1[31:0]`, `read_data2[31:0]`: Register file read buses.
5. `reg_write_data[31:0]`: Selected write-back value from ALU or Data Memory.
6. `zero`: Zero flag controlling branch decisions.
7. `mem_write`, `mem_read`: Data memory strobe signals.
