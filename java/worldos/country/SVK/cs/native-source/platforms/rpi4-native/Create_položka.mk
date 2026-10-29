PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords vzdálený_spojit
remote: build
	$(PYTHON) nástroje/Provést_příkaz.py --remote --resolution $(RESOLUTION) $(ARGS)
vzdálený_spojit: remote
test-remote: build
	$(PYTHON) nástroje/vzdálené_připojení_test.py
test-passwords: build
	$(PYTHON) nástroje/heslo_délka_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter síť_Štos -I vendor/lwip/src/include zkoušky/drátový_síť_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) nástroje/BLD_Systém.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) nástroje/COSL배포.py check
cosl-dist: build
	$(PYTHON) nástroje/Create_image.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) nástroje/COSL배포.py bundle
	$(PYTHON) nástroje/재연결시험.py
desktop: build
	$(PYTHON) nástroje/Provést_příkaz.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) nástroje/test_prostředí.py
test-windows: build
	$(PYTHON) nástroje/test_Windows.py
test-swing: build
	$(PYTHON) nástroje/test_Swing.py
test-stream: build
	$(PYTHON) nástroje/test_tok.py
test-ftp: build
	$(PYTHON) nástroje/test_protokol_FTP.py
test-elf: build
	$(PYTHON) nástroje/실행파일시험.py
test-examples: build
	$(PYTHON) nástroje/예제시험.py
network: build
	$(PYTHON) nástroje/Provést_příkaz.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) nástroje/코딩시험.py
test-desktop: build
	$(PYTHON) nástroje/test_Plocha.py
run: build
	$(PYTHON) nástroje/Provést_příkaz.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) nástroje/test_JVM.py
test: build test-compiler
	$(PYTHON) nástroje/한글입력시험.py
	$(PYTHON) nástroje/test_prostředí.py
	$(PYTHON) nástroje/test_Plocha.py
	$(PYTHON) nástroje/test_Windows.py
	$(PYTHON) nástroje/test_Swing.py
	$(PYTHON) nástroje/test_tok.py
	$(PYTHON) nástroje/코딩시험.py
	$(PYTHON) nástroje/test_JVM.py
	$(PYTHON) nástroje/부팅시험.py
	$(PYTHON) nástroje/test_sada.py
	$(PYTHON) nástroje/řešení_test.py
	$(PYTHON) nástroje/test_okno_změna_velikosti.py
image: build
	$(PYTHON) nástroje/Create_image.py --resolution $(RESOLUTION)
	$(PYTHON) nástroje/exportovat_sada_SDK.py
sdk: build
	$(PYTHON) nástroje/exportovat_sada_SDK.py

.PHONY: 모두 BLD_Systém Provést_příkaz zkoušky komunikace Plocha_pohled image_HODNOTA Development_Kit
모두: all
BLD_Systém: build
Provést_příkaz: run
zkoušky: test
komunikace: network
Plocha_pohled: desktop
image_HODNOTA: image
Development_Kit: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) nástroje/부팅시험.py
test-remmina: build
	$(PYTHON) nástroje/원격한글시험.py
test-naming:
	$(PYTHON) nástroje/명명검사.py --C_Jazyk
	$(PYTHON) nástroje/직접호출검사.py
	$(PYTHON) nástroje/zdroj_revize.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) nástroje/test_sada.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) nástroje/řešení_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) nástroje/test_okno_změna_velikosti.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) nástroje/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) nástroje/test_Systém_Nástroje.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) nástroje/실행계층점검.py

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
