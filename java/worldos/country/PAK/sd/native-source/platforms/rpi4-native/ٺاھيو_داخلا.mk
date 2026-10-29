PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords بعيد_ڪنيڪٽ
remote: build
	$(PYTHON) اوزار/تعميل_ڪرڻ_حڪم.py --remote --resolution $(RESOLUTION) $(ARGS)
بعيد_ڪنيڪٽ: remote
test-remote: build
	$(PYTHON) اوزار/원격접속시험.py
test-passwords: build
	$(PYTHON) اوزار/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter نيٽ_ورڪ_اڀرڻ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) اوزار/گڏ_ڪريو_سسٽم.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) اوزار/COSL배포.py check
cosl-dist: build
	$(PYTHON) اوزار/ٺاھيو_نقش.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) اوزار/COSL배포.py bundle
	$(PYTHON) اوزار/재연결시험.py
desktop: build
	$(PYTHON) اوزار/تعميل_ڪرڻ_حڪم.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) اوزار/셸시험.py
test-windows: build
	$(PYTHON) اوزار/창시험.py
test-swing: build
	$(PYTHON) اوزار/화면요소시험.py
test-stream: build
	$(PYTHON) اوزار/흐름시험.py
test-ftp: build
	$(PYTHON) اوزار/파일전송시험.py
test-elf: build
	$(PYTHON) اوزار/실행파일시험.py
test-examples: build
	$(PYTHON) اوزار/예제시험.py
network: build
	$(PYTHON) اوزار/تعميل_ڪرڻ_حڪم.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) اوزار/코딩시험.py
test-desktop: build
	$(PYTHON) اوزار/바탕화면시험.py
run: build
	$(PYTHON) اوزار/تعميل_ڪرڻ_حڪم.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) اوزار/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) اوزار/한글입력시험.py
	$(PYTHON) اوزار/셸시험.py
	$(PYTHON) اوزار/바탕화면시험.py
	$(PYTHON) اوزار/창시험.py
	$(PYTHON) اوزار/화면요소시험.py
	$(PYTHON) اوزار/흐름시험.py
	$(PYTHON) اوزار/코딩시험.py
	$(PYTHON) اوزار/자바가상기계시험.py
	$(PYTHON) اوزار/부팅시험.py
	$(PYTHON) اوزار/꾸러미시험.py
	$(PYTHON) اوزار/해상도시험.py
	$(PYTHON) اوزار/창크기시험.py
image: build
	$(PYTHON) اوزار/ٺاھيو_نقش.py --resolution $(RESOLUTION)
	$(PYTHON) اوزار/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) اوزار/개발꾸러미내보내기.py

.PHONY: 모두 گڏ_ڪريو_سسٽم تعميل_ڪرڻ_حڪم 시험 통신 ڊيسڪٽاپ_منظر نقش_قدر 개발꾸러미
모두: all
گڏ_ڪريو_سسٽم: build
تعميل_ڪرڻ_حڪم: run
시험: test
통신: network
ڊيسڪٽاپ_منظر: desktop
نقش_قدر: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) اوزار/부팅시험.py
test-remmina: build
	$(PYTHON) اوزار/원격한글시험.py
test-naming:
	$(PYTHON) اوزار/명명검사.py --시언어
	$(PYTHON) اوزار/직접호출검사.py
	$(PYTHON) اوزار/ماخذ_جائزو.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) اوزار/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) اوزار/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) اوزار/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) اوزار/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) اوزار/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) اوزار/실행계층점검.py

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
