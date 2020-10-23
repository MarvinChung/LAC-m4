
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


#ifndef NTT_H
#define NTT_H

#define LAC_N 512
#define LAC_Q 251

#define RmodM -48648
#define R2inv512 -53555
#define Rinv512 1985
#define inv512 -260
#define R2inv8 33626
#define Rinv8 -6081
#define inv8 -16640
#define R2inv64 -29077
#define Rinv64 15880
#define inv64 -2080
#define MOD 133121
#define Mprime -540932097
#define Q_bar 17111423

int root_table[511] = {47909, -11575, 35411, -35297, -7910, 14541, 22576, 10897, 53036, 21197, 64984, 17629, -20812, -5818, -36189, 5581, -59960, 14269, 37186, -11543, -28953, 4106, 59376, -17865, 12589, -44850, 52155, 12725, -38484, -60478, -61937, -49811, 64968, 40920, -36687, 53153, 11905, 66281, -12943, -8569, 45894, -23911, 35468, -60737, 43006, 15650, 38378, 35778, 22206, -3134, 17304, -60252, -38801, -15465, -938, 56256, 13682, 62764, 23328, 49652, 38519, 42604, -29257, 126, 11526, 13226, -23861, -46622, 12632, 18422, 46089, -29093, -39667, 27031, 27091, 20899, 47150, 41815, 47291, -54901, -2703, 28706, -44423, -56080, -23094, 54627, -33917, -61158, -25412, 39613, 46241, 12159, -2237, -10028, -48253, 26309, -27344, 20065, -11965, -31347, -65422, -63740, -57041, 23724, 6018, -25043, -16189, -35855, -42204, 23433, -41007, -4645, 34486, -29763, -56536, 54065, 64788, -30106, 17681, -4806, -31020, 25664, 49299, 33009, -16436, -21609, 48676, 6575, 37389, 31558, 57025, 11378, -21893, 40543, -64768, -52723, -35728, -22934, -38689, 25503, 6076, 35443, -52789, 13394, 49926, 60460, -1699, -64416, 23137, -28034, -320, -21965, -51258, -36435, 37999, 34470, 57225, -30880, -56247, -20920, 11729, -14670, 36224, -42861, 31223, -17970, 53398, 58525, 53850, -1670, -2309, 17797, -3532, -38812, -9980, 27380, 6670, 62630, -54858, 15981, 427, -43491, -25914, 11761, -43444, 31043, 11275, -25355, -3570, 42690, -21950, 53350, 38574, 56044, -16287, 61419, -35834, 3408, -65595, -4997, -49715, -40804, 3049, -20250, -64240, -49761, -41266, -32823, -25542, -43446, 28598, 26834, 40609, 11461, -39076, 64496, -65788, -7166, 57527, 56980, 33603, 53874, -14654, 21668, 3165, 60182, -8301, -18775, 7122, 50220, -38974, -17418, 12540, 3787, 25009, -65940, 28151, 37408, 56587, 28498, 21706, -49370, 26598, -12409, 15605, 7168, 12021, 32643, -41085, -14159, 29243, 37483, -40468, -45484, -35307, -37633, 31427, -40152, -43718, 49736, 16138, -11326, 16682, -40546, 61308, 23228, -63876, 54042, 27849, 12361, -52180, 58898, -21555, 26107, -40135, -27991, -27746, 63192, -56388, 64882, -44653, 23334, -41552, -15069, -25538, 16519, 4426, -39704, 36452, -35531, -35672, -2450, -49687, 15239, -12967, -8413, 31971, 18798, 29817, 64121, -60328, -56557, 56472, -34156, 29422, -39671, -44559, -48775, -44479, 53432, -43142, 43682, -34303, 26489, 19008, 29073, 35913, -33008, -15773, 59260, -16376, 57390, 13334, -2398, -2359, 8797, -5613, 17168, -52947, -66350, -62102, 9632, 50126, -16306, -2943, -21048, 34209, 34835, -27962, 44803, 23923, 48803, -34317, 50093, -30261, 46562, -45059, -41495, -36561, 5169, 149, 52440, -44673, -21761, 55923, -430, 32885, -10725, -58085, -32881, -11894, 61355, 63331, 31047, 23035, 1862, 15488, 50318, -3127, 54436, 813, -24942, -43848, -64452, -58768, -6962, -1877, 64603, -52182, -41431, 49452, 53091, -6228, 18551, 44063, -36555, 28540, 37069, 16557, -38726, -4475, 65156, 26381, 62099, -20238, -66262, -9671, 34086, 30867, 39914, -23233, -45116, 2588, 52841, 5202, 20106, -43339, 3401, -1595, -16500, -26002, -30491, -56586, -51246, -45488, 39299, 15390, -37709, 10771, 50843, 5989, -4606, 45764, 20804, 21909, 40994, 47433, -8808, -45674, 47332, -3916, -44155, 8383, -4910, 11098, 60449, 3786, 21469, 65475, -56327, 58669, -19762, -14548, 41424, 54281, 29694, -15475, -40926, -21106, 42565, -34014, -20163, -63191, 37554, 44271, -58103, -4761, -58476, -46364, 4130, -41756, 54184, 36604, 26951, 54880, 51988, -818, -35824, 37037, 33923, 6487, -51852, -57204, -24409, 52293, -31883, -57282, 4912, -28920, -62225, -25851, 54237, 51634, 50703, -27592, -13598, -38070, -4809, 50426, -20674, -61981, -20072, 36656, 53633, 1855, -59368, 1774, 12105, -208, 19003, -50267, 50308, 54406, 27874, 63369, 59867, -56963, 8151, 62366, 58460, 27421};
int root_table_inv[512] = {-63369, 56963, -59867, -27421, -58460, -62366, -8151, -12105, -19003, 208, -27874, -54406, -50308, 50267, 61981, -36656, 20072, -1774, 59368, -1855, -53633, -50703, 13598, 27592, 20674, -50426, 4809, 38070, 57282, 28920, -4912, -51634, -54237, 25851, 62225, -33923, 51852, -6487, 31883, -52293, 24409, 57204, -36604, -54880, -26951, -37037, 35824, 818, -51988, 58103, 58476, 4761, -54184, 41756, -4130, 46364, 21106, 34014, -42565, -44271, -37554, 63191, 20163, 19762, -41424, 14548, 40926, 15475, -29694, -54281, -11098, -3786, -60449, -58669, 56327, -65475, -21469, 8808, -47332, 45674, 4910, -8383, 44155, 3916, -5989, -45764, 4606, -47433, -40994, -21909, -20804, 51246, -39299, 45488, -50843, -10771, 37709, -15390, 43339, 1595, -3401, 56586, 30491, 26002, 16500, -39914, 45116, 23233, -20106, -5202, -52841, -2588, -26381, 20238, -62099, -30867, -34086, 9671, 66262, 36555, -37069, -28540, -65156, 4475, 38726, -16557, 52182, -49452, 41431, -44063, -18551, 6228, -53091, 24942, 64452, 43848, -64603, 1877, 6962, 58768, -23035, -15488, -1862, -813, -54436, 3127, -50318, 10725, 32881, 58085, -31047, -63331, -61355, 11894, -149, 44673, -52440, -32885, 430, -55923, 21761, -50093, -46562, 30261, -5169, 36561, 41495, 45059, -34209, 27962, -34835, 34317, -48803, -23923, -44803, 66350, -9632, 62102, 21048, 2943, 16306, -50126, -13334, 2359, 2398, 52947, -17168, 5613, -8797, -29073, 33008, -35913, -57390, 16376, -59260, 15773, 44479, 43142, -53432, -19008, -26489, 34303, -43682, 56557, 34156, -56472, 48775, 44559, 39671, -29422, 12967, -31971, 8413, 60328, -64121, -29817, -18798, 39704, 35531, -36452, -15239, 49687, 2450, 35672, 44653, 41552, -23334, -4426, -16519, 25538, 15069, -26107, 27991, 40135, -64882, 56388, -63192, 27746, 63876, -27849, -54042, 21555, -58898, 52180, -12361, -49736, 11326, -16138, -23228, -61308, 40546, -16682, 40468, 35307, 45484, 43718, 40152, -31427, 37633, -7168, -32643, -12021, -37483, -29243, 14159, 41085, -56587, -21706, -28498, -15605, 12409, -26598, 49370, 17418, -3787, -12540, -37408, -28151, 65940, -25009, -3165, 8301, -60182, 38974, -50220, -7122, 18775, 7166, -56980, -57527, -21668, 14654, -53874, -33603, -28598, -40609, -26834, 65788, -64496, 39076, -11461, 20250, 49761, 64240, 43446, 25542, 32823, 41266, 35834, 65595, -3408, -3049, 40804, 49715, 4997, -42690, -53350, 21950, -61419, 16287, -56044, -38574, 25914, 43444, -11761, 3570, 25355, -11275, -31043, -27380, -62630, -6670, 43491, -427, -15981, 54858, -53850, 2309, 1670, 9980, 38812, 3532, -17797, 14670, 42861, -36224, -58525, -53398, 17970, -31223, -37999, -57225, -34470, -11729, 20920, 56247, 30880, 64416, 28034, -23137, 36435, 51258, 21965, 320, -6076, 52789, -35443, 1699, -60460, -49926, -13394, -40543, 52723, 64768, -25503, 38689, 22934, 35728, -48676, -37389, -6575, 21893, -11378, -57025, -31558, 4806, -25664, 31020, 21609, 16436, -33009, -49299, -34486, 56536, 29763, -17681, 30106, -64788, -54065, 25043, 35855, 16189, 4645, 41007, -23433, 42204, 11965, 65422, 31347, -6018, -23724, 57041, 63740, -12159, 10028, 2237, -20065, 27344, -26309, 48253, 23094, 33917, -54627, -46241, -39613, 25412, 61158, -41815, 54901, -47291, 56080, 44423, -28706, 2703, -46089, 39667, 29093, -47150, -20899, -27091, -27031, -126, -13226, -11526, -18422, -12632, 46622, 23861, -13682, -23328, -62764, 29257, -42604, -38519, -49652, 3134, 60252, -17304, -56256, 938, 15465, 38801, -35468, -43006, 60737, -22206, -35778, -38378, -15650, -53153, -66281, -11905, 23911, -45894, 8569, 12943, 38484, 61937, 60478, 36687, -40920, -64968, 49811, -4106, 17865, -59376, -12725, -52155, 44850, -12589, 36189, 59960, -5581, 28953, 11543, -37186, -14269, -10897, -21197, -53036, 5818, 20812, -17629, -64984, -7659, -35411, 11575, -22576, -14541, 7910, 35297, -53555};
#endif
