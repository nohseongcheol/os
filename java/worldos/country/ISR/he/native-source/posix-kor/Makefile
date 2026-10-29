PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files קודמקור)
구현이름 := קובץ_קלט_פלט 통신종단점 בית_מחרוזת משתמש_הזן
אובייקט_קובץ_רשימה := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/מערכת_הפעלה_שיחות_טלפון.o
시험이름 := 파일규약시험 יחידת_נתונים_נסה תקן_קלט_נסה 파일보존시험
רשימת_בדיקות := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/קודמקור/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(רשימת_בדיקות)
build/변환완료: $(원문목록) כלים/מזהה_המרה.py
	mkdir -p build
	$(PYTHON) כלים/מזהה_המרה.py קודמקור build/קודמקור
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/קודמקור/구현/$*.c -o $@
build/מערכת_הפעלה_שיחות_טלפון.o: מחשב/מערכת_הפעלה_שיחות_טלפון.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/התחל_משתמש_תוכנית.o: מחשב/התחל_משתמש_תוכנית.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(אובייקט_קובץ_רשימה)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/התחל_משתמש_תוכנית.o build/libposix-kor.a ../compiler/משתמש_לקשר_ניווט.ld
	$(CC) $(CFLAGS) -c build/קודמקור/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/משתמש_לקשר_ניווט.ld -o $@ build/התחל_משתמש_תוכנית.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) כלים/המרה_נסה.py

.PHONY: clean
clean:
	rm -rf -- build
