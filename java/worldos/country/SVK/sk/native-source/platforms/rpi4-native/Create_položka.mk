PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords vzdialený_spojiť
remote: build
	$(PYTHON) Nástroje/Vykonať_príkaz.py --remote --resolution $(RESOLUTION) $(ARGS)
vzdialený_spojiť: remote
test-remote: build
	$(PYTHON) Nástroje/vzdialené_pripojenie_test.py
test-passwords: build
	$(PYTHON) Nástroje/heslo_dĺžka_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter sieť_Vrstvy -I vendor/lwip/src/include 시험/drôtový_sieť_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Nástroje/zostava_systém.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Nástroje/COSL배포.py check
cosl-dist: build
	$(PYTHON) Nástroje/Create_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Nástroje/COSL배포.py bundle
	$(PYTHON) Nástroje/재연결시험.py
desktop: build
	$(PYTHON) Nástroje/Vykonať_príkaz.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Nástroje/셸시험.py
test-windows: build
	$(PYTHON) Nástroje/test_Windows.py
test-swing: build
	$(PYTHON) Nástroje/test_Swing.py
test-stream: build
	$(PYTHON) Nástroje/test_Stream.py
test-ftp: build
	$(PYTHON) Nástroje/test_FTP.py
test-elf: build
	$(PYTHON) Nástroje/실행파일시험.py
test-examples: build
	$(PYTHON) Nástroje/예제시험.py
network: build
	$(PYTHON) Nástroje/Vykonať_príkaz.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Nástroje/코딩시험.py
test-desktop: build
	$(PYTHON) Nástroje/test_počítač.py
run: build
	$(PYTHON) Nástroje/Vykonať_príkaz.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Nástroje/test_virtuálny_počítač_Java.py
test: build test-compiler
	$(PYTHON) Nástroje/한글입력시험.py
	$(PYTHON) Nástroje/셸시험.py
	$(PYTHON) Nástroje/test_počítač.py
	$(PYTHON) Nástroje/test_Windows.py
	$(PYTHON) Nástroje/test_Swing.py
	$(PYTHON) Nástroje/test_Stream.py
	$(PYTHON) Nástroje/코딩시험.py
	$(PYTHON) Nástroje/test_virtuálny_počítač_Java.py
	$(PYTHON) Nástroje/부팅시험.py
	$(PYTHON) Nástroje/test_zväzok.py
	$(PYTHON) Nástroje/rozlíšenie_test.py
	$(PYTHON) Nástroje/창크기시험.py
image: build
	$(PYTHON) Nástroje/Create_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Nástroje/exportovať_SDK.py
sdk: build
	$(PYTHON) Nástroje/exportovať_SDK.py

.PHONY: 모두 zostava_systém Vykonať_príkaz 시험 통신 počítač_zobraziť IMAGE_VALUE Development_Kit
모두: all
zostava_systém: build
Vykonať_príkaz: run
시험: test
통신: network
počítač_zobraziť: desktop
IMAGE_VALUE: image
Development_Kit: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Nástroje/부팅시험.py
test-remmina: build
	$(PYTHON) Nástroje/원격한글시험.py
test-naming:
	$(PYTHON) Nástroje/명명검사.py --C_Jazyky
	$(PYTHON) Nástroje/직접호출검사.py
	$(PYTHON) Nástroje/zdroj_recenzia.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Nástroje/test_zväzok.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Nástroje/rozlíšenie_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Nástroje/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Nástroje/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Nástroje/test_systém_Nástroje.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Nástroje/실행계층점검.py

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
