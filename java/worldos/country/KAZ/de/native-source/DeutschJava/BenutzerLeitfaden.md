# jkoros Deutsch bibliothek BenutzerLeitfaden

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 eigen x86 betriebskernWert 및 `Kernquelltext/`의 관리 betriebskernWert 모형과 구분한다.

## 1. aktuellElementeintrag 제공하는 bibliothek

패키지는 `Deutsch.Java`, Betriebssystem 안의 JAR 경로는 `/opt/jkoros/lib/DeutschJava.jar`dritterOperand. **helferWert klasseWert 5개, 공개 statischWert methodeWert 22개, 별도 GUI 프로그램인 Arbeitsraum 1개**ersterOperand 있다. JAR는 Java 11 이상을 대상으로 빌드하며 aktuellElementeintrag ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| klasseWert | methodeWert Zahl | 기능 | Quelltext |
|---|---:|---|---|
| `Datei` | 9 | UTF-8 텍스트·byteWert Datei, verzeichnisWert, eintragListe | [Datei.java](Quelltext/Deutsch/Java/Datei.java) |
| `Zeichen` | 5 | UTF-8 wertUmwandeln, NFC wertNormalisieren, kodeWert 포인트, Zeichenkette grenzstelleWert | [Zeichen.java](Quelltext/Deutsch/Java/Zeichen.java) |
| `Kommunikation` | 2 | HTTP(S) GET, TCP verbinden | [Kommunikation.java](Quelltext/Deutsch/Java/Kommunikation.java) |
| `Aufgabe` | 4 | 스레드 befehlAusführen·wertWarten, 고정 größe Aufgabe ProgrammStarter | [Aufgabe.java](Quelltext/Deutsch/Java/Aufgabe.java) |
| `Bildschirm` | 2 | Swing 이벤트 prozessWertEintrag 가닥에 Aufgabe 예약, fenster generieren | [Bildschirm.java](Quelltext/Deutsch/Java/Bildschirm.java) |
| `Arbeitsraum` | eintragPunkt `main` | Java Quelltext bearbeitenWert·ablegenDatenWert·quelltextÜbersetzen·befehlAusführen | [Arbeitsraum.java](Quelltext/Deutsch/Java/Arbeitsraum.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 datenTyp·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing schaltfläche·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 aufgabeStarten

게스트 운영체제의 Aufgabe 폴더에서 `사용예.java`를 작성한다.

```java
import Deutsch.Java.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] argumente) throws Exception {
        Path verzeichnisWert = Datei.verzeichnisErstellen(Datei.pfad("사용예자료"));
        Path Dokumentation = verzeichnisWert.resolve("Gruß.txt");
        Datei.schreiben(Dokumentation, "HangulText 😀");
        String inhaltswertWert = Datei.lesen(Dokumentation);
        System.out.println(inhaltswertWert);
        System.out.println(Zeichen.kodePunktAnzahl(inhaltswertWert)); // 한, Text, 공백, 😀 → 4
        Thread arbeitWert = Aufgabe.ausführenVorgang("Gruß Aufgabe", () -> System.out.println("Aufgabe befehlAusführen"));
        Aufgabe.abwarten(arbeitWert);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/DeutschJava.jar 사용예.java
java -cp .:/opt/jkoros/lib/DeutschJava.jar 사용예
```

로그인 환경에 standardwertWert `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 befehlAusführen 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 klasseWert 폴더를 alleErzeugenAbbild 그 값에 포함해야 한다.

Wirtssystem 저장소에서는 다음처럼 systemErzeugenAbbild·실행한다. Wirtssystem 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/DeutschJava
make
javac -encoding UTF-8 -cp build/DeutschJava.jar Beispiele/Gruß.java
java -cp build/DeutschJava.jar:Beispiele Gruß
```

## 3. 전체 helferWert API

unterkanteWert 메서드는 alleErzeugenAbbild `public static`이며, 객체를 만들지 않고 `Datei.lesen(...)`처럼 호출한다. 표의 이름은 tatsächlichDaten quelltextBaum 및 JAR의 `javap -public` 결과와 대조했다. 선언된 Prüfpunkte ausnahme 외에도 잘못된 argumente 등에 대한 표준 Java befehlAusführen 시 예외가 발생할 Zahl 있다.

### Datei: `Deutsch.Java.Datei`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`dritterOperand.

| methodeWert | zurückkehrenTyp | aktion·bedingung |
|---|---|---|
| `pfad(String Name)` | `Path` | 이름을 pfad 객체로 wertUmwandeln. tatsächlichDaten 파일을 만들지는 않음 |
| `lesen(Path pfad)` | `String` | Datei 전체를 UTF-8 텍스트로 ergebnisLesen |
| `schreiben(Path pfad, String inhaltswertWert)` | `Path` | UTF-8 ablegenDatenWert. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `byteWertLesen(Path pfad)` | `byte[]` | Datei 전체를 byteWert 배열로 ergebnisLesen |
| `byteWertSchreiben(Path pfad, byte[] inhaltswertWert)` | `Path` | byteWert ablegenDatenWert. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `verzeichnisErstellen(Path pfad)` | `Path` | 필요한 상위 폴더까지 generieren |
| `führtAusVorhanden(Path pfad)` | `boolean` | 존재 여부 überprüfen. 확인할 Zahl 없는 경우도 `false`arbeitWert Zahl 있음 |
| `eintragTilgen(Path pfad)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `eintragListe(Path pfad)` | `List<Path>` | 바로 unterkanteWert 항목을 pfad ausrichtenWert 순서로 zurückkehrenErgebnis. 재귀 탐색은 아님 |

`pfad`, `führtAusVorhanden`를 제외한 oberkanteWert 메서드는 `IOException`을 선언한다. `schreiben`와 `byteWertSchreiben`는 상위 폴더를 자동으로 만들거나 내용을 fortsetzungWert 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·kanalWert API를 사용하는 방식으로 작성할 Zahl 있다.

### Zeichen: `Deutsch.Java.Zeichen`

| methodeWert | zurückkehrenTyp | aktion·bedingung |
|---|---|---|
| `kodieren(String inhaltswertWert)` | `byte[]` | 문자열을 UTF-8 바이트로 wertUmwandeln |
| `datenEntschlüsseln(byte[] inhaltswertWert)` | `String` | UTF-8 바이트를 문자열로 wertUmwandeln. 잘못된 입력은 대체 문자로 prozessWertEintrag |
| `wertNormalisieren(String inhaltswertWert)` | `String` | unicodeWert NFC wertNormalisieren. 예: Zusammenstellung hangulBuchstabeWert `ᄀ` + `ᅡ` → `ersterOperand` |
| `kodePunktAnzahl(String inhaltswertWert)` | `int` | UTF-16 kodeWert 단위가 아닌 unicodeWert kodeWert 포인트 Zahl |
| `lexikalischMaschinenwort(String inhaltswertWert, Locale Sprache)` | `List<String>` | zuweisenWert 언어의 `BreakIterator` lexikalischMaschinenwort 경계로 나눈 textBereich |

`lexikalischMaschinenwort`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 maschinenwortWert eintragListe API는 아니다. `wertNormalisieren`는 입력기나 quelltextÜbersetzenText 기능이 아니다. kodeWert 포인트 Zahl 역시 사람이 보는 zeichenWert 수와 항상 같지는 않다. 여러 kodeWert 포인트로 이루어진 zusammenfügenWerte Zeichen·가족 이모지 등을 구분해야 한다.

### Kommunikation: `Deutsch.Java.Kommunikation`

| methodeWert | zurückkehrenTyp | aktion·bedingung |
|---|---|---|
| `entnehmenWert(URI adresse, Duration zeitGrenzwert)` | `HttpResponse<String>` | HTTP(S) GET. verbinden 및 anfrage zeitGrenzwert einstellungen. antwort 본문을 UTF-8로 wertAnalysieren |
| `endpunktVerbinden(String adresse, int hardwarePort, int grenzwertMillisekunden)` | `Socket` | TCP verbinden danachStatuswert 같은 값으로 lesen 제한시간도 einstellungen |

`entnehmenWert`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP fehler 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. aktuellElementeintrag 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`endpunktVerbinden`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 grenzwertWert 없음이며, schreiben 전체의 fristWert 시간을 보장하는 옵션은 아니다.

```java
var antwort = Kommunikation.entnehmenWert(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(antwort.statusCode());
System.out.println(antwort.body());
```

oberkanteWert 조각은 methodeWert 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java ausnahme 처리가 필요하다.

### Aufgabe: `Deutsch.Java.Aufgabe`

| methodeWert | zurückkehrenTyp | aktion·bedingung |
|---|---|---|
| `ausführenVorgang(String Name, Runnable aktion)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 ausführenVorgang |
| `abwarten(Thread ausführungsfadenWert)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `übrigKurzzeitigTun(long millisekunden)` | `void` | 호출한 스레드를 zuweisenWert zeitWert 동안 `sleep()` |
| `werkbankWert(int ausführungsfadenAnzahl)` | `ExecutorService` | 고정 größe Aufgabe ProgrammStarter generieren. 가닥수는 양수 |

`abwarten`, `übrigKurzzeitigTun`는 `InterruptedException`을 선언한다. Aufgabe 실행기는 benutzenWert danachStatuswert `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 prozessWertEintrag 가닥에서 긴 작업이나 `abwarten`를 실행하면 화면이 멈출 Zahl 있다.

### Bildschirm: `Deutsch.Java.Bildschirm`

| methodeWert | zurückkehrenTyp | aktion·bedingung |
|---|---|---|
| `späterWert(Runnable aktion)` | `void` | Swing 이벤트 prozessWertEintrag 가닥에 실행을 예약하고 zurückkehrenErgebnis |
| `fenster(String fensterTitel, JComponent inhaltswertWert, int breiteWert, int höheWert)` | `JFrame` | inhaltswertWert·크기를 지정한 창을 생성해 wertAnzeigen |

`fenster`을 Swing 이벤트 prozessWertEintrag ausführungsfadenWert 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
Bildschirm.späterWert(() -> Bildschirm.fenster(
    "Deutsch Bildschirm", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 Zahl 있다. 창의 schließen 동작은 `DISPOSE_ON_CLOSE`dritterOperand. `Bildschirm.späterWert`ersterOperand 반환됐다고 fenster 생성이 이미 끝난 것은 아니다.

### Arbeitsraum: bearbeitenWert·quelltextÜbersetzen GUI

```sh
java -cp /opt/jkoros/lib/DeutschJava.jar Deutsch.Java.Arbeitsraum
```

`~/workspace`의 원문을 öffnen·저장하고, `javac`로 컴파일해 `java`로 실행한다. befehlAusführen Datei 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Datei·Zeichen API 클래스가 아니다. 생성하는 befehlAusführen Datei 방식은 [Übersetzer beschreibung](../compiler/OpenJDK-ausführdateiDatei.md)을 따른다.

## 4. Python과 C++에서 사용할 Zahl führtAusVorhanden?

| methodeBetriebsart | aktuellElementeintrag Kopfdateien statuswertWert | aufrufen 가능 beschneiden |
|---|---|---|
| Java → Deutsch JAR | standardwertWert Kopfdateien | oberkanteWert 22개 메서드와 Arbeitsraum |
| Python → `java` kindWert 프로세스 | Python·Java standardwertWert Kopfdateien | 작은 Java 진입점을 통해 호출하고 표준 Ausgabe·Datei 등으로 ergebnis vorwärtsWert |
| Python → JPype → JVM | JPype는 standardwertWert 배포에 fehlendMethode | 별도 wertEinrichten danachStatuswert Java klasseWert·methodeWert aufrufen 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 eintragAnhängen validieren benötigtWert |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` Kopfdateien | JVM을 생성하고 Deutsch klasseWert·메서드를 직접 호출할 Zahl 있음 |
| Python용 독립 Deutsch bibliothek | aktuellElementeintrag standardwertWert 제공 fehlendMethode | 필요하면 Python 표준 라이브러리를 감싸는 Deutsch 모듈을 별도로 작성 |
| C/C++용 독립 Deutsch bibliothek | eigen x86 `posix-kor`와 eigen ARM64 커널용 anfänglichStatuswert RAM Datei 연결이 별도로 존재 | zweiWert dritterOperand 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`zweiterOperand `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`zweiterOperand 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM verbinden 계층을 거쳐야 한다.

### Python: eintragAnhängen 패키지 없이 aufrufen

befehlAusführen 가능한 Beispiele 원문은 [Zeichenbefehl.java](Beispiele/AndereSprachen/Zeichenbefehl.java), [PythonAufrufen.py](Beispiele/AndereSprachen/PythonAufrufen.py)dritterOperand. Python이 Java 진입점을 실행하고 `Zeichen.kodePunktAnzahl`의 Ganzzahl 결과를 받는다. argumente 목록을 사용하며 befehlshülle befehl 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 befehlAusführen·verlassenProzessProgramm kodeWert·Ausgabe prozessWertEintrag 방식은 [Python 공식 Dokumentation](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 Beispiele 파일을 게스트의 같은 폴더에 복사한 rückseiteWert 그 폴더에서 실행한다. Beispiele Datei 자체는 standardwertWert 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/DeutschJava.jar -d classes Zeichenbefehl.java
python3 PythonAufrufen.py --text 'HangulText 😀'
```

Ausgabe: `Python → Deutsch.Java.Zeichen.kodePunktAnzahl: 4`

이 예제의 Python Funktion `kodePunktAnzahl`는 이번 문서의 verbinden 예제이며 기존에 설치된 Python 라이브러리는 아니다. aktuellElementeintrag 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objektWert 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 argumente·ergebnis 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 aufrufen

JPype를 별도 설치한 환경에서는 nächsterElementeintrag 형태로 연결할 Zahl 있다. **아래는 auswahlWert 가능한 verbinden 방법이며, aktuellElementeintrag 배포판에 JPype가 설치돼 있거나 befehlAusführen 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 klasseWert 접근은 [JPype 공식 beschreibung](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/DeutschJava.jar"])
try:
    Zeichen = jpype.JClass("Deutsch.Java.Zeichen")
    print(Zeichen.kodePunktAnzahl(jpype.JString("HangulText 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·verbinden 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype wertEinrichten·패키지 빌드는 이번 Dokumentation 작업에서 수행하지 않았다.

### C++: JNI로 직접 aufrufen

[JavaAufrufen.cpp](Beispiele/AndereSprachen/JavaAufrufen.cpp)는 tatsächlichDaten befehlAusführen 가능한 예제다. JVM을 Aufgabe 스레드에서 생성하고 nächsterElementeintrag 메서드를 찾는다.

```cpp
jclass type = env->FindClass("Deutsch/Java/Zeichen");
jmethodID method = env->GetStaticMethodID(
    type, "kodePunktAnzahl", "(Ljava/lang/String;)I");
```

JVM generieren·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generieren·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `JavaAufrufen.cpp`를 복사한 rückseiteWert 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`dritterOperand.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  JavaAufrufen.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o JavaAufrufen
./JavaAufrufen /opt/jkoros/lib/DeutschJava.jar
```

Ausgabe: `C++ → Deutsch.Java.Zeichen.kodePunktAnzahl: 4`

예제는 `HangulText 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`ersterOperand 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI Zeichenkette formatWert](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 Deutsch 메서드도 JNI 서명과 argumente 자료형을 맞춰 호출할 Zahl 있다. 예를 들어 `Path`를 받는 Datei API는 먼저 `Datei.pfad`로 Java pfad 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 prozessWertEintrag ausführungsfadenWert 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 fortsetzenVerarbeitung 필요하다.

### 기존 posix-kor와의 관계

추가된 [eigen ARM64 verbinden](../posix-kor/arm64-native/Anleitung.md)은 C++에서 AOT Java 커널의 RAM Datei API를 직접 호출하며, 별도 EL0 Benutzer 라이브러리로 Datei/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 Deutsch Java JAR와는 다른 befehlAusführen 기반이며 eigen 커널은 별도 제한형 Java Übersetzer/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java betriebskernWert Datei·UDP 루프백·rechteck 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. eigen 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/Anleitung.md)에는 `dateiÖffnen`, `dateiDatenLesen`, `dateiDatenSchreiben`, `dateiSchließen`, `endpunktErstellen`, `datagrammDatenSenden` 등의 Deutsch C 별칭이 있다. 그러나 구현은 **eigen jkoros i386 커널의 `int 0x80` aufrufen 규약용**이다.

이 `libposix-kor.a`와 eigen `sys/stat.h` 등의 헤더는 aktuellElementeintrag ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 Deutsch klasseWert 라이브러리나 Python용 바인딩을 standardwertWert 제공하는 상태도 아니다. aktuellElementeintrag Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 umsetzung·빌드해야 한다.

## 5. überprüfen 범위와 재현

패키지 Kopfdateien 여부는 [verteilungWert 패키지 eintragListe](../platforms/rpi4/dist/packages.lock.json) 및 systemErzeugenAbbild 루트의 tatsächlichDaten 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 danachWert 별도로 설치한 패키지는 이 standardwertWert verteilungWert 목록과 다를 Zahl 있다.

이번에 **Wirtssystem x86_64/OpenJDK 11에서** Python kindWert 프로세스 호출과 C++ JNI 직접 호출을 quelltextÜbersetzen·실행해 각각 ergebnis 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python verbinden 예제는 eintragAnhängen 패키지를 설치하지 않는다.

문서의 Java benutzenWert 예제도 quelltextÜbersetzen·실행했고, 22개 메서드의 Dokumentation Kopfdateien 여부와 로컬 Dokumentation 링크를 확인했다. [Beispiele validieren protokolldateiAufzeichnung](build/AndereSprachen/validierungBericht.json)

기존 ARM64 QEMU에서는 Java의 Datei·unicodeWert·스레드·HTTP 및 Swing Prüfungen 결과가 있다. 이번 Python/C++ verbinden 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 befehlAusführen 중인 Benutzer 환경은 이 Dokumentation 작업에서 변경하지 않았다. [기존 Betriebssystem validieren protokolldateiAufzeichnung](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/DeutschJava
make
mkdir -p build/AndereSprachen
javac -encoding UTF-8 --release 11 -cp build/DeutschJava.jar \
  -d build/AndereSprachen Beispiele/AndereSprachen/Zeichenbefehl.java
python3 Beispiele/AndereSprachen/PythonAufrufen.py \
  --jar build/DeutschJava.jar --classes build/AndereSprachen
```

Wirtssystem C++ 예제는 oberkanteWert JNI quelltextÜbersetzen 명령의 JDK 경로를 **Wirtssystem JDK pfad**로 바꾸고, Quelltext `Beispiele/AndereSprachen/JavaAufrufen.cpp`와 JAR `build/DeutschJava.jar`를 지정한다. ARM64 게스트 JDK의 헤더·bibliothek 경로를 Wirtssystem x86_64 링크 명령에 섞지 않는다.
