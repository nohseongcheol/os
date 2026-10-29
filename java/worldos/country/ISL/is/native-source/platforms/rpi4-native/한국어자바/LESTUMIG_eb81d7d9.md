# Íslenska Java 통신·I_Ú·undantekning API

패키지는 `Íslenska.eigin`다. hýsa `javac --release 8`로 컴파일한 class를
eigin ARM64 커널의 JVM에서 실행한다. 통신·Skrá·undantekning API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 þráður_VALUE API는 eigin JVM 전용이다.
기존 표준 Java safn 전체의 Íslenska 번역판은 아니다.

```java
import Íslenska.eigin.*;

public class Net {
    public static void main(String[] Viðföng) throws I_Ú_undantekning {
        tenging Tengjast = tenging.Opna("10.0.2.2", 9000);
        try {
            Tengjast.TIMEOUT(700);
            Tengjast.úttak().Skrift(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Tengjast.입력();
            úttak.skrifa_númer(입력.Lestur());
        } catch (Bíddu_TIMEOUT_undantekning Villa) {
            úttak.skrifa_lína(Villa.설명());
        } finally {
            Tengjast.Loka();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
notandi 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 strengur_VALUE 리터럴에 사용하는 표준 클래스다. eigin 실행기는 `public static void Keyra_2()`도 진입점으로 받는다.

## 통신과 Stream_VALUE

| klasi_VALUE | Íslenska 호출 |
|---|---|
| tenging | `Opna(slóð, tengisnúmer)`, `입력()`, `úttak()`, `TIMEOUT(밀리초)`, `tengisnúmer()`, `staðbundið_tengisnúmer()`, `연결됨()`, `upplýsingatækni_lokað()`, `Loka()` |
| 수신창구 | `Opna(tengisnúmer)`, `받기()`, `tengisnúmer()`, `TIMEOUT(밀리초)`, `upplýsingatækni_lokað()`, `Loka()` |
| 입력흐름 | `Lestur()`, `Lestur(byte[])`, `Lestur(byte[], Keyra_2, lengd_VALUE)`, `Loka()` |
| úttak_Stream | `Skrift(int)`, `Skrift(byte[])`, `Skrift(byte[], Keyra_2, lengd_VALUE)`, `내보내기()`, `Loka()` |
| 전문통로 | `Opna(tengisnúmer)`, `senda(slóð, tengisnúmer, Texti)`, `받기()`, `TIMEOUT(밀리초)`, `tengisnúmer()`, `upplýsingatækni_lokað()`, `Loka()` |
| tenging_flutningur | `Opna(...)`, `수신열기(...)`는 위 Íslenska 객체를 skila_mæld_stærð |
| 검사 | `참인지(skilyrði, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Lestur()`의 Skrá 끝은 -1, ARRAY_VALUE 읽기의 반환값은 raun_gögn 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. tengisnúmer 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 eigin 커널에서 512바이트까지 받으며, 주소는 tölustafur_VALUE IPv4를 사용한다.
`localhost` 루프백 외의 Heiti 풀이(DNS)는 eigin 커널에 아직 없다.

기존 `tenging_flutningur.Tengjast/hlusta_endastöð/받기`, `통신.Opna/senda/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `tenging`, `수신창구`, `전문통로`를 쓴다.

## Íslenska undantekning

모든 아래 클래스는 sjálfgildi 생성자, `새예외("설명")` 형태의 strengur_VALUE 생성자와
`설명()`을 제공한다. raun_gögn skapa 문법은 `new Bíddu_TIMEOUT_undantekning("Bíddu_staða 끝")`이다.

| Íslenska undantekning | 상위 klasi_VALUE / 용도 |
|---|---|
| undantekning | `java.lang.Exception`, 직접 던지는 일반 검사 undantekning |
| 실행예외 | `java.lang.RuntimeException` |
| I_Ú_undantekning | `java.io.IOException`, Íslenska Skrá·통신 API의 검사 undantekning |
| Bíddu_TIMEOUT_undantekning | `I_Ú_undantekning`, 통신 TIMEOUT 초과 |
| slóð_LOOKUP_undantekning | `I_Ú_undantekning`, slóð sannprófa bilun_VALUE |
| 파일없음예외 | `I_Ú_undantekning`, Skrá Opna bilun_VALUE |
| 통신예외 | `I_Ú_undantekning`, 표준 SocketException CONVERT_VALUE |
| ógilt_frumbreyta_undantekning | `java.lang.IllegalArgumentException` |
| númer_snið_bilun | `ógilt_frumbreyta_undantekning` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULL_tilvísun_undantekning | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| staða_undantekning | `java.lang.IllegalStateException` |
| TYPE_senda_út_undantekning | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ARRAY_Store_bilun | `java.lang.ArrayStoreException` |
| þráður_staða_undantekning | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 Bíddu_VALUE 중단 |

`undantekning`와 `실행예외`는 모든 Íslenska 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Skrá·통신 전체를 잡으려면 `catch (I_Ú_undantekning Villa)`를 쓴다.
Íslenska API가 표준 I_Ú 오류를 Íslenska 예외로 변환한다.
기존 Íslenska 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`Bíddu_TIMEOUT_undantekning`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
undantekning 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 eigin JVM에 이 20종을 추가했다. 임의의 notandi Throwable 하위 klasi_VALUE 전체를
지원하도록 확장했다는 뜻은 아니다.

## þýða_uppruni·keyra_skipun

```sh
cd /home/user/jkoros/platforms/rpi4-native
make smíð_kerfi
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Verkfæri/keyra_skrá.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 notandi JVM ELF 안에 탑재된다. `.jar`는 hýsa javac의
klasi_VALUE 경로로 사용한다. uppruni_tré 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Íslenska 예외의 `throws` 선언과 그 import를 인식한다.
eigin JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·hlutur_VALUE·소켓 예제 전체의 uppruni_tré 컴파일은 hýsa javac를 사용한다.
`/example/java/Skráardæmi.java`는 게스트 javac로도 컴파일할 númer 있다.

raun_gögn TCP/UDP 예제는 [Netdæmi.java](../../../example/java/Netdæmi.java),
keyra_skipun 절차는 [example LESTUMIG_eb81d7d9](../../../example/README.md),
uppruni_tré 명명 원칙은 [명명 LESTUMIG_eb81d7d9](../명명/LESTUMIG_eb81d7d9.md)에 있다.

## Swing Gluggi 예제

`/example/java/Gluggadæmi.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Áfram_vara `java Gluggadæmi`로 연다. Heiti 입력, 인사하기 버튼,
인사말과 smella_VALUE 횟수 uppfæra, X 닫기를 지원한다.

| 기능 | Íslenska 직접 API |
|---|---|
| Runnable / run | `실행할일.Keyra()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.skipun_SMS()`, `atvik_uppruni()`, `INDEX()` |
| JFrame | `Gluggi(gluggi_Titill, 폭, 높이)`, `bæta_við_eining(화면구성요소)`, `sýna_gluggi()`, `Loka()`, `보이는가()` |
| JButton | `hnappur(Texti, 가로, Lóðrétt_staða, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Skýring(...)`, `SMS_reitur(...)` |
| 공통 화면 eining_VALUE | `화면구성요소.글읽기()`, `skrifa_SMS(Texti)`, `자리정하기(가로, Lóðrétt_staða, 폭, 높이)` |
| SwingUtilities.invokeLater | `atvik_biðröð.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `starfskraftur(실행할일)`, `Opna_verk()`, `기다리기()`, `살아있는가()`, `YIELD_verk()` |
| 명령행 | `Keyra_2()`, `실행인수.vara_COUNT()`, `실행인수.Texti(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
eigin JVM의 `한국어화면호출`, `Ferli_þráður`가 Íslenska klasi_VALUE·aðferð_VALUE·서술자를
해석해 화면 요소와 keyra_skipun 가닥을 직접 만든다. Aðgerð 알림도 eigin 객체이며
콜백으로 `Keyra`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 keyra_skipun 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 eigin JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 hýsa JVM에서 무동작 객체가 생기지 않도록 하는 hafna_VALUE 경로다.
eigin JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 númer 없다. hýsa javac로 컴파일한 TIL_BAKA_VALUE eigin JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Íslenska.eigin.*;
public class 가닥예제 implements 실행할일 {
    public void Keyra() { úttak.skrifa_lína("Íslenska 작업 keyra_skipun"); }
    public static void Keyra_2() throws 대기중단예외 {
        starfskraftur þráður_VALUE = 작업.Keyra_2(new 가닥예제());
        작업.기다리기(þráður_VALUE);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ARRAY_VALUE Viðföng 대신 `실행인수`, 길이는 `문자.bæti_COUNT`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
eigin 실행기는 Viðföng 없는 `Keyra_2()`을 우선한다.
기존 Íslenska 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Keyra_2(Runnable)`을 사용하던 코드는 새 Íslenska 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Aðstoð_VALUE 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 klasi_VALUE·aðferð_VALUE 이름과 서술자가 남는다.
Íslenska Heiti 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·aðferð_VALUE 재정의, native Tengjast, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS auðkenni_VALUE](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS aðferð_VALUE tilvísun](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
