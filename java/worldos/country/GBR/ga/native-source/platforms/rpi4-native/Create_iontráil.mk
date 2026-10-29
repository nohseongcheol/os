PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords cianda_nasc
remote: build
	$(PYTHON) Uirlisí/Rith_ordú.py --remote --resolution $(RESOLUTION) $(ARGS)
cianda_nasc: remote
test-remote: build
	$(PYTHON) Uirlisí/원격접속시험.py
test-passwords: build
	$(PYTHON) Uirlisí/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Líonra_Cruach -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Uirlisí/tóg_córas.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Uirlisí/COSL배포.py check
cosl-dist: build
	$(PYTHON) Uirlisí/Create_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Uirlisí/COSL배포.py bundle
	$(PYTHON) Uirlisí/재연결시험.py
desktop: build
	$(PYTHON) Uirlisí/Rith_ordú.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Uirlisí/셸시험.py
test-windows: build
	$(PYTHON) Uirlisí/창시험.py
test-swing: build
	$(PYTHON) Uirlisí/화면요소시험.py
test-stream: build
	$(PYTHON) Uirlisí/흐름시험.py
test-ftp: build
	$(PYTHON) Uirlisí/파일전송시험.py
test-elf: build
	$(PYTHON) Uirlisí/실행파일시험.py
test-examples: build
	$(PYTHON) Uirlisí/예제시험.py
network: build
	$(PYTHON) Uirlisí/Rith_ordú.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Uirlisí/코딩시험.py
test-desktop: build
	$(PYTHON) Uirlisí/바탕화면시험.py
run: build
	$(PYTHON) Uirlisí/Rith_ordú.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Uirlisí/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Uirlisí/한글입력시험.py
	$(PYTHON) Uirlisí/셸시험.py
	$(PYTHON) Uirlisí/바탕화면시험.py
	$(PYTHON) Uirlisí/창시험.py
	$(PYTHON) Uirlisí/화면요소시험.py
	$(PYTHON) Uirlisí/흐름시험.py
	$(PYTHON) Uirlisí/코딩시험.py
	$(PYTHON) Uirlisí/자바가상기계시험.py
	$(PYTHON) Uirlisí/부팅시험.py
	$(PYTHON) Uirlisí/꾸러미시험.py
	$(PYTHON) Uirlisí/해상도시험.py
	$(PYTHON) Uirlisí/창크기시험.py
image: build
	$(PYTHON) Uirlisí/Create_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Uirlisí/easportáil_SDK.py
sdk: build
	$(PYTHON) Uirlisí/easportáil_SDK.py

.PHONY: 모두 tóg_córas Rith_ordú 시험 통신 deasc_Amharc IMAGE_VALUE 개발꾸러미
모두: all
tóg_córas: build
Rith_ordú: run
시험: test
통신: network
deasc_Amharc: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Uirlisí/부팅시험.py
test-remmina: build
	$(PYTHON) Uirlisí/원격한글시험.py
test-naming:
	$(PYTHON) Uirlisí/명명검사.py --시언어
	$(PYTHON) Uirlisí/직접호출검사.py
	$(PYTHON) Uirlisí/foinse_léirmheas.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Uirlisí/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Uirlisí/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Uirlisí/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Uirlisí/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Uirlisí/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Uirlisí/실행계층점검.py

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
