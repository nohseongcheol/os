PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ekstern_KOBLE_TIL
remote: build
	$(PYTHON) Verktøy/Utfør_kommando.py --remote --resolution $(RESOLUTION) $(ARGS)
ekstern_KOBLE_TIL: remote
test-remote: build
	$(PYTHON) Verktøy/ekstern_tilkobling_test.py
test-passwords: build
	$(PYTHON) Verktøy/passord_lengde_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter nettverk_stakk -I vendor/lwip/src/include 시험/kabelbasert_nettverk_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Verktøy/bygg_System.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Verktøy/COSL배포.py check
cosl-dist: build
	$(PYTHON) Verktøy/åpne_BILDE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Verktøy/COSL배포.py bundle
	$(PYTHON) Verktøy/재연결시험.py
desktop: build
	$(PYTHON) Verktøy/Utfør_kommando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Verktøy/test_Shell.py
test-windows: build
	$(PYTHON) Verktøy/test_Windows.py
test-swing: build
	$(PYTHON) Verktøy/test_Swing.py
test-stream: build
	$(PYTHON) Verktøy/test_strøm.py
test-ftp: build
	$(PYTHON) Verktøy/test_FTP.py
test-elf: build
	$(PYTHON) Verktøy/실행파일시험.py
test-examples: build
	$(PYTHON) Verktøy/예제시험.py
network: build
	$(PYTHON) Verktøy/Utfør_kommando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Verktøy/코딩시험.py
test-desktop: build
	$(PYTHON) Verktøy/test_stasjonær.py
run: build
	$(PYTHON) Verktøy/Utfør_kommando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Verktøy/test_JVM.py
test: build test-compiler
	$(PYTHON) Verktøy/한글입력시험.py
	$(PYTHON) Verktøy/test_Shell.py
	$(PYTHON) Verktøy/test_stasjonær.py
	$(PYTHON) Verktøy/test_Windows.py
	$(PYTHON) Verktøy/test_Swing.py
	$(PYTHON) Verktøy/test_strøm.py
	$(PYTHON) Verktøy/코딩시험.py
	$(PYTHON) Verktøy/test_JVM.py
	$(PYTHON) Verktøy/부팅시험.py
	$(PYTHON) Verktøy/test_bunt.py
	$(PYTHON) Verktøy/oppløsning_test.py
	$(PYTHON) Verktøy/창크기시험.py
image: build
	$(PYTHON) Verktøy/åpne_BILDE.py --resolution $(RESOLUTION)
	$(PYTHON) Verktøy/eksportere_SDK.py
sdk: build
	$(PYTHON) Verktøy/eksportere_SDK.py

.PHONY: 모두 bygg_System Utfør_kommando 시험 통신 stasjonær_vise BILDE_VERDI utviklingspakke
모두: all
bygg_System: build
Utfør_kommando: run
시험: test
통신: network
stasjonær_vise: desktop
BILDE_VERDI: image
utviklingspakke: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Verktøy/부팅시험.py
test-remmina: build
	$(PYTHON) Verktøy/원격한글시험.py
test-naming:
	$(PYTHON) Verktøy/명명검사.py --C_Språk
	$(PYTHON) Verktøy/직접호출검사.py
	$(PYTHON) Verktøy/kilde_anmeldelse.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Verktøy/test_bunt.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Verktøy/oppløsning_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Verktøy/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Verktøy/skjermbilde_oppdatere_test.py

.PHONY: test-system
test-system: build
	$(PYTHON) Verktøy/test_System_Verktøy.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Verktøy/실행계층점검.py

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
