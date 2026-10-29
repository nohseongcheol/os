PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files манбаъ)
구현이름 := файл_вуруд_хуруҷ 통신종단점 байт_сатр корбар_ворид_кардан
объект_файл_Рӯйхат := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/운영체제호출.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/манбаъ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) Абзорҳо/식별자변환.py
	mkdir -p build
	$(PYTHON) Абзорҳо/식별자변환.py манбаъ build/манбаъ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/манбаъ/구현/$*.c -o $@
build/운영체제호출.o: компютер/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Оғоз_корбар_барнома.o: компютер/Оғоз_корбар_барнома.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(объект_файл_Рӯйхат)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Оғоз_корбар_барнома.o build/libposix-kor.a ../compiler/корбар_Пайванд_Тарҳбандӣ.ld
	$(CC) $(CFLAGS) -c build/манбаъ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/корбар_Пайванд_Тарҳбандӣ.ld -o $@ build/Оғоз_корбар_барнома.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Абзорҳо/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
