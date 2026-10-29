PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords 원격접속
remote: build
	$(PYTHON) Құралдар/орындау_пәрмен.py --remote --resolution $(RESOLUTION) $(ARGS)
원격접속: remote
test-remote: build
	$(PYTHON) Құралдар/원격접속시험.py
test-passwords: build
	$(PYTHON) Құралдар/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter желі_Бума -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Құралдар/құрастыру_жүйе.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Құралдар/COSL배포.py check
cosl-dist: build
	$(PYTHON) Құралдар/жасау_сурет.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Құралдар/COSL배포.py bundle
	$(PYTHON) Құралдар/재연결시험.py
desktop: build
	$(PYTHON) Құралдар/орындау_пәрмен.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Құралдар/셸시험.py
test-windows: build
	$(PYTHON) Құралдар/창시험.py
test-swing: build
	$(PYTHON) Құралдар/화면요소시험.py
test-stream: build
	$(PYTHON) Құралдар/흐름시험.py
test-ftp: build
	$(PYTHON) Құралдар/파일전송시험.py
test-elf: build
	$(PYTHON) Құралдар/실행파일시험.py
test-examples: build
	$(PYTHON) Құралдар/예제시험.py
network: build
	$(PYTHON) Құралдар/орындау_пәрмен.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Құралдар/코딩시험.py
test-desktop: build
	$(PYTHON) Құралдар/바탕화면시험.py
run: build
	$(PYTHON) Құралдар/орындау_пәрмен.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Құралдар/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Құралдар/한글입력시험.py
	$(PYTHON) Құралдар/셸시험.py
	$(PYTHON) Құралдар/바탕화면시험.py
	$(PYTHON) Құралдар/창시험.py
	$(PYTHON) Құралдар/화면요소시험.py
	$(PYTHON) Құралдар/흐름시험.py
	$(PYTHON) Құралдар/코딩시험.py
	$(PYTHON) Құралдар/자바가상기계시험.py
	$(PYTHON) Құралдар/부팅시험.py
	$(PYTHON) Құралдар/꾸러미시험.py
	$(PYTHON) Құралдар/해상도시험.py
	$(PYTHON) Құралдар/창크기시험.py
image: build
	$(PYTHON) Құралдар/жасау_сурет.py --resolution $(RESOLUTION)
	$(PYTHON) Құралдар/экспорттау_бағдарламалық_құралды_әзірлеуге_арналған_құралдар_жиынтығы.py
sdk: build
	$(PYTHON) Құралдар/экспорттау_бағдарламалық_құралды_әзірлеуге_арналған_құралдар_жиынтығы.py

.PHONY: 모두 құрастыру_жүйе орындау_пәрмен 시험 통신 үстелдік_Көрініс сурет_мән 개발꾸러미
모두: all
құрастыру_жүйе: build
орындау_пәрмен: run
시험: test
통신: network
үстелдік_Көрініс: desktop
сурет_мән: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Құралдар/부팅시험.py
test-remmina: build
	$(PYTHON) Құралдар/원격한글시험.py
test-naming:
	$(PYTHON) Құралдар/명명검사.py --시언어
	$(PYTHON) Құралдар/직접호출검사.py
	$(PYTHON) Құралдар/көз_сараптау.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Құралдар/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Құралдар/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Құралдар/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Құралдар/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Құралдар/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Құралдар/실행계층점검.py

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
