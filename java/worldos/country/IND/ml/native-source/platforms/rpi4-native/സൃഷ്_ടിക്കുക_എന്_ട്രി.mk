PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords വിദൂര_കണക്റ്റ്
remote: build
	$(PYTHON) ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py --remote --resolution $(RESOLUTION) $(ARGS)
വിദൂര_കണക്റ്റ്: remote
test-remote: build
	$(PYTHON) ഉപകരണങ്ങൾ/원격접속시험.py
test-passwords: build
	$(PYTHON) ഉപകരണങ്ങൾ/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ഉപകരണങ്ങൾ/ബിൽഡ്_సిస్టమ్.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ഉപകരണങ്ങൾ/COSL배포.py check
cosl-dist: build
	$(PYTHON) ഉപകരണങ്ങൾ/സൃഷ്_ടിക്കുക_ഇമേജ്.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ഉപകരണങ്ങൾ/COSL배포.py bundle
	$(PYTHON) ഉപകരണങ്ങൾ/재연결시험.py
desktop: build
	$(PYTHON) ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ഉപകരണങ്ങൾ/셸시험.py
test-windows: build
	$(PYTHON) ഉപകരണങ്ങൾ/창시험.py
test-swing: build
	$(PYTHON) ഉപകരണങ്ങൾ/화면요소시험.py
test-stream: build
	$(PYTHON) ഉപകരണങ്ങൾ/흐름시험.py
test-ftp: build
	$(PYTHON) ഉപകരണങ്ങൾ/파일전송시험.py
test-elf: build
	$(PYTHON) ഉപകരണങ്ങൾ/실행파일시험.py
test-examples: build
	$(PYTHON) ഉപകരണങ്ങൾ/예제시험.py
network: build
	$(PYTHON) ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ഉപകരണങ്ങൾ/코딩시험.py
test-desktop: build
	$(PYTHON) ഉപകരണങ്ങൾ/바탕화면시험.py
run: build
	$(PYTHON) ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ഉപകരണങ്ങൾ/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ഉപകരണങ്ങൾ/한글입력시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/셸시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/바탕화면시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/창시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/화면요소시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/흐름시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/코딩시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/자바가상기계시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/부팅시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/꾸러미시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/해상도시험.py
	$(PYTHON) ഉപകരണങ്ങൾ/창크기시험.py
image: build
	$(PYTHON) ഉപകരണങ്ങൾ/സൃഷ്_ടിക്കുക_ഇമേജ്.py --resolution $(RESOLUTION)
	$(PYTHON) ഉപകരണങ്ങൾ/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ഉപകരണങ്ങൾ/개발꾸러미내보내기.py

.PHONY: 모두 ബിൽഡ്_సిస్టమ్ നടപ്പാക്കുക_കമാന്_ഡ് 시험 통신 ഡെസ്ക്ടോപ്പ്_കാഴ്ച ഇമേജ്_മൂല്യം 개발꾸러미
모두: all
ബിൽഡ്_సిస్టమ్: build
നടപ്പാക്കുക_കമാന്_ഡ്: run
시험: test
통신: network
ഡെസ്ക്ടോപ്പ്_കാഴ്ച: desktop
ഇമേജ്_മൂല്യം: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ഉപകരണങ്ങൾ/부팅시험.py
test-remmina: build
	$(PYTHON) ഉപകരണങ്ങൾ/원격한글시험.py
test-naming:
	$(PYTHON) ഉപകരണങ്ങൾ/명명검사.py --시언어
	$(PYTHON) ഉപകരണങ്ങൾ/직접호출검사.py
	$(PYTHON) ഉപകരണങ്ങൾ/ഉറവിടം_അവലോകനം.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ഉപകരണങ്ങൾ/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ഉപകരണങ്ങൾ/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ഉപകരണങ്ങൾ/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ഉപകരണങ്ങൾ/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ഉപകരണങ്ങൾ/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ഉപകരണങ്ങൾ/실행계층점검.py

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
