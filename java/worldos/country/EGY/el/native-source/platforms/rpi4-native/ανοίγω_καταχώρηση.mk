PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords απομακρυσμένος_συνδέω
remote: build
	$(PYTHON) Εργαλεία/εκτελώ_εντολή.py --remote --resolution $(RESOLUTION) $(ARGS)
απομακρυσμένος_συνδέω: remote
test-remote: build
	$(PYTHON) Εργαλεία/απομακρυσμένη_σύνδεση_δοκιμή.py
test-passwords: build
	$(PYTHON) Εργαλεία/κωδικός_πρόσβασης_διάρκεια_δοκιμή.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter δίκτυο_δέσμη -I vendor/lwip/src/include 시험/ενσύρματος_δίκτυο_δοκιμή.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) Εργαλεία/δομή_Σύστημα.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) Εργαλεία/COSL배포.py check
cosl-dist: build
	$(PYTHON) Εργαλεία/ανοίγω_εικόνα.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) Εργαλεία/COSL배포.py bundle
	$(PYTHON) Εργαλεία/재연결시험.py
desktop: build
	$(PYTHON) Εργαλεία/εκτελώ_εντολή.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) Εργαλεία/δοκιμή_κέλυφος.py
test-windows: build
	$(PYTHON) Εργαλεία/창시험.py
test-swing: build
	$(PYTHON) Εργαλεία/δοκιμή_Σουϊνγκ.py
test-stream: build
	$(PYTHON) Εργαλεία/δοκιμή_ροή.py
test-ftp: build
	$(PYTHON) Εργαλεία/δοκιμή_πρωτόκολλο_μεταφοράς_αρχείων.py
test-elf: build
	$(PYTHON) Εργαλεία/실행파일시험.py
test-examples: build
	$(PYTHON) Εργαλεία/예제시험.py
network: build
	$(PYTHON) Εργαλεία/εκτελώ_εντολή.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) Εργαλεία/코딩시험.py
test-desktop: build
	$(PYTHON) Εργαλεία/δοκιμή_υπολογιστής.py
run: build
	$(PYTHON) Εργαλεία/εκτελώ_εντολή.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) Εργαλεία/δοκιμή_εικονική_μηχανή_Java.py
test: build test-compiler
	$(PYTHON) Εργαλεία/한글입력시험.py
	$(PYTHON) Εργαλεία/δοκιμή_κέλυφος.py
	$(PYTHON) Εργαλεία/δοκιμή_υπολογιστής.py
	$(PYTHON) Εργαλεία/창시험.py
	$(PYTHON) Εργαλεία/δοκιμή_Σουϊνγκ.py
	$(PYTHON) Εργαλεία/δοκιμή_ροή.py
	$(PYTHON) Εργαλεία/코딩시험.py
	$(PYTHON) Εργαλεία/δοκιμή_εικονική_μηχανή_Java.py
	$(PYTHON) Εργαλεία/부팅시험.py
	$(PYTHON) Εργαλεία/δοκιμή_πακέτο.py
	$(PYTHON) Εργαλεία/ανάλυση_δοκιμή.py
	$(PYTHON) Εργαλεία/창크기시험.py
image: build
	$(PYTHON) Εργαλεία/ανοίγω_εικόνα.py --resolution $(RESOLUTION)
	$(PYTHON) Εργαλεία/개발꾸러미내보내기.py
sdk: build
	$(PYTHON) Εργαλεία/개발꾸러미내보내기.py

.PHONY: 모두 δομή_Σύστημα εκτελώ_εντολή 시험 통신 υπολογιστής_Προβολή εικόνα_τιμή κιτ_ανάπτυξης_λογισμικού
모두: all
δομή_Σύστημα: build
εκτελώ_εντολή: run
시험: test
통신: network
υπολογιστής_Προβολή: desktop
εικόνα_τιμή: image
κιτ_ανάπτυξης_λογισμικού: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) Εργαλεία/부팅시험.py
test-remmina: build
	$(PYTHON) Εργαλεία/원격한글시험.py
test-naming:
	$(PYTHON) Εργαλεία/명명검사.py --Ταχυδρομικός_κώδικας_Γλώσσα
	$(PYTHON) Εργαλεία/직접호출검사.py
	$(PYTHON) Εργαλεία/προέλευση_κριτική.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) Εργαλεία/δοκιμή_πακέτο.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) Εργαλεία/ανάλυση_δοκιμή.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) Εργαλεία/창크기시험.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) Εργαλεία/화면갱신시험.py

.PHONY: test-system
test-system: build
	$(PYTHON) Εργαλεία/δοκιμή_Σύστημα_Εργαλεία.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) Εργαλεία/실행계층점검.py

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
