# Java 네이티브 Betriebssystem

이 문서는 기존 **x86 betriebskernWert**을 설명한다. Raspberry Pi 4의 eigen ARM64 anfänglichStatuswert 이식은 [별도 Anleitung](../platforms/rpi4-native/README.md)를 참고한다. unterkanteWert x86 Benutzer ELF·네트워크·IDE ablegenDatenWert 기능이 ARM64에 alleErzeugenAbbild 이식된 상태는 아니다.

Java 원문을 eigen AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 eigen 제한형 Java Übersetzer·JVM ELF를 Benutzer 모드에 적재할 Zahl 있다. Linux, engos, koros4와 externWert OpenJDK는 게스트에 적재하지 않는다. Startvorgang 진입과 hardwarePort/물리 Speicherraum 접근은 어셈블리이며, Zeichen TerminalEinAusgabe·Eingabewert prozessWertEintrag·befehl wertAnalysieren·Aufgabe abschnittWert 관리는 `Quelltext/*.java`에 있다.

## 게스트 Java entwicklung

`javac Hello.java`, `java Hello`로 부팅된 Betriebssystem 안에서 quelltextÜbersetzen·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 höchstwertWert 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 Zahl 있다. 이 기능은 eigen 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·unterstützungWert 문법·Datei 적재·교차 시험은 [Java entwicklung umgebung](../Dokumentation/JavaEntwicklungsumgebung.md)에 있다. `make test-java`로 검증한다.

## 빌드와 befehlAusführen

`compiler/`ersterOperand 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS modulWert, `xorriso`ersterOperand 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. aktuellElementeintrag 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 ablegenDatenWert 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 standardwertWert 64MiB이며 mindestwertWert 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (Benutzer ELF gruppeWert Kopfdateien)
make run             # ELF 직접 Startvorgang, seriellWert TerminalEinAusgabe
make run-gui         # GRUB ISO Startvorgang, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM befehlAusführen
make vbox-status     # 전용 VirtualBox VM statuswertWert überprüfen
make test            # ELF와 ISO 두 경로의 tatsächlichDaten Startvorgang/Eingabewert Prüfungen
make apps            # Benutzer 프로그램만 systemErzeugenAbbild
make test-network    # Benutzer befehlAusführen/UDP/wertSchützen Prüfungen
```

`make run`은 QEMU의 seriellWert 표준 입출력을 쓴다. `Ctrl+A`를 누른 rückseiteWert `X`로 QEMU를 종료할 Zahl 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU fenster/프로세스는 별도로 닫는다. 폴링 방식이라 wertWarten 중에도 Wirtssystem CPU를 사용할 Zahl 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 speicherDaten 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 benötigtWert 없다. tatsächlichDaten VirtualBox 5.2.42에서 Startvorgang, Java eigen Prüfungen, befehlshülle Eingabewert, `run hello vbox`의 ring 3 실행과 istNormal 종료를 확인했다. aktuellElementeintrag Kommunikation 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 Zahl 없어 네트워크 장치를 비활성화한다. ablegenDatenWert statuswertWert 재개와 새 systemErzeugenAbbild 반영 방법은 [VirtualBox befehlAusführen Anleitung](../Dokumentation/VirtualBoxStarten.md)에 있다.

## 셸에서 Benutzer Programm befehlAusführen 및 네트워크 aufrufen

독립 ELF32 befehlAusführen 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 TerminalEinAusgabe Ausgabe, argumente abfragenWert, UDP öffnen·senden·empfangen·닫기를 제공한다. Benutzer 코드를 betriebskernWert 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

letzterElementeintrag 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/Werkzeuge/DatenWiederherstellen.py --port 9000`을 먼저 실행한다. 상세 API, Programm eintragAnhängen, adresse 공간과 제한은 [Benutzer befehlAusführen·네트워크 Anleitung](Benutzer/Anleitung.md)에 있다.

Startvorgang überprüfen wortgruppeWert:

