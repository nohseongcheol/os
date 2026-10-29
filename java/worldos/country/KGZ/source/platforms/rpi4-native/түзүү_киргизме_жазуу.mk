PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords алыскы_ТУТАШУУ
remote: build
	$(PYTHON) Куралдар/аткаруу_буйрук.py --remote --resolution $(RESOLUTION) $(ARGS)
алыскы_ТУТАШУУ: remote
test-remote: build
	$(PYTHON) Куралдар/원격접속시험.py
test-passwords: build
	$(PYTHON) Куралдар/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Желе_стек -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Куралдар/курам_тутум.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Куралдар/COSL배포.py check
cosl-dist: build
	$(PYTHON) Куралдар/түзүү_сүрөт.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Куралдар/COSL배포.py bundle
	$(PYTHON) Куралдар/재연결시험.py
desktop: build
	$(PYTHON) Куралдар/аткаруу_буйрук.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Куралдар/셸시험.py
test-windows: build
	$(PYTHON) Куралдар/창시험.py
test-swing: build
	$(PYTHON) Куралдар/화면요소시험.py
test-stream: build
	$(PYTHON) Куралдар/흐름시험.py
test-ftp: build
	$(PYTHON) Куралдар/파일전송시험.py
test-elf: build
	$(PYTHON) Куралдар/실행파일시험.py
test-examples: build
	$(PYTHON) Куралдар/예제시험.py
network: build
	$(PYTHON) Куралдар/аткаруу_буйрук.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Куралдар/코딩시험.py
test-desktop: build
	$(PYTHON) Куралдар/바탕화면시험.py
run: build
	$(PYTHON) Куралдар/аткаруу_буйрук.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Куралдар/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Куралдар/한글입력시험.py
	$(PYTHON) Куралдар/셸시험.py
	$(PYTHON) Куралдар/바탕화면시험.py
	$(PYTHON) Куралдар/창시험.py
	$(PYTHON) Куралдар/화면요소시험.py
	$(PYTHON) Куралдар/흐름시험.py
	$(PYTHON) Куралдар/코딩시험.py
	$(PYTHON) Куралдар/자바가상기계시험.py
	$(PYTHON) Куралдар/부팅시험.py
	$(PYTHON) Куралдар/꾸러미시험.py
	$(PYTHON) Куралдар/해상도시험.py
	$(PYTHON) Куралдар/창크기시험.py
image: build
	$(PYTHON) Куралдар/түзүү_сүрөт.py --resolution $(RESOLUTION)
	$(PYTHON) Куралдар/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Куралдар/개발꾸러미내보내기.py

.PHONY: 모두 курам_тутум аткаруу_буйрук 시험 통신 иш_такта_көрүү сүрөт_маани 개발꾸러미
모두: all
курам_тутум: build
аткаруу_буйрук: run
시험: test
통신: network
иш_такта_көрүү: desktop
сүрөт_маани: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Куралдар/부팅시험.py
test-remmina: build
	$(PYTHON) Куралдар/원격한글시험.py
test-naming:
	$(PYTHON) Куралдар/명명검사.py --시언어
	$(PYTHON) Куралдар/직접호출검사.py
	$(PYTHON) Куралдар/башат_карап_чыгуу.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Куралдар/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Куралдар/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Куралдар/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Куралдар/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Куралдар/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Куралдар/실행계층점검.py

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
