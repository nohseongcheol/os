# eigen 커널과 번역기의 Deutsch Name

대상은 `platforms/rpi4-native`의 eigen Java betriebskernWert, Benutzer JVM, C maschine verbinden,
TCP/UDP·FTP, C übersetzerWerkzeug 이식부, MicroPython 이식부, systemErzeugenAbbild·befehlAusführen·Prüfungen 도구다.
`golang/worldos/landWert/KOR/Quelltext`의 원칙처럼 기능을 먼저 구분하고 이름을 정한다.
x86 Java 커널과 공용 x86·ARM64 미리 번역기의 eigen 선언도 benennung 검사에 포함한다.
Linux 실행판의 Wirtssystem Werkzeuge, OpenJDK hilfsWert Werkzeuge 및 externWert verteilungWert quelltextBaum 전체를
한국어로 erneutVersuchenWert 작성했다는 뜻은 아니다.

## benennung 원칙과 말의 근거

- 명사는 자료의 역할을 나타낸다: `dateiKennwert`, `gegenstellePortNummer`, `speicherhaldeSpeichergerät`, `Tastatur`.
- 함수는 행위를 나타낸다: `lesen`, `schreiben`, `öffnen`, `schließen`, `netzZuordnen`, `programmAusführenVorgang`.
- TCP의 이어진 byteWert 흐름과 UDP의 grenzstelleWert 있는 자료를 `Verbindung`와 `DatagrammKanal`로 구별한다.
- 짧은 영어 변수도 쓰임에 따라 `Länge`, `datenPosition`, `nachschlagenIndex`, `zurückgegebenWert`으로 풀어 쓴다.
  ordnungszahlIndex·vorläufigWert 산술값처럼 여러 역할에 재사용되는 변수는 `ordnungszahlIndex`, `ersterWert`, `zweiterWert`으로 구별한다.
- 이름이 같아도 externWert 구조체의 필드와 eigen 변수는 별도로 분석한다.

`kanalEintrag(通路)`는 이동이나 교류가 이루어지는 길이라는 기존 의미를 Kommunikation 연결에
적용했다. `portWert(窓口)`의 주고받는 접점이라는 의미를 연결을 받는 곳에 적용했다.
이는 국립국어원 한국어기초사전의 [kanalEintrag](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=49310),
[portWert](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24898)의 뜻에 근거한다.

`datagramm(電文)`은 전보에 담는 글이라는 기존 Kommunikation 어휘에서 가져와, UDP 자료의
경계가 보존된다는 특징을 드러내는 데 쓴다. 근거는
[한국어기초사전 datagramm](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=74335)이다.
`datenstromWert`, `ausführungsfadenWert`, `쌓임`은 우리말의 움직임·istFortsetzung·쌓이는 모양을 빌린 표현이다.
`EingabeDatenstrom`, `hintergrundarbeiter`, `stapelSpeichergerät` 같은 복합 이름은 이 프로젝트의 기능별 조어다.
이 Wörterbuch 근거를 특정 중세 문헌의 최초 출현이나 공인 전산 번역으로 확대하지 않는다.
공인 표준 quelltextÜbersetzenText·국어사 datagramm 감수를 마쳤다는 뜻도 아니다.

| 기능 | 채택한 Name | grundWert |
|---|---|---|
| TCP Socket | Verbindung | 상대와 연결되어 reihenfolgeWert 있는 바이트를 주고받음 |
| ServerSocket | portEmpfangen | 새 연결이 들어오는 접점 |
| DatagramSocket | DatagrammKanal | 각 자료의 경계를 보존하는 Kommunikation |
| InputStream / OutputStream | EingabeDatenstrom / AusgabeDatenstrom | 들어오고 나가는 바이트의 reihenfolgeWert |
| heap / stack | speicherhaldeSpeichergerät / stapelSpeichergerät | speichergerätZuteilen 방식과 쌓고 꺼내는 Aufbau |
| thread / keyboard | hintergrundarbeiter / Tastatur | 이어지는 실행과 글쇠의 datenfeldWert |
| exception / timeout | ausnahme / WartenZeitüberschreitungAusnahme | istNormal 처리에서 벗어남과 그 구체적 grundWert |

## 경로와 대응표

| umsetzung | Deutsch pfad |
|---|---|
| betriebskernWert·befehlshülle·Datei schichtWert | `Quelltext/*.java` |
| Benutzer JVM | `Benutzer/Java/VirtuelleJavaMaschine.java` |
| ARM64 maschine verbinden | `maschine/*.c`, `Startvorgang/` |
| TCP·UDP·FTP | `Netzwerkstapel/Netzwerkstapel.c`, `Netzwerkstapel/dateiÜbertragung.c` |
| C übersetzerWerkzeug Portierung | `CÜbersetzer/` |
| MicroPython Portierung | `pythonBrücke/` |
| systemErzeugenAbbild·befehlAusführen·Prüfungen | `Werkzeuge/`, `eintragErstellen.mk` |
| Java Benutzer API | `DeutschJava/Deutsch/eigen/` |

