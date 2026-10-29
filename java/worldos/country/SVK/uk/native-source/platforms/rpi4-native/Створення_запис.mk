PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords віддалений_зв_язок
remote: build
	$(PYTHON) інструменти/Виконати_команда.py --remote --resolution $(RESOLUTION) $(ARGS)
віддалений_зв_язок: remote
test-remote: build
	$(PYTHON) інструменти/원격접속시험.py
test-passwords: build
	$(PYTHON) інструменти/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter мережа_Стіс -I vendor/lwip/src/include випробування/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) інструменти/збирання.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) інструменти/COSL배포.py check
cosl-dist: build
	$(PYTHON) інструменти/Створення_фото.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) інструменти/COSL배포.py bundle
	$(PYTHON) інструменти/재연결시험.py
desktop: build
	$(PYTHON) інструменти/Виконати_команда.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) інструменти/셸시험.py
test-windows: build
	$(PYTHON) інструменти/창시험.py
test-swing: build
	$(PYTHON) інструменти/화면요소시험.py
test-stream: build
	$(PYTHON) інструменти/흐름시험.py
test-ftp: build
	$(PYTHON) інструменти/파일전송시험.py
test-elf: build
	$(PYTHON) інструменти/실행파일시험.py
test-examples: build
	$(PYTHON) інструменти/예제시험.py
network: build
	$(PYTHON) інструменти/Виконати_команда.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) інструменти/코딩시험.py
test-desktop: build
	$(PYTHON) інструменти/바탕화면시험.py
run: build
	$(PYTHON) інструменти/Виконати_команда.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) інструменти/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) інструменти/한글입력시험.py
	$(PYTHON) інструменти/셸시험.py
	$(PYTHON) інструменти/바탕화면시험.py
	$(PYTHON) інструменти/창시험.py
	$(PYTHON) інструменти/화면요소시험.py
	$(PYTHON) інструменти/흐름시험.py
	$(PYTHON) інструменти/코딩시험.py
	$(PYTHON) інструменти/자바가상기계시험.py
	$(PYTHON) інструменти/부팅시험.py
	$(PYTHON) інструменти/꾸러미시험.py
	$(PYTHON) інструменти/해상도시험.py
	$(PYTHON) інструменти/창크기시험.py
image: build
	$(PYTHON) інструменти/Створення_фото.py --resolution $(RESOLUTION)
	$(PYTHON) інструменти/експортувати_пакет_інструментів_розробки.py
sdk: build
	$(PYTHON) інструменти/експортувати_пакет_інструментів_розробки.py

.PHONY: 모두 збирання Виконати_команда випробування 통신 настільний_Вигляд фото_значення пакет_розробки
모두: all
збирання: build
Виконати_команда: run
випробування: test
통신: network
настільний_Вигляд: desktop
фото_значення: image
пакет_розробки: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) інструменти/부팅시험.py
test-remmina: build
	$(PYTHON) інструменти/원격한글시험.py
test-naming:
	$(PYTHON) інструменти/명명검사.py --시언어
	$(PYTHON) інструменти/직접호출검사.py
	$(PYTHON) інструменти/джерело_відгук.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) інструменти/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) інструменти/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) інструменти/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) інструменти/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) інструменти/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) інструменти/실행계층점검.py

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
