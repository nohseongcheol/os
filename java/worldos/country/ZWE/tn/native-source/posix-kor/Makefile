PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files Motswedi)
구현이름 := faele_I_O 통신종단점 baete_dikwalwa modirisi_kwadisa
selwana_faele_lenaane := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Motswedi/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Thuluse/setlhaodi_phetolelo.py
	mkdir -p build
	$(PYTHON) Thuluse/setlhaodi_phetolelo.py Motswedi build/Motswedi
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/Motswedi/구현/$*.c -o $@
build/운영체제호출.o: motšhine/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/simolola_modirisi_Tiriso.o: motšhine/simolola_modirisi_Tiriso.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(selwana_faele_lenaane)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/simolola_modirisi_Tiriso.o build/libposix-kor.a ../compiler/modirisi_Kgokagano_Boalo.ld
	$(CC) $(CFLAGS) -c build/Motswedi/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/modirisi_Kgokagano_Boalo.ld -o $@ build/simolola_modirisi_Tiriso.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Thuluse/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
