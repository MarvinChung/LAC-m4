## tree
```
.
├── LAC
│   └── our-lac-(version)
│       ├── opt (LAC with NTT multiplication)
│       │   ├── NTT.S
│       │   ├── NTT.h
│       │   ├── api.h
│       │   ├── bch-light.h
│       │   ├── bch.c
│       │   ├── bch.h
│       │   ├── bch128.h
│       │   ├── bch192.h
│       │   ├── bch256.h
│       │   ├── bin-lwe.c
│       │   ├── bin-lwe.h
│       │   ├── ecc.c
│       │   ├── ecc.h
│       │   ├── encrypt.c
│       │   ├── kem.c
│       │   ├── lac_param.h
│       │   ├── rand.c
│       │   └── rand.h	
│       └── ref (LAC original code in opt)
│           ├── api.h
│           ├── bch-light.h
│           ├── bch.c
│           ├── bch.h
│           ├── bch128.h
│           ├── bch192.h
│           ├── bch256.h
│           ├── bin-lwe.c
│           ├── bin-lwe.h
│           ├── ecc.c
│           ├── ecc.h
│           ├── encrypt.c
│           ├── kem.c
│           ├── lac_param.h
│           ├── rand.c
│           └── rand.h
└── pqm4
    ├── Makefile
    ├── README.md
    ├── benchmarks.csv
    ├── benchmarks.md
    ├── benchmarks.py
    ├── bin
    ├── build_everything.py
    ├── common
    ├── convert_benchmarks.py
    ├── crypto_kem
    ├── hostside
    │   └── host_unidirectional.py
    ├── interface.py
    ├── libopencm3
    └── mupq
        └── crypto_kem
            └── our-lac
```
## usage
Preprare cortex-m4, r->pa2, t->pa3.  
If you see " No such file or directory: '/dev/ttyUSB0' ", you are using os other than Linux.
MAC: change "/dev/ttyUSB0" to "/dev/tty.usbserial-0001" in host_unidirectional.py 
Other: find the name of your device.
```
sh cp2pqm4.sh   (copy our-lac-* to ../pqm4/mupq/crypto_kem/our-lac-*)
cd ../pqm4
cd hostside
./host_unidirectional.py
```
open another terminal
```
cd ../pqm4
./build_everything.py our-lac-(version)
(test lac with NTT speed)
st-flash write ./bin/mupq_crypto_kem_our-lac-(version)_opt_speed.bin 0x8000000
(test lac with c code speed)
st-flash write ./bin/mupq_crypto_kem_our-lac-(version)_ref_speed.bin 0x8000000
```
the result will be shown on the first terminal

## comparison
### lac-256 with NTT1024
 - speed 
	```
	keypair cycles(non constant):  
	547500
	encaps cycles (non constant):
	907519
	decaps cycles (non constant):
	1337201
	```
- poly mul (speed.bin)
	```
	poly_aff(a,sk,e,pk+SEED_LEN,DIM_N):   145705
	poly_aff(a,r,e1,c,DIM_N):             145705
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 143761
	poly_mul(c,sk,out,c2_len):            131853
	poly_aff(a,r,e1,c,DIM_N):             145715
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 143771
	```
- stack
	```
	keypair stack usage:
	12744
	encaps stack usage:
	15840
	decaps stack usage:
	18792
	```
- hashing
	```
	keypair hash cycles:
	252681
	encaps hash cycles:
	354692
	decaps hash cycles:
	354515
	```

### lac-256 with c code 
- speed
	```
	keypair cycles(non constant):  
	2109580
	encaps cycles (non constant):
	3798305
	decaps cycles (non constant):
	5562511
	```
- poly mul (speed.bin)
	```
	poly_aff(a,sk,e,pk+SEED_LEN,DIM_N):   1705457 (non constant)
	poly_aff(a,r,e1,c,DIM_N):             1706992 (non constant)
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 1468673 (non constant)
	poly_mul(c,sk,out,c2_len):            1464260 (non constant)
	poly_aff(a,r,e1,c,DIM_N):             1706992 (non constant)
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 1468673 (non constant)
	```
- stack
	```
	keypair stack usage:
	14756
	encaps stack usage:
	17852
	decaps stack usage:
	20804
	```
- hashing
	```
	keypair hash cycles:
	252682
	encaps hash cycles:
	354695
	decaps hash cycles:
	354517
	```

### lac-128 with NTT512
 - speed 
	```
	keypair cycles(non constant):  
	368006
	encaps cycles (non constant):
	604930
	decaps cycles (non constant):
	785468
	```
- poly mul (speed.bin)
	```
	poly_aff(a,sk,e,pk+SEED_LEN,DIM_N):   72187
	poly_aff(a,r,e1,c,DIM_N):             72188
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 70459
	poly_mul(c,sk,out,c2_len):            65247
	poly_aff(a,r,e1,c,DIM_N):             72188
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 70459
	```
