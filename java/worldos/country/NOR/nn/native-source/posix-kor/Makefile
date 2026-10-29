PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files KJELDE)
구현이름 := fil_I_U 통신종단점 byte_streng brukar_skrive_inn
objekt_fil_Liste := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operativsystem_Samtalar.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/KJELDE/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Verktøy/identifikator_konvertering.py
	mkdir -p build
	$(PYTHON) Verktøy/identifikator_konvertering.py KJELDE build/KJELDE
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/KJELDE/구현/$*.c -o $@
build/operativsystem_Samtalar.o: maskin/operativsystem_Samtalar.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_brukar_app.o: maskin/START_brukar_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekt_fil_Liste)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_brukar_app.o build/libposix-kor.a ../compiler/brukar_kople_Oppsett.ld
	$(CC) $(CFLAGS) -c build/KJELDE/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/brukar_kople_Oppsett.ld -o $@ build/START_brukar_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Verktøy/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
