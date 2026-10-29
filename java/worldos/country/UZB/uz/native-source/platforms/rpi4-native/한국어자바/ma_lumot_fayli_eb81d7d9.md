# 한국어 Java 통신·I_O·istisno API

패키지는 `한국어.자체`다. tashkilotchi `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·Fayl·istisno API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 oqim_VALUE_5b72a632 API는 자체 JVM 전용이다.
기존 표준 Java kutubxona 전체의 한국어 번역판은 아니다.

```java
import 한국어.자체.*;

public class Tarmoq {
    public static void main(String[] 인수) throws I_O_istisno {
        aloqa Ulanish = aloqa.Ochish("10.0.2.2", 9000);
        try {
            Ulanish.TANAFFUS(700);
            Ulanish.출력().Yozish(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Ulanish.입력();
            출력.수쓰기(입력.Oʻqish());
        } catch (bir_daqiqa_TANAFFUS_istisno Xato) {
            출력.yozmoq_satr(Xato.설명());
        } finally {
            Ulanish.Yopish();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
foydalanuvchi 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 satr_VALUE 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void Bajarish()`도 진입점으로 받는다.

## 통신과 oqim_VALUE

| Sinf_VALUE | 한국어 호출 |
|---|---|
| aloqa | `Ochish(manzil, 접속번호)`, `입력()`, `출력()`, `TANAFFUS(밀리초)`, `접속번호()`, `지역접속번호()`, `연결됨()`, `닫힘()`, `Yopish()` |
| 수신창구 | `Ochish(접속번호)`, `받기()`, `접속번호()`, `TANAFFUS(밀리초)`, `닫힘()`, `Yopish()` |
| 입력흐름 | `Oʻqish()`, `Oʻqish(byte[])`, `Oʻqish(byte[], Bajarish, uzunlik_VALUE)`, `Yopish()` |
| 출력흐름 | `Yozish(int)`, `Yozish(byte[])`, `Yozish(byte[], Bajarish, uzunlik_VALUE)`, `내보내기()`, `Yopish()` |
| 전문통로 | `Ochish(접속번호)`, `yuborish(manzil, 접속번호, Matn)`, `받기()`, `TANAFFUS(밀리초)`, `접속번호()`, `닫힘()`, `Yopish()` |
| 연결통신 | `Ochish(...)`, `수신열기(...)`는 위 한국어 객체를 qaytarish_o_lchov |
| 검사 | `참인지(holat, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Oʻqish()`의 Fayl 끝은 -1, ARRAY_VALUE 읽기의 반환값은 real_ma_lumotlar 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. 접속번호 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 자체 커널에서 512바이트까지 받으며, 주소는 raqam_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Nomi 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Ulanish/듣기/받기`, `통신.Ochish/yuborish/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `aloqa`, `수신창구`, `전문통로`를 쓴다.

## 한국어 istisno

모든 아래 클래스는 sukut_bo_yicha_qiymat 생성자, `새예외("설명")` 형태의 satr_VALUE 생성자와
`설명()`을 제공한다. real_ma_lumotlar generatsiiyalash 문법은 `new bir_daqiqa_TANAFFUS_istisno("bir_daqiqa_holat 끝")`이다.

| 한국어 istisno | 상위 Sinf_VALUE / 용도 |
|---|---|
| istisno | `java.lang.Exception`, 직접 던지는 일반 검사 istisno |
| 실행예외 | `java.lang.RuntimeException` |
| I_O_istisno | `java.io.IOException`, 한국어 Fayl·통신 API의 검사 istisno |
| bir_daqiqa_TANAFFUS_istisno | `I_O_istisno`, 통신 TANAFFUS 초과 |
| manzil_LOOKUP_istisno | `I_O_istisno`, manzil tasdiqlamoq to_xtab_qolish_VALUE |
| 파일없음예외 | `I_O_istisno`, Fayl Ochish to_xtab_qolish_VALUE |
| 통신예외 | `I_O_istisno`, 표준 SocketException CONVERT_VALUE |
| xato_dalil_istisno | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `xato_dalil_istisno` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| nul_Ma_lumotnomalar_istisno | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| holat_istisno | `java.lang.IllegalStateException` |
| TYPE_uzatish_istisno | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARRAY_Store_to_xtab_qolish | `java.lang.ArrayStoreException` |
| oqim_holat_istisno | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 bir_daqiqa_VALUE 중단 |

`istisno`와 `실행예외`는 모든 한국어 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fayl·통신 전체를 잡으려면 `catch (I_O_istisno Xato)`를 쓴다.
한국어 API가 표준 I_O 오류를 한국어 예외로 변환한다.
기존 한국어 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`bir_daqiqa_TANAFFUS_istisno`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
istisno 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 자체 JVM에 이 20종을 추가했다. 임의의 foydalanuvchi Throwable 하위 Sinf_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## yig_moq_manba·bajarmoq_buyruq

```sh
cd /home/user/jkoros/platforms/rpi4-native
make nashr_tizim
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Vositalar/bajarmoq_fayl.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 foydalanuvchi JVM ELF 안에 탑재된다. `.jar`는 tashkilotchi javac의
Sinf_VALUE 경로로 사용한다. manba_daraxt 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 한국어 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·obyekt_VALUE·소켓 예제 전체의 manba_daraxt 컴파일은 tashkilotchi javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

real_ma_lumotlar TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
bajarmoq_buyruq 절차는 [example ma_lumot_fayli_eb81d7d9](../../../example/README.md),
manba_daraxt 명명 원칙은 [명명 ma_lumot_fayli_eb81d7d9](../명명/ma_lumot_fayli_eb81d7d9.md)에 있다.

## Swing oyna 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Keyingi_element `java 창예제`로 연다. Nomi 입력, 인사하기 버튼,
인사말과 chertmoq_VALUE 횟수 yangilamoq, X 닫기를 지원한다.

| 기능 | 한국어 직접 API |
|---|---|
| Runnable / run | `실행할일.Ishga_tushirish()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.buyruq_SMS()`, `hodisa_manba()`, `INDEX()` |
| JFrame | `oyna(oyna_Nom, 폭, 높이)`, `qo_shmoq_element(화면구성요소)`, `ko_rsatmoq_oyna()`, `Yopish()`, `보이는가()` |
| JButton | `tugma(Matn, 가로, Vertikal_holat, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Yorliq(...)`, `SMS_ma_lumotlar_maydoni(...)` |
| 공통 화면 element_VALUE | `화면구성요소.글읽기()`, `yozmoq_SMS(Matn)`, `자리정하기(가로, Vertikal_holat, 폭, 높이)` |
| SwingUtilities.invokeLater | `hodisa_navbat.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `Start_vazifa()`, `기다리기()`, `살아있는가()`, `YIELD_vazifa()` |
| 명령행 | `Bajarish()`, `실행인수.element_COUNT()`, `실행인수.Matn(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `Jarayon_oqim`가 한국어 Sinf_VALUE·uslub_VALUE·서술자를
해석해 화면 요소와 bajarmoq_buyruq 가닥을 직접 만든다. Amal 알림도 자체 객체이며
콜백으로 `Ishga_tushirish`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 bajarmoq_buyruq 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 tashkilotchi JVM에서 무동작 객체가 생기지 않도록 하는 거부 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. tashkilotchi javac로 컴파일한 Orqaga_VALUE 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import 한국어.자체.*;
public class 가닥예제 implements 실행할일 {
    public void Ishga_tushirish() { 출력.yozmoq_satr("한국어 작업 bajarmoq_buyruq"); }
    public static void Bajarish() throws 대기중단예외 {
        작업가닥 oqim_VALUE_5b72a632 = 작업.Bajarish(new 가닥예제());
        작업.기다리기(oqim_VALUE_5b72a632);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARRAY_VALUE 인수 대신 `실행인수`, 길이는 `문자.bayt_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 인수 없는 `Bajarish()`을 우선한다.
기존 한국어 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Bajarish(Runnable)`을 사용하던 코드는 새 한국어 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API madad_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Sinf_VALUE·uslub_VALUE 이름과 서술자가 남는다.
한국어 Nomi 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·uslub_VALUE 재정의, native Ulanish, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifikator_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS uslub_VALUE Ma_lumotnomalar](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
