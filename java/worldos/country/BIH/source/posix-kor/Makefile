PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files извор)
구현이름 := фајл_У_И 통신종단점 бајт_стринг корисник_унијети
објект_фајл_списак := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/извор/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) 도구/식별자변환.py
	mkdir -p build
	$(PYTHON) 도구/식별자변환.py извор build/извор
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/извор/구현/$*.c -o $@
build/운영체제호출.o: 기계/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/почети_корисник_програм.o: 기계/почети_корисник_програм.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(објект_фајл_списак)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/почети_корисник_програм.o build/libposix-kor.a ../compiler/корисник_веза_изглед.ld
	$(CC) $(CFLAGS) -c build/извор/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/корисник_веза_изглед.ld -o $@ build/почети_корисник_програм.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) 도구/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
