PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords читтәге_ялгау
remote: build
	$(PYTHON) Кораллар/үтәргә_команда.py --remote --resolution $(RESOLUTION) $(ARGS)
читтәге_ялгау: remote
test-remote: build
	$(PYTHON) Кораллар/원격접속시험.py
test-passwords: build
	$(PYTHON) Кораллар/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Челтәр_Стәк -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Кораллар/төзү_система.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Кораллар/COSL배포.py check
cosl-dist: build
	$(PYTHON) Кораллар/Төзү_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Кораллар/COSL배포.py bundle
	$(PYTHON) Кораллар/재연결시험.py
desktop: build
	$(PYTHON) Кораллар/үтәргә_команда.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Кораллар/셸시험.py
test-windows: build
	$(PYTHON) Кораллар/창시험.py
test-swing: build
	$(PYTHON) Кораллар/화면요소시험.py
test-stream: build
	$(PYTHON) Кораллар/흐름시험.py
test-ftp: build
	$(PYTHON) Кораллар/파일전송시험.py
test-elf: build
	$(PYTHON) Кораллар/실행파일시험.py
test-examples: build
	$(PYTHON) Кораллар/예제시험.py
network: build
	$(PYTHON) Кораллар/үтәргә_команда.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Кораллар/코딩시험.py
test-desktop: build
	$(PYTHON) Кораллар/바탕화면시험.py
run: build
	$(PYTHON) Кораллар/үтәргә_команда.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Кораллар/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Кораллар/한글입력시험.py
	$(PYTHON) Кораллар/셸시험.py
	$(PYTHON) Кораллар/바탕화면시험.py
	$(PYTHON) Кораллар/창시험.py
	$(PYTHON) Кораллар/화면요소시험.py
	$(PYTHON) Кораллар/흐름시험.py
	$(PYTHON) Кораллар/코딩시험.py
	$(PYTHON) Кораллар/자바가상기계시험.py
	$(PYTHON) Кораллар/부팅시험.py
	$(PYTHON) Кораллар/꾸러미시험.py
	$(PYTHON) Кораллар/해상도시험.py
	$(PYTHON) Кораллар/창크기시험.py
image: build
	$(PYTHON) Кораллар/Төзү_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Кораллар/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Кораллар/개발꾸러미내보내기.py

.PHONY: 모두 төзү_система үтәргә_команда 시험 통신 классик_карау IMAGE_VALUE 개발꾸러미
모두: all
төзү_система: build
үтәргә_команда: run
시험: test
통신: network
классик_карау: desktop
IMAGE_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Кораллар/부팅시험.py
test-remmina: build
	$(PYTHON) Кораллар/원격한글시험.py
test-naming:
	$(PYTHON) Кораллар/명명검사.py --시언어
	$(PYTHON) Кораллар/직접호출검사.py
	$(PYTHON) Кораллар/чыганак_бәяләмә.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Кораллар/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Кораллар/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Кораллар/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Кораллар/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Кораллар/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Кораллар/실행계층점검.py

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
