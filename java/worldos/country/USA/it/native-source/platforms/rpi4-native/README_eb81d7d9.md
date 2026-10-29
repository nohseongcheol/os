# Raspberry Pi 4 nativo Java kernel_VALORE — spazio_utente Esegui_comando 기반

Regolari_articolo nativo 코드의 COSL 상업 condizione, 제3자 고지 및 LGPL 재연결 자료는 [COSL distribuzione_VALORE README_eb81d7d9](COSL배포안내.md)를 참고한다. SWITCH_MODA 전 GPL 구성의 판단은 [Indietro_articolo 라이선스 검토](licenza_rivedere.md)에 기록했다.

Italiano comunicazione·eccezione 사용법은 [Italiano Java API](한국어자바/README_eb81d7d9.md), FUNZIONE_VALORE·variabile_VALORE·file 이름의 변경과 어원 근거는 [명명 README_eb81d7d9](명명/README_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 nativo AArch64 커널이다. Java AOT kernel_VALORE 위에 **riga_di_comando Shell, 게스트 Java compilatore·JVM, MicroPython, EL0 C++ Esegui_comando, file·UDP 루프백 시스템 호출, 여러 한글 GUI terminale·vi Editor·Swing 부분집합**을 제공한다. 커널의 file dati/정책·루프백 trasferire_VALORE·Shell 상태는 Java, schermata 합성·pixel cambiare_VALORE·puntatore·클리핑도 Java로 구현하며, CPU/MMU/cellulare_VALORE 경계와 terminale·carattere_VALORE Paint_schermata 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 nativo 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 Esegui_comando, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, fisico_hardware Pi4의 cablato_VALORE 송수신은 아직 미검증이다.** Esegui_comando·connessione_e05f319b·password_VALORE 확인은 [esterno_VALORE connessione_e05f319b README_eb81d7d9](esterno_connessione_guida.md)에 정리했다.

셸은 EL1 kernel_VALORE, `java` 등 spazio_utente Esegui_comando 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 Esegui_comando·connessione_e05f319b 방법 및 effettivo_dati 검증은
[Esegui_comando 계층과 esterno_VALORE comunicazione 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 effettivo_dati Esegui_comando 형식으로 검사한다. `./messaggio_di_saluto_ae353e94`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statico_VALORE ELF는 `run --linux nome_file_SMS`으로 실행한다. [ELF·Linux ABI Supporto_VALORE 범위와 동일 바이너리 prove](eseguibile_ABI.md).

GUI와 네트워크는 `python3 strumenti/Esegui_comando.py --desktop --network`로 함께 사용한다. Java·C·Python의 Italiano 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 avvio_macchina 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 numero 있다. Remmina에서 **F9/Shift+Space/한·zero_operando tasto_VALORE**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·effettivo_dati TCP/UDP·file byte_VALORE·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java EsempioFinestra`로 Italiano Swing 예제를 실행한다. terminale 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 Regolari_articolo colonna_VALORE·riga_VALORE 수를 보여 준다.

## Regolari_articolo Supporto_VALORE ritagliare

| 기능 | implementazione·시험한 ritagliare | 아직 미지원 |
|---|---|---|
| avvio_macchina | Pi4 AArch64 EL1, UART, SD용 BLD_foto, QEMU raspi4b avvio_macchina | effettivo_dati Pi4 보드에서의 펌웨어 avvio_macchina prove |
| Java kernel_VALORE | statico_VALORE Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java oggetto_VALORE/eccezione/GC/JVM/표준 Catalogo |
| Java sviluppo strumenti | 게스트 nativo `javac`/`java`, JVM 0.4/JAR: 다중 Corso_VALORE·oggetto_VALORE·상속·eccezione·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Italiano Catalogo. 게스트 컴파일러는 statico_VALORE Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | effettivo_dati MicroPython 1.24.1 EL0 이식, fonte_albero compilare_fonte/Esegui_comando, Corso_VALORE·eccezione·GC·큰 intero·Unicode·file·UDP/schermata Connetti | CPython, pip, C estensione_VALORE, 부동소수점, 일반 OS/스레드/socket_VALORE modulo_VALORE, interattivo REPL |
| Shell | UTF-8 Modifica_VALORE·LOG_riga·Completate_VALORE, 디렉터리·file comando, variabile_VALORE·condizione·script_VALORE, 16 KiB 순차 파이프·리다이렉션, ELF Esegui_comando | 전체 POSIX sh/Bash, 작업 controllo_VALORE·동시 프로세스·PTY |
| C/AOT compilare_fonte | 게스트 TinyCC 및 statico_VALORE Java 부분집합 `jaot` → nativo ARM64 ELF | 전체 libc·모든 Java Corso_VALORE AOT |
| C++ | 독립 ELF64를 EL0에서 Esegui_comando; statico_VALORE 생성자, RAII 소멸자, FP/SIMD, Italiano file/루프백 호출 | libc/libstdc++, STL, C++ eccezione·RTTI·동적 Connetti |
| spazio_utente proteggere_VALORE | 4 KiB 페이지, CODICE_VALORE RX/dati RW·NX, kernel_VALORE·MMIO 차단, guard page, 잘못된 puntatore 검사 | 다중 spazio_utente privilegio_VALORE, 일반 프로세스/스레드 스케줄러 |
| Esegui_comando valore 제한 | GIC-400 타이머로 무한 sprint_VALORE Esci_app; interattivo input_VALORE 대기는 기한 aggiornare, 터미널별 EL0 app_f5044b9b 중단·CV_esecuzione | 일반적인 선점형 다중작업. 긴 kernel_VALORE 호출 도중에는 종료가 지연될 numero 있음 |
| file | Java RAM file 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, peer_VALORE/절대 percorso 63바이트, descrittore_voce 16개 | privilegio_VALORE, 디스크/SD 영속 Store_VALORE |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP implementazione, 게스트 FTP·SSH·VNC | GENET fisico_hardware convalidare, Wi-Fi, DNS, 일반 TLS socket_VALORE, RDP |
| GUI | 최대 네 terminale Finestra, selezione_VALORE·spostare_VALORE·X Chiudi, 한글 tipo_di_carattere_VALORE, Swing 부분집합; 게스트 VNC schermata·input_VALORE·두벌식 | fisico_hardware USB input_VALORE, 전체 AWT/Swing·Java2D·Finestra 관리 정책 |
| 작업 thread_VALORE | kernel_VALORE 작업 2개와 주 작업; JVM 내부 thread_VALORE 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 nome_file_SMS/datagramma | GUI의 일반 다국어 조판 |

Esegui_comando 버튼 화면은 5×7 영문 글꼴을 쓰며, terminale 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 effettivo_dati 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 kernel_VALORE 내부의 datagramma 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 strumenti/Esegui_comando.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·Esegui_comando 제한과 Italiano 사용법은 [nativo JVM과 Italiano Catalogo](자바실행환경.md)에 정리했다. Corso_VALORE file/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `Italiano.자바`와 별도인 `Italiano.nativo` 패키지다.

**vi·여러 Finestra·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 sviluppo 매뉴얼](sviluppo_guida.md)에 정리했다.**

GUI terminale Esegui_comando·단축키·Shell comando·제한은 [셸과 terminale 사용법](Shell_E_Terminale.md)에 정리했다.

## Regolari_articolo 컴퓨터에서 Esegui_comando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

Esci_app: **Ctrl+A Avanti_articolo X**. 게스트 C/AOT strumenti 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc aritmetico_VALORE 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. host 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. compilatore 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/percorso/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` Supporto_VALORE 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 Esegui_comando**한다. 기존 한 carattere_VALORE 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 argomenti 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| comando | Azione |
|---|---|
| `help` / `info` | comando·effettivo_dati implementazione Stato_VALORE |
| `ls` / `cat FILE` / `rm FILE` | RAM file voce_elenco·Contenuto_VALORE·삭제 |
| `vi FILE` | spazio_utente area_VALORE vi 부분집합, 한글 Modifica_VALORE·Store_VALORE·검색·되돌리기 |
| `edit FILE` | file 전체를 새로 input_VALORE; 단독 `.` 줄로 Store_VALORE, Ctrl-C로 Chiudi_operazione |
| `javac FILE.java` / `java CLASS [ARGS]` | nativo 제한형 Java compilare_fonte·Esegui_comando |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython compilare_fonte·Esegui_comando |
| `load FILE` / `hex FILE` | 16진수 바이너리 input_VALORE/uscitaTesto; 입력은 단독 `.` 줄로 Store_VALORE |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 nativo ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 proteggere_VALORE prove |
| `gui` / `terminal` | Esegui_comando schermata / 한글 GUI terminale; F12로 terminale Apri·Chiudi |
| `samples` | 삭제한 valore_predefinito 예제 recuperare_Stato; 기존 파일은 보존 |

예를 들어 `edit messaggio_di_saluto_ae353e94.java`를 입력한 Avanti_articolo 아래 소스를 입력한다.

```java
public class messaggio_di_saluto_ae353e94 { public static void main(String[] args) { int VALORE = 7; System.out.println("한글=" + VALORE); } }
```

그다음 단독 `.` 줄로 저장하고 `javac messaggio_di_saluto_ae353e94.java`, `java messaggio_di_saluto_ae353e94`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Chiudi_operazione·잘못된 16진수·capacità_VALORE 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, Esegui_comando 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 comando 인수는 최대 32개다. offerta·백슬래시·Shell variabile_VALORE·파이프·리다이렉션 범위는 [Shell 설명](Shell_E_Terminale.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, e_mail **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode input_VALORE·명시적 incollare_VALORE·Esegui_comando 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 strumenti/Esegui_comando.py --desktop --network
# 다른 hardware_porta: python3 strumenti/Esegui_comando.py --desktop --port 5903
```

종료는 실행한 host 터미널에서 Ctrl+C다. 기존 `python3 strumenti/Esegui_comando.py --vnc 127.0.0.1:2`는 schermata 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. effettivo_dati Pi4 USB 입력기는 아직 없으며, VNC Connetti 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 effettivo_dati C++/UDP ELF Esegui_comando, `Hello.java` compilare_fonte 후 JVM Esegui_comando, `hello.py` Esegui_comando, GUI terminale 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interattivo 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Memoria_dati·CPU 문맥을 보관한다. Shell·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## effettivo_dati 산출물과 Pi4 SD BLD_foto

```sh
make image   # kernel_VALORE, SD BLD_foto, avvio_macchina ZIP, 사용자용 SDK
make sdk     # SDK만 retry_VALORE generare
```

| percorso | 용도 |
|---|---|
| `build/kernel8.img` | nativo kernel_VALORE 기계어, 적재 e_mail 0x80000 |
| `build/kernel.elf`, `kernel.map` | kernel_VALORE simbolo_VALORE·disposizione_di_collegamento |
| `build/user/demo.elf` | spazio_utente MODA_VALORE C++ file/heap_VALORE/virgola_mobile_VALORE/그래픽 예제 |
| `build/user/network.elf` | spazio_utente MODA_VALORE C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | nativo Java 부분집합 compilatore/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | host javac용 Italiano API Corso_VALORE; 같은 클래스가 nativo JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Italiano API Java codiceSorgente |
| `build/user/vi.elf` | nativo UTF-8 vi comando 부분집합 Editor |
| `build/user/python.elf` | nativo ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 proteggere_VALORE prove 전용 |
| `build/libposix-kor-arm64.a` | **kernel_VALORE 내부**에서 Java file 구현을 직접 부르는 기존 Connetti |
| `build/libposix-kor-user.a` | **EL0 spazio_utente app_f5044b9b**에서 SVC로 file/루프백을 호출하는 새 Connetti |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD BLD_foto |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 avvio_macchina 파티션에 복사할 file gruppo_VALORE |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·avvia CODICE_VALORE·Catalogo·링커 script_VALORE·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 effettivo_dati Supporto_VALORE Stato_VALORE |

이미지는 확인된 공식 Pi avvio_macchina 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·terminale tipo_di_carattere_VALORE 라이선스와 tipo_di_carattere_VALORE origine_VALORE 해시도 동봉한다. file generare 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 BLD_foto LOG_riga 도구로 `.img`를 기록하거나 FAT32 avvio_macchina 파티션 최상위에 ZIP 내용을 푼다. BLD_foto 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 valore_predefinito EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**fisico_hardware Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD file 구성·kernel_VALORE 체크섬 검사와 물리 scheda avvio_macchina 검증은 별개다. MMU usare_VALORE 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 avvio_macchina 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 Italiano API usare_VALORE

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/EsempioFile.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int START_USER_app(int)`이다. spazio_utente C++는 FP/SIMD를 사용할 numero 있다. kernel_VALORE C/Java AOT는 일반 레지스터만 사용하므로 eccezione Processi_VALORE_voce 중 spazio_utente FP 상태를 건드리지 않는다. spazio_utente punto_di_ingresso_VALORE 시 FP 상태를 초기화하고 kernel_VALORE 복귀에 필요한 상태를 보존한다.

```cpp
#include "File_ABI.h"
extern "C" int START_USER_app(int) {
    int file = aperto_File("messaggio_di_saluto_ae353e94.txt", in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600);
    if (file < 0) return 1;
    const char Contenuto_VALORE[] = "안녕하세요";
    int risultato = scrivere_File_dati(file, Contenuto_VALORE, sizeof(Contenuto_VALORE) - 1);
    Chiudi_File(file);
    return risultato == sizeof(Contenuto_VALORE) - 1 ? 0 : 2;
}
```

[file 예제](spazio_utente/EsempioFile.cpp)와 [comunicazione 예제](spazio_utente/통신예제.cpp)가 effettivo_dati avvio_macchina prove 대상이다. `File_ABI.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 file Processi_VALORE_voce 및 루프백 전달은 Java 커널에서 실행한다. `rete_ABI.h`의 socket_VALORE 함수는 Regolari_articolo 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kernel_VALORE 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Avanti_articolo 도구를 사용하면 **새 QEMU를 부팅해 업로드한 effettivo_dati 바이트를 재확인한 BACK_VALORE 게스트에서 Esegui_comando**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 strumenti/Esegui_File.py build/jkoros-native-sdk/demo.elf
python3 strumenti/Esegui_File.py 예제/Hello.java "한글 argomenti"
python3 strumenti/Esegui_File.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kernel_VALORE 묶음에 포함되어 이 file 한도를 적용받지 않는다. **C++ 컴파일러는 host SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 Catalogo, PT_TLS, PT_INTERP, PT_DYNAMIC, Esegui_comando·Scrittura 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDICE·e_mail ritagliare·오류는 [spazio_utente ABI](USER_Chiama_ABI.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `commit_File`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 privilegio_VALORE·dup/fcntl은 없다. 디렉터리와 peer_VALORE/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, ricevere_VALORE 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. spazio_utente Esci_app 시 열린 file 서술자와 소켓을 회수한다.

## convalidare risultato

`make test-jvm`은 9개 프로그램을 OpenJDK와 effettivo_dati nativo 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `strumenti/부팅시험.py`는 Java rettangolo API의 effettivo_dati schermata 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 effettivo_dati VNC input_VALORE·한글 terminale 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT operazione_VALORE risultato 비교, 런타임 errore 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kernel_VALORE 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/e_mail 초과/겹친 페이지/W+X 등 ELF rifiutare_VALORE 사례 22개.
- EL0 C++ 생성자·RAII·virgola_mobile_VALORE operazione_VALORE·file·heap_VALORE 및 잘못된 시스템 호출 puntatore.
- kernel_VALORE/CODICE_VALORE/MMIO Scrittura·accesso_voce, NX operando_Pila·NULL Esegui_comando, guard page, 특권 comando 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 reparto_IT_normale app_f5044b9b 재실행.
- sprint_VALORE Esegui_comando 시 file/socket_VALORE 누수 방지, UDP 왕복·보낸 e_mail·잘린 ricevere_VALORE·큐 포화·빈 datagramma·미지원 comunicazione errore.
- Shell Modifica_VALORE·Chiudi_operazione·16진수 업로드/다운로드·spazio_utente ELF 실행과 잘못된 ELF rifiutare_VALORE.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 Esegui_comando, 한글 Corso_VALORE·variabile_VALORE·nome_file_SMS.
- 여러 Finestra·vi Store_VALORE·Modifica_VALORE·Reso_bridge·spazio_utente Stato_VALORE 중단/CV_esecuzione, Swing 한글 input_VALORE·이벤트·X Chiudi, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 intero·Corso_VALORE·GC sprint_VALORE·file import·eccezione·file·UDP 왕복·valore 초과 후 복귀.
- GUI selezione_VALORE spostare_VALORE, C++/UDP/Java/MicroPython 버튼 Esegui_comando, 콘솔 복귀 및 effettivo_dati 프레임버퍼 픽셀/tipo_di_carattere_VALORE.
- 디렉터리·variabile_VALORE·condizione·file comando·script_VALORE·순차 파이프·리다이렉션·capacità_VALORE 초과 recuperare_Stato, Python stdin/EOF와 Java/Python stdout.
- comando LOG_riga·긴 한글 input_VALORE Modifica_VALORE·Completate_VALORE·terminale 스크롤, 그래픽 app_f5044b9b Esci_app 후 Finestra 복원, effettivo_dati VNC Unicode tasto_VALORE·incollare_VALORE·마우스.

[kernel_VALORE prove LOG_riga](build/verification/implementation-test.log), [Shell prove](build/verification/shell/report.json), [VNC prove](build/verification/desktop/report.json), [computer 판독 risultato](build/verification/report.json), [seriale_VALORE LOG_VALORE](build/verification/serial.log), [GUI schermata](build/verification/gui-python.png)을 확인할 numero 있다. VNC RFB 3.8 Connetti 및 640×480 schermata 정보도 검사한다. [SDK 재컴파일 risultato](build/verification/sdk.json)는 두 예제의 punto_di_ingresso·적재 세그먼트·ABI note가 avvio_macchina 시험한 ELF와 일치함을 확인한다. simbolo_VALORE 등 비적재 메타데이터를 포함한 file 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 ritagliare

nativo `javac`는 버전 49 `.class`를 생성하며 JVM은 Supporto_VALORE 명령으로 구성된 버전 45–52 클래스를 실행한다. statico_VALORE FUNZIONE_VALORE·재귀·int/boolean/char/String·condizione/sprint_VALORE·stringa_VALORE 결합과 일부 file 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/composizione_VALORE 자모 식별자를 처리한다. Unicode identificatore_VALORE 전체 tabella_di_ricerca·Unicode fonte_albero 이스케이프는 구현하지 않았다. 게스트 fonte_albero 컴파일러는 일반 oggetto_VALORE·eccezione·Thread 구문을 아직 컴파일하지 못한다. host `javac --release 8`로 만든 Supporto_VALORE 부분집합 클래스는 nativo JVM 0.4의 oggetto_VALORE·eccezione·Thread·UDP와 Italiano API를 사용할 numero 있다. Swing은 문서화한 nativo API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [nativo JVM 설명](자바실행환경.md)이 기준이다. 상세 Lingua 범위는 [공유 Java strumenti 설명](../../Guides/ambiente_IDE_Java.md)을 참고하되, 그 문서의 x86 Shell/Store_VALORE/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 fonte_albero**를 nativo AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 FUNZIONE_VALORE·Corso_VALORE·eccezione·리스트/dizionario·Unicode·GC·가변 precisione_VALORE 정수를 제공한다. Regolari_articolo 구성은 intero 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 Catalogo, pip, subprocess, threading, 일반 socket과 valore_predefinito `open()` file 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 oggetto_VALORE·모듈은 Esci_app 시 회수되고 RAM 파일만 Avanti_articolo 실행에 남는다.

`import jkoros`로 Avanti_articolo 시스템 연결을 쓴다. 모두 SVC를 통해 nativo Java 커널에 접근한다.

| FUNZIONE_VALORE | Azione |
|---|---|
| `stdin(limit)` | Regolari_articolo 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART dati 없음은 OSError(11) |
| `read(name)` | peer_VALORE/절대 RAM 경로의 file 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_VALORE, 쓴 byte_VALORE numero Reso_KR |
| `remove(name)` | RAM file 삭제 |
| `rect(x, y, w, h, color)` | 선택한 effettivo_dati schermata Dimensione 안의 rettangolo disegno_VALORE; 기존 보드의 RGB32 VALORE |
| `ticks_ms()` | avvio_macchina 후 밀리초, 32비트 Cicli_VALORE |
| `udp_open(port)` | 127.0.0.1의 UDP socket_VALORE Apri/BIND_endpoint; 0은 자동 hardware_porta |
| `udp_send(fd, port, data)` | 루프백 meta_VALORE 포트에 str/bytes 버퍼 trasferire_VALORE |
| `udp_recv(fd)` | `(bytes, 보낸포트)` Reso_KR; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | socket_VALORE Chiudi |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 CODICE_VALORE: [python/](PYTHON_bridge/), [spazio_utente Java Connetti](spazio_utente/자바연결.c). 공식 [MicroPython 이식 README_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. fonte_albero URL·hash_File·라이선스는 [vendor README_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Avanti_articolo area_VALORE_29ee1bb7 | 완료 azione_radice |
|---|---|
| 영속 Store_VALORE·Esegui_comando file input_VALORE | SD/MMC 및 디스크 file 시스템, 시스템/spazio_utente 볼륨; Regolari_articolo ELF file 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 e_mail e_mail_area, 선점 스케줄러, TLS, sincronizzare/aspetta_VALORE, 신호, mmap/mprotect |
| libc와 C++ 런타임 | nativo ABI용 libc, malloc/free, 표준 I_O·clock·ambiente·locale, libstdc++/eccezione Processi_VALORE_voce convalidare |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 file/Unicode/스레드/socket_VALORE prove |
| OpenJDK/JRE | HotSpot OS layer_VALORE, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 Catalogo 이식; javac/java effettivo_dati Esegui_comando |
| esterno_VALORE 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 effettivo_dati scheda 송수신 convalidare, DNS·Wi-Fi |
| GUI estensione_VALORE | USB HID, 게스트 입력기·문자 조판, Swing Finestra Dimensione 조절·클리핑 estensione_VALORE, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 implementazione 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 esterno_VALORE 네트워크 드라이버는 fisico_hardware 검증도 필요하다. [QEMU cellulare_VALORE 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

hardware_VALORE 및 ABI 참고: [BCM2711 accessorio](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC e_mail](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox valore_di_contratto](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP controllo_VALORE 레지스터 definizione_VALORE](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Italiano C tipo_di_dati·Python errore·aggregare installare_VALORE

C 네트워크 API는 `struct cloud_socket_e_mail`, enum 상수와 effettivo_dati Italiano 함수로
구현한다. macro_VALORE 별칭을 사용하지 않으며 Indietro_articolo pk_* ABI도 유지한다.
Python 예제는 `errore_di_sistema`, `errore.INDICE`, `errore.설명`을 사용한다.

`python3 strumenti/Esegui_comando.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 numero 있다. 현재는 host 중계를
이용하는 제한형 MicroPython fonte_albero 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_aggregare.md).

## schermata Dimensione selezione_VALORE

`python3 strumenti/Esegui_comando.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. terminale spostare_VALORE, Swing 가운데 disposizione_di_collegamento, Java·C·Python 그리기도 effettivo_dati 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Impostazioni·Italiano API·convalidare README_eb81d7d9](risoluzione_dello_schermo.md).

## Italiano 직접 API와 schermata aggiornare

`example/java`는 `실행할일`, `동작받이`, `Action_informativa`, `pulsante`, `evento_coda`,
`esecutoreAsincrono`, `avvia()`을 사용할 numero 있다. Italiano GUI/가닥을 nativo JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. stringa_VALORE 등 javac의 표준
계약과 전체 fonte_albero 검토 범위는 [명명 README_eb81d7d9](명명/README_eb81d7d9.md), 사용법과 호환성 변경은
[Italiano Java API](한국어자바/README_eb81d7d9.md)를 본다.

terminale spostare_VALORE·Dimensione 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[schermata aggiornare 설명](자바실행환경.md#terminale-부분-aggiornare),
[부분 aggiornare 검사](build/verification/redraw/report.json)를 참고한다.
