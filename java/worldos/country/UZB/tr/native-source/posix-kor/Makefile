PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files kaynakKod)
구현이름 := Dosya_G_Ç yuva_uç_nokta bayt_dize kullanıcı_girmek
nesne_dosyası_Liste := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/işletim_sistemi_Çağrılar.o
시험이름 := Dosya_ABI_test veri_birimi_test STDIN_test 파일보존시험
test_listesi := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/kaynakKod/bildirimler
.PHONY: all test test-tools
all: build/libposix-kor.a $(test_listesi)
build/변환완료: $(원문목록) araçlar/tanımlayıcı_dönüştürme.py
	mkdir -p build
	$(PYTHON) araçlar/tanımlayıcı_dönüştürme.py kaynakKod build/kaynakKod
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/kaynakKod/gerçekleme/$*.c -o $@
build/işletim_sistemi_Çağrılar.o: makine/işletim_sistemi_Çağrılar.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/Start_kullanıcı_program.o: makine/Start_kullanıcı_program.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(nesne_dosyası_Liste)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/Start_kullanıcı_program.o build/libposix-kor.a ../compiler/kullanıcı_köprü_Düzen.ld
	$(CC) $(CFLAGS) -c build/kaynakKod/sınamalar/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/kullanıcı_köprü_Düzen.ld -o $@ build/Start_kullanıcı_program.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) araçlar/dönüştürme_test.py

.PHONY: clean
clean:
	rm -rf -- build
