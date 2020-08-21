#!/usr/bin/env python
# coding: utf-8

# BSD 2-Clause License

# Copyright (c) 2020, Bo-Yin Yang, Cheng-Jhih Shi, Chi-Ming Chung, Vincent Hwang
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

lin = """
/*
BSD 2-Clause License

Copyright (c) 2020, Bo-Yin Yang, Cheng-Jhih Shi, Chi-Ming Chung, Vincent Hwang
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

"""


macro = """.macro montgomery_mul a, b, lower, upper, tmp, M_inv, M
    smull.w \\lower, \\upper, \\a, \\b
    mul.w \\tmp, \\lower, \\M_inv
    smlal.w \\lower, \\upper, \\tmp, \\M
.endm

.macro add_sub a0, b0, a1, b1, a2, b2, a3, b3
    add \\a0, \\b0
    add \\a1, \\b1
    add \\a2, \\b2
    add \\a3, \\b3
    sub.w \\b0, \\a0, \\b0, lsl #1        
    sub.w \\b1, \\a1, \\b1, lsl #1        
    sub.w \\b2, \\a2, \\b2, lsl #1        
    sub.w \\b3, \\a3, \\b3, lsl #1        
.endm

.macro central_reduce target, Mhalf, M
    cmp \\target, \\Mhalf
    it gt
    subgt \\target, \\M
    cmn \\target, \\Mhalf
    it lt
    addlt \\target, \\M
.endm

.macro barret a, O_Mbar, O_M, tmp
    smmulr.w \\tmp, \\a, \\O_Mbar
    mls.w \\a, \\tmp, \\O_M, \\a
.endm

.macro unsigned_char target, Mhalf, M
    cmn \\target, \\Mhalf
    it lt
    addlt \\target, \\M
.endm
"""

start = """
.syntax unified
.cpu cortex-m4
"""

combine_1_2_3 = """
.align 2
.global NTT_1024
.type NTT_1024, %function

NTT_1024:
push.w {{r4-r12, r14}}
vpush.w {{s16, s17, s18}}

tmp_root_table .req s8
outer_counter  .req s9
inner_counter  .req s10
ary_input1     .req s11
ary_input2     .req s12
tmp_counter    .req s13
tmp_inv_table  .req s14
tmp_ans        .req s15
q_bar          .req s16
tmp_mul_table  .req s17
tmp_lr         .req s18

vldr.w ary_input2, [sp, #"""+str(40 + 4*3)+"""]
vldr.w tmp_inv_table, [sp, #"""+str(44 + 4*3)+"""]
vldr.w tmp_ans, [sp, #"""+str(48 + 4*3)+"""]
vldr.w q_bar, [sp, #"""+str(52 + 4*3)+"""]
vldr.w tmp_mul_table, [sp, #"""+str(56 + 4*3)+"""]
vldm.w r1!, {{s0-s6}}
vmov.w tmp_root_table, r1
vmov.w ary_input1, r0

// allocate NTTd array using sp
sub.w sp, #"""+str(8192)+"""
mov.w r0, sp

bl.w _1_2_3_big
add.w r0, #"""+str(4*1024-4*128)+""" // adjust r0

bl.w _1_2_3_small
sub.w r0, #"""+str(4*1024+4*128)+""" // adjust r0

bl.w _4_5_6
vmov.w r1, tmp_root_table
sub.w r1, """+str(4*7*8)+"""
vmov.w tmp_root_table, r1

bl.w _4_5_6
sub.w r0, #"""+str(4*2048)+""" // adjust r0

bl.w _7_8_9
vmov.w r1, tmp_root_table
sub.w r1, """+str(4*7*64)+"""
vmov.w tmp_root_table, r1

bl.w _7_8_9

sub.w r0, #"""+str(4*2048)+"""
bl.w my_mul // do mul and inverse


.align 2
_1_2_3_big:
vmov.w tmp_lr, lr

add.w r12, r0, #"""+str(4*128)+""" // set counter
vmov.w inner_counter, r12

.align 2
loop_1_2_3_big:
"""

