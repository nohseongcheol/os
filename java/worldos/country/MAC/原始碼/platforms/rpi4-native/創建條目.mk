PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords 遠程連接
remote: build
	$(PYTHON) 工具集/執行命令.py --remote --resolution $(RESOLUTION) $(ARGS)
遠程連接: remote
test-remote: build
	$(PYTHON) 工具集/遠程連接狀態測試.py
test-passwords: build
	$(PYTHON) 工具集/密碼長度測試.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter 通信網絡 -I vendor/lwip/src/include 測試/有線網路測試.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) 工具集/構建系統.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) 工具集/COSL分發.py check
cosl-dist: build
	$(PYTHON) 工具集/創建映像.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) 工具集/COSL分發.py bundle
	$(PYTHON) 工具集/重新連接測試.py
desktop: build
	$(PYTHON) 工具集/執行命令.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) 工具集/測試命令殼.py
test-windows: build
	$(PYTHON) 工具集/測試窗口列.py
test-swing: build
	$(PYTHON) 工具集/界面元素測試.py
test-stream: build
	$(PYTHON) 工具集/測試流.py
test-ftp: build
	$(PYTHON) 工具集/測試FTP.py
test-elf: build
	$(PYTHON) 工具集/測試ELF.py
test-examples: build
	$(PYTHON) 工具集/測試範例集.py
network: build
	$(PYTHON) 工具集/執行命令.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) 工具集/測試編碼方式.py
test-desktop: build
	$(PYTHON) 工具集/測試桌面.py
run: build
	$(PYTHON) 工具集/執行命令.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) 工具集/測試JVM.py
test: build test-compiler
	$(PYTHON) 工具集/測試韓文字母輸入.py
	$(PYTHON) 工具集/測試命令殼.py
	$(PYTHON) 工具集/測試桌面.py
	$(PYTHON) 工具集/測試窗口列.py
	$(PYTHON) 工具集/界面元素測試.py
	$(PYTHON) 工具集/測試流.py
	$(PYTHON) 工具集/測試編碼方式.py
	$(PYTHON) 工具集/測試JVM.py
	$(PYTHON) 工具集/啓動測試.py
	$(PYTHON) 工具集/測試捆綁.py
	$(PYTHON) 工具集/分辨率測試.py
	$(PYTHON) 工具集/測試窗口尺寸調整中.py
image: build
	$(PYTHON) 工具集/創建映像.py --resolution $(RESOLUTION)
	$(PYTHON) 工具集/導出SDK.py
sdk: build
	$(PYTHON) 工具集/導出SDK.py

.PHONY: 構建全部 構建系統 執行命令 測試 通信 桌面視圖 映像值 開發工具套件
構建全部: all
構建系統: build
執行命令: run
測試: test
通信: network
桌面視圖: desktop
映像值: image
開發工具套件: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) 工具集/啓動測試.py
test-remmina: build
	$(PYTHON) 工具集/測試Remmina.py
test-naming:
	$(PYTHON) 工具集/檢查命名.py --C語言
	$(PYTHON) 工具集/檢查直接調用列.py
	$(PYTHON) 工具集/原始碼審閱.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) 工具集/測試捆綁.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) 工具集/分辨率測試.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) 工具集/測試窗口尺寸調整中.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) 工具集/屏幕刷新測試.py

.PHONY: test-system
test-system: build
	$(PYTHON) 工具集/測試系統工具.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) 工具集/運行時檢查項.py

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
