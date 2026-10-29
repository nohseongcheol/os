PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files чыганак)
구현이름 := файл_К_Ч 통신종단점 байт_юл кулланучы_кертү
объект_файл_Исемлек := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/операцион_система_Шалтыратулар.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/чыганак/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Кораллар/күрсәткеч_үзгәртү.py
	mkdir -p build
	$(PYTHON) Кораллар/күрсәткеч_үзгәртү.py чыганак build/чыганак
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/чыганак/구현/$*.c -o $@
build/операцион_система_Шалтыратулар.o: машина/операцион_система_Шалтыратулар.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_кулланучы_кушымта.o: машина/Start_кулланучы_кушымта.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(объект_файл_Исемлек)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_кулланучы_кушымта.o build/libposix-kor.a ../compiler/кулланучы_бәйләү_план.ld
	$(CC) $(CFLAGS) -c build/чыганак/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/кулланучы_бәйләү_план.ld -o $@ build/Start_кулланучы_кушымта.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Кораллар/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
