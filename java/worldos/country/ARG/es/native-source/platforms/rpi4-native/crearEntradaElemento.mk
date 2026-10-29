PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords conectarRemoto
remote: build
	$(PYTHON) Herramientas/ejecutarComando.py --remote --resolution $(RESOLUTION) $(ARGS)
conectarRemoto: remote
test-remote: build
	$(PYTHON) Herramientas/PruebaConexiónRemoto.py
test-passwords: build
	$(PYTHON) Herramientas/PruebaLongitudContraseña.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter PilaRed -I vendor/lwip/src/include Pruebas/PruebaRedCableado.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Herramientas/construirSistema.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Herramientas/DistribuciónCOSL.py check
cosl-dist: build
	$(PYTHON) Herramientas/crearImagen.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Herramientas/DistribuciónCOSL.py bundle
	$(PYTHON) Herramientas/PruebaReconectar.py
desktop: build
	$(PYTHON) Herramientas/ejecutarComando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Herramientas/pruebaIntérpreteComandos.py
test-windows: build
	$(PYTHON) Herramientas/pruebaVentanas.py
test-swing: build
	$(PYTHON) Herramientas/pruebaSwing.py
test-stream: build
	$(PYTHON) Herramientas/pruebaFlujo.py
test-ftp: build
	$(PYTHON) Herramientas/pruebaFTP.py
test-elf: build
	$(PYTHON) Herramientas/pruebaELF.py
test-examples: build
	$(PYTHON) Herramientas/pruebaColecciónEjemplos.py
network: build
	$(PYTHON) Herramientas/ejecutarComando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Herramientas/pruebaCodificación.py
test-desktop: build
	$(PYTHON) Herramientas/pruebaEscritorio.py
run: build
	$(PYTHON) Herramientas/ejecutarComando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Herramientas/pruebaJVM.py
test: build test-compiler
	$(PYTHON) Herramientas/pruebaEntradaHangul.py
	$(PYTHON) Herramientas/pruebaIntérpreteComandos.py
	$(PYTHON) Herramientas/pruebaEscritorio.py
	$(PYTHON) Herramientas/pruebaVentanas.py
	$(PYTHON) Herramientas/pruebaSwing.py
	$(PYTHON) Herramientas/pruebaFlujo.py
	$(PYTHON) Herramientas/pruebaCodificación.py
	$(PYTHON) Herramientas/pruebaJVM.py
	$(PYTHON) Herramientas/PruebaArranque.py
	$(PYTHON) Herramientas/pruebaPaquete.py
	$(PYTHON) Herramientas/PruebaResolución.py
	$(PYTHON) Herramientas/pruebaRedimensionamientoVentana.py
image: build
	$(PYTHON) Herramientas/crearImagen.py --resolution $(RESOLUTION)
	$(PYTHON) Herramientas/sDKExportar.py
sdk: build
	$(PYTHON) Herramientas/sDKExportar.py

.PHONY: construirTodos construirSistema ejecutarComando Pruebas Comunicación vistaEscritorio valorImagen juegoHerramientasDesarrollo
construirTodos: all
construirSistema: build
ejecutarComando: run
Pruebas: test
Comunicación: network
vistaEscritorio: desktop
valorImagen: image
juegoHerramientasDesarrollo: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Herramientas/PruebaArranque.py
test-remmina: build
	$(PYTHON) Herramientas/pruebaRemmina.py
test-naming:
	$(PYTHON) Herramientas/comprobarDenominación.py --lenguaC
	$(PYTHON) Herramientas/comprobarLlamadasDirecto.py
	$(PYTHON) Herramientas/RevisiónExamenFuente.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Herramientas/pruebaPaquete.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Herramientas/PruebaResolución.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Herramientas/pruebaRedimensionamientoVentana.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Herramientas/PruebaActualizarPantalla.py

.PHONY: test-system
test-system: build
	$(PYTHON) Herramientas/pruebaHerramientasSistema.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Herramientas/ComprobacionesEntornoEjecución.py

.PHONY: clean
clean:
	# Keep device credentials and downloaded packages.
	@if test -d build/remote; then \
		find build/remote -mindepth 1 -maxdepth 1 ! -name access.json ! -name host-key.der -exec rm -rf -- {} +; \
	fi
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name remote ! -name pip-cache -exec rm -rf -- {} +; \
	fi
	rm -rf -- dist
