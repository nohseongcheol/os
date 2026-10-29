# Cymraeg Java 통신·I_O·eithriad API

패키지는 `Cymraeg.자체`다. lletya `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·Ffeil·eithriad API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 edefyn_VALUE API는 자체 JVM 전용이다.
기존 표준 Java llyfrgell 전체의 Cymraeg 번역판은 아니다.

```java
import Cymraeg.자체.*;

public class Rhwydwaith {
    public static void main(String[] 인수) throws I_O_eithriad {
        cyswllt Cysylltu = cyswllt.Agor("10.0.2.2", 9000);
        try {
            Cysylltu.TIMEOUT(700);
            Cysylltu.Allbwn().Ysgrifennu(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Cysylltu.입력();
            Allbwn.수쓰기(입력.Darllen());
        } catch (aros_TIMEOUT_eithriad Gwall) {
            Allbwn.ysgrifennu_llinell(Gwall.설명());
        } finally {
            Cysylltu.Cau();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
defnyddiwr 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 testun_VALUE 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void Gweithredu_2()`도 진입점으로 받는다.

## 통신과 ffrwd_VALUE

| Dosbarth_VALUE | Cymraeg 호출 |
|---|---|
| cyswllt | `Agor(ADDRESS, rhif_porth)`, `입력()`, `Allbwn()`, `TIMEOUT(밀리초)`, `rhif_porth()`, `lleol_rhif_porth()`, `연결됨()`, `닫힘()`, `Cau()` |
| 수신창구 | `Agor(rhif_porth)`, `받기()`, `rhif_porth()`, `TIMEOUT(밀리초)`, `닫힘()`, `Cau()` |
| 입력흐름 | `Darllen()`, `Darllen(byte[])`, `Darllen(byte[], Gweithredu_2, hyd_VALUE)`, `Cau()` |
| 출력흐름 | `Ysgrifennu(int)`, `Ysgrifennu(byte[])`, `Ysgrifennu(byte[], Gweithredu_2, hyd_VALUE)`, `내보내기()`, `Cau()` |
| 전문통로 | `Agor(rhif_porth)`, `anfon(ADDRESS, rhif_porth, Testun)`, `받기()`, `TIMEOUT(밀리초)`, `rhif_porth()`, `닫힘()`, `Cau()` |
| 연결통신 | `Agor(...)`, `수신열기(...)`는 위 Cymraeg 객체를 return_mesur |
| 검사 | `참인지(cyflwr, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Darllen()`의 Ffeil 끝은 -1, ARAE_VALUE 읽기의 반환값은 go_iawn_data 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. rhif_porth 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 자체 커널에서 512바이트까지 받으며, 주소는 digid_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Enw 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Cysylltu/듣기/받기`, `통신.Agor/anfon/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `cyswllt`, `수신창구`, `전문통로`를 쓴다.

## Cymraeg eithriad

모든 아래 클래스는 gwerth_diofyn 생성자, `새예외("설명")` 형태의 testun_VALUE 생성자와
`설명()`을 제공한다. go_iawn_data cynhyrchu 문법은 `new aros_TIMEOUT_eithriad("aros_cyflwr 끝")`이다.

| Cymraeg eithriad | 상위 Dosbarth_VALUE / 용도 |
|---|---|
| eithriad | `java.lang.Exception`, 직접 던지는 일반 검사 eithriad |
| 실행예외 | `java.lang.RuntimeException` |
| I_O_eithriad | `java.io.IOException`, Cymraeg Ffeil·통신 API의 검사 eithriad |
| aros_TIMEOUT_eithriad | `I_O_eithriad`, 통신 TIMEOUT 초과 |
| ADDRESS_LOOKUP_eithriad | `I_O_eithriad`, ADDRESS dilysu methiant_VALUE |
| 파일없음예외 | `I_O_eithriad`, Ffeil Agor methiant_VALUE |
| 통신예외 | `I_O_eithriad`, 표준 SocketException CONVERT_VALUE |
| annilys_arg_eithriad | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `annilys_arg_eithriad` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NWL_cyfeiriad_eithriad | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| cyflwr_eithriad | `java.lang.IllegalStateException` |
| TYPE_Castio_eithriad | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARAE_Store_methiant | `java.lang.ArrayStoreException` |
| edefyn_cyflwr_eithriad | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 aros_VALUE 중단 |

`eithriad`와 `실행예외`는 모든 Cymraeg 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Ffeil·통신 전체를 잡으려면 `catch (I_O_eithriad Gwall)`를 쓴다.
Cymraeg API가 표준 I_O 오류를 Cymraeg 예외로 변환한다.
기존 Cymraeg 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`aros_TIMEOUT_eithriad`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
eithriad 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 자체 JVM에 이 20종을 추가했다. 임의의 defnyddiwr Throwable 하위 Dosbarth_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## llunio_ffynhonnell·Gweithredu_gorchymyn

```sh
cd /home/user/jkoros/platforms/rpi4-native
make llunio_system
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Offer/Gweithredu_ffeil.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 defnyddiwr JVM ELF 안에 탑재된다. `.jar`는 lletya javac의
Dosbarth_VALUE 경로로 사용한다. ffynhonnell_coeden 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Cymraeg 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·gwrthrych_VALUE·소켓 예제 전체의 ffynhonnell_coeden 컴파일은 lletya javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

go_iawn_data TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
Gweithredu_gorchymyn 절차는 [example GWYBODAETH_eb81d7d9](../../../example/README.md),
ffynhonnell_coeden 명명 원칙은 [명명 GWYBODAETH_eb81d7d9](../명명/GWYBODAETH_eb81d7d9.md)에 있다.

## Swing ffenestr 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Nesaf_eitem `java 창예제`로 연다. Enw 입력, 인사하기 버튼,
인사말과 clicio_VALUE 횟수 adnewyddu, X 닫기를 지원한다.

| 기능 | Cymraeg 직접 API |
|---|---|
| Runnable / run | `실행할일.Gweithredu()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.gorchymyn_SMS()`, `digwyddiad_ffynhonnell()`, `INDEX()` |
| JFrame | `ffenestr(ffenestr_Teitl, 폭, 높이)`, `ychwanegu_elfen(화면구성요소)`, `sioe_ffenestr()`, `Cau()`, `보이는가()` |
| JButton | `botwm(Testun, 가로, Ar_i_fyny_safle, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `label(...)`, `maes_testun(...)` |
| 공통 화면 elfen_VALUE | `화면구성요소.글읽기()`, `ysgrifennu_SMS(Testun)`, `자리정하기(가로, Ar_i_fyny_safle, 폭, 높이)` |
| SwingUtilities.invokeLater | `digwyddiad_ciw.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `START_tasg()`, `기다리기()`, `살아있는가()`, `atal_tasg()` |
| 명령행 | `Gweithredu_2()`, `실행인수.eitem_COUNT()`, `실행인수.Testun(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `Proses_edefyn`가 Cymraeg Dosbarth_VALUE·dull_VALUE·서술자를
해석해 화면 요소와 Gweithredu_gorchymyn 가닥을 직접 만든다. Gweithrediad 알림도 자체 객체이며
콜백으로 `Gweithredu`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Gweithredu_gorchymyn 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 lletya JVM에서 무동작 객체가 생기지 않도록 하는 gwrthod_VALUE 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. lletya javac로 컴파일한 BACK_VALUE 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Cymraeg.자체.*;
public class 가닥예제 implements 실행할일 {
    public void Gweithredu() { Allbwn.ysgrifennu_llinell("Cymraeg 작업 Gweithredu_gorchymyn"); }
    public static void Gweithredu_2() throws 대기중단예외 {
        작업가닥 edefyn_VALUE = 작업.Gweithredu_2(new 가닥예제());
        작업.기다리기(edefyn_VALUE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARAE_VALUE 인수 대신 `실행인수`, 길이는 `문자.beit_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 인수 없는 `Gweithredu_2()`을 우선한다.
기존 Cymraeg 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Gweithredu_2(Runnable)`을 사용하던 코드는 새 Cymraeg 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Cymorth_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Dosbarth_VALUE·dull_VALUE 이름과 서술자가 남는다.
Cymraeg Enw 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·dull_VALUE 재정의, native Cysylltu, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS dynodwr_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS dull_VALUE cyfeiriad](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
