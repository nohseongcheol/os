PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords udaljen_veze
remote: build
	$(PYTHON) Alatke/Izvrši_komanda.py --remote --resolution $(RESOLUTION) $(ARGS)
udaljen_veze: remote
test-remote: build
	$(PYTHON) Alatke/원격접속시험.py
test-passwords: build
	$(PYTHON) Alatke/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Mreža_stek -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Alatke/verzija_sistem.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Alatke/COSL배포.py check
cosl-dist: build
	$(PYTHON) Alatke/Create_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Alatke/COSL배포.py bundle
	$(PYTHON) Alatke/재연결시험.py
desktop: build
	$(PYTHON) Alatke/Izvrši_komanda.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Alatke/셸시험.py
test-windows: build
	$(PYTHON) Alatke/창시험.py
test-swing: build
	$(PYTHON) Alatke/화면요소시험.py
test-stream: build
	$(PYTHON) Alatke/흐름시험.py
test-ftp: build
	$(PYTHON) Alatke/파일전송시험.py
test-elf: build
	$(PYTHON) Alatke/실행파일시험.py
test-examples: build
	$(PYTHON) Alatke/예제시험.py
network: build
	$(PYTHON) Alatke/Izvrši_komanda.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Alatke/코딩시험.py
test-desktop: build
	$(PYTHON) Alatke/바탕화면시험.py
run: build
	$(PYTHON) Alatke/Izvrši_komanda.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Alatke/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Alatke/한글입력시험.py
	$(PYTHON) Alatke/셸시험.py
	$(PYTHON) Alatke/바탕화면시험.py
	$(PYTHON) Alatke/창시험.py
	$(PYTHON) Alatke/화면요소시험.py
	$(PYTHON) Alatke/흐름시험.py
	$(PYTHON) Alatke/코딩시험.py
	$(PYTHON) Alatke/자바가상기계시험.py
	$(PYTHON) Alatke/부팅시험.py
	$(PYTHON) Alatke/꾸러미시험.py
	$(PYTHON) Alatke/해상도시험.py
	$(PYTHON) Alatke/창크기시험.py
image: build
	$(PYTHON) Alatke/Create_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Alatke/izvesti_SDK.py
sdk: build
	$(PYTHON) Alatke/izvesti_SDK.py

.PHONY: 모두 verzija_sistem Izvrši_komanda 시험 통신 desktop_Prikaz IMAGE_VALUE komplet_za_razvoj_programa
모두: all
verzija_sistem: build
Izvrši_komanda: run
시험: test
통신: network
desktop_Prikaz: desktop
IMAGE_VALUE: image
komplet_za_razvoj_programa: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Alatke/부팅시험.py
test-remmina: build
	$(PYTHON) Alatke/원격한글시험.py
test-naming:
	$(PYTHON) Alatke/명명검사.py --C_jezik
	$(PYTHON) Alatke/직접호출검사.py
	$(PYTHON) Alatke/izvor_komentar.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Alatke/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Alatke/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Alatke/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Alatke/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Alatke/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Alatke/실행계층점검.py

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
