# Deutsch Java Kommunikation·eingabeAusgabe·ausnahme API

패키지는 `Deutsch.eigen`dritterOperand. Wirtssystem `javac --release 8`로 컴파일한 class를
eigen ARM64 커널의 JVM에서 실행한다. Kommunikation·Datei·ausnahme API는 OpenJDK와 대조한다. 아래의 직접 구현한 Bildschirm·Aufgabe ausführungsfadenWert API는 eigen JVM 전용이다.
기존 표준 Java bibliothek 전체의 Deutsch 번역판은 아니다.

```java
import Deutsch.eigen.*;

public class netzwerk {
    public static void main(String[] argumente) throws EingabeAusgabeAusnahme {
        Verbindung verbinden = Verbindung.öffnen("10.0.2.2", 9000);
        try {
            verbinden.zeitüberschreitung(700);
            verbinden.Ausgabe().schreiben(Zeichen.kodieren("안녕하세요\n"));
            EingabeDatenstrom Eingabewert = verbinden.Eingabewert();
            Ausgabe.nummerSchreiben(Eingabewert.lesen());
        } catch (WartenZeitüberschreitungAusnahme fehler) {
            Ausgabe.zeileSchreiben(fehler.beschreibung());
        } finally {
            verbinden.schließen();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
Benutzer 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 Zeichenkette 리터럴에 사용하는 표준 클래스다. eigen 실행기는 `public static void ausführenVorgang()`도 진입점으로 받는다.

## 통신과 datenstromWert

| klasseWert | Deutsch aufrufen |
|---|---|
| Verbindung | `öffnen(adresse, portNummer)`, `Eingabewert()`, `Ausgabe()`, `zeitüberschreitung(millisekunden)`, `portNummer()`, `lokalPortNummer()`, `verbunden()`, `istGeschlossen()`, `schließen()` |
| portEmpfangen | `öffnen(portNummer)`, `empfangen()`, `portNummer()`, `zeitüberschreitung(millisekunden)`, `istGeschlossen()`, `schließen()` |
| EingabeDatenstrom | `lesen()`, `lesen(byte[])`, `lesen(byte[], ausführenVorgang, Länge)`, `schließen()` |
| AusgabeDatenstrom | `schreiben(int)`, `schreiben(byte[])`, `schreiben(byte[], ausführenVorgang, Länge)`, `wertAusgeben()`, `schließen()` |
| DatagrammKanal | `öffnen(portNummer)`, `senden(adresse, portNummer, Text)`, `empfangen()`, `zeitüberschreitung(millisekunden)`, `portNummer()`, `istGeschlossen()`, `schließen()` |
| verbindungBeförderung | `öffnen(...)`, `empfängerÖffnen(...)`는 oberkanteWert Deutsch 객체를 zurückkehrenErgebnis |
| Prüfpunkte | `erfordern(bedingung, ursacheWert)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`lesen()`의 Datei 끝은 -1, datenfeldWert 읽기의 반환값은 tatsächlichDaten 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. portNummer 0은 빈 번호를 자동 배정한다.
UDP 전문은 aktuellElementeintrag eigen 커널에서 512바이트까지 받으며, 주소는 zifferWert IPv4를 사용한다.
`localhost` 루프백 외의 Name 풀이(DNS)는 eigen 커널에 아직 없다.

기존 `verbindungBeförderung.verbinden/endpunktLauschen/empfangen`, `Kommunikation.öffnen/senden/empfangen`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `Verbindung`, `portEmpfangen`, `DatagrammKanal`를 쓴다.

## Deutsch ausnahme

모든 unterkanteWert 클래스는 standardwertWert 생성자, `새예외("beschreibung")` 형태의 Zeichenkette 생성자와
`beschreibung()`을 제공한다. tatsächlichDaten generieren 문법은 `new WartenZeitüberschreitungAusnahme("statuswertWarten endung")`이다.

