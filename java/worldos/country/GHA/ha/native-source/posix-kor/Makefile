PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files tushe)
구현이름 := Fayil_I_O 통신종단점 bayit_Zare Mai_anfani_da_kwamfuta_Shiga
abu_Fayil_Jeri := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/tushe/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Kaya/mai_ganewa_juyawa.py
	mkdir -p build
	$(PYTHON) Kaya/mai_ganewa_juyawa.py tushe build/tushe
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/tushe/구현/$*.c -o $@
build/운영체제호출.o: na_ura_mai_kwakwalwa/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Fara_Mai_anfani_da_kwamfuta_Shiri.o: na_ura_mai_kwakwalwa/Fara_Mai_anfani_da_kwamfuta_Shiri.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(abu_Fayil_Jeri)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Fara_Mai_anfani_da_kwamfuta_Shiri.o build/libposix-kor.a ../compiler/Mai_anfani_da_kwamfuta_Kafa_Zagaye.ld
	$(CC) $(CFLAGS) -c build/tushe/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/Mai_anfani_da_kwamfuta_Kafa_Zagaye.ld -o $@ build/Fara_Mai_anfani_da_kwamfuta_Shiri.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Kaya/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
