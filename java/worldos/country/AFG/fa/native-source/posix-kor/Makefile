PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files مبداء)
구현이름 := فایل_ورودی_خروجی 통신종단점 بایت_رشته کاربر_وارد_کردن
شئ_فایل_لیست := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/سیستم_عامل_تماس_ها.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/مبداء/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ابزارها/شناسه_جایگزینی.py
	mkdir -p build
	$(PYTHON) ابزارها/شناسه_جایگزینی.py مبداء build/مبداء
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/مبداء/구현/$*.c -o $@
build/سیستم_عامل_تماس_ها.o: دستگاه/سیستم_عامل_تماس_ها.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/شروع_کاربر_برنامه.o: دستگاه/شروع_کاربر_برنامه.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(شئ_فایل_لیست)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/شروع_کاربر_برنامه.o build/libposix-kor.a ../compiler/کاربر_پیوند_پیمایش.ld
	$(CC) $(CFLAGS) -c build/مبداء/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/کاربر_پیوند_پیمایش.ld -o $@ build/شروع_کاربر_برنامه.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ابزارها/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
