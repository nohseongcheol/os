PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ምንጭ)
구현이름 := ፋይል_ግቤት_ውጤት 통신종단점 ባይት_ኅብረቁምፊ ተጠቃሚ_አስገባ
ነገር_ፋይል_ዝርዝር := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ስርዓተ_ክወና_የስልክ_ጥሪዎች.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ምንጭ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) መሳሪያዎች/መለያ_ንግግር.py
	mkdir -p build
	$(PYTHON) መሳሪያዎች/መለያ_ንግግር.py ምንጭ build/ምንጭ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ምንጭ/구현/$*.c -o $@
build/ስርዓተ_ክወና_የስልክ_ጥሪዎች.o: ማሽን/ስርዓተ_ክወና_የስልክ_ጥሪዎች.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ጀምር_ተጠቃሚ_ፕሮግራም.o: ማሽን/ጀምር_ተጠቃሚ_ፕሮግራም.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ነገር_ፋይል_ዝርዝር)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ጀምር_ተጠቃሚ_ፕሮግራም.o build/libposix-kor.a ../compiler/ተጠቃሚ_አገናኝ_አሰሳ.ld
	$(CC) $(CFLAGS) -c build/ምንጭ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ተጠቃሚ_አገናኝ_አሰሳ.ld -o $@ build/ጀምር_ተጠቃሚ_ፕሮግራም.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) መሳሪያዎች/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
