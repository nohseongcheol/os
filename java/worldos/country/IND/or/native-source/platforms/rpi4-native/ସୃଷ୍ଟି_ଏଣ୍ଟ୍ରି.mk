PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ଦୂରବର୍ତ୍ତୀ_ସଂଯୋଗ
remote: build
	$(PYTHON) ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py --remote --resolution $(RESOLUTION) $(ARGS)
ଦୂରବର୍ତ୍ତୀ_ସଂଯୋଗ: remote
test-remote: build
	$(PYTHON) ଉପକରଣସମୂହ/원격접속시험.py
test-passwords: build
	$(PYTHON) ଉପକରଣସମୂହ/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ନେଟ୍_ୱାର୍କ୍_ଗଦା -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ଉପକରଣସମୂହ/ବିଲ୍ଡ୍_ସିଷ୍ଟମ.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ଉପକରଣସମୂହ/COSL배포.py check
cosl-dist: build
	$(PYTHON) ଉପକରଣସମୂହ/ସୃଷ୍ଟି_ଚିତ୍ର.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ଉପକରଣସମୂହ/COSL배포.py bundle
	$(PYTHON) ଉପକରଣସମୂହ/재연결시험.py
desktop: build
	$(PYTHON) ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ଉପକରଣସମୂହ/셸시험.py
test-windows: build
	$(PYTHON) ଉପକରଣସମୂହ/창시험.py
test-swing: build
	$(PYTHON) ଉପକରଣସମୂହ/화면요소시험.py
test-stream: build
	$(PYTHON) ଉପକରଣସମୂହ/흐름시험.py
test-ftp: build
	$(PYTHON) ଉପକରଣସମୂହ/파일전송시험.py
test-elf: build
	$(PYTHON) ଉପକରଣସମୂହ/실행파일시험.py
test-examples: build
	$(PYTHON) ଉପକରଣସମୂହ/예제시험.py
network: build
	$(PYTHON) ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ଉପକରଣସମୂହ/코딩시험.py
test-desktop: build
	$(PYTHON) ଉପକରଣସମୂହ/바탕화면시험.py
run: build
	$(PYTHON) ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ଉପକରଣସମୂହ/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ଉପକରଣସମୂହ/한글입력시험.py
	$(PYTHON) ଉପକରଣସମୂହ/셸시험.py
	$(PYTHON) ଉପକରଣସମୂହ/바탕화면시험.py
	$(PYTHON) ଉପକରଣସମୂହ/창시험.py
	$(PYTHON) ଉପକରଣସମୂହ/화면요소시험.py
	$(PYTHON) ଉପକରଣସମୂହ/흐름시험.py
	$(PYTHON) ଉପକରଣସମୂହ/코딩시험.py
	$(PYTHON) ଉପକରଣସମୂହ/자바가상기계시험.py
	$(PYTHON) ଉପକରଣସମୂହ/부팅시험.py
	$(PYTHON) ଉପକରଣସମୂହ/꾸러미시험.py
	$(PYTHON) ଉପକରଣସମୂହ/해상도시험.py
	$(PYTHON) ଉପକରଣସମୂହ/창크기시험.py
image: build
	$(PYTHON) ଉପକରଣସମୂହ/ସୃଷ୍ଟି_ଚିତ୍ର.py --resolution $(RESOLUTION)
	$(PYTHON) ଉପକରଣସମୂହ/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ଉପକରଣସମୂହ/개발꾸러미내보내기.py

.PHONY: 모두 ବିଲ୍ଡ୍_ସିଷ୍ଟମ ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 시험 통신 ଡେସ୍କଟପ୍_ଭିୟୁ ଚିତ୍ର_ମୂଲ୍ୟ 개발꾸러미
모두: all
ବିଲ୍ଡ୍_ସିଷ୍ଟମ: build
ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ: run
시험: test
통신: network
ଡେସ୍କଟପ୍_ଭିୟୁ: desktop
ଚିତ୍ର_ମୂଲ୍ୟ: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ଉପକରଣସମୂହ/부팅시험.py
test-remmina: build
	$(PYTHON) ଉପକରଣସମୂହ/원격한글시험.py
test-naming:
	$(PYTHON) ଉପକରଣସମୂହ/명명검사.py --시언어
	$(PYTHON) ଉପକରଣସମୂହ/직접호출검사.py
	$(PYTHON) ଉପକରଣସମୂହ/ଉତ୍ସ_ସମୀକ୍ଷା.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ଉପକରଣସମୂହ/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ଉପକରଣସମୂହ/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ଉପକରଣସମୂହ/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ଉପକରଣସମୂହ/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ଉପକରଣସମୂହ/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ଉପକରଣସମୂହ/실행계층점검.py

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
