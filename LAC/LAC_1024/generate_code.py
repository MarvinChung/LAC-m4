
# BSD 2-Clause License

# Copyright (c) 2020, Cheng-Jhih Shi, Chi-Ming Chung, Vincent Hwang
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



from sympy import *
from argparse import ArgumentParser
import math
import sys
import os
import serial
import sys
import subprocess
import multiprocessing as mp
import shlex
import time
import platform
import re
import queue

parser = ArgumentParser()
parser.add_argument("-n", help="n is poly length", dest="n", default="1024")
parser.add_argument("-q", help="q is prime", dest="q", default="251")
parser.add_argument("-small", help="small range", dest="small", default="1")
args = parser.parse_args()

n = int(args.n)
q = int(args.q)
small = int(args.small)

MOD = q * n * small + 1

# find prime
while True:
    MOD = nextprime(MOD)
    if (MOD - 1) % (n*2) == 0:
        # print(MOD)
        break

# find generator
G = 2
for i in range(2, MOD):
    if is_primitive_root(i, MOD):
        G = i
        break

print("MOD: ", MOD)
print("G: ", G)
print("n: ", n)
print("q: ", q)

os.system('python3 code_gen/NTT.py > NTT.S')
os.system('python3 code_gen/gen_table.py -n '+str(n)+' -q '+str(q)+' -m '+str(MOD)+' -g '+str(G)+' > NTT.h')
