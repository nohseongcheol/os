PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ebe_dị̀anyā_JIKỌ
remote: build
	$(PYTHON) Ngwaọrụ/mee_nnyemiwu.py --remote --resolution $(RESOLUTION) $(ARGS)
ebe_dị̀anyā_JIKỌ: remote
test-remote: build
	$(PYTHON) Ngwaọrụ/원격접속시험.py
test-passwords: build
	$(PYTHON) Ngwaọrụ/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Netwọọkụ_ikpo -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Ngwaọrụ/wue_sistèm.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Ngwaọrụ/COSL배포.py check
cosl-dist: build
	$(PYTHON) Ngwaọrụ/mepụta_foto.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Ngwaọrụ/COSL배포.py bundle
	$(PYTHON) Ngwaọrụ/재연결시험.py
desktop: build
	$(PYTHON) Ngwaọrụ/mee_nnyemiwu.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Ngwaọrụ/셸시험.py
test-windows: build
	$(PYTHON) Ngwaọrụ/창시험.py
test-swing: build
	$(PYTHON) Ngwaọrụ/화면요소시험.py
test-stream: build
	$(PYTHON) Ngwaọrụ/흐름시험.py
test-ftp: build
	$(PYTHON) Ngwaọrụ/파일전송시험.py
test-elf: build
	$(PYTHON) Ngwaọrụ/실행파일시험.py
test-examples: build
	$(PYTHON) Ngwaọrụ/예제시험.py
network: build
	$(PYTHON) Ngwaọrụ/mee_nnyemiwu.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Ngwaọrụ/코딩시험.py
test-desktop: build
	$(PYTHON) Ngwaọrụ/바탕화면시험.py
run: build
	$(PYTHON) Ngwaọrụ/mee_nnyemiwu.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Ngwaọrụ/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Ngwaọrụ/한글입력시험.py
	$(PYTHON) Ngwaọrụ/셸시험.py
	$(PYTHON) Ngwaọrụ/바탕화면시험.py
	$(PYTHON) Ngwaọrụ/창시험.py
	$(PYTHON) Ngwaọrụ/화면요소시험.py
	$(PYTHON) Ngwaọrụ/흐름시험.py
	$(PYTHON) Ngwaọrụ/코딩시험.py
	$(PYTHON) Ngwaọrụ/자바가상기계시험.py
	$(PYTHON) Ngwaọrụ/부팅시험.py
	$(PYTHON) Ngwaọrụ/꾸러미시험.py
	$(PYTHON) Ngwaọrụ/해상도시험.py
	$(PYTHON) Ngwaọrụ/창크기시험.py
image: build
	$(PYTHON) Ngwaọrụ/mepụta_foto.py --resolution $(RESOLUTION)
	$(PYTHON) Ngwaọrụ/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Ngwaọrụ/개발꾸러미내보내기.py

.PHONY: 모두 wue_sistèm mee_nnyemiwu 시험 통신 desktọpụ_lèe foto_valuu 개발꾸러미
모두: all
wue_sistèm: build
mee_nnyemiwu: run
시험: test
통신: network
desktọpụ_lèe: desktop
foto_valuu: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Ngwaọrụ/부팅시험.py
test-remmina: build
	$(PYTHON) Ngwaọrụ/원격한글시험.py
test-naming:
	$(PYTHON) Ngwaọrụ/명명검사.py --시언어
	$(PYTHON) Ngwaọrụ/직접호출검사.py
	$(PYTHON) Ngwaọrụ/ebensìbịa_Nyocha.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Ngwaọrụ/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Ngwaọrụ/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Ngwaọrụ/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Ngwaọrụ/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Ngwaọrụ/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Ngwaọrụ/실행계층점검.py

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
