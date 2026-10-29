PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords отдалечен_връзка
remote: build
	$(PYTHON) Инструменти/изпълнявам_команда.py --remote --resolution $(RESOLUTION) $(ARGS)
отдалечен_връзка: remote
test-remote: build
	$(PYTHON) Инструменти/원격접속시험.py
test-passwords: build
	$(PYTHON) Инструменти/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter мрежа_стек -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Инструменти/компилация_система.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Инструменти/COSL배포.py check
cosl-dist: build
	$(PYTHON) Инструменти/Създаване_снимка.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Инструменти/COSL배포.py bundle
	$(PYTHON) Инструменти/재연결시험.py
desktop: build
	$(PYTHON) Инструменти/изпълнявам_команда.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Инструменти/셸시험.py
test-windows: build
	$(PYTHON) Инструменти/창시험.py
test-swing: build
	$(PYTHON) Инструменти/화면요소시험.py
test-stream: build
	$(PYTHON) Инструменти/흐름시험.py
test-ftp: build
	$(PYTHON) Инструменти/파일전송시험.py
test-elf: build
	$(PYTHON) Инструменти/실행파일시험.py
test-examples: build
	$(PYTHON) Инструменти/예제시험.py
network: build
	$(PYTHON) Инструменти/изпълнявам_команда.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Инструменти/코딩시험.py
test-desktop: build
	$(PYTHON) Инструменти/바탕화면시험.py
run: build
	$(PYTHON) Инструменти/изпълнявам_команда.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Инструменти/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Инструменти/한글입력시험.py
	$(PYTHON) Инструменти/셸시험.py
	$(PYTHON) Инструменти/바탕화면시험.py
	$(PYTHON) Инструменти/창시험.py
	$(PYTHON) Инструменти/화면요소시험.py
	$(PYTHON) Инструменти/흐름시험.py
	$(PYTHON) Инструменти/코딩시험.py
	$(PYTHON) Инструменти/자바가상기계시험.py
	$(PYTHON) Инструменти/부팅시험.py
	$(PYTHON) Инструменти/꾸러미시험.py
	$(PYTHON) Инструменти/해상도시험.py
	$(PYTHON) Инструменти/창크기시험.py
image: build
	$(PYTHON) Инструменти/Създаване_снимка.py --resolution $(RESOLUTION)
	$(PYTHON) Инструменти/експортирам_софтуерен_развоен_пакет.py
sdk: build
	$(PYTHON) Инструменти/експортирам_софтуерен_развоен_пакет.py

.PHONY: 모두 компилация_система изпълнявам_команда 시험 통신 десктоп_Изглед снимка_стойност развоен_пакет
모두: all
компилация_система: build
изпълнявам_команда: run
시험: test
통신: network
десктоп_Изглед: desktop
снимка_стойност: image
развоен_пакет: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Инструменти/부팅시험.py
test-remmina: build
	$(PYTHON) Инструменти/원격한글시험.py
test-naming:
	$(PYTHON) Инструменти/명명검사.py --시언어
	$(PYTHON) Инструменти/직접호출검사.py
	$(PYTHON) Инструменти/източник_рецензия.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Инструменти/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Инструменти/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Инструменти/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Инструменти/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Инструменти/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Инструменти/실행계층점검.py

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
