# Latviešu Java 통신·ievadizvade·izņēmums API

패키지는 `Latviešu.savs`다. viesot `javac --release 8`로 컴파일한 class를
savs ARM64 커널의 JVM에서 실행한다. 통신·Fails·izņēmums API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 saruna_VALUE API는 savs JVM 전용이다.
기존 표준 Java bibliotēka 전체의 Latviešu 번역판은 아니다.

```java
import Latviešu.savs.*;

public class tīkls {
    public static void main(String[] Parametri) throws ievadizvade_izņēmums {
        paziņa Savienoties = paziņa.Atvērt("10.0.2.2", 9000);
        try {
            Savienoties.NOILGUMS(700);
            Savienoties.Izvade().Rakstīt(문자.kodēt("안녕하세요\n"));
            ievades_straume 입력 = Savienoties.입력();
            Izvade.rakstīšana_numurs(입력.Lasīt());
        } catch (pagaidi_NOILGUMS_izņēmums Kļūda) {
            Izvade.rakstīšana_līnija(Kļūda.설명());
        } finally {
            Savienoties.Aizvērt();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
lietotājs 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 virkne_VALUE 리터럴에 사용하는 표준 클래스다. savs 실행기는 `public static void Palaist()`도 진입점으로 받는다.

## 통신과 Stream_VALUE

| klase_VALUE | Latviešu 호출 |
|---|---|
| paziņa | `Atvērt(adrese, porta_numurs)`, `입력()`, `Izvade()`, `NOILGUMS(밀리초)`, `porta_numurs()`, `vietējs_porta_numurs()`, `연결됨()`, `informācijas_tehnoloģija_slēgts()`, `Aizvērt()` |
| saņemt_ports | `Atvērt(porta_numurs)`, `saņemt()`, `porta_numurs()`, `NOILGUMS(밀리초)`, `informācijas_tehnoloģija_slēgts()`, `Aizvērt()` |
| ievades_straume | `Lasīt()`, `Lasīt(byte[])`, `Lasīt(byte[], Palaist, 길이)`, `Aizvērt()` |
| ražojums_Stream | `Rakstīt(int)`, `Rakstīt(byte[])`, `Rakstīt(byte[], Palaist, 길이)`, `내보내기()`, `Aizvērt()` |
| datogramma_Kanāls | `Atvērt(porta_numurs)`, `sūtīt(adrese, porta_numurs, Teksts)`, `saņemt()`, `NOILGUMS(밀리초)`, `porta_numurs()`, `informācijas_tehnoloģija_slēgts()`, `Aizvērt()` |
| paziņa_transportēšana | `Atvērt(...)`, `수신열기(...)`는 위 Latviešu 객체를 atdot_mērs |
| 검사 | `참인지(nosacījums, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Lasīt()`의 Fails 끝은 -1, ARRAY_VALUE 읽기의 반환값은 faktisks_dati 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. porta_numurs 0은 빈 번호를 자동 배정한다.
UDP 전문은 pašreizējais_krājums savs 커널에서 512바이트까지 받으며, 주소는 cipars_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Nosaukums 풀이(DNS)는 savs 커널에 아직 없다.

기존 `paziņa_transportēšana.Savienoties/klausīties_dalībnieks/saņemt`, `통신.Atvērt/sūtīt/saņemt`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `paziņa`, `saņemt_ports`, `datogramma_Kanāls`를 쓴다.

## Latviešu izņēmums

모든 아래 클래스는 noklusējuma_vērtība 생성자, `새예외("설명")` 형태의 virkne_VALUE 생성자와
`설명()`을 제공한다. faktisks_dati ģenerēt 문법은 `new pagaidi_NOILGUMS_izņēmums("nogaides_stāvoklis 끝")`이다.

| Latviešu izņēmums | 상위 klase_VALUE / 용도 |
|---|---|
| izņēmums | `java.lang.Exception`, 직접 던지는 일반 검사 izņēmums |
| 실행예외 | `java.lang.RuntimeException` |
| ievadizvade_izņēmums | `java.io.IOException`, Latviešu Fails·통신 API의 검사 izņēmums |
| pagaidi_NOILGUMS_izņēmums | `ievadizvade_izņēmums`, 통신 NOILGUMS 초과 |
| adrese_LOOKUP_izņēmums | `ievadizvade_izņēmums`, adrese verificēt kļūme_VALUE |
| 파일없음예외 | `ievadizvade_izņēmums`, Fails Atvērt kļūme_VALUE |
| 통신예외 | `ievadizvade_izņēmums`, 표준 SocketException CONVERT_VALUE |
| nederīgs_arg_izņēmums | `java.lang.IllegalArgumentException` |
| numurs_formāts_kļūme | `nederīgs_arg_izņēmums` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULL_Uzziņas_izņēmums | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Statuss_izņēmums | `java.lang.IllegalStateException` |
| TYPE_atskaņot_izņēmums | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARRAY_Store_kļūme | `java.lang.ArrayStoreException` |
| saruna_Statuss_izņēmums | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 pagaidi_VALUE 중단 |

`izņēmums`와 `실행예외`는 모든 Latviešu 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fails·통신 전체를 잡으려면 `catch (ievadizvade_izņēmums Kļūda)`를 쓴다.
Latviešu API가 표준 ievadizvade 오류를 Latviešu 예외로 변환한다.
기존 Latviešu 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`pagaidi_NOILGUMS_izņēmums`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
izņēmums 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
pašreizējais_krājums savs JVM에 이 20종을 추가했다. 임의의 lietotājs Throwable 하위 klase_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## kompilēt_avots·Izpildīt_komanda

```sh
cd /home/user/jkoros/platforms/rpi4-native
make būvējums_sistēma
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Rīki/Izpildīt_Fails.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 lietotājs JVM ELF 안에 탑재된다. `.jar`는 viesot javac의
klase_VALUE 경로로 사용한다. avots_koks 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Latviešu 예외의 `throws` 선언과 그 import를 인식한다.
savs JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objekts_VALUE·소켓 예제 전체의 avots_koks 컴파일은 viesot javac를 사용한다.
`/example/java/DatnesPiemērs.java`는 게스트 javac로도 컴파일할 numurs 있다.

faktisks_dati TCP/UDP 예제는 [TīklaPiemērs.java](../../../example/java/TīklaPiemērs.java),
Izpildīt_komanda 절차는 [example fails_Lasi_mani_eb81d7d9](../../../example/README.md),
avots_koks 명명 원칙은 [명명 fails_Lasi_mani_eb81d7d9](../명명/fails_Lasi_mani_eb81d7d9.md)에 있다.

## Swing Logs 예제

`/example/java/LogaPiemērs.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Tālāk_krājums `java LogaPiemērs`로 연다. Nosaukums 입력, 인사하기 버튼,
인사말과 klikšķis_VALUE 횟수 atsvaidzināt, X 닫기를 지원한다.

| 기능 | Latviešu 직접 API |
|---|---|
| Runnable / run | `실행할일.Izpildīt()` |
| ActionListener / actionPerformed | `동작받이.saņemt_darbība(darbība_informēšana informēšana)` |
| ActionEvent | `darbība_informēšana.komanda_SMS()`, `notikuma_avots()`, `INDEX()` |
| JFrame | `Logs(logs_nosaukums, 폭, 높이)`, `Pievienot_elements(화면구성요소)`, `rādīt_logs()`, `Aizvērt()`, `보이는가()` |
| JButton | `Pogas(Teksts, 가로, vertikāle_amats, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiķete(...)`, `teksta_lauks(...)` |
| 공통 화면 elements_VALUE | `화면구성요소.글읽기()`, `rakstīšana_SMS(Teksts)`, `자리정하기(가로, vertikāle_amats, 폭, 높이)` |
| SwingUtilities.invokeLater | `notikums_rinda.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `nodarbinātais(실행할일)`, `Sākt_uzdevums()`, `기다리기()`, `살아있는가()`, `YIELD_uzdevums()` |
| 명령행 | `Palaist()`, `실행인수.krājums_COUNT()`, `실행인수.Teksts(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
savs JVM의 `한국어화면호출`, `Process_saruna`가 Latviešu klase_VALUE·metode_VALUE·서술자를
해석해 화면 요소와 Izpildīt_komanda 가닥을 직접 만든다. Darbība 알림도 savs 객체이며
콜백으로 `Izpildīt`와 `saņemt_darbība`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Izpildīt_komanda 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 savs JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 viesot JVM에서 무동작 객체가 생기지 않도록 하는 noraidīt_VALUE 경로다.
savs JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 numurs 없다. viesot javac로 컴파일한 ATPAKAĻ_VALUE savs JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Latviešu.savs.*;
public class 가닥예제 implements 실행할일 {
    public void Izpildīt() { Izvade.rakstīšana_līnija("Latviešu 작업 Izpildīt_komanda"); }
    public static void Palaist() throws 대기중단예외 {
        nodarbinātais saruna_VALUE = 작업.Palaist(new 가닥예제());
        작업.기다리기(saruna_VALUE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARRAY_VALUE Parametri 대신 `실행인수`, 길이는 `문자.byte_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
savs 실행기는 Parametri 없는 `Palaist()`을 우선한다.
기존 Latviešu 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Palaist(Runnable)`을 사용하던 코드는 새 Latviešu 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Atbalsts_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 klase_VALUE·metode_VALUE 이름과 서술자가 남는다.
Latviešu Nosaukums 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metode_VALUE 재정의, native Savienoties, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifikators_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metode_VALUE Uzziņas](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
