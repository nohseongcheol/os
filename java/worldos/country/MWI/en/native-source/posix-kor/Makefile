PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
sources := $(shell rg --files source)
implementationNames := FileInputOutput SocketEndpoint ByteString userEnter
objectFileList := $(addprefix build/,$(addsuffix .o,$(implementationNames))) build/OperatingSystemCalls.o
testNames := FileAbiTest DatagramTest StandardInputTest FilePreservationTest
testList := $(addprefix build/,$(addsuffix .elf,$(testNames)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/source/headers
.PHONY: all test test-tools
all: build/libposix-kor.a $(testList)
build/conversionComplete: $(sources) tools/IdentifierConversion.py
	mkdir -p build
	$(PYTHON) tools/IdentifierConversion.py source build/source
	touch $@
build/%.o: build/conversionComplete
	$(CC) $(CFLAGS) -c build/source/implementation/$*.c -o $@
build/OperatingSystemCalls.o: machine/OperatingSystemCalls.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/startUserProgram.o: machine/startUserProgram.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objectFileList)
	$(AR) rcs $@ $^
build/%.elf: build/conversionComplete build/startUserProgram.o build/libposix-kor.a ../compiler/userLinkLayout.ld
	$(CC) $(CFLAGS) -c build/source/tests/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/userLinkLayout.ld -o $@ build/startUserProgram.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) tools/ConversionTest.py

.PHONY: clean
clean:
	rm -rf -- build
