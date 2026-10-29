PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords fjern_Forbind
remote: build
	$(PYTHON) Værktøjer/Udfør_kommando.py --remote --resolution $(RESOLUTION) $(ARGS)
fjern_Forbind: remote
test-remote: build
	$(PYTHON) Værktøjer/fjernforbindelse_test.py
test-passwords: build
	$(PYTHON) Værktøjer/adgangskode_varighed_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter netværk_Stak -I vendor/lwip/src/include 시험/traditionel_netværk_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Værktøjer/build_System.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Værktøjer/COSL배포.py check
cosl-dist: build
	$(PYTHON) Værktøjer/åbne_Image.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Værktøjer/COSL배포.py bundle
	$(PYTHON) Værktøjer/재연결시험.py
desktop: build
	$(PYTHON) Værktøjer/Udfør_kommando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Værktøjer/test_Shell.py
test-windows: build
	$(PYTHON) Værktøjer/test_Windows.py
test-swing: build
	$(PYTHON) Værktøjer/test_Swing.py
test-stream: build
	$(PYTHON) Værktøjer/test_strøm.py
test-ftp: build
	$(PYTHON) Værktøjer/test_FTP.py
test-elf: build
	$(PYTHON) Værktøjer/실행파일시험.py
test-examples: build
	$(PYTHON) Værktøjer/예제시험.py
network: build
	$(PYTHON) Værktøjer/Udfør_kommando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Værktøjer/코딩시험.py
test-desktop: build
	$(PYTHON) Værktøjer/test_desktop.py
run: build
	$(PYTHON) Værktøjer/Udfør_kommando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Værktøjer/test_JVM.py
test: build test-compiler
	$(PYTHON) Værktøjer/한글입력시험.py
	$(PYTHON) Værktøjer/test_Shell.py
	$(PYTHON) Værktøjer/test_desktop.py
	$(PYTHON) Værktøjer/test_Windows.py
	$(PYTHON) Værktøjer/test_Swing.py
	$(PYTHON) Værktøjer/test_strøm.py
	$(PYTHON) Værktøjer/코딩시험.py
	$(PYTHON) Værktøjer/test_JVM.py
	$(PYTHON) Værktøjer/부팅시험.py
	$(PYTHON) Værktøjer/test_bundt.py
	$(PYTHON) Værktøjer/opløsning_test.py
	$(PYTHON) Værktøjer/창크기시험.py
image: build
	$(PYTHON) Værktøjer/åbne_Image.py --resolution $(RESOLUTION)
	$(PYTHON) Værktøjer/eksportere_SDK.py
sdk: build
	$(PYTHON) Værktøjer/eksportere_SDK.py

.PHONY: 모두 build_System Udfør_kommando 시험 통신 desktop_Visning Image_VÆRDI Development_Kit
모두: all
build_System: build
Udfør_kommando: run
시험: test
통신: network
desktop_Visning: desktop
Image_VÆRDI: image
Development_Kit: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Værktøjer/부팅시험.py
test-remmina: build
	$(PYTHON) Værktøjer/원격한글시험.py
test-naming:
	$(PYTHON) Værktøjer/명명검사.py --C_Sprog
	$(PYTHON) Værktøjer/직접호출검사.py
	$(PYTHON) Værktøjer/kilde_gennemse.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Værktøjer/test_bundt.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Værktøjer/opløsning_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Værktøjer/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Værktøjer/skærmbillede_opdatere_test.py

.PHONY: test-system
test-system: build
	$(PYTHON) Værktøjer/test_System_Værktøjer.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Værktøjer/실행계층점검.py

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
