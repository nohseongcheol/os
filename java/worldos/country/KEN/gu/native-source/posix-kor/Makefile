PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files સ્રોત)
구현이름 := ફાઇલ_ઇનપુટ_આઉટપુટ 통신종단점 બાઇટ_સ્ટ્રિંગ ઉપયોગકર્તા_દાખલ_કરો
ઑબ્જેક્ટ_ફાઇલ_સૂચી := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ઑપરેટિંગ_સિસ્ટમ_કૉલ્સ.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/સ્રોત/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ઉપકરણો/ઓળખકર્તા_રૂપાંતરણ.py
	mkdir -p build
	$(PYTHON) ઉપકરણો/ઓળખકર્તા_રૂપાંતરણ.py સ્રોત build/સ્રોત
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/સ્રોત/구현/$*.c -o $@
build/ઑપરેટિંગ_સિસ્ટમ_કૉલ્સ.o: મશીન/ઑપરેટિંગ_સિસ્ટમ_કૉલ્સ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન.o: મશીન/પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ઑબ્જેક્ટ_ફાઇલ_સૂચી)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન.o build/libposix-kor.a ../compiler/ઉપયોગકર્તા_લિંક_લેઆઉટ.ld
	$(CC) $(CFLAGS) -c build/સ્રોત/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ઉપયોગકર્તા_લિંક_લેઆઉટ.ld -o $@ build/પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ઉપકરણો/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
