PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files स्रोत)
구현이름 := फाइल_आगत_लगत 통신종단점 बाइट_स्ट्रिङ प्रयोगकर्ता_प्रविष्टि_गराउनुहोस्
वस्तु_फाइल_सूची := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/सञ्चालनप्रणाली_कलहरू.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/स्रोत/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) उपकरणहरू/परिचायक_परिवर्तन.py
	mkdir -p build
	$(PYTHON) उपकरणहरू/परिचायक_परिवर्तन.py स्रोत build/स्रोत
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/स्रोत/구현/$*.c -o $@
build/सञ्चालनप्रणाली_कलहरू.o: मेशिन/सञ्चालनप्रणाली_कलहरू.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/सुरु_प्रयोगकर्ता_अनुप्रयोग.o: मेशिन/सुरु_प्रयोगकर्ता_अनुप्रयोग.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(वस्तु_फाइल_सूची)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/सुरु_प्रयोगकर्ता_अनुप्रयोग.o build/libposix-kor.a ../compiler/प्रयोगकर्ता_लिङ्क_लेआउट.ld
	$(CC) $(CFLAGS) -c build/स्रोत/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/प्रयोगकर्ता_लिङ्क_लेआउट.ld -o $@ build/सुरु_प्रयोगकर्ता_अनुप्रयोग.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) उपकरणहरू/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
