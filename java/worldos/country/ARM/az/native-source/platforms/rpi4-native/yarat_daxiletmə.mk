PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords uzaq_QOŞUN
remote: build
	$(PYTHON) Alətlər/icra_etmək_əmr.py --remote --resolution $(RESOLUTION) $(ARGS)
uzaq_QOŞUN: remote
test-remote: build
	$(PYTHON) Alətlər/원격접속시험.py
test-passwords: build
	$(PYTHON) Alətlər/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Şəbəkə_Yığın -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Alətlər/qurmaq_sistem.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Alətlər/COSL배포.py check
cosl-dist: build
	$(PYTHON) Alətlər/yarat_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Alətlər/COSL배포.py bundle
	$(PYTHON) Alətlər/재연결시험.py
desktop: build
	$(PYTHON) Alətlər/icra_etmək_əmr.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Alətlər/셸시험.py
test-windows: build
	$(PYTHON) Alətlər/창시험.py
test-swing: build
	$(PYTHON) Alətlər/화면요소시험.py
test-stream: build
	$(PYTHON) Alətlər/흐름시험.py
test-ftp: build
	$(PYTHON) Alətlər/파일전송시험.py
test-elf: build
	$(PYTHON) Alətlər/실행파일시험.py
test-examples: build
	$(PYTHON) Alətlər/예제시험.py
network: build
	$(PYTHON) Alətlər/icra_etmək_əmr.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Alətlər/코딩시험.py
test-desktop: build
	$(PYTHON) Alətlər/바탕화면시험.py
run: build
	$(PYTHON) Alətlər/icra_etmək_əmr.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Alətlər/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Alətlər/한글입력시험.py
	$(PYTHON) Alətlər/셸시험.py
	$(PYTHON) Alətlər/바탕화면시험.py
	$(PYTHON) Alətlər/창시험.py
	$(PYTHON) Alətlər/화면요소시험.py
	$(PYTHON) Alətlər/흐름시험.py
	$(PYTHON) Alətlər/코딩시험.py
	$(PYTHON) Alətlər/자바가상기계시험.py
	$(PYTHON) Alətlər/부팅시험.py
	$(PYTHON) Alətlər/꾸러미시험.py
	$(PYTHON) Alətlər/해상도시험.py
	$(PYTHON) Alətlər/창크기시험.py
image: build
	$(PYTHON) Alətlər/yarat_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Alətlər/ixrac_etmək_SDK.py
sdk: build
	$(PYTHON) Alətlər/ixrac_etmək_SDK.py

.PHONY: 모두 qurmaq_sistem icra_etmək_əmr 시험 통신 iş_masası_baxmaq IMAGE_VALUE 개발꾸러미
모두: all
qurmaq_sistem: build
icra_etmək_əmr: run
시험: test
통신: network
iş_masası_baxmaq: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Alətlər/부팅시험.py
test-remmina: build
	$(PYTHON) Alətlər/원격한글시험.py
test-naming:
	$(PYTHON) Alətlər/명명검사.py --시언어
	$(PYTHON) Alətlər/직접호출검사.py
	$(PYTHON) Alətlər/mənbə_rəy.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Alətlər/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Alətlər/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Alətlər/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Alətlər/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Alətlər/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Alətlər/실행계층점검.py

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
