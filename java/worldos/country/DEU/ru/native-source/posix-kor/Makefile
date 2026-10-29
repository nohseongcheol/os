PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files исходныйКод)
구현이름 := файл_входные_данные_выход сокет_участник байт_строка пользователь_ввести
объектный_файл_Список := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/операционная_система_Вызовы.o
시험이름 := файл_ABI_тест датаграмма_тест стандарт_входные_данные_тест 파일보존시험
список_тестов := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/исходныйКод/объявления
.PHONY: all test test-tools
all: build/libposix-kor.a $(список_тестов)
build/변환완료: $(원문목록) инструменты/идентификатор_преобразование.py
	mkdir -p build
	$(PYTHON) инструменты/идентификатор_преобразование.py исходныйКод build/исходныйКод
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/исходныйКод/реализация/$*.c -o $@
build/операционная_система_Вызовы.o: компьютер_5eb260fa/операционная_система_Вызовы.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Пуск_пользователь_программа.o: компьютер_5eb260fa/Пуск_пользователь_программа.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(объектный_файл_Список)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Пуск_пользователь_программа.o build/libposix-kor.a ../compiler/пользователь_канал_Макет.ld
	$(CC) $(CFLAGS) -c build/исходныйКод/испытания/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/пользователь_канал_Макет.ld -o $@ build/Пуск_пользователь_программа.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) инструменты/преобразование_тест.py

.PHONY: clean
clean:
	rm -rf -- build
