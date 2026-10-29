PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords remoto_CONNETTI
remote: build
	$(PYTHON) strumenti/Esegui_comando.py --remote --resolution $(RESOLUTION) $(ARGS)
remoto_CONNETTI: remote
test-remote: build
	$(PYTHON) strumenti/connessione_remota_test.py
test-passwords: build
	$(PYTHON) strumenti/password_durata_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter rete_Pila -I vendor/lwip/src/include prove/cablato_rete_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) strumenti/costruire.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) strumenti/COSL배포.py check
cosl-dist: build
	$(PYTHON) strumenti/Crea_foto.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) strumenti/COSL배포.py bundle
	$(PYTHON) strumenti/재연결시험.py
desktop: build
	$(PYTHON) strumenti/Esegui_comando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) strumenti/test_Shell.py
test-windows: build
	$(PYTHON) strumenti/test_Windows.py
test-swing: build
	$(PYTHON) strumenti/test_Swing.py
test-stream: build
	$(PYTHON) strumenti/test_Stream.py
test-ftp: build
	$(PYTHON) strumenti/test_FTP.py
test-elf: build
	$(PYTHON) strumenti/실행파일시험.py
test-examples: build
	$(PYTHON) strumenti/예제시험.py
network: build
	$(PYTHON) strumenti/Esegui_comando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) strumenti/코딩시험.py
test-desktop: build
	$(PYTHON) strumenti/test_PC.py
run: build
	$(PYTHON) strumenti/Esegui_comando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) strumenti/test_JVM.py
test: build test-compiler
	$(PYTHON) strumenti/한글입력시험.py
	$(PYTHON) strumenti/test_Shell.py
	$(PYTHON) strumenti/test_PC.py
	$(PYTHON) strumenti/test_Windows.py
	$(PYTHON) strumenti/test_Swing.py
	$(PYTHON) strumenti/test_Stream.py
	$(PYTHON) strumenti/코딩시험.py
	$(PYTHON) strumenti/test_JVM.py
	$(PYTHON) strumenti/부팅시험.py
	$(PYTHON) strumenti/test_aggregare.py
	$(PYTHON) strumenti/risoluzione_test.py
	$(PYTHON) strumenti/test_finestra_ridimensionamento.py
image: build
	$(PYTHON) strumenti/Crea_foto.py --resolution $(RESOLUTION)
	$(PYTHON) strumenti/esportare_SDK.py
sdk: build
	$(PYTHON) strumenti/esportare_SDK.py

.PHONY: 모두 costruire Esegui_comando prove comunicazione PC_Vista foto_VALORE kit_di_sviluppo
모두: all
costruire: build
Esegui_comando: run
prove: test
comunicazione: network
PC_Vista: desktop
foto_VALORE: image
kit_di_sviluppo: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) strumenti/부팅시험.py
test-remmina: build
	$(PYTHON) strumenti/원격한글시험.py
test-naming:
	$(PYTHON) strumenti/명명검사.py --C_Lingua
	$(PYTHON) strumenti/직접호출검사.py
	$(PYTHON) strumenti/fonte_rivedere.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) strumenti/test_aggregare.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) strumenti/risoluzione_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) strumenti/test_finestra_ridimensionamento.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) strumenti/schermata_aggiornare_test.py

.PHONY: test-system
test-system: build
	$(PYTHON) strumenti/test_Sistema_Strumenti.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) strumenti/실행계층점검.py

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