- stack
	```
	keypair stack usage:
	6588
	encaps stack usage:
	8124
	decaps stack usage:
	9556
	```
- hashing
	```
	keypair hash cycles:
	173295
	encaps hash cycles:
	247316
	decaps hash cycles:
	247312
	```

### lac-128 with c code 
- speed
	```
	keypair cycles(non constant):  
	936890
	encaps cycles (non constant):
	1586275
	decaps cycles (non constant):
	2183438
	```
- poly mul (speed.bin)
	```
	poly_aff(a,sk,e,pk+SEED_LEN,DIM_N):   638827 (non constant)
	poly_aff(a,r,e1,c,DIM_N):             638572 (non constant)
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 480683 (non constant)
	poly_mul(c,sk,out,c2_len):            479519 (non constant)
	poly_aff(a,r,e1,c,DIM_N):             638572 (non constant)
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 480683 (non constant)
	```
- stack
	```
	keypair stack usage:
	7588
	encaps stack usage:
	9124
	decaps stack usage:
	10556
	```
- hashing
	```
	keypair hash cycles:
	173295
	encaps hash cycles:
	247314
	decaps hash cycles:
	247312
	```

### lac-192 with NTT1024
 - speed 
	```
	keypair cycles(non constant):  
	461388
	encaps cycles (non constant):
	769503
	decaps cycles (non constant):
	1048654
	```
- poly mul (speed.bin)
	```
	poly_aff(a,sk,e,pk+SEED_LEN,DIM_N):   145065
	poly_aff(a,r,e1,c,DIM_N):             145063
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 140096
	poly_mul(c,sk,out,c2_len):            131214
	poly_aff(a,r,e1,c,DIM_N):             145072
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 140105
	```
- stack
	```
	keypair stack usage:
	12744
	encaps stack usage:
	15616
	decaps stack usage:
	18344
	```
- hashing
	```
	keypair hash cycles:
	180521
	encaps hash cycles:
	246452
	decaps hash cycles:
	246324
	```

### lac-192 with c code 
- speed
	```
	keypair cycles(non constant):  
	1462700
	encaps cycles (non constant):
	2375053
	decaps cycles (non constant):
	3257822
	```
- poly mul (speed.bin)
	```
	poly_aff(a,sk,e,pk+SEED_LEN,DIM_N):   1144049 (non constant)
	poly_aff(a,r,e1,c,DIM_N):             1148656 (non constant)
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 739809 (non constant)
	poly_mul(c,sk,out,c2_len):            734548 (non constant)
	poly_aff(a,r,e1,c,DIM_N):             1148656 (non constant)
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 739809 (non constant)
	```
- stack
	```
	keypair stack usage:
	14756
	encaps stack usage:
	17628
	decaps stack usage:
	20356
	```
- hashing
	```
	keypair hash cycles:
	180522
	encaps hash cycles:
	246455
	decaps hash cycles:
	246326
	```

### lac-LIGHT with NTT512
 - speed 
	```
	keypair cycles(non constant):  
	275660
	encaps cycles (non constant):
	461869
	decaps cycles (non constant):
	608330
	```
- poly mul (speed.bin)
	```
	poly_aff(a,sk,e,pk+SEED_LEN,DIM_N):   71547
	poly_aff(a,r,e1,c,DIM_N):             71548
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 68307
	poly_mul(c,sk,out,c2_len):            64607
	poly_aff(a,r,e1,c,DIM_N):             71548
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 68307
	```
- stack
	```
	keypair stack usage:
	6588
	encaps stack usage:
	8012
	decaps stack usage:
	9332
	```
- hashing
	```
	keypair hash cycles:
	95724
	encaps hash cycles:
	130958
	decaps hash cycles:
	130955
	```

### lac-LIGHT with c code 
- speed
	```
	keypair cycles(non constant):  
	534614
	encaps cycles (non constant):
	832734
	decaps cycles (non constant):
	1092752
	```
- poly mul (speed.bin)
	```
	poly_aff(a,sk,e,pk+SEED_LEN,DIM_N):   326443 (non constant)
	poly_aff(a,r,e1,c,DIM_N):             329004 (non constant)
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 177563 (non constant)
	poly_mul(c,sk,out,c2_len):            175237 (non constant)
	poly_aff(a,r,e1,c,DIM_N):             329004 (non constant)
	poly_aff(pk+SEED_LEN,r,e2,c2,c2_len): 177563 (non constant)
	```
- stack
	```
	keypair stack usage:
	7588
	encaps stack usage:
	9012
	decaps stack usage:
	10332
	```
- hashing
	```
	keypair hash cycles:
	95723
	encaps hash cycles:
	130957
	decaps hash cycles:
	130952
	```	
