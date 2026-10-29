PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ALLIKAS)
구현이름 := Fail_I_O 통신종단점 bait_string kasutaja_sisestama
objekt_Fail_Loend := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operatsioonisüsteem_Kõned.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ALLIKAS/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Tööriistad/identifikaator_teisendamine.py
	mkdir -p build
	$(PYTHON) Tööriistad/identifikaator_teisendamine.py ALLIKAS build/ALLIKAS
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ALLIKAS/구현/$*.c -o $@
build/operatsioonisüsteem_Kõned.o: arvuti/operatsioonisüsteem_Kõned.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_kasutaja_programm.o: arvuti/START_kasutaja_programm.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objekt_Fail_Loend)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_kasutaja_programm.o build/libposix-kor.a ../compiler/kasutaja_Link_küljend.ld
	$(CC) $(CFLAGS) -c build/ALLIKAS/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/kasutaja_Link_küljend.ld -o $@ build/START_kasutaja_programm.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Tööriistad/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
