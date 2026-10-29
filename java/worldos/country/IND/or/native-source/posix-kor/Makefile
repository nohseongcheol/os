PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ଉତ୍ସ)
구현이름 := ଫାଇଲ୍_ଇନପୁଟ୍_ଆଉଟପୁଟ୍ 통신종단점 ବାଇଟ୍_ଷ୍ଟ୍ରିଂ ଉପଭୋକ୍ତା_ଏଣ୍ଟର୍_କରନ୍ତୁ
ଅବଜେକ୍ଟ_ଫାଇଲ୍_ତାଲିକା := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ଅପରେଟିଂ_ସିଷ୍ଟମ_କଲ୍ସ.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ଉତ୍ସ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ଉପକରଣସମୂହ/ପରିଚାୟକ_ପରିବର୍ତ୍ତନ.py
	mkdir -p build
	$(PYTHON) ଉପକରଣସମୂହ/ପରିଚାୟକ_ପରିବର୍ତ୍ତନ.py ଉତ୍ସ build/ଉତ୍ସ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ଉତ୍ସ/구현/$*.c -o $@
build/ଅପରେଟିଂ_ସିଷ୍ଟମ_କଲ୍ସ.o: ମେସିନ୍/ଅପରେଟିଂ_ସିଷ୍ଟମ_କଲ୍ସ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ଆରମ୍ଭ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ.o: ମେସିନ୍/ଆରମ୍ଭ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ଅବଜେକ୍ଟ_ଫାଇଲ୍_ତାଲିକା)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ଆରମ୍ଭ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ.o build/libposix-kor.a ../compiler/ଉପଭୋକ୍ତା_ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld
	$(CC) $(CFLAGS) -c build/ଉତ୍ସ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ଉପଭୋକ୍ତା_ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld -o $@ build/ଆରମ୍ଭ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ଉପକରଣସମୂହ/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
