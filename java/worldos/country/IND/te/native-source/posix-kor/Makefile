PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files వనరు)
구현이름 := ఫైలు_మూ_ఫ 통신종단점 బైట్_అక్షరసరం వినియోగదారు_ప్రవేశపెట్టు
అంశం_ఫైలు_జాబితా := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/నిర్వహణా_వ్యవస్థ_కాల్_లు.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/వనరు/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ఉపకరణాలు/ఐడెంటిఫయర్_మార్పిడి.py
	mkdir -p build
	$(PYTHON) ఉపకరణాలు/ఐడెంటిఫయర్_మార్పిడి.py వనరు build/వనరు
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/వనరు/구현/$*.c -o $@
build/నిర్వహణా_వ్యవస్థ_కాల్_లు.o: యంత్రం/నిర్వహణా_వ్యవస్థ_కాల్_లు.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ప్రారంభం_వినియోగదారు_అనువర్తనం.o: యంత్రం/ప్రారంభం_వినియోగదారు_అనువర్తనం.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(అంశం_ఫైలు_జాబితా)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ప్రారంభం_వినియోగదారు_అనువర్తనం.o build/libposix-kor.a ../compiler/వినియోగదారు_బంధం_లేవుట్.ld
	$(CC) $(CFLAGS) -c build/వనరు/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/వినియోగదారు_బంధం_లేవుట్.ld -o $@ build/ప్రారంభం_వినియోగదారు_అనువర్తనం.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ఉపకరణాలు/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
