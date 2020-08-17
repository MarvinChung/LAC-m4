/*
BSD 2-Clause License

Copyright (c) 2020, Cheng-Jhih Shi, Chi-Ming Chung, Vincent Hwang
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


#include "NTT.h"
#include "../../common/stm32wrapper.h"
#include <string.h>
#include <stdio.h>

void naive_mul(unsigned char des[], int src1[], int src2[]){
    int temp[2*LAC_N];
    memset(&temp, '\0', sizeof(temp));

    for (int i = 0; i < LAC_N; i++)
        for (int j = 0; j < LAC_N; j++)
            temp[i + j] = src1[i] * src2[j] + temp[i + j];

    for (int i = 0; i < LAC_N; i++){
        temp[i] = (temp[i] - temp[i + LAC_N]);
        temp[i] = temp[i] % LAC_Q;
    }

    for (int i = 0; i < LAC_N; i++){
        temp[i] = (temp[i] + LAC_Q) % LAC_Q;
    }

    for(int i = 0; i < LAC_N; i++)
        des[i] = (unsigned char)(temp[i]);
}


int main(){
    clock_setup();
    gpio_setup();
    usart_setup(115200);

    SCS_DEMCR |= SCS_DEMCR_TRCENA;
    DWT_CYCCNT = 0;
    DWT_CTRL |= DWT_CTRL_CYCCNTENA;

    send_USART_str((unsigned char*)"\n============ IGNORE OUTPUT BEFORE THIS LINE ============\n");
    
    int testtest1[LAC_N];
    int testtest2[LAC_N];
    unsigned char ary_input8_1[LAC_N] = {0};
    char ary_input8_2[LAC_N] = {0};
    unsigned char my_ans[LAC_N];
    
    int ary_test1[LAC_N] = {0}, ary_test2[LAC_N] = {0};
    unsigned char ary_test3[LAC_N] = {0};    
    
    
    char outstr[128];
    unsigned long long int oldcount, newcount;
    unsigned long long int accumulate = 0;
    
    // Generate input
    for(int i = 0; i < LAC_N; i++){
      ary_test1[i] = (rand() % LAC_Q);
      ary_test2[i] = (rand() % 3) - 1;
    }
    
    // pack inputs
    for(int i = 0; i < LAC_N; i++)
        ary_input8_1[i] = (unsigned char)ary_test1[i];
    
    for(int i = 0; i < LAC_N; i++)
        ary_input8_2[i] = (char)ary_test2[i];
    
    // naive multiplication
    naive_mul(ary_test3, ary_test1, ary_test2);

    // 512 NTT
    oldcount = DWT_CYCCNT;
    NTT_512(&ary_input8_1[0], root_table, MOD, Mprime, 
        &ary_input8_2[0], root_table_inv, &my_ans[0], Q_bar);
    newcount = DWT_CYCCNT;
    accumulate += (newcount-oldcount);
    sprintf(outstr, "Total: %llu", newcount-oldcount);
    send_USART_str((unsigned char*)outstr);

    // compare
    int flag = 0;
    for(int i = 0; i < LAC_N; i++){
        if(ary_test3[i] != my_ans[i]){
            sprintf(outstr, "%5x %5x %5d", ary_test3[i], my_ans[i], i);
            send_USART_str((unsigned char*)outstr);
            flag = 1;
        }
    }
    
    if(flag)
        send_USART_str((unsigned char*)"Test failed!\n");
    else
        send_USART_str((unsigned char*)"Test successful!\n");
    while(1);
    
    return 0;
}
