## tree
```
.
├── LAC
│   └── our-lac-/version/
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
If you see " No such file or directory: '/dev/ttyUSB0' ", you are using os other than Linux.
MAC: change "/dev/ttyUSB0" to "/dev/tty.usbserial-0001" in host_unidirectional.py 
Other: find the name of your device.
```
sh cp2pqm4.sh   (copy our-lac to ../pqm4/mupq/crypto_kem/our-lac)
cd ../pqm4
cd hostside
./host_unidirectional.py
```
open another terminal
```
cd ../pqm4
./build_everything.py our-lac-/version/
(test lac with NTT speed)
st-flash write ./bin/mupq_crypto_kem_our-lac_opt_speed.bin 0x8000000
(test lac with c code speed)
st-flash write ./bin/mupq_crypto_kem_our-lac_ref_speed.bin 0x8000000
```
the result will be shown on the first terminal

## comparison
### lac with NTT1024
 - speed
	```
	keypair cycles(non constant):  
	547500
	encaps cycles (non constant):
	907519
	decaps cycles (non constant):
	1337201
	```
- poly mul
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
## lac c code
- speed
	```
	keypair cycles(non constant):  
	2109580
	encaps cycles (non constant):
	3798305
	decaps cycles (non constant):
	5562511
	```
- poly mul
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
