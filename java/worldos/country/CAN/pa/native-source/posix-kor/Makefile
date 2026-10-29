PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ਸਰੋਤ)
구현이름 := ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ 통신종단점 ਬਾਈਟ_ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ ਉਪਭੋਗਤਾ_ਦਾਖ਼ਲ_ਕਰੋ
ਔਬਜੈਕਟ_ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕਾਲਾਂ.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ਸਰੋਤ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ਸਾਧਨ/ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਰੂਪਾਂਤਰਨ.py
	mkdir -p build
	$(PYTHON) ਸਾਧਨ/ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਰੂਪਾਂਤਰਨ.py ਸਰੋਤ build/ਸਰੋਤ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ਸਰੋਤ/구현/$*.c -o $@
build/ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕਾਲਾਂ.o: ਮਸ਼ੀਨ/ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕਾਲਾਂ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ਸੁਰੂ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼.o: ਮਸ਼ੀਨ/ਸੁਰੂ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ਔਬਜੈਕਟ_ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ਸੁਰੂ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼.o build/libposix-kor.a ../compiler/ਉਪਭੋਗਤਾ_ਲਿੰਕ_ਖਾਕਾ.ld
	$(CC) $(CFLAGS) -c build/ਸਰੋਤ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ਉਪਭੋਗਤਾ_ਲਿੰਕ_ਖਾਕਾ.ld -o $@ build/ਸੁਰੂ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ਸਾਧਨ/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
