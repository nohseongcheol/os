PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files lähdetiedosto)
구현이름 := Tiedosto_I_O vastake_päätepiste tavu_merkkijono käyttäjä_anna
objekti_tiedostoluettelo := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/käyttöjärjestelmä_Puhelut.o
시험이름 := 파일규약시험 datagrammi_testi STDIN_testi 파일보존시험
testi_luettelo := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/lähdetiedosto/esittelyt
.PHONY: all test test-tools
all: build/libposix-kor.a $(testi_luettelo)
build/변환완료: $(원문목록) työkalut/tunniste_muunnos.py
	mkdir -p build
	$(PYTHON) työkalut/tunniste_muunnos.py lähdetiedosto build/lähdetiedosto
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/lähdetiedosto/toteutus/$*.c -o $@
build/käyttöjärjestelmä_Puhelut.o: kone/käyttöjärjestelmä_Puhelut.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/alku_käyttäjä_ohjelma.o: kone/alku_käyttäjä_ohjelma.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekti_tiedostoluettelo)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/alku_käyttäjä_ohjelma.o build/libposix-kor.a ../compiler/käyttäjä_Linkki_Asettelu.ld
	$(CC) $(CFLAGS) -c build/lähdetiedosto/testit/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/käyttäjä_Linkki_Asettelu.ld -o $@ build/alku_käyttäjä_ohjelma.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) työkalut/muunnos_testi.py

.PHONY: clean
clean:
	rm -rf -- build
