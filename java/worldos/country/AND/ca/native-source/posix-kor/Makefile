PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files FONT)
구현이름 := arxiu_E_S 통신종단점 byte_cadena usuari_introduir
objecte_arxiu_Llista := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/sistema_operatiu_Trucades.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/FONT/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Eines/identificador_conversió.py
	mkdir -p build
	$(PYTHON) Eines/identificador_conversió.py FONT build/FONT
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/FONT/구현/$*.c -o $@
build/sistema_operatiu_Trucades.o: màquina/sistema_operatiu_Trucades.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Inici_usuari_programa.o: màquina/Inici_usuari_programa.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objecte_arxiu_Llista)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Inici_usuari_programa.o build/libposix-kor.a ../compiler/usuari_enllaç_disseny.ld
	$(CC) $(CFLAGS) -c build/FONT/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/usuari_enllaç_disseny.ld -o $@ build/Inici_usuari_programa.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Eines/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
