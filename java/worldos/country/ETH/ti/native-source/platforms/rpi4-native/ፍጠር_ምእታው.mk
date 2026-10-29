PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ርሑቕ_ኣላግብ
remote: build
	$(PYTHON) መሳርሒታት/ተግብር_ትእዛዝ.py --remote --resolution $(RESOLUTION) $(ARGS)
ርሑቕ_ኣላግብ: remote
test-remote: build
	$(PYTHON) መሳርሒታት/원격접속시험.py
test-passwords: build
	$(PYTHON) መሳርሒታት/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ማሕበራዊ_ኔትወርክ_ድርደራ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) መሳርሒታት/ህነጽ_ስርዓት.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) መሳርሒታት/COSL배포.py check
cosl-dist: build
	$(PYTHON) መሳርሒታት/ፍጠር_ምስሊ.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) መሳርሒታት/COSL배포.py bundle
	$(PYTHON) መሳርሒታት/재연결시험.py
desktop: build
	$(PYTHON) መሳርሒታት/ተግብር_ትእዛዝ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) መሳርሒታት/셸시험.py
test-windows: build
	$(PYTHON) መሳርሒታት/창시험.py
test-swing: build
	$(PYTHON) መሳርሒታት/화면요소시험.py
test-stream: build
	$(PYTHON) መሳርሒታት/흐름시험.py
test-ftp: build
	$(PYTHON) መሳርሒታት/파일전송시험.py
test-elf: build
	$(PYTHON) መሳርሒታት/실행파일시험.py
test-examples: build
	$(PYTHON) መሳርሒታት/예제시험.py
network: build
	$(PYTHON) መሳርሒታት/ተግብር_ትእዛዝ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) መሳርሒታት/코딩시험.py
test-desktop: build
	$(PYTHON) መሳርሒታት/바탕화면시험.py
run: build
	$(PYTHON) መሳርሒታት/ተግብር_ትእዛዝ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) መሳርሒታት/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) መሳርሒታት/한글입력시험.py
	$(PYTHON) መሳርሒታት/셸시험.py
	$(PYTHON) መሳርሒታት/바탕화면시험.py
	$(PYTHON) መሳርሒታት/창시험.py
	$(PYTHON) መሳርሒታት/화면요소시험.py
	$(PYTHON) መሳርሒታት/흐름시험.py
	$(PYTHON) መሳርሒታት/코딩시험.py
	$(PYTHON) መሳርሒታት/자바가상기계시험.py
	$(PYTHON) መሳርሒታት/부팅시험.py
	$(PYTHON) መሳርሒታት/꾸러미시험.py
	$(PYTHON) መሳርሒታት/해상도시험.py
	$(PYTHON) መሳርሒታት/창크기시험.py
image: build
	$(PYTHON) መሳርሒታት/ፍጠር_ምስሊ.py --resolution $(RESOLUTION)
	$(PYTHON) መሳርሒታት/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) መሳርሒታት/개발꾸러미내보내기.py

.PHONY: 모두 ህነጽ_ስርዓት ተግብር_ትእዛዝ 시험 통신 ዴስክቶፕ_ትርኢት ምስሊ_ዋጋ 개발꾸러미
모두: all
ህነጽ_ስርዓት: build
ተግብር_ትእዛዝ: run
시험: test
통신: network
ዴስክቶፕ_ትርኢት: desktop
ምስሊ_ዋጋ: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) መሳርሒታት/부팅시험.py
test-remmina: build
	$(PYTHON) መሳርሒታት/원격한글시험.py
test-naming:
	$(PYTHON) መሳርሒታት/명명검사.py --시언어
	$(PYTHON) መሳርሒታት/직접호출검사.py
	$(PYTHON) መሳርሒታት/ምንጪ_ገምጋም.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) መሳርሒታት/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) መሳርሒታት/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) መሳርሒታት/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) መሳርሒታት/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) መሳርሒታት/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) መሳርሒታት/실행계층점검.py

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
