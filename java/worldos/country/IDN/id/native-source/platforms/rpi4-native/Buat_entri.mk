PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords jarak_jauh_CONNECT
remote: build
	$(PYTHON) alat/Jalankan_perintah.py --remote --resolution $(RESOLUTION) $(ARGS)
jarak_jauh_CONNECT: remote
test-remote: build
	$(PYTHON) alat/원격접속시험.py
test-passwords: build
	$(PYTHON) alat/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter jaringan_tumpuk -I vendor/lwip/src/include pengujian/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) alat/bangun.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) alat/COSL배포.py check
cosl-dist: build
	$(PYTHON) alat/Buat_foto.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) alat/COSL배포.py bundle
	$(PYTHON) alat/재연결시험.py
desktop: build
	$(PYTHON) alat/Jalankan_perintah.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) alat/셸시험.py
test-windows: build
	$(PYTHON) alat/창시험.py
test-swing: build
	$(PYTHON) alat/화면요소시험.py
test-stream: build
	$(PYTHON) alat/흐름시험.py
test-ftp: build
	$(PYTHON) alat/파일전송시험.py
test-elf: build
	$(PYTHON) alat/실행파일시험.py
test-examples: build
	$(PYTHON) alat/예제시험.py
network: build
	$(PYTHON) alat/Jalankan_perintah.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) alat/코딩시험.py
test-desktop: build
	$(PYTHON) alat/바탕화면시험.py
run: build
	$(PYTHON) alat/Jalankan_perintah.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) alat/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) alat/한글입력시험.py
	$(PYTHON) alat/셸시험.py
	$(PYTHON) alat/바탕화면시험.py
	$(PYTHON) alat/창시험.py
	$(PYTHON) alat/화면요소시험.py
	$(PYTHON) alat/흐름시험.py
	$(PYTHON) alat/코딩시험.py
	$(PYTHON) alat/자바가상기계시험.py
	$(PYTHON) alat/부팅시험.py
	$(PYTHON) alat/꾸러미시험.py
	$(PYTHON) alat/해상도시험.py
	$(PYTHON) alat/창크기시험.py
image: build
	$(PYTHON) alat/Buat_foto.py --resolution $(RESOLUTION)
	$(PYTHON) alat/Ekspor_SDK.py
sdk: build
	$(PYTHON) alat/Ekspor_SDK.py

.PHONY: 모두 bangun Jalankan_perintah pengujian komunikasi desktop_Tampilan foto_VALUE 개발꾸러미
모두: all
bangun: build
Jalankan_perintah: run
pengujian: test
komunikasi: network
desktop_Tampilan: desktop
foto_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) alat/부팅시험.py
test-remmina: build
	$(PYTHON) alat/원격한글시험.py
test-naming:
	$(PYTHON) alat/명명검사.py --시언어
	$(PYTHON) alat/직접호출검사.py
	$(PYTHON) alat/sumber_ulasan.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) alat/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) alat/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) alat/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) alat/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) alat/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) alat/실행계층점검.py

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
