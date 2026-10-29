PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
स्रोतसूची := $(shell rg --files स्रोत)
अंमलबजावणी_नावे := संचिका_इनपुट_आउटपुट संचारद्वार_संचारटोक बाइट_स्ट्रींग प्रयोक्ता_प्रविष्ठ_करणे
ऑब्जेक्ट_संचिका_यादी := $(addprefix build/,$(addsuffix .o,$(अंमलबजावणी_नावे))) build/ऑपरेटिंग_सिस्टम_कॉल्स.o
नावे_चाचणी := संचिका_द्विमानजोडणी_चाचणी स्वतंत्रसंदेश_चाचणी प्रमाणित_आदान_चाचणी संचिका_जतन_चाचणी
यादी_चाचणी := $(addprefix build/,$(addsuffix .elf,$(नावे_चाचणी)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/स्रोत/घोषणाशीर्षे
.PHONY: all test test-tools
all: build/libposix-kor.a $(यादी_चाचणी)
build/रुपांतरण_पूर्ण: $(स्रोतसूची) साधने/आयडेंटिफायर_रुपांतरण.py
	mkdir -p build
	$(PYTHON) साधने/आयडेंटिफायर_रुपांतरण.py स्रोत build/स्रोत
	touch $@
build/%.o: build/रुपांतरण_पूर्ण
	$(CC) $(CFLAGS) -c build/स्रोत/अंमलबजावणी/$*.c -o $@
build/ऑपरेटिंग_सिस्टम_कॉल्स.o: मशीन/ऑपरेटिंग_सिस्टम_कॉल्स.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/प्रारंभ_प्रयोक्ता_अनुप्रयोग.o: मशीन/प्रारंभ_प्रयोक्ता_अनुप्रयोग.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ऑब्जेक्ट_संचिका_यादी)
	$(AR) rcs $@ $^
build/%.elf: build/रुपांतरण_पूर्ण build/प्रारंभ_प्रयोक्ता_अनुप्रयोग.o build/libposix-kor.a ../compiler/प्रयोक्ता_लिंक_लेआउट.ld
	$(CC) $(CFLAGS) -c build/स्रोत/चाचण्या/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/प्रयोक्ता_लिंक_लेआउट.ld -o $@ build/प्रारंभ_प्रयोक्ता_अनुप्रयोग.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) साधने/रुपांतरण_चाचणी.py

.PHONY: clean
clean:
	rm -rf -- build
