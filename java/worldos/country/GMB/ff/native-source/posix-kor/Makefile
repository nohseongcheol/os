PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files sewnde)
구현이름 := fiilde_I_O 통신종단점 oktee_ɓoggol kuutoro_naatnude
huunde_fiilde_Doggol := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/sewnde/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) 도구/식별자변환.py
	mkdir -p build
	$(PYTHON) 도구/식별자변환.py sewnde build/sewnde
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/sewnde/구현/$*.c -o $@
build/운영체제호출.o: 기계/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/huɓɓude_kuutoro_tafirde.o: 기계/huɓɓude_kuutoro_tafirde.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(huunde_fiilde_Doggol)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/huɓɓude_kuutoro_tafirde.o build/libposix-kor.a ../compiler/kuutoro_jokkere_lelngo.ld
	$(CC) $(CFLAGS) -c build/sewnde/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/kuutoro_jokkere_lelngo.ld -o $@ build/huɓɓude_kuutoro_tafirde.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) 도구/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
