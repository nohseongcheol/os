# norsk Java 통신·I_U·unntak API

패키지는 `norsk.eget`다. vert `javac --release 8`로 컴파일한 class를
eget ARM64 커널의 JVM에서 실행한다. 통신·Fil·unntak API는 OpenJDK와 대조한다. 아래의 직접 구현한 skjermbilde·작업 tråd_VERDI API는 eget JVM 전용이다.
기존 표준 Java bibliotek 전체의 norsk 번역판은 아니다.

```java
import norsk.eget.*;

public class nettverk {
    public static void main(String[] Argumenter) throws I_U_unntak {
        kontakt Koble_til = kontakt.Åpne("10.0.2.2", 9000);
        try {
            Koble_til.TIMEOUT(700);
            Koble_til.Utgang().Skriv(문자.부호화("안녕하세요\n"));
            inndataflyt inndata_VERDI = Koble_til.inndata_VERDI();
            Utgang.skrive_nummer(inndata_VERDI.Les());
        } catch (vent_TIMEOUT_unntak feil) {
            Utgang.skrive_linje(feil.설명());
        } finally {
            Koble_til.Lukk();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
bruker 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 streng_VERDI 리터럴에 사용하는 표준 클래스다. eget 실행기는 `public static void Kjør_2()`도 진입점으로 받는다.

## 통신과 strøm_VERDI

| time_VERDI | norsk 호출 |
|---|---|
| kontakt | `Åpne(e_post, portnummer)`, `inndata_VERDI()`, `Utgang()`, `TIMEOUT(밀리초)`, `portnummer()`, `lokal_portnummer()`, `연결됨()`, `informasjonssystemer_lukket()`, `Lukk()` |
| motta_port | `Åpne(portnummer)`, `motta()`, `portnummer()`, `TIMEOUT(밀리초)`, `informasjonssystemer_lukket()`, `Lukk()` |
| inndataflyt | `Les()`, `Les(byte[])`, `Les(byte[], Kjør_2, lengde_VERDI)`, `Lukk()` |
| utdataflyt | `Skriv(int)`, `Skriv(byte[])`, `Skriv(byte[], Kjør_2, lengde_VERDI)`, `내보내기()`, `Lukk()` |
| datagram_Kanal | `Åpne(portnummer)`, `sende(e_post, portnummer, Tekst)`, `motta()`, `TIMEOUT(밀리초)`, `portnummer()`, `informasjonssystemer_lukket()`, `Lukk()` |
| kontakt_transport | `Åpne(...)`, `수신열기(...)`는 위 norsk 객체를 return_KR |
| 검사 | `참인지(vilkår, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Les()`의 Fil 끝은 -1, MATRISE_VERDI 읽기의 반환값은 faktisk_data 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. portnummer 0은 빈 번호를 자동 배정한다.
UDP 전문은 betalt_vare eget 커널에서 512바이트까지 받으며, 주소는 siffer_VERDI IPv4를 사용한다.
`localhost` 루프백 외의 Navn 풀이(DNS)는 eget 커널에 아직 없다.

기존 `kontakt_transport.Koble_til/듣기/motta`, `통신.Åpne/sende/motta`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `kontakt`, `motta_port`, `datagram_Kanal`를 쓴다.

## norsk unntak

모든 아래 클래스는 standardverdi 생성자, `새예외("설명")` 형태의 streng_VERDI 생성자와
`설명()`을 제공한다. faktisk_data generere 문법은 `new vent_TIMEOUT_unntak("ventende_tilstand 끝")`이다.

| norsk unntak | 상위 time_VERDI / 용도 |
|---|---|
| unntak | `java.lang.Exception`, 직접 던지는 일반 검사 unntak |
| kjøring_unntak | `java.lang.RuntimeException` |
| I_U_unntak | `java.io.IOException`, norsk Fil·통신 API의 검사 unntak |
| vent_TIMEOUT_unntak | `I_U_unntak`, 통신 TIMEOUT 초과 |
| e_post_Oppslag_unntak | `I_U_unntak`, e_post bekrefte feil_VERDI |
| 파일없음예외 | `I_U_unntak`, Fil Åpne feil_VERDI |
| 통신예외 | `I_U_unntak`, 표준 SocketException KONVERTER_VERDI |
| ugyldig_argument_unntak | `java.lang.IllegalArgumentException` |
| nummer_format_feil | `ugyldig_argument_unntak` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULL_referere_unntak | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| status_unntak | `java.lang.IllegalStateException` |
| Type_strømme_unntak | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| MATRISE_Store_feil | `java.lang.ArrayStoreException` |
| tråd_status_unntak | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 vent_VERDI 중단 |

`unntak`와 `kjøring_unntak`는 모든 norsk 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fil·통신 전체를 잡으려면 `catch (I_U_unntak feil)`를 쓴다.
norsk API가 표준 I_U 오류를 norsk 예외로 변환한다.
기존 norsk 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`vent_TIMEOUT_unntak`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
unntak 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
betalt_vare eget JVM에 이 20종을 추가했다. 임의의 bruker Throwable 하위 time_VERDI 전체를
지원하도록 확장했다는 뜻은 아니다.

## kompilere_kilde·Utfør_kommando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make bygg_System
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Verktøy/Utfør_Fil.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 bruker JVM ELF 안에 탑재된다. `.jar`는 vert javac의
time_VERDI 경로로 사용한다. kilde_tre 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 norsk 예외의 `throws` 선언과 그 import를 인식한다.
eget JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objekt_VERDI·socket_VERDI 예제 전체의 kilde_tre 컴파일은 vert javac를 사용한다.
`/example/java/Fileksempel.java`는 게스트 javac로도 컴파일할 nummer 있다.

faktisk_data TCP/UDP 예제는 [Nettverkseksempel.java](../../../example/java/Nettverkseksempel.java),
Utfør_kommando 절차는 [example Viktig_fil_eb81d7d9](../../../example/README.md),
kilde_tre 명명 원칙은 [명명 Viktig_fil_eb81d7d9](../명명/Viktig_fil_eb81d7d9.md)에 있다.

## Swing Vindu 예제

`/example/java/Vinduseksempel.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Neste_vare `java Vinduseksempel`로 연다. Navn inndata_VERDI, 인사하기 버튼,
인사말과 klikk_VERDI 횟수 oppdatere, X 닫기를 지원한다.

| 기능 | norsk 직접 API |
|---|---|
| Runnable / run | `실행할일.Kjør()` |
| ActionListener / actionPerformed | `동작받이.motta_Gjøremål(Gjøremål_notice notice)` |
| ActionEvent | `Gjøremål_notice.kommando_SMS()`, `hendelseskilde()`, `INDEKS()` |
| JFrame | `Vindu(vindu_Tittel, 폭, 높이)`, `Legg_til_element(skjermbilde_element)`, `vise_vindu()`, `Lukk()`, `보이는가()` |
| JButton | `Knapp(Tekst, 가로, vertikal_plassere, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etikett(...)`, `tekstfelt(...)` |
| 공통 skjermbilde element_VERDI | `skjermbilde_element.글읽기()`, `skrive_SMS(Tekst)`, `자리정하기(가로, vertikal_plassere, 폭, 높이)` |
| SwingUtilities.invokeLater | `hendelse_kø.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `arbeider(실행할일)`, `START_oppgave()`, `기다리기()`, `살아있는가()`, `AVKAST_oppgave()` |
| 명령행 | `Kjør_2()`, `실행인수.vare_ANTALL()`, `실행인수.Tekst(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
eget JVM의 `한국어화면호출`, `Prosess_tråd`가 norsk time_VERDI·metode_VERDI·서술자를
해석해 skjermbilde 요소와 Utfør_kommando 가닥을 직접 만든다. Handling 알림도 eget 객체이며
콜백으로 `Kjør`와 `motta_Gjøremål`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Utfør_kommando 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 eget JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 vert JVM에서 무동작 객체가 생기지 않도록 하는 avvise_VERDI 경로다.
eget JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 nummer 없다. vert javac로 컴파일한 TILBAKE_VERDI eget JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, skjermbilde 큐 기능은 `SwingUtilities`에 해당한다.

```java
import norsk.eget.*;
public class 가닥예제 implements 실행할일 {
    public void Kjør() { Utgang.skrive_linje("norsk 작업 Utfør_kommando"); }
    public static void Kjør_2() throws 대기중단예외 {
        arbeider tråd_VERDI = 작업.Kjør_2(new 가닥예제());
        작업.기다리기(tråd_VERDI);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
MATRISE_VERDI Argumenter 대신 `실행인수`, 길이는 `문자.byte_ANTALL`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
eget 실행기는 Argumenter 없는 `Kjør_2()`을 우선한다.
기존 norsk skjermbilde 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Kjør_2(Runnable)`을 사용하던 코드는 새 norsk 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API støtte_VERDI 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 time_VERDI·metode_VERDI 이름과 서술자가 남는다.
norsk Navn 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metode_VERDI 재정의, native Koble_til, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifikator_VERDI](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metode_VERDI referere](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
