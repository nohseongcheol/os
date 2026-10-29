# Raspberry Pi 4 Eigen Java kernel_WAARDE — gebruikersruimte Uitvoeren_opdracht 기반

actueel_item Eigen 코드의 COSL 상업 toestand, 제3자 고지 및 LGPL 재연결 자료는 [COSL distributie_WAARDE LEESMIJ_eb81d7d9](COSL배포안내.md)를 참고한다. switch_MODUS 전 GPL 구성의 판단은 [Vorige_item 라이선스 검토](licentie_beoordeling.md)에 기록했다.

Nederlands communicatie·uitzondering 사용법은 [Nederlands Java API](한국어자바/LEESMIJ_eb81d7d9.md), FUNCTIE_WAARDE·variabele_WAARDE·bestand 이름의 변경과 어원 근거는 [명명 LEESMIJ_eb81d7d9](명명/LEESMIJ_eb81d7d9.md)를 참고한다.

Linux 없이 부팅하는 Eigen AArch64 커널이다. Java AOT kernel_WAARDE 위에 **opdrachtregel Shell, 게스트 Java compiler·JVM, MicroPython, EL0 C++ Uitvoeren_opdracht, bestand·UDP 루프백 시스템 호출, 여러 한글 GUI terminal·vi Editor·Swing 부분집합**을 제공한다. 커널의 bestand gegevens/정책·루프백 transfer_WAARDE·Shell 상태는 Java, scherm 합성·pixel wijzigen_WAARDE·wijzer·클리핑도 Java로 구현하며, CPU/MMU/mobiel_WAARDE 경계와 terminal·teken_WAARDE Paint_scherm 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 Eigen 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 Uitvoeren_opdracht, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](파일전송과번역.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, 실물 Pi4의 bekabeld_WAARDE 송수신은 아직 미검증이다.** Uitvoeren_opdracht·verbinding_e05f319b·wachtwoord_WAARDE 확인은 [extern_WAARDE verbinding_e05f319b LEESMIJ_eb81d7d9](extern_verbinding_guide.md)에 정리했다.

셸은 EL1 kernel_WAARDE, `java` 등 gebruikersruimte Uitvoeren_opdracht 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 제한, QEMU 네트워크 Uitvoeren_opdracht·verbinding_e05f319b 방법 및 werkelijk_gegevens 검증은
[Uitvoeren_opdracht 계층과 extern_WAARDE communicatie 점검](실행계층과외부통신점검.md)을 참고한다.

ELF는 확장자가 아닌 werkelijk_gegevens Uitvoeren_opdracht 형식으로 검사한다. `./인사`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statisch_WAARDE ELF는 `run --linux bestandsnaam_sms`으로 실행한다. [ELF·Linux ABI steun_WAARDE 범위와 동일 바이너리 tests](실행파일규약.md).

GUI와 네트워크는 `python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --network`로 함께 사용한다. Java·C·Python의 Nederlands 예제 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 machineopstart 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 nummer 있다. Remmina에서 **F9/Shift+Space/한·nul_operand toets_WAARDE**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·werkelijk_gegevens TCP/UDP·bestand byte_WAARDE·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` 후 `java Venstervoorbeeld`로 Nederlands Swing 예제를 실행한다. terminal 모서리에 마우스를 대고 **왼쪽 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 actueel_item KOLOM_WAARDE·RIJ_WAARDE 수를 보여 준다.

## actueel_item steun_WAARDE clip

| 기능 | implementatie·시험한 clip | 아직 미지원 |
|---|---|---|
| machineopstart | Pi4 AArch64 EL1, UART, SD용 build_kopie, QEMU raspi4b machineopstart | werkelijk_gegevens Pi4 보드에서의 펌웨어 machineopstart tests |
| Java kernel_WAARDE | statisch_WAARDE Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java object_WAARDE/uitzondering/GC/JVM/표준 bibliotheek |
| Java ontwikkeling hulpmiddelen | 게스트 Eigen `javac`/`java`, JVM 0.4/JAR: 다중 les_WAARDE·object_WAARDE·상속·uitzondering·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Nederlands bibliotheek. 게스트 컴파일러는 statisch_WAARDE Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | werkelijk_gegevens MicroPython 1.24.1 EL0 이식, bron_structuur compileren_bron/Uitvoeren_opdracht, les_WAARDE·uitzondering·GC·큰 geheel_getal·Unicode·bestand·UDP/scherm Verbinden | CPython, pip, C extensie_WAARDE, 부동소수점, 일반 OS/스레드/socket_WAARDE module_WAARDE, interactief REPL |
| Shell | UTF-8 Bewerk_WAARDE·LOG_RECORD·Voltooid_WAARDE, 디렉터리·bestand opdracht, variabele_WAARDE·toestand·script_WAARDE, 16 KiB 순차 파이프·리다이렉션, ELF Uitvoeren_opdracht | 전체 POSIX sh/Bash, 작업 controle_WAARDE·동시 프로세스·PTY |
| C/AOT compileren_bron | 게스트 TinyCC 및 statisch_WAARDE Java 부분집합 `jaot` → Eigen ARM64 ELF | 전체 libc·모든 Java les_WAARDE AOT |
| C++ | 독립 ELF64를 EL0에서 Uitvoeren_opdracht; statisch_WAARDE 생성자, RAII 소멸자, FP/SIMD, Nederlands bestand/루프백 호출 | libc/libstdc++, STL, C++ uitzondering·RTTI·동적 Verbinden |
| gebruikersruimte beschermen_WAARDE | 4 KiB 페이지, CODE_WAARDE RX/gegevens RW·NX, kernel_WAARDE·MMIO 차단, guard page, 잘못된 wijzer 검사 | 다중 gebruikersruimte machtiging_WAARDE, 일반 프로세스/스레드 스케줄러 |
| Uitvoeren_opdracht TIJD_WAARDE 제한 | GIC-400 타이머로 무한 sprint_WAARDE Einde_app; interactief invoer_WAARDE 대기는 기한 vernieuwen, 터미널별 EL0 app_f5044b9b 중단·cv_uitvoerbewerking | 일반적인 선점형 다중작업. 긴 kernel_WAARDE 호출 도중에는 종료가 지연될 nummer 있음 |
| bestand | Java RAM bestand 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, peer_WAARDE/절대 pad 63바이트, 서술자 16개 | machtiging_WAARDE, 디스크/SD 영속 Store_WAARDE |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP implementatie, 게스트 FTP·SSH·VNC | GENET 실물 valideren, Wi-Fi, DNS, 일반 TLS socket_WAARDE, RDP |
| GUI | 최대 네 terminal Venster, selectie_WAARDE·verplaatsen_WAARDE_83b651b8·X Sluiten, 한글 lettertype_WAARDE, Swing 부분집합; 게스트 VNC scherm·invoer_WAARDE·두벌식 | 실물 USB invoer_WAARDE, 전체 AWT/Swing·Java2D·Venster 관리 정책 |
| 작업 thread_WAARDE | kernel_WAARDE 작업 2개와 주 작업; JVM 내부 thread_WAARDE 최대 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, 한글·일본어·아랍어·이모지, UTF-8 bestandsnaam_sms/datagram | GUI의 일반 다국어 조판 |

Uitvoeren_opdracht 버튼 화면은 5×7 영문 글꼴을 쓰며, terminal 창은 Noto CJK/DejaVu에서 생성한 한글·Unicode 비트맵 글꼴을 쓴다. UART와 werkelijk_gegevens 프레임버퍼의 한글 표시를 시험한다. 루프백은 동일 kernel_WAARDE 내부의 datagram 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 보조 UART SLIP 경로를 사용한다. `python3 hulpmiddelen/Uitvoeren_opdracht.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·Uitvoeren_opdracht 제한과 Nederlands 사용법은 [Eigen JVM과 Nederlands bibliotheek](자바실행환경.md)에 정리했다. les_WAARDE bestand/JAR 배포는 [한국어자바](한국어자바) 소스에서 재현한다. 기존 Linux판 `Nederlands.자바`와 별도인 `Nederlands.Eigen` 패키지다.

**vi·여러 Venster·Swing·한글 Java/Python/C/C++·posix-kor 예제는 [한글 ontwikkeling 매뉴얼](ontwikkeling_guide.md)에 정리했다.**

GUI terminal Uitvoeren_opdracht·단축키·Shell opdracht·제한은 [셸과 terminal 사용법](Shell_EN_Terminal.md)에 정리했다.

## actueel_item 컴퓨터에서 Uitvoeren_opdracht

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

Einde_app: **Ctrl+A Volgende_item X**. 게스트 C/AOT hulpmiddelen 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc 산술 보조 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. host 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 이식·링크한 것은 아니다. compiler 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/pad/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` steun_WAARDE 여부를 확인한 후 실행한다.

명령은 **Enter를 눌러 Uitvoeren_opdracht**한다. 기존 한 teken_WAARDE 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "한글 argumenten 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| opdracht | Actie |
|---|---|
| `help` / `info` | opdracht·werkelijk_gegevens implementatie Status_WAARDE |
| `ls` / `cat FILE` / `rm FILE` | RAM bestand invoer_Lijst_f07b3200·Inhoud_WAARDE·삭제 |
| `vi FILE` | gebruikersruimte regio_WAARDE vi 부분집합, 한글 Bewerk_WAARDE·Store_WAARDE·검색·되돌리기 |
| `edit FILE` | bestand 전체를 새로 invoer_WAARDE; 단독 `.` 줄로 Store_WAARDE, Ctrl-C로 Annuleren_operatie |
| `javac FILE.java` / `java CLASS [ARGS]` | Eigen 제한형 Java compileren_bron·Uitvoeren_opdracht |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython compileren_bron·Uitvoeren_opdracht |
| `load FILE` / `hex FILE` | 16진수 바이너리 invoer_WAARDE/tekstuitvoer; 입력은 단독 `.` 줄로 Store_WAARDE |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 Eigen ABI ELF / 내장 C++ 예제 |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 작업 / EL0 beschermen_WAARDE tests |
| `gui` / `terminal` | Uitvoeren_opdracht scherm / 한글 GUI terminal; F12로 terminal Openen·Sluiten |
| `samples` | 삭제한 standaardwaarde 예제 herstellen_Status; 기존 파일은 보존 |

예를 들어 `edit 인사.java`를 입력한 Volgende_item 아래 소스를 입력한다.

```java
public class 인사 { public static void main(String[] args) { int WAARDE = 7; System.out.println("한글=" + WAARDE); } }
```

그다음 단독 `.` 줄로 저장하고 `javac 인사.java`, `java 인사`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. Annuleren_operatie·잘못된 16진수·capaciteit_WAARDE 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, Uitvoeren_opdracht 인수는 최대 8개·각각 UTF-8 255바이트다. 일반 opdracht 인수는 최대 32개다. Citaat·백슬래시·Shell variabele_WAARDE·파이프·리다이렉션 범위는 [Shell 설명](Shell_EN_Terminal.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, ADRES **127.0.0.1:5902**로 연결한다. 키보드·한글 Unicode invoer_WAARDE·명시적 plakken_WAARDE·Uitvoeren_opdracht 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --network
# 다른 hardware_poort: python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --port 5903
```

종료는 실행한 host 터미널에서 Ctrl+C다. 기존 `python3 hulpmiddelen/Uitvoeren_opdracht.py --vnc 127.0.0.1:2`는 scherm 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. werkelijk_gegevens Pi4 USB 입력기는 아직 없으며, VNC Verbinden 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 werkelijk_gegevens C++/UDP ELF Uitvoeren_opdracht, `Hello.java` compileren_bron 후 JVM Uitvoeren_opdracht, `hello.py` Uitvoeren_opdracht, GUI terminal 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interactief 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 Geheugen_gegevens·CPU 문맥을 보관한다. Shell·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## werkelijk_gegevens 산출물과 Pi4 SD build_kopie

```sh
make image   # kernel_WAARDE, SD build_kopie, machineopstart ZIP, 사용자용 SDK
make sdk     # SDK만 opnieuw_proberen_WAARDE genereren
```

| pad | 용도 |
|---|---|
| `build/kernel8.img` | Eigen kernel_WAARDE 기계어, 적재 ADRES 0x80000 |
| `build/kernel.elf`, `kernel.map` | kernel_WAARDE symbool_WAARDE·koppelindeling |
| `build/user/demo.elf` | gebruikersruimte MODUS_WAARDE C++ bestand/heap_WAARDE/drijvende_komma_WAARDE/그래픽 예제 |
| `build/user/network.elf` | gebruikersruimte MODUS_WAARDE C++ UDP 루프백 예제 |
| `build/user/java-tools.elf` | Eigen Java 부분집합 compiler/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | host javac용 Nederlands API les_WAARDE; 같은 클래스가 Eigen JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Nederlands API Java broncode |
| `build/user/vi.elf` | Eigen UTF-8 vi opdracht 부분집합 Editor |
| `build/user/python.elf` | Eigen ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 beschermen_WAARDE tests 전용 |
| `build/libposix-kor-arm64.a` | **kernel_WAARDE 내부**에서 Java bestand 구현을 직접 부르는 기존 Verbinden |
| `build/libposix-kor-user.a` | **EL0 gebruikersruimte app_f5044b9b**에서 SVC로 bestand/루프백을 호출하는 새 Verbinden |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD build_kopie |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 machineopstart 파티션에 복사할 bestand Groep_WAARDE |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·starten CODE_WAARDE·bibliotheek·링커 script_WAARDE·예제 |
| `dist/manifest.json`, `build/build.json` | SHA256과 werkelijk_gegevens steun_WAARDE Status_WAARDE |

이미지는 확인된 공식 Pi machineopstart 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·terminal lettertype_WAARDE 라이선스와 lettertype_WAARDE oorsprong_WAARDE 해시도 동봉한다. bestand genereren 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 build_kopie LOG_RECORD 도구로 `.img`를 기록하거나 FAT32 machineopstart 파티션 최상위에 ZIP 내용을 푼다. build_kopie 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 standaardwaarde EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**실물 Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD bestand 구성·kernel_WAARDE 체크섬 검사와 물리 Bord machineopstart 검증은 별개다. MMU gebruik_WAARDE 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 machineopstart 조건을 전제로 한다. 세 보조 코어는 대기시키며 한 코어만 사용한다.

## C++와 Nederlands API gebruik_WAARDE

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/Bestandsvoorbeeld.cpp -o demo.elf
python3 compile.py examples/통신예제.cpp -o network.elf
```

진입점은 `extern "C" int START_gebruiker_app(int)`이다. gebruikersruimte C++는 FP/SIMD를 사용할 nummer 있다. kernel_WAARDE C/Java AOT는 일반 레지스터만 사용하므로 uitzondering Proces_WAARDE_invoer 중 gebruikersruimte FP 상태를 건드리지 않는다. gebruikersruimte beginpunt_WAARDE 시 FP 상태를 초기화하고 kernel_WAARDE 복귀에 필요한 상태를 보존한다.

```cpp
#include "파일규약.h"
extern "C" int START_gebruiker_app(int) {
    int bestand = open_Bestand("인사.txt", lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600);
    if (bestand < 0) return 1;
    const char Inhoud_WAARDE[] = "안녕하세요";
    int resultaat = schrijven_Bestand_gegevens(bestand, Inhoud_WAARDE, sizeof(Inhoud_WAARDE) - 1);
    Sluiten_Bestand(bestand);
    return resultaat == sizeof(Inhoud_WAARDE) - 1 ? 0 : 2;
}
```

[bestand 예제](gebruikersruimte/Bestandsvoorbeeld.cpp)와 [communicatie 예제](gebruikersruimte/통신예제.cpp)가 werkelijk_gegevens machineopstart tests 대상이다. `파일규약.h`의 이름은 커널용/사용자용 모두 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 bestand Proces_WAARDE_invoer 및 루프백 전달은 Java 커널에서 실행한다. `통신규약.h`의 socket_WAARDE 함수는 actueel_item 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kernel_WAARDE 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 Volgende_item 도구를 사용하면 **새 QEMU를 부팅해 업로드한 werkelijk_gegevens 바이트를 재확인한 BACK_WAARDE 게스트에서 Uitvoeren_opdracht**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 hulpmiddelen/Uitvoeren_Bestand.py build/jkoros-native-sdk/demo.elf
python3 hulpmiddelen/Uitvoeren_Bestand.py 예제/Hello.java "한글 argumenten"
python3 hulpmiddelen/Uitvoeren_Bestand.py 예제/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kernel_WAARDE 묶음에 포함되어 이 bestand 한도를 적용받지 않는다. **C++ 컴파일러는 host SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 bibliotheek, PT_TLS, PT_INTERP, PT_DYNAMIC, Uitvoeren_opdracht·Schrijven 겸용 세그먼트는 로더가 거부한다. 구체적인 호출 INDEX·ADRES clip·오류는 [gebruikersruimte ABI](사용자호출규약.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `doorvoeren_Files`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 machtiging_WAARDE·dup/fcntl은 없다. 디렉터리와 peer_WAARDE/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 최대 512바이트, 소켓은 8개, ontvangen_WAARDE 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. gebruikersruimte Einde_app 시 열린 bestand 서술자와 소켓을 회수한다.

## valideren resultaat

`make test-jvm`은 9개 프로그램을 OpenJDK와 werkelijk_gegevens Eigen 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `hulpmiddelen/부팅시험.py`는 Java rechthoek API의 werkelijk_gegevens scherm 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 werkelijk_gegevens VNC invoer_WAARDE·한글 terminal 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT operatie_WAARDE resultaat 비교, 런타임 fout 중단, 미지원 Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kernel_WAARDE 계산·UTF-8·C++ 직접 호출·협력식 작업 및 프레임버퍼.
- 손상/잘못된 ABI/ADRES 초과/겹친 페이지/W+X 등 ELF weigeren_WAARDE 사례 22개.
- EL0 C++ 생성자·RAII·drijvende_komma_WAARDE operatie_WAARDE·bestand·heap_WAARDE 및 잘못된 시스템 호출 wijzer.
- kernel_WAARDE/CODE_WAARDE/MMIO Schrijven·toegang_invoer, NX operand_stack·NULL Uitvoeren_opdracht, guard page, 특권 opdracht 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 후 informatie_normaal app_f5044b9b 재실행.
- sprint_WAARDE Uitvoeren_opdracht 시 bestand/socket_WAARDE 누수 방지, UDP 왕복·보낸 ADRES·잘린 ontvangen_WAARDE·큐 포화·빈 datagram·미지원 communicatie fout.
- Shell Bewerk_WAARDE·Annuleren_operatie·16진수 업로드/다운로드·gebruikersruimte ELF 실행과 잘못된 ELF weigeren_WAARDE.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 Uitvoeren_opdracht, 한글 les_WAARDE·variabele_WAARDE·bestandsnaam_sms.
- 여러 Venster·vi Store_WAARDE·Bewerk_WAARDE·Retour_brug·gebruikersruimte Status_WAARDE 중단/cv_uitvoerbewerking, Swing 한글 invoer_WAARDE·이벤트·X Sluiten, 연결형 루프백, C/C++ 한글 SDK 예제.
- MicroPython Unicode·큰 geheel_getal·les_WAARDE·GC sprint_WAARDE·bestand import·uitzondering·bestand·UDP 왕복·TIJD_WAARDE 초과 후 복귀.
- GUI selectie_WAARDE verplaatsen_WAARDE_83b651b8, C++/UDP/Java/MicroPython 버튼 Uitvoeren_opdracht, 콘솔 복귀 및 werkelijk_gegevens 프레임버퍼 픽셀/lettertype_WAARDE.
- 디렉터리·variabele_WAARDE·toestand·bestand opdracht·script_WAARDE·순차 파이프·리다이렉션·capaciteit_WAARDE 초과 herstellen_Status, Python stdin/EOF와 Java/Python stdout.
- opdracht LOG_RECORD·긴 한글 invoer_WAARDE Bewerk_WAARDE·Voltooid_WAARDE·terminal 스크롤, 그래픽 app_f5044b9b Einde_app 후 Venster 복원, werkelijk_gegevens VNC Unicode toets_WAARDE·plakken_WAARDE·마우스.

[kernel_WAARDE tests LOG_RECORD](build/verification/implementation-test.log), [Shell tests](build/verification/shell/report.json), [VNC tests](build/verification/desktop/report.json), [machine 판독 resultaat](build/verification/report.json), [직렬 LOG_WAARDE](build/verification/serial.log), [GUI scherm](build/verification/gui-python.png)을 확인할 nummer 있다. VNC RFB 3.8 Verbinden 및 640×480 scherm 정보도 검사한다. [SDK 재컴파일 resultaat](build/verification/sdk.json)는 두 예제의 beginpunt·적재 세그먼트·ABI note가 machineopstart 시험한 ELF와 일치함을 확인한다. symbool_WAARDE 등 비적재 메타데이터를 포함한 bestand 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 clip

Eigen `javac`는 버전 49 `.class`를 생성하며 JVM은 steun_WAARDE 명령으로 구성된 버전 45–52 클래스를 실행한다. statisch_WAARDE FUNCTIE_WAARDE·재귀·int/boolean/char/String·toestand/sprint_WAARDE·tekenreeks_WAARDE 결합과 일부 bestand 스트림을 지원한다. UTF-8 문자열과 문자 리터럴, ASCII 및 현대 한글 음절/samenstelling_WAARDE 자모 식별자를 처리한다. Unicode id_WAARDE 전체 opzoektabel·Unicode bron_structuur 이스케이프는 구현하지 않았다. 게스트 bron_structuur 컴파일러는 일반 object_WAARDE·uitzondering·Thread 구문을 아직 컴파일하지 못한다. host `javac --release 8`로 만든 steun_WAARDE 부분집합 클래스는 Eigen JVM 0.4의 object_WAARDE·uitzondering·Thread·UDP와 Nederlands API를 사용할 nummer 있다. Swing은 문서화한 Eigen API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [Eigen JVM 설명](자바실행환경.md)이 기준이다. 상세 Taal 범위는 [공유 Java hulpmiddelen 설명](../../Guides/Java_IDE.md)을 참고하되, 그 문서의 x86 Shell/Store_WAARDE/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 bron_structuur**를 Eigen AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 FUNCTIE_WAARDE·les_WAARDE·uitzondering·리스트/woordenlijst·Unicode·GC·가변 precisie_WAARDE 정수를 제공한다. actueel_item 구성은 geheel_getal 빌드로 `float`, `complex`, `math`가 없으며 CPython 전체 표준 bibliotheek, pip, subprocess, threading, 일반 socket과 standaardwaarde `open()` bestand 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 object_WAARDE·모듈은 Einde_app 시 회수되고 RAM 파일만 Volgende_item 실행에 남는다.

`import jkoros`로 Volgende_item 시스템 연결을 쓴다. 모두 SVC를 통해 Eigen Java 커널에 접근한다.

| FUNCTIE_WAARDE | Actie |
|---|---|
| `stdin(limit)` | actueel_item 표준 입력에서 최대 limit바이트(0…16384)를 bytes로 읽음; EOF는 빈 bytes, UART gegevens 없음은 OSError(11) |
| `read(name)` | peer_WAARDE/절대 RAM 경로의 bestand 전체를 bytes로 읽음 |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 Store_WAARDE, 쓴 byte_WAARDE nummer Retour_HR |
| `remove(name)` | RAM bestand 삭제 |
| `rect(x, y, w, h, color)` | 선택한 werkelijk_gegevens scherm Grootte 안의 rechthoek tekening_WAARDE; 기존 보드의 RGB32 WAARDE |
| `ticks_ms()` | machineopstart 후 밀리초, 32비트 cyclus_WAARDE |
| `udp_open(port)` | 127.0.0.1의 UDP socket_WAARDE Openen/BIND_eindpunt; 0은 자동 hardware_poort |
| `udp_send(fd, port, data)` | 루프백 doel_WAARDE 포트에 str/bytes 버퍼 transfer_WAARDE |
| `udp_recv(fd)` | `(bytes, 보낸포트)` Retour_HR; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | socket_WAARDE Sluiten |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

이식 CODE_WAARDE: [python/](PYTHON_brug/), [gebruikersruimte Java Verbinden](gebruikersruimte/자바연결.c). 공식 [MicroPython 이식 LEESMIJ_eb81d7d9](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. bron_structuur URL·hash_Bestand·라이선스는 [vendor LEESMIJ_eb81d7d9](vendor/README.md)에 기록했다.

## 남은 작업

| Volgende_item fase_WAARDE | 완료 Taken_wortel |
|---|---|
| 영속 Store_WAARDE·Uitvoeren_opdracht bestand invoer_WAARDE | SD/MMC 및 디스크 bestand 시스템, 시스템/gebruikersruimte 볼륨; actueel_item ELF bestand 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 ADRES ADRES_regio, 선점 스케줄러, TLS, synchroniseren/wachten_WAARDE, 신호, mmap/mprotect |
| libc와 C++ 런타임 | Eigen ABI용 libc, malloc/free, 표준 I_O·Klok·omgeving·locale, libstdc++/uitzondering Proces_WAARDE_invoer valideren |
| CPython | 해당 libc와 OS API 대상으로 이식·교차 빌드하고 bestand/Unicode/스레드/socket_WAARDE tests |
| OpenJDK/JRE | HotSpot OS laag_WAARDE, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 bibliotheek 이식; javac/java werkelijk_gegevens Uitvoeren_opdracht |
| extern_WAARDE 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 werkelijk_gegevens Bord 송수신 valideren, DNS·Wi-Fi |
| GUI extensie_WAARDE | USB HID, 게스트 입력기·문자 조판, Swing Venster Grootte 조절·클리핑 extensie_WAARDE, 전체 AWT/Swing 이식 |

이 표는 남은 작업이며 implementatie 완료 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 extern_WAARDE 네트워크 드라이버는 실물 검증도 필요하다. [QEMU mobiel_WAARDE 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

hardware_WAARDE 및 ABI 참고: [BCM2711 accessoire](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC ADRES](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox contractwaarde](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP controle_WAARDE 레지스터 Definitie_WAARDE](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Nederlands C gegevenstype·Python fout·bundel installeren_WAARDE

C 네트워크 API는 `struct mesh_socket_ADRES`, enum 상수와 werkelijk_gegevens Nederlands 함수로
구현한다. macro_WAARDE 별칭을 사용하지 않으며 Vorige_item pk_* ABI도 유지한다.
Python 예제는 `systeemfout`, `fout.INDEX`, `fout.설명`을 사용한다.

`python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 nummer 있다. 현재는 host 중계를
이용하는 제한형 MicroPython bron_structuur 설치기이며 CPython pip·자동 의존성 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 제한](PYTHON_bundel.md).

## scherm Grootte selectie_WAARDE

`python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. terminal verplaatsen_WAARDE_83b651b8, Swing 가운데 koppelindeling, Java·C·Python 그리기도 werkelijk_gegevens 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [Instellingen·Nederlands API·valideren LEESMIJ_eb81d7d9](beeldschermresolutie.md).

## Nederlands 직접 API와 scherm vernieuwen

`example/java`는 `실행할일`, `동작받이`, `Actie_kennisgeving`, `knop`, `gebeurtenis_wachtrij`,
`achtergrondwerker`, `starten()`을 사용할 nummer 있다. Nederlands GUI/가닥을 Eigen JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. tekenreeks_WAARDE 등 javac의 표준
계약과 전체 bron_structuur 검토 범위는 [명명 LEESMIJ_eb81d7d9](명명/LEESMIJ_eb81d7d9.md), 사용법과 호환성 변경은
[Nederlands Java API](한국어자바/LEESMIJ_eb81d7d9.md)를 본다.

terminal verplaatsen_WAARDE_83b651b8·Grootte 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[scherm vernieuwen 설명](자바실행환경.md#terminal-부분-vernieuwen),
[부분 vernieuwen 검사](build/verification/redraw/report.json)를 참고한다.
