# 🎤 Single-Cycle MIPS Processor with Memory Interface
## 10-Minute Slide-by-Slide Presentation Script (Hinglish) & Viva Q&A Guide

Aligned 1-to-1 with the 9 slides of `presentation/prototype_presentation.pptx`.

---

## ⏱️ Slide-by-Slide Timing Roadmap (Total: 9 - 10 Minutes)

| Slide | Slide Title | Recommended Time | Cumulative Time |
| :---: | :--- | :---: | :---: |
| **Slide 1** | Title & Team Members | 0:45 min | 0:45 |
| **Slide 2** | Problem Statement & Project Objectives | 1:00 min | 1:45 |
| **Slide 3** | Single-Cycle MIPS Architecture & Datapath | 1:15 min | 3:00 |
| **Slide 4** | Modular Verilog RTL Hierarchy | 1:15 min | 4:15 |
| **Slide 5** | Supported ISA & Control Unit Decoding Matrix | 1:15 min | 5:30 |
| **Slide 6** | Simulation Methodology & Automated Testbenches | 1:00 min | 6:30 |
| **Slide 7** | Benchmark Program: Array Summation (& Additional Programs) | 1:15 min | 7:45 |
| **Slide 8** | Waveform Analysis & Hardware Verification | 1:00 min | 8:45 |
| **Slide 9** | Conclusion & Future Scope | 0:45 min | 9:30 |
| **Buffer**| Q&A Transition & Panel Questions | 0:30 min | 10:00 |

---

## 🗣️ Slide-by-Slide Presentation Script (Hinglish)

---

### 📌 Slide 1: Title & Team Members
**Slide Title:** *Single-Cycle MIPS Processor with Memory Interface*  
**Visuals on Slide:** Project Title, Subtitle (Hardware Design, Verilog Implementation, and Full System Verification), Team Members & Roles list.  
**Estimated Time:** ~45 seconds  

> *"Respected professors and panel members, good morning / afternoon.*  
>
> *Aaj hum present karne ja rahe hain hamara project: **Single-Cycle MIPS Processor with Memory Interface**.*  
>
> *Is project mein humne ek complete 32-bit RISC microprocessor architecture ko synthesizable Verilog HDL mein ground-up design aur verify kiya hai.*  
>
> *Hamari team ne is project ko modular tarike se distribute kiya tha:*
> * Architecture and Datapath Integration,
> * ALU, Control Unit, and Register File design,
> * Memory Subsystems, Verification, aur Technical Documentation.*  
>
> *Chaliye ab project ke main objectives aur problem statement par chalte hain."*

---

### 📌 Slide 2: Problem Statement & Project Objectives
**Slide Title:** *Problem Statement & Project Objectives*  
**Visuals on Slide:** 4 Bullets (Context & Challenge, Primary Objectives, Key Architectural Requirements, Phase I Verification Target).  
**Estimated Time:** ~1 minute  

> *"Slide 2 par aap dekh sakte hain hamara **Problem Statement aur Objectives**.*  
>
> * **Context & Challenge:** Computer architecture mein hardware aur software ke beech ka bridge samajhna sabse critical hota hai. Hamara goal tha ek practical 32-bit processor design karna jo software assembly instructions ko physical digital circuits aur control signals ke through accurately execute kare.
> * **Primary Objectives:** Humne Verilog 2001 standard mein ek single-cycle MIPS processor develop kiya jo 10 essential instructions support karta hai — spanning R-Type, I-Type, aur J-Type.
> * **Key Architectural Requirements:**
>   1. Full 32 general-purpose registers jisme Register `$0` ($zero) hardware level par zero par locked hai.
>   2. Harvard Architecture — yaani separate Instruction Memory aur Data Memory taaki single clock cycle mein memory hazard na aaye.
>   3. Combinational branch aur jump calculation without any unintended latches.
> * **Verification Target:** Hamara target tha 100% automated self-checking testbench coverage achieve karna aur 3 real-world benchmark programs successfully execute karna — **Array Sum** (Result: 100), **Maximum Search** (Result: 67), aur **Factorial** (Result: 120)."*

---

