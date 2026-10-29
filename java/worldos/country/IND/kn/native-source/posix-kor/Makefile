PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ಮೂಲ)
구현이름 := ಫೈಲ್_ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್ 통신종단점 ಬೈಟ್_ಸ್ಟ್ರಿಂಗ್ ಬಳಕೆದಾರ_ನಮೂದಿಸು
ಆಬ್ಜೆಕ್ಟ್_ಫೈಲ್_ಪಟ್ಟಿ := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಕರೆಗಳು.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ಮೂಲ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ಪರಿಕರಗಳು/ಗುರುತಿಸುವಿಕೆ_ಪರಿವರ್ತನೆ.py
	mkdir -p build
	$(PYTHON) ಪರಿಕರಗಳು/ಗುರುತಿಸುವಿಕೆ_ಪರಿವರ್ತನೆ.py ಮೂಲ build/ಮೂಲ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ಮೂಲ/구현/$*.c -o $@
build/ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಕರೆಗಳು.o: ಯಂತ್ರ/ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ_ಕರೆಗಳು.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ.o: ಯಂತ್ರ/ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ಆಬ್ಜೆಕ್ಟ್_ಫೈಲ್_ಪಟ್ಟಿ)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ.o build/libposix-kor.a ../compiler/ಬಳಕೆದಾರ_ಜೋಡಣೆ_ಲೇಔಟ್.ld
	$(CC) $(CFLAGS) -c build/ಮೂಲ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ಬಳಕೆದಾರ_ಜೋಡಣೆ_ಲೇಔಟ್.ld -o $@ build/ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ಪರಿಕರಗಳು/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