```text
JKOROS NATIVE JAVA
Java 기계어 betriebskernWert ausführenVorgang
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF Startvorgang, x86 wertSchützen betriebsartWert GDT, BSS initialisieren, 64KiB operandStapel.
- Java Funktion tatsächlichDaten 실행과 Startvorgang systemInformation markierungWert überprüfen.
- COM1 seriellWert eingabeAusgabe, VGA Zeichen Bildschirm·mauszeigerWert·스크롤·eintragTilgen.
- PS/2 standardwertWert 자판, 좌우 Shift, Enter, Backspace. erweiterungWert tasteWert/마우스 자료는 befehl 입력으로 쓰지 않는다.
- Länge 128의 befehl Eingabewert 버퍼, überlaufWert 방지, CR/LF prozessWertEintrag.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB Aufgabe abschnittWert 8개의 speichergerätZuteilen·zurückkehrenErgebnis·재사용과 중복 zurückkehrenErgebnis 방지.
- Java datenfeldWert 256KiB 영역의 größe·feldindexWert 검사와 런타임 fehler 중단.
- lesen 전용 JKAP befehlAusführen gruppeWert, ELF32 abschnittWert/eintragPunkt validieren, Benutzer betriebsartWert·argumente·verlassenProzessProgramm kodeWert.
- betriebskernWert/Benutzer 페이지 erlaubnisWert 분리, TSS, IDT, PIT 100Hz, Benutzer CPU ausnahme prozessWertEintrag 및 befehlAusführen zeitWert 상한.
- PCI RTL8139 폴링 드라이버, ARP, statischWert IPv4, UDP kontrollsumme·송수신·wertWarten grenzwertWert.

`mem`의 Upper memory는 Multiboot의 1MiB obererSeiteRand dichtUmschaltenFallliste speicherDaten größe(KiB)이며, 전체 speicherDaten 지도 분석이나 자유 물리 speicherDaten 수치가 아니다. `alloc`은 이미 확보한 Ganzzahl datenfeldWert 안의 Aufgabe abschnittWert 번호를 반환한다. 일반 물리 seiteWert speichergerätZuteilen, adresse adresseGebiet 또는 Benutzer prozessWert speicherDaten 관리가 아니다.

## 명시적인 grenzstelleGrenzwert

이 커널은 **Benutzer 프로그램을 한 번에 einsWert 실행하는 anfänglichStatuswert betriebskernWert**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. Benutzer CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 betriebskernWert 예외는 중단한다. befehlAusführen 시간은 약 3초로 제한한다. 완전한 선점 다중 prozessWert 스케줄러, FAT/ext 등 일반 디스크 DateiSystem, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 objektWert 모델/GC는 아직 없다. 전용 IDE Datei 보존과 POSIX Datei/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 befehlAusführen 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 befehlAusführen 파일은 systemErzeugenAbbild 시 lesen 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../Kernquelltext/`의 JVM 관리 betriebskernWert 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. seriellWert 출력은 이 프로젝트의 HangulText(BMP Zeichen)을 UTF-8로 표시한다. VGA는 standardwertWert ASCII 글꼴만 사용하므로 HangulText 자리에 `?`ersterOperand 나온다. befehl 입력도 aktuellElementeintrag ASCII만 지원하며 HangulText schriftartWert·입력기 및 hilfsWert 평면 Zeichen 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 Prüfungen

`Prüfungen/Startprüfung.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 Startvorgang 및 GRUB ISO Startvorgang.
- Java eigen 시험과 UTF-8 seriellWert wortgruppeWert.
- befehl hilfeAnzeigen·systemInformation·speicherDaten·Ausgabe·fehler Eingabewert·Bildschirm eintragTilgen.
- Aufgabe abschnittWert 8개 speichergerätZuteilen, 부족 prozessWertEintrag, zurückkehrenErgebnis/중복 zurückkehrenErgebnis/재할당.
- seriellWert zeilenumbruch·백스페이스·긴 Eingabewert prozessWertEintrag.
- QEMU PS/2 tasteWert 입력으로 `info` befehlAusführen, `halt` anhaltenAusführung.

erfolgWert 로그는 `build/Startprüfung.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 Prüfungen 도구에 해당 권한이 필요하다. Prüfungen 도중 새로 만든 QEMU만 종료하며 기존 VM과 tatsächlichDaten 디스크는 건드리지 않는다.

`Prüfungen/benutzerNetzwerkPrüfung.py`는 ELF/ISO 각각에서 Benutzer ELF, tatsächlichDaten ring 3, argumente, Wirtssystem 루프백 UDP 왕복, 1,023/1,024바이트 24회 dichtUmschaltenFallliste 왕복, zeitWert 초과, NIC fehlendMethode, speicherDaten/hardwarePort zugriffEintrag 차단, CPU ausnahme, 무한 wiederholungsschrittWert, 잘못된 ELF를 시험한다. `build/benutzerNetzwerkPrüfung.json`에 게스트 기록과 호스트가 받은 데이터의 Länge·해시를 저장한다. `Prüfungen/PaketPrüfung.py`는 tatsächlichDaten Java vertragWert 처리기에 손상된 패킷을 넣어 2,201개 grenzstelleWert/kontrollsumme 조건을 검사한다. Wirtssystem 루프백 외 externWert 서버에는 Prüfungen 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot vorgabe](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 dateiDeskriptor·C ABI·IDE ablegenDatenWert·Java Datei 흐름의 범위와 Deutsch benennung 대응은 [posix-kor Anleitung](../posix-kor/Anleitung.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
