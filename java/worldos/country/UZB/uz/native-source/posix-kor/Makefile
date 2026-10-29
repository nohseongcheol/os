PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files manba)
구현이름 := fayl_I_O 통신종단점 bayt_satr foydalanuvchi_kiritmoq
obyekt_fayl_Ro_yxat := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/operatsion_tizim_Qo_ng_iroqlar.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/manba/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Vositalar/identifikator_aylantirish.py
	mkdir -p build
	$(PYTHON) Vositalar/identifikator_aylantirish.py manba build/manba
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/manba/구현/$*.c -o $@
build/operatsion_tizim_Qo_ng_iroqlar.o: 기계/operatsion_tizim_Qo_ng_iroqlar.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_foydalanuvchi_ilova.o: 기계/Start_foydalanuvchi_ilova.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(obyekt_fayl_Ro_yxat)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_foydalanuvchi_ilova.o build/libposix-kor.a ../compiler/foydalanuvchi_ulash_Maket.ld
	$(CC) $(CFLAGS) -c build/manba/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/foydalanuvchi_ulash_Maket.ld -o $@ build/Start_foydalanuvchi_ilova.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Vositalar/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
