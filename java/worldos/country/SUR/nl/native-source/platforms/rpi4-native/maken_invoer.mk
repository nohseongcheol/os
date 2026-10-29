PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords extern_VERBINDEN
remote: build
	$(PYTHON) hulpmiddelen/Uitvoeren_opdracht.py --remote --resolution $(RESOLUTION) $(ARGS)
extern_VERBINDEN: remote
test-remote: build
	$(PYTHON) hulpmiddelen/externe_verbinding_test.py
test-passwords: build
	$(PYTHON) hulpmiddelen/wachtwoord_tijdsduur_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter net_stack -I vendor/lwip/src/include tests/bekabeld_net_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) hulpmiddelen/bouwen.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) hulpmiddelen/COSL배포.py check
cosl-dist: build
	$(PYTHON) hulpmiddelen/maken_kopie.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) hulpmiddelen/COSL배포.py bundle
	$(PYTHON) hulpmiddelen/재연결시험.py
desktop: build
	$(PYTHON) hulpmiddelen/Uitvoeren_opdracht.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) hulpmiddelen/test_Shell.py
test-windows: build
	$(PYTHON) hulpmiddelen/test_Windows.py
test-swing: build
	$(PYTHON) hulpmiddelen/test_Swing.py
test-stream: build
	$(PYTHON) hulpmiddelen/test_Stream.py
test-ftp: build
	$(PYTHON) hulpmiddelen/test_FTP.py
test-elf: build
	$(PYTHON) hulpmiddelen/실행파일시험.py
test-examples: build
	$(PYTHON) hulpmiddelen/예제시험.py
network: build
	$(PYTHON) hulpmiddelen/Uitvoeren_opdracht.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) hulpmiddelen/코딩시험.py
test-desktop: build
	$(PYTHON) hulpmiddelen/test_pc.py
run: build
	$(PYTHON) hulpmiddelen/Uitvoeren_opdracht.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) hulpmiddelen/test_JVM.py
test: build test-compiler
	$(PYTHON) hulpmiddelen/한글입력시험.py
	$(PYTHON) hulpmiddelen/test_Shell.py
	$(PYTHON) hulpmiddelen/test_pc.py
	$(PYTHON) hulpmiddelen/test_Windows.py
	$(PYTHON) hulpmiddelen/test_Swing.py
	$(PYTHON) hulpmiddelen/test_Stream.py
	$(PYTHON) hulpmiddelen/코딩시험.py
	$(PYTHON) hulpmiddelen/test_JVM.py
	$(PYTHON) hulpmiddelen/부팅시험.py
	$(PYTHON) hulpmiddelen/test_bundel.py
	$(PYTHON) hulpmiddelen/resolutie_test.py
	$(PYTHON) hulpmiddelen/창크기시험.py
image: build
	$(PYTHON) hulpmiddelen/maken_kopie.py --resolution $(RESOLUTION)
	$(PYTHON) hulpmiddelen/exporteren_SDK.py
sdk: build
	$(PYTHON) hulpmiddelen/exporteren_SDK.py

.PHONY: 모두 bouwen Uitvoeren_opdracht tests communicatie pc_Weergave kopie_WAARDE Development_Kit
모두: all
bouwen: build
Uitvoeren_opdracht: run
tests: test
communicatie: network
pc_Weergave: desktop
kopie_WAARDE: image
Development_Kit: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) hulpmiddelen/부팅시험.py
test-remmina: build
	$(PYTHON) hulpmiddelen/원격한글시험.py
test-naming:
	$(PYTHON) hulpmiddelen/명명검사.py --C_Taal
	$(PYTHON) hulpmiddelen/직접호출검사.py
	$(PYTHON) hulpmiddelen/bron_beoordeling.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) hulpmiddelen/test_bundel.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) hulpmiddelen/resolutie_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) hulpmiddelen/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) hulpmiddelen/scherm_vernieuwen_test.py

.PHONY: test-system
test-system: build
	$(PYTHON) hulpmiddelen/test_Systeem_Hulpprogramma_s.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) hulpmiddelen/실행계층점검.py

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
