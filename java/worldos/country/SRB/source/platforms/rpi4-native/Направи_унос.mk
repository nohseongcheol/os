PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords удаљен_ПОВЕЖИ
remote: build
	$(PYTHON) Алатке/Изврши_команда.py --remote --resolution $(RESOLUTION) $(ARGS)
удаљен_ПОВЕЖИ: remote
test-remote: build
	$(PYTHON) Алатке/원격접속시험.py
test-passwords: build
	$(PYTHON) Алатке/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Мрежа_комплет -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Алатке/градити_систем.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Алатке/COSL배포.py check
cosl-dist: build
	$(PYTHON) Алатке/Направи_слика.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Алатке/COSL배포.py bundle
	$(PYTHON) Алатке/재연결시험.py
desktop: build
	$(PYTHON) Алатке/Изврши_команда.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Алатке/셸시험.py
test-windows: build
	$(PYTHON) Алатке/창시험.py
test-swing: build
	$(PYTHON) Алатке/화면요소시험.py
test-stream: build
	$(PYTHON) Алатке/흐름시험.py
test-ftp: build
	$(PYTHON) Алатке/파일전송시험.py
test-elf: build
	$(PYTHON) Алатке/실행파일시험.py
test-examples: build
	$(PYTHON) Алатке/예제시험.py
network: build
	$(PYTHON) Алатке/Изврши_команда.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Алатке/코딩시험.py
test-desktop: build
	$(PYTHON) Алатке/바탕화면시험.py
run: build
	$(PYTHON) Алатке/Изврши_команда.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Алатке/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Алатке/한글입력시험.py
	$(PYTHON) Алатке/셸시험.py
	$(PYTHON) Алатке/바탕화면시험.py
	$(PYTHON) Алатке/창시험.py
	$(PYTHON) Алатке/화면요소시험.py
	$(PYTHON) Алатке/흐름시험.py
	$(PYTHON) Алатке/코딩시험.py
	$(PYTHON) Алатке/자바가상기계시험.py
	$(PYTHON) Алатке/부팅시험.py
	$(PYTHON) Алатке/꾸러미시험.py
	$(PYTHON) Алатке/해상도시험.py
	$(PYTHON) Алатке/창크기시험.py
image: build
	$(PYTHON) Алатке/Направи_слика.py --resolution $(RESOLUTION)
	$(PYTHON) Алатке/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Алатке/개발꾸러미내보내기.py

.PHONY: 모두 градити_систем Изврши_команда 시험 통신 десктоп_Приказ слика_вриједност 개발꾸러미
모두: all
градити_систем: build
Изврши_команда: run
시험: test
통신: network
десктоп_Приказ: desktop
слика_вриједност: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Алатке/부팅시험.py
test-remmina: build
	$(PYTHON) Алатке/원격한글시험.py
test-naming:
	$(PYTHON) Алатке/명명검사.py --시언어
	$(PYTHON) Алатке/직접호출검사.py
	$(PYTHON) Алатке/извор_коментар.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Алатке/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Алатке/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Алатке/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Алатке/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Алатке/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Алатке/실행계층점검.py

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
