PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords రిమోట్_అనుసంధానించు
remote: build
	$(PYTHON) ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py --remote --resolution $(RESOLUTION) $(ARGS)
రిమోట్_అనుసంధానించు: remote
test-remote: build
	$(PYTHON) ఉపకరణాలు/원격접속시험.py
test-passwords: build
	$(PYTHON) ఉపకరణాలు/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter నెట్_వర్క్_దొంతర -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ఉపకరణాలు/బిల్డ్_సిస్టం.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ఉపకరణాలు/COSL배포.py check
cosl-dist: build
	$(PYTHON) ఉపకరణాలు/క్రియేట్_చిత్రం.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ఉపకరణాలు/COSL배포.py bundle
	$(PYTHON) ఉపకరణాలు/재연결시험.py
desktop: build
	$(PYTHON) ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ఉపకరణాలు/셸시험.py
test-windows: build
	$(PYTHON) ఉపకరణాలు/창시험.py
test-swing: build
	$(PYTHON) ఉపకరణాలు/화면요소시험.py
test-stream: build
	$(PYTHON) ఉపకరణాలు/흐름시험.py
test-ftp: build
	$(PYTHON) ఉపకరణాలు/파일전송시험.py
test-elf: build
	$(PYTHON) ఉపకరణాలు/실행파일시험.py
test-examples: build
	$(PYTHON) ఉపకరణాలు/예제시험.py
network: build
	$(PYTHON) ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ఉపకరణాలు/코딩시험.py
test-desktop: build
	$(PYTHON) ఉపకరణాలు/바탕화면시험.py
run: build
	$(PYTHON) ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ఉపకరణాలు/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ఉపకరణాలు/한글입력시험.py
	$(PYTHON) ఉపకరణాలు/셸시험.py
	$(PYTHON) ఉపకరణాలు/바탕화면시험.py
	$(PYTHON) ఉపకరణాలు/창시험.py
	$(PYTHON) ఉపకరణాలు/화면요소시험.py
	$(PYTHON) ఉపకరణాలు/흐름시험.py
	$(PYTHON) ఉపకరణాలు/코딩시험.py
	$(PYTHON) ఉపకరణాలు/자바가상기계시험.py
	$(PYTHON) ఉపకరణాలు/부팅시험.py
	$(PYTHON) ఉపకరణాలు/꾸러미시험.py
	$(PYTHON) ఉపకరణాలు/해상도시험.py
	$(PYTHON) ఉపకరణాలు/창크기시험.py
image: build
	$(PYTHON) ఉపకరణాలు/క్రియేట్_చిత్రం.py --resolution $(RESOLUTION)
	$(PYTHON) ఉపకరణాలు/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ఉపకరణాలు/개발꾸러미내보내기.py

.PHONY: 모두 బిల్డ్_సిస్టం అమలు_చేయి_ఆదేశం 시험 통신 డెస్క్_టాప్_వీక్షణ చిత్రం_మూల్యం 개발꾸러미
모두: all
బిల్డ్_సిస్టం: build
అమలు_చేయి_ఆదేశం: run
시험: test
통신: network
డెస్క్_టాప్_వీక్షణ: desktop
చిత్రం_మూల్యం: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ఉపకరణాలు/부팅시험.py
test-remmina: build
	$(PYTHON) ఉపకరణాలు/원격한글시험.py
test-naming:
	$(PYTHON) ఉపకరణాలు/명명검사.py --시언어
	$(PYTHON) ఉపకరణాలు/직접호출검사.py
	$(PYTHON) ఉపకరణాలు/మూలం_సమీక్ష.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ఉపకరణాలు/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ఉపకరణాలు/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ఉపకరణాలు/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ఉపకరణాలు/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ఉపకరణాలు/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ఉపకరణాలు/실행계층점검.py

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
