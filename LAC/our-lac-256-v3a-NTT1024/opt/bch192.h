uint16_t a_pow_tab[512] = {1,2,4,8,16,32,64,128,256,17,34,68,136,272,49,98,196,392,257,19,38,76,152,304,113,226,452,409,291,87,174,348,169,
338,181,362,197,394,261,27,54,108,216,432,369,243,486,477,427,327,159,318,109,218,436,377,227,454,413,299,71,142,284,41,82,
164,328,129,258,21,42,84,168,336,177,354,213,426,325,155,310,125,250,500,505,483,471,447,367,207,414,301,75,150,300,73,146,
292,89,178,356,217,434,373,251,502,509,491,455,415,303,79,158,316,105,210,420,345,163,326,157,314,101,202,404,313,99,198,396,
265,3,6,12,24,48,96,192,384,273,51,102,204,408,289,83,166,332,137,274,53,106,212,424,321,147,294,93,186,372,249,498,
501,507,487,479,431,335,143,286,45,90,180,360,193,386,277,59,118,236,472,417,339,183,366,205,410,293,91,182,364,201,402,309,
123,246,492,457,387,279,63,126,252,504,481,467,439,383,239,478,429,331,135,270,13,26,52,104,208,416,337,179,358,221,442,357,
219,438,381,235,470,445,363,199,398,269,11,22,44,88,176,352,209,418,341,187,374,253,506,485,475,423,351,175,350,173,346,165,
330,133,266,5,10,20,40,80,160,320,145,290,85,170,340,185,370,245,490,453,411,295,95,190,380,233,466,437,379,231,462,397,
267,7,14,28,56,112,224,448,401,307,119,238,476,425,323,151,302,77,154,308,121,242,484,473,419,343,191,382,237,474,421,347,
167,334,141,282,37,74,148,296,65,130,260,25,50,100,200,400,305,115,230,460,393,259,23,46,92,184,368,241,482,469,443,359,
223,446,365,203,406,317,107,214,428,329,131,262,29,58,116,232,464,433,371,247,494,461,395,263,31,62,124,248,496,497,499,503,
511,495,463,399,271,15,30,60,120,240,480,465,435,375,255,510,493,459,391,287,47,94,188,376,225,450,405,315,103,206,412,297,
67,134,268,9,18,36,72,144,288,81,162,324,153,306,117,234,468,441,355,215,430,333,139,278,61,122,244,488,449,403,311,127,
254,508,489,451,407,319,111,222,444,361,195,390,285,43,86,172,344,161,322,149,298,69,138,276,57,114,228,456,385,275,55,110,
220,440,353,211,422,349,171,342,189,378,229,458,389,283,39,78,156,312,97,194,388,281,35,70,140,280,33,66,132,264,1};

uint16_t a_log_tab[512] = {0,0,1,130,2,260,131,290,3,420,261,235,132,213,291,390,4,9,421,19,262,69,236,343,133,332,214,39,292,365,391,377,5,
507,10,503,422,325,20,495,263,63,70,462,237,169,344,405,134,14,333,139,215,149,40,479,293,473,366,176,392,441,378,199,6,
329,508,417,11,470,504,60,423,95,326,92,21,306,496,111,264,426,64,144,71,269,463,29,238,98,170,187,345,156,406,279,135,
499,15,126,334,122,140,413,216,114,150,359,41,52,480,455,294,24,474,338,367,431,177,299,393,309,442,193,379,81,200,448,7,
67,330,363,509,258,418,211,12,147,471,439,505,323,61,167,424,267,96,154,327,468,93,304,22,429,307,79,497,120,112,50,265,
466,427,118,65,256,145,321,72,32,270,487,464,254,30,252,239,74,99,220,171,34,188,182,346,272,157,244,407,489,280,315,136,
173,500,459,16,36,127,232,335,190,123,356,141,184,414,89,217,241,115,484,151,76,360,436,42,101,53,225,481,222,456,353,295,
409,25,56,475,491,339,286,368,282,432,228,178,317,300,207,394,348,310,45,443,274,194,372,380,159,82,104,201,246,449,399,8,
18,68,342,331,38,364,376,510,129,259,289,419,234,212,389,13,138,148,478,472,175,440,198,506,502,324,494,62,461,168,404,425,
143,268,28,97,186,155,278,328,416,469,59,94,91,305,110,23,337,430,298,308,192,80,447,498,125,121,412,113,358,51,454,266,
153,467,303,428,78,119,49,66,362,257,210,146,438,322,166,73,219,33,181,271,243,488,314,465,117,255,320,31,486,253,251,240,
483,75,435,100,224,221,352,172,458,35,231,189,355,183,88,347,44,273,371,158,103,245,398,408,55,490,285,281,227,316,206,137,
477,174,197,501,493,460,403,17,341,37,375,128,288,233,388,336,297,191,446,124,411,357,453,142,27,185,277,415,58,90,109,218,
180,242,313,116,319,485,250,152,302,77,48,361,209,437,165,43,370,102,397,54,284,226,205,482,434,223,351,457,230,354,87,296,
445,410,452,26,276,57,108,476,196,492,402,340,374,287,387,369,396,283,204,433,350,229,86,179,312,318,249,301,47,208,164,395,
203,349,85,311,248,46,163,444,451,275,107,195,401,373,386,381,382,160,383,83,161,105,384,202,84,247,162,450,106,400,385};

uint32_t mod8_tab_half[48] = {0,0,0,3099199131,2334129702,3841982464,3385723820,2636120683,788529152,1903430967,373292109,3388997632,723915202,2975857392,3137339392,2476480345,977274070,
1577058304,3806861934,746584219,2483027968,1515330805,2808088253,1895825408,1447830405,1656747489,1979711488,4009108766,3919580103,2466250752,2676107305,4288673674,1493172224,
657993394,1954548140,3154116608,2104111687,3554676497,3439329280,3318756572,1493168439,671088640,3030661611,1321209210,3791650816,203308912,3319788380,117440512};

uint32_t g[3] = {3697083213,3314548499,1920991232};

struct bch_control bch={
.m = 9,
.t = 8,
.n = 511,
.ecc_bytes = 9,
.ecc_bits = 72,
.ecc_words = 3,
};

#define BCH_N 511
#define BCH_T 8
#define BCH_M 9
#define BCH_ECC_WORDS 3
#define BCH_ECC_BYTES 9

struct gf_poly {
unsigned int deg;
unsigned int c[2*BCH_T+1];
};