### 📌 Slide 3: Single-Cycle MIPS Architecture & Datapath
**Slide Title:** *Single-Cycle MIPS Architecture & Datapath*  
**Visuals on Slide:** Left side bullets (Harvard Subsystem, Next-PC Calculation, Write-Back Multiplexing); Right side datapath diagram (`datapath_architecture.png`).  
**Estimated Time:** ~1 minute 15 seconds  

> *"Slide 3 par hamara **Single-Cycle Datapath Architecture** ka schematic diagram hai.*  
>
> *'Single-Cycle' ka fundamental principle yeh hai ki **har instruction exactly ek clock cycle mein execute hoti hai** — instruction fetch, decode, ALU execution, memory access, aur register write-back.*  
>
> *Yahan 3 core datapath concepts highlight karne layak hain:*
> 1. **Harvard Memory Subsystem:** Instruction Memory aur Data Memory physically separate hain. Jab CPU current cycle mein instruction fetch karta hai, usi cycle mein Data Memory se `LW` ya `SW` access bina collision ke ho sakta hai.
> 2. **Next-PC Calculation Logic:**
>    * Normally, `PC` har cycle mein `PC + 4` hota hai kyunki MIPS byte-addressable hai aur har instruction 4 bytes ki hoti hai.
>    * Agar `BEQ` (Branch if Equal) instruction aati hai aur dono registers equal hote hain, to branch target calculate hota hai: $(\text{PC} + 4) + (\text{Sign-Extended Immediate} \times 4)$.
>    * Agar `J` (Jump) instruction aati hai, to direct 26-bit target address ko shift karke jump target assign hota hai.
> 3. **Write-Back Multiplexer (`MemtoReg`):**
>    * R-Type ya `ADDI` ke case mein ALU result wapas register mein likha jata hai.
>    * `LW` ke case mein Data Memory ka read data register mein likha jata hai."*

---

### 📌 Slide 4: Modular Verilog RTL Hierarchy
**Slide Title:** *Modular Verilog RTL Hierarchy*  
**Visuals on Slide:** Left list of 10 Verilog modules with descriptions; Right side memory interface diagram (`memory_interface.png`).  
**Estimated Time:** ~1 minute 15 seconds  

> *"Slide 4 par hamare design ki **Modular Verilog RTL Hierarchy** listed hai. Humne code ko monolithic nahi banaya, balki clean modules mein divide kiya hai:*
>
> 1. **`program_counter.v`:** 32-bit register jo synchronous reset par `0x00000000` par initialize hota hai.
> 2. **`instruction_memory.v`:** 256-word ROM jo hex file se code load karke combinational read deti hai.
> 3. **`control_unit.v`:** Opcode decode karke saare 9 multiplexer control signals generate karta hai.
> 4. **`register_file.v`:** 32x32-bit dual read ports aur single synchronous write port.
> 5. **`sign_extend.v`:** 16-bit immediate values ko sign-bit ke sath 32-bit 2's complement mein extend karta hai.
> 6. **`alu.v` & `alu_control.v`:** Core arithmetic/logical engine jo addition, subtraction, AND, OR, aur SLT perform karta hai, plus zero flag generate karta hai.
> 7. **`data_memory.v`:** 256-word RAM with synchronous write (`mem_write`) aur asynchronous read (`mem_read`).
> 8. **`mips_cpu.v`:** Core datapath aur internal multiplexers ko connect karta hai.
> 9. **`top_module.v`:** Top-level wrapper jo CPU, Instruction Memory aur Data Memory ko interconnect karta hai aur debug signals bahar expose karta hai."*

---

### 📌 Slide 5: Supported ISA & Control Unit Decoding Matrix
**Slide Title:** *Supported ISA & Control Unit Decoding Matrix*  
**Visuals on Slide:** Bullets (Complete 10-Instruction Scope, Single-Level Decoding, Safe Default Guarantees); Control unit flow diagram (`control_unit_flow.png`).  
**Estimated Time:** ~1 minute 15 seconds  

