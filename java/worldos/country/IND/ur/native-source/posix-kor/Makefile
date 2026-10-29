PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ماخذ_فائل)
구현이름 := فائل_ان_پٹ_آؤٹ_پٹ 통신종단점 بائٹ_سلک صارف_داخل_کریں
آبجیکٹ_فائل_فہرست := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/آپریٹنگ_سسٹم_کالز.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ماخذ_فائل/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ٹولز/شناخت_کنندہ_تبدیلی.py
	mkdir -p build
	$(PYTHON) ٹولز/شناخت_کنندہ_تبدیلی.py ماخذ_فائل build/ماخذ_فائل
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ماخذ_فائل/구현/$*.c -o $@
build/آپریٹنگ_سسٹم_کالز.o: مشین/آپریٹنگ_سسٹم_کالز.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ابتدا_صارف_ایپ.o: مشین/ابتدا_صارف_ایپ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(آبجیکٹ_فائل_فہرست)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ابتدا_صارف_ایپ.o build/libposix-kor.a ../compiler/صارف_ربط_ترتیب.ld
	$(CC) $(CFLAGS) -c build/ماخذ_فائل/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/صارف_ربط_ترتیب.ld -o $@ build/ابتدا_صارف_ایپ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ٹولز/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
