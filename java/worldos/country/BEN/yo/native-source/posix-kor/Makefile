PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files orísun)
구현이름 := fáìlì_I_O 통신종단점 báìtì_fọ́nrán aṣàmúlò_ṣàtẹ̀wọlé
nǹkan_fáìlì_Àtòkọ := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/orísun/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Àwọn_irinṣẹ́/Àfidámọ̀_ìbánisọ̀rọ̀.py
	mkdir -p build
	$(PYTHON) Àwọn_irinṣẹ́/Àfidámọ̀_ìbánisọ̀rọ̀.py orísun build/orísun
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/orísun/구현/$*.c -o $@
build/운영체제호출.o: maṣíìnì/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò.o: maṣíìnì/bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(nǹkan_fáìlì_Àtòkọ)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò.o build/libposix-kor.a ../compiler/aṣàmúlò_ṣàsopọ̀_ètò_ìrísí.ld
	$(CC) $(CFLAGS) -c build/orísun/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/aṣàmúlò_ṣàsopọ̀_ètò_ìrísí.ld -o $@ build/bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Àwọn_irinṣẹ́/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
