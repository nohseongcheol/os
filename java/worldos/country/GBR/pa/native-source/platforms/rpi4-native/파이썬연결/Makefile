MICROPYTHON_DIR ?= ../build/micropython-1.24.1
BUILD = ../build/python
CLEAN_EXTRA += ../build/user/python.elf
# Cleaning must also work before MicroPython has been extracted.
ifeq ($(strip $(MAKECMDGOALS)),clean)
.PHONY: clean
clean:
	rm -rf -- "$(BUILD)" $(CLEAN_EXTRA)
else
include $(MICROPYTHON_DIR)/py/mkenv.mk
QSTR_DEFS = qstrdefsport.h
MICROPY_ROM_TEXT_COMPRESSION = 0
include $(TOP)/py/py.mk
CC = clang
LD = aarch64-linux-gnu-ld
NEWLIB_INCLUDE ?= /usr/include/newlib
INC = -I. -I$(TOP) -I$(BUILD) -I../ਉਪਭੋਗਤਾ -I../../../posix-kor/arm64-native/포함 -isystem $(NEWLIB_INCLUDE)
CFLAGS = --target=aarch64-none-elf -mcpu=cortex-a72 -mgeneral-regs-only -std=gnu11 -Os -g \
    -ffreestanding -fno-builtin -fno-stack-protector -fno-pic -fno-unwind-tables \
    -fno-asynchronous-unwind-tables -ffunction-sections -fdata-sections -DNDEBUG $(INC)
SRC_C = ਚਲਾਓ_2.c 제이코로스모듈.c shared/libc/string0.c shared/libc/printf.c shared/runtime/gchelper_native.c extmod/modhashlib.c extmod/modjson.c
SRC_QSTR += ਚਲਾਓ_2.c 제이코로스모듈.c extmod/modhashlib.c extmod/modjson.c
OBJ = $(PY_CORE_O) $(addprefix $(BUILD)/,$(SRC_C:.c=.o)) $(BUILD)/수거저장기.o
all: ../build/user/python.elf
../build/user/python.elf: $(OBJ) ../build/user/start.o ../ਉਪਭੋਗਤਾ/ਲਿੰਕ_ਖਾਕਾ.ld
	$(ECHO) "LINK $@"
	$(Q)$(LD) -T ../ਉਪਭੋਗਤਾ/ਲਿੰਕ_ਖਾਕਾ.ld -z max-page-size=4096 --gc-sections -o $@ ../build/user/start.o $(OBJ)
include $(TOP)/py/mkrules.mk
endif
