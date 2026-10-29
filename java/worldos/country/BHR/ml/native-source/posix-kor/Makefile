PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ഉറവിടം)
구현이름 := ഫയല്_ഇന്_പുട്ട്_ഔട്ട്_പുട്ട് 통신종단점 బైట్_സ്ട്രിംഗ് ഉപയോക്താവ്_നല്_കുക
ഓബ്ജക്റ്റ്_ഫയല്_ലിസ്റ്റ് := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_കോളുകൾ.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
പരിശോധന_ലിസ്റ്റ് := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ഉറവിടം/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(പരിശോധന_ലിസ്റ്റ്)
build/변환완료: $(원문목록) ഉപകരണങ്ങൾ/ఐడెంటిఫయర్_പരിവര്_ത്തനം.py
	mkdir -p build
	$(PYTHON) ഉപകരണങ്ങൾ/ఐడెంటిఫయర్_പരിവര്_ത്തനം.py ഉറവിടം build/ഉറവിടം
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ഉറവിടം/구현/$*.c -o $@
build/ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_കോളുകൾ.o: മെഷീൻ/ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_കോളുകൾ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം.o: മെഷീൻ/ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ഓബ്ജക്റ്റ്_ഫയല്_ലിസ്റ്റ്)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം.o build/libposix-kor.a ../compiler/ഉപയോക്താവ്_ലിങ്ക്_ലേഔട്ട്.ld
	$(CC) $(CFLAGS) -c build/ഉറവിടം/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ഉപയോക്താവ്_ലിങ്ക്_ലേഔട്ട്.ld -o $@ build/ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ഉപകരണങ്ങൾ/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
