PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files BURIMI)
구현이름 := skedar_I_O 통신종단점 bajt_varg përdorues_fut
objekt_skedar_Listë := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/sistem_operativ_Thirrjet.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/BURIMI/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Mjete/identifikues_konvertim.py
	mkdir -p build
	$(PYTHON) Mjete/identifikues_konvertim.py BURIMI build/BURIMI
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/BURIMI/구현/$*.c -o $@
build/sistem_operativ_Thirrjet.o: makinë/sistem_operativ_Thirrjet.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/nis_përdorues_program.o: makinë/nis_përdorues_program.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekt_skedar_Listë)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/nis_përdorues_program.o build/libposix-kor.a ../compiler/përdorues_lidh_Navigimi.ld
	$(CC) $(CFLAGS) -c build/BURIMI/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/përdorues_lidh_Navigimi.ld -o $@ build/nis_përdorues_program.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Mjete/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
