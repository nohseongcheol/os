PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files مەنبە)
구현이름 := 파일입출력 통신종단점 بايت_ھەرپ_تىزمىسى ئىشلەتكۈچى_كىرمەك
ئوبيېكت_ھۆججەت_تىزىم := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/مەشغۇلات_سىستېمىسى_تېلېفون.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/مەنبە/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) قوراللار/پەرقلەندۈرگۈچ_ئالماشتۇرۇش.py
	mkdir -p build
	$(PYTHON) قوراللار/پەرقلەندۈرگۈچ_ئالماشتۇرۇش.py مەنبە build/مەنبە
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/مەنبە/구현/$*.c -o $@
build/مەشغۇلات_سىستېمىسى_تېلېفون.o: ماشىنا/مەشغۇلات_سىستېمىسى_تېلېفون.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/باشلاش_ئىشلەتكۈچى_ئەپ.o: ماشىنا/باشلاش_ئىشلەتكۈچى_ئەپ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ئوبيېكت_ھۆججەت_تىزىم)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/باشلاش_ئىشلەتكۈچى_ئەپ.o build/libposix-kor.a ../compiler/ئىشلەتكۈچى_ئۇلانما_لايىھە.ld
	$(CC) $(CFLAGS) -c build/مەنبە/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ئىشلەتكۈچى_ئۇلانما_لايىھە.ld -o $@ build/باشلاش_ئىشلەتكۈچى_ئەپ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) قوراللار/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
