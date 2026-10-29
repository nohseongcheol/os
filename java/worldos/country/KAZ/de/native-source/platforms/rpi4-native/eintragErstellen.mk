PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords entferntVerbinden
remote: build
	$(PYTHON) Werkzeuge/befehlAusführen.py --remote --resolution $(RESOLUTION) $(ARGS)
entferntVerbinden: remote
test-remote: build
	$(PYTHON) Werkzeuge/EntferntVerbindungPrüfung.py
test-passwords: build
	$(PYTHON) Werkzeuge/PasswortLängePrüfung.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter Netzwerkstapel -I vendor/lwip/src/include Prüfungen/VerdrahtetNetzwerkPrüfung.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Werkzeuge/systemErzeugenAbbild.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Werkzeuge/COSLVerteilung.py check
cosl-dist: build
	$(PYTHON) Werkzeuge/abbildErstellen.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Werkzeuge/COSLVerteilung.py bundle
	$(PYTHON) Werkzeuge/NeuverbindenPrüfung.py
desktop: build
	$(PYTHON) Werkzeuge/befehlAusführen.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Werkzeuge/befehlshüllePrüfung.py
test-windows: build
	$(PYTHON) Werkzeuge/fensterlistePrüfung.py
test-swing: build
	$(PYTHON) Werkzeuge/swingPrüfung.py
test-stream: build
	$(PYTHON) Werkzeuge/datenstromPrüfung.py
test-ftp: build
	$(PYTHON) Werkzeuge/fTPPrüfung.py
test-elf: build
	$(PYTHON) Werkzeuge/eLFPrüfung.py
test-examples: build
	$(PYTHON) Werkzeuge/beispielsammlungPrüfung.py
network: build
	$(PYTHON) Werkzeuge/befehlAusführen.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Werkzeuge/kodierweisePrüfung.py
test-desktop: build
	$(PYTHON) Werkzeuge/arbeitsflächePrüfung.py
run: build
	$(PYTHON) Werkzeuge/befehlAusführen.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Werkzeuge/jVMPrüfung.py
test: build test-compiler
	$(PYTHON) Werkzeuge/hangulEingabePrüfung.py
	$(PYTHON) Werkzeuge/befehlshüllePrüfung.py
	$(PYTHON) Werkzeuge/arbeitsflächePrüfung.py
	$(PYTHON) Werkzeuge/fensterlistePrüfung.py
	$(PYTHON) Werkzeuge/swingPrüfung.py
	$(PYTHON) Werkzeuge/datenstromPrüfung.py
	$(PYTHON) Werkzeuge/kodierweisePrüfung.py
	$(PYTHON) Werkzeuge/jVMPrüfung.py
	$(PYTHON) Werkzeuge/Startprüfung.py
	$(PYTHON) Werkzeuge/bündelPrüfung.py
	$(PYTHON) Werkzeuge/AuflösungPrüfung.py
	$(PYTHON) Werkzeuge/fensterGrößenänderungPrüfung.py
image: build
	$(PYTHON) Werkzeuge/abbildErstellen.py --resolution $(RESOLUTION)
	$(PYTHON) Werkzeuge/exportierenSDK.py
sdk: build
	$(PYTHON) Werkzeuge/exportierenSDK.py

.PHONY: alleErzeugenAbbild systemErzeugenAbbild befehlAusführen Prüfungen Kommunikation arbeitsflächeAnsicht abbildWert entwicklungWerkzeugsatz
alleErzeugenAbbild: all
systemErzeugenAbbild: build
befehlAusführen: run
Prüfungen: test
Kommunikation: network
arbeitsflächeAnsicht: desktop
abbildWert: image
entwicklungWerkzeugsatz: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Werkzeuge/Startprüfung.py
test-remmina: build
	$(PYTHON) Werkzeuge/remminaPrüfung.py
test-naming:
	$(PYTHON) Werkzeuge/benennungPrüfen.py --cSprache
	$(PYTHON) Werkzeuge/direktAufruflistePrüfen.py
	$(PYTHON) Werkzeuge/QuelltextDurchsicht.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Werkzeuge/bündelPrüfung.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Werkzeuge/AuflösungPrüfung.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Werkzeuge/fensterGrößenänderungPrüfung.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Werkzeuge/BildschirmAuffrischenPrüfung.py

.PHONY: test-system
test-system: build
	$(PYTHON) Werkzeuge/systemWerkzeugePrüfung.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Werkzeuge/LaufzeitPrüfpunkte.py

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
