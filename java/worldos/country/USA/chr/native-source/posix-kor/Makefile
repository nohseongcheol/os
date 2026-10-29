PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ᎦᏟᏌᏅᎯ_0201f362)
구현이름 := ᎠᏍᏆᏂᎪᏙᏗ_I_O 통신종단점 byte_ᎠᏍᏘ ᎬᏗᏍᎩ_ᎥᎧᏁᏉᏍᎬᎢ
ᎪᎱᏍᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
ᎠᏓᎪᎵᏰᏍᎩ_ᏕᎦᏅᏅᏛ := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ᎦᏟᏌᏅᎯ_0201f362/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(ᎠᏓᎪᎵᏰᏍᎩ_ᏕᎦᏅᏅᏛ)
build/변환완료: $(원문목록) 도구/식별자변환.py
	mkdir -p build
	$(PYTHON) 도구/식별자변환.py ᎦᏟᏌᏅᎯ_0201f362 build/ᎦᏟᏌᏅᎯ_0201f362
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ᎦᏟᏌᏅᎯ_0201f362/구현/$*.c -o $@
build/운영체제호출.o: 기계/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ.o: 기계/ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ᎪᎱᏍᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ.o build/libposix-kor.a ../compiler/ᎬᏗᏍᎩ_ᎫᏓᎸᎢ_ᏱᎬᏂ.ld
	$(CC) $(CFLAGS) -c build/ᎦᏟᏌᏅᎯ_0201f362/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ᎬᏗᏍᎩ_ᎫᏓᎸᎢ_ᏱᎬᏂ.ld -o $@ build/ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) 도구/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
