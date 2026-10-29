PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files Булак)
구현이름 := файл_киргизүү_чыгаруу 통신종단점 байт_сап колдонуучу_кирүү
объект_файл_Тизме := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Булак/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Куралдар/аныктагыч_конверсия.py
	mkdir -p build
	$(PYTHON) Куралдар/аныктагыч_конверсия.py Булак build/Булак
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/Булак/구현/$*.c -o $@
build/운영체제호출.o: машина/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Баштоо_колдонуучу_програм.o: машина/Баштоо_колдонуучу_програм.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(объект_файл_Тизме)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Баштоо_колдонуучу_програм.o build/libposix-kor.a ../compiler/колдонуучу_Шилтеме_түзүлүш.ld
	$(CC) $(CFLAGS) -c build/Булак/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/колдонуучу_Шилтеме_түзүлүш.ld -o $@ build/Баштоо_колдонуучу_програм.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Куралдар/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
