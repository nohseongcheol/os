PYTHON ?= python3
RESOLUTION ?= 1920x1080
ARGS ?=
.PHONY: all build run desktop image check
all: build
build:
	sh native-launch.sh build
run:
	sh native-launch.sh run --resolution $(RESOLUTION) $(ARGS)
desktop:
	sh native-launch.sh desktop --resolution $(RESOLUTION) $(ARGS)
image:
	sh native-launch.sh image --resolution $(RESOLUTION) $(ARGS)
check:
	sh native-launch.sh check
.PHONY: test-system
test-system:
	sh native-launch.sh test-system $(ARGS)

.PHONY: x86-build x86-iso
x86-build:
	$(MAKE) -C "source/os"
x86-iso:
	$(MAKE) -C "source/os" iso

.PHONY: clean
clean:
	$(MAKE) -C "source" clean
	@set -e; for makefile in $(wildcard */Makefile); do \
		$(MAKE) -C "$${makefile%/Makefile}" clean; \
	done
