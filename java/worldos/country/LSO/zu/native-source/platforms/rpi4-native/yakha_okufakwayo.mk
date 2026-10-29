PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords kude_xhuma
remote: build
	$(PYTHON) Amathuluzi/yenza_umyalo.py --remote --resolution $(RESOLUTION) $(ARGS)
kude_xhuma: remote
test-remote: build
	$(PYTHON) Amathuluzi/원격접속시험.py
test-passwords: build
	$(PYTHON) Amathuluzi/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter iNethiwekhi_Isitaki -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Amathuluzi/akha_isistimu.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Amathuluzi/COSL배포.py check
cosl-dist: build
	$(PYTHON) Amathuluzi/yakha_isithombe.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Amathuluzi/COSL배포.py bundle
	$(PYTHON) Amathuluzi/재연결시험.py
desktop: build
	$(PYTHON) Amathuluzi/yenza_umyalo.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Amathuluzi/셸시험.py
test-windows: build
	$(PYTHON) Amathuluzi/창시험.py
test-swing: build
	$(PYTHON) Amathuluzi/화면요소시험.py
test-stream: build
	$(PYTHON) Amathuluzi/흐름시험.py
test-ftp: build
	$(PYTHON) Amathuluzi/파일전송시험.py
test-elf: build
	$(PYTHON) Amathuluzi/실행파일시험.py
test-examples: build
	$(PYTHON) Amathuluzi/예제시험.py
network: build
	$(PYTHON) Amathuluzi/yenza_umyalo.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Amathuluzi/코딩시험.py
test-desktop: build
	$(PYTHON) Amathuluzi/바탕화면시험.py
run: build
	$(PYTHON) Amathuluzi/yenza_umyalo.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Amathuluzi/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Amathuluzi/한글입력시험.py
	$(PYTHON) Amathuluzi/셸시험.py
	$(PYTHON) Amathuluzi/바탕화면시험.py
	$(PYTHON) Amathuluzi/창시험.py
	$(PYTHON) Amathuluzi/화면요소시험.py
	$(PYTHON) Amathuluzi/흐름시험.py
	$(PYTHON) Amathuluzi/코딩시험.py
	$(PYTHON) Amathuluzi/자바가상기계시험.py
	$(PYTHON) Amathuluzi/부팅시험.py
	$(PYTHON) Amathuluzi/꾸러미시험.py
	$(PYTHON) Amathuluzi/해상도시험.py
	$(PYTHON) Amathuluzi/창크기시험.py
image: build
	$(PYTHON) Amathuluzi/yakha_isithombe.py --resolution $(RESOLUTION)
	$(PYTHON) Amathuluzi/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Amathuluzi/개발꾸러미내보내기.py

.PHONY: 모두 akha_isistimu yenza_umyalo 시험 통신 ideskithophu_buka isithombe_inani 개발꾸러미
모두: all
akha_isistimu: build
yenza_umyalo: run
시험: test
통신: network
ideskithophu_buka: desktop
isithombe_inani: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Amathuluzi/부팅시험.py
test-remmina: build
	$(PYTHON) Amathuluzi/원격한글시험.py
test-naming:
	$(PYTHON) Amathuluzi/명명검사.py --시언어
	$(PYTHON) Amathuluzi/직접호출검사.py
	$(PYTHON) Amathuluzi/umthombo_isibuyekezo.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Amathuluzi/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Amathuluzi/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Amathuluzi/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Amathuluzi/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Amathuluzi/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Amathuluzi/실행계층점검.py

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
