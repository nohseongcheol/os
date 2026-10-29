PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files উৎস_নথি)
구현이름 := ফাইল_ইনপুট_আউটপুট 통신종단점 বাইট_স্ট্রিং ব্যবহারকারী_প্রবেশ_করা
বস্তু_ফাইল_তালিকা := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/অপারেটিং_সিস্টেম_কলগুলি.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/উৎস_নথি/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) সরঞ্জামগুলি/식별자변환.py
	mkdir -p build
	$(PYTHON) সরঞ্জামগুলি/식별자변환.py উৎস_নথি build/উৎস_নথি
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/উৎস_নথি/구현/$*.c -o $@
build/অপারেটিং_সিস্টেম_কলগুলি.o: মেশিন/অপারেটিং_সিস্টেম_কলগুলি.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/শুরু_ব্যবহারকারী_অ্যাপ.o: মেশিন/শুরু_ব্যবহারকারী_অ্যাপ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(বস্তু_ফাইল_তালিকা)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/শুরু_ব্যবহারকারী_অ্যাপ.o build/libposix-kor.a ../compiler/ব্যবহারকারী_লিংক_লেআউট.ld
	$(CC) $(CFLAGS) -c build/উৎস_নথি/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ব্যবহারকারী_লিংক_লেআউট.ld -o $@ build/শুরু_ব্যবহারকারী_অ্যাপ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) সরঞ্জামগুলি/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
