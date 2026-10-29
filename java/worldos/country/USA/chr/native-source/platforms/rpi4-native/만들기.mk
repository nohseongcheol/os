PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords 원격접속
remote: build
	$(PYTHON) 도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py --remote --resolution $(RESOLUTION) $(ARGS)
원격접속: remote
test-remote: build
	$(PYTHON) 도구/원격접속시험.py
test-passwords: build
	$(PYTHON) 도구/ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏱᎦᏅᎯᏓ_ᎠᏓᎪᎵᏰᏍᎩ.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter 통신망 -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) 도구/ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) 도구/COSL배포.py check
cosl-dist: build
	$(PYTHON) 도구/영상만들기.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) 도구/COSL배포.py bundle
	$(PYTHON) 도구/재연결시험.py
desktop: build
	$(PYTHON) 도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎤᏯᏍᎦ.py
test-windows: build
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_Windows.py
test-swing: build
	$(PYTHON) 도구/화면요소시험.py
test-stream: build
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎤᏪᎬ.py
test-ftp: build
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_FTP.py
test-elf: build
	$(PYTHON) 도구/실행파일시험.py
test-examples: build
	$(PYTHON) 도구/예제시험.py
network: build
	$(PYTHON) 도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) 도구/코딩시험.py
test-desktop: build
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏍᎩᎶᎩ_ᎦᏚ.py
run: build
	$(PYTHON) 도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) 도구/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) 도구/한글입력시험.py
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎤᏯᏍᎦ.py
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏍᎩᎶᎩ_ᎦᏚ.py
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_Windows.py
	$(PYTHON) 도구/화면요소시험.py
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎤᏪᎬ.py
	$(PYTHON) 도구/코딩시험.py
	$(PYTHON) 도구/자바가상기계시험.py
	$(PYTHON) 도구/부팅시험.py
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ.py
	$(PYTHON) 도구/ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ.py
	$(PYTHON) 도구/창크기시험.py
image: build
	$(PYTHON) 도구/영상만들기.py --resolution $(RESOLUTION)
	$(PYTHON) 도구/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) 도구/개발꾸러미내보내기.py

.PHONY: 모두 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 시험 통신 ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ 개발꾸러미
모두: all
ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ: build
ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ: run
시험: test
통신: network
ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ: desktop
ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) 도구/부팅시험.py
test-remmina: build
	$(PYTHON) 도구/원격한글시험.py
test-naming:
	$(PYTHON) 도구/명명검사.py --시언어
	$(PYTHON) 도구/직접호출검사.py
	$(PYTHON) 도구/ᎦᏟᏌᏅᎯ_ᏘᎪᎵᏯ.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) 도구/ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) 도구/ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᎠᏓᎪᎵᏰᏍᎩ.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) 도구/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) 도구/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) 도구/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) 도구/실행계층점검.py

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
