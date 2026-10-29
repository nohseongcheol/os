PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files КРЫНІЦА)
구현이름 := файл_увод_вывад 통신종단점 байт_радок карыстальнік_увесці
аб_ект_файл_Спіс := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/КРЫНІЦА/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Інструменты/ідэнтыфікатар_замена.py
	mkdir -p build
	$(PYTHON) Інструменты/ідэнтыфікатар_замена.py КРЫНІЦА build/КРЫНІЦА
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/КРЫНІЦА/구현/$*.c -o $@
build/운영체제호출.o: камп_ютар/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Пуск_карыстальнік_праграма.o: камп_ютар/Пуск_карыстальнік_праграма.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(аб_ект_файл_Спіс)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Пуск_карыстальнік_праграма.o build/libposix-kor.a ../compiler/карыстальнік_сувязь_Макет.ld
	$(CC) $(CFLAGS) -c build/КРЫНІЦА/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/карыстальнік_сувязь_Макет.ld -o $@ build/Пуск_карыстальнік_праграма.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Інструменты/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
