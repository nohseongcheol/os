PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords etä_YHDISTÄ
remote: build
	$(PYTHON) työkalut/Suorita_komento.py --remote --resolution $(RESOLUTION) $(ARGS)
etä_YHDISTÄ: remote
test-remote: build
	$(PYTHON) työkalut/etäyhteys_testi.py
test-passwords: build
	$(PYTHON) työkalut/salasana_kesto_testi.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter verkko_Pino -I vendor/lwip/src/include testit/lanka_verkko_testi.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) työkalut/kääntää_Järjestelmä.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) työkalut/COSL배포.py check
cosl-dist: build
	$(PYTHON) työkalut/Luo_KUVA.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) työkalut/COSL배포.py bundle
	$(PYTHON) työkalut/재연결시험.py
desktop: build
	$(PYTHON) työkalut/Suorita_komento.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) työkalut/testi_liittymä.py
test-windows: build
	$(PYTHON) työkalut/testi_Windows.py
test-swing: build
	$(PYTHON) työkalut/testi_swing.py
test-stream: build
	$(PYTHON) työkalut/testi_virta.py
test-ftp: build
	$(PYTHON) työkalut/testi_FTP.py
test-elf: build
	$(PYTHON) työkalut/실행파일시험.py
test-examples: build
	$(PYTHON) työkalut/예제시험.py
network: build
	$(PYTHON) työkalut/Suorita_komento.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) työkalut/코딩시험.py
test-desktop: build
	$(PYTHON) työkalut/testi_työpöytä.py
run: build
	$(PYTHON) työkalut/Suorita_komento.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) työkalut/testi_Java_VM.py
test: build test-compiler
	$(PYTHON) työkalut/한글입력시험.py
	$(PYTHON) työkalut/testi_liittymä.py
	$(PYTHON) työkalut/testi_työpöytä.py
	$(PYTHON) työkalut/testi_Windows.py
	$(PYTHON) työkalut/testi_swing.py
	$(PYTHON) työkalut/testi_virta.py
	$(PYTHON) työkalut/코딩시험.py
	$(PYTHON) työkalut/testi_Java_VM.py
	$(PYTHON) työkalut/부팅시험.py
	$(PYTHON) työkalut/testi_nippu.py
	$(PYTHON) työkalut/tarkkuus_testi.py
	$(PYTHON) työkalut/창크기시험.py
image: build
	$(PYTHON) työkalut/Luo_KUVA.py --resolution $(RESOLUTION)
	$(PYTHON) työkalut/viedä_SDK.py
sdk: build
	$(PYTHON) työkalut/viedä_SDK.py

.PHONY: 모두 kääntää_Järjestelmä Suorita_komento testit 통신 työpöytä_Näkymä KUVA_ARVO ohjelmankehityspaketti
모두: all
kääntää_Järjestelmä: build
Suorita_komento: run
testit: test
통신: network
työpöytä_Näkymä: desktop
KUVA_ARVO: image
ohjelmankehityspaketti: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) työkalut/부팅시험.py
test-remmina: build
	$(PYTHON) työkalut/원격한글시험.py
test-naming:
	$(PYTHON) työkalut/명명검사.py --C_Kieli
	$(PYTHON) työkalut/직접호출검사.py
	$(PYTHON) työkalut/lähde_arvostelu.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) työkalut/testi_nippu.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) työkalut/tarkkuus_testi.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) työkalut/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) työkalut/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) työkalut/testi_Järjestelmä_Työkalut.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) työkalut/실행계층점검.py

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
