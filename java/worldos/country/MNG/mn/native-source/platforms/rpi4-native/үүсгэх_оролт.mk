PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords алсын_холбох
remote: build
	$(PYTHON) Хэрэгслүүд/Гүйцэтгэх_команд.py --remote --resolution $(RESOLUTION) $(ARGS)
алсын_холбох: remote
test-remote: build
	$(PYTHON) Хэрэгслүүд/원격접속시험.py
test-passwords: build
	$(PYTHON) Хэрэгслүүд/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Сүлжээ_давхцал -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Хэрэгслүүд/хувилбар_систем.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Хэрэгслүүд/COSL배포.py check
cosl-dist: build
	$(PYTHON) Хэрэгслүүд/үүсгэх_зураг.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Хэрэгслүүд/COSL배포.py bundle
	$(PYTHON) Хэрэгслүүд/재연결시험.py
desktop: build
	$(PYTHON) Хэрэгслүүд/Гүйцэтгэх_команд.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Хэрэгслүүд/셸시험.py
test-windows: build
	$(PYTHON) Хэрэгслүүд/창시험.py
test-swing: build
	$(PYTHON) Хэрэгслүүд/화면요소시험.py
test-stream: build
	$(PYTHON) Хэрэгслүүд/흐름시험.py
test-ftp: build
	$(PYTHON) Хэрэгслүүд/파일전송시험.py
test-elf: build
	$(PYTHON) Хэрэгслүүд/실행파일시험.py
test-examples: build
	$(PYTHON) Хэрэгслүүд/예제시험.py
network: build
	$(PYTHON) Хэрэгслүүд/Гүйцэтгэх_команд.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Хэрэгслүүд/코딩시험.py
test-desktop: build
	$(PYTHON) Хэрэгслүүд/바탕화면시험.py
run: build
	$(PYTHON) Хэрэгслүүд/Гүйцэтгэх_команд.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Хэрэгслүүд/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Хэрэгслүүд/한글입력시험.py
	$(PYTHON) Хэрэгслүүд/셸시험.py
	$(PYTHON) Хэрэгслүүд/바탕화면시험.py
	$(PYTHON) Хэрэгслүүд/창시험.py
	$(PYTHON) Хэрэгслүүд/화면요소시험.py
	$(PYTHON) Хэрэгслүүд/흐름시험.py
	$(PYTHON) Хэрэгслүүд/코딩시험.py
	$(PYTHON) Хэрэгслүүд/자바가상기계시험.py
	$(PYTHON) Хэрэгслүүд/부팅시험.py
	$(PYTHON) Хэрэгслүүд/꾸러미시험.py
	$(PYTHON) Хэрэгслүүд/해상도시험.py
	$(PYTHON) Хэрэгслүүд/창크기시험.py
image: build
	$(PYTHON) Хэрэгслүүд/үүсгэх_зураг.py --resolution $(RESOLUTION)
	$(PYTHON) Хэрэгслүүд/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Хэрэгслүүд/개발꾸러미내보내기.py

.PHONY: 모두 хувилбар_систем Гүйцэтгэх_команд 시험 통신 дэлгэц_харах зураг_утга 개발꾸러미
모두: all
хувилбар_систем: build
Гүйцэтгэх_команд: run
시험: test
통신: network
дэлгэц_харах: desktop
зураг_утга: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Хэрэгслүүд/부팅시험.py
test-remmina: build
	$(PYTHON) Хэрэгслүүд/원격한글시험.py
test-naming:
	$(PYTHON) Хэрэгслүүд/명명검사.py --시언어
	$(PYTHON) Хэрэгслүүд/직접호출검사.py
	$(PYTHON) Хэрэгслүүд/эх_тойм.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Хэрэгслүүд/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Хэрэгслүүд/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Хэрэгслүүд/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Хэрэгслүүд/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Хэрэгслүүд/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Хэрэгслүүд/실행계층점검.py

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
