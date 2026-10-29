PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files Quell)
구현이름 := Fichier_I_O 통신종단점 Byte_Zeechefolleg Benotzer_aginn
Objet_Fichier_Lëscht := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/Betribssystem_Uriff.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Quell/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Tools/Identifikateur_Wiessel.py
	mkdir -p build
	$(PYTHON) Tools/Identifikateur_Wiessel.py Quell build/Quell
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/Quell/구현/$*.c -o $@
build/Betribssystem_Uriff.o: Computer/Betribssystem_Uriff.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_Benotzer_App.o: Computer/Start_Benotzer_App.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(Objet_Fichier_Lëscht)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_Benotzer_App.o build/libposix-kor.a ../compiler/Benotzer_Link_Layout.ld
	$(CC) $(CFLAGS) -c build/Quell/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/Benotzer_Link_Layout.ld -o $@ build/Start_Benotzer_App.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Tools/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
