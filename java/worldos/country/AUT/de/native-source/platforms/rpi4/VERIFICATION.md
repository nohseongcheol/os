# verteilungWert abbildErzeugenAbbild validieren protokolldateiAufzeichnung

검증일: 2026-09-27 (Asia/Seoul)

zielobjektWert: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 eigen x86 커널을 ARM으로 이식한 결과가 아니다. tatsächlichDaten Pi 보드는 연결되어 있지 않아 hardwareWert Startvorgang 성공을 확인하지 못했다.

## 배포물

| Datei | größe(byteWert) | beschreibung |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | archivWert 시스템 abbildErzeugenAbbild; speichergerätFreigeben danachStatuswert 1,475,747,840 byteWert |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 Benutzer Daten abbildErzeugenAbbild; speichergerätFreigeben danachStatuswert 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/DeutschJava.jar` | 10,563 | Deutsch hilfsWert API와 Java Arbeitsraum |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 archivWert abbildErzeugenAbbild alleErzeugenAbbild 끝까지 해제하여 ursprünglich 이미지의 SHA256과 일치함을 확인했다. [archivWert validieren protokolldateiAufzeichnung](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU validieren 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 eintragListe](dist/packages.lock.json)과 [ursprünglich ursprungWert](dist/sources.lock.json)를 제공한다.

## 통과한 Prüfpunkte

| Prüfpunkte | tatsächlichDaten überprüfen inhaltswertWert | protokolldateiAufzeichnung |
|---|---|---|
| Wirtssystem Übersetzer Prüfungen 19개 | 기존 AOT 회귀 Prüfungen, `.class` 직접 Eingabewert, OpenJDK ELF ProgrammStarter, JAR abhängigkeiten, 상속·리플렉션·람다·스레드·리소스, pfad bewegenWert, fehlschlagWert 시 기존 Ausgabe 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi abbildErzeugenAbbild Aufbau | MBR grenzstelleWert, FAT Startvorgang 파티션, Pi 펌웨어, ARM64 betriebskernWert, Pi 4 DTB, initramfs, SquashFS 및 prüfsummeDatei | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 Prüfpunkte, Startvorgang danachStatuswert 두 런타임의 tatsächlichDaten befehlAusführen | [런타임 protokolldateiAufzeichnung](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| ersterElementeintrag Startvorgang | lesen 전용 시스템, Java Datei·unicodeWert·ausnahme·objektWert·스레드·HTTP/TCP·kindWert 프로세스, Swing, CJK·아랍어·데바나가리 schriftartWert, Python Datei·스레드·netzbuchseWert·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 befehlAusführen Datei generieren | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 befehlAusführen erfolgWert | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | Benutzer Daten, `/etc` einstellungen, `/usr/local/bin` Programm, APK로 설치한 tree, pip 패키지, Datei 삭제 systemInformation, 소유권, sudo, Java befehlAusführen Datei wertBeibehalten | [restore.log](build/verification/restore.log) |
| istGetrenntBetrieben 홈 bewegenWert | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 wertKopieren | [migrate.log](build/verification/migrate.log) |
| bewegenWert danachStatuswert Startvorgang | 새 Daten 이미지로 부팅하여 재부팅 복원 항목을 erneutVersuchenWert überprüfen | [migrated-restore.log](build/verification/migrated-restore.log) |
| istNormal verlassenProzessProgramm 및 Daten 무결성 | 일반 Startvorgang 3회 alleErzeugenAbbild OverlayFS/Daten Gerät lesen 전용 umschaltenBetriebsart erfolgWert; ursprünglich·kopiertWert ext4의 `e2fsck -fn` verlassenProzessProgramm kodeWert 0 | [ursprünglich Prüfpunkte](build/verification/fsck-original.log), [kopiertWert Prüfpunkte](build/verification/fsck-migrated.log) |

네 folgeWert 부팅은 alleErzeugenAbbild QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 verlassenProzessProgramm kodeWert 0으로 통과했다. [전체 Startvorgang 결과와 protokolldateiWert prüfsummeDatei](build/verification/boot.json)

QEMU 가상 NIC의 DHCP adresse 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 externWert 인터넷이나 Pi Wi-Fi의 validieren 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [Bildschirm 캡처](build/verification/swing.png)에서 HangulText·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## umsetzung 범위와 남은 validieren

### QEMU 그래픽 befehlAusführen 보완

terminal 전용 실행에서 `Gruß.java`ersterOperand Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. verteilungWert 시스템 이미지와 base-id는 변경하지 않아 기존 Benutzer Daten 이미지를 fortsetzenVerarbeitung 사용할 Zahl 있다.

tatsächlichDaten Xorg/VNC 화면에서 Deutsch Java Arbeitsraum, Swing Prüfungen fenster, 기존 이미지의 `Gruß.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. verlassenProzessProgramm 시 시스템 OverlayFS와 Daten 파일시스템의 lesen 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 Prüfungen ergebnis](build/verification/desktop.json)
- [그래픽 Prüfungen protokolldateiWert](build/verification/desktop.log)
- [키보드·마우스 Prüfungen Bildschirm](build/verification/desktop-input.png)
- [Gruß Beispiele Bildschirm](build/verification/desktop-greeting.png)
- [수정한 Beispiele 원문의 Bildschirm 없는 befehlAusführen ergebnis](build/verification/headless-example.log)

