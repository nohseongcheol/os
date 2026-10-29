PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords दूरस्_थ_कनेक्ट
remote: build
	$(PYTHON) साधने/आज्ञा_कार्यवाही_करा.py --remote --resolution $(RESOLUTION) $(ARGS)
दूरस्_थ_कनेक्ट: remote
test-remote: build
	$(PYTHON) साधने/दूरस्_थ_कनेक्शन_चाचणी.py
test-passwords: build
	$(PYTHON) साधने/पासवर्ड_लांबी_चाचणी.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter संचारजाळे_स्टॅक -I vendor/lwip/src/include चाचण्या/वायर्ड_संचारजाळे_चाचणी.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) साधने/सिस्टम_बांधणी.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) साधने/सीओएसएल_वितरण.py check
cosl-dist: build
	$(PYTHON) साधने/चित्र_तयार_करा.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) साधने/सीओएसएल_वितरण.py bundle
	$(PYTHON) साधने/पुन्हाजोडा_चाचणी.py
desktop: build
	$(PYTHON) साधने/आज्ञा_कार्यवाही_करा.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) साधने/शेल_चाचणी.py
test-windows: build
	$(PYTHON) साधने/खिडक्या_चाचणी.py
test-swing: build
	$(PYTHON) साधने/स्विंग_चाचणी.py
test-stream: build
	$(PYTHON) साधने/प्रवाह_चाचणी.py
test-ftp: build
	$(PYTHON) साधने/फाइल_ट्रान्सफर_प्रोटोकॉल_चाचणी.py
test-elf: build
	$(PYTHON) साधने/ईएलएफ_चाचणी.py
test-examples: build
	$(PYTHON) साधने/उदाहरणे_चाचणी.py
network: build
	$(PYTHON) साधने/आज्ञा_कार्यवाही_करा.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) साधने/संकेतन_चाचणी.py
test-desktop: build
	$(PYTHON) साधने/डेस्कटॉप_चाचणी.py
run: build
	$(PYTHON) साधने/आज्ञा_कार्यवाही_करा.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) साधने/जावाआभासीयंत्र_चाचणी.py
test: build test-compiler
	$(PYTHON) साधने/हांगुल_आदान_चाचणी.py
	$(PYTHON) साधने/शेल_चाचणी.py
	$(PYTHON) साधने/डेस्कटॉप_चाचणी.py
	$(PYTHON) साधने/खिडक्या_चाचणी.py
	$(PYTHON) साधने/स्विंग_चाचणी.py
	$(PYTHON) साधने/प्रवाह_चाचणी.py
	$(PYTHON) साधने/संकेतन_चाचणी.py
	$(PYTHON) साधने/जावाआभासीयंत्र_चाचणी.py
	$(PYTHON) साधने/प्रणालीप्रारंभ_चाचणी.py
	$(PYTHON) साधने/बंडल_चाचणी.py
	$(PYTHON) साधने/बिंदूघनता_चाचणी.py
	$(PYTHON) साधने/विंडो_पुनर्मापन_चाचणी.py
image: build
	$(PYTHON) साधने/चित्र_तयार_करा.py --resolution $(RESOLUTION)
	$(PYTHON) साधने/निर्यात_करा_विकाससाधनसंच.py
sdk: build
	$(PYTHON) साधने/निर्यात_करा_विकाससाधनसंच.py

.PHONY: सर्व_बांधणी सिस्टम_बांधणी आज्ञा_कार्यवाही_करा चाचण्या संचार डेस्कटॉप_दृश्य चित्र_मूल्य विकास_संच
सर्व_बांधणी: all
सिस्टम_बांधणी: build
आज्ञा_कार्यवाही_करा: run
चाचण्या: test
संचार: network
डेस्कटॉप_दृश्य: desktop
चित्र_मूल्य: image
विकास_संच: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) साधने/प्रणालीप्रारंभ_चाचणी.py
test-remmina: build
	$(PYTHON) साधने/रेमिना_चाचणी.py
test-naming:
	$(PYTHON) साधने/नामकरण_तपासा.py --सी_भाषा
	$(PYTHON) साधने/थेट_कॉल्स_तपासा.py
	$(PYTHON) साधने/स्रोत_पुनरावलोकन.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) साधने/बंडल_चाचणी.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) साधने/बिंदूघनता_चाचणी.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) साधने/विंडो_पुनर्मापन_चाचणी.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) साधने/पडदा_ताजे_करा_चाचणी.py

.PHONY: test-system
test-system: build
	$(PYTHON) साधने/सिस्टम_साधने_चाचणी.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) साधने/सामान्य_भाषा_रनटाइम_पडताळण्या.py

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
