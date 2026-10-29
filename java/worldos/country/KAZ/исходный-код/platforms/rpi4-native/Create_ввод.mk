PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords удаленный_Connect
remote: build
	$(PYTHON) инструменты/실행.py --remote --resolution $(RESOLUTION) $(ARGS)
удаленный_Connect: remote
test-remote: build
	$(PYTHON) инструменты/удаленное_подключение_тест.py
test-passwords: build
	$(PYTHON) инструменты/пароль_длина_тест.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter сеть_стек -I vendor/lwip/src/include испытания/проводной_сеть_тест.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) инструменты/сборка.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) инструменты/COSL배포.py check
cosl-dist: build
	$(PYTHON) инструменты/Create_фото.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) инструменты/COSL배포.py bundle
	$(PYTHON) инструменты/재연결시험.py
desktop: build
	$(PYTHON) инструменты/실행.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) инструменты/тест_оболочка.py
test-windows: build
	$(PYTHON) инструменты/тест_Windows.py
test-swing: build
	$(PYTHON) инструменты/тест_свинг.py
test-stream: build
	$(PYTHON) инструменты/тест_поток.py
test-ftp: build
	$(PYTHON) инструменты/тест_FTP.py
test-elf: build
	$(PYTHON) инструменты/실행파일시험.py
test-examples: build
	$(PYTHON) инструменты/예제시험.py
network: build
	$(PYTHON) инструменты/실행.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) инструменты/코딩시험.py
test-desktop: build
	$(PYTHON) инструменты/тест_компьютер.py
run: build
	$(PYTHON) инструменты/실행.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) инструменты/тест_виртуальная_машина_Java.py
test: build test-compiler
	$(PYTHON) инструменты/한글입력시험.py
	$(PYTHON) инструменты/тест_оболочка.py
	$(PYTHON) инструменты/тест_компьютер.py
	$(PYTHON) инструменты/тест_Windows.py
	$(PYTHON) инструменты/тест_свинг.py
	$(PYTHON) инструменты/тест_поток.py
	$(PYTHON) инструменты/코딩시험.py
	$(PYTHON) инструменты/тест_виртуальная_машина_Java.py
	$(PYTHON) инструменты/부팅시험.py
	$(PYTHON) инструменты/тест_пакет.py
	$(PYTHON) инструменты/разрешение_тест.py
	$(PYTHON) инструменты/тест_окно_изменение_размера.py
image: build
	$(PYTHON) инструменты/Create_фото.py --resolution $(RESOLUTION)
	$(PYTHON) инструменты/экспортировать_пакет_SDK.py
sdk: build
	$(PYTHON) инструменты/экспортировать_пакет_SDK.py

.PHONY: 모두 сборка 실행 испытания коммуникация компьютер_Вид фото_ЗНАЧЕН комплект_SDK
모두: all
сборка: build
실행: run
испытания: test
коммуникация: network
компьютер_Вид: desktop
фото_ЗНАЧЕН: image
комплект_SDK: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) инструменты/부팅시험.py
test-remmina: build
	$(PYTHON) инструменты/원격한글시험.py
test-naming:
	$(PYTHON) инструменты/명명검사.py --C_Язык
	$(PYTHON) инструменты/직접호출검사.py
	$(PYTHON) инструменты/источник_отзыв.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) инструменты/тест_пакет.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) инструменты/разрешение_тест.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) инструменты/тест_окно_изменение_размера.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) инструменты/экран_обновить_тест.py

.PHONY: test-system
test-system: build
	$(PYTHON) инструменты/тест_система_Инструменты.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) инструменты/실행계층점검.py

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
