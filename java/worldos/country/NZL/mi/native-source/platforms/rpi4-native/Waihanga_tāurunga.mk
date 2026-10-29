PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords mamao_TŪHONO
remote: build
	$(PYTHON) Ngā_Utauta/kawe_tono.py --remote --resolution $(RESOLUTION) $(ARGS)
mamao_TŪHONO: remote
test-remote: build
	$(PYTHON) Ngā_Utauta/원격접속시험.py
test-passwords: build
	$(PYTHON) Ngā_Utauta/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter whatunga_Huinga -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Ngā_Utauta/hanga_pūnaha.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Ngā_Utauta/COSL배포.py check
cosl-dist: build
	$(PYTHON) Ngā_Utauta/Waihanga_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Ngā_Utauta/COSL배포.py bundle
	$(PYTHON) Ngā_Utauta/재연결시험.py
desktop: build
	$(PYTHON) Ngā_Utauta/kawe_tono.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Ngā_Utauta/셸시험.py
test-windows: build
	$(PYTHON) Ngā_Utauta/창시험.py
test-swing: build
	$(PYTHON) Ngā_Utauta/화면요소시험.py
test-stream: build
	$(PYTHON) Ngā_Utauta/흐름시험.py
test-ftp: build
	$(PYTHON) Ngā_Utauta/파일전송시험.py
test-elf: build
	$(PYTHON) Ngā_Utauta/실행파일시험.py
test-examples: build
	$(PYTHON) Ngā_Utauta/예제시험.py
network: build
	$(PYTHON) Ngā_Utauta/kawe_tono.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Ngā_Utauta/코딩시험.py
test-desktop: build
	$(PYTHON) Ngā_Utauta/바탕화면시험.py
run: build
	$(PYTHON) Ngā_Utauta/kawe_tono.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Ngā_Utauta/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Ngā_Utauta/한글입력시험.py
	$(PYTHON) Ngā_Utauta/셸시험.py
	$(PYTHON) Ngā_Utauta/바탕화면시험.py
	$(PYTHON) Ngā_Utauta/창시험.py
	$(PYTHON) Ngā_Utauta/화면요소시험.py
	$(PYTHON) Ngā_Utauta/흐름시험.py
	$(PYTHON) Ngā_Utauta/코딩시험.py
	$(PYTHON) Ngā_Utauta/자바가상기계시험.py
	$(PYTHON) Ngā_Utauta/부팅시험.py
	$(PYTHON) Ngā_Utauta/꾸러미시험.py
	$(PYTHON) Ngā_Utauta/해상도시험.py
	$(PYTHON) Ngā_Utauta/창크기시험.py
image: build
	$(PYTHON) Ngā_Utauta/Waihanga_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Ngā_Utauta/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Ngā_Utauta/개발꾸러미내보내기.py

.PHONY: 모두 hanga_pūnaha kawe_tono 시험 통신 papamahi_tiro IMAGE_uara 개발꾸러미
모두: all
hanga_pūnaha: build
kawe_tono: run
시험: test
통신: network
papamahi_tiro: desktop
IMAGE_uara: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Ngā_Utauta/부팅시험.py
test-remmina: build
	$(PYTHON) Ngā_Utauta/원격한글시험.py
test-naming:
	$(PYTHON) Ngā_Utauta/명명검사.py --시언어
	$(PYTHON) Ngā_Utauta/직접호출검사.py
	$(PYTHON) Ngā_Utauta/pūtake_arotake.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Ngā_Utauta/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Ngā_Utauta/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Ngā_Utauta/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Ngā_Utauta/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Ngā_Utauta/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Ngā_Utauta/실행계층점검.py

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
