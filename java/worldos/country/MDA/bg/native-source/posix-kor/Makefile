PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ИЗТОЧНИК)
구현이름 := Файл_В_И 통신종단점 байт_низ потребител_въвеждам
обект_Файл_Списък := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/операционна_система_Обаждания.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ИЗТОЧНИК/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Инструменти/Идентификатор_замяна.py
	mkdir -p build
	$(PYTHON) Инструменти/Идентификатор_замяна.py ИЗТОЧНИК build/ИЗТОЧНИК
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ИЗТОЧНИК/구현/$*.c -o $@
build/операционна_система_Обаждания.o: машина/операционна_система_Обаждания.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Старт_потребител_програма.o: машина/Старт_потребител_програма.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(обект_Файл_Списък)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Старт_потребител_програма.o build/libposix-kor.a ../compiler/потребител_Връзка_схема.ld
	$(CC) $(CFLAGS) -c build/ИЗТОЧНИК/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/потребител_Връзка_схема.ld -o $@ build/Старт_потребител_програма.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Инструменти/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
