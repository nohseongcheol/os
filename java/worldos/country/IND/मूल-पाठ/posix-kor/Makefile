PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files स्रोत)
구현이름 := फ़ाइल_इनपुट_आउटपुट सॉकेट_एंडपॉइंट बाइट_स्ट्रिंग उपयोगकर्ता_दर्ज_करें
ऑब्जेक्ट_फ़ाइल_सूची := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ऑपरेटिंग_सिस्टम_कॉल्स.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
परिक्षण_सूची := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/स्रोत/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(परिक्षण_सूची)
build/변환완료: $(원문목록) उपकरण/पहचानकर्ता_रूपांतरण.py
	mkdir -p build
	$(PYTHON) उपकरण/पहचानकर्ता_रूपांतरण.py स्रोत build/स्रोत
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/स्रोत/구현/$*.c -o $@
build/ऑपरेटिंग_सिस्टम_कॉल्स.o: यंत्र/ऑपरेटिंग_सिस्टम_कॉल्स.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/प्रारंभ_उपयोगकर्ता_ऐप.o: यंत्र/प्रारंभ_उपयोगकर्ता_ऐप.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ऑब्जेक्ट_फ़ाइल_सूची)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/प्रारंभ_उपयोगकर्ता_ऐप.o build/libposix-kor.a ../compiler/उपयोगकर्ता_लिंक_लेआउट.ld
	$(CC) $(CFLAGS) -c build/स्रोत/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/उपयोगकर्ता_लिंक_लेआउट.ld -o $@ build/प्रारंभ_उपयोगकर्ता_ऐप.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) उपकरण/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
