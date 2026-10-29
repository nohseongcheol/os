PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords 远程连接
remote: build
	$(PYTHON) 工具集/执行命令.py --remote --resolution $(RESOLUTION) $(ARGS)
远程连接: remote
test-remote: build
	$(PYTHON) 工具集/远程连接状态测试.py
test-passwords: build
	$(PYTHON) 工具集/密码长度测试.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter 通信网络 -I vendor/lwip/src/include 测试/有线网络测试.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) 工具集/构建系统.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) 工具集/COSL分发.py check
cosl-dist: build
	$(PYTHON) 工具集/创建映像.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) 工具集/COSL分发.py bundle
	$(PYTHON) 工具集/重新连接测试.py
desktop: build
	$(PYTHON) 工具集/执行命令.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) 工具集/测试命令壳.py
test-windows: build
	$(PYTHON) 工具集/测试窗口列.py
test-swing: build
	$(PYTHON) 工具集/界面元素测试.py
test-stream: build
	$(PYTHON) 工具集/测试流.py
test-ftp: build
	$(PYTHON) 工具集/测试FTP.py
test-elf: build
	$(PYTHON) 工具集/测试ELF.py
test-examples: build
	$(PYTHON) 工具集/测试用例集.py
network: build
	$(PYTHON) 工具集/执行命令.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) 工具集/测试编码方式.py
test-desktop: build
	$(PYTHON) 工具集/测试桌面.py
run: build
	$(PYTHON) 工具集/执行命令.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) 工具集/测试JVM.py
test: build test-compiler
	$(PYTHON) 工具集/测试韩文字母输入.py
	$(PYTHON) 工具集/测试命令壳.py
	$(PYTHON) 工具集/测试桌面.py
	$(PYTHON) 工具集/测试窗口列.py
	$(PYTHON) 工具集/界面元素测试.py
	$(PYTHON) 工具集/测试流.py
	$(PYTHON) 工具集/测试编码方式.py
	$(PYTHON) 工具集/测试JVM.py
	$(PYTHON) 工具集/启动测试.py
	$(PYTHON) 工具集/测试捆绑.py
	$(PYTHON) 工具集/分辨率测试.py
	$(PYTHON) 工具集/测试窗口尺寸调整中.py
image: build
	$(PYTHON) 工具集/创建映像.py --resolution $(RESOLUTION)
	$(PYTHON) 工具集/导出SDK.py
sdk: build
	$(PYTHON) 工具集/导出SDK.py

.PHONY: 构建全部 构建系统 执行命令 测试 通信 桌面视图 映像值 开发工具套件
构建全部: all
构建系统: build
执行命令: run
测试: test
通信: network
桌面视图: desktop
映像值: image
开发工具套件: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) 工具集/启动测试.py
test-remmina: build
	$(PYTHON) 工具集/测试Remmina.py
test-naming:
	$(PYTHON) 工具集/检查命名.py --C语言
	$(PYTHON) 工具集/检查直接调用列.py
	$(PYTHON) 工具集/源代码审阅.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) 工具集/测试捆绑.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) 工具集/分辨率测试.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) 工具集/测试窗口尺寸调整中.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) 工具集/屏幕刷新测试.py

.PHONY: test-system
test-system: build
	$(PYTHON) 工具集/测试系统工具.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) 工具集/运行时检查项.py

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