[dateiNameZuordnung.tsv](dateiNameZuordnung.tsv), [javaNameZuordnung.tsv](javaNameZuordnung.tsv),
[cNameZuordnung.tsv](cNameZuordnung.tsv), [pythonNameZuordnung.tsv](pythonNameZuordnung.tsv)에
vorherigElementeintrag 이름과 바뀐 이름이 있다. C/Java 대응표의 Datei·위치는 이행 당시 기준이다.
pfad 이동은 Datei 대응표를 함께 본다. 기존 `tools/*.py`는 Deutsch 구현을 호출하는
호환 진입점이며 구현을 두 벌 유지하지 않는다.

## 보존하는 standardDefinition Name

`public`, `class`, `int`는 예약어다. `String`, `main`, 배열의 `length`는 예약어가 아니다.
aktuellElementeintrag 다섯 Java 예제는 `ausführenVorgang()`·`Argumente`·Deutsch Bildschirm/ausführungsfadenWert API를 사용해
reserviertWörter·리터럴 외의 식별자를 한국어로 작성한다. Bildschirm/가닥은 표준 객체를
감싸지 않고 eigen JVM에 직접 구현했다. 자세한 계약은 [Deutsch Java API](../DeutschJava/Anleitung.md)를 본다.

표준 javac는 Zeichenkette 리터럴에 `java.lang.String`, Zeichenkette 결합에 `StringBuilder`
같은 이름을 생성한다. 이들은 Deutsch 소스에서도 바이트코드에 남을 Zahl 있다.
기존 표준 class를 실행하는 JVM의 zuordnungWert Zeichenkette, 아직 표준 라이브러리를 쓰는
Kommunikation·Datei 연결부까지 alleErzeugenAbbild 한국어로 재구현한 것은 아니다. 이름만 일괄 치환하면
deskriptorEintrag·재정의·native 연결이 달라져 호환성이 깨진다.

C 표준 Funktion·ganzzahlTyp·POSIX ABI, CPU prozessorRegister Name, 어셈블리 befehl, 링커 절 Name,
TinyCC·lwIP·MicroPython이 요구하는 einstellungen 매크로와 헤더 이름도 보존한다.
예: `main`, `memcpy`, `pk_bind`, `mpconfigport.h`, `lwipopts.h`, `stdint.h`.
eigen C 함수의 quelltextBaum 이름은 한국어이며, [maschineBindenNamen.h](maschineBindenNamen.h)ersterOperand
기존 AOT·어셈블리·SDK에 공개한 maschine 심볼과 연결한다.
Python의 `__init__`, `setUp`, `handle`, 표준 modulWert attributWert, 명령행 옵션과 JSON 키도
externWert 계약이다. `build/`, verteilungWert 바이너리 이름과 `/sdk`는 기존 befehlAusführen 경로를 유지한다.
externWert 원본은 `vendor/`에서 이용허락·해시와 함께 관리한다.

