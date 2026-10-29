PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ZDROJ)
구현이름 := Súbor_vstup_a_výstup soket_účastník Byte_reťazec používateľ_zadať
objekt_Súbor_Zoznam := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operačný_systém_Hovory.o
시험이름 := 파일규약시험 datagram_test STDIN_test 파일보존시험
test_Zoznam := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ZDROJ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(test_Zoznam)
build/변환완료: $(원문목록) Nástroje/identifikátor_konverzia.py
	mkdir -p build
	$(PYTHON) Nástroje/identifikátor_konverzia.py ZDROJ build/ZDROJ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ZDROJ/구현/$*.c -o $@
build/operačný_systém_Hovory.o: počítač_5eb260fa/operačný_systém_Hovory.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_používateľ_program.o: počítač_5eb260fa/START_používateľ_program.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekt_Súbor_Zoznam)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_používateľ_program.o build/libposix-kor.a ../compiler/používateľ_odkaz_Navigácia.ld
	$(CC) $(CFLAGS) -c build/ZDROJ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/používateľ_odkaz_Navigácia.ld -o $@ build/START_používateľ_program.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Nástroje/konverzia_test.py

.PHONY: clean
clean:
	rm -rf -- build
