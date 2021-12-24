## Intro
This repo only contains the LAC with Number Theorectic Transform (NTT) implementation on Cortex M4 and will not be updated in the future.  
The full paper link: [NTT Multiplication for NTT-unfriendly Rings](https://artifacts.iacr.org/tches/2021/a7/).  
The latest repo which contains all artficats in the paper: [ntt-polymul](https://github.com/ntt-polymul/ntt-polymul). 
## setup
```
git clone https://github.com/MarvinChung/LAC-m4.git --recursive
cd LAC-m4/libopencm3
make -j4
cd ../pqm4/libopencm3
make -j4
```

## test with cortex m4 
Set up your cortex-m4. <br> 
Follow README.md usage in LAC folder.
