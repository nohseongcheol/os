PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files tùs)
구현이름 := faidhle_I_O 통신종단점 baidht_sreang cleachdaiche_cuir_a_steach
nì_faidhle_Liosta := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/siostam_obrachaidh_gairmean.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/tùs/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) innealan/aithnichear_iompachadh.py
	mkdir -p build
	$(PYTHON) innealan/aithnichear_iompachadh.py tùs build/tùs
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/tùs/구현/$*.c -o $@
build/siostam_obrachaidh_gairmean.o: inneal/siostam_obrachaidh_gairmean.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_cleachdaiche_ap.o: inneal/Start_cleachdaiche_ap.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(nì_faidhle_Liosta)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_cleachdaiche_ap.o build/libposix-kor.a ../compiler/cleachdaiche_ceangal_co_dhealbhachd.ld
	$(CC) $(CFLAGS) -c build/tùs/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/cleachdaiche_ceangal_co_dhealbhachd.ld -o $@ build/Start_cleachdaiche_ap.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) innealan/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
