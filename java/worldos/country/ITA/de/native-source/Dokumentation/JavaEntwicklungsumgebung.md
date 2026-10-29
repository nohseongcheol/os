# jkoros 안에서 Java quelltextÜbersetzen·befehlAusführen

이 문서의 Startvorgang·befehlshülle·ablegenDatenWert 명령은 **x86 versionWert** 기준이다. 공유 Java Übersetzer/JVM은 [eigen ARM64 Pi4 versionWert](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART Eingabewert·HangulText dateiNameText, `edit`의 단독 `.` ablegenDatenWert, 16개 RAM Datei, 약 2초 befehlAusführen 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 tatsächlichDaten JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. Wirtssystem quelltextÜbersetzen 서버나 Linux 게스트는 사용하지 않는다.

**aktuellElementeintrag 구현은 eigen 제한형 Übersetzer·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java Programm 실행은 아직 지원하지 않는다.

## 바로 befehlAusführen

호스트에서:

```sh
cd /home/user/jkoros
make iso
make run
```

게스트에서:

```text
jkoros> javac -version
jkoros> java -version
jkoros> ls
jkoros> cat Hello.java
jkoros> javac Hello.java
Compiled: Hello.class (JVM class version 49)
Exit: 0
jkoros> java Hello
Hello from jkoros JVM!
55
Exit: 0
```

ISO는 `os/build/kernel.iso`dritterOperand. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. befehlAusführen 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 Startvorgang 절차는 [VirtualBox befehlAusführen Anleitung](VirtualBoxStarten.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 Datei 전체를 새 내용으로 작성한다. 기존 내용의 zeile bearbeitenWert 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

```text
jkoros> edit Demo.java
...> public class Demo {
...>  public static int square(int n) { return n * n; }
...>  public static void main(String[] args) {
...>   int n = Integer.parseInt(args[0]);
...>   System.out.println("square=" + square(n));
...>  }
...> }
...> .save
jkoros> javac Demo.java
jkoros> java Demo 12
square=144
Exit: 0
```

- `ls`: 파일과 byteWert Zahl wertAnzeigen.
- `cat FILE`: Datei inhaltswertWert wertAnzeigen. 텍스트 소스에 사용한다.
- `rm FILE`: speicherDaten Datei 삭제.
- `edit FILE`: 전체 내용을 새로 Eingabewert. 빈 파일도 저장할 Zahl 있다.
- 구문·typWert Prüfpunkte fehlschlagWert 시 기존 `.class`는 유지된다. 소스를 고친 rückseiteWert 컴파일이 실패했다면 vorherigElementeintrag befehlAusführen 파일이 남아 있으므로 quelltextÜbersetzen erfolgWert 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 ablegenDatenWert 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 quelltextBaum·klasseWert·Daten 파일을 보존할 Zahl 있다. höchstwertWert 8개, 파일마다 16KiB, Datei 이름은 ASCII 1~63자다. quelltextBaum 이름은 `.class` 확장자 adresseGebiet 때문에 höchstwertWert 62자다. bearbeitenWert 입력은 ASCII이고 한 zeile höchstwertWert 128자다. zeile 또는 Datei 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. betriebskernWert/Übersetzer/JVM 구현의 Java 식별자는 한국어이며, aktuellElementeintrag 게스트 Eingabewert grenzwertWert 때문에 Benutzer Beispiele 이름은 ASCII로 작성한다.

## externWert Datei 적재

호스트에서 만든 소스나 unterstützungWert beschneiden 안의 `.class`를 Startvorgang 이미지에 포함할 Zahl 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 tatsächlichDaten 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# Wirtssystem JDK로 컴파일한 클래스도 사용할 Zahl 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 Startvorgang danachStatuswert `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 nächsterElementeintrag 빌드에서는 eintragAnhängen 파일을 포함하지 않는다. Datei inhaltswertWert 변경과 eintragListe 제거도 nächsterElementeintrag 빌드에 반영된다. ursprünglich Wirtssystem 파일에는 쓰지 않는다. standardwertWert `Hello.java`bis 합해 8개이며, 같은 이름을 명시하면 standardwertWert 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 klasseWert Datei 버전을 맞추는 옵션이다. 사용하는 문법·bytecode·라이브러리도 unterkanteWert unterstützungWert beschneiden 안에 있어야 한다.

## unterstützungWert beschneiden

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| klasseWert | 패키지 없는 단일 klasseWert, statischWert Funktion, 재귀, argumente/zurückkehrenErgebnis | 실행마다 단일 klasseWert 적재, public static main(String[]) |
| standardwertWert Wert | int, boolean, char, String, main의 String[] argumente | Ganzzahl·verweis operandStapel, String, int[], String[], 내부 StringBuilder |
| anweisungWert | anfänglichWert 있는 lokalGültigkeitsbereich Deklarationen, zuweisungWert, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 Ganzzahl·verweis 바이트코드와 bedingung verzweigung |
| ausdruckWert | 십진 Ganzzahl, UTF-8 소스의 Zeichenkette/Zeichen, + - * / %, 비교, ==/!=, !/&&/\|\|, Zeichenkette zusammenfügenWerte | Ganzzahl vorgangWert·bitWert vorgangWert·typWert wertUmwandeln, 단락 평가, datenfeldWert zugriffEintrag |
| Datei | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | tatsächlichDaten betriebskernWert 파일서술자와 verbinden, generieren·inhaltLöschenInhalt·fortsetzungAnhängen·EOF |
| Ausgabe | System.out.print/println: int/boolean/char/String, println() | 동일 |
| Zeichenkette/argumente | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), Zeichenkette 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, anfänglichWert 없는 lokalGültigkeitsbereich Deklarationen, 오버로드, 임의 typWert wertUmwandeln, datenfeldWert generieren Quelltext, 8/16진 리터럴, Unicode quelltextBaum 이스케이프 등은 미지원이다. `char`는 Zeichen 리터럴로 초기화하며 일반 JDK의 모든 konstanteWert 축소 변환을 구현하지 않는다. externWert `.class`의 `int[]` generieren/lesen/쓰기는 지원하므로 Wirtssystem `javac --release 8`로 만든 datenfeldWert 예제는 실행할 Zahl 있다.

objektWert feldWert·일반 objektWert generieren·상속·인터페이스·여러 klasseWert verbinden, long/float/double, ausnahme prozessWertEintrag, 스레드·모니터, 리플렉션, JNI, JIT, GC, oberkanteWert 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java ausnahme 객체를 던지지 않고 diagnoseWert danachStatuswert aktuellElementeintrag 프로그램을 종료한다. 객체와 Zeichenkette ablegenDatenWert 공간은 befehlAusführen verlassenProzessProgramm 시 Benutzer gebietWert 전체와 함께 회수한다. 지속 befehlAusführen 중 GC는 없다.

## befehlAusführen 한도와 fehler

| betriebsmittelEintragWert | kapazitätGrenzwert |
| --- | --- |
| quelltextBaum/klasseWert Datei | 각각 16KiB |
| Übersetzer | wortzeichenWert 2,047개, generieren kodeWert 4KiB, konstanteWert 풀 4KiB |
| Funktion/argumente | 클래스당 32함수, 함수당 16인수 |
| JVM konstanteWert | 511개 |
| JVM Funktion kodeWert | 함수당 8KiB |
| JVM aufrufen/operandStapel/lokalGültigkeitsbereich variableWert | 32프레임, 프레임당 operandStapel 128칸·lokalGültigkeitsbereich 128칸 |
| JVM objektWert ablegenDatenWert adresseGebiet | 8,192개 32비트 platzEintrag, 헤더 Kopfdateien 약 32KiB |
| befehlAusführen | höchstwertWert 500,000 befehl, 기존 커널의 약 3초 CPU befehlAusführen 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 unterstützungWert 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM Wörterbuch 검증기를 구현한 것은 아니다. Datei/attributWert Länge, konstanteWert verweis, befehl·verzweigung 경계를 검사하고, befehlAusführen 중 operandStapel formatWert·lokalGültigkeitsbereich initialisieren·datenfeldWert feldindexWert·objektWert 참조를 검사한다. Benutzer 코드의 페이지·hardwarePort 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, quelltextÜbersetzen·JVM 오류는 `Exit: 1`, befehl argumente 오류는 `Exit: 2`dritterOperand. CPU zeitWert 상한은 기존 `Exit: 124`이며, Benutzer ELF 자체의 CPU/런타임 오류는 기존 verlassenProzessProgramm 코드를 따른다. fehlschlagWert danachStatuswert 셸에서 다른 프로그램을 fortsetzenVerarbeitung 실행할 Zahl 있다.

## umsetzung 위치와 Prüfungen

- `os/Benutzer/Java/JavaÜbersetzer.java`: 게스트 어휘·구문·typWert Prüfpunkte, konstanteWert 풀 및 bytecode generieren.
- `os/Benutzer/Java/VirtuelleJavaMaschine.java`: klasseWert 적재, operandStapel·프레임·objektWert ablegenDatenWert, befehl 해석과 제한된 표준 aufrufen.
- `os/Quelltext/ArbeitsspeicherDateisystem.java`: speicherDaten DateiSystem, bearbeitenWert, Startvorgang Datei 적재.
- `os/Quelltext/Systemaufruf.java`, `compiler/benutzerProgrammStarten.s`: Datei/Zeichen Ausgabe API와 Benutzer zeiger Prüfpunkte.
- `os/Werkzeuge/JavaDateienPacken.py`: Wirtssystem Eingabewert Datei validieren·Startvorgang gruppeWert generieren.

```sh
make test-java
make test
```

`os/Prüfungen/JavaPrüfung.py`는 ELF/ISO Startvorgang, 게스트 quelltextÜbersetzen·befehlAusführen, Benutzer Eingabewert, 재귀·반복문·Ganzzahl 극값·Zeichenkette zusammenfügenWerte·단락 평가, 재실행, quelltextBaum fehler danachStatuswert 기존 klasseWert 보존, datenfeldWert/Zahl 해독 fehler, 무한 wiederholungsschrittWert grenzwertWert, bearbeitenWert 넘침과 Datei 부족을 검사한다. 게스트 generieren 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 Wirtssystem OpenJDK의 klasseWert, Ganzzahl 배열과 HangulText 상수를 게스트에 적재하며, 손상된 Datei markierungWert·버전·konstanteWert Zahl·verzweigung·스택을 거부하는지도 검사한다. 기록은 `os/build/JavaPrüfung.json`에 남는다. 디스크 없는 별도 Prüfungen VM만 생성하고 종료한다.

umsetzung 형식의 참고 Daten: Oracle [JVM klasseWert Datei vorgabe](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM befehl vorgabe](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java Datei eingabeAusgabe

[FileDemo.java](../posix-kor/JavaBeispiel/FileDemo.java)는 일반 Java 표준 klasseWert 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 Startvorgang 이미지에 넣은 rückseiteWert `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`dritterOperand. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. standardwertWert Ausgabe 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. ausnahme objektWert·try/catch·try-with-resources는 지원하지 않으며 Datei 오류를 진단하고 프로그램을 종료한다. datenfeldWert eingabeAusgabe, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 Datei 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 befehlshülle `sync`ersterOperand 필요하다. 예제의 Datei 이름은 aktuellElementeintrag 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/Prüfungen/JavaDateiprüfung.py`는 tatsächlichDaten 게스트 quelltextÜbersetzen 결과를 OpenJDK `-Xverify:all`로 erneutVersuchenWert 실행해 Datei 바이트와 출력을 대조한다. 범위와 ablegenDatenWert medienWert 사용법은 [posix-kor Anleitung](../posix-kor/Anleitung.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
