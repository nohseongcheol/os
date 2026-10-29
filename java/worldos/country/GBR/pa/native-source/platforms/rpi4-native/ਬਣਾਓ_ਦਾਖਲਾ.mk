PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ਰਿਮੋਟ_ਕਨੈਕਟ_ਕਰੋ
remote: build
	$(PYTHON) ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py --remote --resolution $(RESOLUTION) $(ARGS)
ਰਿਮੋਟ_ਕਨੈਕਟ_ਕਰੋ: remote
test-remote: build
	$(PYTHON) ਸਾਧਨ/원격접속시험.py
test-passwords: build
	$(PYTHON) ਸਾਧਨ/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ਨੈਟਵਰਕ_ਸਟੈਕ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ਸਾਧਨ/ਬਿਲਡ_ਪਰਬੰਧ.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ਸਾਧਨ/COSL배포.py check
cosl-dist: build
	$(PYTHON) ਸਾਧਨ/ਬਣਾਓ_ਤਸਵੀਰ.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ਸਾਧਨ/COSL배포.py bundle
	$(PYTHON) ਸਾਧਨ/재연결시험.py
desktop: build
	$(PYTHON) ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ਸਾਧਨ/셸시험.py
test-windows: build
	$(PYTHON) ਸਾਧਨ/창시험.py
test-swing: build
	$(PYTHON) ਸਾਧਨ/화면요소시험.py
test-stream: build
	$(PYTHON) ਸਾਧਨ/흐름시험.py
test-ftp: build
	$(PYTHON) ਸਾਧਨ/파일전송시험.py
test-elf: build
	$(PYTHON) ਸਾਧਨ/실행파일시험.py
test-examples: build
	$(PYTHON) ਸਾਧਨ/예제시험.py
network: build
	$(PYTHON) ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ਸਾਧਨ/코딩시험.py
test-desktop: build
	$(PYTHON) ਸਾਧਨ/바탕화면시험.py
run: build
	$(PYTHON) ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ਸਾਧਨ/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ਸਾਧਨ/한글입력시험.py
	$(PYTHON) ਸਾਧਨ/셸시험.py
	$(PYTHON) ਸਾਧਨ/바탕화면시험.py
	$(PYTHON) ਸਾਧਨ/창시험.py
	$(PYTHON) ਸਾਧਨ/화면요소시험.py
	$(PYTHON) ਸਾਧਨ/흐름시험.py
	$(PYTHON) ਸਾਧਨ/코딩시험.py
	$(PYTHON) ਸਾਧਨ/자바가상기계시험.py
	$(PYTHON) ਸਾਧਨ/부팅시험.py
	$(PYTHON) ਸਾਧਨ/꾸러미시험.py
	$(PYTHON) ਸਾਧਨ/해상도시험.py
	$(PYTHON) ਸਾਧਨ/창크기시험.py
image: build
	$(PYTHON) ਸਾਧਨ/ਬਣਾਓ_ਤਸਵੀਰ.py --resolution $(RESOLUTION)
	$(PYTHON) ਸਾਧਨ/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ਸਾਧਨ/개발꾸러미내보내기.py

.PHONY: 모두 ਬਿਲਡ_ਪਰਬੰਧ ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 시험 통신 ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼ ਤਸਵੀਰ_ਕੀਮਤ 개발꾸러미
모두: all
ਬਿਲਡ_ਪਰਬੰਧ: build
ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼: run
시험: test
통신: network
ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼: desktop
ਤਸਵੀਰ_ਕੀਮਤ: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ਸਾਧਨ/부팅시험.py
test-remmina: build
	$(PYTHON) ਸਾਧਨ/원격한글시험.py
test-naming:
	$(PYTHON) ਸਾਧਨ/명명검사.py --시언어
	$(PYTHON) ਸਾਧਨ/직접호출검사.py
	$(PYTHON) ਸਾਧਨ/ਸਰੋਤ_ਸਮੀਖਿਆ.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ਸਾਧਨ/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ਸਾਧਨ/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ਸਾਧਨ/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ਸਾਧਨ/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ਸਾਧਨ/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ਸਾਧਨ/실행계층점검.py

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
