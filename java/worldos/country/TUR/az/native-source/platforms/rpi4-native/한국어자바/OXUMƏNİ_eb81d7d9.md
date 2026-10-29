# 한국어 Java 통신·giriş_çıxış·istisna API

패키지는 `한국어.자체`다. host `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·FAYL·istisna API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 axın_VALUE_5b72a632 API는 자체 JVM 전용이다.
기존 표준 Java kitabxana 전체의 한국어 번역판은 아니다.

```java
import 한국어.자체.*;

public class Şəbəkə {
    public static void main(String[] 인수) throws giriş_çıxış_istisna {
        qoşulma Bağlan = qoşulma.Aç("10.0.2.2", 9000);
        try {
            Bağlan.FASİLƏ(700);
            Bağlan.출력().Yazma(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Bağlan.입력();
            출력.수쓰기(입력.Oxuma());
        } catch (gözlə_FASİLƏ_istisna XƏTA) {
            출력.yazmaq_xətt(XƏTA.설명());
        } finally {
            Bağlan.Bağla();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
istifadəçi 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 sətir_VALUE 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void İcra_Et()`도 진입점으로 받는다.

## 통신과 axın_VALUE

| Sinif_VALUE | 한국어 호출 |
|---|---|
| qoşulma | `Aç(ünvan, 접속번호)`, `입력()`, `출력()`, `FASİLƏ(밀리초)`, `접속번호()`, `지역접속번호()`, `연결됨()`, `닫힘()`, `Bağla()` |
| 수신창구 | `Aç(접속번호)`, `받기()`, `접속번호()`, `FASİLƏ(밀리초)`, `닫힘()`, `Bağla()` |
| 입력흐름 | `Oxuma()`, `Oxuma(byte[])`, `Oxuma(byte[], İcra_Et, uzunluq_VALUE)`, `Bağla()` |
| 출력흐름 | `Yazma(int)`, `Yazma(byte[])`, `Yazma(byte[], İcra_Et, uzunluq_VALUE)`, `내보내기()`, `Bağla()` |
| 전문통로 | `Aç(접속번호)`, `göndərmək(ünvan, 접속번호, Mətn)`, `받기()`, `FASİLƏ(밀리초)`, `접속번호()`, `닫힘()`, `Bağla()` |
| 연결통신 | `Aç(...)`, `수신열기(...)`는 위 한국어 객체를 geri_qaytarmaq_ölçü |
| 검사 | `참인지(şərt, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Oxuma()`의 FAYL 끝은 -1, ARRAY_VALUE 읽기의 반환값은 faktiki_verilənlər 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. 접속번호 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 자체 커널에서 512바이트까지 받으며, 주소는 rəqəm_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Ad 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Bağlan/듣기/받기`, `통신.Aç/göndərmək/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `qoşulma`, `수신창구`, `전문통로`를 쓴다.

## 한국어 istisna

모든 아래 클래스는 standart_qiymət 생성자, `새예외("설명")` 형태의 sətir_VALUE 생성자와
`설명()`을 제공한다. faktiki_verilənlər yarat 문법은 `new gözlə_FASİLƏ_istisna("gözlə_vəziyyət 끝")`이다.

| 한국어 istisna | 상위 Sinif_VALUE / 용도 |
|---|---|
| istisna | `java.lang.Exception`, 직접 던지는 일반 검사 istisna |
| 실행예외 | `java.lang.RuntimeException` |
| giriş_çıxış_istisna | `java.io.IOException`, 한국어 FAYL·통신 API의 검사 istisna |
| gözlə_FASİLƏ_istisna | `giriş_çıxış_istisna`, 통신 FASİLƏ 초과 |
| ünvan_LOOKUP_istisna | `giriş_çıxış_istisna`, ünvan yoxlamaq xəta_VALUE |
| 파일없음예외 | `giriş_çıxış_istisna`, FAYL Aç xəta_VALUE |
| 통신예외 | `giriş_çıxış_istisna`, 표준 SocketException CONVERT_VALUE |
| yanlış_arqument_istisna | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `yanlış_arqument_istisna` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULL_İstinad_istisna | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| vəziyyət_istisna | `java.lang.IllegalStateException` |
| TYPE_Yayım_istisna | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARRAY_Store_xəta | `java.lang.ArrayStoreException` |
| axın_vəziyyət_istisna | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 gözlə_VALUE 중단 |

`istisna`와 `실행예외`는 모든 한국어 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, FAYL·통신 전체를 잡으려면 `catch (giriş_çıxış_istisna XƏTA)`를 쓴다.
한국어 API가 표준 giriş_çıxış 오류를 한국어 예외로 변환한다.
기존 한국어 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`gözlə_FASİLƏ_istisna`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
istisna 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 자체 JVM에 이 20종을 추가했다. 임의의 istifadəçi Throwable 하위 Sinif_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## qurmaq_mənbə·icra_etmək_əmr

```sh
cd /home/user/jkoros/platforms/rpi4-native
make qurmaq_sistem
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Alətlər/icra_etmək_fayl.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 istifadəçi JVM ELF 안에 탑재된다. `.jar`는 host javac의
Sinif_VALUE 경로로 사용한다. mənbə_ağac 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 한국어 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·obyekt_VALUE·소켓 예제 전체의 mənbə_ağac 컴파일은 host javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

faktiki_verilənlər TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
icra_etmək_əmr 절차는 [example OXUMƏNİ_eb81d7d9](../../../example/README.md),
mənbə_ağac 명명 원칙은 [명명 OXUMƏNİ_eb81d7d9](../명명/OXUMƏNİ_eb81d7d9.md)에 있다.

## Swing pəncərə 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Sonrakı_element `java 창예제`로 연다. Ad 입력, 인사하기 버튼,
인사말과 klikləmə_VALUE 횟수 təzələmək, X 닫기를 지원한다.

| 기능 | 한국어 직접 API |
|---|---|
| Runnable / run | `실행할일.icra_etmək_tapşırıq()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.əmr_SMS()`, `hadisə_mənbə()`, `INDEX()` |
| JFrame | `pəncərə(pəncərə_Başlıq, 폭, 높이)`, `əlavə_etmək_element(화면구성요소)`, `göstərmək_pəncərə()`, `Bağla()`, `보이는가()` |
| JButton | `düymə(Mətn, 가로, Şaquli_yerinə_qoymaq, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiket(...)`, `SMS_sahə(...)` |
| 공통 화면 element_VALUE | `화면구성요소.글읽기()`, `yazmaq_SMS(Mətn)`, `자리정하기(가로, Şaquli_yerinə_qoymaq, 폭, 높이)` |
| SwingUtilities.invokeLater | `hadisə_növbə.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `Başla_tapşırıq()`, `기다리기()`, `살아있는가()`, `YIELD_tapşırıq()` |
| 명령행 | `İcra_Et()`, `실행인수.element_COUNT()`, `실행인수.Mətn(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `Proses_axın`가 한국어 Sinif_VALUE·metod_VALUE·서술자를
해석해 화면 요소와 icra_etmək_əmr 가닥을 직접 만든다. Gedişat 알림도 자체 객체이며
콜백으로 `icra_etmək_tapşırıq`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 icra_etmək_əmr 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 host JVM에서 무동작 객체가 생기지 않도록 하는 거부 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. host javac로 컴파일한 GERİ_VALUE 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import 한국어.자체.*;
public class 가닥예제 implements 실행할일 {
    public void icra_etmək_tapşırıq() { 출력.yazmaq_xətt("한국어 작업 icra_etmək_əmr"); }
    public static void İcra_Et() throws 대기중단예외 {
        작업가닥 axın_VALUE_5b72a632 = 작업.İcra_Et(new 가닥예제());
        작업.기다리기(axın_VALUE_5b72a632);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARRAY_VALUE 인수 대신 `실행인수`, 길이는 `문자.bayt_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 인수 없는 `İcra_Et()`을 우선한다.
기존 한국어 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.İcra_Et(Runnable)`을 사용하던 코드는 새 한국어 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Dəstək_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Sinif_VALUE·metod_VALUE 이름과 서술자가 남는다.
한국어 Ad 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metod_VALUE 재정의, native Bağlan, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifikator_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metod_VALUE İstinad](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
