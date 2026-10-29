PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords na_nesa_HAƊI
remote: build
	$(PYTHON) Kaya/gudanar_Umarni.py --remote --resolution $(RESOLUTION) $(ARGS)
na_nesa_HAƊI: remote
test-remote: build
	$(PYTHON) Kaya/원격접속시험.py
test-passwords: build
	$(PYTHON) Kaya/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Hanyar_sadarwa_tara -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Kaya/Gina_na_ura.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Kaya/COSL배포.py check
cosl-dist: build
	$(PYTHON) Kaya/ƙirƙíra_Hoto.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Kaya/COSL배포.py bundle
	$(PYTHON) Kaya/재연결시험.py
desktop: build
	$(PYTHON) Kaya/gudanar_Umarni.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Kaya/셸시험.py
test-windows: build
	$(PYTHON) Kaya/창시험.py
test-swing: build
	$(PYTHON) Kaya/화면요소시험.py
test-stream: build
	$(PYTHON) Kaya/흐름시험.py
test-ftp: build
	$(PYTHON) Kaya/파일전송시험.py
test-elf: build
	$(PYTHON) Kaya/실행파일시험.py
test-examples: build
	$(PYTHON) Kaya/예제시험.py
network: build
	$(PYTHON) Kaya/gudanar_Umarni.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Kaya/코딩시험.py
test-desktop: build
	$(PYTHON) Kaya/바탕화면시험.py
run: build
	$(PYTHON) Kaya/gudanar_Umarni.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Kaya/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Kaya/한글입력시험.py
	$(PYTHON) Kaya/셸시험.py
	$(PYTHON) Kaya/바탕화면시험.py
	$(PYTHON) Kaya/창시험.py
	$(PYTHON) Kaya/화면요소시험.py
	$(PYTHON) Kaya/흐름시험.py
	$(PYTHON) Kaya/코딩시험.py
	$(PYTHON) Kaya/자바가상기계시험.py
	$(PYTHON) Kaya/부팅시험.py
	$(PYTHON) Kaya/꾸러미시험.py
	$(PYTHON) Kaya/해상도시험.py
	$(PYTHON) Kaya/창크기시험.py
image: build
	$(PYTHON) Kaya/ƙirƙíra_Hoto.py --resolution $(RESOLUTION)
	$(PYTHON) Kaya/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Kaya/개발꾸러미내보내기.py

.PHONY: 모두 Gina_na_ura gudanar_Umarni 시험 통신 destof_s Hoto_Daraja 개발꾸러미
모두: all
Gina_na_ura: build
gudanar_Umarni: run
시험: test
통신: network
destof_s: desktop
Hoto_Daraja: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Kaya/부팅시험.py
test-remmina: build
	$(PYTHON) Kaya/원격한글시험.py
test-naming:
	$(PYTHON) Kaya/명명검사.py --시언어
	$(PYTHON) Kaya/직접호출검사.py
	$(PYTHON) Kaya/tushe_bita.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Kaya/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Kaya/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Kaya/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Kaya/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Kaya/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Kaya/실행계층점검.py

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