for i in range(2):
    if i == 0:
        combine_1_2_3 += """
    vmov.w {c_temp}, ary_input1
    ldrb.w {a0}, [{c_temp}, #"""+str(0)+"""]
    ldrb.w {a64}, [{c_temp}, #"""+str(128)+"""]
    ldrb.w {a128}, [{c_temp}, #"""+str(256)+"""]
    ldrb.w {a192}, [{c_temp}, #"""+str(384)+"""]
    ldrb.w {a256}, [{c_temp}, #"""+str(512)+"""]
    ldrb.w {a320}, [{c_temp}, #"""+str(640)+"""]
    ldrb.w {a384}, [{c_temp}, #"""+str(768)+"""]
    ldrb.w {a448}, [{c_temp}, #"""+str(896)+"""]
    """
    else:
        combine_1_2_3 += """
    vmov.w {c_temp}, ary_input1
    ldrb.w {a0}, [{c_temp}, #"""+str(0+1)+"""]
    ldrb.w {a64}, [{c_temp}, #"""+str(128+1)+"""]
    ldrb.w {a128}, [{c_temp}, #"""+str(256+1)+"""]
    ldrb.w {a192}, [{c_temp}, #"""+str(384+1)+"""]
    ldrb.w {a256}, [{c_temp}, #"""+str(512+1)+"""]
    ldrb.w {a320}, [{c_temp}, #"""+str(640+1)+"""]
    ldrb.w {a384}, [{c_temp}, #"""+str(768+1)+"""]
    ldrb.w {a448}, [{c_temp}, #"""+str(896+1)+"""]
    add.w {c_temp}, #"""+str(1*2)+"""
    vmov.w ary_input1, {c_temp}
    """
    
    combine_1_2_3 += """
    movw.w {temp_lower}, 251
    movw.w {c_temp}, 125
    central_reduce {a0}, {c_temp}, {temp_lower}
    central_reduce {a64}, {c_temp}, {temp_lower}
    central_reduce {a128}, {c_temp}, {temp_lower}
    central_reduce {a192}, {c_temp}, {temp_lower}
    central_reduce {a256}, {c_temp}, {temp_lower}
    central_reduce {a320}, {c_temp}, {temp_lower}
    central_reduce {a384}, {c_temp}, {temp_lower}
    central_reduce {a448}, {c_temp}, {temp_lower}
    """

    combine_1_2_3 += """
    // level 1
    vmov.w {c_temp}, s0
    mul.w {a256}, {c_temp}
    mul.w {a320}, {c_temp}
    mul.w {a384}, {c_temp}
    mul.w {a448}, {c_temp}
    add_sub {a0}, {a256}, {a64}, {a320}, {a128}, {a384}, {a192}, {a448}
    
    // level 2
    vmov.w {c_temp}, s1
    montgomery_mul {a128}, {c_temp}, {temp_lower}, {a128}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a192}, {c_temp}, {temp_lower}, {a192}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s2
    montgomery_mul {a384}, {c_temp}, {temp_lower}, {a384}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a448}, {c_temp}, {temp_lower}, {a448}, {temp_upper}, {M_inv}, {M}
    
    add_sub {a0}, {a128}, {a64}, {a192}, {a256}, {a384}, {a320}, {a448}
    
    // level 3
    vmov.w {c_temp}, s3
    montgomery_mul {a64}, {c_temp}, {temp_lower}, {a64}, {temp_upper}, {M_inv}, {M} 
    vmov.w {c_temp}, s4
    montgomery_mul {a192}, {c_temp}, {temp_lower}, {a192}, {temp_upper}, {M_inv}, {M} 
    vmov.w {c_temp}, s5
    montgomery_mul {a320}, {c_temp}, {temp_lower}, {a320}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s6
    montgomery_mul {a448}, {c_temp}, {temp_lower}, {a448}, {temp_upper}, {M_inv}, {M}

    add_sub {a0}, {a64}, {a128}, {a192}, {a256}, {a320}, {a384}, {a448}
    
    str.w {a0}, [r0, #"""+str(0+4*i)+"""]
    str.w {a64}, [r0, #"""+str(512+4*i)+"""]
    str.w {a128}, [r0, #"""+str(1024+4*i)+"""]
    str.w {a192}, [r0, #"""+str(1536+4*i)+"""]
    str.w {a256}, [r0, #"""+str(2048+4*i)+"""]
    str.w {a320}, [r0, #"""+str(2560+4*i)+"""]
    str.w {a384}, [r0, #"""+str(3072+4*i)+"""]
    str.w {a448}, [r0, #"""+str(3584+4*i)+"""] 
    """

combine_1_2_3 += """
    add.w r0, #"""+str(4*2)+"""
    
    vmov.w r5, inner_counter
    cmp.w r5, r0
    bne.w loop_1_2_3_big 

vmov.w lr, tmp_lr
bx lr     
"""

