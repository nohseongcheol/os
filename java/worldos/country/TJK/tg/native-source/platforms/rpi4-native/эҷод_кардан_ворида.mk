PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords дурдаст_ПАЙВАСТ
remote: build
	$(PYTHON) Абзорҳо/иҷро_кардан_фармон.py --remote --resolution $(RESOLUTION) $(ARGS)
дурдаст_ПАЙВАСТ: remote
test-remote: build
	$(PYTHON) Абзорҳо/원격접속시험.py
test-passwords: build
	$(PYTHON) Абзорҳо/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Шабака_ҷамъ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Абзорҳо/сохт_система.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Абзорҳо/COSL배포.py check
cosl-dist: build
	$(PYTHON) Абзорҳо/эҷод_кардан_расм.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Абзорҳо/COSL배포.py bundle
	$(PYTHON) Абзорҳо/재연결시험.py
desktop: build
	$(PYTHON) Абзорҳо/иҷро_кардан_фармон.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Абзорҳо/셸시험.py
test-windows: build
	$(PYTHON) Абзорҳо/창시험.py
test-swing: build
	$(PYTHON) Абзорҳо/화면요소시험.py
test-stream: build
	$(PYTHON) Абзорҳо/흐름시험.py
test-ftp: build
	$(PYTHON) Абзорҳо/파일전송시험.py
test-elf: build
	$(PYTHON) Абзорҳо/실행파일시험.py
test-examples: build
	$(PYTHON) Абзорҳо/예제시험.py
network: build
	$(PYTHON) Абзорҳо/иҷро_кардан_фармон.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Абзорҳо/코딩시험.py
test-desktop: build
	$(PYTHON) Абзорҳо/바탕화면시험.py
run: build
	$(PYTHON) Абзорҳо/иҷро_кардан_фармон.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Абзорҳо/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Абзорҳо/한글입력시험.py
	$(PYTHON) Абзорҳо/셸시험.py
	$(PYTHON) Абзорҳо/바탕화면시험.py
	$(PYTHON) Абзорҳо/창시험.py
	$(PYTHON) Абзорҳо/화면요소시험.py
	$(PYTHON) Абзорҳо/흐름시험.py
	$(PYTHON) Абзорҳо/코딩시험.py
	$(PYTHON) Абзорҳо/자바가상기계시험.py
	$(PYTHON) Абзорҳо/부팅시험.py
	$(PYTHON) Абзорҳо/꾸러미시험.py
	$(PYTHON) Абзорҳо/해상도시험.py
	$(PYTHON) Абзорҳо/창크기시험.py
image: build
	$(PYTHON) Абзорҳо/эҷод_кардан_расм.py --resolution $(RESOLUTION)
	$(PYTHON) Абзорҳо/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Абзорҳо/개발꾸러미내보내기.py

.PHONY: 모두 сохт_система иҷро_кардан_фармон 시험 통신 мизи_корӣ_намуд расм_қимат 개발꾸러미
모두: all
сохт_система: build
иҷро_кардан_фармон: run
시험: test
통신: network
мизи_корӣ_намуд: desktop
расм_қимат: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Абзорҳо/부팅시험.py
test-remmina: build
	$(PYTHON) Абзорҳо/원격한글시험.py
test-naming:
	$(PYTHON) Абзорҳо/명명검사.py --시언어
	$(PYTHON) Абзорҳо/직접호출검사.py
	$(PYTHON) Абзорҳо/манбаъ_тақриз.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Абзорҳо/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Абзорҳо/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Абзорҳо/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Абзорҳо/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Абзорҳо/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Абзорҳо/실행계층점검.py

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
