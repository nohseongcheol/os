PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords kếtNốiTừXa
remote: build
	$(PYTHON) CôngCụ/thựcThiLệnh.py --remote --resolution $(RESOLUTION) $(ARGS)
kếtNốiTừXa: remote
test-remote: build
	$(PYTHON) CôngCụ/ThửKếtNốiTừXa.py
test-passwords: build
	$(PYTHON) CôngCụ/ThửĐộDàiMậtKhẩu.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter NgănXếpMạng -I vendor/lwip/src/include KiểmThử/ThửMạngHữuTuyến.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) CôngCụ/xâyDựngHệThống.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) CôngCụ/BảnPhânPhốiCOSL.py check
cosl-dist: build
	$(PYTHON) CôngCụ/tạoẢnh.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) CôngCụ/BảnPhânPhốiCOSL.py bundle
	$(PYTHON) CôngCụ/ThửKếtNốiLại.py
desktop: build
	$(PYTHON) CôngCụ/thựcThiLệnh.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) CôngCụ/thửVỏLệnh.py
test-windows: build
	$(PYTHON) CôngCụ/thửCácCửaSổ.py
test-swing: build
	$(PYTHON) CôngCụ/thửSwing.py
test-stream: build
	$(PYTHON) CôngCụ/thửLuồng.py
test-ftp: build
	$(PYTHON) CôngCụ/thửFTP.py
test-elf: build
	$(PYTHON) CôngCụ/thửELF.py
test-examples: build
	$(PYTHON) CôngCụ/thửCácVíDụ.py
network: build
	$(PYTHON) CôngCụ/thựcThiLệnh.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) CôngCụ/thửLậpTrình.py
test-desktop: build
	$(PYTHON) CôngCụ/thửMànLàmViệc.py
run: build
	$(PYTHON) CôngCụ/thựcThiLệnh.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) CôngCụ/thửJVM.py
test: build test-compiler
	$(PYTHON) CôngCụ/thửĐầuVàoHangul.py
	$(PYTHON) CôngCụ/thửVỏLệnh.py
	$(PYTHON) CôngCụ/thửMànLàmViệc.py
	$(PYTHON) CôngCụ/thửCácCửaSổ.py
	$(PYTHON) CôngCụ/thửSwing.py
	$(PYTHON) CôngCụ/thửLuồng.py
	$(PYTHON) CôngCụ/thửLậpTrình.py
	$(PYTHON) CôngCụ/thửJVM.py
	$(PYTHON) CôngCụ/ThửKhởiĐộng.py
	$(PYTHON) CôngCụ/thửGóiGộp.py
	$(PYTHON) CôngCụ/ThửĐộPhânGiải.py
	$(PYTHON) CôngCụ/thửĐangĐổiCỡCửaSổ.py
image: build
	$(PYTHON) CôngCụ/tạoẢnh.py --resolution $(RESOLUTION)
	$(PYTHON) CôngCụ/sDKXuất.py
sdk: build
	$(PYTHON) CôngCụ/sDKXuất.py

.PHONY: xâyDựngTấtCả xâyDựngHệThống thựcThiLệnh KiểmThử TruyềnThông khungNhìnMànLàmViệc giáTrịẢnh bộCôngCụPhátTriển
xâyDựngTấtCả: all
xâyDựngHệThống: build
thựcThiLệnh: run
KiểmThử: test
TruyềnThông: network
khungNhìnMànLàmViệc: desktop
giáTrịẢnh: image
bộCôngCụPhátTriển: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) CôngCụ/ThửKhởiĐộng.py
test-remmina: build
	$(PYTHON) CôngCụ/thửRemmina.py
test-naming:
	$(PYTHON) CôngCụ/kiểmTraCáchĐặtTên.py --ngônNgữC
	$(PYTHON) CôngCụ/kiểmTraCácLờiGọiTrựcTiếp.py
	$(PYTHON) CôngCụ/XemDuyệtNguồn.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) CôngCụ/thửGóiGộp.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) CôngCụ/ThửĐộPhânGiải.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) CôngCụ/thửĐangĐổiCỡCửaSổ.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) CôngCụ/ThửLàmMớiMànHình.py

.PHONY: test-system
test-system: build
	$(PYTHON) CôngCụ/thửCácCôngCụHệThống.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) CôngCụ/CácPhépKiểmTraMôiTrườngChạy.py

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
