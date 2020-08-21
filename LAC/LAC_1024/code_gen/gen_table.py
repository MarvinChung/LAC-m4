    
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


from argparse import ArgumentParser
import numpy as np
import sys


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
print(lin)

def center(a, b):
    if a > b//2:
        a -= b
    elif a < -b//2:
        a += b
    return a

def modInverse(a, m): 
    m0 = m 
    y = 0
    x = 1 
    if (m == 1) : 
        return 0
    while (a > 1) : 
        q = a // m 
        t = m 
        m = a % m 
        a = t 
        t = y 
        y = x - q * y 
        x = t 
    if (x < 0) : 
        x = x + m0  
    return center(x, m)

parser = ArgumentParser()
parser.add_argument("-n", help="n is poly length", dest="n", default="1024")
parser.add_argument("-q", help="q is prime", dest="q", default="251")
parser.add_argument("-m", help="MOD is prime", dest="m", default="270337")
parser.add_argument("-g", help="generator", dest="g", default="10")
args = parser.parse_args()

MOD = int(args.m)
G = int(args.g)
n = int(args.n)
q = int(args.q)
R = 2**32

RmodM = center(R % MOD, MOD)
inv8 = center(modInverse(8, MOD), MOD)
inv64 = center(modInverse(64, MOD), MOD)
inv512 = center(modInverse(512, MOD), MOD)
inv1024 = center(modInverse(1024, MOD), MOD)
Mprime = center(modInverse(-MOD % R, R), R)
Rinv512 = center((R*inv512) % MOD, MOD)
R2inv512 = center((R*R*inv512) % MOD, MOD)
Rinv8 = center((R*inv8) % MOD, MOD)
R2inv8 = center((R*R*inv8) % MOD, MOD)
Rinv64 = center((R*inv64) % MOD, MOD)
R2inv64 = center((R*R*inv64) % MOD, MOD)
Rinv1024 = center((R*inv1024) % MOD, MOD)
R2inv1024 = center((R*R*inv1024) % MOD, MOD)
qbar = int(round(R/float(q)))
invR = center(modInverse(R, MOD), MOD)

head = """
#ifndef NTT_H
#define NTT_H

#define LAC_N """+str(n)+"""
#define LAC_Q """+str(q)+"""

#define RmodM """+str(RmodM)+"""
#define R2inv512 """+str(R2inv512)+"""
#define Rinv512 """+str(Rinv512)+"""
#define inv512 """+str(inv512)+"""
#define R2inv8 """+str(R2inv8)+"""
#define Rinv8 """+str(Rinv8)+"""
#define inv8 """+str(inv8)+"""
#define R2inv64 """+str(R2inv64)+"""
#define Rinv64 """+str(Rinv64)+"""
#define inv64 """+str(inv64)+"""
#define R2inv1024 """+str(R2inv1024)+"""
#define Rinv1024 """+str(Rinv1024)+"""
#define inv1024 """+str(inv1024)+"""
#define MOD """+str(MOD)+"""
#define Mprime """+str(Mprime)+"""
#define Q_bar """+str(qbar)+"""
"""

print(head)

TABLE = []
for i in range(2,11):
    tmp = []
    for j in range(0, 2**i, 2):
        fmt = '{:0' + str(i) + 'b}'
        bitrev = int(fmt.format(j)[::-1], 2)
        c = (pow(G, bitrev*(MOD-1)//(2**i), MOD) * R) % MOD
        if c > MOD/2:
            c = c-MOD
        tmp.append(c)
    TABLE.append(tmp[int(len(tmp)/2):])


rearrange = []
rearrange.append(center((TABLE[0][0]*invR)%MOD, MOD))
rearrange.append(TABLE[1][0])
rearrange.append(TABLE[1][1])
rearrange.append(TABLE[2][0])
rearrange.append(TABLE[2][1])
rearrange.append(TABLE[2][2])
rearrange.append(TABLE[2][3])
for i in range(0, len(TABLE[3])):
    rearrange.append(TABLE[3][i])
    rearrange.append(TABLE[4][i*2])
    rearrange.append(TABLE[4][i*2+1])
    rearrange.append(TABLE[5][i*4])
    rearrange.append(TABLE[5][i*4+1])
    rearrange.append(TABLE[5][i*4+2])
    rearrange.append(TABLE[5][i*4+3])
for i in range(0, len(TABLE[6])):
    rearrange.append(TABLE[6][i])
    rearrange.append(TABLE[7][i*2])
    rearrange.append(TABLE[7][i*2+1])
    rearrange.append(TABLE[8][i*4])
    rearrange.append(TABLE[8][i*4+1])
    rearrange.append(TABLE[8][i*4+2])
    rearrange.append(TABLE[8][i*4+3])
print("int root_table[" +str(len(rearrange))+ "] = {" + str(rearrange)[1:-1] + "};")


INV_TABLE = []
for i in range(2,11):
    tmp = []
    for j in range(0, 2**i, 2):
        fmt = '{:0' + str(i) + 'b}'
        bitrev = int(fmt.format(j)[::-1], 2)
        c = (pow(G, ((MOD-1)-(bitrev*(MOD-1)//(2**i))) % (MOD-1), MOD) * R) % MOD
        if c > MOD/2:
            c = c-MOD
        tmp.append(c)
    INV_TABLE.append(tmp[int(len(tmp)/2):])
    
rearrange_inv = []
for i in range(0, len(INV_TABLE[6])):
    rearrange_inv.append(INV_TABLE[6][i])
    rearrange_inv.append(INV_TABLE[7][i*2])
    rearrange_inv.append(INV_TABLE[7][i*2+1])
    rearrange_inv.append(INV_TABLE[8][i*4])
    rearrange_inv.append(INV_TABLE[8][i*4+1])
    rearrange_inv.append(INV_TABLE[8][i*4+2])
    rearrange_inv.append(INV_TABLE[8][i*4+3])
for i in range(0, len(INV_TABLE[3])):
    rearrange_inv.append(INV_TABLE[3][i])
    rearrange_inv.append(INV_TABLE[4][i*2])
    rearrange_inv.append(INV_TABLE[4][i*2+1])
    rearrange_inv.append(INV_TABLE[5][i*4])
    rearrange_inv.append(INV_TABLE[5][i*4+1])
    rearrange_inv.append(INV_TABLE[5][i*4+2])
    rearrange_inv.append(INV_TABLE[5][i*4+3])
rearrange_inv.append(center((INV_TABLE[0][0] * Rinv512) % MOD, MOD))
rearrange_inv.append(INV_TABLE[1][0])
rearrange_inv.append(INV_TABLE[1][1])
rearrange_inv.append(INV_TABLE[2][0])
rearrange_inv.append(INV_TABLE[2][1])
rearrange_inv.append(INV_TABLE[2][2])
rearrange_inv.append(INV_TABLE[2][3])
rearrange_inv.append(R2inv512)
print("int root_table_inv[" +str(len(rearrange_inv))+ "] = {" + str(rearrange_inv)[1:-1] + "};")


TABLE = []
for i in range(10,11):
    tmp = []
    for j in range(0, 2**i):
        fmt = '{:0' + str(i) + 'b}'
        bitrev = int(fmt.format(j)[::-1], 2)
        c = (pow(G, bitrev*(MOD-1)//(2**i), MOD) * R) % MOD
        if c > MOD/2:
            c = c-MOD
        tmp.append(c)
    TABLE.append(tmp[int(len(tmp)/2):])
#print(TABLE)
print("int mul_table[" +str(len(TABLE[0]))+ "] = {" + str(TABLE[0])[1:-1] + "};")

print("#endif")