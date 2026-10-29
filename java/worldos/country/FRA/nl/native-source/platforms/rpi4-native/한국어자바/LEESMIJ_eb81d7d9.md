# Nederlands Java communicatie·I_O·uitzondering API

패키지는 `Nederlands.Eigen`다. host `javac --release 8`로 컴파일한 class를
Eigen ARM64 커널의 JVM에서 실행한다. communicatie·bestand·uitzondering API는 OpenJDK와 대조한다. 아래의 직접 구현한 scherm·작업 thread_WAARDE API는 Eigen JVM 전용이다.
기존 표준 Java bibliotheek 전체의 Nederlands 번역판은 아니다.

```java
import Nederlands.Eigen.*;

public class net {
    public static void main(String[] argumenten) throws I_O_uitzondering {
        verbinding Verbinden = verbinding.Openen("10.0.2.2", 9000);
        try {
            Verbinden.TIMEOUT(700);
            Verbinden.tekstuitvoer().Schrijven(문자.coderen("안녕하세요\n"));
            invoerstroom invoer_WAARDE = Verbinden.invoer_WAARDE();
            tekstuitvoer.schrijven_nummer(invoer_WAARDE.Lezen());
        } catch (wachten_TIMEOUT_uitzondering fout) {
            tekstuitvoer.schrijven_lijn(fout.설명());
        } finally {
            Verbinden.Sluiten();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
gebruikersruimte 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 tekenreeks_WAARDE 리터럴에 사용하는 표준 클래스다. Eigen 실행기는 `public static void starten()`도 진입점으로 받는다.

## 통신과 Stream_WAARDE

| les_WAARDE | Nederlands 호출 |
|---|---|
| verbinding | `Openen(ADRES, poortnummer)`, `invoer_WAARDE()`, `tekstuitvoer()`, `TIMEOUT(밀리초)`, `poortnummer()`, `lokaal_poortnummer()`, `연결됨()`, `informatie_afgesloten()`, `Sluiten()` |
| ontvangen_poort | `Openen(poortnummer)`, `ontvangen()`, `poortnummer()`, `TIMEOUT(밀리초)`, `informatie_afgesloten()`, `Sluiten()` |
| invoerstroom | `Lezen()`, `Lezen(byte[])`, `Lezen(byte[], starten, tijdsduur_WAARDE)`, `Sluiten()` |
| uitvoerstroom | `Schrijven(int)`, `Schrijven(byte[])`, `Schrijven(byte[], starten, tijdsduur_WAARDE)`, `내보내기()`, `Sluiten()` |
| datagram_Kanaal | `Openen(poortnummer)`, `e_mailen(ADRES, poortnummer, tekst)`, `ontvangen()`, `TIMEOUT(밀리초)`, `poortnummer()`, `informatie_afgesloten()`, `Sluiten()` |
| verbinding_transport | `Openen(...)`, `수신열기(...)`는 위 Nederlands 객체를 Retour_HR |
| 검사 | `참인지(toestand, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Lezen()`의 bestand 끝은 -1, MATRIX_WAARDE 읽기의 반환값은 werkelijk_gegevens 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. poortnummer 0은 빈 번호를 자동 배정한다.
UDP 전문은 actueel_item Eigen 커널에서 512바이트까지 받으며, 주소는 cijfer_WAARDE IPv4를 사용한다.
`localhost` 루프백 외의 Naam 풀이(DNS)는 Eigen 커널에 아직 없다.

기존 `verbinding_transport.Verbinden/듣기/ontvangen`, `communicatie.Openen/e_mailen/ontvangen`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `verbinding`, `ontvangen_poort`, `datagram_Kanaal`를 쓴다.

## Nederlands uitzondering

모든 아래 클래스는 standaardwaarde 생성자, `새예외("설명")` 형태의 tekenreeks_WAARDE 생성자와
`설명()`을 제공한다. werkelijk_gegevens genereren 문법은 `new wachten_TIMEOUT_uitzondering("wachtstatus 끝")`이다.

| Nederlands uitzondering | 상위 les_WAARDE / 용도 |
|---|---|
| uitzondering | `java.lang.Exception`, 직접 던지는 일반 검사 uitzondering |
| uitvoerbewerking_uitzondering | `java.lang.RuntimeException` |
| I_O_uitzondering | `java.io.IOException`, Nederlands bestand·communicatie API의 검사 uitzondering |
| wachten_TIMEOUT_uitzondering | `I_O_uitzondering`, communicatie TIMEOUT 초과 |
| ADRES_ZOEKEN_uitzondering | `I_O_uitzondering`, ADRES bevestigen fout_WAARDE |
| 파일없음예외 | `I_O_uitzondering`, bestand Openen fout_WAARDE |
| communicatie_uitzondering | `I_O_uitzondering`, 표준 SocketException CONVERTEREN_WAARDE |
| nietig_argument_uitzondering | `java.lang.IllegalArgumentException` |
| nummer_opmaak_fout | `nietig_argument_uitzondering` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| LEEG_verwijzen_uitzondering | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Status_uitzondering | `java.lang.IllegalStateException` |
| TYPE_Weergeven_uitzondering | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| MATRIX_Store_fout | `java.lang.ArrayStoreException` |
| thread_Status_uitzondering | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 wachten_WAARDE 중단 |

`uitzondering`와 `uitvoerbewerking_uitzondering`는 모든 Nederlands 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, bestand·communicatie 전체를 잡으려면 `catch (I_O_uitzondering fout)`를 쓴다.
Nederlands API가 표준 I_O 오류를 Nederlands 예외로 변환한다.
기존 Nederlands communicatie 호출에서 `SocketTimeoutException`을 잡던 코드는
`wachten_TIMEOUT_uitzondering`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
uitzondering 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
actueel_item Eigen JVM에 이 20종을 추가했다. 임의의 gebruikersruimte Throwable 하위 les_WAARDE 전체를
지원하도록 확장했다는 뜻은 아니다.

## compileren_bron·Uitvoeren_opdracht

```sh
cd /home/user/jkoros/platforms/rpi4-native
make bouwen
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 tests/자바/한국어통신시험.java
python3 hulpmiddelen/Uitvoeren_Bestand.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 gebruikersruimte JVM ELF 안에 탑재된다. `.jar`는 host javac의
les_WAARDE 경로로 사용한다. bron_structuur 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Nederlands 예외의 `throws` 선언과 그 import를 인식한다.
Eigen JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·object_WAARDE·socket_WAARDE 예제 전체의 bron_structuur 컴파일은 host javac를 사용한다.
`/example/java/Bestandsvoorbeeld.java`는 게스트 javac로도 컴파일할 nummer 있다.

werkelijk_gegevens TCP/UDP 예제는 [Netwerkvoorbeeld.java](../../../example/java/Netwerkvoorbeeld.java),
Uitvoeren_opdracht 절차는 [example LEESMIJ_eb81d7d9](../../../example/README.md),
bron_structuur 명명 원칙은 [명명 LEESMIJ_eb81d7d9](../명명/LEESMIJ_eb81d7d9.md)에 있다.

## Swing Venster 예제

`/example/java/Venstervoorbeeld.java`와 컴파일된 `.class`가 machineopstart 시 준비된다.
`cd /example/java` Volgende_item `java Venstervoorbeeld`로 연다. Naam invoer_WAARDE, 인사하기 버튼,
인사말과 click_WAARDE herhaling_AANTAL vernieuwen, X 닫기를 지원한다.

| 기능 | Nederlands 직접 API |
|---|---|
| Runnable / run | `실행할일.Uitvoeren()` |
| ActionListener / actionPerformed | `동작받이.ontvangen_Actie(Actie_kennisgeving kennisgeving)` |
| ActionEvent | `Actie_kennisgeving.opdracht_sms()`, `gebeurtenisbron()`, `INDEX()` |
| JFrame | `Venster(venster_Titel, 폭, hoogte_WAARDE)`, `Toevoegen_element(scherm_element)`, `weergeven_venster()`, `Sluiten()`, `보이는가()` |
| JButton | `knop(tekst, 가로, Verticaal_functie, 폭, hoogte_WAARDE, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiket(...)`, `tekstveld(...)` |
| 공통 scherm element_WAARDE | `scherm_element.글읽기()`, `schrijven_sms(tekst)`, `자리정하기(가로, Verticaal_functie, 폭, hoogte_WAARDE)` |
| SwingUtilities.invokeLater | `gebeurtenis_wachtrij.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `achtergrondwerker(실행할일)`, `START_taak()`, `기다리기()`, `살아있는가()`, `RENDEMENT_taak()` |
| 명령행 | `starten()`, `실행인수.item_AANTAL()`, `실행인수.tekst(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
Eigen JVM의 `한국어화면호출`, `Proces_thread`가 Nederlands les_WAARDE·methode_WAARDE·서술자를
해석해 scherm 요소와 Uitvoeren_opdracht 가닥을 직접 만든다. Actie 알림도 Eigen 객체이며
콜백으로 `Uitvoeren`와 `ontvangen_Actie`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Uitvoeren_opdracht 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 Eigen JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 host JVM에서 무동작 객체가 생기지 않도록 하는 weigeren_WAARDE 경로다.
Eigen JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 implementatie API를
실행할 nummer 없다. host javac로 컴파일한 BACK_WAARDE Eigen JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, scherm 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Nederlands.Eigen.*;
public class 가닥예제 implements 실행할일 {
    public void Uitvoeren() { tekstuitvoer.schrijven_lijn("Nederlands 작업 Uitvoeren_opdracht"); }
    public static void starten() throws 대기중단예외 {
        achtergrondwerker thread_WAARDE = 작업.starten(new 가닥예제());
        작업.기다리기(thread_WAARDE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
MATRIX_WAARDE argumenten 대신 `실행인수`, 길이는 `문자.byte_AANTAL`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
Eigen 실행기는 argumenten 없는 `starten()`을 우선한다.
기존 Nederlands scherm 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.starten(Runnable)`을 사용하던 코드는 새 Nederlands 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API steun_WAARDE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 les_WAARDE·methode_WAARDE 이름과 서술자가 남는다.
Nederlands Naam 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·methode_WAARDE 재정의, native Verbinden, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS id_WAARDE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS methode_WAARDE verwijzen](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
