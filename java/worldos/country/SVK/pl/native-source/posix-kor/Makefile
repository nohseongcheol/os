PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files plik_źródłowy)
구현이름 := Plik_We_Wy gniazdo_uczestnik bajt_ciąg użytkownik_wprowadzić
plik_obiektu_Lista := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/system_operacyjny_Połączenia.o
시험이름 := Plik_ABI_test datagram_test STDIN_test 파일보존시험
lista_testów := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/plik_źródłowy/deklaracje
.PHONY: all test test-tools
all: build/libposix-kor.a $(lista_testów)
build/변환완료: $(원문목록) narzędzia/identyfikator_konwersja.py
	mkdir -p build
	$(PYTHON) narzędzia/identyfikator_konwersja.py plik_źródłowy build/plik_źródłowy
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/plik_źródłowy/implementacja/$*.c -o $@
build/system_operacyjny_Połączenia.o: maszyna/system_operacyjny_Połączenia.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_użytkownik_program.o: maszyna/START_użytkownik_program.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(plik_obiektu_Lista)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_użytkownik_program.o build/libposix-kor.a ../compiler/użytkownik_Link_Układ.ld
	$(CC) $(CFLAGS) -c build/plik_źródłowy/testy/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/użytkownik_Link_Układ.ld -o $@ build/START_użytkownik_program.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) narzędzia/konwersja_test.py

.PHONY: clean
clean:
	rm -rf -- build
