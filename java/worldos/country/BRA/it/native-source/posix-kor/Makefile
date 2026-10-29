PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files codiceSorgente)
구현이름 := File_I_O socket_endpoint byte_stringa USER_immettere
file_oggetto_elenco := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/sistema_operativo_Chiamate.o
시험이름 := File_ABI_test datagramma_test STDIN_test 파일보존시험
elenco_dei_test := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/codiceSorgente/dichiarazioni
.PHONY: all test test-tools
all: build/libposix-kor.a $(elenco_dei_test)
build/변환완료: $(원문목록) strumenti/identificatore_conversione.py
	mkdir -p build
	$(PYTHON) strumenti/identificatore_conversione.py codiceSorgente build/codiceSorgente
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/codiceSorgente/implementazione/$*.c -o $@
build/sistema_operativo_Chiamate.o: computer/sistema_operativo_Chiamate.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_USER_app.o: computer/START_USER_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(file_oggetto_elenco)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_USER_app.o build/libposix-kor.a ../compiler/USER_link_Layout.ld
	$(CC) $(CFLAGS) -c build/codiceSorgente/prove/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/USER_link_Layout.ld -o $@ build/START_USER_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) strumenti/conversione_test.py

.PHONY: clean
clean:
	rm -rf -- build
