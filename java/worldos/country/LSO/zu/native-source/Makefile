PYTHON ?= python3
VBOX_NAME ?= jkoros operating system
VBOX_TYPE ?= gui
export VBOX_NAME VBOX_TYPE
.PHONY: all compiler os iso run run-gui test legacy-test apps test-network
.PHONY: vbox vbox-status test-vbox
.PHONY: test-java
.PHONY: posix-kor test-posix
posix-kor:
	$(MAKE) -C posix-kor
test-posix:
	$(MAKE) -C os test-posix
all: compiler os

compiler:
	$(MAKE) -C compiler

os:
	$(MAKE) -C os

apps:
	$(MAKE) -C os apps

test-network:
	$(MAKE) -C os test-network

test-java:
	$(MAKE) -C os test-java

.PHONY: rpi-prepare rpi-image rpi-test korean-java
rpi-prepare:
	$(MAKE) -C platforms/rpi4 prepare
rpi-image:
	$(MAKE) -C platforms/rpi4 image
rpi-test:
	$(MAKE) -C platforms/rpi4 test
korean-java:
	$(MAKE) -C 한국어자바

.PHONY: rpi-native rpi-native-run rpi-native-desktop rpi-native-test rpi-native-image
rpi-native:
	$(MAKE) -C platforms/rpi4-native build
rpi-native-run:
	$(MAKE) -C platforms/rpi4-native run
rpi-native-desktop:
	$(MAKE) -C platforms/rpi4-native desktop
rpi-native-test:
	$(MAKE) -C platforms/rpi4-native test
rpi-native-image:
	$(MAKE) -C platforms/rpi4-native image

iso:
	$(MAKE) -C os iso

run:
	$(MAKE) -C os run

run-gui:
	$(MAKE) -C os run-gui

vbox:
	$(PYTHON) Amathuluzi/가상상자.py run

vbox-status:
	$(PYTHON) Amathuluzi/가상상자.py status

test-vbox:
	$(PYTHON) -m unittest discover -s Amathuluzi/시험 -p 'test_*.py' -v

test:
	$(MAKE) -C compiler test
	$(MAKE) -C os test

legacy-test:
	$(MAKE) -f yakha_okufakwayo.mk 검사

.PHONY: clean
clean:
	$(MAKE) -C compiler clean
	$(MAKE) -C os clean
	$(MAKE) -C posix-kor clean
	$(MAKE) -C 한국어자바 clean
	$(MAKE) -C platforms/rpi4 clean
	$(MAKE) -C platforms/rpi4-native clean
	rm -rf -- build 결과
