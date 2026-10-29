PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords מרוחק_לקשר
remote: build
	$(PYTHON) כלים/לבצע_פקודה.py --remote --resolution $(RESOLUTION) $(ARGS)
מרוחק_לקשר: remote
test-remote: build
	$(PYTHON) כלים/חיבור_מרוחק_נסה.py
test-passwords: build
	$(PYTHON) כלים/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter רשת_רמז -I vendor/lwip/src/include 시험/קווי_רשת_נסה.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) כלים/בנייה.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) כלים/COSL배포.py check
cosl-dist: build
	$(PYTHON) כלים/ליצור_תמונה.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) כלים/COSL배포.py bundle
	$(PYTHON) כלים/재연결시험.py
desktop: build
	$(PYTHON) כלים/לבצע_פקודה.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) כלים/נסה_מעטפת.py
test-windows: build
	$(PYTHON) כלים/창시험.py
test-swing: build
	$(PYTHON) כלים/נסה_מוסיקת_סווינג.py
test-stream: build
	$(PYTHON) כלים/נסה_זרם.py
test-ftp: build
	$(PYTHON) כלים/נסה_פרוטוקול_העברת_קבצים.py
test-elf: build
	$(PYTHON) כלים/실행파일시험.py
test-examples: build
	$(PYTHON) כלים/예제시험.py
network: build
	$(PYTHON) כלים/לבצע_פקודה.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) כלים/코딩시험.py
test-desktop: build
	$(PYTHON) כלים/נסה_מחשב_שולחני.py
run: build
	$(PYTHON) כלים/לבצע_פקודה.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) כלים/נסה_מחשב_וירטואלי_java.py
test: build test-compiler
	$(PYTHON) כלים/한글입력시험.py
	$(PYTHON) כלים/נסה_מעטפת.py
	$(PYTHON) כלים/נסה_מחשב_שולחני.py
	$(PYTHON) כלים/창시험.py
	$(PYTHON) כלים/נסה_מוסיקת_סווינג.py
	$(PYTHON) כלים/נסה_זרם.py
	$(PYTHON) כלים/코딩시험.py
	$(PYTHON) כלים/נסה_מחשב_וירטואלי_java.py
	$(PYTHON) כלים/부팅시험.py
	$(PYTHON) כלים/נסה_חבילה.py
	$(PYTHON) כלים/רזולוציה_נסה.py
	$(PYTHON) כלים/창크기시험.py
image: build
	$(PYTHON) כלים/ליצור_תמונה.py --resolution $(RESOLUTION)
	$(PYTHON) כלים/ייצא_ערכת_פיתוח_תוכנה.py
sdk: build
	$(PYTHON) כלים/ייצא_ערכת_פיתוח_תוכנה.py

.PHONY: 모두 בנייה לבצע_פקודה 시험 통신 מחשב_שולחני_הצג תמונה_ערך ערכת_פיתוח
모두: all
בנייה: build
לבצע_פקודה: run
시험: test
통신: network
מחשב_שולחני_הצג: desktop
תמונה_ערך: image
ערכת_פיתוח: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) כלים/부팅시험.py
test-remmina: build
	$(PYTHON) כלים/원격한글시험.py
test-naming:
	$(PYTHON) כלים/명명검사.py --מ_שפה
	$(PYTHON) כלים/직접호출검사.py
	$(PYTHON) כלים/מקור_סקירה.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) כלים/נסה_חבילה.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) כלים/רזולוציה_נסה.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) כלים/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) כלים/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) כלים/נסה_מערכת_כלים.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) כלים/실행계층점검.py

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
