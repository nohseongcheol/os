# jkoros posix-kor

**eigen ARM64 Java 커널용 C++ verbinden**은 [arm64-native](arm64-native/Anleitung.md)에 있다. betriebskernWert 내부 직접 Datei 호출과 EL0 Benutzer 프로그램의 Datei/UDP 루프백 SVC 호출을 별도 라이브러리로 제공한다. unterkanteWert i386 bibliothek 및 ARM64 Linux libc와는 zielobjektWert·ABI가 다르다.

eigen jkoros 커널에서 실행되는 i386 C 라이브러리와 Deutsch API다. Wirtssystem libc를 연결하지 않고 `int 0x80`으로 tatsächlichDaten 커널의 dateiDeskriptor·TerminalEinAusgabe·UDP·ablegenDatenWert 계층을 호출한다. `Kernquelltext/`의 Wirtssystem JVM 모형과 별개다.

**현재는 POSIX의 일부 기능을 제공하는 호환 계층이며, POSIX 인증·전체 libc·전체 OpenJDK를 뜻하지 않는다.** umsetzung 범위와 제한을 아래에 명시한다. 한국어를 먼저 적용했다. 다른 국가·언어의 번역판은 아직 만들지 않았다.

## 빌드와 befehlAusführen

```sh
cd /home/user/jkoros
make posix-kor
make iso
make test-posix
make -C os run-store
```

`run-store`는 `os/build/files.img`ersterOperand 없을 때만 새 전용 파일을 만들고 QEMU IDE ersterElementeintrag 장치로 연결한다. 기존 파일을 덮어써서 초기화하지 않는다. 일반 `make run`은 디스크 없이 실행된다. VirtualBox 실행기의 디스크 연결은 변경하지 않았다.

부팅된 jkoros에서:

```text
run posixcheck check
run posixstore
cat stored.txt
edit note.txt
hello from jkoros
.save
sync
```

`Sync: 0`은 연결된 전용 매체에 저장했다는 뜻이다. 디스크가 없거나 zuweisenWert 형식이 아니면 `Sync: -19`dritterOperand. 같은 `files.img`로 erneutVersuchenWert 부팅하면 letzterElementeintrag synchronisieren 상태를 복원한다. Java 소스와 `.class`도 같은 ablegenDatenWert 대상이다. `close`zweiterOperand 편집기의 `.save`만으로 재부팅 보존을 보장하지 않으므로 verlassenProzessProgramm 전에 `sync`를 실행한다.

## 한국어로 C Programm 작성

```c
#include <DateiABI.h>

int main(int argumenteAnzahl, char **argumentListe) {
    (void)argumenteAnzahl;
    (void)argumentListe;
    int dateiDeskriptor = dateiÖffnen("note.txt", LesenSchreiben | ErstellenFallsFehlend, 0600);
    if (dateiDeskriptor < 0) return fehlerNummer;
    if (dateiDatenSchreiben(dateiDeskriptor, "hello\n", 6) != 6) return 1;
    if (bestätigenDateiSpeichergerät(dateiDeskriptor) < 0) return fehlerNummer;
    return dateiSchließen(dateiDeskriptor);
}
```

작성 원문은 한글을 그대로 유지한다. `Werkzeuge/BezeichnerUmwandlung.py`ersterOperand systemErzeugenAbbild 복사본의 식별자만 C 표준 UCN 표기로 바꾸어 GCC 7에서도 컴파일되게 한다. Zeichenkette, 주석, `#include` 경로는 변환하지 않는다. 이 도구는 C의 모든 vorverarbeitenQuelltext 표기법을 해석하는 전처리기가 아니며, 프로젝트가 사용하는 일반 토큰과 include 문법을 대상으로 한다.

