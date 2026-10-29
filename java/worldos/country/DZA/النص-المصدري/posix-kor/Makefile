PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files مصدر)
구현이름 := ملف_إدخال_إخراج مأخذ_التوصيل_المشارك بايت_سلسلة مستخدم_يدخل
عنصر_ملف_قائمة := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/نظام_تشغيل_المكالمات.o
시험이름 := 파일규약시험 مخطط_بيانات_يختبر إدخال_قياسي_يختبر 파일보존시험
قائمة_الاخبارات := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/مصدر/تصريحات
.PHONY: all test test-tools
all: build/libposix-kor.a $(قائمة_الاخبارات)
build/변환완료: $(원문목록) أدوات/معرف_تحويل.py
	mkdir -p build
	$(PYTHON) أدوات/معرف_تحويل.py مصدر build/مصدر
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/مصدر/구현/$*.c -o $@
build/نظام_تشغيل_المكالمات.o: جهاز/نظام_تشغيل_المكالمات.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/بدء_مستخدم_تطبيق.o: جهاز/بدء_مستخدم_تطبيق.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(عنصر_ملف_قائمة)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/بدء_مستخدم_تطبيق.o build/libposix-kor.a ../compiler/مستخدم_ربط_تخطيط.ld
	$(CC) $(CFLAGS) -c build/مصدر/اختبارات/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/مستخدم_ربط_تخطيط.ld -o $@ build/بدء_مستخدم_تطبيق.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) أدوات/تحويل_يختبر.py

.PHONY: clean
clean:
	rm -rf -- build
