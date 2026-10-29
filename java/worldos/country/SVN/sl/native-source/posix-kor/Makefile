PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files VIR)
구현이름 := Datoteka_V_I vtičnica_končna_točka bajt_niz uporabnik_vnesti
predmet_Datoteka_Seznam := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operacijski_sistem_Klici.o
시험이름 := 파일규약시험 datagram_preskusiti STDIN_preskusiti 파일보존시험
preskusiti_Seznam := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/VIR/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(preskusiti_Seznam)
build/변환완료: $(원문목록) Orodja/identifikator_sprememba_naročnine.py
	mkdir -p build
	$(PYTHON) Orodja/identifikator_sprememba_naročnine.py VIR build/VIR
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/VIR/구현/$*.c -o $@
build/operacijski_sistem_Klici.o: računalnik/operacijski_sistem_Klici.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_uporabnik_aplikacija.o: računalnik/Start_uporabnik_aplikacija.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(predmet_Datoteka_Seznam)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_uporabnik_aplikacija.o build/libposix-kor.a ../compiler/uporabnik_Povezava_Krmarjenje.ld
	$(CC) $(CFLAGS) -c build/VIR/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/uporabnik_Povezava_Krmarjenje.ld -o $@ build/Start_uporabnik_aplikacija.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Orodja/sprememba_naročnine_preskusiti.py

.PHONY: clean
clean:
	rm -rf -- build
