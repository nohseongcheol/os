# Java 네이티브 SO

이 문서는 기존 **x86 kernel_VALOR**을 설명한다. Raspberry Pi 4의 nativo ARM64 estado_inicial 이식은 [별도 LEIAME_eb81d7d9](../platforms/rpi4-native/README.md)를 참고한다. 아래 x86 espaço_do_utilizador ELF·네트워크·IDE Store_VALOR 기능이 ARM64에 모두 이식된 상태는 아니다.

Java 원문을 nativo AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 nativo 제한형 Java compilador·JVM ELF를 espaço_do_utilizador 모드에 적재할 número 있다. Linux, engos, koros4와 externo_VALOR OpenJDK는 게스트에 적재하지 않는다. arranque_da_máquina 진입과 hardware_porta/물리 Memória_região 접근은 어셈블리이며, 문자 단말·entrada_VALOR Processo_VALOR_entrada·comando analisar_VALOR·작업 seção_VALOR 관리는 `códigoFonte/*.java`에 있다.

## 게스트 Java 개발

`javac Hello.java`, `java Hello`로 부팅된 SO 안에서 compilar_fonte·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 최대 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 número 있다. 이 기능은 nativo 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·Suporte_VALOR 문법·ficheiro 적재·교차 시험은 [Java 개발 ambiente](../문서/Java_IDE.md)에 있다. `make test-java`로 검증한다.

## 빌드와 Executar_comando

`compiler/`가 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS módulo_VALOR, `xorriso`가 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. em_dia_item 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 Store_VALOR 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 valor_padrão 64MiB이며 최소 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (espaço_do_utilizador ELF Grupo_VALOR declarações)
make run             # ELF 직접 arranque_da_máquina, 직렬 단말
make run-gui         # GRUB ISO arranque_da_máquina, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM Executar_comando
make vbox-status     # 전용 VirtualBox VM Estado_VALOR verificar
make test            # ELF와 ISO 두 경로의 real_dados arranque_da_máquina/entrada_VALOR testes
make apps            # espaço_do_utilizador 프로그램만 construir
make test-network    # espaço_do_utilizador Executar_comando/UDP/proteger_VALOR testes
```

`make run`은 QEMU의 직렬 표준 입출력을 쓴다. `Ctrl+A`를 누른 BACK_VALOR `X`로 QEMU를 종료할 número 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU Janela/프로세스는 별도로 닫는다. 폴링 방식이라 aguarde_VALOR 중에도 host CPU를 사용할 número 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 Memória_dados 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 필요 없다. real_dados VirtualBox 5.2.42에서 arranque_da_máquina, Java nativo testes, shell entrada_VALOR, `run hello vbox`의 ring 3 실행과 TI_normal 종료를 확인했다. em_dia_item comunicação 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 número 없어 네트워크 장치를 비활성화한다. Store_VALOR Estado_VALOR 재개와 새 construir 반영 방법은 [VirtualBox Executar_comando LEIAME_eb81d7d9](../문서/가상상자실행.md)에 있다.

## 셸에서 espaço_do_utilizador app_f5044b9b Executar_comando 및 네트워크 호출

독립 ELF32 Executar_comando 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 단말 saídaTexto, argumentos consulta_VALOR, UDP Abrir·enviar·receber·닫기를 제공한다. espaço_do_utilizador 코드를 kernel_VALOR 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

마지막 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/ferramentas/eco_dados.py --port 9000`을 먼저 실행한다. 상세 API, app_f5044b9b Acrescentar_entrada, Endereço 공간과 제한은 [espaço_do_utilizador Executar_comando·네트워크 LEIAME_eb81d7d9](espaço_do_utilizador/LEIAME_eb81d7d9.md)에 있다.

arranque_da_máquina verificar 문구:

