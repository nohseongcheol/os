PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords në_largësi_Lidh
remote: build
	$(PYTHON) Mjete/zbatoj_komandë.py --remote --resolution $(RESOLUTION) $(ARGS)
në_largësi_Lidh: remote
test-remote: build
	$(PYTHON) Mjete/원격접속시험.py
test-passwords: build
	$(PYTHON) Mjete/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter rrjet_Stivë -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Mjete/ndërtoj_sistem.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Mjete/COSL배포.py check
cosl-dist: build
	$(PYTHON) Mjete/Krijo_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Mjete/COSL배포.py bundle
	$(PYTHON) Mjete/재연결시험.py
desktop: build
	$(PYTHON) Mjete/zbatoj_komandë.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Mjete/셸시험.py
test-windows: build
	$(PYTHON) Mjete/창시험.py
test-swing: build
	$(PYTHON) Mjete/화면요소시험.py
test-stream: build
	$(PYTHON) Mjete/흐름시험.py
test-ftp: build
	$(PYTHON) Mjete/파일전송시험.py
test-elf: build
	$(PYTHON) Mjete/실행파일시험.py
test-examples: build
	$(PYTHON) Mjete/예제시험.py
network: build
	$(PYTHON) Mjete/zbatoj_komandë.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Mjete/코딩시험.py
test-desktop: build
	$(PYTHON) Mjete/바탕화면시험.py
run: build
	$(PYTHON) Mjete/zbatoj_komandë.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Mjete/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Mjete/한글입력시험.py
	$(PYTHON) Mjete/셸시험.py
	$(PYTHON) Mjete/바탕화면시험.py
	$(PYTHON) Mjete/창시험.py
	$(PYTHON) Mjete/화면요소시험.py
	$(PYTHON) Mjete/흐름시험.py
	$(PYTHON) Mjete/코딩시험.py
	$(PYTHON) Mjete/자바가상기계시험.py
	$(PYTHON) Mjete/부팅시험.py
	$(PYTHON) Mjete/꾸러미시험.py
	$(PYTHON) Mjete/해상도시험.py
	$(PYTHON) Mjete/창크기시험.py
image: build
	$(PYTHON) Mjete/Krijo_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Mjete/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Mjete/개발꾸러미내보내기.py

.PHONY: 모두 ndërtoj_sistem zbatoj_komandë 시험 통신 desktop_Pamja IMAGE_VALUE 개발꾸러미
모두: all
ndërtoj_sistem: build
zbatoj_komandë: run
시험: test
통신: network
desktop_Pamja: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Mjete/부팅시험.py
test-remmina: build
	$(PYTHON) Mjete/원격한글시험.py
test-naming:
	$(PYTHON) Mjete/명명검사.py --시언어
	$(PYTHON) Mjete/직접호출검사.py
	$(PYTHON) Mjete/burim_recension.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Mjete/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Mjete/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Mjete/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Mjete/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Mjete/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Mjete/실행계층점검.py

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
