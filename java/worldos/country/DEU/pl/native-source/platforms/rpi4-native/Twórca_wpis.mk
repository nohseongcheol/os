PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords zdalny_POŁĄCZ
remote: build
	$(PYTHON) narzędzia/Wykonaj_polecenie.py --remote --resolution $(RESOLUTION) $(ARGS)
zdalny_POŁĄCZ: remote
test-remote: build
	$(PYTHON) narzędzia/połączenie_zdalne_test.py
test-passwords: build
	$(PYTHON) narzędzia/hasło_długość_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter sieć_Stos -I vendor/lwip/src/include testy/przewodowy_sieć_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) narzędzia/BLD_System.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) narzędzia/COSL배포.py check
cosl-dist: build
	$(PYTHON) narzędzia/Twórca_OBRAZ.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) narzędzia/COSL배포.py bundle
	$(PYTHON) narzędzia/재연결시험.py
desktop: build
	$(PYTHON) narzędzia/Wykonaj_polecenie.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) narzędzia/test_powłoka.py
test-windows: build
	$(PYTHON) narzędzia/test_Windows.py
test-swing: build
	$(PYTHON) narzędzia/test_Swing.py
test-stream: build
	$(PYTHON) narzędzia/test_Stream.py
test-ftp: build
	$(PYTHON) narzędzia/test_FTP.py
test-elf: build
	$(PYTHON) narzędzia/실행파일시험.py
test-examples: build
	$(PYTHON) narzędzia/예제시험.py
network: build
	$(PYTHON) narzędzia/Wykonaj_polecenie.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) narzędzia/코딩시험.py
test-desktop: build
	$(PYTHON) narzędzia/test_Pulpit.py
run: build
	$(PYTHON) narzędzia/Wykonaj_polecenie.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) narzędzia/test_JVM.py
test: build test-compiler
	$(PYTHON) narzędzia/한글입력시험.py
	$(PYTHON) narzędzia/test_powłoka.py
	$(PYTHON) narzędzia/test_Pulpit.py
	$(PYTHON) narzędzia/test_Windows.py
	$(PYTHON) narzędzia/test_Swing.py
	$(PYTHON) narzędzia/test_Stream.py
	$(PYTHON) narzędzia/코딩시험.py
	$(PYTHON) narzędzia/test_JVM.py
	$(PYTHON) narzędzia/부팅시험.py
	$(PYTHON) narzędzia/test_pakiet.py
	$(PYTHON) narzędzia/rozdzielczość_test.py
	$(PYTHON) narzędzia/test_okno_zmiana_rozmiaru.py
image: build
	$(PYTHON) narzędzia/Twórca_OBRAZ.py --resolution $(RESOLUTION)
	$(PYTHON) narzędzia/eksportować_SDK.py
sdk: build
	$(PYTHON) narzędzia/eksportować_SDK.py

.PHONY: 모두 BLD_System Wykonaj_polecenie testy komunikacja Pulpit_Widok OBRAZ_WARTOŚĆ zestaw_deweloperski
모두: all
BLD_System: build
Wykonaj_polecenie: run
testy: test
komunikacja: network
Pulpit_Widok: desktop
OBRAZ_WARTOŚĆ: image
zestaw_deweloperski: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) narzędzia/부팅시험.py
test-remmina: build
	$(PYTHON) narzędzia/원격한글시험.py
test-naming:
	$(PYTHON) narzędzia/명명검사.py --C_Język
	$(PYTHON) narzędzia/직접호출검사.py
	$(PYTHON) narzędzia/źródło_przegląd.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) narzędzia/test_pakiet.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) narzędzia/rozdzielczość_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) narzędzia/test_okno_zmiana_rozmiaru.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) narzędzia/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) narzędzia/test_System_Narzędzia.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) narzędzia/실행계층점검.py

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
