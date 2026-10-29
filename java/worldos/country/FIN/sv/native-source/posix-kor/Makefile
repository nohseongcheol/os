PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files källfil)
구현이름 := fil_indata_utleverans socket_deltagare byte_sträng användare_ange
objekt_fillista := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operativsystem_Samtal.o
시험이름 := 파일규약시험 datagram_test Standard_indata_test 파일보존시험
test_ange := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/källfil/deklarationer
.PHONY: all test test-tools
all: build/libposix-kor.a $(test_ange)
build/변환완료: $(원문목록) verktyg/identifierare_konvertering.py
	mkdir -p build
	$(PYTHON) verktyg/identifierare_konvertering.py källfil build/källfil
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/källfil/implementation/$*.c -o $@
build/operativsystem_Samtal.o: dator/operativsystem_Samtal.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_användare_app.o: dator/START_användare_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekt_fillista)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_användare_app.o build/libposix-kor.a ../compiler/användare_Länk_Layout.ld
	$(CC) $(CFLAGS) -c build/källfil/tester/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/användare_Länk_Layout.ld -o $@ build/START_användare_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) verktyg/konvertering_test.py

.PHONY: clean
clean:
	rm -rf -- build
