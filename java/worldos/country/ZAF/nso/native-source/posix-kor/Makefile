PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files mohlodi)
구현이름 := faele_I_O 통신종단점 paete_molokoloko mošomiši_tsenya
selo_faele_Lenaneo := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/mohlodi/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Ditholosi/sešupi_Phetošetšo.py
	mkdir -p build
	$(PYTHON) Ditholosi/sešupi_Phetošetšo.py mohlodi build/mohlodi
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/mohlodi/구현/$*.c -o $@
build/운영체제호출.o: motšhene/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Thomišo_mošomiši_tirišo.o: motšhene/Thomišo_mošomiši_tirišo.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(selo_faele_Lenaneo)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Thomišo_mošomiši_tirišo.o build/libposix-kor.a ../compiler/mošomiši_linke_Sebopego.ld
	$(CC) $(CFLAGS) -c build/mohlodi/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/mošomiši_linke_Sebopego.ld -o $@ build/Thomišo_mošomiši_tirišo.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Ditholosi/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
