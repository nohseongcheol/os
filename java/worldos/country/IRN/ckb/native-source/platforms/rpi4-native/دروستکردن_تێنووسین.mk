PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords دوورەدەس_لكاندن
remote: build
	$(PYTHON) ئامرازەکان/جێبەجێکردن_فەرمان.py --remote --resolution $(RESOLUTION) $(ARGS)
دوورەدەس_لكاندن: remote
test-remote: build
	$(PYTHON) ئامرازەکان/원격접속시험.py
test-passwords: build
	$(PYTHON) ئامرازەکان/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter تۆڕ_ستاك -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ئامرازەکان/دروستکراو_سیستم.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ئامرازەکان/COSL배포.py check
cosl-dist: build
	$(PYTHON) ئامرازەکان/دروستکردن_وێنە.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ئامرازەکان/COSL배포.py bundle
	$(PYTHON) ئامرازەکان/재연결시험.py
desktop: build
	$(PYTHON) ئامرازەکان/جێبەجێکردن_فەرمان.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ئامرازەکان/셸시험.py
test-windows: build
	$(PYTHON) ئامرازەکان/창시험.py
test-swing: build
	$(PYTHON) ئامرازەکان/화면요소시험.py
test-stream: build
	$(PYTHON) ئامرازەکان/흐름시험.py
test-ftp: build
	$(PYTHON) ئامرازەکان/파일전송시험.py
test-elf: build
	$(PYTHON) ئامرازەکان/실행파일시험.py
test-examples: build
	$(PYTHON) ئامرازەکان/예제시험.py
network: build
	$(PYTHON) ئامرازەکان/جێبەجێکردن_فەرمان.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ئامرازەکان/코딩시험.py
test-desktop: build
	$(PYTHON) ئامرازەکان/바탕화면시험.py
run: build
	$(PYTHON) ئامرازەکان/جێبەجێکردن_فەرمان.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ئامرازەکان/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ئامرازەکان/한글입력시험.py
	$(PYTHON) ئامرازەکان/셸시험.py
	$(PYTHON) ئامرازەکان/바탕화면시험.py
	$(PYTHON) ئامرازەکان/창시험.py
	$(PYTHON) ئامرازەکان/화면요소시험.py
	$(PYTHON) ئامرازەکان/흐름시험.py
	$(PYTHON) ئامرازەکان/코딩시험.py
	$(PYTHON) ئامرازەکان/자바가상기계시험.py
	$(PYTHON) ئامرازەکان/부팅시험.py
	$(PYTHON) ئامرازەکان/꾸러미시험.py
	$(PYTHON) ئامرازەکان/해상도시험.py
	$(PYTHON) ئامرازەکان/창크기시험.py
image: build
	$(PYTHON) ئامرازەکان/دروستکردن_وێنە.py --resolution $(RESOLUTION)
	$(PYTHON) ئامرازەکان/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ئامرازەکان/개발꾸러미내보내기.py

.PHONY: 모두 دروستکراو_سیستم جێبەجێکردن_فەرمان 시험 통신 دێسکتۆپ_دیمەن وێنە_نرخ 개발꾸러미
모두: all
دروستکراو_سیستم: build
جێبەجێکردن_فەرمان: run
시험: test
통신: network
دێسکتۆپ_دیمەن: desktop
وێنە_نرخ: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ئامرازەکان/부팅시험.py
test-remmina: build
	$(PYTHON) ئامرازەکان/원격한글시험.py
test-naming:
	$(PYTHON) ئامرازەکان/명명검사.py --시언어
	$(PYTHON) ئامرازەکان/직접호출검사.py
	$(PYTHON) ئامرازەکان/ژێدەر_پێداچوونەوە.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ئامرازەکان/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ئامرازەکان/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ئامرازەکان/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ئامرازەکان/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ئامرازەکان/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ئامرازەکان/실행계층점검.py

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
