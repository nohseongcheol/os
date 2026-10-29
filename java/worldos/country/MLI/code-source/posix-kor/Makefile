PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
ListeSources := $(shell rg --files source)
nomsRéalisation := SortieEntréeFichier ExtrémitéPriseRéseau ChaîneOctet entrerUtilisateur
listeFichierObjet := $(addprefix build/,$(addsuffix .o,$(nomsRéalisation))) build/AppelsSystèmeExploitation.o
testNoms := TestABIFichier TestDatagramme TestEntréeStandard TestPréservationFichier
testListe := $(addprefix build/,$(addsuffix .elf,$(testNoms)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/source/Entêtes
.PHONY: all test test-tools
all: build/libposix-kor.a $(testListe)
build/terminéConversion: $(ListeSources) Outils/ConversionIdentificateur.py
	mkdir -p build
	$(PYTHON) Outils/ConversionIdentificateur.py source build/source
	touch $@
build/%.o: build/terminéConversion
	$(CC) $(CFLAGS) -c build/source/réalisation/$*.c -o $@
build/AppelsSystèmeExploitation.o: machine/AppelsSystèmeExploitation.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/démarrerProgrammeUtilisateur.o: machine/démarrerProgrammeUtilisateur.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(listeFichierObjet)
	$(AR) rcs $@ $^
build/%.elf: build/terminéConversion build/démarrerProgrammeUtilisateur.o build/libposix-kor.a ../compiler/dispositionLierUtilisateur.ld
	$(CC) $(CFLAGS) -c build/source/Tests/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/dispositionLierUtilisateur.ld -o $@ build/démarrerProgrammeUtilisateur.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Outils/TestConversion.py

.PHONY: clean
clean:
	rm -rf -- build
