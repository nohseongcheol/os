PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files Неден)
구현이름 := файл_енгізу_шығару 통신종단점 байт_жол пайдаланушы_енгізу
нысан_файл_Тізім := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/операциялық_жүйе_Қоңыраулар.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Неден/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Құралдар/идентификатор_түрлендіру.py
	mkdir -p build
	$(PYTHON) Құралдар/идентификатор_түрлендіру.py Неден build/Неден
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/Неден/구현/$*.c -o $@
build/операциялық_жүйе_Қоңыраулар.o: компьютер/операциялық_жүйе_Қоңыраулар.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/басы_пайдаланушы_бағдарлама.o: компьютер/басы_пайдаланушы_бағдарлама.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(нысан_файл_Тізім)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/басы_пайдаланушы_бағдарлама.o build/libposix-kor.a ../compiler/пайдаланушы_Cілтеме_макет.ld
	$(CC) $(CFLAGS) -c build/Неден/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/пайдаланушы_Cілтеме_макет.ld -o $@ build/басы_пайдаланушы_бағдарлама.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Құралдар/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
