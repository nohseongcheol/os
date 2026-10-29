PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ពីចម្ងាយ_ភ្ជាប់
remote: build
	$(PYTHON) ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py --remote --resolution $(RESOLUTION) $(ARGS)
ពីចម្ងាយ_ភ្ជាប់: remote
test-remote: build
	$(PYTHON) ឧបករណ៍/원격접속시험.py
test-passwords: build
	$(PYTHON) ឧបករណ៍/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ណិតវឺក_គរ -I vendor/lwip/src/include 시험/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ឧបករណ៍/ចងក្រង_ប្រព័ន្ធ.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ឧបករណ៍/COSL배포.py check
cosl-dist: build
	$(PYTHON) ឧបករណ៍/បង្កើត_រូបថត.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ឧបករណ៍/COSL배포.py bundle
	$(PYTHON) ឧបករណ៍/재연결시험.py
desktop: build
	$(PYTHON) ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ឧបករណ៍/셸시험.py
test-windows: build
	$(PYTHON) ឧបករណ៍/창시험.py
test-swing: build
	$(PYTHON) ឧបករណ៍/화면요소시험.py
test-stream: build
	$(PYTHON) ឧបករណ៍/흐름시험.py
test-ftp: build
	$(PYTHON) ឧបករណ៍/파일전송시험.py
test-elf: build
	$(PYTHON) ឧបករណ៍/실행파일시험.py
test-examples: build
	$(PYTHON) ឧបករណ៍/예제시험.py
network: build
	$(PYTHON) ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ឧបករណ៍/코딩시험.py
test-desktop: build
	$(PYTHON) ឧបករណ៍/바탕화면시험.py
run: build
	$(PYTHON) ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ឧបករណ៍/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) ឧបករណ៍/한글입력시험.py
	$(PYTHON) ឧបករណ៍/셸시험.py
	$(PYTHON) ឧបករណ៍/바탕화면시험.py
	$(PYTHON) ឧបករណ៍/창시험.py
	$(PYTHON) ឧបករណ៍/화면요소시험.py
	$(PYTHON) ឧបករណ៍/흐름시험.py
	$(PYTHON) ឧបករណ៍/코딩시험.py
	$(PYTHON) ឧបករណ៍/자바가상기계시험.py
	$(PYTHON) ឧបករណ៍/부팅시험.py
	$(PYTHON) ឧបករណ៍/꾸러미시험.py
	$(PYTHON) ឧបករណ៍/해상도시험.py
	$(PYTHON) ឧបករណ៍/창크기시험.py
image: build
	$(PYTHON) ឧបករណ៍/បង្កើត_រូបថត.py --resolution $(RESOLUTION)
	$(PYTHON) ឧបករណ៍/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ឧបករណ៍/개발꾸러미내보내기.py

.PHONY: 모두 ចងក្រង_ប្រព័ន្ធ អនុវត្ត_ពាក្យបញ្ជា 시험 통신 ដែសថប_ការមើល រូបថត_តំលៃ 개발꾸러미
모두: all
ចងក្រង_ប្រព័ន្ធ: build
អនុវត្ត_ពាក្យបញ្ជា: run
시험: test
통신: network
ដែសថប_ការមើល: desktop
រូបថត_តំលៃ: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ឧបករណ៍/부팅시험.py
test-remmina: build
	$(PYTHON) ឧបករណ៍/원격한글시험.py
test-naming:
	$(PYTHON) ឧបករណ៍/명명검사.py --시언어
	$(PYTHON) ឧបករណ៍/직접호출검사.py
	$(PYTHON) ឧបករណ៍/ប្រភព_មើល_ឡើង_វិញ.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ឧបករណ៍/꾸러미시험.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ឧបករណ៍/해상도시험.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ឧបករណ៍/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ឧបករណ៍/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ឧបករណ៍/체계도구시험.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ឧបករណ៍/실행계층점검.py

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
