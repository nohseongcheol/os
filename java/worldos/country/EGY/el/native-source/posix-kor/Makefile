PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ΠΗΓΗ)
구현이름 := Αρχείο_είσοδος_έξοδος υποδοχή_τελικό_σημείο 바이트문자열 χρήστης_εισάγω
αντικείμενο_λίστα_αρχείων := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/λειτουργικό_σύστημα_Κλήσεις.o
시험이름 := 파일규약시험 αυτοδύναμο_πακέτο_δοκιμή τυπική_είσοδος_δοκιμή 파일보존시험
λίστα_δοκιμών := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ΠΗΓΗ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(λίστα_δοκιμών)
build/변환완료: $(원문목록) Εργαλεία/αναγνωριστικό_μετατροπή.py
	mkdir -p build
	$(PYTHON) Εργαλεία/αναγνωριστικό_μετατροπή.py ΠΗΓΗ build/ΠΗΓΗ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ΠΗΓΗ/구현/$*.c -o $@
build/λειτουργικό_σύστημα_Κλήσεις.o: υπολογιστής_5eb260fa/λειτουργικό_σύστημα_Κλήσεις.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/αρχή_χρήστης_εφαρμογή.o: υπολογιστής_5eb260fa/αρχή_χρήστης_εφαρμογή.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(αντικείμενο_λίστα_αρχείων)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/αρχή_χρήστης_εφαρμογή.o build/libposix-kor.a ../compiler/χρήστης_συνδέω_Διάταξη.ld
	$(CC) $(CFLAGS) -c build/ΠΗΓΗ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/χρήστης_συνδέω_Διάταξη.ld -o $@ build/αρχή_χρήστης_εφαρμογή.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Εργαλεία/μετατροπή_δοκιμή.py

.PHONY: clean
clean:
	rm -rf -- build
