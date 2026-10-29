PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files উৎস)
구현이름 := ফাইল_ইনপুট_আউটপুট 통신종단점 বাইট_ষ্ট্ৰিং ব্যৱহাৰকৰ্তা_প্ৰৱেশ_কৰক
অবজেক্ট_ফাইল_সূচী := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/অপাৰেটিং_ছিষ্টেম_কলসমূহ.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/উৎস/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) সঁজুলিসমূহ/চিনাক্তকাৰী_ৰূপান্তৰকৰণ.py
	mkdir -p build
	$(PYTHON) সঁজুলিসমূহ/চিনাক্তকাৰী_ৰূপান্তৰকৰণ.py উৎস build/উৎস
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/উৎস/구현/$*.c -o $@
build/অপাৰেটিং_ছিষ্টেম_কলসমূহ.o: মেচিন/অপাৰেটিং_ছিষ্টেম_কলসমূহ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/আৰম্ভ_ব্যৱহাৰকৰ্তা_এপ্প্.o: মেচিন/আৰম্ভ_ব্যৱহাৰকৰ্তা_এপ্প্.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(অবজেক্ট_ফাইল_সূচী)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/আৰম্ভ_ব্যৱহাৰকৰ্তা_এপ্প্.o build/libposix-kor.a ../compiler/ব্যৱহাৰকৰ্তা_লিংক_লেআউট.ld
	$(CC) $(CFLAGS) -c build/উৎস/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ব্যৱহাৰকৰ্তা_লিংক_লেআউট.ld -o $@ build/আৰম্ভ_ব্যৱহাৰকৰ্তা_এপ্প্.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) সঁজুলিসমূহ/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
