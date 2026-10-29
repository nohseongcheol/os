PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files вихіднийКод)
구현이름 := Файл_ввід_вивід сокет_учасник байт_рядок користувач_вводити
об_єкт_Файл_список := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/операційна_система_ОС_Виклики.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/вихіднийКод/оголошення
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) інструменти/ідентифікатор_перетворення.py
	mkdir -p build
	$(PYTHON) інструменти/ідентифікатор_перетворення.py вихіднийКод build/вихіднийКод
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/вихіднийКод/реалізація/$*.c -o $@
build/операційна_система_ОС_Виклики.o: комп_ютер/операційна_система_ОС_Виклики.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ПУСК_користувач_програма.o: комп_ютер/ПУСК_користувач_програма.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(об_єкт_Файл_список)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ПУСК_користувач_програма.o build/libposix-kor.a ../compiler/користувач_зв_язок_Макет.ld
	$(CC) $(CFLAGS) -c build/вихіднийКод/випробування/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/користувач_зв_язок_Макет.ld -o $@ build/ПУСК_користувач_програма.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) інструменти/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
