PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords uzakdan_Birikme
remote: build
	$(PYTHON) Gurallar/ýerine_ýetir_buýruk.py --remote --resolution $(RESOLUTION) $(ARGS)
uzakdan_Birikme: remote
test-remote: build
	$(PYTHON) Gurallar/원격접속시험.py
test-passwords: build
	$(PYTHON) Gurallar/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Tor_Desse -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Gurallar/düz_ulgam.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Gurallar/COSL배포.py check
cosl-dist: build
	$(PYTHON) Gurallar/döretmek_surat.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Gurallar/COSL배포.py bundle
	$(PYTHON) Gurallar/재연결시험.py
desktop: build
	$(PYTHON) Gurallar/ýerine_ýetir_buýruk.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Gurallar/셸시험.py
test-windows: build
	$(PYTHON) Gurallar/창시험.py
test-swing: build
	$(PYTHON) Gurallar/화면요소시험.py
test-stream: build
	$(PYTHON) Gurallar/흐름시험.py
test-ftp: build
	$(PYTHON) Gurallar/파일전송시험.py
test-elf: build
	$(PYTHON) Gurallar/실행파일시험.py
test-examples: build
	$(PYTHON) Gurallar/예제시험.py
network: build
	$(PYTHON) Gurallar/ýerine_ýetir_buýruk.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Gurallar/코딩시험.py
test-desktop: build
	$(PYTHON) Gurallar/바탕화면시험.py
run: build
	$(PYTHON) Gurallar/ýerine_ýetir_buýruk.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Gurallar/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Gurallar/한글입력시험.py
	$(PYTHON) Gurallar/셸시험.py
	$(PYTHON) Gurallar/바탕화면시험.py
	$(PYTHON) Gurallar/창시험.py
	$(PYTHON) Gurallar/화면요소시험.py
	$(PYTHON) Gurallar/흐름시험.py
	$(PYTHON) Gurallar/코딩시험.py
	$(PYTHON) Gurallar/자바가상기계시험.py
	$(PYTHON) Gurallar/부팅시험.py
	$(PYTHON) Gurallar/꾸러미시험.py
	$(PYTHON) Gurallar/해상도시험.py
	$(PYTHON) Gurallar/창크기시험.py
image: build
	$(PYTHON) Gurallar/döretmek_surat.py --resolution $(RESOLUTION)
	$(PYTHON) Gurallar/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Gurallar/개발꾸러미내보내기.py

.PHONY: 모두 düz_ulgam ýerine_ýetir_buýruk 시험 통신 iş_stoly_görkez surat_baha 개발꾸러미
모두: all
düz_ulgam: build
ýerine_ýetir_buýruk: run
시험: test
통신: network
iş_stoly_görkez: desktop
surat_baha: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Gurallar/부팅시험.py
test-remmina: build
	$(PYTHON) Gurallar/원격한글시험.py
test-naming:
	$(PYTHON) Gurallar/명명검사.py --시언어
	$(PYTHON) Gurallar/직접호출검사.py
	$(PYTHON) Gurallar/gor_gözden_geçiriş.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Gurallar/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Gurallar/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Gurallar/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Gurallar/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Gurallar/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Gurallar/실행계층점검.py

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
