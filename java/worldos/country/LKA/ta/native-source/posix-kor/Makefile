PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files மூலக்_கோப்பு)
구현이름 := கோப்பு_உள்ளீடு_வெளியீடு 통신종단점 பைட்_சரம் பயனர்_உள்ளிடு
பொருள்_கோப்பு_பட்டியல் := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/இயக்க_முறைமை_அழைப்புகள்.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
சோதனைப்_பட்டியல் := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/மூலக்_கோப்பு/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(சோதனைப்_பட்டியல்)
build/변환완료: $(원문목록) கருவிகள்/அடையாளங்காட்டி_மாற்றம்.py
	mkdir -p build
	$(PYTHON) கருவிகள்/அடையாளங்காட்டி_மாற்றம்.py மூலக்_கோப்பு build/மூலக்_கோப்பு
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/மூலக்_கோப்பு/구현/$*.c -o $@
build/இயக்க_முறைமை_அழைப்புகள்.o: இயந்திரம்/இயக்க_முறைமை_அழைப்புகள்.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/தொடங்கு_பயனர்_நிரல்.o: இயந்திரம்/தொடங்கு_பயனர்_நிரல்.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(பொருள்_கோப்பு_பட்டியல்)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/தொடங்கு_பயனர்_நிரல்.o build/libposix-kor.a ../compiler/பயனர்_இணை_லேஅவுட்.ld
	$(CC) $(CFLAGS) -c build/மூலக்_கோப்பு/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/பயனர்_இணை_லேஅவுட்.ld -o $@ build/தொடங்கு_பயனர்_நிரல்.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) கருவிகள்/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
