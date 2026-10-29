PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords දුරස්ථ_සබඳින්න
remote: build
	$(PYTHON) මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py --remote --resolution $(RESOLUTION) $(ARGS)
දුරස්ථ_සබඳින්න: remote
test-remote: build
	$(PYTHON) මෙවලම්/원격접속시험.py
test-passwords: build
	$(PYTHON) මෙවලම්/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ජාලය_කැටිය -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) මෙවලම්/තැනුම_පද්ධතිය.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) මෙවලම්/COSL배포.py check
cosl-dist: build
	$(PYTHON) මෙවලම්/සාදන්න_අනුරුව.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) මෙවලම්/COSL배포.py bundle
	$(PYTHON) මෙවලම්/재연결시험.py
desktop: build
	$(PYTHON) මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) මෙවලම්/셸시험.py
test-windows: build
	$(PYTHON) මෙවලම්/창시험.py
test-swing: build
	$(PYTHON) මෙවලම්/화면요소시험.py
test-stream: build
	$(PYTHON) මෙවලම්/흐름시험.py
test-ftp: build
	$(PYTHON) මෙවලම්/파일전송시험.py
test-elf: build
	$(PYTHON) මෙවලම්/실행파일시험.py
test-examples: build
	$(PYTHON) මෙවලම්/예제시험.py
network: build
	$(PYTHON) මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) මෙවලම්/코딩시험.py
test-desktop: build
	$(PYTHON) මෙවලම්/바탕화면시험.py
run: build
	$(PYTHON) මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) මෙවලම්/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) මෙවලම්/한글입력시험.py
	$(PYTHON) මෙවලම්/셸시험.py
	$(PYTHON) මෙවලම්/바탕화면시험.py
	$(PYTHON) මෙවලම්/창시험.py
	$(PYTHON) මෙවලම්/화면요소시험.py
	$(PYTHON) මෙවලම්/흐름시험.py
	$(PYTHON) මෙවලම්/코딩시험.py
	$(PYTHON) මෙවලම්/자바가상기계시험.py
	$(PYTHON) මෙවලම්/부팅시험.py
	$(PYTHON) මෙවලම්/꾸러미시험.py
	$(PYTHON) මෙවලම්/해상도시험.py
	$(PYTHON) මෙවලම්/창크기시험.py
image: build
	$(PYTHON) මෙවලම්/සාදන්න_අනුරුව.py --resolution $(RESOLUTION)
	$(PYTHON) මෙවලම්/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) මෙවලම්/개발꾸러미내보내기.py

.PHONY: 모두 තැනුම_පද්ධතිය ක්_රියාත්මක_කරන්න_විධානය 시험 통신 වැඩතලය_දසුන අනුරුව_අගය 개발꾸러미
모두: all
තැනුම_පද්ධතිය: build
ක්_රියාත්මක_කරන්න_විධානය: run
시험: test
통신: network
වැඩතලය_දසුන: desktop
අනුරුව_අගය: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) මෙවලම්/부팅시험.py
test-remmina: build
	$(PYTHON) මෙවලම්/원격한글시험.py
test-naming:
	$(PYTHON) මෙවලම්/명명검사.py --시언어
	$(PYTHON) මෙවලම්/직접호출검사.py
	$(PYTHON) මෙවලම්/මූලය_සමාලෝචනය.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) මෙවලම්/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) මෙවලම්/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) මෙවලම්/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) මෙවලම්/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) මෙවලම්/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) මෙවලම්/실행계층점검.py

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
