PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files Cosaan)
구현이름 := bara_denc_D_G 통신종단점 okte_araf_yu_bennoo kiy_jariñoo_internet_dugal
yëf_bara_denc_lim := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Cosaan/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Jumtukaay_yi/raññeekaay_tuubal.py
	mkdir -p build
	$(PYTHON) Jumtukaay_yi/raññeekaay_tuubal.py Cosaan build/Cosaan
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/Cosaan/구현/$*.c -o $@
build/운영체제호출.o: masin/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Door_kiy_jariñoo_internet_jëfekaay.o: masin/Door_kiy_jariñoo_internet_jëfekaay.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(yëf_bara_denc_lim)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Door_kiy_jariñoo_internet_jëfekaay.o build/libposix-kor.a ../compiler/kiy_jariñoo_internet_lëkkale_Tëralin.ld
	$(CC) $(CFLAGS) -c build/Cosaan/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/kiy_jariñoo_internet_lëkkale_Tëralin.ld -o $@ build/Door_kiy_jariñoo_internet_jëfekaay.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Jumtukaay_yi/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
