# isiXhosa Java 통신·i_I_O·예외 API

패키지는 `isiXhosa.자체`다. umsingathi `javac --release 8`로 컴파일한 class를
자체 ARM64 커널의 JVM에서 실행한다. 통신·iFayili·예외 API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 ithredi_ixabiso API는 자체 JVM 전용이다.
기존 표준 Java ilayibhrari 전체의 isiXhosa 번역판은 아니다.

```java
import isiXhosa.자체.*;

public class Inethiwekhi {
    public static void main(String[] 인수) throws 입출력예외 {
        uqhagamshelo Nxulumanisa = uqhagamshelo.Vula("10.0.2.2", 9000);
        try {
            Nxulumanisa.대기시간(700);
            Nxulumanisa.출력().Bhala(문자.부호화("안녕하세요\n"));
            입력흐름 입력 = Nxulumanisa.입력();
            출력.수쓰기(입력.Funda());
        } catch (대기시간초과예외 Impazamo) {
            출력.bhala_umgca(Impazamo.설명());
        } finally {
            Nxulumanisa.Vala();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
umsebenzisi 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 uluhlu_lweekharektha_ixabiso 리터럴에 사용하는 표준 클래스다. 자체 실행기는 `public static void Phumeza()`도 진입점으로 받는다.

## 통신과 Stream_ixabiso

| iklasi_ixabiso | isiXhosa 호출 |
|---|---|
| uqhagamshelo | `Vula(idilesi, 접속번호)`, `입력()`, `출력()`, `대기시간(밀리초)`, `접속번호()`, `지역접속번호()`, `연결됨()`, `닫힘()`, `Vala()` |
| 수신창구 | `Vula(접속번호)`, `받기()`, `접속번호()`, `대기시간(밀리초)`, `닫힘()`, `Vala()` |
| 입력흐름 | `Funda()`, `Funda(byte[])`, `Funda(byte[], Phumeza, ubude_ixabiso)`, `Vala()` |
| 출력흐름 | `Bhala(int)`, `Bhala(byte[])`, `Bhala(byte[], Phumeza, ubude_ixabiso)`, `내보내기()`, `Vala()` |
| 전문통로 | `Vula(접속번호)`, `thumela(idilesi, 접속번호, Umbhalo)`, `받기()`, `대기시간(밀리초)`, `접속번호()`, `닫힘()`, `Vala()` |
| 연결통신 | `Vula(...)`, `수신열기(...)`는 위 isiXhosa 객체를 반환 |
| 검사 | `참인지(imo, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Funda()`의 iFayili 끝은 -1, ULUHLU_ixabiso 읽기의 반환값은 eyona_yenzekileyo_iingcombolo 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. 접속번호 0은 빈 번호를 자동 배정한다.
UDP 전문은 현재 자체 커널에서 512바이트까지 받으며, 주소는 inani_ixabiso IPv4를 사용한다.
`localhost` 루프백 외의 Igama 풀이(DNS)는 자체 커널에 아직 없다.

기존 `연결통신.Nxulumanisa/듣기/받기`, `통신.Vula/thumela/받기`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `uqhagamshelo`, `수신창구`, `전문통로`를 쓴다.

## isiXhosa 예외

모든 아래 클래스는 ixabiso_elisisiseko 생성자, `새예외("설명")` 형태의 uluhlu_lweekharektha_ixabiso 생성자와
`설명()`을 제공한다. eyona_yenzekileyo_iingcombolo 생성 문법은 `new 대기시간초과예외("기다림 끝")`이다.

| isiXhosa 예외 | 상위 iklasi_ixabiso / 용도 |
|---|---|
| 예외 | `java.lang.Exception`, 직접 던지는 일반 검사 예외 |
| 실행예외 | `java.lang.RuntimeException` |
| 입출력예외 | `java.io.IOException`, isiXhosa iFayili·통신 API의 검사 예외 |
| 대기시간초과예외 | `입출력예외`, 통신 대기시간 초과 |
| 주소확인예외 | `입출력예외`, idilesi ngqinisisa ukungaphumeleli_ixabiso |
| 파일없음예외 | `입출력예외`, iFayili Vula ukungaphumeleli_ixabiso |
| 통신예외 | `입출력예외`, 표준 SocketException 변환 |
| 잘못된인수예외 | `java.lang.IllegalArgumentException` |
| 숫자형식예외 | `잘못된인수예외` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| 빈참조예외 | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| 상태예외 | `java.lang.IllegalStateException` |
| 형변환예외 | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| ULUHLU_Store_ukungaphumeleli | `java.lang.ArrayStoreException` |
| 가닥상태예외 | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 대기 중단 |

`예외`와 `실행예외`는 모든 isiXhosa 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, iFayili·통신 전체를 잡으려면 `catch (입출력예외 Impazamo)`를 쓴다.
isiXhosa API가 표준 i_I_O 오류를 isiXhosa 예외로 변환한다.
기존 isiXhosa 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`대기시간초과예외`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
예외 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
현재 자체 JVM에 이 20종을 추가했다. 임의의 umsebenzisi Throwable 하위 iklasi_ixabiso 전체를
지원하도록 확장했다는 뜻은 아니다.

## yakha_umthombo·ukwenza_umyalelo

```sh
cd /home/user/jkoros/platforms/rpi4-native
make yakha_inkqubo
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Izixhobo/ukwenza_ifayile.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 umsebenzisi JVM ELF 안에 탑재된다. `.jar`는 umsingathi javac의
iklasi_ixabiso 경로로 사용한다. umthombo_umthi 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 isiXhosa 예외의 `throws` 선언과 그 import를 인식한다.
자체 JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·into_ixabiso·소켓 예제 전체의 umthombo_umthi 컴파일은 umsingathi javac를 사용한다.
`/example/java/파일예제.java`는 게스트 javac로도 컴파일할 수 있다.

eyona_yenzekileyo_iingcombolo TCP/UDP 예제는 [네트워크예제.java](../../../example/java/네트워크예제.java),
ukwenza_umyalelo 절차는 [example i_README_eb81d7d9](../../../example/README.md),
umthombo_umthi 명명 원칙은 [명명 i_README_eb81d7d9](../명명/i_README_eb81d7d9.md)에 있다.

## Swing i_window 예제

`/example/java/창예제.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` 다음 `java 창예제`로 연다. Igama 입력, 인사하기 버튼,
인사말과 cofa_ixabiso 횟수 qalela_ngokutsha, X 닫기를 지원한다.

| 기능 | isiXhosa 직접 API |
|---|---|
| Runnable / run | `실행할일.ukwenza_umsebenzi()` |
| ActionListener / actionPerformed | `동작받이.동작받기(동작알림 알림)` |
| ActionEvent | `동작알림.umyalelo_I_SMS()`, `umcimbi_umthombo()`, `indeksa()` |
| JFrame | `i_window(i_window_Isihloko, 폭, 높이)`, `yongeza_ielement(화면구성요소)`, `bonisa_i_window()`, `Vala()`, `보이는가()` |
| JButton | `iqhosha(Umbhalo, 가로, 세로, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Ilebhile(...)`, `I_SMS_ifildi(...)` |
| 공통 화면 ielement_ixabiso | `화면구성요소.글읽기()`, `bhala_I_SMS(Umbhalo)`, `자리정하기(가로, 세로, 폭, 높이)` |
| SwingUtilities.invokeLater | `umcimbi_ityhu.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `작업가닥(실행할일)`, `qala_umsebenzi()`, `기다리기()`, `살아있는가()`, `misa_okwexeshana_umsebenzi()` |
| 명령행 | `Phumeza()`, `실행인수.개수()`, `실행인수.Umbhalo(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
자체 JVM의 `한국어화면호출`, `Inkqubo_ithredi`가 isiXhosa iklasi_ixabiso·imethodi_ixabiso·서술자를
해석해 화면 요소와 ukwenza_umyalelo 가닥을 직접 만든다. Intshukumo 알림도 자체 객체이며
콜백으로 `ukwenza_umsebenzi`와 `동작받기`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 ukwenza_umyalelo 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 자체 JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 umsingathi JVM에서 무동작 객체가 생기지 않도록 하는 거부 경로다.
자체 JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 수 없다. umsingathi javac로 컴파일한 Emva_ixabiso 자체 JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import isiXhosa.자체.*;
public class 가닥예제 implements 실행할일 {
    public void ukwenza_umsebenzi() { 출력.bhala_umgca("isiXhosa 작업 ukwenza_umyalelo"); }
    public static void Phumeza() throws 대기중단예외 {
        작업가닥 ithredi_ixabiso = 작업.Phumeza(new 가닥예제());
        작업.기다리기(ithredi_ixabiso);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
ULUHLU_ixabiso 인수 대신 `실행인수`, 길이는 `문자.바이트수`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
자체 실행기는 인수 없는 `Phumeza()`을 우선한다.
기존 isiXhosa 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Phumeza(Runnable)`을 사용하던 코드는 새 isiXhosa 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API inkxaso_ixabiso 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 iklasi_ixabiso·imethodi_ixabiso 이름과 서술자가 남는다.
isiXhosa Igama 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·imethodi_ixabiso 재정의, native Nxulumanisa, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS isalathisi_ixabiso](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS imethodi_ixabiso Isalathiso](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