| Deutsch ausnahme | 상위 klasseWert / 용도 |
|---|---|
| ausnahme | `java.lang.Exception`, 직접 던지는 일반 Prüfpunkte ausnahme |
| AusführungAusnahme | `java.lang.RuntimeException` |
| EingabeAusgabeAusnahme | `java.io.IOException`, Deutsch Datei·Kommunikation API의 Prüfpunkte ausnahme |
| WartenZeitüberschreitungAusnahme | `EingabeAusgabeAusnahme`, Kommunikation zeitüberschreitung 초과 |
| AdresseNachschlagenAusnahme | `EingabeAusgabeAusnahme`, adresse überprüfen fehlschlagWert |
| FehlendDateiAusnahme | `EingabeAusgabeAusnahme`, Datei öffnen fehlschlagWert |
| KommunikationAusnahme | `EingabeAusgabeAusnahme`, 표준 SocketException wertUmwandeln |
| UngültigArgumentAusnahme | `java.lang.IllegalArgumentException` |
| NummerFormatFehlschlag | `UngültigArgumentAusnahme` |
| GrenzenAusnahme | `java.lang.IndexOutOfBoundsException` |
| DatenfeldGrenzenAusnahme / ZeichenketteGrenzenAusnahme | `GrenzenAusnahme` |
| NullverweisVerweisAusnahme | `java.lang.NullPointerException` |
| ArithmetikFehlschlag | `java.lang.ArithmeticException` |
| StatuswertAusnahme | `java.lang.IllegalStateException` |
| TypTypumwandlungAusnahme | `java.lang.ClassCastException` |
| NegativDatenfeldGrößeFehlschlag | `java.lang.NegativeArraySizeException` |
| DatenfeldAblegenDatenFehlschlag | `java.lang.ArrayStoreException` |
| AusführungsfadenStatuswertAusnahme | `java.lang.IllegalThreadStateException` |
| WartenUnterbrochenAusnahme | `java.lang.InterruptedException`, `Aufgabe.abwarten`의 wertWarten 중단 |

`ausnahme`와 `AusführungAusnahme`는 모든 Deutsch 예외의 gemeinsamWert 부모가 아니다. oberkanteWert 상속 관계를
사용하며, Datei·Kommunikation 전체를 잡으려면 `catch (EingabeAusgabeAusnahme fehler)`를 쓴다.
Deutsch API가 표준 eingabeAusgabe 오류를 Deutsch 예외로 변환한다.
기존 Deutsch Kommunikation 호출에서 `SocketTimeoutException`을 잡던 코드는
`WartenZeitüberschreitungAusnahme`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
ausnahme 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
aktuellElementeintrag eigen JVM에 이 20종을 추가했다. 임의의 Benutzer Throwable 하위 klasseWert 전체를
지원하도록 확장했다는 뜻은 아니다.

## quelltextÜbersetzen·befehlAusführen

```sh
cd /home/user/jkoros/platforms/rpi4-native
make systemErzeugenAbbild
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 Prüfungen/Java/koreanischNetzbetriebPrüfung.java
python3 Werkzeuge/dateiAusführen.py build/한국어사용/koreanischNetzbetriebPrüfung.class
make test-jvm
```

내장 라이브러리는 Benutzer JVM ELF 안에 탑재된다. `.jar`는 Wirtssystem javac의
klasseWert 경로로 사용한다. quelltextBaum 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Deutsch 예외의 `throws` 선언과 그 import를 인식한다.
eigen JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objektWert·netzbuchseWert Beispiele 전체의 quelltextBaum 컴파일은 Wirtssystem javac를 사용한다.
`/example/java/Dateibeispiel.java`는 게스트 javac로도 컴파일할 Zahl 있다.

tatsächlichDaten TCP/UDP 예제는 [Netzbeispiel.java](../../../example/java/Netzbeispiel.java),
befehlAusführen 절차는 [example Anleitung](../../../example/README.md),
quelltextBaum benennung 원칙은 [benennung Anleitung](../benennung/Anleitung.md)에 있다.

## Swing fenster Beispiele

