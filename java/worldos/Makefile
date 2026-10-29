PYTHON ?= python3
COUNTRY ?= KOR
RESOLUTION ?= 1920x1080
ARGS ?=
.PHONY: native-build native-run native-desktop native-image native-generate native-verify native-test
native-build:
	$(MAKE) -C country/$(COUNTRY) build
native-run:
	$(MAKE) -C country/$(COUNTRY) run RESOLUTION=$(RESOLUTION) ARGS="$(ARGS)"
native-desktop:
	$(MAKE) -C country/$(COUNTRY) desktop RESOLUTION=$(RESOLUTION) ARGS="$(ARGS)"
native-image:
	$(MAKE) -C country/$(COUNTRY) image RESOLUTION=$(RESOLUTION)
native-generate:
	$(PYTHON) native/generate.py
native-verify:
	$(PYTHON) native/verify.py
native-test:
	$(PYTHON) native/verify_runtime.py $(COUNTRY) $(ARGS)
.PHONY: native-test-system
native-test-system:
	$(MAKE) -C country/$(COUNTRY) test-system ARGS="$(ARGS)"
.PHONY: native-relocate
native-relocate:
	$(PYTHON) native/relocate_test.py $(COUNTRY)
.PHONY: native-report
native-report:
	$(PYTHON) native/report.py

.PHONY: native-materialize native-export test-native-archives
native-materialize:
	$(PYTHON) native/archives.py materialize
native-export:
	$(PYTHON) native/export.py $(COUNTRY) --output "$(OUTPUT)"
test-native-archives:
	$(PYTHON) -m unittest discover -s native/tests -p 'test_archives.py' -v

.PHONY: fetch
fetch:
	$(PYTHON) tools/fetch_runtime.py
.PHONY: prepare-runtime
prepare-runtime:
	$(PYTHON) tools/prepare_runtime.py
.PHONY: runtime
runtime:
	$(PYTHON) tools/build_runtime.py

.PHONY: generate build-all build run list export test test-gui
EDITION ?= KOR/ko
generate:
	$(PYTHON) tools/generate.py
build-all:
	$(PYTHON) tools/worldos.py build-all
build:
	$(PYTHON) tools/worldos.py build $(EDITION)
run:
	$(PYTHON) tools/worldos.py run $(EDITION)
list:
	$(PYTHON) tools/worldos.py list
export:
	$(PYTHON) tools/worldos.py export $(EDITION) --output "$(OUTPUT)"
test:
	$(PYTHON) tools/test_guest.py --edition $(EDITION)
test-gui:
	$(PYTHON) tools/test_guest.py --edition $(EDITION) --gui --reboots 1

.PHONY: verify-editions
verify-editions:
	$(PYTHON) tools/verify_editions.py

.PHONY: test-input
test-input:
	$(PYTHON) tools/test_guest.py --edition $(EDITION) --gui --reboots 1 --focus input

.PHONY: test-desktop
test-desktop:
	$(PYTHON) tools/test_guest.py --edition $(EDITION) --gui --reboots 1 --focus desktop

.PHONY: naming-audit naming-test country-naming-plan country-naming-apply country-naming-audit
naming-audit:
	$(PYTHON) tools/audit_naming.py --native --compile
	$(PYTHON) tools/audit_country_naming.py
naming-test:
	$(PYTHON) tests/test_naming_review.py -v
country-naming-plan:
	$(PYTHON) tools/apply_country_naming.py
country-naming-apply:
	$(PYTHON) tools/apply_country_naming.py --apply
country-naming-audit:
	$(PYTHON) tools/audit_country_naming.py

.PHONY: clean
clean:
	@set -e; for makefile in $(wildcard country/*/Makefile); do \
		$(MAKE) -C "$${makefile%/Makefile}" clean; \
	done
	rm -rf -- build
