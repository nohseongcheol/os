PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files Çeşme)
구현이름 := faýl_I_O 통신종단점 baýt_setir ulanyjy_giriz
obýekt_faýl_Sanaw := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Çeşme/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Gurallar/tanaýjy_öwürme.py
	mkdir -p build
	$(PYTHON) Gurallar/tanaýjy_öwürme.py Çeşme build/Çeşme
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/Çeşme/구현/$*.c -o $@
build/운영체제호출.o: kompýuter/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/başlat_ulanyjy_programma.o: kompýuter/başlat_ulanyjy_programma.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(obýekt_faýl_Sanaw)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/başlat_ulanyjy_programma.o build/libposix-kor.a ../compiler/ulanyjy_Bag_Ýerleşiş.ld
	$(CC) $(CFLAGS) -c build/Çeşme/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ulanyjy_Bag_Ýerleşiş.ld -o $@ build/başlat_ulanyjy_programma.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Gurallar/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
