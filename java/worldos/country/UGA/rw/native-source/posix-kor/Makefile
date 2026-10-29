PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files Inkomoko)
구현이름 := dosiye_I_O 통신종단점 bayiti_igicenteruro ukoresha_kwandika
ikintu_dosiye_Urutonde := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Inkomoko/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Ibikoresho/indanga_ihindura.py
	mkdir -p build
	$(PYTHON) Ibikoresho/indanga_ihindura.py Inkomoko build/Inkomoko
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/Inkomoko/구현/$*.c -o $@
build/운영체제호출.o: imashini/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Itangira_ukoresha_porogaramu.o: imashini/Itangira_ukoresha_porogaramu.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ikintu_dosiye_Urutonde)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Itangira_ukoresha_porogaramu.o build/libposix-kor.a ../compiler/ukoresha_Ihuza_Imimerere.ld
	$(CC) $(CFLAGS) -c build/Inkomoko/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ukoresha_Ihuza_Imimerere.ld -o $@ build/Itangira_ukoresha_porogaramu.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Ibikoresho/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
