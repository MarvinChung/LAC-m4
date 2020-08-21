
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


#!/usr/bin/env python
# coding: utf-8

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
.global NTT_512
.type NTT_512, %function

NTT_512:
push.w {{r4-r12, r14}}
vpush.w {{s16, s17}}

tmp_root_table .req s8
outer_counter  .req s9
inner_counter  .req s10
ary_input1     .req s11
ary_input2     .req s12
tmp_counter    .req s13
tmp_inv_table  .req s14
tmp_ans        .req s15
q_bar          .req s16
tmp_save       .req s17

vldr.w ary_input2, [sp, #"""+str(40 + 4*2)+"""]
vldr.w tmp_inv_table, [sp, #"""+str(44 + 4*2)+"""]
vldr.w tmp_ans, [sp, #"""+str(48 + 4*2)+"""]
vldr.w q_bar, [sp, #"""+str(52 + 4*2)+"""]
vldm.w r1!, {{s0-s6}}
vmov.w tmp_root_table, r1
vmov.w ary_input1, r0

// allocate NTTd array using sp
sub.w sp, #"""+str(4096)+"""
mov.w r0, sp
vmov.w tmp_save, r0

.align 2
_1_2_3:

add.w r12, r0, #"""+str(4*64)+""" // set counter
vmov.w inner_counter, r12

.align 2
loop_1_2_3:
"""

for i in range(2):
    if i == 0:
        combine_1_2_3 += """
    vmov.w {c_temp}, ary_input"""+str(i+1)+"""
    ldrb.w {a0}, [{c_temp}, #"""+str(0)+"""]
    ldrb.w {a64}, [{c_temp}, #"""+str(64)+"""]
    ldrb.w {a128}, [{c_temp}, #"""+str(128)+"""]
    ldrb.w {a192}, [{c_temp}, #"""+str(192)+"""]
    ldrb.w {a256}, [{c_temp}, #"""+str(256)+"""]
    ldrb.w {a320}, [{c_temp}, #"""+str(320)+"""]
    ldrb.w {a384}, [{c_temp}, #"""+str(384)+"""]
    ldrb.w {a448}, [{c_temp}, #"""+str(448)+"""]
    add.w {c_temp}, #"""+str(1*1)+"""
    vmov.w ary_input"""+str(i+1)+""", {c_temp}
    """
    else:
        combine_1_2_3 += """
    vmov.w {c_temp}, ary_input"""+str(i+1)+"""
    ldrsb.w {a0}, [{c_temp}, #"""+str(0)+"""]
    ldrsb.w {a64}, [{c_temp}, #"""+str(64)+"""]
    ldrsb.w {a128}, [{c_temp}, #"""+str(128)+"""]
    ldrsb.w {a192}, [{c_temp}, #"""+str(192)+"""]
    ldrsb.w {a256}, [{c_temp}, #"""+str(256)+"""]
    ldrsb.w {a320}, [{c_temp}, #"""+str(320)+"""]
    ldrsb.w {a384}, [{c_temp}, #"""+str(384)+"""]
    ldrsb.w {a448}, [{c_temp}, #"""+str(448)+"""]
    add.w {c_temp}, #"""+str(1*1)+"""
    vmov.w ary_input"""+str(i+1)+""", {c_temp}
    """

    if i == 0:
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
    
    str.w {a0}, [r0, #"""+str(0+2048*i)+"""]
    str.w {a64}, [r0, #"""+str(256+2048*i)+"""]
    str.w {a128}, [r0, #"""+str(512+2048*i)+"""]
    str.w {a192}, [r0, #"""+str(768+2048*i)+"""]
    str.w {a256}, [r0, #"""+str(1024+2048*i)+"""]
    str.w {a320}, [r0, #"""+str(1280+2048*i)+"""]
    str.w {a384}, [r0, #"""+str(1536+2048*i)+"""]
    str.w {a448}, [r0, #"""+str(1792+2048*i)+"""] 
    """

combine_1_2_3 += """
    add.w r0, #"""+str(4)+"""
    
    vmov.w r5, inner_counter
    cmp.w r5, r0
    bne.w loop_1_2_3      
"""

combine_1_2_3 = combine_1_2_3.format(a0="r4", a64="r5", a128="r6", a192="r7", a256="r8", 
            a320="r9", a384="r10", a448="r11", temp_lower="r12", 
            temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")

combine_4_5_6 = """
.align 2
_4_5_6:
"""

combine_4_5_6 += """
sub.w r0, #"""+str(4*64)+""" // reset pointer

add.w r1, r0, #"""+str(8*256)+"""   // outer iteration set counter
vmov.w outer_counter, r1


.align 2
normal_4_5_6_outer:
    vmov.w r1, tmp_root_table
    vldm.w r1!, {{s0-s6}}
    vmov.w tmp_root_table, r1
"""

combine_4_5_6 += """
    add.w r4, r0, #"""+str(4*8)+""" // inner iteration set counter
    vmov.w inner_counter, r4
    normal_4_5_6_inner:
"""

for i in range(2):
    load = """
        ldr.w {a0}, [r0, #"""+str(0 + i*2048)+"""]
        ldr.w {a8}, [r0, #"""+str(32 + i*2048)+"""]
        ldr.w {a16}, [r0, #"""+str(64 + i*2048)+"""]
        ldr.w {a24}, [r0, #"""+str(96 + i*2048)+"""]
        ldr.w {a32}, [r0, #"""+str(128 + i*2048)+"""]
        ldr.w {a40}, [r0, #"""+str(160 + i*2048)+"""]
        ldr.w {a48}, [r0, #"""+str(192 + i*2048)+"""]
        ldr.w {a56}, [r0, #"""+str(224 + i*2048)+"""]
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
        str.w {a0}, [r0, #"""+str(0 + i*2048)+"""]
        str.w {a8}, [r0, #"""+str(32 + i*2048)+"""]
        str.w {a16}, [r0, #"""+str(64 + i*2048)+"""]
        str.w {a24}, [r0, #"""+str(96 + i*2048)+"""]
        str.w {a32}, [r0, #"""+str(128 + i*2048)+"""]
        str.w {a40}, [r0, #"""+str(160 + i*2048)+"""]
        str.w {a48}, [r0, #"""+str(192 + i*2048)+"""]
        str.w {a56}, [r0, #"""+str(224 + i*2048)+"""]
    """

    combine_4_5_6 += (load + calculate_level4_5_6 + store)

combine_4_5_6 += """
        add.w r0, #"""+str(4)+"""
        vmov.w r4, inner_counter
        cmp.w r4, r0
        bne.w normal_4_5_6_inner

    add.w r0, #"""+str(224)+"""
    vmov.w r4, outer_counter
    cmp.w r4, r0
    bne.w normal_4_5_6_outer
"""

combine_4_5_6 = combine_4_5_6.format(a0="r4", a8="r5", a16="r6", a24="r7", a32="r8", 
                    a40="r9", a48="r10", a56="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")

combine_7_8_9 = """
.align 2
_7_8_9:
"""

combine_7_8_9 += """
sub.w r0, #"""+str(8*256)+""" // reset pointer

add.w r12, r0, #"""+str(8*256)+"""   // set counter
vmov.w inner_counter, r12

.align 2
loop_7_8_9:
    vmov.w r1, tmp_root_table
    vldm.w r1!, {{s0-s6}}
    vmov.w tmp_root_table, r1
"""

for i in range(2):
    load = """
    ldr.w {a0}, [r0, #"""+str(0 + i*2048)+"""]
    ldr.w {a1}, [r0, #"""+str(4 + i*2048)+"""]
    ldr.w {a2}, [r0, #"""+str(8 + i*2048)+"""]
    ldr.w {a3}, [r0, #"""+str(12 + i*2048)+"""]
    ldr.w {a4}, [r0, #"""+str(16 + i*2048)+"""]
    ldr.w {a5}, [r0, #"""+str(20 + i*2048)+"""]
    ldr.w {a6}, [r0, #"""+str(24 + i*2048)+"""]
    ldr.w {a7}, [r0, #"""+str(28 + i*2048)+"""]
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
    str.w {a0}, [r0, #"""+str(0 + i*2048)+"""]
    str.w {a1}, [r0, #"""+str(4 + i*2048)+"""]
    str.w {a2}, [r0, #"""+str(8 + i*2048)+"""]
    str.w {a3}, [r0, #"""+str(12 + i*2048)+"""]
    str.w {a4}, [r0, #"""+str(16 + i*2048)+"""]
    str.w {a5}, [r0, #"""+str(20 + i*2048)+"""]
    str.w {a6}, [r0, #"""+str(24 + i*2048)+"""]
    str.w {a7}, [r0, #"""+str(28 + i*2048)+"""]
    """

    combine_7_8_9 += (load + calculate_level7_8_9 + store)

combine_7_8_9 += """
    add.w r0, #"""+str(32)+"""
    vmov.w r4, inner_counter
    cmp.w r4, r0
    bne.w loop_7_8_9
"""

combine_7_8_9 = combine_7_8_9.format(a0="r4", a1="r5", a2="r6", a3="r7", a4="r8", 
                    a5="r9", a6="r10", a7="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")


text = """
sub.w r0, #"""+str(2048)+"""

.align 2
my_mul:
    lower          .req r14
    tmp1           .req r12
    counter        .req r1

    M              .req r2
    M_inv          .req r3
    K0             .req r4
    K1             .req r5
    K2             .req r6
    K3             .req r7
    B0             .req r8
    B1             .req r9
    B2             .req r10
    B3             .req r11

    
    add.w counter, r0, #"""+str(2048)+"""  // set counter
    
    my_multiply:
"""

unroll = 8

for i in range(unroll):
    load = """
        ldr.w K0, [r0, #"""+str(0+16*i)+"""]
        ldr.w K1, [r0, #"""+str(4+16*i)+"""]
        ldr.w K2, [r0, #"""+str(8+16*i)+"""]
        ldr.w K3, [r0, #"""+str(12+16*i)+"""]
        ldr.w B0, [r0, #"""+str(2048+0+16*i)+"""]
        ldr.w B1, [r0, #"""+str(2048+4+16*i)+"""]
        ldr.w B2, [r0, #"""+str(2048+8+16*i)+"""]
        ldr.w B3, [r0, #"""+str(2048+12+16*i)+"""]
        """
    
    compute = """
        smull.w lower, K0, K0, B0
        mul.w tmp1, lower, M_inv
        smlal.w lower, K0, tmp1, M 

        smull.w lower, K1, K1, B1
        mul.w tmp1, lower, M_inv
        smlal.w lower, K1, tmp1, M 

        smull.w lower, K2, K2, B2
        mul.w tmp1, lower, M_inv
        smlal.w lower, K2, tmp1, M

        smull.w lower, K3, K3, B3
        mul.w tmp1, lower, M_inv
        smlal.w lower, K3, tmp1, M  
        """
    
    store = """
        str.w K0, [r0, #"""+str(0+16*i)+"""]
        str.w K1, [r0, #"""+str(4+16*i)+"""]
        str.w K2, [r0, #"""+str(8+16*i)+"""]
        str.w K3, [r0, #"""+str(12+16*i)+"""]
    """

    text += (load + compute + store)

store = """
        add.w r0, #"""+str(4*4*8)+"""
        cmp.w counter, r0
        bne.w my_multiply
"""

text += store

combine_9_8_7 = """
sub.w r0, #"""+str(2048)+""" // reset pointer

_9_8_7:
add.w r12, r0, #"""+str(8*256)+"""   // set counter
vmov.w inner_counter, r12

.align 2
loop_9_8_7:
"""

for i in range(2):
    load = """
    vmov.w r1, tmp_inv_table
    vldm.w r1!, {{s0-s6}}
    vmov.w tmp_inv_table, r1

    ldr.w {a0}, [r0, #"""+str(0 + i*32)+"""]
    ldr.w {a1}, [r0, #"""+str(4 + i*32)+"""]
    ldr.w {a2}, [r0, #"""+str(8 + i*32)+"""]
    ldr.w {a3}, [r0, #"""+str(12 + i*32)+"""]
    ldr.w {a4}, [r0, #"""+str(16 + i*32)+"""]
    ldr.w {a5}, [r0, #"""+str(20 + i*32)+"""]
    ldr.w {a6}, [r0, #"""+str(24 + i*32)+"""]
    ldr.w {a7}, [r0, #"""+str(28 + i*32)+"""]
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
    str.w {a0}, [r0, #"""+str(0 + i*32)+"""]
    str.w {a1}, [r0, #"""+str(4 + i*32)+"""]
    str.w {a2}, [r0, #"""+str(8 + i*32)+"""]
    str.w {a3}, [r0, #"""+str(12 + i*32)+"""]
    str.w {a4}, [r0, #"""+str(16 + i*32)+"""]
    str.w {a5}, [r0, #"""+str(20 + i*32)+"""]
    str.w {a6}, [r0, #"""+str(24 + i*32)+"""]
    str.w {a7}, [r0, #"""+str(28 + i*32)+"""]
    """

    combine_9_8_7 += (load + calculate_level9_8_7 + store)

combine_9_8_7 += """
    add.w r0, #"""+str(32*2)+"""
    vmov.w r4, inner_counter
    cmp.w r4, r0
    bne.w loop_9_8_7
"""

combine_9_8_7 = combine_9_8_7.format(a0="r4", a1="r5", a2="r6", a3="r7", a4="r8", 
                    a5="r9", a6="r10", a7="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")


combine_6_5_4 = """
sub.w r0, #"""+str(2048)+""" // reset pointer

.align 2
_6_5_4:
"""

combine_6_5_4 += """
add.w r1, r0, #"""+str(8*256)+"""   // outer iteration set counter
vmov.w outer_counter, r1

.align 2
normal_6_5_4_outer:
    vmov.w r1, tmp_inv_table
    vldm.w r1!, {{s0-s6}}
    vmov.w tmp_inv_table, r1
"""

combine_6_5_4 += """
    add.w r4, r0, #"""+str(32)+""" // inner iteration set counter
    vmov.w inner_counter, r4
 
    normal_6_5_4_inner:
"""

for i in range(2):
    load = """
        ldr.w {a0}, [r0, #"""+str(0 + i*4)+"""]
        ldr.w {a8}, [r0, #"""+str(32 + i*4)+"""]
        ldr.w {a16}, [r0, #"""+str(64 + i*4)+"""]
        ldr.w {a24}, [r0, #"""+str(96 + i*4)+"""]
        ldr.w {a32}, [r0, #"""+str(128 + i*4)+"""]
        ldr.w {a40}, [r0, #"""+str(160 + i*4)+"""]
        ldr.w {a48}, [r0, #"""+str(192 + i*4)+"""]
        ldr.w {a56}, [r0, #"""+str(224 + i*4)+"""]
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
        str.w {a8}, [r0, #"""+str(32 + i*4)+"""]
        str.w {a16}, [r0, #"""+str(64 + i*4)+"""]
        str.w {a24}, [r0, #"""+str(96 + i*4)+"""]
        str.w {a32}, [r0, #"""+str(128 + i*4)+"""]
        str.w {a40}, [r0, #"""+str(160 + i*4)+"""]
        str.w {a48}, [r0, #"""+str(192 + i*4)+"""]
        str.w {a56}, [r0, #"""+str(224 + i*4)+"""]
    """

    combine_6_5_4 += (load + calculate_level6_5_4 + store)

combine_6_5_4 += """
        add.w r0, #"""+str(4*2)+"""
        vmov.w r4, inner_counter
        cmp.w r4, r0
        bne.w normal_6_5_4_inner

    add.w r0, #224
    vmov.w r4, outer_counter
    cmp.w r4, r0
    bne.w normal_6_5_4_outer
"""

combine_6_5_4 = combine_6_5_4.format(a0="r4", a8="r5", a16="r6", a24="r7", a32="r8", 
                    a40="r9", a48="r10", a56="r11", temp_lower="r12", 
                    temp_upper="r14", M="r2", M_inv="r3", c_temp="r1")

combine_3_2_1 = """
sub.w r0, #"""+str(2048)+""" // reset pointer
vmov.w tmp_save, r0
add.w r12, r0, #"""+str(4*64)+""" // set counter
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
    ldr.w {a64}, [r0, #"""+str(256+4*i)+"""]
    ldr.w {a128}, [r0, #"""+str(512+4*i)+"""]
    ldr.w {a192}, [r0, #"""+str(768+4*i)+"""]
    ldr.w {a256}, [r0, #"""+str(1024+4*i)+"""]
    ldr.w {a320}, [r0, #"""+str(1280+4*i)+"""]
    ldr.w {a384}, [r0, #"""+str(1536+4*i)+"""]
    ldr.w {a448}, [r0, #"""+str(1792+4*i)+"""]
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
    strb.w {a64}, [{c_temp}, #"""+str(64+1*i)+"""]
    strb.w {a128}, [{c_temp}, #"""+str(128+1*i)+"""]
    strb.w {a192}, [{c_temp}, #"""+str(192+1*i)+"""]
    strb.w {a256}, [{c_temp}, #"""+str(256+1*i)+"""]
    strb.w {a320}, [{c_temp}, #"""+str(320+1*i)+"""]
    strb.w {a384}, [{c_temp}, #"""+str(384+1*i)+"""]
    strb.w {a448}, [{c_temp}, #"""+str(448+1*i)+"""]
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
add.w sp, #"""+str(4096)+"""
vpop.w {s16, s17}
pop.w {r4-r12, pc}
"""

NTT = lin + macro + start + combine_1_2_3 + combine_4_5_6 + combine_7_8_9 + text + \
                   combine_9_8_7 + combine_6_5_4 + combine_3_2_1 + End
print(NTT)