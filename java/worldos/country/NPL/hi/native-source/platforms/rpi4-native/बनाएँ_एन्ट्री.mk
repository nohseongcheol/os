PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords दूरस्थ_कनेक्ट
remote: build
	$(PYTHON) उपकरण/निष्पादित_करें_आदेश.py --remote --resolution $(RESOLUTION) $(ARGS)
दूरस्थ_कनेक्ट: remote
test-remote: build
	$(PYTHON) उपकरण/원격접속시험.py
test-passwords: build
	$(PYTHON) उपकरण/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter नेटवर्क_स्टैक -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) उपकरण/बिल्ड_सिस्टम.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) उपकरण/COSL배포.py check
cosl-dist: build
	$(PYTHON) उपकरण/बनाएँ_छवि.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) उपकरण/COSL배포.py bundle
	$(PYTHON) उपकरण/재연결시험.py
desktop: build
	$(PYTHON) उपकरण/निष्पादित_करें_आदेश.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) उपकरण/셸시험.py
test-windows: build
	$(PYTHON) उपकरण/창시험.py
test-swing: build
	$(PYTHON) उपकरण/화면요소시험.py
test-stream: build
	$(PYTHON) उपकरण/흐름시험.py
test-ftp: build
	$(PYTHON) उपकरण/파일전송시험.py
test-elf: build
	$(PYTHON) उपकरण/실행파일시험.py
test-examples: build
	$(PYTHON) उपकरण/예제시험.py
network: build
	$(PYTHON) उपकरण/निष्पादित_करें_आदेश.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) उपकरण/코딩시험.py
test-desktop: build
	$(PYTHON) उपकरण/바탕화면시험.py
run: build
	$(PYTHON) उपकरण/निष्पादित_करें_आदेश.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) उपकरण/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) उपकरण/한글입력시험.py
	$(PYTHON) उपकरण/셸시험.py
	$(PYTHON) उपकरण/바탕화면시험.py
	$(PYTHON) उपकरण/창시험.py
	$(PYTHON) उपकरण/화면요소시험.py
	$(PYTHON) उपकरण/흐름시험.py
	$(PYTHON) उपकरण/코딩시험.py
	$(PYTHON) उपकरण/자바가상기계시험.py
	$(PYTHON) उपकरण/부팅시험.py
	$(PYTHON) उपकरण/꾸러미시험.py
	$(PYTHON) उपकरण/해상도시험.py
	$(PYTHON) उपकरण/창크기시험.py
image: build
	$(PYTHON) उपकरण/बनाएँ_छवि.py --resolution $(RESOLUTION)
	$(PYTHON) उपकरण/निर्यात_करें_सॉफ़्टवेयर_डेवलपमेंट_किट.py
sdk: build
	$(PYTHON) उपकरण/निर्यात_करें_सॉफ़्टवेयर_डेवलपमेंट_किट.py

.PHONY: 모두 बिल्ड_सिस्टम निष्पादित_करें_आदेश 시험 통신 डेस्कटॉप_दृश्य छवि_मान डेवलपमेंट_किट
모두: all
बिल्ड_सिस्टम: build
निष्पादित_करें_आदेश: run
시험: test
통신: network
डेस्कटॉप_दृश्य: desktop
छवि_मान: image
डेवलपमेंट_किट: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) उपकरण/부팅시험.py
test-remmina: build
	$(PYTHON) उपकरण/원격한글시험.py
test-naming:
	$(PYTHON) उपकरण/명명검사.py --सी_भाषा
	$(PYTHON) उपकरण/직접호출검사.py
	$(PYTHON) उपकरण/स्रोत_समीक्षा.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) उपकरण/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) उपकरण/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) उपकरण/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) उपकरण/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) उपकरण/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) उपकरण/실행계층점검.py

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
