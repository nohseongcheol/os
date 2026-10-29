PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords ระยะไกล_เชื่อมต่อ
remote: build
	$(PYTHON) เครื่องมือ/ดําเนินการ_คําสั่ง.py --remote --resolution $(RESOLUTION) $(ARGS)
ระยะไกล_เชื่อมต่อ: remote
test-remote: build
	$(PYTHON) เครื่องมือ/การเชื่อมต่อระยะไกล_การทดสอบ.py
test-passwords: build
	$(PYTHON) เครื่องมือ/암호길이시험.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter เครือข่าย_สแตก -I vendor/lwip/src/include 시험/แบบผ่านสาย_เครือข่าย_การทดสอบ.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) เครื่องมือ/สร้าง.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) เครื่องมือ/COSL배포.py check
cosl-dist: build
	$(PYTHON) เครื่องมือ/เปิด_รูป.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) เครื่องมือ/COSL배포.py bundle
	$(PYTHON) เครื่องมือ/재연결시험.py
desktop: build
	$(PYTHON) เครื่องมือ/ดําเนินการ_คําสั่ง.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) เครื่องมือ/การทดสอบ_เชลล์.py
test-windows: build
	$(PYTHON) เครื่องมือ/창시험.py
test-swing: build
	$(PYTHON) เครื่องมือ/การทดสอบ_สวิง.py
test-stream: build
	$(PYTHON) เครื่องมือ/การทดสอบ_สตรีม.py
test-ftp: build
	$(PYTHON) เครื่องมือ/파일전송시험.py
test-elf: build
	$(PYTHON) เครื่องมือ/실행파일시험.py
test-examples: build
	$(PYTHON) เครื่องมือ/예제시험.py
network: build
	$(PYTHON) เครื่องมือ/ดําเนินการ_คําสั่ง.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) เครื่องมือ/코딩시험.py
test-desktop: build
	$(PYTHON) เครื่องมือ/การทดสอบ_เดสก์ท็อป.py
run: build
	$(PYTHON) เครื่องมือ/ดําเนินการ_คําสั่ง.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) เครื่องมือ/자바가상기계시험.py
test: build test-compiler
	$(PYTHON) เครื่องมือ/한글입력시험.py
	$(PYTHON) เครื่องมือ/การทดสอบ_เชลล์.py
	$(PYTHON) เครื่องมือ/การทดสอบ_เดสก์ท็อป.py
	$(PYTHON) เครื่องมือ/창시험.py
	$(PYTHON) เครื่องมือ/การทดสอบ_สวิง.py
	$(PYTHON) เครื่องมือ/การทดสอบ_สตรีม.py
	$(PYTHON) เครื่องมือ/코딩시험.py
	$(PYTHON) เครื่องมือ/자바가상기계시험.py
	$(PYTHON) เครื่องมือ/부팅시험.py
	$(PYTHON) เครื่องมือ/การทดสอบ_รวม.py
	$(PYTHON) เครื่องมือ/ความละเอียด_การทดสอบ.py
	$(PYTHON) เครื่องมือ/창크기시험.py
image: build
	$(PYTHON) เครื่องมือ/เปิด_รูป.py --resolution $(RESOLUTION)
	$(PYTHON) เครื่องมือ/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) เครื่องมือ/개발꾸러미내보내기.py

.PHONY: 모두 สร้าง ดําเนินการ_คําสั่ง 시험 통신 เดสก์ท็อป_ดู รูป_ค่า ชุดเครื่องมือการพัฒนา
모두: all
สร้าง: build
ดําเนินการ_คําสั่ง: run
시험: test
통신: network
เดสก์ท็อป_ดู: desktop
รูป_ค่า: image
ชุดเครื่องมือการพัฒนา: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) เครื่องมือ/부팅시험.py
test-remmina: build
	$(PYTHON) เครื่องมือ/원격한글시험.py
test-naming:
	$(PYTHON) เครื่องมือ/명명검사.py --시언어
	$(PYTHON) เครื่องมือ/직접호출검사.py
	$(PYTHON) เครื่องมือ/แหล่ง_รีวิว.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) เครื่องมือ/การทดสอบ_รวม.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) เครื่องมือ/ความละเอียด_การทดสอบ.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) เครื่องมือ/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) เครื่องมือ/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) เครื่องมือ/การทดสอบ_ระบบ_เครื่องมือ.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) เครื่องมือ/실행계층점검.py

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
