# Euskara Java 통신·S_I·salbuespen API

패키지는 `Euskara.자체`다. Ostalari `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·Fitxategia·salbuespen API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 hari_balio API는 자체 JVM 전용이다.
기존 표준 Java liburutegi 전체의 Euskara 번역판은 아니다.

```java
import Euskara.자체.*;

public class sare {
    public static void main(String[] Argumentuak) throws S_I_salbuespen {
        konexio Konektatu = konexio.Ireki("10.0.2.2", 9000);
        try {
            Konektatu.DENBORA_MUGA(700);
            Konektatu.Irteera().Idatzi(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Konektatu.입력();
            Irteera.수쓰기(입력.Irakurri());
        } catch (itxaron_DENBORA_MUGA_salbuespen errorea) {
            Irteera.idatzi_lerro(errorea.설명());
        } finally {
            Konektatu.Itxi();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
erabiltzaile 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 kate_balio 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void Exekutatu_2()`도 진입점으로 받는다.

## 통신과 Stream_balio

| Gela_balio | Euskara 호출 |
|---|---|
| konexio | `Ireki(helbide, ataka_zenbaki)`, `입력()`, `Irteera()`, `DENBORA_MUGA(밀리초)`, `ataka_zenbaki()`, `lokal_ataka_zenbaki()`, `연결됨()`, `닫힘()`, `Itxi()` |
| 수신창구 | `Ireki(ataka_zenbaki)`, `받기()`, `ataka_zenbaki()`, `DENBORA_MUGA(밀리초)`, `닫힘()`, `Itxi()` |
| 입력흐름 | `Irakurri()`, `Irakurri(byte[])`, `Irakurri(byte[], Exekutatu_2, luzera_balio)`, `Itxi()` |
| 출력흐름 | `Idatzi(int)`, `Idatzi(byte[])`, `Idatzi(byte[], Exekutatu_2, luzera_balio)`, `내보내기()`, `Itxi()` |
| 전문통로 | `Ireki(ataka_zenbaki)`, `bidali(helbide, ataka_zenbaki, Testua)`, `받기()`, `DENBORA_MUGA(밀리초)`, `ataka_zenbaki()`, `닫힘()`, `Itxi()` |
| 연결통신 | `Ireki(...)`, `수신열기(...)`는 위 Euskara 객체를 itzuli_neurria |
| 검사 | `참인지(baldintza, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Irakurri()`의 Fitxategia 끝은 -1, matrize_balio 읽기의 반환값은 benetako_datuak 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. ataka_zenbaki 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 자체 커널에서 512바이트까지 받으며, 주소는 digitu_balio IPv4를 사용한다.
`localhost` 루프백 외의 Izena 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Konektatu/entzun_amaiera_puntu/받기`, `통신.Ireki/bidali/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `konexio`, `수신창구`, `전문통로`를 쓴다.

## Euskara salbuespen

모든 아래 클래스는 balio_lehenetsi 생성자, `새예외("설명")` 형태의 kate_balio 생성자와
`설명()`을 제공한다. benetako_datuak sortu 문법은 `new itxaron_DENBORA_MUGA_salbuespen("itxaron_Egoera 끝")`이다.

| Euskara salbuespen | 상위 Gela_balio / 용도 |
|---|---|
| salbuespen | `java.lang.Exception`, 직접 던지는 일반 검사 salbuespen |
| 실행예외 | `java.lang.RuntimeException` |
| S_I_salbuespen | `java.io.IOException`, Euskara Fitxategia·통신 API의 검사 salbuespen |
| itxaron_DENBORA_MUGA_salbuespen | `S_I_salbuespen`, 통신 DENBORA_MUGA 초과 |
| helbide_BEGIRATU_salbuespen | `S_I_salbuespen`, helbide egiaztatu hutsegite_balio |
| 파일없음예외 | `S_I_salbuespen`, Fitxategia Ireki hutsegite_balio |
| 통신예외 | `S_I_salbuespen`, 표준 SocketException BIHURTU_balio |
| baliogabe_arg_salbuespen | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `baliogabe_arg_salbuespen` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| nulu_Erreferentzia_materiala_salbuespen | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Egoera_salbuespen | `java.lang.IllegalStateException` |
| MOTA_igorri_salbuespen | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| matrize_Store_hutsegite | `java.lang.ArrayStoreException` |
| hari_Egoera_salbuespen | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 itxaron_balio 중단 |

`salbuespen`와 `실행예외`는 모든 Euskara 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fitxategia·통신 전체를 잡으려면 `catch (S_I_salbuespen errorea)`를 쓴다.
Euskara API가 표준 S_I 오류를 Euskara 예외로 변환한다.
기존 Euskara 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`itxaron_DENBORA_MUGA_salbuespen`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
salbuespen 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 자체 JVM에 이 20종을 추가했다. 임의의 erabiltzaile Throwable 하위 Gela_balio 전체를
지원하도록 확장했다는 뜻은 아니다.

## eraiki_iturburu·exekutatu_komando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make eraiki_sistema
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Tresnak/exekutatu_fitxategi.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 erabiltzaile JVM ELF 안에 탑재된다. `.jar`는 Ostalari javac의
Gela_balio 경로로 사용한다. iturburu_zuhaitz 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Euskara 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objektu_balio·소켓 예제 전체의 iturburu_zuhaitz 컴파일은 Ostalari javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

benetako_datuak TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
exekutatu_komando 절차는 [example IRAKHAU_eb81d7d9](../../../example/README.md),
iturburu_zuhaitz 명명 원칙은 [명명 IRAKHAU_eb81d7d9](../명명/IRAKHAU_eb81d7d9.md)에 있다.

## Swing Leihoa 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Hurrengoa_elementu `java 창예제`로 연다. Izena 입력, 인사하기 버튼,
인사말과 klik_balio 횟수 freskatu, X 닫기를 지원한다.

| 기능 | Euskara 직접 API |
|---|---|
| Runnable / run | `실행할일.Exekutatu()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.komando_SMS()`, `gertaera_iturburu()`, `INDIZE()` |
| JFrame | `Leihoa(leiho_Izenburua, 폭, 높이)`, `gehitu_elementu(화면구성요소)`, `erakutsi_leiho()`, `Itxi()`, `보이는가()` |
| JButton | `botoia(Testua, 가로, Bertikala_kargu, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiketa(...)`, `SMS_eremu(...)` |
| 공통 화면 elementu_balio | `화면구성요소.글읽기()`, `idatzi_SMS(Testua)`, `자리정하기(가로, Bertikala_kargu, 폭, 높이)` |
| SwingUtilities.invokeLater | `gertaera_ilara.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `HASI_ataza()`, `기다리기()`, `살아있는가()`, `YIELD_ataza()` |
| 명령행 | `Exekutatu_2()`, `실행인수.elementu_ZENBATU()`, `실행인수.Testua(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `prozesu_hari`가 Euskara Gela_balio·메서드·서술자를
해석해 화면 요소와 exekutatu_komando 가닥을 직접 만든다. Ekintza 알림도 자체 객체이며
콜백으로 `Exekutatu`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 exekutatu_komando 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 Ostalari JVM에서 무동작 객체가 생기지 않도록 하는 baztertu_balio 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. Ostalari javac로 컴파일한 ATZERA_balio 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Euskara.자체.*;
public class 가닥예제 implements 실행할일 {
    public void Exekutatu() { Irteera.idatzi_lerro("Euskara 작업 exekutatu_komando"); }
    public static void Exekutatu_2() throws 대기중단예외 {
        작업가닥 hari_balio = 작업.Exekutatu_2(new 가닥예제());
        작업.기다리기(hari_balio);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
matrize_balio Argumentuak 대신 `실행인수`, 길이는 `문자.byte_ZENBATU`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 Argumentuak 없는 `Exekutatu_2()`을 우선한다.
기존 Euskara 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Exekutatu_2(Runnable)`을 사용하던 코드는 새 Euskara 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Laguntza_balio 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Gela_balio·메서드 이름과 서술자가 남는다.
Euskara Izena 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·메서드 재정의, native Konektatu, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifikatzaile_balio](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS 메서드 Erreferentzia_materiala](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
