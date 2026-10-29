PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords oddaljen_POVEŽI
remote: build
	$(PYTHON) Orodja/Izvedi_ukaz.py --remote --resolution $(RESOLUTION) $(ARGS)
oddaljen_POVEŽI: remote
test-remote: build
	$(PYTHON) Orodja/oddaljena_povezava_preskusiti.py
test-passwords: build
	$(PYTHON) Orodja/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter mreža_Sklad -I vendor/lwip/src/include 시험/žičen_mreža_preskusiti.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Orodja/graditev_sistem.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Orodja/COSL배포.py check
cosl-dist: build
	$(PYTHON) Orodja/Ustvari_IMAGE.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Orodja/COSL배포.py bundle
	$(PYTHON) Orodja/재연결시험.py
desktop: build
	$(PYTHON) Orodja/Izvedi_ukaz.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Orodja/preskusiti_lupina.py
test-windows: build
	$(PYTHON) Orodja/preskusiti_Windows.py
test-swing: build
	$(PYTHON) Orodja/preskusiti_Swing.py
test-stream: build
	$(PYTHON) Orodja/preskusiti_tok.py
test-ftp: build
	$(PYTHON) Orodja/preskusiti_FTP.py
test-elf: build
	$(PYTHON) Orodja/실행파일시험.py
test-examples: build
	$(PYTHON) Orodja/예제시험.py
network: build
	$(PYTHON) Orodja/Izvedi_ukaz.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Orodja/코딩시험.py
test-desktop: build
	$(PYTHON) Orodja/preskusiti_namizje.py
run: build
	$(PYTHON) Orodja/Izvedi_ukaz.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Orodja/preskusiti_Javanski_navidezni_mehanizem.py
test: build test-compiler
	$(PYTHON) Orodja/한글입력시험.py
	$(PYTHON) Orodja/preskusiti_lupina.py
	$(PYTHON) Orodja/preskusiti_namizje.py
	$(PYTHON) Orodja/preskusiti_Windows.py
	$(PYTHON) Orodja/preskusiti_Swing.py
	$(PYTHON) Orodja/preskusiti_tok.py
	$(PYTHON) Orodja/코딩시험.py
	$(PYTHON) Orodja/preskusiti_Javanski_navidezni_mehanizem.py
	$(PYTHON) Orodja/부팅시험.py
	$(PYTHON) Orodja/preskusiti_sveženj.py
	$(PYTHON) Orodja/ločljivost_preskusiti.py
	$(PYTHON) Orodja/창크기시험.py
image: build
	$(PYTHON) Orodja/Ustvari_IMAGE.py --resolution $(RESOLUTION)
	$(PYTHON) Orodja/izvoziti_komplet_za_razvoj_programske_opreme.py
sdk: build
	$(PYTHON) Orodja/izvoziti_komplet_za_razvoj_programske_opreme.py

.PHONY: 모두 graditev_sistem Izvedi_ukaz 시험 통신 namizje_Pogled IMAGE_VALUE razvijalski_komplet
모두: all
graditev_sistem: build
Izvedi_ukaz: run
시험: test
통신: network
namizje_Pogled: desktop
IMAGE_VALUE: image
razvijalski_komplet: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Orodja/부팅시험.py
test-remmina: build
	$(PYTHON) Orodja/원격한글시험.py
test-naming:
	$(PYTHON) Orodja/명명검사.py --C_jezik
	$(PYTHON) Orodja/직접호출검사.py
	$(PYTHON) Orodja/vir_mnenje.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Orodja/preskusiti_sveženj.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Orodja/ločljivost_preskusiti.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Orodja/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Orodja/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Orodja/preskusiti_sistem_Orodja.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Orodja/실행계층점검.py

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
