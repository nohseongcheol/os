PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ರಿಮೋಟ್_ಕನೆಕ್ಟ್
remote: build
	$(PYTHON) ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py --remote --resolution $(RESOLUTION) $(ARGS)
ರಿಮೋಟ್_ಕನೆಕ್ಟ್: remote
test-remote: build
	$(PYTHON) ಪರಿಕರಗಳು/원격접속시험.py
test-passwords: build
	$(PYTHON) ಪರಿಕರಗಳು/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ಪರಿಕರಗಳು/ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ಪರಿಕರಗಳು/COSL배포.py check
cosl-dist: build
	$(PYTHON) ಪರಿಕರಗಳು/ರಚಿಸು_ಇಮೇಜ್.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ಪರಿಕರಗಳು/COSL배포.py bundle
	$(PYTHON) ಪರಿಕರಗಳು/재연결시험.py
desktop: build
	$(PYTHON) ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ಪರಿಕರಗಳು/셸시험.py
test-windows: build
	$(PYTHON) ಪರಿಕರಗಳು/창시험.py
test-swing: build
	$(PYTHON) ಪರಿಕರಗಳು/화면요소시험.py
test-stream: build
	$(PYTHON) ಪರಿಕರಗಳು/흐름시험.py
test-ftp: build
	$(PYTHON) ಪರಿಕರಗಳು/파일전송시험.py
test-elf: build
	$(PYTHON) ಪರಿಕರಗಳು/실행파일시험.py
test-examples: build
	$(PYTHON) ಪರಿಕರಗಳು/예제시험.py
network: build
	$(PYTHON) ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ಪರಿಕರಗಳು/코딩시험.py
test-desktop: build
	$(PYTHON) ಪರಿಕರಗಳು/바탕화면시험.py
run: build
	$(PYTHON) ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ಪರಿಕರಗಳು/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ಪರಿಕರಗಳು/한글입력시험.py
	$(PYTHON) ಪರಿಕರಗಳು/셸시험.py
	$(PYTHON) ಪರಿಕರಗಳು/바탕화면시험.py
	$(PYTHON) ಪರಿಕರಗಳು/창시험.py
	$(PYTHON) ಪರಿಕರಗಳು/화면요소시험.py
	$(PYTHON) ಪರಿಕರಗಳು/흐름시험.py
	$(PYTHON) ಪರಿಕರಗಳು/코딩시험.py
	$(PYTHON) ಪರಿಕರಗಳು/자바가상기계시험.py
	$(PYTHON) ಪರಿಕರಗಳು/부팅시험.py
	$(PYTHON) ಪರಿಕರಗಳು/꾸러미시험.py
	$(PYTHON) ಪರಿಕರಗಳು/해상도시험.py
	$(PYTHON) ಪರಿಕರಗಳು/창크기시험.py
image: build
	$(PYTHON) ಪರಿಕರಗಳು/ರಚಿಸು_ಇಮೇಜ್.py --resolution $(RESOLUTION)
	$(PYTHON) ಪರಿಕರಗಳು/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ಪರಿಕರಗಳು/개발꾸러미내보내기.py

.PHONY: 모두 ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ ಪೂರೈಸು_ಆದೇಶ 시험 통신 ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ ಇಮೇಜ್_ಮೌಲ್ಯ 개발꾸러미
모두: all
ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ: build
ಪೂರೈಸು_ಆದೇಶ: run
시험: test
통신: network
ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ: desktop
ಇಮೇಜ್_ಮೌಲ್ಯ: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ಪರಿಕರಗಳು/부팅시험.py
test-remmina: build
	$(PYTHON) ಪರಿಕರಗಳು/원격한글시험.py
test-naming:
	$(PYTHON) ಪರಿಕರಗಳು/명명검사.py --시언어
	$(PYTHON) ಪರಿಕರಗಳು/직접호출검사.py
	$(PYTHON) ಪರಿಕರಗಳು/ಮೂಲ_ಪರಿಶೀಲನೆ.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ಪರಿಕರಗಳು/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ಪರಿಕರಗಳು/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ಪರಿಕರಗಳು/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ಪರಿಕರಗಳು/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ಪರಿಕರಗಳು/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ಪರಿಕರಗಳು/실행계층점검.py

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
