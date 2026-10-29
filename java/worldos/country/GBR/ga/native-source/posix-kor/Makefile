PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files FOINSE)
구현이름 := comhad_I_O 통신종단점 beart_teaghrán úsáideoir_iontráil
oibiacht_comhad_Liosta := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/córas_oibriúcháin_Glaonna.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/FOINSE/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Uirlisí/aitheantóir_comhshó.py
	mkdir -p build
	$(PYTHON) Uirlisí/aitheantóir_comhshó.py FOINSE build/FOINSE
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/FOINSE/구현/$*.c -o $@
build/córas_oibriúcháin_Glaonna.o: meaisín/córas_oibriúcháin_Glaonna.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_úsáideoir_clár.o: meaisín/Start_úsáideoir_clár.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(oibiacht_comhad_Liosta)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_úsáideoir_clár.o build/libposix-kor.a ../compiler/úsáideoir_Nasc_dáileadh.ld
	$(CC) $(CFLAGS) -c build/FOINSE/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/úsáideoir_Nasc_dáileadh.ld -o $@ build/Start_úsáideoir_clár.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Uirlisí/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
