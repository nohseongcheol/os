PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files KILDE)
구현이름 := Fil_I_U socket_deltaker byte_streng bruker_angi
objekt_filliste := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operativsystem_Anrop.o
시험이름 := 파일규약시험 datagram_test STDIN_test 파일보존시험
test_Liste := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/KILDE/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(test_Liste)
build/변환완료: $(원문목록) Verktøy/identifikator_konvertering.py
	mkdir -p build
	$(PYTHON) Verktøy/identifikator_konvertering.py KILDE build/KILDE
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/KILDE/구현/$*.c -o $@
build/operativsystem_Anrop.o: maskin/operativsystem_Anrop.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_bruker_app.o: maskin/START_bruker_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekt_filliste)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_bruker_app.o build/libposix-kor.a ../compiler/bruker_koble_Oppsett.ld
	$(CC) $(CFLAGS) -c build/KILDE/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/bruker_koble_Oppsett.ld -o $@ build/START_bruker_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Verktøy/konvertering_test.py

.PHONY: clean
clean:
	rm -rf -- build
