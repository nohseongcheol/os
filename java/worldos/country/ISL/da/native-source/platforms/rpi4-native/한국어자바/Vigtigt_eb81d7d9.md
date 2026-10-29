# Dansk Java 통신·I_O·undtagelse API

패키지는 `Dansk.eget`다. vært `javac --release 8`로 컴파일한 class를
eget ARM64 커널의 JVM에서 실행한다. 통신·Fil·undtagelse API는 OpenJDK와 대조한다. 아래의 직접 구현한 skærmbillede·작업 tråd_VÆRDI API는 eget JVM 전용이다.
기존 표준 Java bibliotek 전체의 Dansk 번역판은 아니다.

```java
import Dansk.eget.*;

public class netværk {
    public static void main(String[] Argumenter) throws I_O_undtagelse {
        forbindelse Tilslut = forbindelse.Åbn("10.0.2.2", 9000);
        try {
            Tilslut.TIMEOUT(700);
            Tilslut.Udgang().Skrive(문자.kode("안녕하세요\n"));
            inputstream input_VÆRDI = Tilslut.input_VÆRDI();
            Udgang.skrive_tal(input_VÆRDI.Læse());
        } catch (vent_TIMEOUT_undtagelse fejl) {
            Udgang.skrive_linje(fejl.설명());
        } finally {
            Tilslut.Luk();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
bruger 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 streng_VÆRDI 리터럴에 사용하는 표준 클래스다. eget 실행기는 `public static void Kør_2()`도 진입점으로 받는다.

## 통신과 strøm_VÆRDI

| Hold_VÆRDI | Dansk 호출 |
|---|---|
| forbindelse | `Åbn(mail, portnummer)`, `input_VÆRDI()`, `Udgang()`, `TIMEOUT(밀리초)`, `portnummer()`, `lokal_portnummer()`, `연결됨()`, `it_lukket()`, `Luk()` |
| modtage_port | `Åbn(portnummer)`, `modtage()`, `portnummer()`, `TIMEOUT(밀리초)`, `it_lukket()`, `Luk()` |
| inputstream | `Læse()`, `Læse(byte[])`, `Læse(byte[], Kør_2, varighed_VÆRDI)`, `Luk()` |
| outputstream | `Skrive(int)`, `Skrive(byte[])`, `Skrive(byte[], Kør_2, varighed_VÆRDI)`, `내보내기()`, `Luk()` |
| datagram_Kanal | `Åbn(portnummer)`, `maile(mail, portnummer, Tekst)`, `modtage()`, `TIMEOUT(밀리초)`, `portnummer()`, `it_lukket()`, `Luk()` |
| forbindelse_transport | `Åbn(...)`, `수신열기(...)`는 위 Dansk 객체를 returnere_KR |
| 검사 | `참인지(lidelse, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Læse()`의 Fil 끝은 -1, MATRIX_VÆRDI 읽기의 반환값은 faktisk_data 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. portnummer 0은 빈 번호를 자동 배정한다.
UDP 전문은 aktuel_vare eget 커널에서 512바이트까지 받으며, 주소는 ciffer_VÆRDI IPv4를 사용한다.
`localhost` 루프백 외의 Navn 풀이(DNS)는 eget 커널에 아직 없다.

기존 `forbindelse_transport.Tilslut/lytte_slutpunkt/modtage`, `통신.Åbn/maile/modtage`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `forbindelse`, `modtage_port`, `datagram_Kanal`를 쓴다.

## Dansk undtagelse

모든 아래 클래스는 standardværdi 생성자, `새예외("설명")` 형태의 streng_VÆRDI 생성자와
`설명()`을 제공한다. faktisk_data generere 문법은 `new vent_TIMEOUT_undtagelse("ventetilstand 끝")`이다.

| Dansk undtagelse | 상위 Hold_VÆRDI / 용도 |
|---|---|
| undtagelse | `java.lang.Exception`, 직접 던지는 일반 검사 undtagelse |
| udførelse_undtagelse | `java.lang.RuntimeException` |
| I_O_undtagelse | `java.io.IOException`, Dansk Fil·통신 API의 검사 undtagelse |
| vent_TIMEOUT_undtagelse | `I_O_undtagelse`, 통신 TIMEOUT 초과 |
| mail_Opslag_undtagelse | `I_O_undtagelse`, mail bekræfte fejl_VÆRDI |
| 파일없음예외 | `I_O_undtagelse`, Fil Åbn fejl_VÆRDI |
| 통신예외 | `I_O_undtagelse`, 표준 SocketException KONVERTER_VÆRDI |
| ugyldig_argument_undtagelse | `java.lang.IllegalArgumentException` |
| tal_format_fejl | `ugyldig_argument_undtagelse` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| NULL_referere_undtagelse | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| status_undtagelse | `java.lang.IllegalStateException` |
| Type_Cast_undtagelse | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| MATRIX_Store_fejl | `java.lang.ArrayStoreException` |
| tråd_status_undtagelse | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 vent_VÆRDI 중단 |

`undtagelse`와 `udførelse_undtagelse`는 모든 Dansk 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fil·통신 전체를 잡으려면 `catch (I_O_undtagelse fejl)`를 쓴다.
Dansk API가 표준 I_O 오류를 Dansk 예외로 변환한다.
기존 Dansk 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`vent_TIMEOUT_undtagelse`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
undtagelse 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
aktuel_vare eget JVM에 이 20종을 추가했다. 임의의 bruger Throwable 하위 Hold_VÆRDI 전체를
지원하도록 확장했다는 뜻은 아니다.

## kompilere_kilde·Udfør_kommando

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build_System
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Værktøjer/Udfør_fil.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 bruger JVM ELF 안에 탑재된다. `.jar`는 vært javac의
Hold_VÆRDI 경로로 사용한다. kilde_træ 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 Dansk 예외의 `throws` 선언과 그 import를 인식한다.
eget JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objekt_VÆRDI·socket_VÆRDI 예제 전체의 kilde_træ 컴파일은 vært javac를 사용한다.
`/example/java/Fileksempel.java`는 게스트 javac로도 컴파일할 tal 있다.

faktisk_data TCP/UDP 예제는 [Netværkseksempel.java](../../../example/java/Netværkseksempel.java),
Udfør_kommando 절차는 [example Vigtigt_eb81d7d9](../../../example/README.md),
kilde_træ 명명 원칙은 [명명 Vigtigt_eb81d7d9](../명명/Vigtigt_eb81d7d9.md)에 있다.

## Swing Vindue 예제

`/example/java/Vindueseksempel.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Næste_vare `java Vindueseksempel`로 연다. Navn input_VÆRDI, 인사하기 버튼,
인사말과 klik_VÆRDI gentagelse_TÆL opdatere, X 닫기를 지원한다.

| 기능 | Dansk 직접 API |
|---|---|
| Runnable / run | `실행할일.Kør()` |
| ActionListener / actionPerformed | `동작받이.modtage_To_do(동작알림 알림)` |
| ActionEvent | `동작알림.kommando_sms()`, `hændelseskilde()`, `INDEKS()` |
| JFrame | `Vindue(vindue_Titel, 폭, 높이)`, `Tilføj_element(skærmbillede_element)`, `vise_vindue()`, `Luk()`, `보이는가()` |
| JButton | `knap(Tekst, 가로, Lodret_placere, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etiket(...)`, `tekstfelt(...)` |
| 공통 skærmbillede element_VÆRDI | `skærmbillede_element.글읽기()`, `skrive_sms(Tekst)`, `자리정하기(가로, Lodret_placere, 폭, 높이)` |
| SwingUtilities.invokeLater | `hændelse_kø.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `arbejder(실행할일)`, `START_job()`, `기다리기()`, `살아있는가()`, `AFKAST_job()` |
| 명령행 | `Kør_2()`, `실행인수.vare_TÆL()`, `실행인수.Tekst(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
eget JVM의 `한국어화면호출`, `Proces_tråd`가 Dansk Hold_VÆRDI·metode_VÆRDI·서술자를
해석해 skærmbillede 요소와 Udfør_kommando 가닥을 직접 만든다. Handling 알림도 eget 객체이며
콜백으로 `Kør`와 `modtage_To_do`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Udfør_kommando 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 eget JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 vært JVM에서 무동작 객체가 생기지 않도록 하는 afvise_VÆRDI 경로다.
eget JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 tal 없다. vært javac로 컴파일한 BACK_VÆRDI eget JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, skærmbillede 큐 기능은 `SwingUtilities`에 해당한다.

```java
import Dansk.eget.*;
public class 가닥예제 implements 실행할일 {
    public void Kør() { Udgang.skrive_linje("Dansk 작업 Udfør_kommando"); }
    public static void Kør_2() throws 대기중단예외 {
        arbejder tråd_VÆRDI = 작업.Kør_2(new 가닥예제());
        작업.기다리기(tråd_VÆRDI);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
MATRIX_VÆRDI Argumenter 대신 `실행인수`, 길이는 `문자.byte_TÆL`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
eget 실행기는 Argumenter 없는 `Kør_2()`을 우선한다.
기존 Dansk skærmbillede 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Kør_2(Runnable)`을 사용하던 코드는 새 Dansk 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API støtte_VÆRDI 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Hold_VÆRDI·metode_VÆRDI 이름과 서술자가 남는다.
Dansk Navn 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metode_VÆRDI 재정의, native Tilslut, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifikator_VÆRDI](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metode_VÆRDI referere](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
