PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files SURSĂ)
구현이름 := Fișier_I_O 통신종단점 byte_șir utilizator_introduce
obiect_Fișier_Listă := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/sistem_de_operare_Apeluri.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/SURSĂ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Instrumente/identificator_conversie.py
	mkdir -p build
	$(PYTHON) Instrumente/identificator_conversie.py SURSĂ build/SURSĂ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/SURSĂ/구현/$*.c -o $@
build/sistem_de_operare_Apeluri.o: mașină/sistem_de_operare_Apeluri.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/buta_utilizator_program.o: mașină/buta_utilizator_program.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(obiect_Fișier_Listă)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/buta_utilizator_program.o build/libposix-kor.a ../compiler/utilizator_Link_Aspect.ld
	$(CC) $(CFLAGS) -c build/SURSĂ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/utilizator_Link_Aspect.ld -o $@ build/buta_utilizator_program.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Instrumente/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
