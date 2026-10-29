PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords 遠隔接続
remote: build
	$(PYTHON) 道具/命令実行.py --remote --resolution $(RESOLUTION) $(ARGS)
遠隔接続: remote
test-remote: build
	$(PYTHON) 道具/遠隔接続状態試験.py
test-passwords: build
	$(PYTHON) 道具/合言葉長さ試験.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter 通信網 -I vendor/lwip/src/include 試験/結線済み通信網試験.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) 道具/システム構築.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) 道具/COSL配布.py check
cosl-dist: build
	$(PYTHON) 道具/イメージ作成.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) 道具/COSL配布.py bundle
	$(PYTHON) 道具/再接続試験.py
desktop: build
	$(PYTHON) 道具/命令実行.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) 道具/シェル試験.py
test-windows: build
	$(PYTHON) 道具/窓一覧試験.py
test-swing: build
	$(PYTHON) 道具/画面部品試験.py
test-stream: build
	$(PYTHON) 道具/ストリーム試験.py
test-ftp: build
	$(PYTHON) 道具/FTP試験.py
test-elf: build
	$(PYTHON) 道具/ELF試験.py
test-examples: build
	$(PYTHON) 道具/用例集試験.py
network: build
	$(PYTHON) 道具/命令実行.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) 道具/符号化方式試験.py
test-desktop: build
	$(PYTHON) 道具/デスクトップ試験.py
run: build
	$(PYTHON) 道具/命令実行.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) 道具/JVM試験.py
test: build test-compiler
	$(PYTHON) 道具/ハングル入力試験.py
	$(PYTHON) 道具/シェル試験.py
	$(PYTHON) 道具/デスクトップ試験.py
	$(PYTHON) 道具/窓一覧試験.py
	$(PYTHON) 道具/画面部品試験.py
	$(PYTHON) 道具/ストリーム試験.py
	$(PYTHON) 道具/符号化方式試験.py
	$(PYTHON) 道具/JVM試験.py
	$(PYTHON) 道具/起動試験.py
	$(PYTHON) 道具/束試験.py
	$(PYTHON) 道具/解像度試験.py
	$(PYTHON) 道具/窓寸法変更中試験.py
image: build
	$(PYTHON) 道具/イメージ作成.py --resolution $(RESOLUTION)
	$(PYTHON) 道具/公開SDK.py
sdk: build
	$(PYTHON) 道具/公開SDK.py

.PHONY: 全体構築 システム構築 命令実行 試験 通信 デスクトップ表示像 イメージ値 開発道具一式
全体構築: all
システム構築: build
命令実行: run
試験: test
通信: network
デスクトップ表示像: desktop
イメージ値: image
開発道具一式: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) 道具/起動試験.py
test-remmina: build
	$(PYTHON) 道具/Remmina試験.py
test-naming:
	$(PYTHON) 道具/命名検査.py --C言語
	$(PYTHON) 道具/直接呼出し一覧検査.py
	$(PYTHON) 道具/ソース検討.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) 道具/束試験.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) 道具/解像度試験.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) 道具/窓寸法変更中試験.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) 道具/画面再読込試験.py

.PHONY: test-system
test-system: build
	$(PYTHON) 道具/システム道具試験.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) 道具/実行環境検査項目.py

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
