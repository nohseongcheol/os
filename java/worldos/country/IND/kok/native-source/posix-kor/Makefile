PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files स्त्रोत)
구현이름 := फायल_I_O 통신종단점 बायट_स्ट्रिंग उपेगकर्तो_प्रवेश_करचो
ऑब्जॅक्ट_फायल_सुची := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ऑपरेटिंग_प्रणाली_कॉलां.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/स्त्रोत/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) साधनां/वळखुपी_रूपांतर.py
	mkdir -p build
	$(PYTHON) साधनां/वळखुपी_रूपांतर.py स्त्रोत build/स्त्रोत
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/स्त्रोत/구현/$*.c -o $@
build/ऑपरेटिंग_प्रणाली_कॉलां.o: यंत्र/ऑपरेटिंग_प्रणाली_कॉलां.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_उपेगकर्तो_एप्लिकेशन.o: यंत्र/Start_उपेगकर्तो_एप्लिकेशन.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ऑब्जॅक्ट_फायल_सुची)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_उपेगकर्तो_एप्लिकेशन.o build/libposix-kor.a ../compiler/उपेगकर्तो_लिंक_रचणाय.ld
	$(CC) $(CFLAGS) -c build/स्त्रोत/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/उपेगकर्तो_लिंक_रचणाय.ld -o $@ build/Start_उपेगकर्तो_एप्लिकेशन.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) साधनां/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
