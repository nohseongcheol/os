PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords jauh_CONNECT
remote: build
	$(PYTHON) alat/laksanakan_perintah.py --remote --resolution $(RESOLUTION) $(ARGS)
jauh_CONNECT: remote
test-remote: build
	$(PYTHON) alat/sambungan_jauh_ujian.py
test-passwords: build
	$(PYTHON) alat/kata_laluan_kepanjangan_ujian.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter rangkaian_tindan -I vendor/lwip/src/include ujian/berwayar_rangkaian_ujian.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) alat/bina_sistem.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) alat/COSL배포.py check
cosl-dist: build
	$(PYTHON) alat/cipta_imej.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) alat/COSL배포.py bundle
	$(PYTHON) alat/재연결시험.py
desktop: build
	$(PYTHON) alat/laksanakan_perintah.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) alat/ujian_cangkerang.py
test-windows: build
	$(PYTHON) alat/ujian_Windows.py
test-swing: build
	$(PYTHON) alat/화면요소시험.py
test-stream: build
	$(PYTHON) alat/ujian_strim.py
test-ftp: build
	$(PYTHON) alat/ujian_FTP.py
test-elf: build
	$(PYTHON) alat/실행파일시험.py
test-examples: build
	$(PYTHON) alat/예제시험.py
network: build
	$(PYTHON) alat/laksanakan_perintah.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) alat/코딩시험.py
test-desktop: build
	$(PYTHON) alat/ujian_meja.py
run: build
	$(PYTHON) alat/laksanakan_perintah.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) alat/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) alat/한글입력시험.py
	$(PYTHON) alat/ujian_cangkerang.py
	$(PYTHON) alat/ujian_meja.py
	$(PYTHON) alat/ujian_Windows.py
	$(PYTHON) alat/화면요소시험.py
	$(PYTHON) alat/ujian_strim.py
	$(PYTHON) alat/코딩시험.py
	$(PYTHON) alat/자바가상기계시험.py
	$(PYTHON) alat/부팅시험.py
	$(PYTHON) alat/ujian_pakej.py
	$(PYTHON) alat/resolusi_ujian.py
	$(PYTHON) alat/창크기시험.py
image: build
	$(PYTHON) alat/cipta_imej.py --resolution $(RESOLUTION)
	$(PYTHON) alat/Eksport_SDK.py
sdk: build
	$(PYTHON) alat/Eksport_SDK.py

.PHONY: 모두 bina_sistem laksanakan_perintah ujian 통신 meja_lihat imej_VALUE 개발꾸러미
모두: all
bina_sistem: build
laksanakan_perintah: run
ujian: test
통신: network
meja_lihat: desktop
imej_VALUE: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) alat/부팅시험.py
test-remmina: build
	$(PYTHON) alat/원격한글시험.py
test-naming:
	$(PYTHON) alat/명명검사.py --C_Bahasa
	$(PYTHON) alat/직접호출검사.py
	$(PYTHON) alat/sumber_ulasan.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) alat/ujian_pakej.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) alat/resolusi_ujian.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) alat/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) alat/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) alat/ujian_sistem_Alat.py

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
