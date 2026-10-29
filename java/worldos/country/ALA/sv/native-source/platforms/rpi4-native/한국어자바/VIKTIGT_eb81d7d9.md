# Svenska Java kommunikation·indata_utleverans·fel_31f743d2 API

패키지는 `Svenska.eget`다. värd `javac --release 8`로 컴파일한 class를
eget ARM64 커널의 JVM에서 실행한다. kommunikation·filnamn·fel_31f743d2 API는 OpenJDK와 대조한다. 아래의 직접 구현한 skärmbild·작업 tråd_värde API는 eget JVM 전용이다.
기존 표준 Java bibliotek 전체의 Svenska 번역판은 아니다.

```java
import Svenska.eget.*;

public class nätverk {
    public static void main(String[] argument) throws indata_utleverans_fel {
        kontakt Anslut = kontakt.Öppna("10.0.2.2", 9000);
        try {
            Anslut.TIMEOUT(700);
            Anslut.utmatningsposition().Skriv(문자.koda("안녕하세요\n"));
            indataström indata_värde = Anslut.indata_värde();
            utmatningsposition.skriva_nummer(indata_värde.Läs());
        } catch (vänta_TIMEOUT_fel fel) {
            utmatningsposition.skriva_rad(fel.설명());
        } finally {
            Anslut.Stäng();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
användarutrymme 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 sträng_värde 리터럴에 사용하는 표준 클래스다. eget 실행기는 `public static void Kör()`도 진입점으로 받는다.

## 통신과 flöde_värde

| Kurs_värde | Svenska 호출 |
|---|---|
| kontakt | `Öppna(Adress, portnummer)`, `indata_värde()`, `utmatningsposition()`, `TIMEOUT(밀리초)`, `portnummer()`, `lokal_portnummer()`, `연결됨()`, `informationsteknik_stängd()`, `Stäng()` |
| få_port | `Öppna(portnummer)`, `få()`, `portnummer()`, `TIMEOUT(밀리초)`, `informationsteknik_stängd()`, `Stäng()` |
| indataström | `Läs()`, `Läs(byte[])`, `Läs(byte[], Kör, längd_värde)`, `Stäng()` |
| utdataström | `Skriv(int)`, `Skriv(byte[])`, `Skriv(byte[], Kör, längd_värde)`, `내보내기()`, `Stäng()` |
| datagram_Kanal | `Öppna(portnummer)`, `skicka(Adress, portnummer, text)`, `få()`, `TIMEOUT(밀리초)`, `portnummer()`, `informationsteknik_stängd()`, `Stäng()` |
| kontakt_transport | `Öppna(...)`, `수신열기(...)`는 위 Svenska 객체를 Retur_KR |
| 검사 | `참인지(villkor, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Läs()`의 filnamn 끝은 -1, MATRIS_värde 읽기의 반환값은 verklig_data 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. portnummer 0은 빈 번호를 자동 배정한다.
UDP 전문은 aktuellt_objekt eget 커널에서 512바이트까지 받으며, 주소는 siffra_värde IPv4를 사용한다.
`localhost` 루프백 외의 Namn 풀이(DNS)는 eget 커널에 아직 없다.

기존 `kontakt_transport.Anslut/lyssna_deltagare/få`, `kommunikation.Öppna/skicka/få`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `kontakt`, `få_port`, `datagram_Kanal`를 쓴다.

## Svenska fel_31f743d2

모든 아래 클래스는 standardvärde 생성자, `새예외("설명")` 형태의 sträng_värde 생성자와
`설명()`을 제공한다. verklig_data generera 문법은 `new vänta_TIMEOUT_fel("tillståndet_Vänta 끝")`이다.

| Svenska fel_31f743d2 | 상위 Kurs_värde / 용도 |
|---|---|
| fel_31f743d2 | `java.lang.Exception`, 직접 던지는 일반 검사 fel_31f743d2 |
| körning_fel | `java.lang.RuntimeException` |
| indata_utleverans_fel | `java.io.IOException`, Svenska filnamn·kommunikation API의 검사 fel_31f743d2 |
| vänta_TIMEOUT_fel | `indata_utleverans_fel`, kommunikation TIMEOUT 초과 |
| ADRESS_LETAUPP_fel | `indata_utleverans_fel`, Adress verifiera fel_värde |
| 파일없음예외 | `indata_utleverans_fel`, filnamn Öppna fel_värde |
| kommunikation_fel | `indata_utleverans_fel`, 표준 SocketException KONVERTERA_värde |
| ogiltig_argument_fel | `java.lang.IllegalArgumentException` |
| nummer_format_fel | `ogiltig_argument_fel` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| null_referens_fel | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| status_fel | `java.lang.IllegalStateException` |
| Typ_Sänd_fel | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| MATRIS_Store_fel | `java.lang.ArrayStoreException` |
| tråd_status_fel | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 vänta_värde 중단 |

`fel_31f743d2`와 `körning_fel`는 모든 Svenska 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, filnamn·kommunikation 전체를 잡으려면 `catch (indata_utleverans_fel fel)`를 쓴다.
Svenska API가 표준 indata_utleverans 오류를 Svenska 예외로 변환한다.
기존 Svenska kommunikation 호출에서 `SocketTimeoutException`을 잡던 코드는
`vänta_TIMEOUT_fel`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
fel_31f743d2 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
aktuellt_objekt eget JVM에 이 20종을 추가했다. 임의의 användarutrymme Throwable 하위 Kurs_värde 전체를
지원하도록 확장했다는 뜻은 아니다.

## kompilera_källa·köra_kommando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make version_System
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 tester/자바/한국어통신시험.java
python3 verktyg/köra_fil.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 användarutrymme JVM ELF 안에 탑재된다. `.jar`는 värd javac의
Kurs_värde 경로로 사용한다. källa_träd 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Svenska 예외의 `throws` 선언과 그 import를 인식한다.
eget JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objekt_värde·socket_värde 예제 전체의 källa_träd 컴파일은 värd javac를 사용한다.
`/example/java/Filexempel.java`는 게스트 javac로도 컴파일할 nummer 있다.

verklig_data TCP/UDP 예제는 [Nätverksexempel.java](../../../example/java/Nätverksexempel.java),
köra_kommando 절차는 [example VIKTIGT_eb81d7d9](../../../example/README.md),
källa_träd 명명 원칙은 [명명 VIKTIGT_eb81d7d9](../명명/VIKTIGT_eb81d7d9.md)에 있다.

## Swing Fönster 예제

`/example/java/Fönsterexempel.java`와 컴파일된 `.class`가 maskinstart 시 준비된다.
`cd /example/java` Nästa_objekt `java Fönsterexempel`로 연다. Namn indata_värde, 인사하기 버튼,
인사말과 klick_värde repetition_ANTAL uppdatera, X 닫기를 지원한다.

| 기능 | Svenska 직접 API |
|---|---|
| Runnable / run | `실행할일.Starta()` |
| ActionListener / actionPerformed | `동작받이.få_Action(동작알림 알림)` |
| ActionEvent | `동작알림.kommando_SMS()`, `händelsekälla()`, `INDEX()` |
| JFrame | `Fönster(fönster_titel, 폭, 높이)`, `Lägg_till_element(skärmbild_element)`, `visa_fönster()`, `Stäng()`, `보이는가()` |
| JButton | `knapp(text, 가로, bransch_placera, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etikett(...)`, `textfält(...)` |
| 공통 skärmbild element_värde | `skärmbild_element.läsa_SMS()`, `skriva_SMS(text)`, `자리정하기(가로, bransch_placera, 폭, 높이)` |
| SwingUtilities.invokeLater | `händelse_kö.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `arbete(실행할일)`, `START_uppgift()`, `기다리기()`, `살아있는가()`, `NOMAVK_uppgift()` |
| 명령행 | `Kör()`, `실행인수.objekt_ANTAL()`, `실행인수.text(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
eget JVM의 `한국어화면호출`, `Process_tråd`가 Svenska Kurs_värde·metod_värde·서술자를
해석해 skärmbild 요소와 köra_kommando 가닥을 직접 만든다. Åtgärd 알림도 eget 객체이며
콜백으로 `Starta`와 `få_Action`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 köra_kommando 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 eget JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 värd JVM에서 무동작 객체가 생기지 않도록 하는 avvisa_värde 경로다.
eget JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 implementation API를
실행할 nummer 없다. värd javac로 컴파일한 BACK_värde eget JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, skärmbild 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Svenska.eget.*;
public class 가닥예제 implements 실행할일 {
    public void Starta() { utmatningsposition.skriva_rad("Svenska 작업 köra_kommando"); }
    public static void Kör() throws 대기중단예외 {
        arbete tråd_värde = 작업.Kör(new 가닥예제());
        작업.기다리기(tråd_värde);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
MATRIS_värde argument 대신 `실행인수`, 길이는 `문자.byte_ANTAL`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
eget 실행기는 argument 없는 `Kör()`을 우선한다.
기존 Svenska skärmbild 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Kör(Runnable)`을 사용하던 코드는 새 Svenska 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API stöd_värde 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Kurs_värde·metod_värde 이름과 서술자가 남는다.
Svenska Namn 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metod_värde 재정의, native Anslut, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifierare_värde](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metod_värde referens](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
