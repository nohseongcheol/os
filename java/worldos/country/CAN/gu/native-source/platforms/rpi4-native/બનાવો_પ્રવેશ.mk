PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords રિમોટ_કનેક્ટ
remote: build
	$(PYTHON) ઉપકરણો/અમલ_કરો_આદેશ.py --remote --resolution $(RESOLUTION) $(ARGS)
રિમોટ_કનેક્ટ: remote
test-remote: build
	$(PYTHON) ઉપકરણો/원격접속시험.py
test-passwords: build
	$(PYTHON) ઉપકરણો/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter નેટવર્ક_સ્ટેક -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ઉપકરણો/બિલ્ડ_સિસ્ટમ.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ઉપકરણો/COSL배포.py check
cosl-dist: build
	$(PYTHON) ઉપકરણો/બનાવો_છબી.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ઉપકરણો/COSL배포.py bundle
	$(PYTHON) ઉપકરણો/재연결시험.py
desktop: build
	$(PYTHON) ઉપકરણો/અમલ_કરો_આદેશ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ઉપકરણો/셸시험.py
test-windows: build
	$(PYTHON) ઉપકરણો/창시험.py
test-swing: build
	$(PYTHON) ઉપકરણો/화면요소시험.py
test-stream: build
	$(PYTHON) ઉપકરણો/흐름시험.py
test-ftp: build
	$(PYTHON) ઉપકરણો/파일전송시험.py
test-elf: build
	$(PYTHON) ઉપકરણો/실행파일시험.py
test-examples: build
	$(PYTHON) ઉપકરણો/예제시험.py
network: build
	$(PYTHON) ઉપકરણો/અમલ_કરો_આદેશ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ઉપકરણો/코딩시험.py
test-desktop: build
	$(PYTHON) ઉપકરણો/바탕화면시험.py
run: build
	$(PYTHON) ઉપકરણો/અમલ_કરો_આદેશ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ઉપકરણો/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ઉપકરણો/한글입력시험.py
	$(PYTHON) ઉપકરણો/셸시험.py
	$(PYTHON) ઉપકરણો/바탕화면시험.py
	$(PYTHON) ઉપકરણો/창시험.py
	$(PYTHON) ઉપકરણો/화면요소시험.py
	$(PYTHON) ઉપકરણો/흐름시험.py
	$(PYTHON) ઉપકરણો/코딩시험.py
	$(PYTHON) ઉપકરણો/자바가상기계시험.py
	$(PYTHON) ઉપકરણો/부팅시험.py
	$(PYTHON) ઉપકરણો/꾸러미시험.py
	$(PYTHON) ઉપકરણો/해상도시험.py
	$(PYTHON) ઉપકરણો/창크기시험.py
image: build
	$(PYTHON) ઉપકરણો/બનાવો_છબી.py --resolution $(RESOLUTION)
	$(PYTHON) ઉપકરણો/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ઉપકરણો/개발꾸러미내보내기.py

.PHONY: 모두 બિલ્ડ_સિસ્ટમ અમલ_કરો_આદેશ 시험 통신 ડેસ્કટૉપ_જુઓ છબી_મૂલ્ય 개발꾸러미
모두: all
બિલ્ડ_સિસ્ટમ: build
અમલ_કરો_આદેશ: run
시험: test
통신: network
ડેસ્કટૉપ_જુઓ: desktop
છબી_મૂલ્ય: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ઉપકરણો/부팅시험.py
test-remmina: build
	$(PYTHON) ઉપકરણો/원격한글시험.py
test-naming:
	$(PYTHON) ઉપકરણો/명명검사.py --시언어
	$(PYTHON) ઉપકરણો/직접호출검사.py
	$(PYTHON) ઉપકરણો/સ્રોત_સમીક્ષા.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ઉપકરણો/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ઉપકરણો/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ઉપકરણો/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ઉપકરણો/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ઉપકરણો/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ઉપકરણો/실행계층점검.py

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