> *"Slide 5 par processor ka instruction set aur **Control Unit Decoding Logic** hai.*  
>
> *Hamara processor 10 standard MIPS instructions ko support karta hai:*
> * **5 R-Type:** `ADD`, `SUB`, `AND`, `OR`, `SLT`
> * **4 I-Type:** `ADDI` (arithmetic with immediate), `LW` (load word), `SW` (store word), `BEQ` (branch if equal)
> * **1 J-Type:** `J` (unconditional jump)
>
> * **Control Unit Working:**  
>   * Instruction ke top 6 bits `inst[31:26]` (Opcode) ko decode kiya jata hai.
>   * R-Type instructions mein Opcode `000000` hota hai. Yahan Control Unit `RegDst = 1`, `RegWrite = 1`, aur `ALUSrc = 0` set karta hai, aur exact operation decide karne ke liye ALU Control module instruction ke bottom 6 bits (`funct`) ko read karta hai.
>   * `LW` ke liye: `ALUSrc = 1` (immediate offset), `MemRead = 1`, `MemtoReg = 1`, aur `RegWrite = 1`.
>   * `SW` ke liye: `ALUSrc = 1`, `MemWrite = 1`, aur `RegWrite = 0` taaki register file overwrite na ho.
>   * `BEQ` ke liye: `Branch = 1`, `ALUSrc = 0`.
>
> *Sabse important: Kisi bhi undefined opcode ke aane par saare write enables (`RegWrite`, `MemWrite`) automatically 0 par latch-free default ho jate hain, jisse hardware safety ensure hoti hai."*

---

### 📌 Slide 6: Simulation Methodology & Automated Testbenches
**Slide Title:** *Simulation Methodology & Automated Testbenches*  
**Visuals on Slide:** 4 Bullets (Verification Environment, Hierarchical Testing, 100% Verification Coverage, Robust Corner-Case Validation).  
**Estimated Time:** ~1 minute  

> *"Slide 6 par aati hai hamari **Simulation & Verification Strategy**.*  
>
> * *Verification Environment:* Humne open-source **Icarus Verilog (`iverilog`)** aur **GTKWave** use kiya hai. Humne testbench ko purely automated banaya hai using programmatic `assert_test` tasks.
> * *Hierarchical Bottom-Up Testing:* Humne direct top module test karne ke bajaye pehle individual unit testbenches banaye — ALU, Control Unit, Register File, aur Data Memory ke liye. Jab units pass ho gaye, tab full CPU integration testbench run kiya.
> * *100% Test Coverage:* Unit tests aur full system tests mila kar total **57 assertions** run huye, aur sabhi 57 assertions **PASS** huye with zero errors.
> * *Corner-Cases Tested:*
>   1. Signed negative numbers: `-5 + 25 = 20` and `-10 < 5` (SLT correctly set to 1).
>   2. Register `$0` protection: `$0` par write instruction execute karne ke baad bhi `$0` hamesha 0 raha.
>   3. Branch take vs not-take conditions accurate test huyi."*

---

### 📌 Slide 7: Benchmark Program: Array Summation (& Additional Programs)
**Slide Title:** *Benchmark Program: Array Summation (Mandatory)*  
**Visuals on Slide:** Left side: Program Objective, Instructions Used, Execution Performance; Right side: Expected vs Observed Result (Mem[16] = 100, $t1 = 100) + Extra programs (Max Search = 67, Factorial = 120).  
**Estimated Time:** ~1 minute 15 seconds  

> *"Slide 7 hamari evaluation ka sabse crucial proof hai: **Real-World Benchmark Programs**.*  
>
> *Humne ek custom Python assembler script (`assemble.py`) likhi jo MIPS assembly code ko 32-bit machine code hexadecimal instructions mein convert karti hai.*  
>
> 1. **Array Summation (Mandatory Benchmark):**
>    * Array values `10, 20, 30, 40` data memory mein store the.
>    * Program ne loop chala kar `LW`, `ADD`, `ADDI`, `BEQ`, `SW`, aur `J` instructions execute ki.
>    * **Result:** Total sum $100$ (`0x00000064`) Data Memory address 16 aur register `$t1` dono par calculate hua aur testbench ne automatically **PASS** assert kiya.
>
> 2. **Additional Benchmarks:**
>    * **Maximum Search:** Array `[12, 45, 23, 67, 34]` par loop chalaya using `SLT` instruction $\rightarrow$ Maximum value $67$ (`0x43`) accurately find huyi.
>    * **Factorial Calculation:** $5!$ calculate kiya $\rightarrow$ Result $120$ (`0x78`) Data Memory address 0 par successfully store hua."*

---

