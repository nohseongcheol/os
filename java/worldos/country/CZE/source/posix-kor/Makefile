PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files zdrojový_soubor)
구현이름 := Soubor_vstup_a_výstup soket_účastník bajt_řetězec uživatel_zadat
objekt_seznam_souborů := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operační_systém_Hovory.o
시험이름 := Soubor_ABI_test datagram_test zařízení_STDIN_test 파일보존시험
seznam_testů := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/zdrojový_soubor/deklarace
.PHONY: all test test-tools
all: build/libposix-kor.a $(seznam_testů)
build/변환완료: $(원문목록) nástroje/identifikátor_převod.py
	mkdir -p build
	$(PYTHON) nástroje/identifikátor_převod.py zdrojový_soubor build/zdrojový_soubor
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/zdrojový_soubor/implementace/$*.c -o $@
build/operační_systém_Hovory.o: počítač/operační_systém_Hovory.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_uživatel_program.o: počítač/START_uživatel_program.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekt_seznam_souborů)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_uživatel_program.o build/libposix-kor.a ../compiler/uživatel_Odkaz_Navigace.ld
	$(CC) $(CFLAGS) -c build/zdrojový_soubor/zkoušky/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/uživatel_Odkaz_Navigace.ld -o $@ build/START_uživatel_program.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) nástroje/převod_test.py

.PHONY: clean
clean:
	rm -rf -- build
