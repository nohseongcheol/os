PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords بعید_جڑیں
remote: build
	$(PYTHON) ٹولز/نفاذ_کریں_حکم.py --remote --resolution $(RESOLUTION) $(ARGS)
بعید_جڑیں: remote
test-remote: build
	$(PYTHON) ٹولز/원격접속시험.py
test-passwords: build
	$(PYTHON) ٹولز/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter نیٹ_ورک_اسٹیک -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ٹولز/بلڈ_نظام.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ٹولز/COSL배포.py check
cosl-dist: build
	$(PYTHON) ٹولز/بنائیں_نقش.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ٹولز/COSL배포.py bundle
	$(PYTHON) ٹولز/재연결시험.py
desktop: build
	$(PYTHON) ٹولز/نفاذ_کریں_حکم.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ٹولز/셸시험.py
test-windows: build
	$(PYTHON) ٹولز/창시험.py
test-swing: build
	$(PYTHON) ٹولز/화면요소시험.py
test-stream: build
	$(PYTHON) ٹولز/흐름시험.py
test-ftp: build
	$(PYTHON) ٹولز/파일전송시험.py
test-elf: build
	$(PYTHON) ٹولز/실행파일시험.py
test-examples: build
	$(PYTHON) ٹولز/예제시험.py
network: build
	$(PYTHON) ٹولز/نفاذ_کریں_حکم.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ٹولز/코딩시험.py
test-desktop: build
	$(PYTHON) ٹولز/바탕화면시험.py
run: build
	$(PYTHON) ٹولز/نفاذ_کریں_حکم.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ٹولز/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ٹولز/한글입력시험.py
	$(PYTHON) ٹولز/셸시험.py
	$(PYTHON) ٹولز/바탕화면시험.py
	$(PYTHON) ٹولز/창시험.py
	$(PYTHON) ٹولز/화면요소시험.py
	$(PYTHON) ٹولز/흐름시험.py
	$(PYTHON) ٹولز/코딩시험.py
	$(PYTHON) ٹولز/자바가상기계시험.py
	$(PYTHON) ٹولز/부팅시험.py
	$(PYTHON) ٹولز/꾸러미시험.py
	$(PYTHON) ٹولز/해상도시험.py
	$(PYTHON) ٹولز/창크기시험.py
image: build
	$(PYTHON) ٹولز/بنائیں_نقش.py --resolution $(RESOLUTION)
	$(PYTHON) ٹولز/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ٹولز/개발꾸러미내보내기.py

.PHONY: 모두 بلڈ_نظام نفاذ_کریں_حکم 시험 통신 ڈیسک_ٹاپ_منظر نقش_قدر 개발꾸러미
모두: all
بلڈ_نظام: build
نفاذ_کریں_حکم: run
시험: test
통신: network
ڈیسک_ٹاپ_منظر: desktop
نقش_قدر: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ٹولز/부팅시험.py
test-remmina: build
	$(PYTHON) ٹولز/원격한글시험.py
test-naming:
	$(PYTHON) ٹولز/명명검사.py --시언어
	$(PYTHON) ٹولز/직접호출검사.py
	$(PYTHON) ٹولز/ماخذ_جائزہ.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ٹولز/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ٹولز/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ٹولز/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ٹولز/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ٹولز/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ٹولز/실행계층점검.py

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
