PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files මූලය)
구현이름 := ගොනුව_ආදාන_ප්_රතිදාන 통신종단점 බයිටය_අනුලකුණු_වැල පරිශීලක_ඇතුල්_කිරීම
වස්තුව_ගොනුව_ලැයිස්තුව := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/මූලය/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) මෙවලම්/හඳුන්වනය_පරිවර්තනය.py
	mkdir -p build
	$(PYTHON) මෙවලම්/හඳුන්වනය_පරිවර්තනය.py මූලය build/මූලය
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/මූලය/구현/$*.c -o $@
build/운영체제호출.o: යන්ත්_රය/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ඇරඹුම_පරිශීලක_යෙදු.o: යන්ත්_රය/ඇරඹුම_පරිශීලක_යෙදු.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(වස්තුව_ගොනුව_ලැයිස්තුව)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ඇරඹුම_පරිශීලක_යෙදු.o build/libposix-kor.a ../compiler/පරිශීලක_සබැඳිය_සැකැස්ම.ld
	$(CC) $(CFLAGS) -c build/මූලය/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/පරිශීලක_සබැඳිය_සැකැස්ම.ld -o $@ build/ඇරඹුම_පරිශීලක_යෙදු.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) මෙවලම්/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
