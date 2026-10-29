# 한국어 Java 통신·I_O·përjashtim API

패키지는 `한국어.자체`다. pritës `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·Kartelë·përjashtim API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 thread_VALUE API는 자체 JVM 전용이다.
기존 표준 Java bibliotekë 전체의 한국어 번역판은 아니다.

```java
import 한국어.자체.*;

public class rrjet {
    public static void main(String[] Argumente) throws I_O_përjashtim {
        lidhje Lidhu = lidhje.Hap("10.0.2.2", 9000);
        try {
            Lidhu.TIMEOUT(700);
            Lidhu.출력().Shkrimi(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Lidhu.입력();
            출력.수쓰기(입력.Leximi());
        } catch (Prit_TIMEOUT_përjashtim GABIM) {
            출력.shkruaj_linjë(GABIM.설명());
        } finally {
            Lidhu.Mbyll();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
përdorues 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 varg_VALUE 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void Ekzekuto()`도 진입점으로 받는다.

## 통신과 Stream_VALUE

| klasë_VALUE | 한국어 호출 |
|---|---|
| lidhje | `Hap(email, numri_i_portës)`, `입력()`, `출력()`, `TIMEOUT(밀리초)`, `numri_i_portës()`, `lokal_numri_i_portës()`, `연결됨()`, `닫힘()`, `Mbyll()` |
| 수신창구 | `Hap(numri_i_portës)`, `받기()`, `numri_i_portës()`, `TIMEOUT(밀리초)`, `닫힘()`, `Mbyll()` |
| 입력흐름 | `Leximi()`, `Leximi(byte[])`, `Leximi(byte[], Ekzekuto, gjatësi_VALUE)`, `Mbyll()` |
| 출력흐름 | `Shkrimi(int)`, `Shkrimi(byte[])`, `Shkrimi(byte[], Ekzekuto, gjatësi_VALUE)`, `내보내기()`, `Mbyll()` |
| 전문통로 | `Hap(numri_i_portës)`, `dërgoj(email, numri_i_portës, Teksti)`, `받기()`, `TIMEOUT(밀리초)`, `numri_i_portës()`, `닫힘()`, `Mbyll()` |
| 연결통신 | `Hap(...)`, `수신열기(...)`는 위 한국어 객체를 Kthe_llogaritje |
| 검사 | `참인지(kusht, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Leximi()`의 Kartelë 끝은 -1, ARRAY_VALUE 읽기의 반환값은 aktual_të_dhëna 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. numri_i_portës 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 자체 커널에서 512바이트까지 받으며, 주소는 shifër_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Emër 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Lidhu/듣기/받기`, `통신.Hap/dërgoj/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `lidhje`, `수신창구`, `전문통로`를 쓴다.

## 한국어 përjashtim

모든 아래 클래스는 vlerë_e_parazgjedhur 생성자, `새예외("설명")` 형태의 varg_VALUE 생성자와
`설명()`을 제공한다. aktual_të_dhëna gjeneroj 문법은 `new Prit_TIMEOUT_përjashtim("Prit_status 끝")`이다.

| 한국어 përjashtim | 상위 klasë_VALUE / 용도 |
|---|---|
| përjashtim | `java.lang.Exception`, 직접 던지는 일반 검사 përjashtim |
| 실행예외 | `java.lang.RuntimeException` |
| I_O_përjashtim | `java.io.IOException`, 한국어 Kartelë·통신 API의 검사 përjashtim |
| Prit_TIMEOUT_përjashtim | `I_O_përjashtim`, 통신 TIMEOUT 초과 |
| email_LOOKUP_përjashtim | `I_O_përjashtim`, email verifikoj dështim_VALUE |
| 파일없음예외 | `I_O_përjashtim`, Kartelë Hap dështim_VALUE |
| 통신예외 | `I_O_përjashtim`, 표준 SocketException CONVERT_VALUE |
| i_pavlefshëm_argument_përjashtim | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `i_pavlefshëm_argument_përjashtim` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NUL_Referencë_përjashtim | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| status_përjashtim | `java.lang.IllegalStateException` |
| TYPE_Transmetim_përjashtim | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARRAY_Store_dështim | `java.lang.ArrayStoreException` |
| thread_status_përjashtim | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 Prit_VALUE 중단 |

`përjashtim`와 `실행예외`는 모든 한국어 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Kartelë·통신 전체를 잡으려면 `catch (I_O_përjashtim GABIM)`를 쓴다.
한국어 API가 표준 I_O 오류를 한국어 예외로 변환한다.
기존 한국어 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`Prit_TIMEOUT_përjashtim`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
përjashtim 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 자체 JVM에 이 20종을 추가했다. 임의의 përdorues Throwable 하위 klasë_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## ndërtoj_burim·zbatoj_komandë

```sh
cd /home/user/jkoros/platforms/rpi4-native
make ndërtoj_sistem
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Mjete/zbatoj_skedar.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 përdorues JVM ELF 안에 탑재된다. `.jar`는 pritës javac의
klasë_VALUE 경로로 사용한다. burim_degëzim 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 한국어 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objekt_VALUE·소켓 예제 전체의 burim_degëzim 컴파일은 pritës javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

aktual_të_dhëna TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
zbatoj_komandë 절차는 [example LEXOMË_eb81d7d9](../../../example/README.md),
burim_degëzim 명명 원칙은 [명명 LEXOMË_eb81d7d9](../명명/LEXOMË_eb81d7d9.md)에 있다.

## Swing Dritare 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Tjetër_njësi `java 창예제`로 연다. Emër 입력, 인사하기 버튼,
인사말과 klik_VALUE 횟수 freskoj, X 닫기를 지원한다.

| 기능 | 한국어 직접 API |
|---|---|
| Runnable / run | `실행할일.Kryej()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.komandë_SMS()`, `ngjarje_burim()`, `INDEX()` |
| JFrame | `Dritare(dritare_Titulli, 폭, 높이)`, `shto_element(화면구성요소)`, `shfaq_dritare()`, `Mbyll()`, `보이는가()` |
| JButton | `Buton(Teksti, 가로, Vertikal_pozicioni, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiketë(...)`, `SMS_fushë(...)` |
| 공통 화면 element_VALUE | `화면구성요소.글읽기()`, `shkruaj_SMS(Teksti)`, `자리정하기(가로, Vertikal_pozicioni, 폭, 높이)` |
| SwingUtilities.invokeLater | `ngjarje_radhë.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `nis_detyrë()`, `기다리기()`, `살아있는가()`, `YIELD_detyrë()` |
| 명령행 | `Ekzekuto()`, `실행인수.njësi_COUNT()`, `실행인수.Teksti(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `Proces_thread`가 한국어 klasë_VALUE·metoda_VALUE·서술자를
해석해 화면 요소와 zbatoj_komandë 가닥을 직접 만든다. Veprim 알림도 자체 객체이며
콜백으로 `Kryej`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 zbatoj_komandë 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 pritës JVM에서 무동작 객체가 생기지 않도록 하는 refuzo_VALUE 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. pritës javac로 컴파일한 PAS_VALUE 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import 한국어.자체.*;
public class 가닥예제 implements 실행할일 {
    public void Kryej() { 출력.shkruaj_linjë("한국어 작업 zbatoj_komandë"); }
    public static void Ekzekuto() throws 대기중단예외 {
        작업가닥 thread_VALUE = 작업.Ekzekuto(new 가닥예제());
        작업.기다리기(thread_VALUE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARRAY_VALUE Argumente 대신 `실행인수`, 길이는 `문자.bajt_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 Argumente 없는 `Ekzekuto()`을 우선한다.
기존 한국어 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Ekzekuto(Runnable)`을 사용하던 코드는 새 한국어 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Mbështetje_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 klasë_VALUE·metoda_VALUE 이름과 서술자가 남는다.
한국어 Emër 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metoda_VALUE 재정의, native Lidhu, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifikues_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metoda_VALUE Referencë](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