라이브러리는 `build/libposix-kor.a`, ausführenVorgang 코드는 `build/benutzerProgrammStarten.o`, generieren 헤더는 `build/Quelltext/Kopfdateien/`이다. systemErzeugenAbbild 옵션과 verbinden 명령은 [Makefile](Makefile), tatsächlichDaten 예제는 [DateiABIPrüfung.c](Quelltext/Prüfungen/DateiABIPrüfung.c)와 [DatagrammPrüfung.c](Quelltext/Prüfungen/DatagrammPrüfung.c)에 있다. 새 ELF를 OS에 포함하려면 `os/Makefile`의 Benutzer befehlAusführen 묶음에 명시적으로 등록한다. 게스트 안에서 C를 컴파일하는 도구는 제공하지 않는다.

표준 C/POSIX externWert Name `open`, `read`, `write`, `socket`, `errno`, `main`과 헤더 경로는 유지한다. Deutsch 별칭은 같은 함수를 가리킨다. 변수와 umsetzung 파일에는 의미를 드러내는 Deutsch 이름을 사용한다. quelltextÜbersetzenText 근거는 [benennung 원칙](BenennungGrundsätze.md), tatsächlichDaten 대응은 [용어 대응표](fachwortschatzZuordnung.tsv)에 기록했다.

## 제공하는 기능

| beschneiden | umsetzung | aktuellElementeintrag grenzwertWert |
|---|---|---|
| Datei | open/creat/read/write/close/lseek/unlink/ftruncate/fstat/fsync | 루트의 단일 Name, ASCII 63바이트, 8개 Datei, 파일당 16KiB |
| deskriptorEintrag | dup/dup2, F_DUPFD/F_DUPFD_CLOEXEC/F_GETFD/F_SETFD/F_GETFL/F_SETFL | prozessWert einsWert, höchstwertWert 32개; sperreWert·exec 미구현 |
| eingabeAusgabe einstellungen | O_RDONLY/O_WRONLY/O_RDWR/O_CREAT/O_EXCL/O_TRUNC/O_APPEND/O_NONBLOCK/O_CLOEXEC | 그 밖의 비트는 ENOTSUP; tatsächlichDaten Benutzer·그룹 zugriffEintrag erlaubnisWert 검사는 fehlendMethode |
| 표준 TerminalEinAusgabe | 0 lesen, 1·2 schreiben, byteWert einheitWert Eingabewert | terminal bearbeitenWert·termios·시그널 fehlendMethode, HangulText schriftartWert/입력기 fehlendMethode |
| UDP | socket/bind/sendto/recvfrom/getsockname, SO_RCVTIMEO | IPv4 UDP만, 묶인 endpunktWert 4개, 전문당 1,024바이트, wertEmpfangen wertWarten einstellungen höchstwertWert 2초 |
| adresse | htons/ntohs/htonl/ntohl/inet_pton/inet_ntop | IPv4 zifferWert 주소만; DNS/IPv6 fehlendMethode |
| 작은 C unterstützungWert | strlen/strcmp/memcpy/memset/memcmp/puts/putchar | 전체 libc·stdio FILE·malloc fehlendMethode |
| ablegenDatenWert | JKSTORE1 전용 IDE ablegenDatenWert, 두 보존본과 kontrollsumme | FAT/ext DateiSystem·디렉터리·하드 링크·심볼릭 링크 fehlendMethode |
| 게스트 Java | FileInputStream(String).read()/close(), FileOutputStream(String[, boolean]).write(int)/close() | datenfeldWert eingabeAusgabe·일반 java.io·ausnahme prozessWertEintrag fehlendMethode |

`dup`으로 복제한 서술자는 Datei 위치와 fortsetzungAnhängen 설정을 공유한다. `FD_CLOEXEC`는 서술자마다 저장한다. `unlink`는 이름만 제거하며, 열린 파일의 내용은 letzterElementeintrag 참조가 닫힐 때까지 접근할 Zahl 있다. 빈 위치를 건너뛰어 쓰거나 길이를 늘린 영역은 0으로 읽힌다. dateiDeskriptor 부족으로 실패한 `open`은 파일을 생성하거나 비우지 않는다. C aufrufen 실패는 `-1`과 `errno`, 내부 betriebskernWert 호출은 negativWert fehler 번호를 반환한다.