combine_1_2_3 = combine_1_2_3.format(a0="r4", a64="r5", a128="r6", a192="r7", a256="r8", 
            a320="r9", a384="r10", a448="r11", temp_lower="r12", 
            temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")

combine_1_2_3_small = """
.align 2
_1_2_3_small:
vmov.w tmp_lr, lr

add.w r12, r0, #"""+str(4*128)+""" // set counter
vmov.w inner_counter, r12

.align 2
loop_1_2_3_small:
"""

for i in range(2):
    if i == 0:
        combine_1_2_3_small += """
    vmov.w {c_temp}, ary_input2
    ldrsb.w {a0}, [{c_temp}, #"""+str(0)+"""]
    ldrsb.w {a64}, [{c_temp}, #"""+str(128)+"""]
    ldrsb.w {a128}, [{c_temp}, #"""+str(256)+"""]
    ldrsb.w {a192}, [{c_temp}, #"""+str(384)+"""]
    ldrsb.w {a256}, [{c_temp}, #"""+str(512)+"""]
    ldrsb.w {a320}, [{c_temp}, #"""+str(640)+"""]
    ldrsb.w {a384}, [{c_temp}, #"""+str(768)+"""]
    ldrsb.w {a448}, [{c_temp}, #"""+str(896)+"""]
    """
    else:
        combine_1_2_3_small += """
    vmov.w {c_temp}, ary_input2
    ldrsb.w {a0}, [{c_temp}, #"""+str(0+1)+"""]
    ldrsb.w {a64}, [{c_temp}, #"""+str(128+1)+"""]
    ldrsb.w {a128}, [{c_temp}, #"""+str(256+1)+"""]
    ldrsb.w {a192}, [{c_temp}, #"""+str(384+1)+"""]
    ldrsb.w {a256}, [{c_temp}, #"""+str(512+1)+"""]
    ldrsb.w {a320}, [{c_temp}, #"""+str(640+1)+"""]
    ldrsb.w {a384}, [{c_temp}, #"""+str(768+1)+"""]
    ldrsb.w {a448}, [{c_temp}, #"""+str(896+1)+"""]
    add.w {c_temp}, #"""+str(1*2)+"""
    vmov.w ary_input2, {c_temp}
    """
    
    combine_1_2_3_small += """
    // level 1
    vmov.w {c_temp}, s0
    mul.w {a256}, {c_temp}
    mul.w {a320}, {c_temp}
    mul.w {a384}, {c_temp}
    mul.w {a448}, {c_temp}
    add_sub {a0}, {a256}, {a64}, {a320}, {a128}, {a384}, {a192}, {a448}
    
    // level 2
    vmov.w {c_temp}, s1
    montgomery_mul {a128}, {c_temp}, {temp_lower}, {a128}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a192}, {c_temp}, {temp_lower}, {a192}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s2
    montgomery_mul {a384}, {c_temp}, {temp_lower}, {a384}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a448}, {c_temp}, {temp_lower}, {a448}, {temp_upper}, {M_inv}, {M}
    
    add_sub {a0}, {a128}, {a64}, {a192}, {a256}, {a384}, {a320}, {a448}
    
    // level 3
    vmov.w {c_temp}, s3
    montgomery_mul {a64}, {c_temp}, {temp_lower}, {a64}, {temp_upper}, {M_inv}, {M} 
    vmov.w {c_temp}, s4
    montgomery_mul {a192}, {c_temp}, {temp_lower}, {a192}, {temp_upper}, {M_inv}, {M} 
    vmov.w {c_temp}, s5
    montgomery_mul {a320}, {c_temp}, {temp_lower}, {a320}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s6
    montgomery_mul {a448}, {c_temp}, {temp_lower}, {a448}, {temp_upper}, {M_inv}, {M}

    add_sub {a0}, {a64}, {a128}, {a192}, {a256}, {a320}, {a384}, {a448}
    
    str.w {a0}, [r0, #"""+str(0+4*i)+"""]
    str.w {a64}, [r0, #"""+str(512+4*i)+"""]
    str.w {a128}, [r0, #"""+str(1024+4*i)+"""]
    str.w {a192}, [r0, #"""+str(1536+4*i)+"""]
    str.w {a256}, [r0, #"""+str(2048+4*i)+"""]
    str.w {a320}, [r0, #"""+str(2560+4*i)+"""]
    str.w {a384}, [r0, #"""+str(3072+4*i)+"""]
    str.w {a448}, [r0, #"""+str(3584+4*i)+"""] 
    """

combine_1_2_3_small += """
    add.w r0, #"""+str(4*2)+"""
    
    vmov.w r5, inner_counter
    cmp.w r5, r0
    bne.w loop_1_2_3_small 

vmov.w lr, tmp_lr
bx lr     
"""

combine_1_2_3_small = combine_1_2_3_small.format(a0="r4", a64="r5", a128="r6", a192="r7", a256="r8", 
            a320="r9", a384="r10", a448="r11", temp_lower="r12", 
            temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")


combine_4_5_6 = """
.align 2
_4_5_6:
vmov.w tmp_lr, lr
"""

combine_4_5_6 += """
add.w r1, r0, #"""+str(8*512)+"""   // outer iteration set counter
vmov.w outer_counter, r1


.align 2
normal_4_5_6_outer:
    vmov.w r1, tmp_root_table
    vldm.w r1!, {{s0-s6}}
    vmov.w tmp_root_table, r1
"""

combine_4_5_6 += """
    add.w r4, r0, #"""+str(4*16)+""" // inner iteration set counter
    vmov.w inner_counter, r4
    normal_4_5_6_inner:
"""

for i in range(2):
    load = """
        ldr.w {a0}, [r0, #"""+str(0 + i*4)+"""]
        ldr.w {a8}, [r0, #"""+str(64 + i*4)+"""]
        ldr.w {a16}, [r0, #"""+str(128 + i*4)+"""]
        ldr.w {a24}, [r0, #"""+str(192 + i*4)+"""]
        ldr.w {a32}, [r0, #"""+str(256 + i*4)+"""]
        ldr.w {a40}, [r0, #"""+str(320 + i*4)+"""]
        ldr.w {a48}, [r0, #"""+str(384 + i*4)+"""]
        ldr.w {a56}, [r0, #"""+str(448 + i*4)+"""]
    """

    calculate_level4_5_6 = """
        // level 4
        vmov.w {c_temp}, s0
        montgomery_mul {a32}, {c_temp}, {temp_lower}, {a32}, {temp_upper}, {M_inv}, {M}
        montgomery_mul {a40}, {c_temp}, {temp_lower}, {a40}, {temp_upper}, {M_inv}, {M}
        montgomery_mul {a48}, {c_temp}, {temp_lower}, {a48}, {temp_upper}, {M_inv}, {M}
        montgomery_mul {a56}, {c_temp}, {temp_lower}, {a56}, {temp_upper}, {M_inv}, {M}
        
        add_sub {a0}, {a32}, {a8}, {a40}, {a16}, {a48}, {a24}, {a56}
        
        // level 5
        vmov.w {c_temp}, s1
        montgomery_mul {a16}, {c_temp}, {temp_lower}, {a16}, {temp_upper}, {M_inv}, {M}   
        montgomery_mul {a24}, {c_temp}, {temp_lower}, {a24}, {temp_upper}, {M_inv}, {M}
        vmov.w {c_temp}, s2
        montgomery_mul {a48}, {c_temp}, {temp_lower}, {a48}, {temp_upper}, {M_inv}, {M}   
        montgomery_mul {a56}, {c_temp}, {temp_lower}, {a56}, {temp_upper}, {M_inv}, {M}
        
        add_sub {a0}, {a16}, {a8}, {a24}, {a32}, {a48}, {a40}, {a56}
        
        // level 6
        vmov.w {c_temp}, s3
        montgomery_mul {a8}, {c_temp}, {temp_lower}, {a8}, {temp_upper}, {M_inv}, {M}    
        vmov.w {c_temp}, s4
        montgomery_mul {a24}, {c_temp}, {temp_lower}, {a24}, {temp_upper}, {M_inv}, {M}         
        vmov.w {c_temp}, s5
        montgomery_mul {a40}, {c_temp}, {temp_lower}, {a40}, {temp_upper}, {M_inv}, {M}         
        vmov.w {c_temp}, s6
        montgomery_mul {a56}, {c_temp}, {temp_lower}, {a56}, {temp_upper}, {M_inv}, {M}   
        
        add_sub {a0}, {a8}, {a16}, {a24}, {a32}, {a40}, {a48}, {a56}
    """

    store = """
        // save
        str.w {a0}, [r0, #"""+str(0 + i*4)+"""]
        str.w {a8}, [r0, #"""+str(64 + i*4)+"""]
        str.w {a16}, [r0, #"""+str(128 + i*4)+"""]
        str.w {a24}, [r0, #"""+str(192 + i*4)+"""]
        str.w {a32}, [r0, #"""+str(256 + i*4)+"""]
        str.w {a40}, [r0, #"""+str(320 + i*4)+"""]
        str.w {a48}, [r0, #"""+str(384 + i*4)+"""]
        str.w {a56}, [r0, #"""+str(448 + i*4)+"""]
    """

    combine_4_5_6 += (load + calculate_level4_5_6 + store)

combine_4_5_6 += """
        add.w r0, #"""+str(4*2)+"""
        vmov.w r4, inner_counter
        cmp.w r4, r0
        bne.w normal_4_5_6_inner

    add.w r0, #"""+str(448)+"""
    vmov.w r4, outer_counter
    cmp.w r4, r0
    bne.w normal_4_5_6_outer

vmov.w lr, tmp_lr
bx lr 
"""

combine_4_5_6 = combine_4_5_6.format(a0="r4", a8="r5", a16="r6", a24="r7", a32="r8", 
                    a40="r9", a48="r10", a56="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")

combine_7_8_9 = """
.align 2
_7_8_9:
vmov.w tmp_lr, lr
"""

combine_7_8_9 += """
add.w r12, r0, #"""+str(64*64)+"""   // set counter
vmov.w inner_counter, r12

.align 2
loop_7_8_9:
    vmov.w r1, tmp_root_table
    vldm.w r1!, {{s0-s6}}
    vmov.w tmp_root_table, r1
"""

for i in range(2):
    load = """
    ldr {a0}, [r0, #"""+str(0 + i*4)+"""]
    ldr {a1}, [r0, #"""+str(8 + i*4)+"""]
    ldr {a2}, [r0, #"""+str(16 + i*4)+"""]
    ldr {a3}, [r0, #"""+str(24 + i*4)+"""]
    ldr.w {a4}, [r0, #"""+str(32 + i*4)+"""]
    ldr.w {a5}, [r0, #"""+str(40 + i*4)+"""]
    ldr.w {a6}, [r0, #"""+str(48 + i*4)+"""]
    ldr.w {a7}, [r0, #"""+str(56 + i*4)+"""]
    """

    calculate_level7_8_9 = """
    // level 7
    vmov.w {c_temp}, s0
    montgomery_mul {a4}, {c_temp}, {temp_lower}, {a4}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a5}, {c_temp}, {temp_lower}, {a5}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a6}, {c_temp}, {temp_lower}, {a6}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a7}, {c_temp}, {temp_lower}, {a7}, {temp_upper}, {M_inv}, {M}
    
    add_sub {a0}, {a4}, {a1}, {a5}, {a2}, {a6}, {a3}, {a7}
    
    // level 8
    vmov.w {c_temp}, s1
    montgomery_mul {a2}, {c_temp}, {temp_lower}, {a2}, {temp_upper}, {M_inv}, {M}   
    montgomery_mul {a3}, {c_temp}, {temp_lower}, {a3}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s2
    montgomery_mul {a6}, {c_temp}, {temp_lower}, {a6}, {temp_upper}, {M_inv}, {M}   
    montgomery_mul {a7}, {c_temp}, {temp_lower}, {a7}, {temp_upper}, {M_inv}, {M}
    
    add_sub {a0}, {a2}, {a1}, {a3}, {a4}, {a6}, {a5}, {a7}
    
    // level 9
    vmov.w {c_temp}, s3
    montgomery_mul {a1}, {c_temp}, {temp_lower}, {a1}, {temp_upper}, {M_inv}, {M}    
    vmov.w {c_temp}, s4
    montgomery_mul {a3}, {c_temp}, {temp_lower}, {a3}, {temp_upper}, {M_inv}, {M}         
    vmov.w {c_temp}, s5
    montgomery_mul {a5}, {c_temp}, {temp_lower}, {a5}, {temp_upper}, {M_inv}, {M}         
    vmov.w {c_temp}, s6
    montgomery_mul {a7}, {c_temp}, {temp_lower}, {a7}, {temp_upper}, {M_inv}, {M}   
    
    add_sub {a0}, {a1}, {a2}, {a3}, {a4}, {a5}, {a6}, {a7}
    """

    store = """
    // save
    str {a0}, [r0, #"""+str(0 + i*4)+"""]
    str {a1}, [r0, #"""+str(8 + i*4)+"""]
    str {a2}, [r0, #"""+str(16 + i*4)+"""]
    str {a3}, [r0, #"""+str(24 + i*4)+"""]
    str.w {a4}, [r0, #"""+str(32 + i*4)+"""]
    str.w {a5}, [r0, #"""+str(40 + i*4)+"""]
    str.w {a6}, [r0, #"""+str(48 + i*4)+"""]
    str.w {a7}, [r0, #"""+str(56 + i*4)+"""]
    """

    combine_7_8_9 += (load + calculate_level7_8_9 + store)

combine_7_8_9 += """
    add.w r0, #"""+str(64)+"""
    vmov.w r4, inner_counter
    cmp.w r4, r0
    bne.w loop_7_8_9

vmov.w lr, tmp_lr
bx lr
"""

combine_7_8_9 = combine_7_8_9.format(a0="r4", a1="r5", a2="r6", a3="r7", a4="r8", 
                    a5="r9", a6="r10", a7="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")


text = """
.align 2
my_mul:
    upper          .req r10
    lower          .req r14
    tmp1           .req r12
    root           .req r1

    M              .req r2
    M_inv          .req r3
    K0             .req r4
    K1             .req r5
    B0             .req r8
    B1             .req r9
    counter        .req r6
    mul_table      .req r7

    add.w r0, #"""+str(128)+"""  // adjust r0 to access two polys
    add.w counter, r0, #"""+str(4096)+"""  // set counter
    vmov.w mul_table, tmp_mul_table
    
    my_multiply:
"""

unroll = 8

for i in range(unroll):
    load = """
        ldr.w root, [mul_table], #4
        ldr.w K0, [r0, #"""+str(-128+0+8*i)+"""]
        ldr.w K1, [r0, #"""+str(-128+4+8*i)+"""]
        ldr.w B0, [r0, #"""+str(-128+4096+0+8*i)+"""]
        ldr.w B1, [r0, #"""+str(-128+4096+4+8*i)+"""]
        """
    
    compute = """
        smull.w lower, upper, K1, B0
        smlal.w lower, upper, K0, B1
        mul.w tmp1, lower, M_inv
        smlal.w lower, upper, tmp1, M  @ upper = K1B0 + K0B1

        smull.w lower, K1, K1, B1
        mul.w tmp1, lower, M_inv
        smlal.w lower, K1, tmp1, M
        smull.w lower, K1, K1, root
        smlal.w lower, K1, K0, B0
        mul.w tmp1, lower, M_inv
        smlal.w lower, K1, tmp1, M     @ K1 = K1B1*root + K0B0 
        """
    
    store = """
        str.w K1, [r0, #"""+str(-128+0+8*i)+"""]
        str.w upper, [r0, #"""+str(-128+4+8*i)+"""]
    """

    text += (load + compute + store)

store = """
        add.w r0, #"""+str(4*2*8)+"""
        cmp.w counter, r0
        bne.w my_multiply
"""

text += store

combine_9_8_7 = """
sub.w r0, #"""+str(4096+128)+""" // reset pointer

_9_8_7:
add.w r12, r0, #"""+str(4096)+"""   // set counter
vmov.w inner_counter, r12

.align 2
loop_9_8_7:
    vmov.w r1, tmp_inv_table
    vldm.w r1!, {{s0-s6}}
    vmov.w tmp_inv_table, r1
"""

for i in range(2):
    load = """
    ldr {a0}, [r0, #"""+str(0 + i*4)+"""]
    ldr {a1}, [r0, #"""+str(8 + i*4)+"""]
    ldr {a2}, [r0, #"""+str(16 + i*4)+"""]
    ldr {a3}, [r0, #"""+str(24 + i*4)+"""]
    ldr.w {a4}, [r0, #"""+str(32 + i*4)+"""]
    ldr.w {a5}, [r0, #"""+str(40 + i*4)+"""]
    ldr.w {a6}, [r0, #"""+str(48 + i*4)+"""]
    ldr.w {a7}, [r0, #"""+str(56 + i*4)+"""]
    """

    calculate_level9_8_7 = """
    // level 9
    add_sub {a0}, {a1}, {a2}, {a3}, {a4}, {a5}, {a6}, {a7}
    
    vmov.w {c_temp}, s3
    montgomery_mul {a1}, {c_temp}, {temp_lower}, {a1}, {temp_upper}, {M_inv}, {M}    
    vmov.w {c_temp}, s4
    montgomery_mul {a3}, {c_temp}, {temp_lower}, {a3}, {temp_upper}, {M_inv}, {M}         
    vmov.w {c_temp}, s5
    montgomery_mul {a5}, {c_temp}, {temp_lower}, {a5}, {temp_upper}, {M_inv}, {M}         
    vmov.w {c_temp}, s6
    montgomery_mul {a7}, {c_temp}, {temp_lower}, {a7}, {temp_upper}, {M_inv}, {M}   
    
    // level 8
    add_sub {a0}, {a2}, {a1}, {a3}, {a4}, {a6}, {a5}, {a7}
    
    vmov.w {c_temp}, s1
    montgomery_mul {a2}, {c_temp}, {temp_lower}, {a2}, {temp_upper}, {M_inv}, {M}   
    montgomery_mul {a3}, {c_temp}, {temp_lower}, {a3}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s2
    montgomery_mul {a6}, {c_temp}, {temp_lower}, {a6}, {temp_upper}, {M_inv}, {M}   
    montgomery_mul {a7}, {c_temp}, {temp_lower}, {a7}, {temp_upper}, {M_inv}, {M}
    
    // level 7
    add_sub {a0}, {a4}, {a1}, {a5}, {a2}, {a6}, {a3}, {a7}
    
    vmov.w {c_temp}, s0
    montgomery_mul {a4}, {c_temp}, {temp_lower}, {a4}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a5}, {c_temp}, {temp_lower}, {a5}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a6}, {c_temp}, {temp_lower}, {a6}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a7}, {c_temp}, {temp_lower}, {a7}, {temp_upper}, {M_inv}, {M}
    """

    store = """
    // save
    str {a0}, [r0, #"""+str(0 + i*4)+"""]
    str {a1}, [r0, #"""+str(8 + i*4)+"""]
    str {a2}, [r0, #"""+str(16 + i*4)+"""]
    str {a3}, [r0, #"""+str(24 + i*4)+"""]
    str.w {a4}, [r0, #"""+str(32 + i*4)+"""]
    str.w {a5}, [r0, #"""+str(40 + i*4)+"""]
    str.w {a6}, [r0, #"""+str(48 + i*4)+"""]
    str.w {a7}, [r0, #"""+str(56 + i*4)+"""]
    """

    combine_9_8_7 += (load + calculate_level9_8_7 + store)

combine_9_8_7 += """
    add.w r0, #"""+str(64)+"""
    vmov.w r4, inner_counter
    cmp.w r4, r0
    bne.w loop_9_8_7
"""

combine_9_8_7 = combine_9_8_7.format(a0="r4", a1="r5", a2="r6", a3="r7", a4="r8", 
                    a5="r9", a6="r10", a7="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")


combine_6_5_4 = """
sub.w r0, #"""+str(4096)+""" // reset pointer

.align 2
_6_5_4:
"""

combine_6_5_4 += """
add.w r1, r0, #"""+str(4096)+"""   // outer iteration set counter
vmov.w outer_counter, r1

.align 2
normal_6_5_4_outer:
    vmov.w r1, tmp_inv_table
    vldm.w r1!, {{s0-s6}}
    vmov.w tmp_inv_table, r1
"""

combine_6_5_4 += """
    add.w r4, r0, #"""+str(64)+""" // inner iteration set counter
    vmov.w inner_counter, r4
 
    normal_6_5_4_inner:
"""

for i in range(2):
    load = """
        ldr.w {a0}, [r0, #"""+str(0 + i*4)+"""]
        ldr.w {a8}, [r0, #"""+str(64 + i*4)+"""]
        ldr.w {a16}, [r0, #"""+str(128 + i*4)+"""]
        ldr.w {a24}, [r0, #"""+str(192 + i*4)+"""]
        ldr.w {a32}, [r0, #"""+str(256 + i*4)+"""]
        ldr.w {a40}, [r0, #"""+str(320 + i*4)+"""]
        ldr.w {a48}, [r0, #"""+str(384 + i*4)+"""]
        ldr.w {a56}, [r0, #"""+str(448 + i*4)+"""]
    """

    calculate_level6_5_4 = """
        // level 6
        add_sub {a0}, {a8}, {a16}, {a24}, {a32}, {a40}, {a48}, {a56}
        
        vmov.w {c_temp}, s3
        montgomery_mul {a8}, {c_temp}, {temp_lower}, {a8}, {temp_upper}, {M_inv}, {M}
        vmov.w {c_temp}, s4
        montgomery_mul {a24}, {c_temp}, {temp_lower}, {a24}, {temp_upper}, {M_inv}, {M}
        vmov.w {c_temp}, s5
        montgomery_mul {a40}, {c_temp}, {temp_lower}, {a40}, {temp_upper}, {M_inv}, {M}
        vmov.w {c_temp}, s6
        montgomery_mul {a56}, {c_temp}, {temp_lower}, {a56}, {temp_upper}, {M_inv}, {M}
        
        // level 5
        add_sub {a0}, {a16}, {a8}, {a24}, {a32}, {a48}, {a40}, {a56}
        
        vmov.w {c_temp}, s1
        montgomery_mul {a16}, {c_temp}, {temp_lower}, {a16}, {temp_upper}, {M_inv}, {M}
        montgomery_mul {a24}, {c_temp}, {temp_lower}, {a24}, {temp_upper}, {M_inv}, {M}
        vmov.w {c_temp}, s2
        montgomery_mul {a48}, {c_temp}, {temp_lower}, {a48}, {temp_upper}, {M_inv}, {M}
        montgomery_mul {a56}, {c_temp}, {temp_lower}, {a56}, {temp_upper}, {M_inv}, {M}
        
        // level 4
        add_sub {a0}, {a32}, {a8}, {a40}, {a16}, {a48}, {a24}, {a56}
        
        vmov.w {c_temp}, s0
        montgomery_mul {a32}, {c_temp}, {temp_lower}, {a32}, {temp_upper}, {M_inv}, {M}
        montgomery_mul {a40}, {c_temp}, {temp_lower}, {a40}, {temp_upper}, {M_inv}, {M}
        montgomery_mul {a48}, {c_temp}, {temp_lower}, {a48}, {temp_upper}, {M_inv}, {M}
        montgomery_mul {a56}, {c_temp}, {temp_lower}, {a56}, {temp_upper}, {M_inv}, {M}
    """

    store = """
        // save
        str.w {a0}, [r0, #"""+str(0 + i*4)+"""]
        str.w {a8}, [r0, #"""+str(64 + i*4)+"""]
        str.w {a16}, [r0, #"""+str(128 + i*4)+"""]
        str.w {a24}, [r0, #"""+str(192 + i*4)+"""]
        str.w {a32}, [r0, #"""+str(256 + i*4)+"""]
        str.w {a40}, [r0, #"""+str(320 + i*4)+"""]
        str.w {a48}, [r0, #"""+str(384 + i*4)+"""]
        str.w {a56}, [r0, #"""+str(448 + i*4)+"""]
    """

    combine_6_5_4 += (load + calculate_level6_5_4 + store)

combine_6_5_4 += """
        add.w r0, #"""+str(4*2)+"""
        vmov.w r4, inner_counter
        cmp.w r4, r0
        bne.w normal_6_5_4_inner

    add.w r0, #"""+str(448)+"""
    vmov.w r4, outer_counter
    cmp.w r4, r0
    bne.w normal_6_5_4_outer
"""

combine_6_5_4 = combine_6_5_4.format(a0="r4", a8="r5", a16="r6", a24="r7", a32="r8", 
                    a40="r9", a48="r10", a56="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")

combine_3_2_1 = """
sub.w r0, #"""+str(4096)+""" // reset pointer

add.w r12, r0, #"""+str(4*128)+""" // set counter
vmov.w inner_counter, r12

vmov.w r4, tmp_inv_table
vldm.w r4, {{s0-s7}}

.align 2
_3_2_1:
loop_3_2_1:
"""

for i in range(1):
    combine_3_2_1 += """
    ldr.w {a0}, [r0, #"""+str(0+4*i)+"""]
    ldr.w {a64}, [r0, #"""+str(512+4*i)+"""]
    ldr.w {a128}, [r0, #"""+str(1024+4*i)+"""]
    ldr.w {a192}, [r0, #"""+str(1536+4*i)+"""]
    ldr.w {a256}, [r0, #"""+str(2048+4*i)+"""]
    ldr.w {a320}, [r0, #"""+str(2560+4*i)+"""]
    ldr.w {a384}, [r0, #"""+str(3072+4*i)+"""]
    ldr.w {a448}, [r0, #"""+str(3584+4*i)+"""]
    add.w r0, #"""+str(4)+""" 
    """

    combine_3_2_1 += """
    // level 3
    add_sub {a0}, {a64}, {a128}, {a192}, {a256}, {a320}, {a384}, {a448}
    
    vmov.w {c_temp}, s3
    montgomery_mul {a64}, {c_temp}, {temp_lower}, {a64}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s4
    montgomery_mul {a192}, {c_temp}, {temp_lower}, {a192}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s5
    montgomery_mul {a320}, {c_temp}, {temp_lower}, {a320}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s6
    montgomery_mul {a448}, {c_temp}, {temp_lower}, {a448}, {temp_upper}, {M_inv}, {M} 
    
    // level 2
    add_sub {a0}, {a128}, {a64}, {a192}, {a256}, {a384}, {a320}, {a448}
    
    vmov.w {c_temp}, s1
    montgomery_mul {a128}, {c_temp}, {temp_lower}, {a128}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a192}, {c_temp}, {temp_lower}, {a192}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s2
    montgomery_mul {a384}, {c_temp}, {temp_lower}, {a384}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a448}, {c_temp}, {temp_lower}, {a448}, {temp_upper}, {M_inv}, {M}
    
    // level 1
    add_sub {a0}, {a256}, {a64}, {a320}, {a128}, {a384}, {a192}, {a448}

    vmov.w {c_temp}, s7
    montgomery_mul {a0}, {c_temp}, {temp_lower}, {a0}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a64}, {c_temp}, {temp_lower}, {a64}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a128}, {c_temp}, {temp_lower}, {a128}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a192}, {c_temp}, {temp_lower}, {a192}, {temp_upper}, {M_inv}, {M}
    vmov.w {c_temp}, s0
    montgomery_mul {a256}, {c_temp}, {temp_lower}, {a256}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a320}, {c_temp}, {temp_lower}, {a320}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a384}, {c_temp}, {temp_lower}, {a384}, {temp_upper}, {M_inv}, {M}
    montgomery_mul {a448}, {c_temp}, {temp_lower}, {a448}, {temp_upper}, {M_inv}, {M}
    
    mov.w {c_temp}, {M}, asr #1
    central_reduce {a0}, {c_temp}, {M}
    central_reduce {a64}, {c_temp}, {M}
    central_reduce {a128}, {c_temp}, {M}
    central_reduce {a192}, {c_temp}, {M}
    central_reduce {a256}, {c_temp}, {M}
    central_reduce {a320}, {c_temp}, {M}
    central_reduce {a384}, {c_temp}, {M}
    central_reduce {a448}, {c_temp}, {M}

    vmov.w {c_temp}, q_bar
    movw.w {temp_upper}, 251
    barret {a0}, {c_temp}, {temp_upper}, {temp_lower}
    barret {a64}, {c_temp}, {temp_upper}, {temp_lower}
    barret {a128}, {c_temp}, {temp_upper}, {temp_lower}
    barret {a192}, {c_temp}, {temp_upper}, {temp_lower}
    barret {a256}, {c_temp}, {temp_upper}, {temp_lower}
    barret {a320}, {c_temp}, {temp_upper}, {temp_lower}
    barret {a384}, {c_temp}, {temp_upper}, {temp_lower}
    barret {a448}, {c_temp}, {temp_upper}, {temp_lower}

    mov.w {c_temp}, 0
    unsigned_char {a0}, {c_temp}, {temp_upper}
    unsigned_char {a64}, {c_temp}, {temp_upper}
    unsigned_char {a128}, {c_temp}, {temp_upper}
    unsigned_char {a192}, {c_temp}, {temp_upper}
    unsigned_char {a256}, {c_temp}, {temp_upper}
    unsigned_char {a320}, {c_temp}, {temp_upper}
    unsigned_char {a384}, {c_temp}, {temp_upper}
    unsigned_char {a448}, {c_temp}, {temp_upper}
    """

    combine_3_2_1 += """
    vmov.w {c_temp}, tmp_ans
    strb.w {a0}, [{c_temp}, #"""+str(0+1*i)+"""]
    strb.w {a64}, [{c_temp}, #"""+str(128+1*i)+"""]
    strb.w {a128}, [{c_temp}, #"""+str(256+1*i)+"""]
    strb.w {a192}, [{c_temp}, #"""+str(384+1*i)+"""]
    strb.w {a256}, [{c_temp}, #"""+str(512+1*i)+"""]
    strb.w {a320}, [{c_temp}, #"""+str(640+1*i)+"""]
    strb.w {a384}, [{c_temp}, #"""+str(768+1*i)+"""]
    strb.w {a448}, [{c_temp}, #"""+str(896+1*i)+"""]
    """

combine_3_2_1 += """
    add.w {c_temp}, #"""+str(1*1)+"""
    vmov.w tmp_ans, {c_temp}
    
    vmov.w r5, inner_counter
    cmp.w r5, r0
    bne.w loop_3_2_1               
"""

combine_3_2_1 = combine_3_2_1.format(a0="r4", a64="r5", a128="r6", a192="r7", a256="r8", 
                    a320="r9", a384="r10", a448="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1") # r0 points to polynomial

End = """
add.w sp, #"""+str(8192)+"""
vpop.w {s16, s17, s18}
pop.w {r4-r12, pc}
"""

NTT = lin + macro + start + combine_1_2_3 + combine_1_2_3_small + combine_4_5_6 + combine_7_8_9 + text + \
                   combine_9_8_7 + combine_6_5_4 + combine_3_2_1 + End
print(NTT)