PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files წყარო)
구현이름 := ფაილი_შეტანა_გამოტანა 통신종단점 ბაიტი_სტრიქონი მომხმარებელი_შეყვანა
ობიექტი_ფაილი_სია := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ოპერაციული_სისტემა_ზარები.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/წყარო/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ხელსაწყოები/იდენტიფიკატორი_გარდაქმნა.py
	mkdir -p build
	$(PYTHON) ხელსაწყოები/იდენტიფიკატორი_გარდაქმნა.py წყარო build/წყარო
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/წყარო/구현/$*.c -o $@
build/ოპერაციული_სისტემა_ზარები.o: კომპიუტერი/ოპერაციული_სისტემა_ზარები.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/დაწყება_მომხმარებელი_აპი.o: კომპიუტერი/დაწყება_მომხმარებელი_აპი.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ობიექტი_ფაილი_სია)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/დაწყება_მომხმარებელი_აპი.o build/libposix-kor.a ../compiler/მომხმარებელი_ბმული_განლაგება.ld
	$(CC) $(CFLAGS) -c build/წყარო/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/მომხმარებელი_ბმული_განლაგება.ld -o $@ build/დაწყება_მომხმარებელი_აპი.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ხელსაწყოები/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