`fstat`는 이 프로젝트 전용 48바이트 구조체에 artWert·größe·링크 Zahl·erlaubnisGewähren bitWert 등을 반환한다. POSIX의 전체 zeitWert 속성은 아직 제공하지 않는다. 다른 운영체제의 `struct stat` 또는 Linux 바이너리 ABI와 호환되지 않는다. `O_CLOEXEC`는 기록할 Zahl 있지만 aktuellElementeintrag exec 기능은 없다. 성공하는 Funktion 이름만으로 전체 POSIX 의미가 구현되었다고 간주하면 안 된다.

UDP는 QEMU RTL8139의 tatsächlichDaten Wirtssystem 왕복을 지원한다. 짧은 wertEmpfangen 버퍼에는 앞부분을 복사하고 restwertWert 전문을 버린다. 빈 전문도 송수신한다. `SO_RCVTIMEO` 또는 비차단 수신의 Daten 없음은 `EAGAIN`이다. TCP를 요청하면 `EPROTONOSUPPORT`를 반환한다. 루프백·브로드캐스트·멀티캐스트·연결형 netzbuchseWert·listen/accept는 아직 없다. 기존 AOT Java UDP 손잡이는 이 POSIX 서술자와 별개이므로 서로 섞어 닫지 않는다.

모든 Benutzer 프로그램에는 기존 약 3초 befehlAusführen 상한이 적용된다. `errno`는 aktuellElementeintrag 단일 prozessWert·단일 스레드 변수다. JDK 전체, Swing/AWT/JavaFX, TCP/DNS/HTTP/TLS, 스레드·GC·JIT·동적 연결은 아직 구현하지 않았다. 전체 Java SE befehlAusführen 환경을 만들려면 해당 betriebskernWert 기반과 런타임 이식을 fortsetzenVerarbeitung 진행하거나 별도 Linux grundlage befehlAusführen 방식을 결정해야 한다.

## ablegenDatenWert 형식과 validieren

매체는 512바이트 abschnittWert 2,048개(1MiB)dritterOperand. abschnittWert 0의 `JKSTORE1` bezeichnerWert·größe·formatWert 번호가 alleErzeugenAbbild 맞는 장치만 schreiben 대상으로 삼는다. abschnittWert 1과 260에서 각각 259구역짜리 보존본이 시작한다. 각 보존본은 istFertig kopfWert 1구역, Datei Tabelle 2구역, Datei Daten 256구역으로 구성된다.

`fsync`와 `sync`는 이름이 남아 있는 모든 파일의 aktuellElementeintrag 상태를 저장한다. 반대편 보존본을 무효화한 rückseiteWert Datei 표와 자료를 쓰고 ATA 캐시 비우기를 실행한다. 마지막에 erzeugungsstufeWert 번호와 FNV-1a 검사합을 가진 istFertig 머리를 기록하고 erneutVersuchenWert 캐시를 비운다. Startvorgang 시 검사합과 표가 유효한 가장 kürzlichWert 세대를 선택한다. 검사합은 우발적인 손상을 eintragFinden 위한 것이며 암호학적 무결성 검증은 아니다. tatsächlichDaten Gerät 전원 차단 시험은 하지 않았다.

복원된 Datei 목록은 Startvorgang 이미지의 standardwertWert Beispiele/`JAVA_FILES` 목록을 대체한다. 새 예제를 이미지에 추가해도 기존 ablegenDatenWert 매체를 연결하면 저장된 목록이 우선한다. 동기화하지 않은 변경은 재부팅 danachStatuswert 사라진다.

`make test-posix`는 Deutsch bezeichnerWert wertUmwandeln, ELF/ISO의 tatsächlichDaten C ABI aufrufen, 공유 position, 삭제된 파일의 수명, Datei/deskriptorEintrag 고갈, zeiger fehler, 표준 Eingabewert, UDP, `fsync`, 재부팅, 손상된 neuesterWert 보존본의 회피, 다른 형식의 medienWert 비변경, 게스트 Java Datei 처리와 OpenJDK 교차 실행을 확인한다. 기록은 `os/build/VertragPrüfung.json`, `Beständigkeitsprüfung.json`, `JavaDateiprüfung.json`이다.
