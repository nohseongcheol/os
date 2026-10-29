PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords بعيد_يتصل
remote: build
	$(PYTHON) أدوات/ينفذ_أمر.py --remote --resolution $(RESOLUTION) $(ARGS)
بعيد_يتصل: remote
test-remote: build
	$(PYTHON) أدوات/اتصال_بعيد_يختبر.py
test-passwords: build
	$(PYTHON) أدوات/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter شبكة_رمز -I vendor/lwip/src/include اختبارات/سلكي_شبكة_يختبر.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) أدوات/بنية_نظام.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) أدوات/COSL배포.py check
cosl-dist: build
	$(PYTHON) أدوات/فتح_صورة.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) أدوات/COSL배포.py bundle
	$(PYTHON) أدوات/재연결시험.py
desktop: build
	$(PYTHON) أدوات/ينفذ_أمر.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) أدوات/셸시험.py
test-windows: build
	$(PYTHON) أدوات/창시험.py
test-swing: build
	$(PYTHON) أدوات/화면요소시험.py
test-stream: build
	$(PYTHON) أدوات/يختبر_بث.py
test-ftp: build
	$(PYTHON) أدوات/يختبر_بروتوكول_نقل_الملفات.py
test-elf: build
	$(PYTHON) أدوات/실행파일시험.py
test-examples: build
	$(PYTHON) أدوات/예제시험.py
network: build
	$(PYTHON) أدوات/ينفذ_أمر.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) أدوات/코딩시험.py
test-desktop: build
	$(PYTHON) أدوات/يختبر_سطح_مكتب.py
run: build
	$(PYTHON) أدوات/ينفذ_أمر.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) أدوات/يختبر_جهاز_Java_ظاهري.py
test: build test-compiler
	$(PYTHON) أدوات/한글입력시험.py
	$(PYTHON) أدوات/셸시험.py
	$(PYTHON) أدوات/يختبر_سطح_مكتب.py
	$(PYTHON) أدوات/창시험.py
	$(PYTHON) أدوات/화면요소시험.py
	$(PYTHON) أدوات/يختبر_بث.py
	$(PYTHON) أدوات/코딩시험.py
	$(PYTHON) أدوات/يختبر_جهاز_Java_ظاهري.py
	$(PYTHON) أدوات/부팅시험.py
	$(PYTHON) أدوات/يختبر_يُجمع.py
	$(PYTHON) أدوات/دقة_يختبر.py
	$(PYTHON) أدوات/창크기시험.py
image: build
	$(PYTHON) أدوات/فتح_صورة.py --resolution $(RESOLUTION)
	$(PYTHON) أدوات/تصدير_عدة_تطوير_البرامج.py
sdk: build
	$(PYTHON) أدوات/تصدير_عدة_تطوير_البرامج.py

.PHONY: 모두 بنية_نظام ينفذ_أمر اختبارات 통신 سطح_مكتب_عرض صورة_قيمة أداة_التطوير
모두: all
بنية_نظام: build
ينفذ_أمر: run
اختبارات: test
통신: network
سطح_مكتب_عرض: desktop
صورة_قيمة: image
أداة_التطوير: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) أدوات/부팅시험.py
test-remmina: build
	$(PYTHON) أدوات/원격한글시험.py
test-naming:
	$(PYTHON) أدوات/명명검사.py --الرمز_البريدي_لغة
	$(PYTHON) أدوات/직접호출검사.py
	$(PYTHON) أدوات/مصدر_تقييم.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) أدوات/يختبر_يُجمع.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) أدوات/دقة_يختبر.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) أدوات/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) أدوات/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) أدوات/يختبر_نظام_أدوات.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) أدوات/실행계층점검.py

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
