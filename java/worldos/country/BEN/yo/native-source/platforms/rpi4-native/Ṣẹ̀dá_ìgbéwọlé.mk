PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords Ìjìnnà_SOMỌ́
remote: build
	$(PYTHON) Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py --remote --resolution $(RESOLUTION) $(ARGS)
Ìjìnnà_SOMỌ́: remote
test-remote: build
	$(PYTHON) Àwọn_irinṣẹ́/원격접속시험.py
test-passwords: build
	$(PYTHON) Àwọn_irinṣẹ́/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Alásopọ̀_kójọ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Àwọn_irinṣẹ́/àtòpọ̀_ètò.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Àwọn_irinṣẹ́/COSL배포.py check
cosl-dist: build
	$(PYTHON) Àwọn_irinṣẹ́/Ṣẹ̀dá_àwòrán.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Àwọn_irinṣẹ́/COSL배포.py bundle
	$(PYTHON) Àwọn_irinṣẹ́/재연결시험.py
desktop: build
	$(PYTHON) Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Àwọn_irinṣẹ́/셸시험.py
test-windows: build
	$(PYTHON) Àwọn_irinṣẹ́/창시험.py
test-swing: build
	$(PYTHON) Àwọn_irinṣẹ́/화면요소시험.py
test-stream: build
	$(PYTHON) Àwọn_irinṣẹ́/흐름시험.py
test-ftp: build
	$(PYTHON) Àwọn_irinṣẹ́/파일전송시험.py
test-elf: build
	$(PYTHON) Àwọn_irinṣẹ́/실행파일시험.py
test-examples: build
	$(PYTHON) Àwọn_irinṣẹ́/예제시험.py
network: build
	$(PYTHON) Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Àwọn_irinṣẹ́/코딩시험.py
test-desktop: build
	$(PYTHON) Àwọn_irinṣẹ́/바탕화면시험.py
run: build
	$(PYTHON) Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Àwọn_irinṣẹ́/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Àwọn_irinṣẹ́/한글입력시험.py
	$(PYTHON) Àwọn_irinṣẹ́/셸시험.py
	$(PYTHON) Àwọn_irinṣẹ́/바탕화면시험.py
	$(PYTHON) Àwọn_irinṣẹ́/창시험.py
	$(PYTHON) Àwọn_irinṣẹ́/화면요소시험.py
	$(PYTHON) Àwọn_irinṣẹ́/흐름시험.py
	$(PYTHON) Àwọn_irinṣẹ́/코딩시험.py
	$(PYTHON) Àwọn_irinṣẹ́/자바가상기계시험.py
	$(PYTHON) Àwọn_irinṣẹ́/부팅시험.py
	$(PYTHON) Àwọn_irinṣẹ́/꾸러미시험.py
	$(PYTHON) Àwọn_irinṣẹ́/해상도시험.py
	$(PYTHON) Àwọn_irinṣẹ́/창크기시험.py
image: build
	$(PYTHON) Àwọn_irinṣẹ́/Ṣẹ̀dá_àwòrán.py --resolution $(RESOLUTION)
	$(PYTHON) Àwọn_irinṣẹ́/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Àwọn_irinṣẹ́/개발꾸러미내보내기.py

.PHONY: 모두 àtòpọ̀_ètò ṣiṣẹ́_àṣẹ 시험 통신 àtẹ_iṣẹ́_wo àwòrán_iye 개발꾸러미
모두: all
àtòpọ̀_ètò: build
ṣiṣẹ́_àṣẹ: run
시험: test
통신: network
àtẹ_iṣẹ́_wo: desktop
àwòrán_iye: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Àwọn_irinṣẹ́/부팅시험.py
test-remmina: build
	$(PYTHON) Àwọn_irinṣẹ́/원격한글시험.py
test-naming:
	$(PYTHON) Àwọn_irinṣẹ́/명명검사.py --시언어
	$(PYTHON) Àwọn_irinṣẹ́/직접호출검사.py
	$(PYTHON) Àwọn_irinṣẹ́/orísun_àtùnyẹ̀wò.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Àwọn_irinṣẹ́/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Àwọn_irinṣẹ́/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Àwọn_irinṣẹ́/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Àwọn_irinṣẹ́/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Àwọn_irinṣẹ́/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Àwọn_irinṣẹ́/실행계층점검.py

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
