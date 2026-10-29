PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords დისტანციური_დაკავშირება
remote: build
	$(PYTHON) ხელსაწყოები/შესრულება_ბრძანება.py --remote --resolution $(RESOLUTION) $(ARGS)
დისტანციური_დაკავშირება: remote
test-remote: build
	$(PYTHON) ხელსაწყოები/원격접속시험.py
test-passwords: build
	$(PYTHON) ხელსაწყოები/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ქსელი_დასტა -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ხელსაწყოები/აწყობა_სისტემა.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ხელსაწყოები/COSL배포.py check
cosl-dist: build
	$(PYTHON) ხელსაწყოები/შექმნა_ნახატი.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ხელსაწყოები/COSL배포.py bundle
	$(PYTHON) ხელსაწყოები/재연결시험.py
desktop: build
	$(PYTHON) ხელსაწყოები/შესრულება_ბრძანება.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ხელსაწყოები/셸시험.py
test-windows: build
	$(PYTHON) ხელსაწყოები/창시험.py
test-swing: build
	$(PYTHON) ხელსაწყოები/화면요소시험.py
test-stream: build
	$(PYTHON) ხელსაწყოები/흐름시험.py
test-ftp: build
	$(PYTHON) ხელსაწყოები/파일전송시험.py
test-elf: build
	$(PYTHON) ხელსაწყოები/실행파일시험.py
test-examples: build
	$(PYTHON) ხელსაწყოები/예제시험.py
network: build
	$(PYTHON) ხელსაწყოები/შესრულება_ბრძანება.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ხელსაწყოები/코딩시험.py
test-desktop: build
	$(PYTHON) ხელსაწყოები/바탕화면시험.py
run: build
	$(PYTHON) ხელსაწყოები/შესრულება_ბრძანება.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ხელსაწყოები/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ხელსაწყოები/한글입력시험.py
	$(PYTHON) ხელსაწყოები/셸시험.py
	$(PYTHON) ხელსაწყოები/바탕화면시험.py
	$(PYTHON) ხელსაწყოები/창시험.py
	$(PYTHON) ხელსაწყოები/화면요소시험.py
	$(PYTHON) ხელსაწყოები/흐름시험.py
	$(PYTHON) ხელსაწყოები/코딩시험.py
	$(PYTHON) ხელსაწყოები/자바가상기계시험.py
	$(PYTHON) ხელსაწყოები/부팅시험.py
	$(PYTHON) ხელსაწყოები/꾸러미시험.py
	$(PYTHON) ხელსაწყოები/해상도시험.py
	$(PYTHON) ხელსაწყოები/창크기시험.py
image: build
	$(PYTHON) ხელსაწყოები/შექმნა_ნახატი.py --resolution $(RESOLUTION)
	$(PYTHON) ხელსაწყოები/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ხელსაწყოები/개발꾸러미내보내기.py

.PHONY: 모두 აწყობა_სისტემა შესრულება_ბრძანება 시험 통신 სამუშაო_დაფა_ხედი ნახატი_მნიშვნელობა 개발꾸러미
모두: all
აწყობა_სისტემა: build
შესრულება_ბრძანება: run
시험: test
통신: network
სამუშაო_დაფა_ხედი: desktop
ნახატი_მნიშვნელობა: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ხელსაწყოები/부팅시험.py
test-remmina: build
	$(PYTHON) ხელსაწყოები/원격한글시험.py
test-naming:
	$(PYTHON) ხელსაწყოები/명명검사.py --시언어
	$(PYTHON) ხელსაწყოები/직접호출검사.py
	$(PYTHON) ხელსაწყოები/წყარო_განხილვა.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ხელსაწყოები/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ხელსაწყოები/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ხელსაწყოები/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ხელსაწყოები/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ხელსაწყოები/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ხელსაწყოები/실행계층점검.py

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
