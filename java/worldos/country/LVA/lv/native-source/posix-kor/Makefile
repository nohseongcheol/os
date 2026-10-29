PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files AVOTS)
구현이름 := Fails_ievadizvade 통신종단점 byte_virkne lietotājs_ievadīt
objekts_Fails_Saraksts := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operētājsistēma_Zvani.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/AVOTS/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Rīki/identifikators_pārvēršana.py
	mkdir -p build
	$(PYTHON) Rīki/identifikators_pārvēršana.py AVOTS build/AVOTS
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/AVOTS/구현/$*.c -o $@
build/operētājsistēma_Zvani.o: mašīna/operētājsistēma_Zvani.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Sākt_lietotājs_programma.o: mašīna/Sākt_lietotājs_programma.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekts_Fails_Saraksts)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Sākt_lietotājs_programma.o build/libposix-kor.a ../compiler/lietotājs_Saite_shēma.ld
	$(CC) $(CFLAGS) -c build/AVOTS/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/lietotājs_Saite_shēma.ld -o $@ build/Sākt_lietotājs_programma.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Rīki/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
