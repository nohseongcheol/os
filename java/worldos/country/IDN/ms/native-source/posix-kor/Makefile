PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files SUMBER)
구현이름 := fail_I_O 통신종단점 bait_rentetan pengguna_masuk
objek_fail_Senarai := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/sistem_pengendalian_Panggilan.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
senarai_ujian := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/SUMBER/pengisytiharan
.PHONY: all test test-tools
all: build/libposix-kor.a $(senarai_ujian)
build/변환완료: $(원문목록) alat/식별자변환.py
	mkdir -p build
	$(PYTHON) alat/식별자변환.py SUMBER build/SUMBER
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/SUMBER/pelaksanaan/$*.c -o $@
build/sistem_pengendalian_Panggilan.o: mesin/sistem_pengendalian_Panggilan.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Mula_pengguna_aplikasi.o: mesin/Mula_pengguna_aplikasi.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objek_fail_Senarai)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Mula_pengguna_aplikasi.o build/libposix-kor.a ../compiler/pengguna_paut_Navigasi.ld
	$(CC) $(CFLAGS) -c build/SUMBER/ujian/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/pengguna_paut_Navigasi.ld -o $@ build/Mula_pengguna_aplikasi.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) alat/penukaran_ujian.py

.PHONY: clean
clean:
	rm -rf -- build
