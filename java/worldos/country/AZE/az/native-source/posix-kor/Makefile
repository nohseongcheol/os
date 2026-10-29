PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files QAYNAQ)
구현이름 := fayl_giriş_çıxış 통신종단점 bayt_sətir istifadəçi_daxil_etmək
obyekt_fayl_Siyahı := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/əməliyyat_sistemi_Zənglər.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/QAYNAQ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Alətlər/identifikator_çevirmə.py
	mkdir -p build
	$(PYTHON) Alətlər/identifikator_çevirmə.py QAYNAQ build/QAYNAQ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/QAYNAQ/구현/$*.c -o $@
build/əməliyyat_sistemi_Zənglər.o: maşın/əməliyyat_sistemi_Zənglər.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Başla_istifadəçi_proqram.o: maşın/Başla_istifadəçi_proqram.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(obyekt_fayl_Siyahı)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Başla_istifadəçi_proqram.o build/libposix-kor.a ../compiler/istifadəçi_keçid_Düzüm.ld
	$(CC) $(CFLAGS) -c build/QAYNAQ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/istifadəçi_keçid_Düzüm.ld -o $@ build/Başla_istifadəçi_proqram.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Alətlər/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
