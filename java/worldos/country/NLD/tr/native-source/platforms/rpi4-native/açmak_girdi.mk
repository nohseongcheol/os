PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords uzak_bağla
remote: build
	$(PYTHON) araçlar/yürütmek_komut.py --remote --resolution $(RESOLUTION) $(ARGS)
uzak_bağla: remote
test-remote: build
	$(PYTHON) araçlar/uzak_bağlantı_test.py
test-passwords: build
	$(PYTHON) araçlar/parola_süre_test.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ağ_Yığın -I vendor/lwip/src/include sınamalar/kablolu_ağ_test.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) araçlar/oluştur.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) araçlar/COSL배포.py check
cosl-dist: build
	$(PYTHON) araçlar/açmak_RESİM.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) araçlar/COSL배포.py bundle
	$(PYTHON) araçlar/재연결시험.py
desktop: build
	$(PYTHON) araçlar/yürütmek_komut.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) araçlar/test_kabuk.py
test-windows: build
	$(PYTHON) araçlar/test_Windows.py
test-swing: build
	$(PYTHON) araçlar/test_Swing.py
test-stream: build
	$(PYTHON) araçlar/test_akış.py
test-ftp: build
	$(PYTHON) araçlar/test_FTP.py
test-elf: build
	$(PYTHON) araçlar/실행파일시험.py
test-examples: build
	$(PYTHON) araçlar/예제시험.py
network: build
	$(PYTHON) araçlar/yürütmek_komut.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) araçlar/코딩시험.py
test-desktop: build
	$(PYTHON) araçlar/test_Masaüstü.py
run: build
	$(PYTHON) araçlar/yürütmek_komut.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) araçlar/test_Java_Sanal_Makinesi.py
test: build test-compiler
	$(PYTHON) araçlar/한글입력시험.py
	$(PYTHON) araçlar/test_kabuk.py
	$(PYTHON) araçlar/test_Masaüstü.py
	$(PYTHON) araçlar/test_Windows.py
	$(PYTHON) araçlar/test_Swing.py
	$(PYTHON) araçlar/test_akış.py
	$(PYTHON) araçlar/코딩시험.py
	$(PYTHON) araçlar/test_Java_Sanal_Makinesi.py
	$(PYTHON) araçlar/부팅시험.py
	$(PYTHON) araçlar/test_paket_iş.py
	$(PYTHON) araçlar/çözme_test.py
	$(PYTHON) araçlar/test_pencere_yeniden_boyutlandırma.py
image: build
	$(PYTHON) araçlar/açmak_RESİM.py --resolution $(RESOLUTION)
	$(PYTHON) araçlar/dışarı_aktarmak_SDK.py
sdk: build
	$(PYTHON) araçlar/dışarı_aktarmak_SDK.py

.PHONY: 모두 oluştur yürütmek_komut sınamalar iletişim Masaüstü_Görünüm RESİM_değer geliştirme_seti
모두: all
oluştur: build
yürütmek_komut: run
sınamalar: test
iletişim: network
Masaüstü_Görünüm: desktop
RESİM_değer: image
geliştirme_seti: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) araçlar/부팅시험.py
test-remmina: build
	$(PYTHON) araçlar/원격한글시험.py
test-naming:
	$(PYTHON) araçlar/명명검사.py --C_Dil
	$(PYTHON) araçlar/직접호출검사.py
	$(PYTHON) araçlar/kaynak_inceleme.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) araçlar/test_paket_iş.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) araçlar/çözme_test.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) araçlar/test_pencere_yeniden_boyutlandırma.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) araçlar/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) araçlar/test_Sistem_Araçlar.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) araçlar/실행계층점검.py

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
