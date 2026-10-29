PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ŠALTINIS)
구현이름 := Failas_Į_I 통신종단점 baitas_eilutė naudotojas_įvesti
objektas_Failas_Sąrašas := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operacinė_sistema_Skambučiai.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ŠALTINIS/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Įrankiai/identifikatorius_konvertavimas.py
	mkdir -p build
	$(PYTHON) Įrankiai/identifikatorius_konvertavimas.py ŠALTINIS build/ŠALTINIS
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ŠALTINIS/구현/$*.c -o $@
build/operacinė_sistema_Skambučiai.o: mašina/operacinė_sistema_Skambučiai.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_naudotojas_programa.o: mašina/Start_naudotojas_programa.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objektas_Failas_Sąrašas)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_naudotojas_programa.o build/libposix-kor.a ../compiler/naudotojas_sieti_schema.ld
	$(CC) $(CFLAGS) -c build/ŠALTINIS/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/naudotojas_sieti_schema.ld -o $@ build/Start_naudotojas_programa.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Įrankiai/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
