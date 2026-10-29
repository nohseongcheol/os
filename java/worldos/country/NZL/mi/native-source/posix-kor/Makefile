PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files pūtake)
구현이름 := kōnae_I_O 통신종단점 paita_aho kaiwhakamahi_tāuru
ahanoa_kōnae_Rārangi := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/pūnaha_mahi_Ngā_Waeatanga.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/pūtake/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Ngā_Utauta/pūtāutu_tahuritanga.py
	mkdir -p build
	$(PYTHON) Ngā_Utauta/pūtāutu_tahuritanga.py pūtake build/pūtake
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/pūtake/구현/$*.c -o $@
build/pūnaha_mahi_Ngā_Waeatanga.o: mīhini/pūnaha_mahi_Ngā_Waeatanga.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_kaiwhakamahi_kaupapa.o: mīhini/Start_kaiwhakamahi_kaupapa.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ahanoa_kōnae_Rārangi)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_kaiwhakamahi_kaupapa.o build/libposix-kor.a ../compiler/kaiwhakamahi_Hono_Tahora.ld
	$(CC) $(CFLAGS) -c build/pūtake/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/kaiwhakamahi_Hono_Tahora.ld -o $@ build/Start_kaiwhakamahi_kaupapa.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Ngā_Utauta/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
