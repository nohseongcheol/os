# Java 네이티브 Übersetzer

OpenJDK eigen 소스를 빌드하는 **`--target openjdk-build`**와 eigen betriebskernWert ABI Prüfpunkte 도구를 추가했다.
이는 공식 javac/C/C++ 도구를 연결하는 별도 경로다. [systemErzeugenAbbild 방법·tatsächlichDaten validieren·betriebskernWert Portierung beschneiden](OpenJDK-QuelltextErzeugenAbbildUnd-SystemnahBetriebskern-Portierung.md)를 참고한다.

x86 직접 변환과 ARM64 C generieren 후단은 alleErzeugenAbbild [Vorabübersetzung.java](JavaWerkzeug/Vorabübersetzung.java)로 구현한다. `sh vorabVonElementZeit.sh`로 직접 실행하며, [Vorabübersetzung.py](Vorabübersetzung.py)와 `Übersetzer.py`는 vorherigElementeintrag befehl·API 및 OpenJDK 도구를 위한 호환 진입점이다. eigen Pi4 후단은 freestanding C를 거쳐 AArch64로 만든다. [arm64.py](arm64.py)는 vorherigElementeintrag 경로와 Python 호출을 위한 호환 진입점이다. Funktion·variableWert·generieren C 이름의 뜻과 예외는 [Deutsch benennung Anleitung](../platforms/rpi4-native/benennung/Anleitung.md)를 참고한다. [ARM64 systemErzeugenAbbild·unterstützungWert beschneiden](../platforms/rpi4-native/Anleitung.md)에 befehlAusführen 조건이 있다. 전체 OpenJDK나 일반 klasseWert 실행기는 아니다.

befehlAusführen 시 JVM이 benötigtWert 없는 x86 32비트 ELF를 만든다. JDK 11 이상으로 실행하는 Java eigen AOT 후단이며, Java 전체를 새로 구현한 컴파일러는 아니다. Java 문법·zugriffEintrag steuerungWert·typWert 검사는 JDK의 `javac`에 맡기고, Java 8 klasseWert 파일을 읽어 각 바이트코드를 x86 명령으로 직접 변환한다. C 코드로 우회하거나 bytecode 해석기를 커널에 넣지 않는다.

```text
Java Quelltext → javac의 문법·typWert Prüfpunkte → vorläufigWert .class
          → eigen x86 변환기 → GNU as/ld → 네이티브 ELF32
```

## 준비와 befehlAusführen

systemErzeugenAbbild Wirtssystem: Linux, Python 3.6 이상, JDK 11 이상(`javac --release 8`), GNU binutils(`as`, `ld`), Make. aktuellElementeintrag 환경의 OpenJDK 11, Python 3.6, binutils 2.30으로 검증했다. externWert Python 패키지와 네트워크 다운로드는 사용하지 않는다.

```sh
cd /home/user/jkoros/compiler
make
./build/berechnung
echo $?                  # 0이면 Beispiele Prüfungen erfolgWert

python3 Übersetzer.py --target linux --entry berechnung.ausführenVorgang \
    -o build/berechnung Beispiele/berechnung.java

make test
```

`linux` 대상은 Linux의 32비트 befehlAusführen 호환 기능이 필요하다. `int 0x80`을 차단하는 샌드박스에서는 `Bad system call`이 발생할 Zahl 있다. istNormal Linux Wirtssystem 또는 해당 실행을 허용한 Prüfungen 환경에서 실행한다. 시험의 비정상 종료를 통과로 처리하지 않는다.

진입점은 `static int ausführenVorgang()` 또는 `static void ausführenVorgang()`처럼 인수가 없어야 한다. `--entry 패키지.klasseWert.Funktion`로 선택한다. `int` 반환값은 Linux 프로세스 verlassenProzessProgramm 코드가 되며 셸에는 하위 8비트가 보인다. 일반 `main(String[] args)` befehlAusführen 환경이나 표준 eingabeAusgabe 라이브러리는 제공하지 않는다.

`--target kernel`은 Startvorgang 코드와 연결할 재배치 ELF 오브젝트를 생성한다.

```sh
cd /home/user/jkoros
python3 compiler/Übersetzer.py --target kernel --entry Betriebskern.ausführenVorgang \
    --export kernel_dispatch=Systemaufruf.prozessWertEintrag \
    -o os/build/java.o os/Quelltext/*.java
```

`--target user`는 jkoros 셸에서 실행할 독립 ELF를 생성한다. `Benutzer` 클래스의 제한된 native API는 `int 0x80` 시스템 호출로 연결하며 `Gerät` 클래스의 hardwareWert 직접 접근은 거부한다. Benutzer ELF는 Linux befehlAusführen Datei ABI와 다르므로 호스트에서 실행하지 않는다. generieren·eintragRegister 방법은 [Benutzer befehlAusführen Anleitung](../os/Benutzer/Anleitung.md)에 있다. `--export 외부기호=klasseWert.Funktion`는 오버로드되지 않은 statischWert 함수를 eigen operandStapel ABI로 노출한다. 커널의 시스템 aufrufen 진입점에 사용한다.