### 📌 Slide 8: Waveform Analysis & Hardware Verification
**Slide Title:** *Waveform Analysis & Hardware Verification*  
**Visuals on Slide:** Left bullets (Waveform Evidence, Signal Timing Analysis, Glitch & Hazard Free); Right side: Instruction timing flow diagram (`instruction_flow.png`).  
**Estimated Time:** ~1 minute  

> *"Slide 8 par **Waveform Analysis** aur signal timing verification hai.*  
>
> * *Waveform Evidence:* Simulation run hone par Value Change Dump (`.vcd`) file generate hoti hai jo 225 simulation cycles ko capture karti hai.
> * *GTKWave Setup:* Humne demonstration ke liye ek dedicated GTKWave save file `mips_demo.gtkw` create ki hai. Examiner screen par single command se saare 15 vital signals hex radix mein auto-load ho jaate hain.
> * *Timing Stability:*
>   * Clock ke positive edge par PC cleanly update hota hai.
>   * Asynchronous instruction memory read se clock high period ke dauraan valid instruction decode ho jaati hai.
>   * ALU result aur memory output next positive clock edge se pehle setup time maintain karte huye stably settle ho jaate hain.
>   * Control signals (`mem_write`, `reg_write`) par koi glitch ya unknown (`X` / `Z`) values nahi aati."*

---

### 📌 Slide 9: Conclusion & Phase II Future Scope
**Slide Title:** *Conclusion & Phase II Future Scope*  
**Visuals on Slide:** 3 Bullets (Phase I Achievements, Phase I Evaluation Deliverables Completed, Phase II Roadmap & Enhancements).  
**Estimated Time:** ~45 seconds  

> *"Slide 9 par hum conclude karte hain hamare project ko.*  
>
> * **Phase I Deliverables Completed:**
>   * Hamara 32-bit Single-Cycle MIPS processor 100% synthesizable aur functionally verified hai.
>   * Saari 10 instructions, Harvard memory interface, automated testbenches, IEEE project report, presentation deck, aur GTKWave automated waveforms fully prepared hain.
>
> * **Future Roadmap:**
>   * Agle phase mein is single-cycle processor ko classic **5-stage pipeline architecture** (IF, ID, EX, MEM, WB) mein upgrade kiya ja sakta hai with forwarding and hazard detection units taaki clock frequency aur throughput significantly increase ho sake.
>   * Sath hi shift instructions (`SLL`, `SRL`), function calls (`JAL`, `JR`), aur FPGA deployment (Xilinx Artix-7 board par 7-segment display ke sath) implement kiya ja sakta hai.
>
> *Thank you very much. We are now ready to take your questions."*

---

## 🎓 High-Yield Viva Voce Q&A (Directly Aligned with the PPT)

### Q1: "Slide 3 par aapne Harvard Architecture batayi. Von Neumann Architecture kyu nahi use ki?"
* **Answer:**  
  * *"Single-Cycle processor mein **ek hi clock cycle** ke andar Instruction Fetch (IMEM se) aur Data Memory Access (LW/SW ke time DMEM se) dono simultaneously hote hain.*  
  * *Agar hum Von Neumann (single shared memory) use karte, to ek single memory bus par do alag addresses ek sath access nahi ho sakte the (Structural Hazard). Isliye single-cycle design mein separate Instruction Memory aur Data Memory hona compulsory hai."*

---

### Q2: "Slide 3 par Next-PC calculation mein branch target address kaise nikalta hai?"
* **Answer:**  
  * *"Formula hota hai: $\text{Branch Target} = (\text{PC} + 4) + (\text{Sign-Extended Immediate} \times 4)$.*  
  * *Yahan 3 cheezein hoti hain:*
    1. *Pehele immediate 16-bit field ko 32-bit sign-extend karte hain.*
    2. *Fir usko 2 bits left-shift karte hain (yaani $\times 4$) kyunki MIPS branch offset word count hota hai, jabki PC byte-addressable hai.*
    3. *Fir usse $(\text{PC} + 4)$ mein add karte hain.*
    4. *Agar ALU ka `zero` flag high ho aur Control Unit ka `Branch` signal high ho, to MUX branch target ko choose kar leta hai."*

---

