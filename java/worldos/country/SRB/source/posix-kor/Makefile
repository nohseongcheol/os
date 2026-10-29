PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ИЗВОР)
구현이름 := фајл_У_И 통신종단점 бајт_ниска корисник_унети
објекат_фајл_Листа := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/оперативни_систем_Позиви.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ИЗВОР/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Алатке/идентификатор_конверзија.py
	mkdir -p build
	$(PYTHON) Алатке/идентификатор_конверзија.py ИЗВОР build/ИЗВОР
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ИЗВОР/구현/$*.c -o $@
build/оперативни_систем_Позиви.o: рачунар/оперативни_систем_Позиви.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Старт_корисник_програм.o: рачунар/Старт_корисник_програм.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(објекат_фајл_Листа)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Старт_корисник_програм.o build/libposix-kor.a ../compiler/корисник_Веза_изглед.ld
	$(CC) $(CFLAGS) -c build/ИЗВОР/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/корисник_Веза_изглед.ld -o $@ build/Старт_корисник_програм.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Алатке/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
