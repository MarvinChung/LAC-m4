
#ifndef NTT_H
#define NTT_H

#define LAC_N 1024
#define LAC_Q 251

#define RmodM 123377
#define R2inv512 -125628
#define Rinv512 8161
#define inv512 -528
#define R2inv8 69918
#define Rinv8 -18370
#define inv8 -33792
#define R2inv64 76324
#define Rinv64 65288
#define inv64 -4224
#define R2inv1024 -62814
#define Rinv1024 -131088
#define inv1024 -264
#define MOD 270337
#define Mprime -66838529
#define Q_bar 17111423

int root_table[511] = {87291, -81168, 26545, 55408, 20461, 43494, 21926, 128281, -36898, -68300, -16795, -14794, 53415, -123811, -122443, -99788, -65831, -109043, 93257, -40153, -76318, -91292, -128306, 102864, -76056, -68250, 100564, -50940, 24114, -51322, 76062, 78004, 69145, 133558, 128253, -18521, -40994, 43615, 27699, -20719, 101359, -131204, -101351, -86922, 40277, 43889, -101265, -51136, 91968, -92964, -80229, 80683, 12809, -3413, 100346, 113549, 55542, -120365, -133710, -79264, -28646, -76272, 484, -126039, 81710, -23798, 25119, -40778, 89927, 42288, 104877, 112677, 16936, 107700, 1188, -94889, -100356, -84447, -117044, -41563, 46517, 53707, -101103, 39729, 86239, -27825, 105870, -124584, 54892, -2557, 95275, -120127, -30211, -10966, -253, 83011, 81447, -2686, 95936, 48036, -86731, 111144, 16648, -107291, 16347, -32265, 60572, -130931, 8335, 93618, 22263, -93160, -73249, -51399, 113080, 29086, -59078, 22422, -1078, -111105, -123814, -44951, 106758, -44486, -72658, -13121, -126680, -97640, 91696, -107445, 90383, 89732, 51774, -27076, -133769, 106599, -129880, 38026, -76738, -126572, 65275, -7630, 80038, -54781, 102922, 83765, 125776, 124742, -64732, 62962, -76820, 14665, -116157, 69172, -50101, 56018, 11582, -44765, -130617, -112433, -74555, 82053, -54120, -49845, 73200, 15868, -96873, 317, -90392, -114068, -57404, 107055, -71411, -97747, -56983, 79694, -134605, 122313, -117218, -91325, 93370, -29543, -13067, 2916, -116898, 24563, 86086, -32407, -33069, -11935, 22789, 134953, 71647, -108218, -132255, 70380, 60713, -117387, 25031, 13545, -97443, 60018, -99822, -65925, 67452, 12672, 46748, -57347, 59608, 65689, 4544, -111026, 10884, -26249, 74953, 60143, -1927, -34351, 58098, -89602, 88336, 115525, 96352, -62312, 44863, -74516, 2401, 75124, 84475, 32780, -118165, -106977, -91318, -82756, -103772, 90544, -108586, -24632, 121684, -32865, -2471, -111216, -83849, 64221, -63058, 99350, 130026, 621, -19782, 122194, -73823, -60424, -50110, -31169, -101611, -89757, -71353, 37340, -7269, -31423, 104188, -2646, -59740, 36390, -111727, -83945, -105891, 27023, -95969, 115383, -48156, -72162, 29295, 43923, 57757, -118763, 107811, -41643, 84151, 27977, -107078, -105785, 92811, 52918, 16819, -49269, 51054, 19526, 83672, 117823, 17177, 108505, -80223, 63755, -30719, 69818, 5710, 35259, 6624, 27980, -92615, 40835, -120933, 27010, 120103, -28224, -72204, -122546, 134640, 41283, 42143, -104824, -95345, 43087, -91364, -126887, 68636, 96482, -91523, 135168, -12817, 116096, -115890, -93625, -62028, 79038, 35481, 106286, 115723, 9033, 113897, -822, 62858, -92411, 99557, -93452, -73426, 15138, 3902, 31104, 104773, -47013, -96123, 105759, 59329, 41830, 128311, 63254, -28290, 66105, 70656, 113678, 76376, 15315, 45200, -7582, -55386, -61996, 123940, -40200, -77009, 7223, -26463, 47932, -86770, 37844, -77536, 120540, 426, 106604, 29550, -44701, -104956, 6734, 30424, -49304, -33261, 33429, 49267, -125987, 48280, -36606, 8994, -45265, 18477, -104186, 103322, 97708, 14928, 55708, 98838, 132840, -93109, -25433, -64559, 129967, -13145, -119028, 59110, 39699, 43336, 17135, -71945, 47852, 119199, -884, -84594, -59035, -60291, 46845, 29433, -25045, 12224, -109519, -125857, 41956, 47229, 27389, 24437, -99100, -95698, 99518, 16580, -96509, -125525, 113461, 57819, 61439, -98444, -72985, 121391, -57608, 127559, 112313, 126343, 104887, -82399, -129974, -57218, 122350, 120328, 39202, 4711, 45324, -80902, -3031, -109935, 86741, 56036, -73010, 78865, 91192, -102430, 92661, -11689, 32061, -48985, -29306, 101331, 128018, -7431, -120958, 108127, 36519, -33875, 43441, -8768, -108865, -48491, -37743, 80424, -90169, 61733, 107882, -100322, 89076, -27194, -10796, 1146, 113939, -119318, -4794, 8622, 43510, 80460, 78600, -128295, -18283, 97936, 64425, 66897, 10739, -110667, -69359, 50983, 89164, -57843, 90107, -85080, -20216, 60454, 111874, 43220, -106152, 75122, 19085, 132141, 41105, -86446, -4375, 88056};
int root_table_inv[512] = {-75122, -132141, -19085, -88056, 4375, 86446, -41105, -90107, 20216, 85080, 106152, -43220, -111874, -60454, -66897, 110667, -10739, 57843, -89164, -50983, 69359, -43510, -78600, -80460, -64425, -97936, 18283, 128295, 27194, -1146, 10796, -8622, 4794, 119318, -113939, 37743, 90169, -80424, -89076, 100322, -107882, -61733, -108127, 33875, -36519, 48491, 108865, 8768, -43441, -32061, 29306, 48985, 120958, 7431, -128018, -101331, -56036, -78865, 73010, 11689, -92661, 102430, -91192, -39202, -45324, -4711, -86741, 109935, 3031, 80902, -126343, 82399, -104887, -120328, -122350, 57218, 129974, -61439, 72985, 98444, -112313, -127559, 57608, -121391, 95698, -16580, -99518, -57819, -113461, 125525, 96509, 109519, -41956, 125857, 99100, -24437, -27389, -47229, 84594, 60291, 59035, -12224, 25045, -29433, -46845, -39699, -17135, -43336, 884, -119199, -47852, 71945, 93109, 64559, 25433, -59110, 119028, 13145, -129967, 104186, -97708, -103322, -132840, -98838, -55708, -14928, -49267, -48280, 125987, -18477, 45265, -8994, 36606, 44701, -6734, 104956, -33429, 33261, 49304, -30424, 86770, 77536, -37844, -29550, -106604, -426, -120540, 61996, 40200, -123940, -47932, 26463, -7223, 77009, -70656, -76376, -113678, 55386, 7582, -45200, -15315, -105759, -41830, -59329, -66105, 28290, -63254, -128311, 73426, -3902, -15138, 96123, 47013, -104773, -31104, -9033, 822, -113897, 93452, -99557, 92411, -62858, 115890, 62028, 93625, -115723, -106286, -35481, -79038, 126887, -96482, -68636, -116096, 12817, -135168, 91523, -134640, -42143, -41283, 91364, -43087, 95345, 104824, -40835, -27010, 120933, 122546, 72204, 28224, -120103, 30719, -5710, -69818, 92615, -27980, -6624, -35259, -19526, -117823, -83672, -63755, 80223, -108505, -17177, 107078, -92811, 105785, -51054, 49269, -16819, -52918, -43923, 118763, -57757, -27977, -84151, 41643, -107811, 105891, 95969, -27023, -29295, 72162, 48156, -115383, 31423, 2646, -104188, 83945, 111727, -36390, 59740, 50110, 101611, 31169, 7269, -37340, 71353, 89757, -99350, -621, -130026, 60424, 73823, -122194, 19782, -121684, 2471, 32865, 63058, -64221, 83849, 111216, 106977, 82756, 91318, 24632, 108586, -90544, 103772, -44863, -2401, 74516, 118165, -32780, -84475, -75124, 34351, 89602, -58098, 62312, -96352, -115525, -88336, -4544, -10884, 111026, 1927, -60143, -74953, 26249, 65925, -12672, -67452, -65689, -59608, 57347, -46748, -60713, -25031, 117387, 99822, -60018, 97443, -13545, 11935, -134953, -22789, -70380, 132255, 108218, -71647, 13067, 116898, -2916, 33069, 32407, -86086, -24563, -79694, -122313, 134605, 29543, -93370, 91325, 117218, 90392, 57404, 114068, 56983, 97747, 71411, -107055, -82053, 49845, 54120, -317, 96873, -15868, -73200, 50101, -11582, -56018, 74555, 112433, 130617, 44765, -124742, -62962, 64732, -69172, 116157, -14665, 76820, -65275, -80038, 7630, -125776, -83765, -102922, 54781, 27076, -106599, 133769, 126572, 76738, -38026, 129880, 126680, -91696, 97640, -51774, -89732, -90383, 107445, 111105, 44951, 123814, 13121, 72658, 44486, -106758, 73249, -113080, 51399, 1078, -22422, 59078, -29086, 32265, 130931, -60572, 93160, -22263, -93618, -8335, -95936, 86731, -48036, -16347, 107291, -16648, -111144, 120127, 10966, 30211, 2686, -81447, -83011, 253, -86239, -105870, 27825, -95275, 2557, -54892, 124584, 84447, 41563, 117044, -39729, 101103, -53707, -46517, -104877, -16936, -112677, 100356, 94889, -1188, -107700, 126039, 23798, -81710, -42288, -89927, 40778, -25119, -55542, 133710, 120365, -484, 76272, 28646, 79264, 92964, -80683, 80229, -113549, -100346, 3413, -12809, 101351, -40277, 86922, -91968, 51136, 101265, -43889, 18521, -43615, 40994, 131204, -101359, 20719, -27699, -24114, -76062, 51322, -128253, -133558, -69145, -78004, 91292, -102864, 128306, 50940, -100564, 68250, 76056, 122443, 65831, 99788, 76318, 40153, -93257, 109043, -128281, 68300, 36898, 123811, -53415, 14794, 16795, -26657, -26545, 81168, -21926, -43494, -20461, -55408, -125628};
int mul_table[512] = {25119, -25119, -40778, 40778, 89927, -89927, 42288, -42288, 107700, -107700, 1188, -1188, -94889, 94889, -100356, 100356, 46517, -46517, 53707, -53707, -101103, 101103, 39729, -39729, -124584, 124584, 54892, -54892, -2557, 2557, 95275, -95275, -253, 253, 83011, -83011, 81447, -81447, -2686, 2686, 111144, -111144, 16648, -16648, -107291, 107291, 16347, -16347, 8335, -8335, 93618, -93618, 22263, -22263, -93160, 93160, 29086, -29086, -59078, 59078, 22422, -22422, -1078, 1078, 106758, -106758, -44486, 44486, -72658, 72658, -13121, 13121, -107445, 107445, 90383, -90383, 89732, -89732, 51774, -51774, -129880, 129880, 38026, -38026, -76738, 76738, -126572, 126572, -54781, 54781, 102922, -102922, 83765, -83765, 125776, -125776, -76820, 76820, 14665, -14665, -116157, 116157, 69172, -69172, -44765, 44765, -130617, 130617, -112433, 112433, -74555, 74555, 73200, -73200, 15868, -15868, -96873, 96873, 317, -317, 107055, -107055, -71411, 71411, -97747, 97747, -56983, 56983, -117218, 117218, -91325, 91325, 93370, -93370, -29543, 29543, 24563, -24563, 86086, -86086, -32407, 32407, -33069, 33069, 71647, -71647, -108218, 108218, -132255, 132255, 70380, -70380, 13545, -13545, -97443, 97443, 60018, -60018, -99822, 99822, 46748, -46748, -57347, 57347, 59608, -59608, 65689, -65689, -26249, 26249, 74953, -74953, 60143, -60143, -1927, 1927, 88336, -88336, 115525, -115525, 96352, -96352, -62312, 62312, 75124, -75124, 84475, -84475, 32780, -32780, -118165, 118165, -103772, 103772, 90544, -90544, -108586, 108586, -24632, 24632, -111216, 111216, -83849, 83849, 64221, -64221, -63058, 63058, -19782, 19782, 122194, -122194, -73823, 73823, -60424, 60424, -89757, 89757, -71353, 71353, 37340, -37340, -7269, 7269, -59740, 59740, 36390, -36390, -111727, 111727, -83945, 83945, 115383, -115383, -48156, 48156, -72162, 72162, 29295, -29295, 107811, -107811, -41643, 41643, 84151, -84151, 27977, -27977, 52918, -52918, 16819, -16819, -49269, 49269, 51054, -51054, 17177, -17177, 108505, -108505, -80223, 80223, 63755, -63755, 35259, -35259, 6624, -6624, 27980, -27980, -92615, 92615, 120103, -120103, -28224, 28224, -72204, 72204, -122546, 122546, -104824, 104824, -95345, 95345, 43087, -43087, -91364, 91364, -91523, 91523, 135168, -135168, -12817, 12817, 116096, -116096, 79038, -79038, 35481, -35481, 106286, -106286, 115723, -115723, 62858, -62858, -92411, 92411, 99557, -99557, -93452, 93452, 31104, -31104, 104773, -104773, -47013, 47013, -96123, 96123, 128311, -128311, 63254, -63254, -28290, 28290, 66105, -66105, 15315, -15315, 45200, -45200, -7582, 7582, -55386, 55386, -77009, 77009, 7223, -7223, -26463, 26463, 47932, -47932, 120540, -120540, 426, -426, 106604, -106604, 29550, -29550, 30424, -30424, -49304, 49304, -33261, 33261, 33429, -33429, -36606, 36606, 8994, -8994, -45265, 45265, 18477, -18477, 14928, -14928, 55708, -55708, 98838, -98838, 132840, -132840, 129967, -129967, -13145, 13145, -119028, 119028, 59110, -59110, -71945, 71945, 47852, -47852, 119199, -119199, -884, 884, 46845, -46845, 29433, -29433, -25045, 25045, 12224, -12224, 47229, -47229, 27389, -27389, 24437, -24437, -99100, 99100, -96509, 96509, -125525, 125525, 113461, -113461, 57819, -57819, 121391, -121391, -57608, 57608, 127559, -127559, 112313, -112313, -129974, 129974, -57218, 57218, 122350, -122350, 120328, -120328, -80902, 80902, -3031, 3031, -109935, 109935, 86741, -86741, 91192, -91192, -102430, 102430, 92661, -92661, -11689, 11689, 101331, -101331, 128018, -128018, -7431, 7431, -120958, 120958, 43441, -43441, -8768, 8768, -108865, 108865, -48491, 48491, 61733, -61733, 107882, -107882, -100322, 100322, 89076, -89076, 113939, -113939, -119318, 119318, -4794, 4794, 8622, -8622, -128295, 128295, -18283, 18283, 97936, -97936, 64425, -64425, -69359, 69359, 50983, -50983, 89164, -89164, -57843, 57843, 60454, -60454, 111874, -111874, 43220, -43220, -106152, 106152, 41105, -41105, -86446, 86446, -4375, 4375, 88056, -88056};
#endif
