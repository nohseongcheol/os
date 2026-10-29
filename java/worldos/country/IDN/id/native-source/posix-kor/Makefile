PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files kodeSumber)
구현이름 := file_I_O 통신종단점 byte_string pengguna_masukkan
objek_file_Daftar := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/sistem_operasi_Panggilan.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/kodeSumber/deklarasi
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) alat/pengidentifikasi_konversi.py
	mkdir -p build
	$(PYTHON) alat/pengidentifikasi_konversi.py kodeSumber build/kodeSumber
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/kodeSumber/implementasi/$*.c -o $@
build/sistem_operasi_Panggilan.o: mesin/sistem_operasi_Panggilan.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Mulai_pengguna_apl.o: mesin/Mulai_pengguna_apl.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objek_file_Daftar)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Mulai_pengguna_apl.o build/libposix-kor.a ../compiler/pengguna_link_Navigasi.ld
	$(CC) $(CFLAGS) -c build/kodeSumber/pengujian/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/pengguna_link_Navigasi.ld -o $@ build/Mulai_pengguna_apl.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) alat/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
