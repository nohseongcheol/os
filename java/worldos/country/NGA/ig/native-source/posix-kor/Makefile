PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ebensìbịa)
구현이름 := ọbọakwụkwọ_I_O 통신종단점 baịtị_ùsòròokwū òjìàrụ_tinye
ihe_ọbọakwụkwọ_ndepụta := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ebensìbịa/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Ngwaọrụ/ihe_nkọwapụta_mgbanwe.py
	mkdir -p build
	$(PYTHON) Ngwaọrụ/ihe_nkọwapụta_mgbanwe.py ebensìbịa build/ebensìbịa
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ebensìbịa/구현/$*.c -o $@
build/운영체제호출.o: ngwa_komputa/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Mbido_òjìàrụ_app.o: ngwa_komputa/Mbido_òjìàrụ_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ihe_ọbọakwụkwọ_ndepụta)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Mbido_òjìàrụ_app.o build/libposix-kor.a ../compiler/òjìàrụ_Njikọ_Nhàzi.ld
	$(CC) $(CFLAGS) -c build/ebensìbịa/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/òjìàrụ_Njikọ_Nhàzi.ld -o $@ build/Mbido_òjìàrụ_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Ngwaọrụ/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