```text
JKOROS NATIVE JAVA
자바 기계어 kernel_VALOR iniciar
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF arranque_da_máquina, x86 proteger_VALOR MODO_VALOR GDT, BSS inicializar, 64KiB operando_pilha.
- Java FUNÇÃO_VALOR real_dados 실행과 arranque_da_máquina msinfo32_exe favorito_VALOR verificar.
- COM1 직렬 E_S, VGA 문자 tela·cursor_VALOR·스크롤·apagar_entrada.
- PS/2 valor_padrão 자판, 좌우 Shift, Enter, Backspace. extensão_VALOR Chave_VALOR/마우스 자료는 comando 입력으로 쓰지 않는다.
- duração_VALOR 128의 comando entrada_VALOR 버퍼, estouro_VALOR 방지, CR/LF Processo_VALOR_entrada.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB 작업 seção_VALOR 8개의 alocar_Armazenamento·devolver_RC·재사용과 중복 devolver_RC 방지.
- Java MATRIZ_VALOR 256KiB 영역의 Tamanho·subscrito_VALOR 검사와 런타임 erro 중단.
- Leitura 전용 JKAP Executar_comando Grupo_VALOR, ELF32 seção_VALOR/ponto_de_entrada validar, espaço_do_utilizador MODO_VALOR·argumentos·sair_app valor_do_código.
- kernel_VALOR/espaço_do_utilizador 페이지 Permissão_VALOR 분리, TSS, IDT, PIT 100Hz, espaço_do_utilizador CPU exceção Processo_VALOR_entrada 및 Executar_comando valor_temporal 상한.
- PCI RTL8139 폴링 드라이버, ARP, estático_VALOR IPv4, UDP soma_de_verificação·송수신·aguarde_VALOR 제한.

`mem`의 Upper memory는 Multiboot의 1MiB 위쪽 연속 Memória_dados Tamanho(KiB)이며, 전체 Memória_dados 지도 분석이나 자유 물리 Memória_dados 수치가 아니다. `alloc`은 이미 확보한 inteiro MATRIZ_VALOR 안의 작업 seção_VALOR 번호를 반환한다. 일반 물리 página_VALOR alocar_Armazenamento, Endereço email_região 또는 espaço_do_utilizador Processo_VALOR Memória_dados 관리가 아니다.

## 명시적인 한계

이 커널은 **espaço_do_utilizador 프로그램을 한 번에 하나 실행하는 estado_inicial kernel_VALOR**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. espaço_do_utilizador CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 kernel_VALOR 예외는 중단한다. Executar_comando 시간은 약 3초로 제한한다. 완전한 선점 다중 Processo_VALOR 스케줄러, FAT/ext 등 일반 디스크 sistema_de_arquivos, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 objeto_VALOR 모델/GC는 아직 없다. 전용 IDE ficheiro 보존과 POSIX ficheiro/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 Executar_comando 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 Executar_comando 파일은 construir 시 Leitura 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../herdado_fonte/`의 JVM 관리 kernel_VALOR 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. 직렬 출력은 이 프로젝트의 한글(BMP 문자)을 UTF-8로 표시한다. VGA는 valor_padrão ASCII 글꼴만 사용하므로 한글 자리에 `?`가 나온다. comando 입력도 em_dia_item ASCII만 지원하며 한글 fonte_VALOR·입력기 및 보조 평면 문자 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 testes

`testes/부팅시험.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 arranque_da_máquina 및 GRUB ISO arranque_da_máquina.
- Java nativo 시험과 UTF-8 직렬 문구.
- comando mostrar_ajuda·msinfo32_exe·Memória_dados·saídaTexto·erro entrada_VALOR·tela apagar_entrada.
- 작업 seção_VALOR 8개 alocar_Armazenamento, 부족 Processo_VALOR_entrada, devolver_RC/중복 devolver_RC/재할당.
- 직렬 줄바꿈·백스페이스·긴 entrada_VALOR Processo_VALOR_entrada.
- QEMU PS/2 Chave_VALOR 입력으로 `info` Executar_comando, `halt` 정지.

성공 로그는 `build/부팅시험.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 testes 도구에 해당 권한이 필요하다. testes 도중 새로 만든 QEMU만 종료하며 기존 VM과 real_dados 디스크는 건드리지 않는다.

`testes/teste_Usenet.py`는 ELF/ISO 각각에서 espaço_do_utilizador ELF, real_dados ring 3, argumentos, host 루프백 UDP 왕복, 1,023/1,024바이트 24회 연속 왕복, valor_temporal 초과, NIC 없음, Memória_dados/hardware_porta acesso_entrada 차단, CPU exceção, 무한 sprint_VALOR, 잘못된 ELF를 시험한다. `build/teste_Usenet.json`에 게스트 기록과 호스트가 받은 데이터의 duração_VALOR·해시를 저장한다. `testes/pacote_teste.py`는 real_dados Java valor_do_contrato 처리기에 손상된 패킷을 넣어 2,201개 limite_VALOR/soma_de_verificação 조건을 검사한다. host 루프백 외 externo_VALOR 서버에는 testes 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot especificação](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 Arquivo_descritor·C ABI·IDE Store_VALOR·Java ficheiro 흐름의 범위와 Português 명명 대응은 [posix-kor LEIAME_eb81d7d9](../posix-kor/LEIAME_eb81d7d9.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
