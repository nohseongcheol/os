# 한국어 Java 통신·U_I·izuzetak API

패키지는 `한국어.자체`다. organizator `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·Fajl·izuzetak API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 nit_VALUE API는 자체 JVM 전용이다.
기존 표준 Java biblioteka 전체의 한국어 번역판은 아니다.

```java
import 한국어.자체.*;

public class Mreža {
    public static void main(String[] Argumenti) throws U_I_izuzetak {
        veza Spoji_se = veza.Otvori("10.0.2.2", 9000);
        try {
            Spoji_se.TIMEOUT(700);
            Spoji_se.Ispis().Piši(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Spoji_se.입력();
            Ispis.수쓰기(입력.Čitaj());
        } catch (čekaj_TIMEOUT_izuzetak GRESKA) {
            Ispis.pisati_redak(GRESKA.설명());
        } finally {
            Spoji_se.Zatvori();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
korisnik 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 string_VALUE 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void Pokreni()`도 진입점으로 받는다.

## 통신과 tok_VALUE

| klasa_VALUE | 한국어 호출 |
|---|---|
| veza | `Otvori(adresa, broj_priključka)`, `입력()`, `Ispis()`, `TIMEOUT(밀리초)`, `broj_priključka()`, `lokalni_broj_priključka()`, `연결됨()`, `닫힘()`, `Zatvori()` |
| 수신창구 | `Otvori(broj_priključka)`, `받기()`, `broj_priključka()`, `TIMEOUT(밀리초)`, `닫힘()`, `Zatvori()` |
| 입력흐름 | `Čitaj()`, `Čitaj(byte[])`, `Čitaj(byte[], Pokreni, dužina_VALUE)`, `Zatvori()` |
| 출력흐름 | `Piši(int)`, `Piši(byte[])`, `Piši(byte[], Pokreni, dužina_VALUE)`, `내보내기()`, `Zatvori()` |
| 전문통로 | `Otvori(broj_priključka)`, `poslati(adresa, broj_priključka, Tekst)`, `받기()`, `TIMEOUT(밀리초)`, `broj_priključka()`, `닫힘()`, `Zatvori()` |
| 연결통신 | `Otvori(...)`, `수신열기(...)`는 위 한국어 객체를 vratiti_mjera |
| 검사 | `참인지(uvjet, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Čitaj()`의 Fajl 끝은 -1, niz_VALUE 읽기의 반환값은 stvaran_podaci 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. broj_priključka 0은 빈 번호를 자동 배정한다.
UDP 전문은 trenutno_stavka 자체 커널에서 512바이트까지 받으며, 주소는 cifra_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Naziv 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Spoji_se/slušati_završna_tačka/받기`, `통신.Otvori/poslati/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `veza`, `수신창구`, `전문통로`를 쓴다.

## 한국어 izuzetak

모든 아래 클래스는 zadana_vrijednost 생성자, `새예외("설명")` 형태의 string_VALUE 생성자와
`설명()`을 제공한다. stvaran_podaci generirati 문법은 `new čekaj_TIMEOUT_izuzetak("čekaj_stanje 끝")`이다.

| 한국어 izuzetak | 상위 klasa_VALUE / 용도 |
|---|---|
| izuzetak | `java.lang.Exception`, 직접 던지는 일반 검사 izuzetak |
| 실행예외 | `java.lang.RuntimeException` |
| U_I_izuzetak | `java.io.IOException`, 한국어 Fajl·통신 API의 검사 izuzetak |
| čekaj_TIMEOUT_izuzetak | `U_I_izuzetak`, 통신 TIMEOUT 초과 |
| adresa_LOOKUP_izuzetak | `U_I_izuzetak`, adresa potvrditi neuspjeh_VALUE |
| 파일없음예외 | `U_I_izuzetak`, Fajl Otvori neuspjeh_VALUE |
| 통신예외 | `U_I_izuzetak`, 표준 SocketException CONVERT_VALUE |
| nevažeće_argument_izuzetak | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `nevažeće_argument_izuzetak` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULL_Reference_izuzetak | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| stanje_izuzetak | `java.lang.IllegalStateException` |
| TYPE_Emitiranje_izuzetak | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| niz_Store_neuspjeh | `java.lang.ArrayStoreException` |
| nit_stanje_izuzetak | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 čekaj_VALUE 중단 |

`izuzetak`와 `실행예외`는 모든 한국어 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fajl·통신 전체를 잡으려면 `catch (U_I_izuzetak GRESKA)`를 쓴다.
한국어 API가 표준 U_I 오류를 한국어 예외로 변환한다.
기존 한국어 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`čekaj_TIMEOUT_izuzetak`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
izuzetak 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
trenutno_stavka 자체 JVM에 이 20종을 추가했다. 임의의 korisnik Throwable 하위 klasa_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## napraviti_izvor·Izvrši_komanda

```sh
cd /home/user/jkoros/platforms/rpi4-native
make verzija_sistem
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Alati/Izvrši_fajl.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 korisnik JVM ELF 안에 탑재된다. `.jar`는 organizator javac의
klasa_VALUE 경로로 사용한다. izvor_stablo 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 한국어 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objekt_VALUE·소켓 예제 전체의 izvor_stablo 컴파일은 organizator javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

stvaran_podaci TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
Izvrši_komanda 절차는 [example Pročitaj_me_eb81d7d9](../../../example/README.md),
izvor_stablo 명명 원칙은 [명명 Pročitaj_me_eb81d7d9](../명명/Pročitaj_me_eb81d7d9.md)에 있다.

## Swing prozor 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Dalje_stavka `java 창예제`로 연다. Naziv 입력, 인사하기 버튼,
인사말과 klik_VALUE 횟수 osvježiti, X 닫기를 지원한다.

| 기능 | 한국어 직접 API |
|---|---|
| Runnable / run | `실행할일.Izvrši()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.komanda_SMS()`, `događaj_izvor()`, `INDEX()` |
| JFrame | `prozor(prozor_Naslov, 폭, 높이)`, `dodati_element(화면구성요소)`, `program_prozor()`, `Zatvori()`, `보이는가()` |
| JButton | `dugme(Tekst, 가로, Vertikalno_položaj, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Oznaka(...)`, `SMS_polje(...)` |
| 공통 화면 element_VALUE | `화면구성요소.글읽기()`, `pisati_SMS(Tekst)`, `자리정하기(가로, Vertikalno_položaj, 폭, 높이)` |
| SwingUtilities.invokeLater | `događaj_redoslijed.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `START_zadatak()`, `기다리기()`, `살아있는가()`, `YIELD_zadatak()` |
| 명령행 | `Pokreni()`, `실행인수.stavka_COUNT()`, `실행인수.Tekst(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `proces_nit`가 한국어 klasa_VALUE·metoda_VALUE·서술자를
해석해 화면 요소와 Izvrši_komanda 가닥을 직접 만든다. radnja 알림도 자체 객체이며
콜백으로 `Izvrši`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Izvrši_komanda 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 organizator JVM에서 무동작 객체가 생기지 않도록 하는 odbiti_VALUE 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. organizator javac로 컴파일한 ZAD_VALUE 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import 한국어.자체.*;
public class 가닥예제 implements 실행할일 {
    public void Izvrši() { Ispis.pisati_redak("한국어 작업 Izvrši_komanda"); }
    public static void Pokreni() throws 대기중단예외 {
        작업가닥 nit_VALUE = 작업.Pokreni(new 가닥예제());
        작업.기다리기(nit_VALUE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
niz_VALUE Argumenti 대신 `실행인수`, 길이는 `문자.bajt_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 Argumenti 없는 `Pokreni()`을 우선한다.
기존 한국어 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Pokreni(Runnable)`을 사용하던 코드는 새 한국어 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Podrška_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 klasa_VALUE·metoda_VALUE 이름과 서술자가 남는다.
한국어 Naziv 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metoda_VALUE 재정의, native Spoji_se, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifikator_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metoda_VALUE Reference](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