Java 파일은 필요한 클래스들을 한꺼번에 전달한다. Ausgabe 옆의 `.s`는 생성된 어셈블리, `.json`은 Quelltext SHA-256 및 네이티브 symbol↔Java Funktion 대응표다. Deutsch 함수명은 원문과 대응표에 보존하고 ELF 내부에는 충돌 방지용 maschine 기호를 쓴다. quelltextÜbersetzen·wertZusammenbauen·verbinden 중 실패하면 기존 ergebnis 파일을 덮어쓰지 않는다.

## unterstützungWert beschneiden

- `int`, `boolean`, `byte`, `short`, `char`의 32비트 berechnung 및 typWert wertUmwandeln.
- statischWert 필드와 statischWert Funktion, 매개변수·zurückgegebenWert, 재귀, 클래스별 지연 초기화와 initialisieren zyklusWert.
- 조건문, 반복문, 단락 평가, 삼항식, Ganzzahl `switch`, 넓은 lokalGültigkeitsbereich variableWert 인덱스.
- additionErgebnis·subtraktionErgebnis·곱셈·나눗셈·restwertWert·bitWert 연산과 bewegenWert. Java의 오버플로 및 `MIN_VALUE / -1` 동작을 유지한다.
- `int[]` generieren·anfänglichWert 0·Länge·lesen·schreiben·verweis 비교. 256KiB 고정 datenfeldWert gebietWert, 널/feldindexWert/größe/adresseGebiet Prüfpunkte.
- Zeichenkette 리터럴과 `String` verweis, `length()` 및 `charAt()`. 문자열은 UTF-16 kodeWert 단위로 저장하고 같은 리터럴은 공유한다. NUL 및 대리쌍도 시험한다.
- Deutsch klasseWert·Funktion·variableWert·Datei Name.

`new Object`, 인스턴스 feldWert/Funktion, 상속/인터페이스, `long/float/double` befehlAusführen vorgangWert, `int[]` 이외 datenfeldWert, Zeichenkette 동적 zusammenfügenWerte, Java 표준 bibliothek, ausnahme prozessWertEintrag, 스레드·synchronisieren·GC는 미지원이다. 실행에 필요한 istNichtUnterstützt 바이트코드나 externWert 호출을 발견하면 실패한다. 사용되지 않는 standardwertWert 생성자는 befehlAusführen 코드로 만들지 않는다. Java 8 문법이어도 모든 프로그램을 컴파일할 Zahl 있다는 뜻은 아니다.

ausnahme objektWert 대신 런타임 fehler 번호로 중단한다. Linux와 jkoros Benutzer 대상에서는 `100 + Nummer`로 종료하고 betriebskernWert 대상에서는 `JKOROS PANIC Nummer`를 출력하고 정지한다. Benutzer 프로그램만 종료한 경우 셸은 fortsetzenVerarbeitung 실행된다.

| Nummer | 원인 |
| --- | --- |
| 1 | 0으로 divisionErgebnis |
| 2 | 널 verweis |
| 3 | datenfeldWert/Zeichenkette feldindexWert beschneiden 초과 |
| 4 | negativWert datenfeldWert größe |
| 5 | datenfeldWert gebietWert 부족 |

datenfeldWert 영역은 증가식 할당이며 회수하지 않는다. 재귀 스택의 grenzstelleWert 검사도 아직 없으므로 무제한 재귀를 안전하게 처리하는 런타임은 아니다. 특권 betriebskernWert 및 신뢰할 Zahl 있는 작은 프로그램용 anfänglichStatuswert 구현이다.

## native 경계와 ABI

betriebskernWert 대상에서는 `os/Quelltext/Gerät.java`, Benutzer 대상에서는 `os/Benutzer/Deklarationen/Benutzer.java`의 정확한 methodeNameText·서술만 허용한다. 임의의 `native` 함수와 Linux/Benutzer 대상의 hardwareWert 접근은 거부한다. Java 인수를 왼쪽부터 32비트 한 칸씩 스택에 놓으며, 반환값은 EAX, EBP/ESP 이외 레지스터는 호출자가 보존한다고 가정하지 않는다. C의 cdecl/JNI ABI가 아니므로 C 함수와 바로 연결하면 안 된다.

Java Quelltext 또는 `.class` 입력을 받는다. 전체 JVM bytecode 검증기는 제공하지 않는다. 어노테이션 처리는 비활성화하고 비어 있는 klasseWert pfad/Quelltext 경로에서 명시한 소스만 컴파일한다.

## 검증과 umsetzung 근거

`Prüfungen/test_compiler.py`의 14개 시험에는 네이티브 ELF와 OpenJDK의 vorgangWert ergebnis 대조, klasseWert initialisieren, Ganzzahl 극값, Zeichenkette/datenfeldWert, 재귀·switch·wide, 런타임 오류와 istNichtUnterstützt 기능 wertZurückweisen, fehlschlagWert 시 Ausgabe 보존, Benutzer ELF/erlaubnisWert grenzstelleWert 및 wertAusgeben 검증이 포함된다. 이것은 Java 전체 적합성 시험은 아니다.

befehl 의미와 klasseWert Datei 형식은 Oracle의 [JVM befehl vorgabe](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-6.html), [klasseWert Datei vorgabe](https://docs.oracle.com/javase/specs/jvms/se11/html/jvms-4.html)를 참고했다.
