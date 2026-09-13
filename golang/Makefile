.DEFAULT_GOAL := catalog
.PHONY: catalog country-sources refine-country-names verify-country-names test-country-names verify-named-boots verify-named-packages verify verify-country-sources verify-country-builds kernel iso-language iso-country

LANGUAGE ?= kor
COUNTRY ?= KOR
VARIANT ?= IND/hi_Deva

.PHONY: localize-layout verify-layout test-layout
localize-layout:
	python3 tools/localize_layout.py --apply

verify-layout:
	python3 tools/localize_layout.py --check

test-layout:
	python3 -m unittest discover -s tools -p 'test_layout.py'

.PHONY: install-vbox verify-vbox test-vbox vbox script-vbox
install-vbox:
	python3 tools/install_vbox.py

verify-vbox:
	python3 tools/install_vbox.py --check

test-vbox:
	python3 -m unittest discover -s tools -p 'test_vbox.py'

vbox:
	$(MAKE) -C 나라/$(COUNTRY) vbox

script-vbox:
	$(MAKE) -C 문자판/$(VARIANT) vbox

.PHONY: install-posix posix script-posix verify-posix verify-posix-builds test-posix
install-posix:
	python3 tools/neutralize_posix.py
	python3 tools/install_posix.py
	python3 tools/install_shells.py --refresh

posix:
	$(MAKE) -C 나라/$(COUNTRY) posix

script-posix:
	$(MAKE) -C 문자판/$(VARIANT) posix

verify-posix:
	python3 tools/verify_posix.py

verify-posix-builds:
	python3 tools/verify_posix.py --build

test-posix:
	python3 -m unittest discover -s tools -p 'test_posix*.py'

.PHONY: install-shells shell script-shell verify-shells verify-shell-builds test-shells
install-shells:
	python3 tools/install_shells.py

shell:
	$(MAKE) -C 나라/$(COUNTRY) shell

script-shell:
	$(MAKE) -C 문자판/$(VARIANT) shell

verify-shells:
	python3 tools/verify_shells.py

verify-shell-builds:
	python3 tools/verify_shells.py --build

test-shells:
	python3 -m unittest discover -s tools -p 'test_shells.py'

SHELL_EDITION ?= $(COUNTRY)
SHELL_DISK ?= build/worldos-shell.vdi
.PHONY: shell-disk verify-shell-boots verify-all-shell-boots fix-shell-kernel-paths
shell-disk:
	python3 tools/shell_disk.py --edition "$(SHELL_EDITION)" --source "$(TEST_DISK)" --output "$(SHELL_DISK)"

verify-shell-boots:
	python3 tools/verify_shell_boots.py --disk "$(TEST_DISK)"

verify-all-shell-boots:
	python3 tools/verify_shell_boots.py --disk "$(TEST_DISK)" --all --rebuild-kernels

fix-shell-kernel-paths:
	python3 tools/fix_shell_kernel_paths.py

.PHONY: script-variants verify-script-variants test-script-variants script-kernel script-iso

script-variants:
	python3 tools/generate_script_variants.py

verify-script-variants:
	python3 tools/verify_script_variants.py

test-script-variants:
	python3 -m unittest discover -s tools -p 'test_script_variants.py'

script-kernel:
	$(MAKE) -C 문자판/$(VARIANT) source

script-iso:
	$(MAKE) -C 문자판/$(VARIANT) source-iso

catalog:
	go run tools/generate_catalog.go

country-sources:
	go build -o tools/localize_engos /home/user/localize_engos.go
	go build -o tools/build_semantic_glossary tools/build_semantic_glossary.go
	go build -o tools/generate_country_sources tools/generate_country_sources.go
	tools/generate_country_sources -replace

verify:
	go run tools/verify_catalog.go

verify-country-sources:
	go run tools/verify_country_sources.go
	python3 tools/refine_country_names.py --check

refine-country-names:
	python3 tools/refine_country_names.py --apply

verify-country-names:
	python3 tools/refine_country_names.py --check

test-country-names:
	python3 -m unittest discover -s tools -p 'test_naming.py'

verify-named-boots:
	python3 tools/verify_named_boots.py --disk "$(TEST_DISK)" --idle "$(IDLE_PROGRAM)" --full-suite

verify-named-packages:
	python3 tools/verify_named_packages.py

verify-country-builds:
	go run tools/verify_country_sources.go -build

kernel:
	$(MAKE) -C /home/user/engos kernel

iso-language:
	$(MAKE) -C 언어/$(LANGUAGE) iso

iso-country:
	$(MAKE) -C 나라/$(COUNTRY) iso
