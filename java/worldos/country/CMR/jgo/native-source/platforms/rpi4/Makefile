PYTHON ?= python3
.PHONY: all prepare prepare-host runtimes image test test-desktop test-korean verify release data run run-console
all: image
prepare:
	$(PYTHON) tools/prepare.py
prepare-host:
	$(PYTHON) tools/prepare.py --host-tools
runtimes:
	$(PYTHON) tools/export_runtime.py
image:
	$(PYTHON) tools/build.py
test:
	$(PYTHON) tools/test_boot.py
test-desktop:
	$(PYTHON) tools/test_desktop.py
test-korean:
	$(PYTHON) tools/test_korean.py
run:
	$(PYTHON) tools/run_qemu.py
run-console:
	$(PYTHON) tools/run_qemu.py --console
verify:
	$(PYTHON) tools/verify_image.py
release:
	$(PYTHON) tools/release.py
data:
	$(PYTHON) tools/build.py --data-only $(OUTPUT)

.PHONY: clean
clean:
	# Keep persistent user disks and their locks.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name '*user.img' ! -name '*.lock' -exec rm -rf -- {} +; \
	fi
	@if test -d dist; then \
		find dist -mindepth 1 -maxdepth 1 ! -name 'jkoros-user.img*' -exec rm -rf -- {} +; \
	fi
