PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files chanzo)
구현이름 := faili_I_T 통신종단점 baiti_tungo mtumiaji_ingiza
kipengee_faili_Orodha := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/chanzo/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Zana/kitambulishi_ubadilishaji.py
	mkdir -p build
	$(PYTHON) Zana/kitambulishi_ubadilishaji.py chanzo build/chanzo
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/chanzo/구현/$*.c -o $@
build/운영체제호출.o: mashine/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Anza_mtumiaji_programu.o: mashine/Anza_mtumiaji_programu.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(kipengee_faili_Orodha)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Anza_mtumiaji_programu.o build/libposix-kor.a ../compiler/mtumiaji_Kiungo_Muundo.ld
	$(CC) $(CFLAGS) -c build/chanzo/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/mtumiaji_Kiungo_Muundo.ld -o $@ build/Anza_mtumiaji_programu.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Zana/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
