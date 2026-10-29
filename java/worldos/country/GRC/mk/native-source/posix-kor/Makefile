PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ИЗВОР)
구현이름 := датотека_В_И 통신종단점 бајт_низа корисник_внеси
објект_датотека_Список := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/оперативен_систем_Повици.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ИЗВОР/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Алатки/идентификатор_конверзија.py
	mkdir -p build
	$(PYTHON) Алатки/идентификатор_конверзија.py ИЗВОР build/ИЗВОР
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ИЗВОР/구현/$*.c -o $@
build/оперативен_систем_Повици.o: машина/оперативен_систем_Повици.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_корисник_програма.o: машина/Start_корисник_програма.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(објект_датотека_Список)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_корисник_програма.o build/libposix-kor.a ../compiler/корисник_Врска_Распоред.ld
	$(CC) $(CFLAGS) -c build/ИЗВОР/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/корисник_Врска_Распоред.ld -o $@ build/Start_корисник_програма.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Алатки/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