### Q3: "Slide 5 par ALUOp aur funct field ka kya relation hai? (Two-level decoding kyu ki?)"
* **Answer:**  
  * *"Ise **Two-Level Decoding** kehte hain:*
    * *Main Control Unit pure 32 bits decode nahi karta; wo sirf 6-bit opcode dekh kar 2-bit `ALUOp` deta hai:*
      * `00` $\rightarrow$ `LW`/`SW` (addition for address)
      * `01` $\rightarrow$ `BEQ` (subtraction for zero flag)
      * `10` $\rightarrow$ R-Type instructions
    * *Jab `ALUOp = 10` hota hai, tab `alu_control` module instruction ke aakhiri 6 bits (`funct`) ko dekh kar final 4-bit `alu_ctrl` signal generate karta hai (jaise ADD ke liye `0010`, SUB ke liye `0110`, etc.).*  
  * *Isse control unit chhota aur fast rehta hai."*

---

### Q4: "Slide 2 par aapne likha hai ki Register `$0` ($zero) write-protected hai. Verilog mein yeh kaise implement kiya?"
* **Answer:**  
  * *"`register_file.v` ke andar synchronous write logic mein humne condition lagayi hai:*
    ```verilog
    if (reg_write && write_reg != 5'd0)
        registers[write_reg] <= write_data;
    ```
  * *Agar koi instruction destination register 0 par data write karne ki koshish kare (jaise `ADDI $0, $zero, 100`), to condition false ho jaati hai aur `$0` hamesha ground (`32'd0`) hi rehta hai."*

---

### Q5: "Single-Cycle Processor ka sabse bada disadvantage kya hota hai? (Critical Path kya hai?)"
* **Answer:**  
  * *"Sabse bada disadvantage hai **Poor Clock Frequency (Long Cycle Time)**.*  
  * *Clock period worst-case combinational delay se decide hota hai, jise **Critical Path** kehte hain. Hamare design mein critical path **`LW` (Load Word)** instruction hai:*
    $$\text{Delay} = T_{\text{PC}} + T_{\text{IMEM}} + T_{\text{RegRead}} + T_{\text{ALU}} + T_{\text{DMEM}} + T_{\text{MUX}} + T_{\text{RegSetup}}$$
  * *Kyunki har instruction ko ek hi cycle mein complete hona hai, isliye fast instructions (jaise `ADD` ya `BEQ`) ko bhi `LW` ke delay jitna lamba wait karna padta hai."*

---

### Q6: "Slide 7 par Array Sum program ka loop terminate kaise hua?"
* **Answer:**  
  * *"Loop counter register `$t2` ko 0 se initialize kiya aur loop boundary `$t3` ko 4 set kiya.*  
  * *Har iteration mein array element load karke sum accumulate kiya, pointer ko 4 bytes aage badhaya, aur counter `$t2` ko 1 se increment kiya.*  
  * *Har loop ke top par `BEQ $t3, $t2, end` check kiya. Jab `$t2 == 4` ho gaya, to ALU ne zero flag set kiya aur execution loop se bahar nikal kar result ko `SW` ke through memory address 16 par store kar diya."*

---

### Q7: "Slide 8 par aapne GTKWave ka zikr kiya. Examiner agar live wave dekhne ko kahe to kya command chalani hai?"
* **Answer:**  
  * *"Hum directly terminal mein run kar sakte hain:*  
    ```bash
    make wave
    ```  
    *ya direct command:*  
    ```bash
    gtkwave simulation/waveforms/tb_mips_cpu.vcd simulation/waveforms/mips_demo.gtkw
    ```  
  * *Isse GTKWave turant open hota hai aur 15 essential signals (Clock, Reset, PC, Instruction, ALU Result, Zero, Memory Read/Write, etc.) organized hex format mein samne aa jate hain."*

---

### 💡 Panel Delivery Pro-Tips:
1. **Slide sync:** Jab slide change ho, turant first line bol kar panel ka attention slide ke visual diagram par le aao (e.g. *"Slide 3 par datapath schematic hai...", "Slide 7 par Array Sum benchmark hai..."*).
2. **Numbers bolna:** Result values hamesha confidently bolo: *"Array Sum ka result 100 tha, Max search ka 67, aur Factorial ka 120"*. Examiner ko pata chalega ki aapne code run karke dekha hai.
3. **Pacing:** Slide 3 (Datapath) aur Slide 7 (Benchmarks) par thoda zyada time spend karo, wahan examiners sabse zyada questions poochte hain.
