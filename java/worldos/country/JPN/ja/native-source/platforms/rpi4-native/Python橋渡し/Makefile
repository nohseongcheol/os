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
INC = -I. -I$(TOP) -I$(BUILD) -I../利用者 -I../../../posix-kor/arm64-native/ヘッダー -isystem $(NEWLIB_INCLUDE)
CFLAGS = --target=aarch64-none-elf -mcpu=cortex-a72 -mgeneral-regs-only -std=gnu11 -Os -g \
    -ffreestanding -fno-builtin -fno-stack-protector -fno-pic -fno-unwind-tables \
    -fno-asynchronous-unwind-tables -ffunction-sections -fdata-sections -DNDEBUG $(INC)
SRC_C = 起動処理.c JKorOSモジュール.c shared/libc/string0.c shared/libc/printf.c shared/runtime/gchelper_native.c extmod/modhashlib.c extmod/modjson.c
SRC_QSTR += 起動処理.c JKorOSモジュール.c extmod/modhashlib.c extmod/modjson.c
OBJ = $(PY_CORE_O) $(addprefix $(BUILD)/,$(SRC_C:.c=.o)) $(BUILD)/不要物回収レジスタ群.o
all: ../build/user/python.elf
../build/user/python.elf: $(OBJ) ../build/user/start.o ../利用者/連結配置.ld
	$(ECHO) "LINK $@"
	$(Q)$(LD) -T ../利用者/連結配置.ld -z max-page-size=4096 --gc-sections -o $@ ../build/user/start.o $(OBJ)
include $(TOP)/py/mkrules.mk
endif
