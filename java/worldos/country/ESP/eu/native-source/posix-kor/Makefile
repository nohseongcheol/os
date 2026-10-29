PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ITURBURUA)
구현이름 := fitxategi_S_I 통신종단점 byte_kate erabiltzaile_sartu
objektu_fitxategi_Zerrenda := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/sistema_eragile_Deiak.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ITURBURUA/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Tresnak/identifikatzaile_bihurketa.py
	mkdir -p build
	$(PYTHON) Tresnak/identifikatzaile_bihurketa.py ITURBURUA build/ITURBURUA
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ITURBURUA/구현/$*.c -o $@
build/sistema_eragile_Deiak.o: gailu/sistema_eragile_Deiak.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/HASI_erabiltzaile_aplik.o: gailu/HASI_erabiltzaile_aplik.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objektu_fitxategi_Zerrenda)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/HASI_erabiltzaile_aplik.o build/libposix-kor.a ../compiler/erabiltzaile_lotu_diseinu.ld
	$(CC) $(CFLAGS) -c build/ITURBURUA/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/erabiltzaile_lotu_diseinu.ld -o $@ build/HASI_erabiltzaile_aplik.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Tresnak/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
