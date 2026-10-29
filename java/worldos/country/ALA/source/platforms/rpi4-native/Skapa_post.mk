PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords fjärr_ANSLUT
remote: build
	$(PYTHON) verktyg/köra_kommando.py --remote --resolution $(RESOLUTION) $(ARGS)
fjärr_ANSLUT: remote
test-remote: build
	$(PYTHON) verktyg/fjärranslutning_test.py
test-passwords: build
	$(PYTHON) verktyg/lösenord_längd_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter nätverk_Stack -I vendor/lwip/src/include tester/kabelansluten_nätverk_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) verktyg/version_System.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) verktyg/COSL배포.py check
cosl-dist: build
	$(PYTHON) verktyg/Skapa_BILD.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) verktyg/COSL배포.py bundle
	$(PYTHON) verktyg/재연결시험.py
desktop: build
	$(PYTHON) verktyg/köra_kommando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) verktyg/test_Shell.py
test-windows: build
	$(PYTHON) verktyg/test_Windows.py
test-swing: build
	$(PYTHON) verktyg/test_Swing.py
test-stream: build
	$(PYTHON) verktyg/test_flöde.py
test-ftp: build
	$(PYTHON) verktyg/test_FTP.py
test-elf: build
	$(PYTHON) verktyg/실행파일시험.py
test-examples: build
	$(PYTHON) verktyg/예제시험.py
network: build
	$(PYTHON) verktyg/köra_kommando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) verktyg/코딩시험.py
test-desktop: build
	$(PYTHON) verktyg/test_Dator.py
run: build
	$(PYTHON) verktyg/köra_kommando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) verktyg/test_JVM.py
test: build test-compiler
	$(PYTHON) verktyg/한글입력시험.py
	$(PYTHON) verktyg/test_Shell.py
	$(PYTHON) verktyg/test_Dator.py
	$(PYTHON) verktyg/test_Windows.py
	$(PYTHON) verktyg/test_Swing.py
	$(PYTHON) verktyg/test_flöde.py
	$(PYTHON) verktyg/코딩시험.py
	$(PYTHON) verktyg/test_JVM.py
	$(PYTHON) verktyg/부팅시험.py
	$(PYTHON) verktyg/test_bunt.py
	$(PYTHON) verktyg/upplösning_test.py
	$(PYTHON) verktyg/창크기시험.py
image: build
	$(PYTHON) verktyg/Skapa_BILD.py --resolution $(RESOLUTION)
	$(PYTHON) verktyg/exportera_SDK.py
sdk: build
	$(PYTHON) verktyg/exportera_SDK.py

.PHONY: 모두 version_System köra_kommando tester kommunikation Dator_vy BILD_värde development_kit
모두: all
version_System: build
köra_kommando: run
tester: test
kommunikation: network
Dator_vy: desktop
BILD_värde: image
development_kit: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) verktyg/부팅시험.py
test-remmina: build
	$(PYTHON) verktyg/원격한글시험.py
test-naming:
	$(PYTHON) verktyg/명명검사.py --C_Språk
	$(PYTHON) verktyg/직접호출검사.py
	$(PYTHON) verktyg/källa_granska.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) verktyg/test_bunt.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) verktyg/upplösning_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) verktyg/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) verktyg/skärmbild_uppdatera_test.py

.PHONY: test-system
test-system: build
	$(PYTHON) verktyg/test_System_Verktyg.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) verktyg/실행계층점검.py

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
