PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files códigoFonte)
구현이름 := Arquivo_E_S soquete_empresa byte_cadeia usuário_inserir
arquivo_objeto_Lista := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/SO_Chamadas.o
시험이름 := Arquivo_ABI_teste datagrama_teste STDIN_teste 파일보존시험
lista_de_testes := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/códigoFonte/declarações
.PHONY: all test test-tools
all: build/libposix-kor.a $(lista_de_testes)
build/변환완료: $(원문목록) ferramentas/identificador_conversão.py
	mkdir -p build
	$(PYTHON) ferramentas/identificador_conversão.py códigoFonte build/códigoFonte
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/códigoFonte/implementação/$*.c -o $@
build/SO_Chamadas.o: computador/SO_Chamadas.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_usuário_app.o: computador/START_usuário_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(arquivo_objeto_Lista)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_usuário_app.o build/libposix-kor.a ../compiler/usuário_Link_Layout.ld
	$(CC) $(CFLAGS) -c build/códigoFonte/testes/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/usuário_Link_Layout.ld -o $@ build/START_usuário_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ferramentas/conversão_teste.py

.PHONY: clean
clean:
	rm -rf -- build
