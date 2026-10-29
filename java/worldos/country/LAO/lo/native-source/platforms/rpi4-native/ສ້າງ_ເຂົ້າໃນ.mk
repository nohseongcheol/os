PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ທາງ_ໄກ_ເຊື່ອມຕໍ່
remote: build
	$(PYTHON) ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py --remote --resolution $(RESOLUTION) $(ARGS)
ທາງ_ໄກ_ເຊື່ອມຕໍ່: remote
test-remote: build
	$(PYTHON) ເຄື່ອງມື/원격접속시험.py
test-passwords: build
	$(PYTHON) ເຄື່ອງມື/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ເຄືອຂ່າຍ_ກຸ່ມບັດ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ເຄື່ອງມື/ສ້າງ_ລະບົບ.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ເຄື່ອງມື/COSL배포.py check
cosl-dist: build
	$(PYTHON) ເຄື່ອງມື/ສ້າງ_ຮູບ.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ເຄື່ອງມື/COSL배포.py bundle
	$(PYTHON) ເຄື່ອງມື/재연결시험.py
desktop: build
	$(PYTHON) ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ເຄື່ອງມື/셸시험.py
test-windows: build
	$(PYTHON) ເຄື່ອງມື/창시험.py
test-swing: build
	$(PYTHON) ເຄື່ອງມື/화면요소시험.py
test-stream: build
	$(PYTHON) ເຄື່ອງມື/흐름시험.py
test-ftp: build
	$(PYTHON) ເຄື່ອງມື/파일전송시험.py
test-elf: build
	$(PYTHON) ເຄື່ອງມື/실행파일시험.py
test-examples: build
	$(PYTHON) ເຄື່ອງມື/예제시험.py
network: build
	$(PYTHON) ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ເຄື່ອງມື/코딩시험.py
test-desktop: build
	$(PYTHON) ເຄື່ອງມື/바탕화면시험.py
run: build
	$(PYTHON) ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ເຄື່ອງມື/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ເຄື່ອງມື/한글입력시험.py
	$(PYTHON) ເຄື່ອງມື/셸시험.py
	$(PYTHON) ເຄື່ອງມື/바탕화면시험.py
	$(PYTHON) ເຄື່ອງມື/창시험.py
	$(PYTHON) ເຄື່ອງມື/화면요소시험.py
	$(PYTHON) ເຄື່ອງມື/흐름시험.py
	$(PYTHON) ເຄື່ອງມື/코딩시험.py
	$(PYTHON) ເຄື່ອງມື/자바가상기계시험.py
	$(PYTHON) ເຄື່ອງມື/부팅시험.py
	$(PYTHON) ເຄື່ອງມື/꾸러미시험.py
	$(PYTHON) ເຄື່ອງມື/해상도시험.py
	$(PYTHON) ເຄື່ອງມື/창크기시험.py
image: build
	$(PYTHON) ເຄື່ອງມື/ສ້າງ_ຮູບ.py --resolution $(RESOLUTION)
	$(PYTHON) ເຄື່ອງມື/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ເຄື່ອງມື/개발꾸러미내보내기.py

.PHONY: 모두 ສ້າງ_ລະບົບ ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 시험 통신 ເດັສທັອບ_ເບິ່ງ ຮູບ_ຄ່າ 개발꾸러미
모두: all
ສ້າງ_ລະບົບ: build
ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ: run
시험: test
통신: network
ເດັສທັອບ_ເບິ່ງ: desktop
ຮູບ_ຄ່າ: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ເຄື່ອງມື/부팅시험.py
test-remmina: build
	$(PYTHON) ເຄື່ອງມື/원격한글시험.py
test-naming:
	$(PYTHON) ເຄື່ອງມື/명명검사.py --시언어
	$(PYTHON) ເຄື່ອງມື/직접호출검사.py
	$(PYTHON) ເຄື່ອງມື/ແຫຼ່ງທີ່ມາ_ທົບ_ທວນ_ຄືນ.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ເຄື່ອງມື/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ເຄື່ອງມື/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ເຄື່ອງມື/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ເຄື່ອງມື/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ເຄື່ອງມື/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ເຄື່ອງມື/실행계층점검.py

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
