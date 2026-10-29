# magyar Java kommunikáció·I_O·kivétel API

패키지는 `magyar.saját`다. gazda `javac --release 8`로 컴파일한 class를
saját ARM64 커널의 JVM에서 실행한다. kommunikáció·Fájl·kivétel API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 szál_ÉRTÉK API는 saját JVM 전용이다.
기존 표준 Java kódtár 전체의 magyar 번역판은 아니다.

```java
import magyar.saját.*;

public class hálózat {
    public static void main(String[] Argumentumok) throws I_O_kivétel {
        ismerős Kapcsolódás = ismerős.Megnyitás("10.0.2.2", 9000);
        try {
            Kapcsolódás.IDŐTÚLLÉPÉS(700);
            Kapcsolódás.Kimenet().Írás(문자.kódolás("안녕하세요\n"));
            bemeneti_adatfolyam bevitel_ÉRTÉK = Kapcsolódás.bevitel_ÉRTÉK();
            Kimenet.ír_szám(bevitel_ÉRTÉK.Olvasás());
        } catch (várj_IDŐTÚLLÉPÉS_kivétel HIBA) {
            Kimenet.ír_sor(HIBA.설명());
        } finally {
            Kapcsolódás.Bezárás();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
felhasználó 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 sztring_ÉRTÉK 리터럴에 사용하는 표준 클래스다. saját 실행기는 `public static void Futtatás()`도 진입점으로 받는다.

## 통신과 Stream_ÉRTÉK

| tanóra_ÉRTÉK | magyar 호출 |
|---|---|
| ismerős | `Megnyitás(CÍM, portszám)`, `bevitel_ÉRTÉK()`, `Kimenet()`, `IDŐTÚLLÉPÉS(밀리초)`, `portszám()`, `helyi_portszám()`, `연결됨()`, `informatikai_részleg_lezárt()`, `Bezárás()` |
| fogad_port | `Megnyitás(portszám)`, `fogad()`, `portszám()`, `IDŐTÚLLÉPÉS(밀리초)`, `informatikai_részleg_lezárt()`, `Bezárás()` |
| bemeneti_adatfolyam | `Olvasás()`, `Olvasás(byte[])`, `Olvasás(byte[], Futtatás, hossz_ÉRTÉK)`, `Bezárás()` |
| kimeneti_adatfolyam | `Írás(int)`, `Írás(byte[])`, `Írás(byte[], Futtatás, hossz_ÉRTÉK)`, `내보내기()`, `Bezárás()` |
| datagram_Csatorna | `Megnyitás(portszám)`, `küld(CÍM, portszám, Szöveg)`, `fogad()`, `IDŐTÚLLÉPÉS(밀리초)`, `portszám()`, `informatikai_részleg_lezárt()`, `Bezárás()` |
| ismerős_szállítás | `Megnyitás(...)`, `수신열기(...)`는 위 magyar 객체를 visszaküld_KR |
| 검사 | `참인지(állapot, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Olvasás()`의 Fájl 끝은 -1, TÖMB_ÉRTÉK 읽기의 반환값은 tényleges_adat 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. portszám 0은 빈 번호를 자동 배정한다.
UDP 전문은 aktuális_cikk saját 커널에서 512바이트까지 받으며, 주소는 számjegy_ÉRTÉK IPv4를 사용한다.
`localhost` 루프백 외의 Név 풀이(DNS)는 saját 커널에 아직 없다.

기존 `ismerős_szállítás.Kapcsolódás/figyelés_végpont/fogad`, `kommunikáció.Megnyitás/küld/fogad`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `ismerős`, `fogad_port`, `datagram_Csatorna`를 쓴다.

## magyar kivétel

모든 아래 클래스는 alapértelmezett_érték 생성자, `새예외("설명")` 형태의 sztring_ÉRTÉK 생성자와
`설명()`을 제공한다. tényleges_adat generálás 문법은 `new várj_IDŐTÚLLÉPÉS_kivétel("várakozóállapot 끝")`이다.

| magyar kivétel | 상위 tanóra_ÉRTÉK / 용도 |
|---|---|
| kivétel | `java.lang.Exception`, 직접 던지는 일반 검사 kivétel |
| végrehajtás_kivétel | `java.lang.RuntimeException` |
| I_O_kivétel | `java.io.IOException`, magyar Fájl·kommunikáció API의 검사 kivétel |
| várj_IDŐTÚLLÉPÉS_kivétel | `I_O_kivétel`, kommunikáció IDŐTÚLLÉPÉS 초과 |
| CÍM_KERES_kivétel | `I_O_kivétel`, CÍM igazol hiba_ÉRTÉK |
| 파일없음예외 | `I_O_kivétel`, Fájl Megnyitás hiba_ÉRTÉK |
| kommunikáció_kivétel | `I_O_kivétel`, 표준 SocketException konvertál_ÉRTÉK |
| alaptalan_argumentum_kivétel | `java.lang.IllegalArgumentException` |
| szám_formáz_hiba | `alaptalan_argumentum_kivétel` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| null_hivatkozik_kivétel | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Állapot_kivétel | `java.lang.IllegalStateException` |
| beír_Átjátszás_kivétel | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| TÖMB_tár_hiba | `java.lang.ArrayStoreException` |
| szál_Állapot_kivétel | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 várj_ÉRTÉK 중단 |

`kivétel`와 `végrehajtás_kivétel`는 모든 magyar 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, Fájl·kommunikáció 전체를 잡으려면 `catch (I_O_kivétel HIBA)`를 쓴다.
magyar API가 표준 I_O 오류를 magyar 예외로 변환한다.
기존 magyar kommunikáció 호출에서 `SocketTimeoutException`을 잡던 코드는
`várj_IDŐTÚLLÉPÉS_kivétel`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
kivétel 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
aktuális_cikk saját JVM에 이 20종을 추가했다. 임의의 felhasználó Throwable 하위 tanóra_ÉRTÉK 전체를
지원하도록 확장했다는 뜻은 아니다.

## épít_forrás·végrehajt_parancs

```sh
cd /home/user/jkoros/platforms/rpi4-native
make épít_Rendszer
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 시험/자바/한국어통신시험.java
python3 Eszközök/végrehajt_Fájl.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 felhasználó JVM ELF 안에 탑재된다. `.jar`는 gazda javac의
tanóra_ÉRTÉK 경로로 사용한다. forrás_fa 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 magyar 예외의 `throws` 선언과 그 import를 인식한다.
saját JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objektum_ÉRTÉK·szoftvercsatorna_ÉRTÉK 예제 전체의 forrás_fa 컴파일은 gazda javac를 사용한다.
`/example/java/FájlPélda.java`는 게스트 javac로도 컴파일할 szám 있다.

tényleges_adat TCP/UDP 예제는 [HálózatiPélda.java](../../../example/java/HálózatiPélda.java),
végrehajt_parancs 절차는 [example fontos_fájl_eb81d7d9](../../../example/README.md),
forrás_fa 명명 원칙은 [명명 fontos_fájl_eb81d7d9](../명명/fontos_fájl_eb81d7d9.md)에 있다.

## Swing Ablak 예제

`/example/java/AblakPélda.java`와 컴파일된 `.class`가 부팅 시 준비된다.
`cd /example/java` Tovább_cikk `java AblakPélda`로 연다. Név bevitel_ÉRTÉK, 인사하기 버튼,
인사말과 kattint_ÉRTÉK 횟수 frissít, X 닫기를 지원한다.

| 기능 | magyar 직접 API |
|---|---|
| Runnable / run | `실행할일.Végrehajtás()` |
| ActionListener / actionPerformed | `동작받이.fogad_Action(Action_alapelv alapelv)` |
| ActionEvent | `Action_alapelv.parancs_SMS()`, `eseményforrás()`, `INDEX()` |
| JFrame | `Ablak(ablak_Cím, 폭, 높이)`, `hozzáad_elem(화면구성요소)`, `bemutató_ablak()`, `Bezárás()`, `보이는가()` |
| JButton | `gomb(Szöveg, 가로, szektor_pozíció, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Címke(...)`, `szövegmező(...)` |
| 공통 화면 elem_ÉRTÉK | `화면구성요소.글읽기()`, `ír_SMS(Szöveg)`, `자리정하기(가로, szektor_pozíció, 폭, 높이)` |
| SwingUtilities.invokeLater | `esemény_várólista.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `dolgozó(실행할일)`, `START_teendő()`, `기다리기()`, `살아있는가()`, `HOZAM_teendő()` |
| 명령행 | `Futtatás()`, `실행인수.cikk_DARAB()`, `실행인수.Szöveg(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
saját JVM의 `한국어화면호출`, `folyamat_szál`가 magyar tanóra_ÉRTÉK·metódus_ÉRTÉK·서술자를
해석해 화면 요소와 végrehajt_parancs 가닥을 직접 만든다. Művelet 알림도 saját 객체이며
콜백으로 `Végrehajtás`와 `fogad_Action`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 végrehajt_parancs 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 saját JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 gazda JVM에서 무동작 객체가 생기지 않도록 하는 elutasít_ÉRTÉK 경로다.
saját JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 구현 API를
실행할 szám 없다. gazda javac로 컴파일한 BACK_ÉRTÉK saját JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import magyar.saját.*;
public class 가닥예제 implements 실행할일 {
    public void Végrehajtás() { Kimenet.ír_sor("magyar 작업 végrehajt_parancs"); }
    public static void Futtatás() throws 대기중단예외 {
        dolgozó szál_ÉRTÉK = 작업.Futtatás(new 가닥예제());
        작업.기다리기(szál_ÉRTÉK);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
TÖMB_ÉRTÉK Argumentumok 대신 `실행인수`, 길이는 `문자.bájt_DARAB`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
saját 실행기는 Argumentumok 없는 `Futtatás()`을 우선한다.
기존 magyar 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Futtatás(Runnable)`을 사용하던 코드는 새 magyar 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API támogat_ÉRTÉK 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 tanóra_ÉRTÉK·metódus_ÉRTÉK 이름과 서술자가 남는다.
magyar Név 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metódus_ÉRTÉK 재정의, native Kapcsolódás, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS azonosító_ÉRTÉK](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metódus_ÉRTÉK hivatkozik](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
