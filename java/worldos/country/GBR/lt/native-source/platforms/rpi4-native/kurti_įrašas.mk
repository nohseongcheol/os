PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords nuotolinis_ryšys
remote: build
	$(PYTHON) Įrankiai/Vykdyti_komanda.py --remote --resolution $(RESOLUTION) $(ARGS)
nuotolinis_ryšys: remote
test-remote: build
	$(PYTHON) Įrankiai/원격접속시험.py
test-passwords: build
	$(PYTHON) Įrankiai/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter tinklas_eilė -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Įrankiai/kompiliuoti_sistema.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Įrankiai/COSL배포.py check
cosl-dist: build
	$(PYTHON) Įrankiai/kurti_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Įrankiai/COSL배포.py bundle
	$(PYTHON) Įrankiai/재연결시험.py
desktop: build
	$(PYTHON) Įrankiai/Vykdyti_komanda.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Įrankiai/셸시험.py
test-windows: build
	$(PYTHON) Įrankiai/창시험.py
test-swing: build
	$(PYTHON) Įrankiai/화면요소시험.py
test-stream: build
	$(PYTHON) Įrankiai/흐름시험.py
test-ftp: build
	$(PYTHON) Įrankiai/파일전송시험.py
test-elf: build
	$(PYTHON) Įrankiai/실행파일시험.py
test-examples: build
	$(PYTHON) Įrankiai/예제시험.py
network: build
	$(PYTHON) Įrankiai/Vykdyti_komanda.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Įrankiai/코딩시험.py
test-desktop: build
	$(PYTHON) Įrankiai/바탕화면시험.py
run: build
	$(PYTHON) Įrankiai/Vykdyti_komanda.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Įrankiai/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) Įrankiai/한글입력시험.py
	$(PYTHON) Įrankiai/셸시험.py
	$(PYTHON) Įrankiai/바탕화면시험.py
	$(PYTHON) Įrankiai/창시험.py
	$(PYTHON) Įrankiai/화면요소시험.py
	$(PYTHON) Įrankiai/흐름시험.py
	$(PYTHON) Įrankiai/코딩시험.py
	$(PYTHON) Įrankiai/자바가상기계시험.py
	$(PYTHON) Įrankiai/부팅시험.py
	$(PYTHON) Įrankiai/꾸러미시험.py
	$(PYTHON) Įrankiai/해상도시험.py
	$(PYTHON) Įrankiai/창크기시험.py
image: build
	$(PYTHON) Įrankiai/kurti_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Įrankiai/eksportuoti_SDK.py
sdk: build
	$(PYTHON) Įrankiai/eksportuoti_SDK.py

.PHONY: 모두 kompiliuoti_sistema Vykdyti_komanda 시험 통신 darbalaukis_rodyti IMAGE_VALUE programuotojo_rinkinys
모두: all
kompiliuoti_sistema: build
Vykdyti_komanda: run
시험: test
통신: network
darbalaukis_rodyti: desktop
IMAGE_VALUE: image
programuotojo_rinkinys: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Įrankiai/부팅시험.py
test-remmina: build
	$(PYTHON) Įrankiai/원격한글시험.py
test-naming:
	$(PYTHON) Įrankiai/명명검사.py --C_Kalba
	$(PYTHON) Įrankiai/직접호출검사.py
	$(PYTHON) Įrankiai/šaltinis_atsiliepimas.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Įrankiai/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Įrankiai/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Įrankiai/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Įrankiai/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Įrankiai/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Įrankiai/실행계층점검.py

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
