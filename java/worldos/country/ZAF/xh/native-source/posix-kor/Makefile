PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files UMTHOMBO)
구현이름 := ifayile_i_I_O 통신종단점 ibhayithi_uluhlu_lweekharektha umsebenzisi_ngenisa
into_ifayile_uludwe := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/UMTHOMBO/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Izixhobo/isalathisi_uguqulo.py
	mkdir -p build
	$(PYTHON) Izixhobo/isalathisi_uguqulo.py UMTHOMBO build/UMTHOMBO
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/UMTHOMBO/구현/$*.c -o $@
build/운영체제호출.o: umatshini/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/qala_umsebenzisi_inkqubo.o: umatshini/qala_umsebenzisi_inkqubo.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(into_ifayile_uludwe)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/qala_umsebenzisi_inkqubo.o build/libposix-kor.a ../compiler/umsebenzisi_Ilinki_ubume.ld
	$(CC) $(CFLAGS) -c build/UMTHOMBO/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/umsebenzisi_Ilinki_ubume.ld -o $@ build/qala_umsebenzisi_inkqubo.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Izixhobo/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
