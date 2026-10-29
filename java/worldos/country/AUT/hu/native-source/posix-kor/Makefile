PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files FORRÁS)
구현이름 := Fájl_I_O szoftvercsatorna_végpont bájt_sztring felhasználó_megad
objektum_fájllista := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operációs_rendszer_Hívások.o
시험이름 := 파일규약시험 datagram_teszt STDIN_teszt 파일보존시험
teszt_Lista := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/FORRÁS/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(teszt_Lista)
build/변환완료: $(원문목록) Eszközök/azonosító_átalakítás.py
	mkdir -p build
	$(PYTHON) Eszközök/azonosító_átalakítás.py FORRÁS build/FORRÁS
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/FORRÁS/구현/$*.c -o $@
build/operációs_rendszer_Hívások.o: gép/operációs_rendszer_Hívások.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_felhasználó_app.o: gép/START_felhasználó_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objektum_fájllista)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_felhasználó_app.o build/libposix-kor.a ../compiler/felhasználó_csatol_Navigáció.ld
	$(CC) $(CFLAGS) -c build/FORRÁS/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/felhasználó_csatol_Navigáció.ld -o $@ build/START_felhasználó_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Eszközök/átalakítás_teszt.py

.PHONY: clean
clean:
	rm -rf -- build
