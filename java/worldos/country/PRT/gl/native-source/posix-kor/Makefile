PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files FONTE)
구현이름 := Ficheiro_E_S 통신종단점 byte_cadea usuario_introducir
obxecto_Ficheiro_Lista := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/sistema_operativo_Chamadas.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/FONTE/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Ferramentas/식별자변환.py
	mkdir -p build
	$(PYTHON) Ferramentas/식별자변환.py FONTE build/FONTE
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/FONTE/구현/$*.c -o $@
build/sistema_operativo_Chamadas.o: máquina/sistema_operativo_Chamadas.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_usuario_apl.o: máquina/START_usuario_apl.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(obxecto_Ficheiro_Lista)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_usuario_apl.o build/libposix-kor.a ../compiler/usuario_Ligar_deseño.ld
	$(CC) $(CFLAGS) -c build/FONTE/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/usuario_Ligar_deseño.ld -o $@ build/START_usuario_apl.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Ferramentas/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
