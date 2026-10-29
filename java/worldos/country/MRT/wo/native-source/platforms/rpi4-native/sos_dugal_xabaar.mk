PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords lu_soree_JOKKOO
remote: build
	$(PYTHON) Jumtukaay_yi/def_ndigel.py --remote --resolution $(RESOLUTION) $(ARGS)
lu_soree_JOKKOO: remote
test-remote: build
	$(PYTHON) Jumtukaay_yi/원격접속시험.py
test-passwords: build
	$(PYTHON) Jumtukaay_yi/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter mbaal_Tegalo -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Jumtukaay_yi/tabax_kureel.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Jumtukaay_yi/COSL배포.py check
cosl-dist: build
	$(PYTHON) Jumtukaay_yi/sos_nataal.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Jumtukaay_yi/COSL배포.py bundle
	$(PYTHON) Jumtukaay_yi/재연결시험.py
desktop: build
	$(PYTHON) Jumtukaay_yi/def_ndigel.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Jumtukaay_yi/셸시험.py
test-windows: build
	$(PYTHON) Jumtukaay_yi/창시험.py
test-swing: build
	$(PYTHON) Jumtukaay_yi/화면요소시험.py
test-stream: build
	$(PYTHON) Jumtukaay_yi/흐름시험.py
test-ftp: build
	$(PYTHON) Jumtukaay_yi/파일전송시험.py
test-elf: build
	$(PYTHON) Jumtukaay_yi/실행파일시험.py
test-examples: build
	$(PYTHON) Jumtukaay_yi/예제시험.py
network: build
	$(PYTHON) Jumtukaay_yi/def_ndigel.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Jumtukaay_yi/코딩시험.py
test-desktop: build
	$(PYTHON) Jumtukaay_yi/바탕화면시험.py
run: build
	$(PYTHON) Jumtukaay_yi/def_ndigel.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Jumtukaay_yi/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Jumtukaay_yi/한글입력시험.py
	$(PYTHON) Jumtukaay_yi/셸시험.py
	$(PYTHON) Jumtukaay_yi/바탕화면시험.py
	$(PYTHON) Jumtukaay_yi/창시험.py
	$(PYTHON) Jumtukaay_yi/화면요소시험.py
	$(PYTHON) Jumtukaay_yi/흐름시험.py
	$(PYTHON) Jumtukaay_yi/코딩시험.py
	$(PYTHON) Jumtukaay_yi/자바가상기계시험.py
	$(PYTHON) Jumtukaay_yi/부팅시험.py
	$(PYTHON) Jumtukaay_yi/꾸러미시험.py
	$(PYTHON) Jumtukaay_yi/해상도시험.py
	$(PYTHON) Jumtukaay_yi/창크기시험.py
image: build
	$(PYTHON) Jumtukaay_yi/sos_nataal.py --resolution $(RESOLUTION)
	$(PYTHON) Jumtukaay_yi/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Jumtukaay_yi/개발꾸러미내보내기.py

.PHONY: 모두 tabax_kureel def_ndigel 시험 통신 Biro_wonin nataal_xëyma 개발꾸러미
모두: all
tabax_kureel: build
def_ndigel: run
시험: test
통신: network
Biro_wonin: desktop
nataal_xëyma: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Jumtukaay_yi/부팅시험.py
test-remmina: build
	$(PYTHON) Jumtukaay_yi/원격한글시험.py
test-naming:
	$(PYTHON) Jumtukaay_yi/명명검사.py --시언어
	$(PYTHON) Jumtukaay_yi/직접호출검사.py
	$(PYTHON) Jumtukaay_yi/Cosaan_jàngat.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Jumtukaay_yi/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Jumtukaay_yi/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Jumtukaay_yi/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Jumtukaay_yi/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Jumtukaay_yi/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Jumtukaay_yi/실행계층점검.py

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
