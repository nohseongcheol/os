Python ?= python3
.PHONY: build run
build:
	$(Python) edition.py build
run:
	$(Python) edition.py run

.PHONY: clean
clean:
	# Keep the persistent guest data disk and its lock.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name data.ext4 ! -name data.ext4.lock -exec rm -rf -- {} +; \
	fi

# WORLDOS_NATIVE_JAVA
.PHONY: native-build native-run native-desktop native-image native-check native-clean native-x86-iso
native-build:
	$(MAKE) -f native.mk build
native-run:
	$(MAKE) -f native.mk run
native-desktop:
	$(MAKE) -f native.mk desktop
native-image:
	$(MAKE) -f native.mk image
native-check:
	$(MAKE) -f native.mk check
native-clean:
	$(MAKE) -f native.mk clean
clean: native-clean
native-x86-iso:
	$(MAKE) -f native.mk x86-iso
