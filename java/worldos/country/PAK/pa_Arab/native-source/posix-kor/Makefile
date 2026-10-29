PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ماخذ)
구현이름 := 파일입출력 통신종단점 بائٹ_سٹرنگ صارف_داخل_کرو
آبجیکٹ_فائل_فرست := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ماخذ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) اوزار/شناخت_کرنڑ_آلا_تبدیلی.py
	mkdir -p build
	$(PYTHON) اوزار/شناخت_کرنڑ_آلا_تبدیلی.py ماخذ build/ماخذ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ماخذ/구현/$*.c -o $@
build/운영체제호출.o: مشین/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/مکھ_صارف_ایپ.o: مشین/مکھ_صارف_ایپ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(آبجیکٹ_فائل_فرست)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/مکھ_صارف_ایپ.o build/libposix-kor.a ../compiler/صارف_ربط_لے_آؤٹ.ld
	$(CC) $(CFLAGS) -c build/ماخذ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/صارف_ربط_لے_آؤٹ.ld -o $@ build/مکھ_صارف_ایپ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) اوزار/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
