PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords দূরবর্তী_সংযোগ
remote: build
	$(PYTHON) সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py --remote --resolution $(RESOLUTION) $(ARGS)
দূরবর্তী_সংযোগ: remote
test-remote: build
	$(PYTHON) সরঞ্জামগুলি/원격접속시험.py
test-passwords: build
	$(PYTHON) সরঞ্জামগুলি/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter নেটওয়ার্ক_গাদা -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) সরঞ্জামগুলি/গঠন_সিস্টেম.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) সরঞ্জামগুলি/COSL배포.py check
cosl-dist: build
	$(PYTHON) সরঞ্জামগুলি/ক্রিয়েট_ছবি.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) সরঞ্জামগুলি/COSL배포.py bundle
	$(PYTHON) সরঞ্জামগুলি/재연결시험.py
desktop: build
	$(PYTHON) সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) সরঞ্জামগুলি/셸시험.py
test-windows: build
	$(PYTHON) সরঞ্জামগুলি/창시험.py
test-swing: build
	$(PYTHON) সরঞ্জামগুলি/화면요소시험.py
test-stream: build
	$(PYTHON) সরঞ্জামগুলি/흐름시험.py
test-ftp: build
	$(PYTHON) সরঞ্জামগুলি/파일전송시험.py
test-elf: build
	$(PYTHON) সরঞ্জামগুলি/실행파일시험.py
test-examples: build
	$(PYTHON) সরঞ্জামগুলি/예제시험.py
network: build
	$(PYTHON) সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) সরঞ্জামগুলি/코딩시험.py
test-desktop: build
	$(PYTHON) সরঞ্জামগুলি/바탕화면시험.py
run: build
	$(PYTHON) সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) সরঞ্জামগুলি/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) সরঞ্জামগুলি/한글입력시험.py
	$(PYTHON) সরঞ্জামগুলি/셸시험.py
	$(PYTHON) সরঞ্জামগুলি/바탕화면시험.py
	$(PYTHON) সরঞ্জামগুলি/창시험.py
	$(PYTHON) সরঞ্জামগুলি/화면요소시험.py
	$(PYTHON) সরঞ্জামগুলি/흐름시험.py
	$(PYTHON) সরঞ্জামগুলি/코딩시험.py
	$(PYTHON) সরঞ্জামগুলি/자바가상기계시험.py
	$(PYTHON) সরঞ্জামগুলি/부팅시험.py
	$(PYTHON) সরঞ্জামগুলি/꾸러미시험.py
	$(PYTHON) সরঞ্জামগুলি/해상도시험.py
	$(PYTHON) সরঞ্জামগুলি/창크기시험.py
image: build
	$(PYTHON) সরঞ্জামগুলি/ক্রিয়েট_ছবি.py --resolution $(RESOLUTION)
	$(PYTHON) সরঞ্জামগুলি/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) সরঞ্জামগুলি/개발꾸러미내보내기.py

.PHONY: 모두 গঠন_সিস্টেম কার্যকর_করুন_আদেশ 시험 통신 ডেস্কটপ_ভিউ ছবি_মান 개발꾸러미
모두: all
গঠন_সিস্টেম: build
কার্যকর_করুন_আদেশ: run
시험: test
통신: network
ডেস্কটপ_ভিউ: desktop
ছবি_মান: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) সরঞ্জামগুলি/부팅시험.py
test-remmina: build
	$(PYTHON) সরঞ্জামগুলি/원격한글시험.py
test-naming:
	$(PYTHON) সরঞ্জামগুলি/명명검사.py --시언어
	$(PYTHON) সরঞ্জামগুলি/직접호출검사.py
	$(PYTHON) সরঞ্জামগুলি/উত্স_পর্যালোচনা.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) সরঞ্জামগুলি/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) সরঞ্জামগুলি/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) সরঞ্জামগুলি/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) সরঞ্জামগুলি/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) সরঞ্জামগুলি/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) সরঞ্জামগুলি/실행계층점검.py

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