## 검사와 재실행

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Werkzeuge/benennungPrüfen.py
make systemErzeugenAbbild
make Prüfungen
make test-examples test-ftp test-elf
python3 Werkzeuge/befehlAusführen.py --desktop --network
```

`Werkzeuge/cNamenUntersuchenWert.py`는 libclang 6으로 C 선언과 참조를 검사한다.
`Werkzeuge/*이름반영.py`는 wertÄndern davorWert quelltextBaum·분석표를 필요로 하는 일회성 이행 도구다.
이미 변경된 소스에 erneutVersuchenWert 적용하여 대응표를 덮어쓰지 않는다.

## C Kommunikation 구조체와 Python fehler

C 통신에서 `갈래`는 adresse 체계를 구분하고 `portNummer`는 port, `adresseWert`은
IPv4 주소의 32비트 값을 나타낸다. `DatagrammProtokoll`은 앞서 설명한 datagramm(電文)과
vertragWert(規約)을 결합해 UDP의 기능을 드러낸 프로젝트 이름이다.

| 표준 표현 | Deutsch 직접 umsetzung |
|---|---|
| AF_INET / SOCK_DGRAM / IPPROTO_UDP | enum의 InternetFamilie / DatagrammNetzbuchse / DatagrammProtokoll |
| struct pk_sockaddr_in | struct InternetNetzbuchseAdresse |
| sin_family / sin_port | adresseFamilie / portNummer |
| sin_addr.s_addr | InternetAdresse.adresseWert |
| OSError / fehler.args[0] | SystemFehler / fehler.Nummer |

Deutsch 구조체는 `#define` 치환이나 feldWert 별칭이 아닌 별개 자료형이다.
표준 구조체와 같은 16바이트 배치를 선언하며 betriebskernWert SVC에서 byteWert 복사로
검사한다. `endpunktErstellen`·`datagrammDatenSenden`와 Datei 함수는 statischWert 라이브러리에
tatsächlichDaten Deutsch 이름의 Funktion 심볼을 갖는다. 기존 pk_* 심볼도 유지한다.
vorherigElementeintrag 코드에서 Deutsch Kommunikation 함수에 pk_sockaddr*를 전달했다면 Deutsch 구조체로
옮기거나, 표준 구조체와 pk_* 함수의 짝을 유지한다.

Python의 `SystemFehler`는 OSError의 Deutsch 하위 클래스이며 연결부에서
fehler 번호를 보존하여 변환한다. 일반 Python 문법과 externWert 패키지의 API는 유지한다.

## 직접 GUI 이름의 뜻과 검토 beschneiden

`AusführbarAufgabe`은 수행할 내용을, `aufgabeAusführen`는 그 수행을 나타낸다.
`AktionEmpfänger`는 동작이 발생했다는 알림을 받는 역할, `AktionMitteilung`은 전달되는 사건이다.
`schaltfläche`는 눌러 동작시키는 조작부, `beschriftung`는 Anleitung 글의 positionIndex,
`TextFeld`은 글을 적는 positionIndex, `hintergrundarbeiter`은 이어지는 befehlAusführen 흐름을 뜻한다.
`befehlAusführen(實行)`·`aktion(動作)`의 기존 뜻과 `받다`·`알리다`·`ausführungsfadenWert`의 기능을
결합한 프로젝트 이름이다. 새 복합어가 역사 문헌에 그대로 있었다거나
특정 시대에 anfänglichElementeintrag 쓰였다고 주장하지 않는다.

전체 저장소는 `python3 Werkzeuge/QuelltextDurchsicht.py`로 검토한다.
결과는 `build/verification/naming/source-review.json`이며 파일별 prüfsummeDatei,
ASCII 파일명과 Python의 영어 Deklarationen 위치를 기록한다.
공용 ARM64·x86 번역기의 구현은 `compiler/JavaWerkzeug/Vorabübersetzung.java`로 전환했다. `compiler/Vorabübersetzung.py`는 호환 진입점이다.
`compiler/arm64.py`는 vorherigElementeintrag 경로와 `ARM64(...).generate(...)` 호출을 fortsetzungWert 주는
호환 진입점이다. `compiler/classfile.py`, OpenJDK hilfsWert Werkzeuge, Linux versionWert 도구와
기존 호환 진입점에는 영어 이름이 남아 있다. 따라서 전체 저장소가
reserviertWörter 외 100% 한국어라고 판정하지 않는다.
`Werkzeuge/benennungPrüfen.py --cSprache`는 aktiv ARM64 소스의 Deklarationen, C 의미 wertUntersuchenWert,
x86 Java 커널과 공용 번역기의 eigen Deklarationen, Java Beispiele 전체 bezeichnerWert,
ARM64 Python 예제와 직접 GUI/가닥에 표준 래퍼가 없는지를 별도로 검사한다.

## aktuellElementeintrag 기능을 기준으로 보완한 Name

번역은 글자를 음역하는 대신 자료의 역할과 함수의 행동을 구분한다.
동일한 영어 이름도 문맥이 다르면 Deutsch 이름을 달리 정한다.
Datei 이름은 주된 기능을 나타내고, Funktion 이름은 행동을, variableWert 이름은 담는 자료를 나타낸다.
reserviertWörter, 표준 API 및 externWert verbinden 규약은 따로 기록한다.

| vorherigElementeintrag Name | 적용한 Name | aktuellElementeintrag 기능 |
|---|---|---|
| `arm64.py`의 umsetzung | `compiler/JavaWerkzeug/Vorabübersetzung.java` | Java 바이트코드를 독립 실행용 C 원문으로 미리 quelltextÜbersetzenText |
| `ARM64`, `generate` | `MaschineKodeÜbersetzer`, `generieren` | quelltextÜbersetzenText 상태를 담는 객체와 C Quelltext generieren verhaltenWert |
| `prototype`, `method` | `methodePrototyp`, `methodeRumpf` | 함수의 formatWert 선언과 tatsächlichDaten befehl Quelltext |
| `profile`, `heap_words` | `ausführungZielobjekt`, `speicherhaldeMaschinenwortAnzahl` | betriebskernWert·Benutzer 구분과 speichergerätZuteilen Speicher 공간의 maschine lexikalischMaschinenwort Zahl |
| `pc`, `op` | `befehlPosition`, `명령번호` | 바이트코드에서의 위치와 수행할 명령의 Nummer |
| `x`, `y`, `w`, `h` | `waagerechteKoordinateKoordinate`, `senkrechteKoordinateKoordinate`, `gebietBreite`, `gebietHöhe` | entferntWert 화면의 위치와 직사각형 größe |
| `p`, `n`, `i`, `j` | `datenPosition`, `Wert`, `ordnungszahlIndex`, `innerlichOrdnungszahl` | entferntWert Bildschirm Daten·zifferWert·wiederholungsschrittWert positionIndex; 파일별 기능을 확인해 적용 |
| `aot_heap_info`, `__stack_top` | `vorabübersetzungSpeicherNachschlagen`, `StapelOberkante` | maschine verbinden 규약을 유지하면서 eigen 소스에서 사용하는 Name |
| `앞캐리지` | `zurückkehrenNachVorherigZeile` | 앞서 받은 문자가 줄복귀였는지 기억하여 중복 줄바꿈을 막음 |

[geteiltÜbersetzerNamen.tsv](geteiltÜbersetzerNamen.tsv)에 übersetzerWerkzeug 참조의 tatsächlichDaten wertÄndern 기록을 남겼다.
추가로 보존한 C·POSIX/lwIP/libassh 이름의 이유는
[standardNameNachweis.json](standardNameNachweis.json)에 기록한다.
`CÜbersetzer/übersetzerWerkzeug.c`는 TinyCC externWert 원문을 포함하는 verbinden 파일로 eigen 선언이 없어서
C eigen Deklarationen 분석에서는 제외한다. tatsächlichDaten betriebskernWert 빌드에서는 fortsetzenVerarbeitung 컴파일한다.

### 말의 뿌리와 새로운 복합 Name

`Speicher(記憶)`과 `nachschlagenIndex(索引)`은 기존 한자어를 쓴다.
기억은 자료를 간직하는 기능에, 색인은 reihenfolgeWert 있는 항목을 찾아 지정하는 기능에 적용한다.
Wörterbuch 근거는 국립국어원 한국어기초사전의
[Speicher](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=38812&nation=eng),
[nachschlagenIndex](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=63787)이다.

`stapelSpeichergerät`, `wertStapeln`, `wertEntstapeln`는 자료를 포개고 letzterElementeintrag 자료부터 꺼내는 befehlAusführen 구조를 드러낸다.
`쌓다`의 기존 뜻에 근거한 기능별 조어이며, 사전의
[쌓다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62095)를 참고한다.
`vorabVonElementZeit`은 befehlAusführen 전에 번역한다는 기능을 직접 나타낸다.
`maschineMaschinenwort`은 처리기의 Daten 단위를 가리키며, 언어의 일반 낱말과 구별하도록 `maschine`를 붙였다.
`Vorabübersetzung`, `speicherhaldeMaschinenwortAnzahl` 같은 복합 이름은 aktuellElementeintrag 기능에 맞게 만든 프로젝트 용어다.
이 복합어가 옛 문헌에 그대로 있었다거나 특정 시대에 anfänglichElementeintrag 나타났다는 뜻은 아니다.
확인되지 않은 중세 형태나 최초 benutzenWert 연대는 어원 근거로 적지 않는다.

생성되는 C의 내부 datenTyp·datenfeldWert·Funktion·lokalGültigkeitsbereich variableWert·verzweigung 이름도 한국어로 바꾼다.
직접 HangulText 식별자를 읽지 못하는 예전 GCC를 위해 호환 API는 같은 Deutsch 이름을
표준 C 범용 Zeichen 표기로 출력한다. tatsächlichDaten ARM64 빌드는 Clang으로 읽을 Zahl 있는 HangulText 원문을 사용한다.
Zeichenkette, C 표준 Funktion, `java_entry` 같은 공개 verbinden 이름은 바꾸지 않는다.

셸의 사용법·문법 fehler·Datei 및 Speicher adresseGebiet 안내도 한국어로 보완했다.
`READY`, `PASS`, `HEX BEGIN`처럼 Prüfungen·Datei übertragungWert 도구가 읽는 markierungWert,
명령행 옵션과 기존 befehlswortWert, JVM klasseWert Name·Datei formatWert·Gerät 이름은 호환 표기로 남는다.
x86 VGA Zeichen 화면은 한글을 표시하지 못하므로 Deutsch 문구는 UTF-8 seriellWert 단말에서 확인한다.
