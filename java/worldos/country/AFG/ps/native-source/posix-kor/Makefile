PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files سرچينه)
구현이름 := دوتنه_ننوتنی_وتنی 통신종단점 بايټ_مزى 사용자진입
목적목록 := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/سرچينه/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) 도구/식별자변환.py
	mkdir -p build
	$(PYTHON) 도구/식별자변환.py سرچينه build/سرچينه
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/سرچينه/구현/$*.c -o $@
build/운영체제호출.o: 기계/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/پيل_کارن_کاريال.o: 기계/پيل_کارن_کاريال.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(목적목록)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/پيل_کارن_کاريال.o build/libposix-kor.a ../compiler/کارن_پيوند_هډوانه.ld
	$(CC) $(CFLAGS) -c build/سرچينه/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/کارن_پيوند_هډوانه.ld -o $@ build/پيل_کارن_کاريال.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) 도구/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
