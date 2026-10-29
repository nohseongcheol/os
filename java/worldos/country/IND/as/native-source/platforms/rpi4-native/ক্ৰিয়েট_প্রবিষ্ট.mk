PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords দূৰবৰ্তী_সংযোগ
remote: build
	$(PYTHON) সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py --remote --resolution $(RESOLUTION) $(ARGS)
দূৰবৰ্তী_সংযোগ: remote
test-remote: build
	$(PYTHON) সঁজুলিসমূহ/원격접속시험.py
test-passwords: build
	$(PYTHON) সঁজুলিসমূহ/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter নেটৱৰ্ক_ষ্টেক -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) সঁজুলিসমূহ/বিল্ড_ছিষ্টেম.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) সঁজুলিসমূহ/COSL배포.py check
cosl-dist: build
	$(PYTHON) সঁজুলিসমূহ/ক্ৰিয়েট_ছবি.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) সঁজুলিসমূহ/COSL배포.py bundle
	$(PYTHON) সঁজুলিসমূহ/재연결시험.py
desktop: build
	$(PYTHON) সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) সঁজুলিসমূহ/셸시험.py
test-windows: build
	$(PYTHON) সঁজুলিসমূহ/창시험.py
test-swing: build
	$(PYTHON) সঁজুলিসমূহ/화면요소시험.py
test-stream: build
	$(PYTHON) সঁজুলিসমূহ/흐름시험.py
test-ftp: build
	$(PYTHON) সঁজুলিসমূহ/파일전송시험.py
test-elf: build
	$(PYTHON) সঁজুলিসমূহ/실행파일시험.py
test-examples: build
	$(PYTHON) সঁজুলিসমূহ/예제시험.py
network: build
	$(PYTHON) সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) সঁজুলিসমূহ/코딩시험.py
test-desktop: build
	$(PYTHON) সঁজুলিসমূহ/바탕화면시험.py
run: build
	$(PYTHON) সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) সঁজুলিসমূহ/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) সঁজুলিসমূহ/한글입력시험.py
	$(PYTHON) সঁজুলিসমূহ/셸시험.py
	$(PYTHON) সঁজুলিসমূহ/바탕화면시험.py
	$(PYTHON) সঁজুলিসমূহ/창시험.py
	$(PYTHON) সঁজুলিসমূহ/화면요소시험.py
	$(PYTHON) সঁজুলিসমূহ/흐름시험.py
	$(PYTHON) সঁজুলিসমূহ/코딩시험.py
	$(PYTHON) সঁজুলিসমূহ/자바가상기계시험.py
	$(PYTHON) সঁজুলিসমূহ/부팅시험.py
	$(PYTHON) সঁজুলিসমূহ/꾸러미시험.py
	$(PYTHON) সঁজুলিসমূহ/해상도시험.py
	$(PYTHON) সঁজুলিসমূহ/창크기시험.py
image: build
	$(PYTHON) সঁজুলিসমূহ/ক্ৰিয়েট_ছবি.py --resolution $(RESOLUTION)
	$(PYTHON) সঁজুলিসমূহ/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) সঁজুলিসমূহ/개발꾸러미내보내기.py

.PHONY: 모두 বিল্ড_ছিষ্টেম নিষ্পাদন_আদেশ 시험 통신 ডেস্কটপ_দর্শন ছবি_মান 개발꾸러미
모두: all
বিল্ড_ছিষ্টেম: build
নিষ্পাদন_আদেশ: run
시험: test
통신: network
ডেস্কটপ_দর্শন: desktop
ছবি_মান: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) সঁজুলিসমূহ/부팅시험.py
test-remmina: build
	$(PYTHON) সঁজুলিসমূহ/원격한글시험.py
test-naming:
	$(PYTHON) সঁজুলিসমূহ/명명검사.py --시언어
	$(PYTHON) সঁজুলিসমূহ/직접호출검사.py
	$(PYTHON) সঁজুলিসমূহ/উৎস_সমীক্ষা.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) সঁজুলিসমূহ/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) সঁজুলিসমূহ/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) সঁজুলিসমূহ/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) সঁজুলিসমূহ/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) সঁজুলিসমূহ/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) সঁজুলিসমূহ/실행계층점검.py

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