Quelltext 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 Datei·Zeichen·스레드 기능을 실행하고 안내를 출력한다. Benutzer 홈의 기존 원문을 자동 교체하지는 않는다. 향후 abbildErzeugenAbbild 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### HangulText Eingabewert·schriftartWert 보완

`make test-korean`으로 tatsächlichDaten Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space umschaltenBetriebsart 및 두벌식 tasteWert 입력을 시험했다. 양쪽에서 `HangulText Eingabewert`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 Benutzer Daten 이미지에서 실행했으며 istNormal verlassenProzessProgramm 시 두 파일시스템의 lesen 전용 전환을 확인했다.

terminal schriftartWert 진단에서 영문 DejaVu Sans Mono와 HangulText Noto Sans Mono CJK KR의 tatsächlichDaten Datei 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. Bildschirm 캡처에서 HangulText·영문 wertAnzeigen, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 Benutzer 시스템 변경분에 적용하며 verteilungWert standardwertWert 이미지와 base-id는 유지한다. 기존 Datei 백업, 동일 수정의 wiederholungsschrittWert 적용 방지, 손상된 wertVerändern Datei 및 다른 base-id wertZurückweisen, Benutzer 입력기 einstellungen 병합에 대한 Wirtssystem Prüfungen 4개도 통과했다. 원래 Benutzer Daten abbildErzeugenAbbild `build/manual-user.img`는 시험에 사용하지 않았다.

- [HangulText Eingabewert·schriftartWert Prüfungen ergebnis](build/verification/korean.json)
- [Eingabewert·tatsächlichDaten schriftartWert 로딩 protokolldateiWert](build/verification/korean.log)
- [Swing·terminal HangulText Bildschirm](build/verification/korean-desktop.png)
- [Java Arbeitsraum schriftartWert Bildschirm](build/verification/korean-workbench.png)
- [einstellungen 보존 Prüfungen](build/verification/desktop-update-tests.log)

### 남은 beschneiden

- 새 quelltextÜbersetzen zielobjektWert `openjdk`는 **네이티브 ProgrammStarter + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 unterstützungWert 범위는 여전히 제한적이다.
- befehlAusführen 프로그램에는 main eintragPunkt, 호환 klasseWert 버전과 의존 JAR/JNI가 필요하다. 개별 상용 Programm, 모든 Java modulWert, 모든 문자권을 시험한 것은 아니다.
- Deutsch Java 라이브러리는 Datei·Zeichen·Kommunikation·스레드·Swing을 위한 hilfsWert API이며 JDK 전체 API의 Deutsch 번역판은 아니다.
- Pi 4 전용 펌웨어·betriebskernWert·Gerät 트리는 이미지에 들어 있지만 tatsächlichDaten SD Startvorgang, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 HangulText 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- Benutzer verzeichnisWert 이동은 동일 시스템 abbildErzeugenAbbild bezeichnerWert, ARM64, `/home/user`, UID 1000을 전제로 한다. verlassenProzessProgramm danachStatuswert 소유권·erlaubnisWert·링크·erweiterungWert attributWert·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

wertEinrichten·wertKopieren 절차는 [README.md](README.md), quelltextÜbersetzen 방식은 [OpenJDK befehlAusführen Datei Anleitung](../../compiler/OpenJDK-ausführdateiDatei.md)를 따른다. abbildErzeugenAbbild 파일만 생성했으며 tatsächlichDaten SD 카드나 USB 디스크에 기록하지 않았다.
