PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords հեռակա_Կապակցել
remote: build
	$(PYTHON) Գործիքներ/կատարել_հրաման.py --remote --resolution $(RESOLUTION) $(ARGS)
հեռակա_Կապակցել: remote
test-remote: build
	$(PYTHON) Գործիքներ/원격접속시험.py
test-passwords: build
	$(PYTHON) Գործիքներ/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Ցանց_Շեղջ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Գործիքներ/կառուցել_համակարգ.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Գործիքներ/COSL배포.py check
cosl-dist: build
	$(PYTHON) Գործիքներ/Կերտի_ր_նկար.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Գործիքներ/COSL배포.py bundle
	$(PYTHON) Գործիքներ/재연결시험.py
desktop: build
	$(PYTHON) Գործիքներ/կատարել_հրաման.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Գործիքներ/셸시험.py
test-windows: build
	$(PYTHON) Գործիքներ/창시험.py
test-swing: build
	$(PYTHON) Գործիքներ/화면요소시험.py
test-stream: build
	$(PYTHON) Գործիքներ/흐름시험.py
test-ftp: build
	$(PYTHON) Գործիքներ/파일전송시험.py
test-elf: build
	$(PYTHON) Գործիքներ/실행파일시험.py
test-examples: build
	$(PYTHON) Գործիքներ/예제시험.py
network: build
	$(PYTHON) Գործիքներ/կատարել_հրաման.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Գործիքներ/코딩시험.py
test-desktop: build
	$(PYTHON) Գործիքներ/바탕화면시험.py
run: build
	$(PYTHON) Գործիքներ/կատարել_հրաման.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Գործիքներ/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Գործիքներ/한글입력시험.py
	$(PYTHON) Գործիքներ/셸시험.py
	$(PYTHON) Գործիքներ/바탕화면시험.py
	$(PYTHON) Գործիքներ/창시험.py
	$(PYTHON) Գործիքներ/화면요소시험.py
	$(PYTHON) Գործիքներ/흐름시험.py
	$(PYTHON) Գործիքներ/코딩시험.py
	$(PYTHON) Գործիքներ/자바가상기계시험.py
	$(PYTHON) Գործիքներ/부팅시험.py
	$(PYTHON) Գործիքներ/꾸러미시험.py
	$(PYTHON) Գործիքներ/해상도시험.py
	$(PYTHON) Գործիքներ/창크기시험.py
image: build
	$(PYTHON) Գործիքներ/Կերտի_ր_նկար.py --resolution $(RESOLUTION)
	$(PYTHON) Գործիքներ/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Գործիքներ/개발꾸러미내보내기.py

.PHONY: 모두 կառուցել_համակարգ կատարել_հրաման 시험 통신 սեղան_տեսք նկար_արժեք 개발꾸러미
모두: all
կառուցել_համակարգ: build
կատարել_հրաման: run
시험: test
통신: network
սեղան_տեսք: desktop
նկար_արժեք: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Գործիքներ/부팅시험.py
test-remmina: build
	$(PYTHON) Գործիքներ/원격한글시험.py
test-naming:
	$(PYTHON) Գործիքներ/명명검사.py --시언어
	$(PYTHON) Գործիքներ/직접호출검사.py
	$(PYTHON) Գործիքներ/աղբյուր_կարծիք.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Գործիքներ/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Գործիքներ/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Գործիքներ/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Գործիքներ/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Գործիքներ/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Գործիքներ/실행계층점검.py

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
