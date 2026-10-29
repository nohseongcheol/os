PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords connecterDistant
remote: build
	$(PYTHON) Outils/exécuterCommande.py --remote --resolution $(RESOLUTION) $(ARGS)
connecterDistant: remote
test-remote: build
	$(PYTHON) Outils/TestConnexionDistant.py
test-passwords: build
	$(PYTHON) Outils/TestLongueurMotPasse.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter PileRéseau -I vendor/lwip/src/include Tests/TestRéseauCâblé.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Outils/construireSystème.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Outils/DistributionCOSL.py check
cosl-dist: build
	$(PYTHON) Outils/créerImage.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Outils/DistributionCOSL.py bundle
	$(PYTHON) Outils/TestReconnecter.py
desktop: build
	$(PYTHON) Outils/exécuterCommande.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Outils/testInterpréteurCommandes.py
test-windows: build
	$(PYTHON) Outils/testFenêtres.py
test-swing: build
	$(PYTHON) Outils/testSwing.py
test-stream: build
	$(PYTHON) Outils/testFlux.py
test-ftp: build
	$(PYTHON) Outils/testFTP.py
test-elf: build
	$(PYTHON) Outils/testELF.py
test-examples: build
	$(PYTHON) Outils/testRecueilExemples.py
network: build
	$(PYTHON) Outils/exécuterCommande.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Outils/testCodage.py
test-desktop: build
	$(PYTHON) Outils/testBureau.py
run: build
	$(PYTHON) Outils/exécuterCommande.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Outils/testJVM.py
test: build test-compiler
	$(PYTHON) Outils/testEntréeHangul.py
	$(PYTHON) Outils/testInterpréteurCommandes.py
	$(PYTHON) Outils/testBureau.py
	$(PYTHON) Outils/testFenêtres.py
	$(PYTHON) Outils/testSwing.py
	$(PYTHON) Outils/testFlux.py
	$(PYTHON) Outils/testCodage.py
	$(PYTHON) Outils/testJVM.py
	$(PYTHON) Outils/TestAmorçage.py
	$(PYTHON) Outils/testLot.py
	$(PYTHON) Outils/TestRésolution.py
	$(PYTHON) Outils/testRedimensionnementFenêtre.py
image: build
	$(PYTHON) Outils/créerImage.py --resolution $(RESOLUTION)
	$(PYTHON) Outils/sDKExporter.py
sdk: build
	$(PYTHON) Outils/sDKExporter.py

.PHONY: construireTous construireSystème exécuterCommande Tests Communication vueBureau valeurImage trousseDéveloppement
construireTous: all
construireSystème: build
exécuterCommande: run
Tests: test
Communication: network
vueBureau: desktop
valeurImage: image
trousseDéveloppement: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Outils/TestAmorçage.py
test-remmina: build
	$(PYTHON) Outils/testRemmina.py
test-naming:
	$(PYTHON) Outils/contrôlerNommage.py --langueC
	$(PYTHON) Outils/contrôlerAppelsDirect.py
	$(PYTHON) Outils/RévisionExamenSource.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Outils/testLot.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Outils/TestRésolution.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Outils/testRedimensionnementFenêtre.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Outils/TestActualiserÉcran.py

.PHONY: test-system
test-system: build
	$(PYTHON) Outils/testOutilsSystème.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Outils/ContrôlesEnvironnementExécution.py

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
