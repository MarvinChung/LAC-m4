LDSCRIPT   = ../../libopencm3/lib/stm32/f4/stm32f405x6.ld
LIBNAME    = opencm3_stm32f4
ARCH_FLAGS = -mthumb -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16
DEFINES    = -DSTM32F4
OBJS       = stm32f4_wrapper.o

all: 	test.bin

test.elf: test.o NTT.h NTT.S $(OBJS) $(LDSCRIPT)
		$(LD) -o $@ test.o NTT.h NTT.S $(OBJS) $(LDFLAGS) -l$(LIBNAME) -g

include ../../common/make.mk