`/example/java/Fensterbeispiel.java`와 컴파일된 `.class`ersterOperand Startvorgang 시 준비된다.
`cd /example/java` nächsterElementeintrag `java Fensterbeispiel`로 연다. Name Eingabewert, grüßen 버튼,
인사말과 klickenWert wiederholungAnzahl auffrischen, X 닫기를 지원한다.

| 기능 | Deutsch 직접 API |
|---|---|
| Runnable / run | `AusführbarAufgabe.aufgabeAusführen()` |
| ActionListener / actionPerformed | `AktionEmpfänger.aktionEmpfangen(AktionMitteilung mitteilung)` |
| ActionEvent | `AktionMitteilung.befehlText()`, `ereignisQuelltext()`, `Nummer()` |
| JFrame | `fenster(fensterTitel, breiteSpannweite, höheWert)`, `elementHinzufügen(BildschirmElement)`, `fensterAnzeigen()`, `schließen()`, `istSichtbar()` |
| JButton | `schaltfläche(Text, waagerechtPosition, senkrechtPosition, breiteSpannweite, höheWert, empfängerWert)`, `aktionEmpfängerSetzen(empfängerWert)` |
| JLabel / JTextField | `beschriftung(...)`, `TextFeld(...)` |
| gemeinsamWert Bildschirm elementWert | `BildschirmElement.textLesen()`, `textSchreiben(Text)`, `grenzenSetzen(waagerechtPosition, senkrechtPosition, breiteSpannweite, höheWert)` |
| SwingUtilities.invokeLater | `EreignisWarteschlange.späterAufrufen(AusführbarAufgabe)`, `istEreignisVerteilend()` |
| Thread | `hintergrundarbeiter(AusführbarAufgabe)`, `aufgabeStarten()`, `abwarten()`, `istLebendig()`, `aufgabeAbgeben()` |
| 명령행 | `ausführenVorgang()`, `Argumente.elementeintragAnzahl()`, `Argumente.Text(ordnungszahlIndex)` |

oberkanteWert 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
eigen JVM의 `koreanischBildschirmAufrufen`, `prozessAusführungsfaden`ersterOperand Deutsch klasseWert·methodeWert·서술자를
해석해 Bildschirm 요소와 befehlAusführen 가닥을 직접 만든다. aktion 알림도 eigen 객체이며
콜백으로 `aufgabeAusführen`와 `aktionEmpfangen`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 befehlAusführen 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 eigen JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 Wirtssystem JVM에서 무동작 객체가 생기지 않도록 하는 wertZurückweisen 경로다.
eigen JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 umsetzung API를
실행할 Zahl 없다. Wirtssystem javac로 컴파일한 rückseiteWert eigen JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, Bildschirm 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Deutsch.eigen.*;
public class 가닥예제 implements AusführbarAufgabe {
    public void aufgabeAusführen() { Ausgabe.zeileSchreiben("Deutsch Aufgabe befehlAusführen"); }
    public static void ausführenVorgang() throws WartenUnterbrochenAusnahme {
        hintergrundarbeiter ausführungsfadenWert = Aufgabe.ausführenVorgang(new 가닥예제());
        Aufgabe.abwarten(ausführungsfadenWert);
    }
}
```

`example/java`의 다섯 소스는 reserviertWörter·리터럴 외 식별자를 한국어로 작성한다.
datenfeldWert argumente 대신 `Argumente`, 길이는 `Zeichen.byteAnzahl`를 사용한다.
표준 Java의 `main(String[])`도 fortsetzenVerarbeitung 지원한다. zweiWert dritterOperand 정의되어 있으면
eigen 실행기는 argumente 없는 `ausführenVorgang()`을 우선한다.
기존 Deutsch Bildschirm 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`Aufgabe.ausführenVorgang(Runnable)`을 사용하던 코드는 새 Deutsch 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API unterstützungWert 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 klasseWert·methodeWert 이름과 서술자가 남는다.
Deutsch Name 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 unterteilWert,
상속·methodeWert 재정의, native verbinden, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS bezeichnerWert](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS methodeWert verweis](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)dritterOperand.
