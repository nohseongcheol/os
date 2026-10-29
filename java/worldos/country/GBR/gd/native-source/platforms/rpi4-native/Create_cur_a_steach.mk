PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords cian_CONNECT
remote: build
	$(PYTHON) innealan/gnìomhaich_àithne.py --remote --resolution $(RESOLUTION) $(ARGS)
cian_CONNECT: remote
test-remote: build
	$(PYTHON) innealan/원격접속시험.py
test-passwords: build
	$(PYTHON) innealan/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter lìonra_stac -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) innealan/tog_siostam.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) innealan/COSL배포.py check
cosl-dist: build
	$(PYTHON) innealan/Create_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) innealan/COSL배포.py bundle
	$(PYTHON) innealan/재연결시험.py
desktop: build
	$(PYTHON) innealan/gnìomhaich_àithne.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) innealan/셸시험.py
test-windows: build
	$(PYTHON) innealan/창시험.py
test-swing: build
	$(PYTHON) innealan/화면요소시험.py
test-stream: build
	$(PYTHON) innealan/흐름시험.py
test-ftp: build
	$(PYTHON) innealan/파일전송시험.py
test-elf: build
	$(PYTHON) innealan/실행파일시험.py
test-examples: build
	$(PYTHON) innealan/예제시험.py
network: build
	$(PYTHON) innealan/gnìomhaich_àithne.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) innealan/코딩시험.py
test-desktop: build
	$(PYTHON) innealan/바탕화면시험.py
run: build
	$(PYTHON) innealan/gnìomhaich_àithne.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) innealan/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) innealan/한글입력시험.py
	$(PYTHON) innealan/셸시험.py
	$(PYTHON) innealan/바탕화면시험.py
	$(PYTHON) innealan/창시험.py
	$(PYTHON) innealan/화면요소시험.py
	$(PYTHON) innealan/흐름시험.py
	$(PYTHON) innealan/코딩시험.py
	$(PYTHON) innealan/자바가상기계시험.py
	$(PYTHON) innealan/부팅시험.py
	$(PYTHON) innealan/꾸러미시험.py
	$(PYTHON) innealan/해상도시험.py
	$(PYTHON) innealan/창크기시험.py
image: build
	$(PYTHON) innealan/Create_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) innealan/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) innealan/개발꾸러미내보내기.py

.PHONY: 모두 tog_siostam gnìomhaich_àithne 시험 통신 deasg_seall IMAGE_VALUE 개발꾸러미
모두: all
tog_siostam: build
gnìomhaich_àithne: run
시험: test
통신: network
deasg_seall: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) innealan/부팅시험.py
test-remmina: build
	$(PYTHON) innealan/원격한글시험.py
test-naming:
	$(PYTHON) innealan/명명검사.py --시언어
	$(PYTHON) innealan/직접호출검사.py
	$(PYTHON) innealan/tùs_lèirmheas.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) innealan/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) innealan/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) innealan/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) innealan/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) innealan/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) innealan/실행계층점검.py

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
