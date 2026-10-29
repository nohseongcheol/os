PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords የሩቅ_አገናኝ
remote: build
	$(PYTHON) መሳሪያዎች/ፈጽም_ትእዛዝ.py --remote --resolution $(RESOLUTION) $(ARGS)
የሩቅ_አገናኝ: remote
test-remote: build
	$(PYTHON) መሳሪያዎች/원격접속시험.py
test-passwords: build
	$(PYTHON) መሳሪያዎች/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter መረብ_ክምር -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) መሳሪያዎች/ግንብ_ስርዓት.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) መሳሪያዎች/COSL배포.py check
cosl-dist: build
	$(PYTHON) መሳሪያዎች/ፍጠር_ምስል.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) መሳሪያዎች/COSL배포.py bundle
	$(PYTHON) መሳሪያዎች/재연결시험.py
desktop: build
	$(PYTHON) መሳሪያዎች/ፈጽም_ትእዛዝ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) መሳሪያዎች/셸시험.py
test-windows: build
	$(PYTHON) መሳሪያዎች/창시험.py
test-swing: build
	$(PYTHON) መሳሪያዎች/화면요소시험.py
test-stream: build
	$(PYTHON) መሳሪያዎች/흐름시험.py
test-ftp: build
	$(PYTHON) መሳሪያዎች/파일전송시험.py
test-elf: build
	$(PYTHON) መሳሪያዎች/실행파일시험.py
test-examples: build
	$(PYTHON) መሳሪያዎች/예제시험.py
network: build
	$(PYTHON) መሳሪያዎች/ፈጽም_ትእዛዝ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) መሳሪያዎች/코딩시험.py
test-desktop: build
	$(PYTHON) መሳሪያዎች/바탕화면시험.py
run: build
	$(PYTHON) መሳሪያዎች/ፈጽም_ትእዛዝ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) መሳሪያዎች/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) መሳሪያዎች/한글입력시험.py
	$(PYTHON) መሳሪያዎች/셸시험.py
	$(PYTHON) መሳሪያዎች/바탕화면시험.py
	$(PYTHON) መሳሪያዎች/창시험.py
	$(PYTHON) መሳሪያዎች/화면요소시험.py
	$(PYTHON) መሳሪያዎች/흐름시험.py
	$(PYTHON) መሳሪያዎች/코딩시험.py
	$(PYTHON) መሳሪያዎች/자바가상기계시험.py
	$(PYTHON) መሳሪያዎች/부팅시험.py
	$(PYTHON) መሳሪያዎች/꾸러미시험.py
	$(PYTHON) መሳሪያዎች/해상도시험.py
	$(PYTHON) መሳሪያዎች/창크기시험.py
image: build
	$(PYTHON) መሳሪያዎች/ፍጠር_ምስል.py --resolution $(RESOLUTION)
	$(PYTHON) መሳሪያዎች/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) መሳሪያዎች/개발꾸러미내보내기.py

.PHONY: 모두 ግንብ_ስርዓት ፈጽም_ትእዛዝ 시험 통신 ዴስክቶፕ_እየው ምስል_እሴት 개발꾸러미
모두: all
ግንብ_ስርዓት: build
ፈጽም_ትእዛዝ: run
시험: test
통신: network
ዴስክቶፕ_እየው: desktop
ምስል_እሴት: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) መሳሪያዎች/부팅시험.py
test-remmina: build
	$(PYTHON) መሳሪያዎች/원격한글시험.py
test-naming:
	$(PYTHON) መሳሪያዎች/명명검사.py --시언어
	$(PYTHON) መሳሪያዎች/직접호출검사.py
	$(PYTHON) መሳሪያዎች/ምንጭ_ክለሳ.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) መሳሪያዎች/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) መሳሪያዎች/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) መሳሪያዎች/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) መሳሪያዎች/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) መሳሪያዎች/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) መሳሪያዎች/실행계층점검.py

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
