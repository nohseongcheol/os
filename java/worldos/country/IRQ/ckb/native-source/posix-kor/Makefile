PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ژێدەر)
구현이름 := فایل_I_O 통신종단점 بایت_رست بەکارهێنەر_تێنووسین
شت_فایل_لیست := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ژێدەر/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ئامرازەکان/ناسێنەر_گۆڕین.py
	mkdir -p build
	$(PYTHON) ئامرازەکان/ناسێنەر_گۆڕین.py ژێدەر build/ژێدەر
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ژێدەر/구현/$*.c -o $@
build/운영체제호출.o: مەکینه/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/دەستپێك_بەکارهێنەر_بەرنامە.o: مەکینه/دەستپێك_بەکارهێنەر_بەرنامە.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(شت_فایل_لیست)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/دەستپێك_بەکارهێنەر_بەرنامە.o build/libposix-kor.a ../compiler/بەکارهێنەر_لینك_ڕیزبەست.ld
	$(CC) $(CFLAGS) -c build/ژێدەر/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/بەکارهێنەر_لینك_ڕیزبەست.ld -o $@ build/دەستپێك_بەکارهێنەر_بەرنامە.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ئامرازەکان/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
