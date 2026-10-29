PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files Bron)
구현이름 := lêer_I_O 통신종단점 greep_string gebruiker_invoer
objek_lêer_Lys := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/bedryfstelsel_Oproepe.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Bron/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Nutsmiddels/waarde_konversasie.py
	mkdir -p build
	$(PYTHON) Nutsmiddels/waarde_konversasie.py Bron build/Bron
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/Bron/구현/$*.c -o $@
build/bedryfstelsel_Oproepe.o: masjien/bedryfstelsel_Oproepe.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/BEGIN_gebruiker_program.o: masjien/BEGIN_gebruiker_program.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objek_lêer_Lys)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/BEGIN_gebruiker_program.o build/libposix-kor.a ../compiler/gebruiker_Skakel_Uitleg.ld
	$(CC) $(CFLAGS) -c build/Bron/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/gebruiker_Skakel_Uitleg.ld -o $@ build/BEGIN_gebruiker_program.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Nutsmiddels/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
