PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ماخذ)
구현이름 := 파일입출력 통신종단점 بائٽ_اسٽرنگ صارف_داخل_ڪريو
عنصر_فائل_فهرست := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ماخذ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) اوزار/سڃاڻپ_ڪندڙ_تبديلي.py
	mkdir -p build
	$(PYTHON) اوزار/سڃاڻپ_ڪندڙ_تبديلي.py ماخذ build/ماخذ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ماخذ/구현/$*.c -o $@
build/운영체제호출.o: مشين/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/شروع_صارف_ائپ.o: مشين/شروع_صارف_ائپ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(عنصر_فائل_فهرست)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/شروع_صارف_ائپ.o build/libposix-kor.a ../compiler/صارف_ڪڙي_لي_آئوٽ.ld
	$(CC) $(CFLAGS) -c build/ماخذ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/صارف_ڪڙي_لي_آئوٽ.ld -o $@ build/شروع_صارف_ائپ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) اوزار/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
