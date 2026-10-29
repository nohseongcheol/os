PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ምንጪ)
구현이름 := 파일입출력 통신종단점 ባይት_ሕብረ_ቁምፊ ተጠቃሚ_የእትው
ነገር_ፋይል_ዝርዝር := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ምንጪ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) መሳርሒታት/ፈላዪ_ቅየራ.py
	mkdir -p build
	$(PYTHON) መሳርሒታት/ፈላዪ_ቅየራ.py ምንጪ build/ምንጪ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ምንጪ/구현/$*.c -o $@
build/운영체제호출.o: ማሽን/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ጀምር_ተጠቃሚ_መተግበሪ.o: ማሽን/ጀምር_ተጠቃሚ_መተግበሪ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ነገር_ፋይል_ዝርዝር)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ጀምር_ተጠቃሚ_መተግበሪ.o build/libposix-kor.a ../compiler/ተጠቃሚ_መጋጠሚ_ኣቀማምጣ.ld
	$(CC) $(CFLAGS) -c build/ምንጪ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ተጠቃሚ_መጋጠሚ_ኣቀማምጣ.ld -o $@ build/ጀምር_ተጠቃሚ_መተግበሪ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) መሳርሒታት/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
