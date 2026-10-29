PYTHON ?= python3
RESOLUTION ?= 640x480
ARGS ?=
.PHONY: all build run test test-compiler test-jvm test-shell test-desktop test-windows test-swing test-stream test-coding test-ftp test-elf test-examples network desktop image sdk
all: build
.PHONY: remote test-remote test-passwords remoto_Conexão
remote: build
	$(PYTHON) ferramentas/Executar_comando.py --remote --resolution $(RESOLUTION) $(ARGS)
remoto_Conexão: remote
test-remote: build
	$(PYTHON) ferramentas/conexão_remota_teste.py
test-passwords: build
	$(PYTHON) ferramentas/senha_duração_teste.py
.PHONY: test-genet
test-genet:
	mkdir -p build
	clang -std=c11 -Wall -Wextra -Werror -idirafter rede_pilha -I vendor/lwip/src/include testes/com_fio_rede_teste.c -o build/genet-mock-test
	build/genet-mock-test
build:
	$(PYTHON) ferramentas/construir.py
.PHONY: cosl-check cosl-dist test-relink
cosl-check:
	$(PYTHON) ferramentas/COSL배포.py check
cosl-dist: build
	$(PYTHON) ferramentas/Criar_foto.py --resolution $(RESOLUTION)
test-relink:
	$(PYTHON) ferramentas/COSL배포.py bundle
	$(PYTHON) ferramentas/재연결시험.py
desktop: build
	$(PYTHON) ferramentas/Executar_comando.py --desktop --resolution $(RESOLUTION) $(ARGS)
test-shell: build
	$(PYTHON) ferramentas/teste_shell.py
test-windows: build
	$(PYTHON) ferramentas/teste_Windows.py
test-swing: build
	$(PYTHON) ferramentas/teste_Swing.py
test-stream: build
	$(PYTHON) ferramentas/teste_fluxo.py
test-ftp: build
	$(PYTHON) ferramentas/teste_FTP.py
test-elf: build
	$(PYTHON) ferramentas/실행파일시험.py
test-examples: build
	$(PYTHON) ferramentas/예제시험.py
network: build
	$(PYTHON) ferramentas/Executar_comando.py --network --resolution $(RESOLUTION) $(ARGS)
test-coding: build
	$(PYTHON) ferramentas/코딩시험.py
test-desktop: build
	$(PYTHON) ferramentas/teste_desktop.py
run: build
	$(PYTHON) ferramentas/Executar_comando.py --resolution $(RESOLUTION) $(ARGS)
test-compiler:
	$(PYTHON) ../../compiler/test_arm64.py
test-jvm: build
	$(PYTHON) ferramentas/teste_JVM.py
test: build test-compiler
	$(PYTHON) ferramentas/한글입력시험.py
	$(PYTHON) ferramentas/teste_shell.py
	$(PYTHON) ferramentas/teste_desktop.py
	$(PYTHON) ferramentas/teste_Windows.py
	$(PYTHON) ferramentas/teste_Swing.py
	$(PYTHON) ferramentas/teste_fluxo.py
	$(PYTHON) ferramentas/코딩시험.py
	$(PYTHON) ferramentas/teste_JVM.py
	$(PYTHON) ferramentas/부팅시험.py
	$(PYTHON) ferramentas/teste_grupo.py
	$(PYTHON) ferramentas/resolução_teste.py
	$(PYTHON) ferramentas/teste_janela_redimensionamento.py
image: build
	$(PYTHON) ferramentas/Criar_foto.py --resolution $(RESOLUTION)
	$(PYTHON) ferramentas/exportar_SDK.py
sdk: build
	$(PYTHON) ferramentas/exportar_SDK.py

.PHONY: 모두 construir Executar_comando testes comunicação desktop_Exibir foto_VALOR kit_de_desenvolvimento
모두: all
construir: build
Executar_comando: run
testes: test
comunicação: network
desktop_Exibir: desktop
foto_VALOR: image
kit_de_desenvolvimento: sdk

.PHONY: test-boot test-remmina test-naming
test-boot: build
	$(PYTHON) ferramentas/부팅시험.py
test-remmina: build
	$(PYTHON) ferramentas/원격한글시험.py
test-naming:
	$(PYTHON) ferramentas/명명검사.py --C_Idioma
	$(PYTHON) ferramentas/직접호출검사.py
	$(PYTHON) ferramentas/fonte_análise.py

.PHONY: test-pip
test-pip: build
	$(PYTHON) ferramentas/teste_grupo.py

.PHONY: test-resolution
test-resolution: build
	$(PYTHON) ferramentas/resolução_teste.py

.PHONY: test-resize
test-resize: build
	$(PYTHON) ferramentas/teste_janela_redimensionamento.py

.PHONY: test-redraw
test-redraw: build
	$(PYTHON) ferramentas/tela_renovar_teste.py

.PHONY: test-system
test-system: build
	$(PYTHON) ferramentas/teste_Sistema_Ferramentas.py

.PHONY: test-layers
test-layers: build
	$(PYTHON) ferramentas/실행계층점검.py

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
