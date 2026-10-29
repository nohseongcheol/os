PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ЭХ)
구현이름 := файл_оролт_гаралт 통신종단점 байт_мөр хэрэглэгч_орох
объект_файл_Жагсаалт := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ЭХ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Хэрэгслүүд/танигч_хөрвүүлэлт.py
	mkdir -p build
	$(PYTHON) Хэрэгслүүд/танигч_хөрвүүлэлт.py ЭХ build/ЭХ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ЭХ/구현/$*.c -o $@
build/운영체제호출.o: компьютер/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Эхлэл_хэрэглэгч_програм.o: компьютер/Эхлэл_хэрэглэгч_програм.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(объект_файл_Жагсаалт)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Эхлэл_хэрэглэгч_програм.o build/libposix-kor.a ../compiler/хэрэглэгч_Холбох_Бүдүүвч.ld
	$(CC) $(CFLAGS) -c build/ЭХ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/хэрэглэгч_Холбох_Бүдүүвч.ld -o $@ build/Эхлэл_хэрэглэгч_програм.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Хэрэгслүүд/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
