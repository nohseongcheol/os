PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
ListaFuentes := $(shell rg --files fuente)
nombresImplementación := SalidaEntradaArchivo ExtremoConectorRed CadenaByte entrarUsuario
listaArchivoObjeto := $(addprefix build/,$(addsuffix .o,$(nombresImplementación))) build/LlamadasSistemaOperación.o
pruebaNombres := PruebaABIArchivo PruebaDatagrama PruebaEntradaEstándar PruebaPreservaciónArchivo
pruebaLista := $(addprefix build/,$(addsuffix .elf,$(pruebaNombres)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/fuente/Encabezados
.PHONY: all test test-tools
all: build/libposix-kor.a $(pruebaLista)
build/terminadoConversión: $(ListaFuentes) Herramientas/ConversiónIdentificador.py
	mkdir -p build
	$(PYTHON) Herramientas/ConversiónIdentificador.py fuente build/fuente
	touch $@
build/%.o: build/terminadoConversión
	$(CC) $(CFLAGS) -c build/fuente/implementación/$*.c -o $@
build/LlamadasSistemaOperación.o: máquina/LlamadasSistemaOperación.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/iniciarProgramaUsuario.o: máquina/iniciarProgramaUsuario.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(listaArchivoObjeto)
	$(AR) rcs $@ $^
build/%.elf: build/terminadoConversión build/iniciarProgramaUsuario.o build/libposix-kor.a ../compiler/disposiciónEnlazarUsuario.ld
	$(CC) $(CFLAGS) -c build/fuente/Pruebas/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/disposiciónEnlazarUsuario.ld -o $@ build/iniciarProgramaUsuario.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) Herramientas/PruebaConversión.py

.PHONY: clean
clean:
	rm -rf -- build
