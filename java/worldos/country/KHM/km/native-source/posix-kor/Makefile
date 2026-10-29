PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ប្រភព)
구현이름 := ឯកសារ_ចូល_ចេញ 통신종단점 បៃ_សំនុំអក្សរ អ្នកប្រើ_បញ្ចូល
វត្ថុ_ឯកសារ_បញ្ជី := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ប្រព័ន្ធប្រតិបត្តិការណ៏_ការហៅ.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ប្រភព/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ឧបករណ៍/អង្គសម្គាល់_ការបំលែង.py
	mkdir -p build
	$(PYTHON) ឧបករណ៍/អង្គសម្គាល់_ការបំលែង.py ប្រភព build/ប្រភព
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ប្រភព/구현/$*.c -o $@
build/ប្រព័ន្ធប្រតិបត្តិការណ៏_ការហៅ.o: ម៉ាស៊ីន/ប្រព័ន្ធប្រតិបត្តិការណ៏_ការហៅ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ផ្តើម_អ្នកប្រើ_កម្មវិធី.o: ម៉ាស៊ីន/ផ្តើម_អ្នកប្រើ_កម្មវិធី.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(វត្ថុ_ឯកសារ_បញ្ជី)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ផ្តើម_អ្នកប្រើ_កម្មវិធី.o build/libposix-kor.a ../compiler/អ្នកប្រើ_តំណ_ប្លង់.ld
	$(CC) $(CFLAGS) -c build/ប្រភព/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/អ្នកប្រើ_តំណ_ប្លង់.ld -o $@ build/ផ្តើម_អ្នកប្រើ_កម្មវិធី.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ឧបករណ៍/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
