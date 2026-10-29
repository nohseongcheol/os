PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords தொலைநிலை_இணை
remote: build
	$(PYTHON) கருவிகள்/இயக்கு_கட்டளை.py --remote --resolution $(RESOLUTION) $(ARGS)
தொலைநிலை_இணை: remote
test-remote: build
	$(PYTHON) கருவிகள்/원격접속시험.py
test-passwords: build
	$(PYTHON) கருவிகள்/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter பிணையம்_அடுக்கு_49fba3da -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) கருவிகள்/தொகு_முறைமை.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) கருவிகள்/COSL배포.py check
cosl-dist: build
	$(PYTHON) கருவிகள்/உருவாக்கு_படம்.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) கருவிகள்/COSL배포.py bundle
	$(PYTHON) கருவிகள்/재연결시험.py
desktop: build
	$(PYTHON) கருவிகள்/இயக்கு_கட்டளை.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) கருவிகள்/셸시험.py
test-windows: build
	$(PYTHON) கருவிகள்/창시험.py
test-swing: build
	$(PYTHON) கருவிகள்/화면요소시험.py
test-stream: build
	$(PYTHON) கருவிகள்/흐름시험.py
test-ftp: build
	$(PYTHON) கருவிகள்/파일전송시험.py
test-elf: build
	$(PYTHON) கருவிகள்/실행파일시험.py
test-examples: build
	$(PYTHON) கருவிகள்/예제시험.py
network: build
	$(PYTHON) கருவிகள்/இயக்கு_கட்டளை.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) கருவிகள்/코딩시험.py
test-desktop: build
	$(PYTHON) கருவிகள்/바탕화면시험.py
run: build
	$(PYTHON) கருவிகள்/இயக்கு_கட்டளை.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) கருவிகள்/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) கருவிகள்/한글입력시험.py
	$(PYTHON) கருவிகள்/셸시험.py
	$(PYTHON) கருவிகள்/바탕화면시험.py
	$(PYTHON) கருவிகள்/창시험.py
	$(PYTHON) கருவிகள்/화면요소시험.py
	$(PYTHON) கருவிகள்/흐름시험.py
	$(PYTHON) கருவிகள்/코딩시험.py
	$(PYTHON) கருவிகள்/자바가상기계시험.py
	$(PYTHON) கருவிகள்/부팅시험.py
	$(PYTHON) கருவிகள்/꾸러미시험.py
	$(PYTHON) கருவிகள்/해상도시험.py
	$(PYTHON) கருவிகள்/창크기시험.py
image: build
	$(PYTHON) கருவிகள்/உருவாக்கு_படம்.py --resolution $(RESOLUTION)
	$(PYTHON) கருவிகள்/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) கருவிகள்/개발꾸러미내보내기.py

.PHONY: 모두 தொகு_முறைமை இயக்கு_கட்டளை 시험 통신 டெஸ்க்டாப்_காட்சி படம்_மதிப்பு 개발꾸러미
모두: all
தொகு_முறைமை: build
இயக்கு_கட்டளை: run
시험: test
통신: network
டெஸ்க்டாப்_காட்சி: desktop
படம்_மதிப்பு: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) கருவிகள்/부팅시험.py
test-remmina: build
	$(PYTHON) கருவிகள்/원격한글시험.py
test-naming:
	$(PYTHON) கருவிகள்/명명검사.py --시언어
	$(PYTHON) கருவிகள்/직접호출검사.py
	$(PYTHON) கருவிகள்/மூலம்_மதிப்பாய்வு.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) கருவிகள்/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) கருவிகள்/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) கருவிகள்/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) கருவிகள்/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) கருவிகள்/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) கருவிகள்/실행계층점검.py

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
