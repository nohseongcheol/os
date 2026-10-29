PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
Quelltextliste := $(shell rg --files Quelltext)
umsetzungNamen := DateiEingabeAusgabe NetzbuchseEndpunkt ByteZeichenkette benutzerEintreten
objektDateiListe := $(addprefix build/,$(addsuffix .o,$(umsetzungNamen))) build/BetriebSystemAufrufliste.o
namenPrüfung := DateiABIPrüfung DatagrammPrüfung StandardEingabePrüfung DateiBewahrungPrüfung
listePrüfung := $(addprefix build/,$(addsuffix .elf,$(namenPrüfung)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/Quelltext/Kopfdateien
.PHONY: all test test-tools
all: build/libposix-kor.a $(listePrüfung)
build/umwandlungFertig: $(Quelltextliste) Werkzeuge/BezeichnerUmwandlung.py
	mkdir -p build
	$(PYTHON) Werkzeuge/BezeichnerUmwandlung.py Quelltext build/Quelltext
	touch $@
build/%.o: build/umwandlungFertig
	$(CC) $(CFLAGS) -c build/Quelltext/umsetzung/$*.c -o $@
build/BetriebSystemAufrufliste.o: maschine/BetriebSystemAufrufliste.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/benutzerProgrammStarten.o: maschine/benutzerProgrammStarten.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(objektDateiListe)
	$(AR) rcs $@ $^
build/%.elf: build/umwandlungFertig build/benutzerProgrammStarten.o build/libposix-kor.a ../compiler/benutzerBindenAnordnung.ld
	$(CC) $(CFLAGS) -c build/Quelltext/Prüfungen/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/benutzerBindenAnordnung.ld -o $@ build/benutzerProgrammStarten.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Werkzeuge/UmwandlungPrüfung.py

.PHONY: clean
clean:
	rm -rf -- build
