PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords remoteConnect
remote: build
	$(PYTHON) tools/executeCommand.py --remote --resolution $(RESOLUTION) $(ARGS)
remoteConnect: remote
test-remote: build
	$(PYTHON) tools/RemoteConnectionTest.py
test-passwords: build
	$(PYTHON) tools/PasswordLengthTest.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter networkStack -I vendor/lwip/src/include tests/WiredNetworkTest.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) tools/buildSystem.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) tools/CoslDistribution.py check
cosl-dist: build
	$(PYTHON) tools/createImage.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) tools/CoslDistribution.py bundle
	$(PYTHON) tools/ReconnectTest.py
desktop: build
	$(PYTHON) tools/executeCommand.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) tools/testShell.py
test-windows: build
	$(PYTHON) tools/testWindows.py
test-swing: build
	$(PYTHON) tools/testSwing.py
test-stream: build
	$(PYTHON) tools/testStream.py
test-ftp: build
	$(PYTHON) tools/testFtp.py
test-elf: build
	$(PYTHON) tools/testElf.py
test-examples: build
	$(PYTHON) tools/testExamples.py
network: build
	$(PYTHON) tools/executeCommand.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) tools/testCoding.py
test-desktop: build
	$(PYTHON) tools/testDesktop.py
run: build
	$(PYTHON) tools/executeCommand.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) tools/testJvm.py
test: build test-compiler
	$(PYTHON) tools/testHangulInput.py
	$(PYTHON) tools/testShell.py
	$(PYTHON) tools/testDesktop.py
	$(PYTHON) tools/testWindows.py
	$(PYTHON) tools/testSwing.py
	$(PYTHON) tools/testStream.py
	$(PYTHON) tools/testCoding.py
	$(PYTHON) tools/testJvm.py
	$(PYTHON) tools/testBoot.py
	$(PYTHON) tools/testBundle.py
	$(PYTHON) tools/ResolutionTest.py
	$(PYTHON) tools/testWindowResizing.py
image: build
	$(PYTHON) tools/createImage.py --resolution $(RESOLUTION)
	$(PYTHON) tools/exportSdk.py
sdk: build
	$(PYTHON) tools/exportSdk.py

.PHONY: buildAll buildSystem executeCommand tests communication desktopView imageValue developmentKit
buildAll: all
buildSystem: build
executeCommand: run
tests: test
communication: network
desktopView: desktop
imageValue: image
developmentKit: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) tools/testBoot.py
test-remmina: build
	$(PYTHON) tools/testRemmina.py
test-naming:
	$(PYTHON) tools/checkNaming.py --cLanguage
	$(PYTHON) tools/checkDirectCalls.py
	$(PYTHON) tools/SourceReview.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) tools/testBundle.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) tools/ResolutionTest.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) tools/testWindowResizing.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) tools/ScreenRefreshTest.py

.PHONY: test-system
test-system: build
	$(PYTHON) tools/testSystemTools.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) tools/RuntimeChecks.py

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
