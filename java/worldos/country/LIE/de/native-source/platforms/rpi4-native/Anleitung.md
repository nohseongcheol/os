# Raspberry Pi 4 eigen Java betriebskernWert — Benutzer befehlAusführen grundlage

aktuellElementeintrag eigen 코드의 COSL 상업 bedingung, 제3자 고지 및 LGPL neuverbindenEndpunkt 자료는 [COSL verteilungWert Anleitung](COSLVerteilungLeitfaden.md)를 참고한다. umschaltenBetriebsart davorWert GPL 구성의 판단은 [vorherigElementeintrag 라이선스 검토](LizenzDurchsicht.md)에 기록했다.

Deutsch Kommunikation·ausnahme 사용법은 [Deutsch Java API](DeutschJava/Anleitung.md), Funktion·variableWert·Datei 이름의 변경과 어원 근거는 [benennung Anleitung](benennung/Anleitung.md)를 참고한다.

Linux 없이 부팅하는 eigen AArch64 커널이다. Java AOT betriebskernWert 위에 **befehlZeile befehlshülle, 게스트 Java Übersetzer·JVM, MicroPython, EL0 C++ befehlAusführen, Datei·UDP 루프백 시스템 aufrufen, 여러 HangulText GUI terminal·vi Editor·Swing 부분집합**을 제공한다. 커널의 Datei Daten/정책·루프백 übertragungWert·befehlshülle 상태는 Java, Bildschirm 합성·bildpunkt wertÄndern·zeiger·클리핑도 Java로 구현하며, CPU/MMU/Gerät 경계와 terminal·zeichenWert malenBildschirm 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 eigen 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 befehlAusführen, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](DateiÜbertragungUndÜbersetzungsvorgang.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, physischHardware Pi4의 verdrahtetWert 송수신은 아직 미검증이다.** befehlAusführen·verbindung·passwortWert 확인은 [externWert verbindung Anleitung](ExternVerbindungLeitfaden.md)에 정리했다.

셸은 EL1 betriebskernWert, `java` 등 Benutzer befehlAusführen 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 grenzwertWert, QEMU 네트워크 befehlAusführen·verbindung 방법 및 tatsächlichDaten 검증은
[befehlAusführen 계층과 externWert Kommunikation statuswertUntersuchen](LaufzeitUndExternNetzwerkPrüfpunkte.md)을 참고한다.

ELF는 확장자가 아닌 tatsächlichDaten befehlAusführen 형식으로 검사한다. `./Gruß`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 statischWert ELF는 `run --linux dateiNameText`으로 실행한다. [ELF·Linux ABI unterstützungWert 범위와 동일 바이너리 Prüfungen](ausführdateiABI.md).

GUI와 네트워크는 `python3 Werkzeuge/befehlAusführen.py --desktop --network`로 함께 사용한다. Java·C·Python의 Deutsch Beispiele 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 Startvorgang 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 Zahl 있다. Remmina에서 **F9/Shift+Space/한·nullwertOperand tasteWert**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·tatsächlichDaten TCP/UDP·Datei byteWert·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` danachStatuswert `java Fensterbeispiel`로 Deutsch Swing 예제를 실행한다. terminal 모서리에 마우스를 대고 **linksSeiteRand 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 aktuellElementeintrag spalteWert·zeilennummerWert 수를 보여 준다.

## aktuellElementeintrag unterstützungWert beschneiden

| 기능 | umsetzung·시험한 beschneiden | 아직 istNichtUnterstützt |
|---|---|---|
| Startvorgang | Pi4 AArch64 EL1, UART, SD용 abbildErzeugenAbbild, QEMU raspi4b Startvorgang | tatsächlichDaten Pi4 보드에서의 펌웨어 Startvorgang Prüfungen |
| Java betriebskernWert | statischWert Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objektWert/ausnahme/GC/JVM/표준 bibliothek |
| Java entwicklung Werkzeuge | 게스트 eigen `javac`/`java`, JVM 0.4/JAR: 다중 klasseWert·objektWert·상속·ausnahme·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, Deutsch bibliothek. 게스트 컴파일러는 statischWert Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | tatsächlichDaten MicroPython 1.24.1 EL0 Portierung, quelltextBaum quelltextÜbersetzen/befehlAusführen, klasseWert·ausnahme·GC·큰 Ganzzahl·Unicode·Datei·UDP/Bildschirm verbinden | CPython, pip, C erweiterungWert, 부동소수점, 일반 OS/스레드/netzbuchseWert modulWert, interaktiv REPL |
| befehlshülle | UTF-8 bearbeitenWert·protokolldateiAufzeichnung·abgeschlossenWert, 디렉터리·Datei befehl, variableWert·bedingung·skriptWert, 16 KiB 순차 파이프·리다이렉션, ELF befehlAusführen | 전체 POSIX sh/Bash, Aufgabe steuerungWert·동시 프로세스·PTY |
| C/AOT quelltextÜbersetzen | 게스트 TinyCC 및 statischWert Java 부분집합 `jaot` → eigen ARM64 ELF | 전체 libc·모든 Java klasseWert AOT |
| C++ | 독립 ELF64를 EL0에서 befehlAusführen; statischWert 생성자, RAII 소멸자, FP/SIMD, Deutsch Datei/루프백 aufrufen | libc/libstdc++, STL, C++ ausnahme·RTTI·동적 verbinden |
| Benutzer wertSchützen | 4 KiB 페이지, kodeWert RX/Daten RW·NX, betriebskernWert·MMIO 차단, guard page, 잘못된 zeiger Prüfpunkte | 다중 Benutzer erlaubnisWert, 일반 프로세스/스레드 스케줄러 |
| befehlAusführen zeitWert grenzwertWert | GIC-400 타이머로 무한 wiederholungsschrittWert verlassenProzessProgramm; interaktiv Eingabewert 대기는 기한 auffrischen, 터미널별 EL0 Programm 중단·fortführenAusführung | 일반적인 선점형 다중작업. 긴 betriebskernWert aufrufen 도중에는 종료가 지연될 Zahl 있음 |
| Datei | Java RAM Datei 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, gegenstelleWert/절대 pfad 63바이트, deskriptorEintrag 16개 | erlaubnisWert, 디스크/SD 영속 ablegenDatenWert |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP umsetzung, 게스트 FTP·SSH·VNC | GENET physischHardware validieren, Wi-Fi, DNS, 일반 TLS netzbuchseWert, RDP |
| GUI | höchstwertWert 네 terminal fenster, auswahlWert·bewegenWert·X schließen, HangulText schriftartWert, Swing 부분집합; 게스트 VNC Bildschirm·Eingabewert·두벌식 | physischHardware USB Eingabewert, 전체 AWT/Swing·Java2D·fenster 관리 정책 |
| Aufgabe ausführungsfadenWert | betriebskernWert Aufgabe 2개와 주 Aufgabe; JVM 내부 ausführungsfadenWert höchstwertWert 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, HangulText·일본어·아랍어·이모지, UTF-8 dateiNameText/datagramm | GUI의 일반 다국어 조판 |

befehlAusführen 버튼 화면은 5×7 영문 글꼴을 쓰며, terminal 창은 Noto CJK/DejaVu에서 생성한 HangulText·Unicode 비트맵 글꼴을 쓴다. UART와 tatsächlichDaten 프레임버퍼의 HangulText 표시를 시험한다. 루프백은 동일 betriebskernWert 내부의 datagramm 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 hilfsWert UART SLIP 경로를 사용한다. `python3 Werkzeuge/befehlAusführen.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·befehlAusführen 제한과 Deutsch 사용법은 [eigen JVM과 Deutsch bibliothek](JavaLaufzeitUmgebung.md)에 정리했다. klasseWert Datei/JAR 배포는 [DeutschJava](DeutschJava) 소스에서 재현한다. 기존 Linux판 `Deutsch.Java`와 별도인 `Deutsch.eigen` 패키지다.

**vi·여러 fenster·Swing·HangulText Java/Python/C/C++·posix-kor 예제는 [HangulText entwicklung 매뉴얼](EntwicklungLeitfaden.md)에 정리했다.**

GUI terminal befehlAusführen·단축키·befehlshülle befehl·제한은 [셸과 terminal 사용법](BefehlshülleUndTerminal.md)에 정리했다.

## aktuellElementeintrag 컴퓨터에서 befehlAusführen

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

verlassenProzessProgramm: **Ctrl+A nächsterElementeintrag X**. 게스트 C/AOT Werkzeuge 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc arithmetikWert hilfsWert 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. Wirtssystem 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 Portierung·링크한 것은 아니다. Übersetzer 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/pfad/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` unterstützungWert 여부를 확인한 danachStatuswert 실행한다.

명령은 **Enter를 눌러 befehlAusführen**한다. 기존 한 zeichenWert 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "HangulText argumente 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| befehl | aktion |
|---|---|
| `help` / `info` | befehl·tatsächlichDaten umsetzung statuswertWert |
| `ls` / `cat FILE` / `rm FILE` | RAM Datei eintragListe·inhaltswertWert·삭제 |
| `vi FILE` | Benutzer gebietWert vi 부분집합, HangulText bearbeitenWert·ablegenDatenWert·검색·되돌리기 |
| `edit FILE` | Datei 전체를 새로 Eingabewert; 단독 `.` 줄로 ablegenDatenWert, Ctrl-C로 abbrechenVorgangVorgang |
| `javac FILE.java` / `java CLASS [ARGS]` | eigen 제한형 Java quelltextÜbersetzen·befehlAusführen |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython quelltextÜbersetzen·befehlAusführen |
| `load FILE` / `hex FILE` | 16진수 바이너리 Eingabewert/Ausgabe; 입력은 단독 `.` 줄로 ablegenDatenWert |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 eigen ABI ELF / 내장 C++ Beispiele |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 Aufgabe / EL0 wertSchützen Prüfungen |
| `gui` / `terminal` | befehlAusführen Bildschirm / HangulText GUI terminal; F12로 terminal öffnen·schließen |
| `samples` | 삭제한 standardwertWert Beispiele statuswertWiederherstellen; 기존 파일은 보존 |

예를 들어 `edit Gruß.java`를 입력한 nächsterElementeintrag unterkanteWert 소스를 입력한다.

```java
public class Gruß { public static void main(String[] args) { int Wert = 7; System.out.println("HangulText=" + Wert); } }
```

그다음 단독 `.` 줄로 저장하고 `javac Gruß.java`, `java Gruß`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. abbrechenVorgangVorgang·잘못된 16진수·kapazitätWert 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, befehlAusführen 인수는 höchstwertWert 8개·각각 UTF-8 255바이트다. 일반 befehl 인수는 höchstwertWert 32개다. anführungszeichen·백슬래시·befehlshülle variableWert·파이프·리다이렉션 범위는 [befehlshülle beschreibung](BefehlshülleUndTerminal.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, adresse **127.0.0.1:5902**로 연결한다. 키보드·HangulText Unicode Eingabewert·명시적 einsetzenWert·befehlAusführen 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Werkzeuge/befehlAusführen.py --desktop --network
# 다른 hardwarePort: python3 Werkzeuge/befehlAusführen.py --desktop --port 5903
```

종료는 실행한 Wirtssystem 터미널에서 Ctrl+C다. 기존 `python3 Werkzeuge/befehlAusführen.py --vnc 127.0.0.1:2`는 Bildschirm 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. tatsächlichDaten Pi4 USB 입력기는 아직 없으며, VNC verbinden 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 tatsächlichDaten C++/UDP ELF befehlAusführen, `Hello.java` quelltextÜbersetzen danachStatuswert JVM befehlAusführen, `hello.py` befehlAusführen, GUI terminal 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interaktiv 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 speicherDaten·CPU 문맥을 보관한다. befehlshülle·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## tatsächlichDaten 산출물과 Pi4 SD abbildErzeugenAbbild

```sh
make image   # betriebskernWert, SD abbildErzeugenAbbild, Startvorgang ZIP, 사용자용 SDK
make sdk     # SDK만 erneutVersuchenWert generieren
```

| pfad | 용도 |
|---|---|
| `build/kernel8.img` | eigen betriebskernWert 기계어, 적재 adresse 0x80000 |
| `build/kernel.elf`, `kernel.map` | betriebskernWert symbolWert·Bindungsanordnung |
| `build/user/demo.elf` | Benutzer betriebsartWert C++ Datei/speicherhaldeWert/fließendPunktWert/그래픽 Beispiele |
| `build/user/network.elf` | Benutzer betriebsartWert C++ UDP 루프백 Beispiele |
| `build/user/java-tools.elf` | eigen Java 부분집합 Übersetzer/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | Wirtssystem javac용 Deutsch API klasseWert; 같은 클래스가 eigen JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | Deutsch API Java Quelltext |
| `build/user/vi.elf` | eigen UTF-8 vi befehl 부분집합 Editor |
| `build/user/python.elf` | eigen ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 wertSchützen Prüfungen 전용 |
| `build/libposix-kor-arm64.a` | **betriebskernWert 내부**에서 Java Datei 구현을 직접 부르는 기존 verbinden |
| `build/libposix-kor-user.a` | **EL0 Benutzer Programm**에서 SVC로 Datei/루프백을 호출하는 새 verbinden |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD abbildErzeugenAbbild |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 Startvorgang 파티션에 복사할 Datei gruppeWert |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·ausführenVorgang kodeWert·bibliothek·링커 skriptWert·Beispiele |
| `dist/manifest.json`, `build/build.json` | SHA256과 tatsächlichDaten unterstützungWert statuswertWert |

이미지는 확인된 공식 Pi Startvorgang 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·terminal schriftartWert 라이선스와 schriftartWert ursprungWert 해시도 동봉한다. Datei generieren 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 abbildErzeugenAbbild protokolldateiAufzeichnung 도구로 `.img`를 기록하거나 FAT32 Startvorgang 파티션 최상위에 ZIP 내용을 푼다. abbildErzeugenAbbild 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 standardwertWert EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**physischHardware Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Datei 구성·betriebskernWert 체크섬 검사와 물리 Platine Startvorgang 검증은 별개다. MMU benutzenWert 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 Startvorgang 조건을 전제로 한다. dreiWert hilfsWert 코어는 대기시키며 한 코어만 사용한다.

## C++와 Deutsch API benutzenWert

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/Dateibeispiel.cpp -o demo.elf
python3 compile.py examples/KommunikationBeispiel.cpp -o network.elf
```

진입점은 `extern "C" int benutzerProgrammStarten(int)`이다. Benutzer C++는 FP/SIMD를 사용할 Zahl 있다. betriebskernWert C/Java AOT는 일반 레지스터만 사용하므로 ausnahme prozessWertEintrag 중 Benutzer FP 상태를 건드리지 않는다. Benutzer eintragPunktWert 시 FP 상태를 초기화하고 betriebskernWert 복귀에 필요한 상태를 보존한다.

```cpp
#include "DateiABI.h"
extern "C" int benutzerProgrammStarten(int) {
    int Datei = dateiÖffnen("Gruß.txt", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
    if (Datei < 0) return 1;
    const char inhaltswertWert[] = "안녕하세요";
    int ergebnis = dateiDatenSchreiben(Datei, inhaltswertWert, sizeof(inhaltswertWert) - 1);
    dateiSchließen(Datei);
    return ergebnis == sizeof(inhaltswertWert) - 1 ? 0 : 2;
}
```

[Datei Beispiele](Benutzer/Dateibeispiel.cpp)와 [Kommunikation Beispiele](Benutzer/KommunikationBeispiel.cpp)ersterOperand tatsächlichDaten Startvorgang Prüfungen 대상이다. `DateiABI.h`의 이름은 커널용/사용자용 alleErzeugenAbbild 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Datei prozessWertEintrag 및 루프백 전달은 Java 커널에서 실행한다. `NetzwerkABI.h`의 netzbuchseWert 함수는 aktuellElementeintrag 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 betriebskernWert 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 nächsterElementeintrag 도구를 사용하면 **새 QEMU를 부팅해 업로드한 tatsächlichDaten 바이트를 재확인한 rückseiteWert 게스트에서 befehlAusführen**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Werkzeuge/dateiAusführen.py build/jkoros-native-sdk/demo.elf
python3 Werkzeuge/dateiAusführen.py Beispiele/Hello.java "HangulText argumente"
python3 Werkzeuge/dateiAusführen.py Beispiele/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 betriebskernWert 묶음에 포함되어 이 Datei 한도를 적용받지 않는다. **C++ 컴파일러는 Wirtssystem SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 bibliothek, PT_TLS, PT_INTERP, PT_DYNAMIC, befehlAusführen·schreiben 겸용 세그먼트는 로더가 거부한다. 구체적인 aufrufen Nummer·adresse beschneiden·오류는 [Benutzer ABI](BenutzerAufrufVorgangABI.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `bestätigenDateiSpeichergerät`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 erlaubnisWert·dup/fcntl은 없다. 디렉터리와 gegenstelleWert/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 höchstwertWert 512바이트, 소켓은 8개, wertEmpfangen 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. Benutzer verlassenProzessProgramm 시 열린 Datei 서술자와 소켓을 회수한다.

## validieren ergebnis

`make test-jvm`은 9개 프로그램을 OpenJDK와 tatsächlichDaten eigen 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Werkzeuge/Startprüfung.py`는 Java rechteck API의 tatsächlichDaten Bildschirm 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 tatsächlichDaten VNC Eingabewert·HangulText terminal 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT vorgangWert ergebnis 비교, 런타임 fehler 중단, istNichtUnterstützt Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java betriebskernWert berechnung·UTF-8·C++ 직접 aufrufen·협력식 Aufgabe 및 프레임버퍼.
- 손상/잘못된 ABI/adresse 초과/겹친 페이지/W+X 등 ELF wertZurückweisen 사례 22개.
- EL0 C++ 생성자·RAII·fließendPunktWert vorgangWert·Datei·speicherhaldeWert 및 잘못된 시스템 aufrufen zeiger.
- betriebskernWert/kodeWert/MMIO schreiben·zugriffEintrag, NX operandStapel·NULL befehlAusführen, guard page, 특권 befehl 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 danachStatuswert istNormal Programm 재실행.
- wiederholungsschrittWert befehlAusführen 시 Datei/netzbuchseWert 누수 방지, UDP 왕복·보낸 adresse·beschnittenWert wertEmpfangen·큐 포화·빈 datagramm·istNichtUnterstützt Kommunikation fehler.
- befehlshülle bearbeitenWert·abbrechenVorgangVorgang·16진수 업로드/다운로드·Benutzer ELF 실행과 잘못된 ELF wertZurückweisen.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 befehlAusführen, HangulText klasseWert·variableWert·dateiNameText.
- 여러 fenster·vi ablegenDatenWert·bearbeitenWert·zurückkehrenBrücke·Benutzer statuswertWert 중단/fortführenAusführung, Swing HangulText Eingabewert·이벤트·X schließen, 연결형 루프백, C/C++ HangulText SDK Beispiele.
- MicroPython Unicode·큰 Ganzzahl·klasseWert·GC wiederholungsschrittWert·Datei import·ausnahme·Datei·UDP 왕복·zeitWert 초과 danachStatuswert 복귀.
- GUI auswahlWert bewegenWert, C++/UDP/Java/MicroPython 버튼 befehlAusführen, 콘솔 복귀 및 tatsächlichDaten 프레임버퍼 픽셀/schriftartWert.
- 디렉터리·variableWert·bedingung·Datei befehl·skriptWert·순차 파이프·리다이렉션·kapazitätWert 초과 statuswertWiederherstellen, Python stdin/EOF와 Java/Python stdout.
- befehl protokolldateiAufzeichnung·긴 HangulText Eingabewert bearbeitenWert·abgeschlossenWert·terminal 스크롤, 그래픽 Programm verlassenProzessProgramm danachStatuswert fenster 복원, tatsächlichDaten VNC Unicode tasteWert·einsetzenWert·마우스.

[betriebskernWert Prüfungen protokolldateiAufzeichnung](build/verification/implementation-test.log), [befehlshülle Prüfungen](build/verification/shell/report.json), [VNC Prüfungen](build/verification/desktop/report.json), [maschine 판독 ergebnis](build/verification/report.json), [seriellWert protokolldateiWert](build/verification/serial.log), [GUI Bildschirm](build/verification/gui-python.png)을 확인할 Zahl 있다. VNC RFB 3.8 verbinden 및 640×480 Bildschirm 정보도 검사한다. [SDK 재컴파일 ergebnis](build/verification/sdk.json)는 두 예제의 eintragPunkt·적재 세그먼트·ABI note가 Startvorgang 시험한 ELF와 일치함을 확인한다. symbolWert 등 비적재 메타데이터를 포함한 Datei 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 beschneiden

eigen `javac`는 버전 49 `.class`를 생성하며 JVM은 unterstützungWert 명령으로 구성된 버전 45–52 클래스를 실행한다. statischWert Funktion·재귀·int/boolean/char/String·bedingung/wiederholungsschrittWert·Zeichenkette 결합과 일부 Datei 스트림을 지원한다. UTF-8 문자열과 Zeichen 리터럴, ASCII 및 현대 HangulText 음절/Zusammenstellung hangulBuchstabeWert 식별자를 처리한다. Unicode bezeichnerWert 전체 Tabelle·Unicode quelltextBaum 이스케이프는 구현하지 않았다. 게스트 quelltextBaum 컴파일러는 일반 objektWert·ausnahme·Thread 구문을 아직 컴파일하지 못한다. Wirtssystem `javac --release 8`로 만든 unterstützungWert 부분집합 클래스는 eigen JVM 0.4의 objektWert·ausnahme·Thread·UDP와 Deutsch API를 사용할 Zahl 있다. Swing은 문서화한 eigen API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [eigen JVM beschreibung](JavaLaufzeitUmgebung.md)이 기준이다. 상세 Sprache 범위는 [공유 Java Werkzeuge beschreibung](../../Dokumentation/JavaEntwicklungsumgebung.md)을 참고하되, 그 문서의 x86 befehlshülle/ablegenDatenWert/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 quelltextBaum**를 eigen AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 Funktion·klasseWert·ausnahme·리스트/Wörterbuch·Unicode·GC·가변 genauigkeitWert 정수를 제공한다. aktuellElementeintrag 구성은 Ganzzahl 빌드로 `float`, `complex`, `math`ersterOperand 없으며 CPython 전체 표준 bibliothek, pip, subprocess, threading, 일반 socket과 standardwertWert `open()` Datei 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objektWert·모듈은 verlassenProzessProgramm 시 회수되고 RAM 파일만 nächsterElementeintrag 실행에 남는다.

`import jkoros`로 nächsterElementeintrag 시스템 연결을 쓴다. alleErzeugenAbbild SVC를 통해 eigen Java 커널에 접근한다.

| Funktion | aktion |
|---|---|
| `stdin(limit)` | aktuellElementeintrag 표준 입력에서 höchstwertWert limit바이트(0…16384)를 bytes로 ergebnisLesen; EOF는 빈 bytes, UART Daten 없음은 OSError(11) |
| `read(name)` | gegenstelleWert/절대 RAM 경로의 Datei 전체를 bytes로 ergebnisLesen |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 ablegenDatenWert, 쓴 byteWert Zahl zurückkehrenErgebnis |
| `remove(name)` | RAM Datei 삭제 |
| `rect(x, y, w, h, color)` | 선택한 tatsächlichDaten Bildschirm größe 안의 rechteck Zeichnung; 기존 보드의 RGB32 Wert |
| `ticks_ms()` | Startvorgang danachStatuswert millisekunden, 32비트 zyklusWert |
| `udp_open(port)` | 127.0.0.1의 UDP netzbuchseWert öffnen/AusführbündelPacken; 0은 자동 hardwarePort |
| `udp_send(fd, port, data)` | 루프백 zielWert 포트에 str/bytes 버퍼 übertragungWert |
| `udp_recv(fd)` | `(bytes, 보낸포트)` zurückkehrenErgebnis; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | netzbuchseWert schließen |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

Portierung kodeWert: [python/](pythonBrücke/), [Benutzer Java verbinden](Benutzer/javaBrücke.c). 공식 [MicroPython Portierung Anleitung](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. quelltextBaum URL·prüfsummeDatei·라이선스는 [vendor Anleitung](vendor/README.md)에 기록했다.

## 남은 Aufgabe

| nächsterElementeintrag stufeWert | istFertig projektWurzel |
|---|---|
| 영속 ablegenDatenWert·befehlAusführen Datei Eingabewert | SD/MMC 및 디스크 Datei 시스템, 시스템/Benutzer 볼륨; aktuellElementeintrag ELF Datei 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 adresse adresseGebiet, 선점 스케줄러, TLS, synchronisieren/wertWarten, 신호, mmap/mprotect |
| libc와 C++ 런타임 | eigen ABI용 libc, malloc/free, 표준 eingabeAusgabe·Uhr·umgebung·locale, libstdc++/ausnahme prozessWertEintrag validieren |
| CPython | 해당 libc와 OS API 대상으로 Portierung·교차 빌드하고 Datei/Unicode/스레드/netzbuchseWert Prüfungen |
| OpenJDK/JRE | HotSpot OS schichtWert, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 bibliothek Portierung; javac/java tatsächlichDaten befehlAusführen |
| externWert 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 tatsächlichDaten Platine 송수신 validieren, DNS·Wi-Fi |
| GUI erweiterungWert | USB HID, 게스트 입력기·Zeichen 조판, Swing fenster größe 조절·클리핑 erweiterungWert, 전체 AWT/Swing Portierung |

이 표는 남은 작업이며 umsetzung istFertig 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 externWert 네트워크 드라이버는 physischHardware 검증도 필요하다. [QEMU Gerät 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

hardwareWert 및 ABI 참고: [BCM2711 peripherie](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC adresse](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox vertragWert](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP steuerungWert 레지스터 definitionWert](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## Deutsch C datenTyp·Python fehler·Paket wertEinrichten

C 네트워크 API는 `struct InternetNetzbuchseAdresse`, enum 상수와 tatsächlichDaten Deutsch 함수로
구현한다. makroWert 별칭을 사용하지 않으며 vorherigElementeintrag pk_* ABI도 유지한다.
Python 예제는 `SystemFehler`, `fehler.Nummer`, `fehler.beschreibung`을 사용한다.

`python3 Werkzeuge/befehlAusführen.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 Zahl 있다. 현재는 Wirtssystem 중계를
이용하는 제한형 MicroPython quelltextBaum 설치기이며 CPython pip·자동 abhängigkeiten 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 grenzwertWert](PythonBündel.md).

## Bildschirm größe auswahlWert

`python3 Werkzeuge/befehlAusführen.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. terminal bewegenWert, Swing mitte Bindungsanordnung, Java·C·Python 그리기도 tatsächlichDaten 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [einstellungen·Deutsch API·validieren Anleitung](bildschirmAuflösung.md).

## Deutsch 직접 API와 Bildschirm auffrischen

`example/java`는 `AusführbarAufgabe`, `AktionEmpfänger`, `AktionMitteilung`, `schaltfläche`, `EreignisWarteschlange`,
`hintergrundarbeiter`, `ausführenVorgang()`을 사용할 Zahl 있다. Deutsch GUI/가닥을 eigen JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. Zeichenkette 등 javac의 표준
계약과 전체 quelltextBaum 검토 범위는 [benennung Anleitung](benennung/Anleitung.md), 사용법과 호환성 변경은
[Deutsch Java API](DeutschJava/Anleitung.md)를 본다.

terminal bewegenWert·größe 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[Bildschirm auffrischen beschreibung](JavaLaufzeitUmgebung.md#terminal-unterteilWert-auffrischen),
[unterteilWert auffrischen Prüfpunkte](build/verification/redraw/report.json)를 참고한다.
