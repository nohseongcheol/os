# JUsaOS

aktuellElementeintrag eigen ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, verteilungWert 시 quelltextBaum·neuverbindenEndpunkt 자료를 포함하는 절차는 [COSL verteilungWert Anleitung](platforms/rpi4-native/COSLVerteilungLeitfaden.md)에 있다.

eigen ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 Deutsch 명령은 [네트워크·betriebSystemWert befehl Anleitung](platforms/rpi4-native/NetzwerkUndSystemBefehle.md)를 참고한다. 새 커널을 부팅한 rückseiteWert `help system`으로 볼 Zahl 있다.

Raspberry Pi 4 **eigen Java ARM64 betriebskernWert**은 [eigen Pi4 Anleitung](platforms/rpi4-native/Anleitung.md)에 있다. Linux 없이 부팅하며 GUI terminal·vi, eigen JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [Deutsch Java Kommunikation·ausnahme API](platforms/rpi4-native/DeutschJava/Anleitung.md)와 [Deutsch quelltextBaum benennung](platforms/rpi4-native/benennung/Anleitung.md)을 지원한다. [eigen SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/ExternVerbindungLeitfaden.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. tatsächlichDaten Pi 4 GENET 동작은 미검증이고, USB Eingabewert·영속 저장과 전체 OpenJDK·Swing은 아직 unterstützungWert beschneiden 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 Benutzer umgebung bewegenWert 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. tatsächlichDaten ARM64 JDK/JRE와 시스템·Benutzer abbildErzeugenAbbild systemErzeugenAbbild 경로를 제공한다. 기존 eigen x86 커널과는 별도 befehlAusführen 기반이다. 일반 Java `.class`/JAR의 befehlAusführen Datei 생성은 [OpenJDK befehlAusführen Datei](compiler/OpenJDK-ausführdateiDatei.md), Deutsch API는 [Deutsch Java bibliothek](DeutschJava/Anleitung.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java Funktion, variableWert, formatWert 및 Java Datei 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 bibliothek formatWert, x86 부트 ABI 등 externWert 계약은 보존한다. eigen ARM64 실행기는 Deutsch `ausführenVorgang()`도 진입점으로 지원하며, Deutsch GUI·Aufgabe 가닥을 JVM에 직접 구현했다. eigen ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 eigen 이름도 한국어로 작성한다. vorherigElementeintrag 경로의 호환 eintragPunkt, OpenJDK hilfsWert 도구와 Linux versionWert 도구에는 영어 이름이 남아 있고 [benennung 원칙·말의 근거·전체 Quelltext 검토 beschneiden](platforms/rpi4-native/benennung/Anleitung.md)를 별도로 기록한다.

## aktuellElementeintrag umsetzung

unterkanteWert 목록은 기존 `Kernquelltext/`의 JVM 관리 커널에 대한 것이다. tatsächlichDaten 네이티브 커널의 범위는 `os/Anleitung.md`에서 별도로 설명한다.

- ausrichtenWert 할당과 해제를 지원하는 Speicherraum verwalterWert
- adresse adresseGebiet, seiteWert verbinden, schreiben 시 wertKopieren(COW)
- prozessWert bezeichnerWert, vorbereiten 대기열, fork/wait statuswertWert
- 과정별 Datei deskriptorEintrag, open/read/seek/dup/close
- ELF32 wertIdentifizieren 및 abschnittWert Prüfpunkte
- 키보드·마우스 Eingabewert ereignis 대기열
- seriellWert 단말과 네이티브 hardwareWert grenzstelleWert
- 관리 betriebskernWert 전체 자동 Prüfungen

세부 zuordnungWert 범위와 아직 필요한 네이티브 연결은 [기능 대응표](Dokumentation/Funktionszuordnung.md)에 기록한다.

## 빌드와 Prüfungen

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `Kernquelltext/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 berechnung Beispiele + Java betriebskernWert ELF
make iso             # os/build/kernel.iso
make run             # QEMU seriellWert TerminalEinAusgabe; help Eingabewert (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU Bildschirm/PS2 키보드로 befehlAusführen
make vbox            # 전용 VirtualBox VM 자동 generieren·befehlAusführen (GUI)
make vbox-status     # VirtualBox statuswertWert·ISO·seriellWert protokolldateiAufzeichnung pfad überprüfen
make test-vbox       # VirtualBox ProgrammStarter statuswertWert prozessWertEintrag Prüfungen (tatsächlichDaten VM wertÄndern fehlendMethode)
make test            # Übersetzer Prüfungen + ELF/ISO Startvorgang 및 befehl Eingabewert Prüfungen
make apps            # 독립 Benutzer ELF Programm systemErzeugenAbbild
make test-network    # Benutzer betriebsartWert·UDP 왕복·speicherDaten wertSchützen Prüfungen
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 befehlAusführen Prüfungen
make posix-kor       # Deutsch C 헤더와 tatsächlichDaten betriebskernWert aufrufen bibliothek
make test-posix      # Datei/UDP/ablegenDatenWert/Java Datei eingabeAusgabe Prüfungen
make -C os run-store # 전용 ablegenDatenWert 매체로 QEMU Startvorgang
make legacy-test     # unterkanteWert 기존 JVM 관리 커널의 47개 Prüfungen
```

`compiler/`는 호스트의 `javac`를 문법·typWert Prüfpunkte 전단으로 사용하고 eigen bytecode→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 externWert JVM 없이 실행된다. 전체 Java, objektWert 모델, 표준 라이브러리와 기존 관리 betriebskernWert 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 unterstützungWert 문법과 명령은 [Übersetzer Anleitung](compiler/Anleitung.md), tatsächlichDaten Startvorgang 기능과 한계는 [네이티브 Betriebssystem Anleitung](os/Anleitung.md)를 참고한다.

네이티브 셸에 eigen 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 rückseiteWert `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 befehlAusführen**할 Zahl 있다. standardwertWert 예제는 `javac Hello.java`, `java Hello`dritterOperand. 파일은 RAM에서 동작하며, 전용 ablegenDatenWert 매체를 연결하면 `sync`로 재부팅 후에도 보존할 Zahl 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 klasseWert·statischWert Funktion·Ganzzahl·Zeichenkette·bedingung/반복문과 일부 표준 호출을 지원한다. unterstützungWert beschneiden, externWert Datei 적재와 시험은 [Java entwicklung umgebung Anleitung](Dokumentation/JavaEntwicklungsumgebung.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 Zahl 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 Ausgabe·argumente·UDP 네트워크를 제공한다. 별도 Wirtssystem 터미널에서 `python3 os/Werkzeuge/DatenWiederherstellen.py --port 9000`을 실행한 rückseiteWert 게스트에서 `run udp 10.0.2.2 9000 hello`로 tatsächlichDaten 왕복을 확인한다. 새 Programm eintragRegister, API 및 제한은 [Benutzer befehlAusführen·네트워크 Anleitung](os/Benutzer/Anleitung.md)를 참고한다. aktuellElementeintrag QEMU RTL8139·statischWert IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE ablegenDatenWert 형식과 POSIX Datei/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. befehlAusführen 중이면 유지하고, ablegenDatenWert·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 Benutzer Programm 실행을 확인했다. 다만 aktuellElementeintrag VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 systemErzeugenAbbild 반영 방법은 [VirtualBox befehlAusführen Anleitung](Dokumentation/VirtualBoxStarten.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f eintragErstellen.mk Prüfpunkte
make -f eintragErstellen.mk Wirtssystem
```

`Wirtssystem`는 여전히 JVM 관리 계층의 aktion 시험이다. `make -f eintragErstellen.mk abbildErzeugenAbbild`는 새 `os/`의 제한형 네이티브 betriebskernWert ISO를 만든다. 기존 `Kernquelltext/`의 DateiSystem·prozessWert·Netzwerkstapel umsetzung 전체를 이 ISO에 이식했다는 의미는 아니다.

Deutsch Funktion·variableWert·Datei 이름과 tatsächlichDaten C API는 [posix-kor](posix-kor/Anleitung.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 byteWert 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

externWert 배포용 `pack.sh` / `unpack.sh`와 자동 abhängigkeiten 복원은 [verteilungWert Anleitung](distribution/README.md)를 참고하세요.
