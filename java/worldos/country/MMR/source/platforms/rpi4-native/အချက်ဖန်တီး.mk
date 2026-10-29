PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords အဝေးချိတ်ဆက်
remote: build
	$(PYTHON) ကိရိယာစု/စက်မောင်း.py --remote --resolution $(RESOLUTION) $(ARGS)
အဝေးချိတ်ဆက်: remote
test-remote: build
	$(PYTHON) ကိရိယာစု/အဝေးချိတ်ဆက်မှုစမ်းသပ်.py
test-passwords: build
	$(PYTHON) ကိရိယာစု/စကားဝှက်အလျားစမ်းသပ်.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter ကွန်ရက်အလွှာစု -I vendor/lwip/src/include စမ်းသပ်မှု/유선망시험.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ကိရိယာစု/တည်ဆောက်.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ကိရိယာစု/COSL배포.py check
cosl-dist: build
	$(PYTHON) ကိရိယာစု/စက်ပုံရိပ်ဖန်တီး.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ကိရိယာစု/COSL배포.py bundle
	$(PYTHON) ကိရိယာစု/재연결시험.py
desktop: build
	$(PYTHON) ကိရိယာစု/စက်မောင်း.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ကိရိယာစု/အမိန့်ဝင်းစမ်းသပ်.py
test-windows: build
	$(PYTHON) ကိရိယာစု/ဝင်းများစမ်းသပ်.py
test-swing: build
	$(PYTHON) ကိရိယာစု/화면요소시험.py
test-stream: build
	$(PYTHON) ကိရိယာစု/စီးကြောင်းစမ်းသပ်.py
test-ftp: build
	$(PYTHON) ကိရိယာစု/파일전송시험.py
test-elf: build
	$(PYTHON) ကိရိယာစု/ELFစမ်းသပ်.py
test-examples: build
	$(PYTHON) ကိရိယာစု/ဥပမာများစမ်းသပ်.py
network: build
	$(PYTHON) ကိရိယာစု/စက်မောင်း.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ကိရိယာစု/ကုဒ်ရေးစမ်းသပ်.py
test-desktop: build
	$(PYTHON) ကိရိယာစု/အလုပ်မျက်နှာပြင်စမ်းသပ်.py
run: build
	$(PYTHON) ကိရိယာစု/စက်မောင်း.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ကိရိယာစု/JVMစမ်းသပ်.py
test: build test-compiler
	$(PYTHON) ကိရိယာစု/ဟန်ဂုအဝင်စမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/အမိန့်ဝင်းစမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/အလုပ်မျက်နှာပြင်စမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/ဝင်းများစမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/화면요소시험.py
	$(PYTHON) ကိရိယာစု/စီးကြောင်းစမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/ကုဒ်ရေးစမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/JVMစမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/စက်တင်စမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/အထုပ်စမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/ကြည်လင်ပြတ်သားမှုစမ်းသပ်.py
	$(PYTHON) ကိရိယာစု/창크기시험.py
image: build
	$(PYTHON) ကိရိယာစု/စက်ပုံရိပ်ဖန်တီး.py --resolution $(RESOLUTION)
	$(PYTHON) ကိရိယာစု/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) ကိရိယာစု/개발꾸러미내보내기.py

.PHONY: အားလုံးတည်ဆောက် တည်ဆောက် စက်မောင်း စမ်းသပ်မှု ဆက်သွယ်မှု အလုပ်မျက်နှာပြင်ရှုမြင်ရာ စက်ပုံရိပ်တန်ဖိုး 개발꾸러미
အားလုံးတည်ဆောက်: all
တည်ဆောက်: build
စက်မောင်း: run
စမ်းသပ်မှု: test
ဆက်သွယ်မှု: network
အလုပ်မျက်နှာပြင်ရှုမြင်ရာ: desktop
စက်ပုံရိပ်တန်ဖိုး: image
개발꾸러미: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ကိရိယာစု/စက်တင်စမ်းသပ်.py
test-remmina: build
	$(PYTHON) ကိရိယာစု/원격한글시험.py
test-naming:
	$(PYTHON) ကိရိယာစု/명명검사.py --Cဘာသာစကား
	$(PYTHON) ကိရိယာစု/직접호출검사.py
	$(PYTHON) ကိရိယာစု/မူရင်းကုဒ်သုံးသပ်.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ကိရိယာစု/အထုပ်စမ်းသပ်.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ကိရိယာစု/ကြည်လင်ပြတ်သားမှုစမ်းသပ်.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ကိရိယာစု/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ကိရိယာစု/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) ကိရိယာစု/စနစ်ကိရိယာစုစမ်းသပ်.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ကိရိယာစု/실행계층점검.py

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
