PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files pinagmulan)
구현이름 := file_I_O 통신종단점 byte_string gumagamit_magpasok
bagay_file_list := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operating_system_Mga_Tawag.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/pinagmulan/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Mga_Tool/tagakilala_pagpapalit.py
	mkdir -p build
	$(PYTHON) Mga_Tool/tagakilala_pagpapalit.py pinagmulan build/pinagmulan
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/pinagmulan/구현/$*.c -o $@
build/operating_system_Mga_Tawag.o: machine/operating_system_Mga_Tawag.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_gumagamit_app.o: machine/Start_gumagamit_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(bagay_file_list)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_gumagamit_app.o build/libposix-kor.a ../compiler/gumagamit_Link_Layout.ld
	$(CC) $(CFLAGS) -c build/pinagmulan/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/gumagamit_Link_Layout.ld -o $@ build/Start_gumagamit_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Mga_Tool/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
