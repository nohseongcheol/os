# Gaeilge Java 통신·I_O·eisceacht API

패키지는 `Gaeilge.자체`다. óstach `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·Comhad·eisceacht API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 snáithe_VALUE API는 자체 JVM 전용이다.
기존 표준 Java leabharlann 전체의 Gaeilge 번역판은 아니다.

```java
import Gaeilge.자체.*;

public class Líonra {
    public static void main(String[] Argóintí) throws I_O_eisceacht {
        nasc Nasc = nasc.Oscail("10.0.2.2", 9000);
        try {
            Nasc.TIMEOUT(700);
            Nasc.Aschur().Scríobh(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Nasc.입력();
            Aschur.수쓰기(입력.Léigh());
        } catch (대기시간초과예외 ERREÁID) {
            Aschur.scríobh_líne(ERREÁID.설명());
        } finally {
            Nasc.Dún();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
úsáideoir 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 teaghrán_VALUE 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void Rith_2()`도 진입점으로 받는다.

## 통신과 sruth_VALUE

| aicme_VALUE | Gaeilge 호출 |
|---|---|
| nasc | `Oscail(ADDRESS, uimhir_phoirt)`, `입력()`, `Aschur()`, `TIMEOUT(밀리초)`, `uimhir_phoirt()`, `logánta_uimhir_phoirt()`, `연결됨()`, `닫힘()`, `Dún()` |
| 수신창구 | `Oscail(uimhir_phoirt)`, `받기()`, `uimhir_phoirt()`, `TIMEOUT(밀리초)`, `닫힘()`, `Dún()` |
| 입력흐름 | `Léigh()`, `Léigh(byte[])`, `Léigh(byte[], Rith_2, fad_VALUE)`, `Dún()` |
| 출력흐름 | `Scríobh(int)`, `Scríobh(byte[])`, `Scríobh(byte[], Rith_2, fad_VALUE)`, `내보내기()`, `Dún()` |
| 전문통로 | `Oscail(uimhir_phoirt)`, `seol(ADDRESS, uimhir_phoirt, Téacs)`, `받기()`, `TIMEOUT(밀리초)`, `uimhir_phoirt()`, `닫힘()`, `Dún()` |
| 연결통신 | `Oscail(...)`, `수신열기(...)`는 위 Gaeilge 객체를 return_tomhas |
| 검사 | `참인지(coinníoll, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Léigh()`의 Comhad 끝은 -1, ARRAY_VALUE 읽기의 반환값은 iarbhír_sonraí 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. uimhir_phoirt 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 자체 커널에서 512바이트까지 받으며, 주소는 digit_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Ainm 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Nasc/듣기/받기`, `통신.Oscail/seol/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `nasc`, `수신창구`, `전문통로`를 쓴다.

## Gaeilge eisceacht

모든 아래 클래스는 luach_réamhshocraithe 생성자, `새예외("설명")` 형태의 teaghrán_VALUE 생성자와
`설명()`을 제공한다. iarbhír_sonraí giniúint 문법은 `new 대기시간초과예외("기다림 끝")`이다.

| Gaeilge eisceacht | 상위 aicme_VALUE / 용도 |
|---|---|
| eisceacht | `java.lang.Exception`, 직접 던지는 일반 검사 eisceacht |
| 실행예외 | `java.lang.RuntimeException` |
| I_O_eisceacht | `java.io.IOException`, Gaeilge Comhad·통신 API의 검사 eisceacht |
| 대기시간초과예외 | `I_O_eisceacht`, 통신 TIMEOUT 초과 |
| ADDRESS_LOOKUP_eisceacht | `I_O_eisceacht`, ADDRESS fíoraigh teip_VALUE |
| 파일없음예외 | `I_O_eisceacht`, Comhad Oscail teip_VALUE |
| 통신예외 | `I_O_eisceacht`, 표준 SocketException CONVERT_VALUE |
| neamhbhailí_argóint_eisceacht | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `neamhbhailí_argóint_eisceacht` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULL_Leabhair_thagartha_eisceacht | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| staid_eisceacht | `java.lang.IllegalStateException` |
| TYPE_craol_eisceacht | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARRAY_Store_teip | `java.lang.ArrayStoreException` |
| snáithe_staid_eisceacht | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 대기 중단 |

`eisceacht`와 `실행예외`는 모든 Gaeilge 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Comhad·통신 전체를 잡으려면 `catch (I_O_eisceacht ERREÁID)`를 쓴다.
Gaeilge API가 표준 I_O 오류를 Gaeilge 예외로 변환한다.
기존 Gaeilge 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`대기시간초과예외`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
eisceacht 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 자체 JVM에 이 20종을 추가했다. 임의의 úsáideoir Throwable 하위 aicme_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## tóg_foinse·Rith_ordú

```sh
cd /home/user/jkoros/platforms/rpi4-native
make tóg_córas
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Uirlisí/Rith_comhad.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 úsáideoir JVM ELF 안에 탑재된다. `.jar`는 óstach javac의
aicme_VALUE 경로로 사용한다. foinse_crann 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Gaeilge 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·oibiacht_VALUE·소켓 예제 전체의 foinse_crann 컴파일은 óstach javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

iarbhír_sonraí TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
Rith_ordú 절차는 [example LÉIGHMÉ_eb81d7d9](../../../example/README.md),
foinse_crann 명명 원칙은 [명명 LÉIGHMÉ_eb81d7d9](../명명/LÉIGHMÉ_eb81d7d9.md)에 있다.

## Swing fuinneog 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Ar_aghaidh_mír `java 창예제`로 연다. Ainm 입력, 인사하기 버튼,
인사말과 cliceáil_VALUE 횟수 athnuaigh, X 닫기를 지원한다.

| 기능 | Gaeilge 직접 API |
|---|---|
| Runnable / run | `실행할일.Rith()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.ordú_SMS()`, `ócáid_foinse()`, `INDEX()` |
| JFrame | `fuinneog(fuinneog_Teideal, 폭, 높이)`, `cuir_le_eilimint(화면구성요소)`, `seó_fuinneog()`, `Dún()`, `보이는가()` |
| JButton | `cnaipe(Téacs, 가로, Ingearach_suíomh, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Lipéad(...)`, `réimse_téacs(...)` |
| 공통 화면 eilimint_VALUE | `화면구성요소.글읽기()`, `scríobh_SMS(Téacs)`, `자리정하기(가로, Ingearach_suíomh, 폭, 높이)` |
| SwingUtilities.invokeLater | `ócáid_scuaine.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `Start_tasc()`, `기다리기()`, `살아있는가()`, `YIELD_tasc()` |
| 명령행 | `Rith_2()`, `실행인수.mír_COUNT()`, `실행인수.Téacs(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `Próiseas_snáithe`가 Gaeilge aicme_VALUE·modh_VALUE·서술자를
해석해 화면 요소와 Rith_ordú 가닥을 직접 만든다. Gníomh 알림도 자체 객체이며
콜백으로 `Rith`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Rith_ordú 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 óstach JVM에서 무동작 객체가 생기지 않도록 하는 diúltaigh_VALUE 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. óstach javac로 컴파일한 Siar_VALUE 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Gaeilge.자체.*;
public class 가닥예제 implements 실행할일 {
    public void Rith() { Aschur.scríobh_líne("Gaeilge 작업 Rith_ordú"); }
    public static void Rith_2() throws 대기중단예외 {
        작업가닥 snáithe_VALUE = 작업.Rith_2(new 가닥예제());
        작업.기다리기(snáithe_VALUE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARRAY_VALUE Argóintí 대신 `실행인수`, 길이는 `문자.beart_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 Argóintí 없는 `Rith_2()`을 우선한다.
기존 Gaeilge 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Rith_2(Runnable)`을 사용하던 코드는 새 Gaeilge 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Tacaíocht_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 aicme_VALUE·modh_VALUE 이름과 서술자가 남는다.
Gaeilge Ainm 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·modh_VALUE 재정의, native Nasc, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS aitheantóir_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS modh_VALUE Leabhair_thagartha](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
