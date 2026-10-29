PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files broncode)
구현이름 := Bestand_I_O socket_eindpunt byte_tekenreeks gebruiker_invoeren
object_bestandslijst := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/besturingssysteem_Oproepen.o
시험이름 := 파일규약시험 datagram_test STDIN_test 파일보존시험
test_Lijst := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/broncode/declaraties
.PHONY: all test test-tools
all: build/libposix-kor.a $(test_Lijst)
build/변환완료: $(원문목록) hulpmiddelen/id_omzetten.py
	mkdir -p build
	$(PYTHON) hulpmiddelen/id_omzetten.py broncode build/broncode
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/broncode/implementatie/$*.c -o $@
build/besturingssysteem_Oproepen.o: machine/besturingssysteem_Oproepen.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/START_gebruiker_app.o: machine/START_gebruiker_app.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(object_bestandslijst)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/START_gebruiker_app.o build/libposix-kor.a ../compiler/gebruiker_link_Indeling.ld
	$(CC) $(CFLAGS) -c build/broncode/tests/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/gebruiker_link_Indeling.ld -o $@ build/START_gebruiker_app.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) hulpmiddelen/omzetten_test.py

.PHONY: clean
clean:
	rm -rf -- build
