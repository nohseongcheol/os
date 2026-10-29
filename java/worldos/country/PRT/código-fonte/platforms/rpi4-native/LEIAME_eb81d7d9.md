# Raspberry Pi 4 nativo Java kernel_VALOR — espaço_do_utilizador Executar_comando 기반

em_dia_item nativo 코드의 COSL 상업 doença, 제3자 고지 및 LGPL 재연결 자료는 [COSL distribuição_VALOR LEIAME_eb81d7d9](COSL배포안내.md)를 참고한다. mudar_MODO 전 GPL 구성의 판단은 [Anterior_item 라이선스 검토](licença_análise.md)에 기록했다.

Português comunicação·exceção 사용법은 [Português Java API](한국어자바/LEIAME_eb81d7d9.md), FUNÇÃO_VALOR·variável_VALOR·ficheiro 이름의 변경과 어원 근거는 [명명 LEIAME_eb81d7d9](명명/LEIAME_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 nativo AArch64 커널이다. Java AOT kernel_VALOR 위에 **linha_de_comando shell, 게스트 Java compilador·JVM, MicroPython, EL0 C++ Executar_comando, ficheiro·UDP 루프백 시스템 호출, 여러 한글 GUI terminal·vi Editor·Swing 부분집합**을 제공한다. 커널의 ficheiro dados/정책·루프백 Transferir_VALOR·shell 상태는 Java, tela 합성·pixel alterar_VALOR·ponteiro·클리핑도 Java로 구현하며, CPU/MMU/celular_VALOR 경계와 terminal·caractere_VALOR Paint_tela 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 nativo 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 Executar_comando, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 com_fio_VALOR 송수신은 아직 미검증이다.** Executar_comando·conexão_e05f319b·senha_VALOR 확인은 [externo_VALOR conexão_e05f319b LEIAME_eb81d7d9](externo_conexão_guia.md)에 정리했다.

셸은 EL1 kernel_VALOR, `java` 등 espaço_do_utilizador Executar_comando 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 Executar_comando·conexão_e05f319b 방법 및 real_dados 검증은
[Executar_comando 계층과 externo_VALOR comunicação 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 real_dados Executar_comando 형식으로 검사한다. `./saudação_ae353e94`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 estático_VALOR ELF는 `run --linux nome_de_arquivo_SMS`으로 실행한다. [ELF·Linux ABI Suporte_VALOR 범위와 동일 바이너리 testes](executável_ABI.md).

GUI와 네트워크는 `python3 ferramentas/Executar_comando.py --desktop --network`로 함께 사용한다. Java·C·Python의 Português 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 arranque_da_máquina 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 número 있다. Remmina에서 **F9/Shift+Space/한·zero_operando Chave_VALOR**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·real_dados TCP/UDP·ficheiro byte_VALOR·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java ExemploJanela`로 Português Swing 예제를 실행한다. terminal 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 em_dia_item COL_VALOR·LIN_VALOR 수를 보여 준다.

## em_dia_item Suporte_VALOR recortar

| 기능 | implementação·시험한 recortar | 아직 미지원 |
|---|---|---|
| arranque_da_máquina | Pi4 AArch64 EL1, UART, SD용 BLD_foto, QEMU raspi4b arranque_da_máquina | real_dados Pi4 보드에서의 펌웨어 arranque_da_máquina testes |
| Java kernel_VALOR | estático_VALOR Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objeto_VALOR/exceção/GC/JVM/표준 biblioteca |
| Java 개발 ferramentas | 게스트 nativo `javac`/`java`, JVM 0.4/JAR: 다중 aula_VALOR·objeto_VALOR·상속·exceção·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Português biblioteca. 게스트 컴파일러는 estático_VALOR Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | real_dados MicroPython 1.24.1 EL0 이식, fonte_árvore compilar_fonte/Executar_comando, aula_VALOR·exceção·GC·큰 inteiro·Unicode·ficheiro·UDP/tela Ligar | CPython, pip, C extensão_VALOR, 부동소수점, 일반 OS/스레드/soquete_VALOR módulo_VALOR, interativo REPL |
| shell | UTF-8 Editar_VALOR·LOG_linha·concluído_VALOR, 디렉터리·ficheiro comando, variável_VALOR·doença·script_VALOR, 16 KiB 순차 파이프·리다이렉션, ELF Executar_comando | 전체 POSIX sh/Bash, 작업 visual_VALOR·동시 프로세스·PTY |
| C/AOT compilar_fonte | 게스트 TinyCC 및 estático_VALOR Java 부분집합 `jaot` → nativo ARM64 ELF | 전체 libc·모든 Java aula_VALOR AOT |
| C++ | 독립 ELF64를 EL0에서 Executar_comando; estático_VALOR 생성자, RAII 소멸자, FP/SIMD, Português ficheiro/루프백 호출 | libc/libstdc++, STL, C++ exceção·RTTI·동적 Ligar |
| espaço_do_utilizador proteger_VALOR | 4 KiB 페이지, valor_do_código RX/dados RW·NX, kernel_VALOR·MMIO 차단, guard page, 잘못된 ponteiro 검사 | 다중 espaço_do_utilizador Permissão_VALOR, 일반 프로세스/스레드 스케줄러 |
| Executar_comando valor_temporal 제한 | GIC-400 타이머로 무한 sprint_VALOR sair_app; interativo entrada_VALOR 대기는 기한 renovar, 터미널별 EL0 app_f5044b9b 중단·CV_execução | 일반적인 선점형 다중작업. 긴 kernel_VALOR 호출 도중에는 종료가 지연될 número 있음 |
| ficheiro | Java RAM ficheiro 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, par_VALOR/절대 caminho 63바이트, descritor_entrada 16개 | Permissão_VALOR, 디스크/SD 영속 Store_VALOR |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP implementação, 게스트 FTP·SSH·VNC | GENET 실물 validar, Wi-Fi, DNS, 일반 TLS soquete_VALOR, RDP |
| GUI | 최대 네 terminal Janela, seleção_VALOR·mover_VALOR·X Fechar, 한글 fonte_VALOR, Swing 부분집합; 게스트 VNC tela·entrada_VALOR·두벌식 | 실물 USB entrada_VALOR, 전체 AWT/Swing·Java2D·Janela 관리 정책 |
| 작업 thread_VALOR | kernel_VALOR 작업 2개와 주 작업; JVM 내부 thread_VALOR 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 nome_de_arquivo_SMS/datagrama | GUI의 일반 다국어 조판 |

Executar_comando 버튼 화면은 5×7 영문 글꼴을 쓰며, terminal 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 real_dados 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 kernel_VALOR 내부의 datagrama 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 ferramentas/Executar_comando.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·Executar_comando 제한과 Português 사용법은 [nativo JVM과 Português biblioteca](자바실행환경.md)에 정리했다. aula_VALOR ficheiro/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `Português.자바`와 별도인 `Português.nativo` 패키지다.

**vi·여러 Janela·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 개발 매뉴얼](개발안내.md)에 정리했다.**

GUI terminal Executar_comando·단축키·shell comando·제한은 [셸과 terminal 사용법](shell_E_Terminal.md)에 정리했다.

## em_dia_item 컴퓨터에서 Executar_comando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

sair_app: **Ctrl+A Avançar_item X**. 게스트 C/AOT ferramentas 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. host 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. compilador 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/caminho/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` Suporte_VALOR 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 Executar_comando**한다. 기존 한 caractere_VALOR 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 argumentos 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| comando | Acção |
|---|---|
| `help` / `info` | comando·real_dados implementação Estado_VALOR |
| `ls` / `cat FILE` / `rm FILE` | RAM ficheiro entrada_Lista_f07b3200·Conteúdo_VALOR·삭제 |
| `vi FILE` | espaço_do_utilizador região_VALOR vi 부분집합, 한글 Editar_VALOR·Store_VALOR·검색·되돌리기 |
| `edit FILE` | ficheiro 전체를 새로 entrada_VALOR; 단독 `.` 줄로 Store_VALOR, Ctrl-C로 Close_cirurgia |
| `javac FILE.java` / `java CLASS [ARGS]` | nativo 제한형 Java compilar_fonte·Executar_comando |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython compilar_fonte·Executar_comando |
| `load FILE` / `hex FILE` | 16진수 바이너리 entrada_VALOR/saídaTexto; 입력은 단독 `.` 줄로 Store_VALOR |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 nativo ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 proteger_VALOR testes |
| `gui` / `terminal` | Executar_comando tela / 한글 GUI terminal; F12로 terminal Abrir·Fechar |
| `samples` | 삭제한 valor_padrão 예제 recuperar_Estado; 기존 파일은 보존 |

예를 들어 `edit saudação_ae353e94.java`를 입력한 Avançar_item 아래 소스를 입력한다.

```java
public class saudação_ae353e94 { public static void main(String[] args) { int VALOR = 7; System.out.println("한글=" + VALOR); } }
```

그다음 단독 `.` 줄로 저장하고 `javac saudação_ae353e94.java`, `java saudação_ae353e94`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Close_cirurgia·잘못된 16진수·capacidade_VALOR 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, Executar_comando 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 comando 인수는 최대 32개다. Citação·백슬래시·shell variável_VALOR·파이프·리다이렉션 범위는 [shell 설명](shell_E_Terminal.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, Endereço **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode entrada_VALOR·명시적 colar_VALOR·Executar_comando 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 ferramentas/Executar_comando.py --desktop --network
# 다른 hardware_porta: python3 ferramentas/Executar_comando.py --desktop --port 5903
```

종료는 실행한 host 터미널에서 Ctrl+C다. 기존 `python3 ferramentas/Executar_comando.py --vnc 127.0.0.1:2`는 tela 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. real_dados Pi4 USB 입력기는 아직 없으며, VNC Ligar 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 real_dados C++/UDP ELF Executar_comando, `Hello.java` compilar_fonte 후 JVM Executar_comando, `hello.py` Executar_comando, GUI terminal 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interativo 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Memória_dados·CPU 문맥을 보관한다. shell·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## real_dados 산출물과 Pi4 SD BLD_foto

```sh
make image   # kernel_VALOR, SD BLD_foto, arranque_da_máquina ZIP, 사용자용 SDK
make sdk     # SDK만 repetir_VALOR gerar
```

| caminho | 용도 |
|---|---|
| `build/kernel8.img` | nativo kernel_VALOR 기계어, 적재 Endereço 0x80000 |
| `build/kernel.elf`, `kernel.map` | kernel_VALOR símbolo_VALOR·disposição_de_ligação |
| `build/user/demo.elf` | espaço_do_utilizador MODO_VALOR C++ ficheiro/heap_VALOR/ponto_flutuante_VALOR/그래픽 예제 |
| `build/user/network.elf` | espaço_do_utilizador MODO_VALOR C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | nativo Java 부분집합 compilador/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | host javac용 Português API aula_VALOR; 같은 클래스가 nativo JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Português API Java códigoFonte |
| `build/user/vi.elf` | nativo UTF-8 vi comando 부분집합 Editor |
| `build/user/python.elf` | nativo ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 proteger_VALOR testes 전용 |
| `build/libposix-kor-arm64.a` | **kernel_VALOR 내부**에서 Java ficheiro 구현을 직접 부르는 기존 Ligar |
| `build/libposix-kor-user.a` | **EL0 espaço_do_utilizador app_f5044b9b**에서 SVC로 ficheiro/루프백을 호출하는 새 Ligar |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD BLD_foto |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 arranque_da_máquina 파티션에 복사할 ficheiro Grupo_VALOR |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·iniciar valor_do_código·biblioteca·링커 script_VALOR·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 real_dados Suporte_VALOR Estado_VALOR |

이미지는 확인된 공식 Pi arranque_da_máquina 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·terminal fonte_VALOR 라이선스와 fonte_VALOR origem_VALOR 해시도 동봉한다. ficheiro gerar 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 BLD_foto LOG_linha 도구로 `.img`를 기록하거나 FAT32 arranque_da_máquina 파티션 최상위에 ZIP 내용을 푼다. BLD_foto 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 valor_padrão EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD ficheiro 구성·kernel_VALOR 체크섬 검사와 물리 Quadro arranque_da_máquina 검증은 별개다. MMU uso_VALOR 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 arranque_da_máquina 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 Português API uso_VALOR

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/ExemploFicheiro.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int START_usuário_app(int)`이다. espaço_do_utilizador C++는 FP/SIMD를 사용할 número 있다. kernel_VALOR C/Java AOT는 일반 레지스터만 사용하므로 exceção Processo_VALOR_entrada 중 espaço_do_utilizador FP 상태를 건드리지 않는다. espaço_do_utilizador ponto_de_entrada_VALOR 시 FP 상태를 초기화하고 kernel_VALOR 복귀에 필요한 상태를 보존한다.

```cpp
#include "Arquivo_ABI.h"
extern "C" int START_usuário_app(int) {
    int ficheiro = abrir_Arquivo("saudação_ae353e94.txt", de_leitura_gravação | 없으면만들기 | cortar_Sumário, 0600);
    if (ficheiro < 0) return 1;
    const char Conteúdo_VALOR[] = "안녕하세요";
    int resultado = gravar_Arquivo_dados(ficheiro, Conteúdo_VALOR, sizeof(Conteúdo_VALOR) - 1);
    Close_Arquivo(ficheiro);
    return resultado == sizeof(Conteúdo_VALOR) - 1 ? 0 : 2;
}
```

[ficheiro 예제](espaço_do_utilizador/ExemploFicheiro.cpp)와 [comunicação 예제](espaço_do_utilizador/통신예제.cpp)가 real_dados arranque_da_máquina testes 대상이다. `Arquivo_ABI.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 ficheiro Processo_VALOR_entrada 및 루프백 전달은 Java 커널에서 실행한다. `rede_ABI.h`의 soquete_VALOR 함수는 em_dia_item 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kernel_VALOR 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Avançar_item 도구를 사용하면 **새 QEMU를 부팅해 업로드한 real_dados 바이트를 재확인한 BACK_VALOR 게스트에서 Executar_comando**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 ferramentas/Executar_Arquivo.py build/jkoros-native-sdk/demo.elf
python3 ferramentas/Executar_Arquivo.py 예제/Hello.java "한글 argumentos"
python3 ferramentas/Executar_Arquivo.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kernel_VALOR 묶음에 포함되어 이 ficheiro 한도를 적용받지 않는다. **C++ 컴파일러는 host SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 biblioteca, PT_TLS, PT_INTERP, PT_DYNAMIC, Executar_comando·Escrita 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 ÍNDICE·Endereço recortar·오류는 [espaço_do_utilizador ABI](usuário_Ligar_ABI.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `commit_Arquivos`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 Permissão_VALOR·dup/fcntl은 없다. 디렉터리와 par_VALOR/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, receber_VALOR 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. espaço_do_utilizador sair_app 시 열린 ficheiro 서술자와 소켓을 회수한다.

## validar resultado

`make test-jvm`은 9개 프로그램을 OpenJDK와 real_dados nativo 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `ferramentas/부팅시험.py`는 Java retângulo API의 real_dados tela 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 real_dados VNC entrada_VALOR·한글 terminal 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT cirurgia_VALOR resultado 비교, 런타임 erro 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kernel_VALOR 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/Endereço 초과/겹친 페이지/W+X 등 ELF rejeitar_VALOR 사례 22개.
- EL0 C++ 생성자·RAII·ponto_flutuante_VALOR cirurgia_VALOR·ficheiro·heap_VALOR 및 잘못된 시스템 호출 ponteiro.
- kernel_VALOR/valor_do_código/MMIO Escrita·acesso_entrada, NX operando_pilha·NULL Executar_comando, guard page, 특권 comando 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 TI_normal app_f5044b9b 재실행.
- sprint_VALOR Executar_comando 시 ficheiro/soquete_VALOR 누수 방지, UDP 왕복·보낸 Endereço·잘린 receber_VALOR·큐 포화·빈 datagrama·미지원 comunicação erro.
- shell Editar_VALOR·Close_cirurgia·16진수 업로드/다운로드·espaço_do_utilizador ELF 실행과 잘못된 ELF rejeitar_VALOR.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 Executar_comando, 한글 aula_VALOR·variável_VALOR·nome_de_arquivo_SMS.
- 여러 Janela·vi Store_VALOR·Editar_VALOR·devolver_ponte·espaço_do_utilizador Estado_VALOR 중단/CV_execução, Swing 한글 entrada_VALOR·이벤트·X Fechar, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 inteiro·aula_VALOR·GC sprint_VALOR·ficheiro import·exceção·ficheiro·UDP 왕복·valor_temporal 초과 후 복귀.
- GUI seleção_VALOR mover_VALOR, C++/UDP/Java/MicroPython 버튼 Executar_comando, 콘솔 복귀 및 real_dados 프레임버퍼 픽셀/fonte_VALOR.
- 디렉터리·variável_VALOR·doença·ficheiro comando·script_VALOR·순차 파이프·리다이렉션·capacidade_VALOR 초과 recuperar_Estado, Python stdin/EOF와 Java/Python stdout.
- comando LOG_linha·긴 한글 entrada_VALOR Editar_VALOR·concluído_VALOR·terminal 스크롤, 그래픽 app_f5044b9b sair_app 후 Janela 복원, real_dados VNC Unicode Chave_VALOR·colar_VALOR·마우스.

[kernel_VALOR testes LOG_linha](build/verification/implementation-test.log), [shell testes](build/verification/shell/report.json), [VNC testes](build/verification/desktop/report.json), [computador 판독 resultado](build/verification/report.json), [직렬 LOG_VALOR](build/verification/serial.log), [GUI tela](build/verification/gui-python.png)을 확인할 número 있다. VNC RFB 3.8 Ligar 및 640×480 tela 정보도 검사한다. [SDK 재컴파일 resultado](build/verification/sdk.json)는 두 예제의 ponto_de_entrada·적재 세그먼트·ABI note가 arranque_da_máquina 시험한 ELF와 일치함을 확인한다. símbolo_VALOR 등 비적재 메타데이터를 포함한 ficheiro 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 recortar

nativo `javac`는 버전 49 `.class`를 생성하며 JVM은 Suporte_VALOR 명령으로 구성된 버전 45–52 클래스를 실행한다. estático_VALOR FUNÇÃO_VALOR·재귀·int/boolean/char/String·doença/sprint_VALOR·cadeia_VALOR 결합과 일부 ficheiro 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/composição_VALOR 자모 식별자를 처리한다. Unicode identificador_VALOR 전체 tabela_de_pesquisa·Unicode fonte_árvore 이스케이프는 구현하지 않았다. 게스트 fonte_árvore 컴파일러는 일반 objeto_VALOR·exceção·Thread 구문을 아직 컴파일하지 못한다. host `javac --release 8`로 만든 Suporte_VALOR 부분집합 클래스는 nativo JVM 0.4의 objeto_VALOR·exceção·Thread·UDP와 Português API를 사용할 número 있다. Swing은 문서화한 nativo API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [nativo JVM 설명](자바실행환경.md)이 기준이다. 상세 Idioma 범위는 [공유 Java ferramentas 설명](../../문서/Java_IDE.md)을 참고하되, 그 문서의 x86 shell/Store_VALOR/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 fonte_árvore**를 nativo AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 FUNÇÃO_VALOR·aula_VALOR·exceção·리스트/dicionário·Unicode·GC·가변 precisão_VALOR 정수를 제공한다. em_dia_item 구성은 inteiro 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 biblioteca, pip, subprocess, threading, 일반 socket과 valor_padrão `open()` ficheiro 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objeto_VALOR·모듈은 sair_app 시 회수되고 RAM 파일만 Avançar_item 실행에 남는다.

`import jkoros`로 Avançar_item 시스템 연결을 쓴다. 모두 SVC를 통해 nativo Java 커널에 접근한다.

| FUNÇÃO_VALOR | Acção |
|---|---|
| `stdin(limit)` | em_dia_item 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 leitura_RC; EOF는 빈 bytes, UART dados 없음은 OSError(11) |
| `read(name)` | par_VALOR/절대 RAM 경로의 ficheiro 전체를 bytes로 leitura_RC |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_VALOR, 쓴 byte_VALOR número devolver_RC |
| `remove(name)` | RAM ficheiro 삭제 |
| `rect(x, y, w, h, color)` | 선택한 real_dados tela Tamanho 안의 retângulo desenho_VALOR; 기존 보드의 RGB32 VALOR |
| `ticks_ms()` | arranque_da_máquina 후 밀리초, 32비트 Ciclo_VALOR |
| `udp_open(port)` | 127.0.0.1의 UDP soquete_VALOR Abrir/BIND_empresa; 0은 자동 hardware_porta |
| `udp_send(fd, port, data)` | 루프백 destino_VALOR 포트에 str/bytes 버퍼 Transferir_VALOR |
| `udp_recv(fd)` | `(bytes, 보낸포트)` devolver_RC; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | soquete_VALOR Fechar |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 valor_do_código: [python/](PYTHON_ponte/), [espaço_do_utilizador Java Ligar](espaço_do_utilizador/자바연결.c). 공식 [MicroPython 이식 LEIAME_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. fonte_árvore URL·hash_Arquivo·라이선스는 [vendor LEIAME_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Avançar_item fase_VALOR | 완료 ação_raiz |
|---|---|
| 영속 Store_VALOR·Executar_comando ficheiro entrada_VALOR | SD/MMC 및 디스크 ficheiro 시스템, 시스템/espaço_do_utilizador 볼륨; em_dia_item ELF ficheiro 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 Endereço email_região, 선점 스케줄러, TLS, sincronizar/aguarde_VALOR, 신호, mmap/mprotect |
| libc와 C++ 런타임 | nativo ABI용 libc, malloc/free, 표준 E_S·Relógio·ambiente·locale, libstdc++/exceção Processo_VALOR_entrada validar |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 ficheiro/Unicode/스레드/soquete_VALOR testes |
| OpenJDK/JRE | HotSpot OS camada_VALOR, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 biblioteca 이식; javac/java real_dados Executar_comando |
| externo_VALOR 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 real_dados Quadro 송수신 validar, DNS·Wi-Fi |
| GUI extensão_VALOR | USB HID, 게스트 입력기·문자 조판, Swing Janela Tamanho 조절·클리핑 extensão_VALOR, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 implementação 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 externo_VALOR 네트워크 드라이버는 실물 검증도 필요하다. [QEMU celular_VALOR 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

hardware_VALOR 및 ABI 참고: [BCM2711 acessório](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC Endereço](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox valor_do_contrato](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP visual_VALOR 레지스터 Definição_VALOR](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Português C tipo_de_dados·Python erro·grupo instalar_VALOR

C 네트워크 API는 `struct malha_soquete_email`, enum 상수와 real_dados Português 함수로
구현한다. macro_VALOR 별칭을 사용하지 않으며 Anterior_item pk_* ABI도 유지한다.
Python 예제는 `erro_do_sistema`, `erro.ÍNDICE`, `erro.설명`을 사용한다.

`python3 ferramentas/Executar_comando.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 número 있다. 현재는 host 중계를
이용하는 제한형 MicroPython fonte_árvore 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_grupo.md).

## tela Tamanho seleção_VALOR

`python3 ferramentas/Executar_comando.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. terminal mover_VALOR, Swing 가운데 disposição_de_ligação, Java·C·Python 그리기도 real_dados 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Definições·Português API·validar LEIAME_eb81d7d9](resolução_da_tela.md).

## Português 직접 API와 tela renovar

`example/java`는 `실행할일`, `동작받이`, `Ação_aviso`, `botão`, `Evento_Fila`,
`tarefaSegundoPlano`, `iniciar()`을 사용할 número 있다. Português GUI/가닥을 nativo JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. cadeia_VALOR 등 javac의 표준
계약과 전체 fonte_árvore 검토 범위는 [명명 LEIAME_eb81d7d9](명명/LEIAME_eb81d7d9.md), 사용법과 호환성 변경은
[Português Java API](한국어자바/LEIAME_eb81d7d9.md)를 본다.

terminal mover_VALOR·Tamanho 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[tela renovar 설명](자바실행환경.md#terminal-부분-renovar),
[부분 renovar 검사](build/verification/redraw/report.json)를 참고한다.
