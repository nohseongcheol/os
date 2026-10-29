PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords távoli_KAPCSOLAT
remote: build
	$(PYTHON) Eszközök/végrehajt_parancs.py --remote --resolution $(RESOLUTION) $(ARGS)
távoli_KAPCSOLAT: remote
test-remote: build
	$(PYTHON) Eszközök/távoli_kapcsolat_teszt.py
test-passwords: build
	$(PYTHON) Eszközök/jelszó_hossz_teszt.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter hálózat_Sor -I vendor/lwip/src/include 시험/vezetékes_hálózat_teszt.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Eszközök/épít_Rendszer.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Eszközök/COSL배포.py check
cosl-dist: build
	$(PYTHON) Eszközök/készít_KÉP.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Eszközök/COSL배포.py bundle
	$(PYTHON) Eszközök/재연결시험.py
desktop: build
	$(PYTHON) Eszközök/végrehajt_parancs.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Eszközök/teszt_felület.py
test-windows: build
	$(PYTHON) Eszközök/teszt_Windows.py
test-swing: build
	$(PYTHON) Eszközök/teszt_Szving.py
test-stream: build
	$(PYTHON) Eszközök/teszt_Stream.py
test-ftp: build
	$(PYTHON) Eszközök/teszt_FTP.py
test-elf: build
	$(PYTHON) Eszközök/실행파일시험.py
test-examples: build
	$(PYTHON) Eszközök/예제시험.py
network: build
	$(PYTHON) Eszközök/végrehajt_parancs.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Eszközök/코딩시험.py
test-desktop: build
	$(PYTHON) Eszközök/teszt_Asztal.py
run: build
	$(PYTHON) Eszközök/végrehajt_parancs.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Eszközök/teszt_JVM.py
test: build test-compiler
	$(PYTHON) Eszközök/한글입력시험.py
	$(PYTHON) Eszközök/teszt_felület.py
	$(PYTHON) Eszközök/teszt_Asztal.py
	$(PYTHON) Eszközök/teszt_Windows.py
	$(PYTHON) Eszközök/teszt_Szving.py
	$(PYTHON) Eszközök/teszt_Stream.py
	$(PYTHON) Eszközök/코딩시험.py
	$(PYTHON) Eszközök/teszt_JVM.py
	$(PYTHON) Eszközök/부팅시험.py
	$(PYTHON) Eszközök/teszt_köteg.py
	$(PYTHON) Eszközök/felbontás_teszt.py
	$(PYTHON) Eszközök/창크기시험.py
image: build
	$(PYTHON) Eszközök/készít_KÉP.py --resolution $(RESOLUTION)
	$(PYTHON) Eszközök/exportál_SDK.py
sdk: build
	$(PYTHON) Eszközök/exportál_SDK.py

.PHONY: 모두 épít_Rendszer végrehajt_parancs 시험 kommunikáció Asztal_Nézet KÉP_ÉRTÉK fejlesztőkészlet
모두: all
épít_Rendszer: build
végrehajt_parancs: run
시험: test
kommunikáció: network
Asztal_Nézet: desktop
KÉP_ÉRTÉK: image
fejlesztőkészlet: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Eszközök/부팅시험.py
test-remmina: build
	$(PYTHON) Eszközök/원격한글시험.py
test-naming:
	$(PYTHON) Eszközök/명명검사.py --C_Nyelv
	$(PYTHON) Eszközök/직접호출검사.py
	$(PYTHON) Eszközök/forrás_vélemény.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Eszközök/teszt_köteg.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Eszközök/felbontás_teszt.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Eszközök/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Eszközök/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Eszközök/teszt_Rendszer_Eszközök.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Eszközök/실행계층점검.py

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
