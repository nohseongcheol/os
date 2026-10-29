PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files izvor)
구현이름 := Datoteka_U_I 통신종단점 bajt_niska korisnik_uneti
objekat_Datoteka_Lista := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operativni_sistem_Pozivi.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/izvor/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Alatke/identifikator_konverzija.py
	mkdir -p build
	$(PYTHON) Alatke/identifikator_konverzija.py izvor build/izvor
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/izvor/구현/$*.c -o $@
build/operativni_sistem_Pozivi.o: računar/operativni_sistem_Pozivi.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_korisnik_program.o: računar/START_korisnik_program.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekat_Datoteka_Lista)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_korisnik_program.o build/libposix-kor.a ../compiler/korisnik_Veza_Raspored.ld
	$(CC) $(CFLAGS) -c build/izvor/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/korisnik_Veza_Raspored.ld -o $@ build/START_korisnik_program.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Alatke/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
