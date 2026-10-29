# suomi Java 통신·I_O·poikkeus API

패키지는 `suomi.oma`다. isäntä `javac --release 8`로 컴파일한 class를
oma ARM64 커널의 JVM에서 실행한다. 통신·tiedoston_nimi·poikkeus API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 säie_ARVO API는 oma JVM 전용이다.
기존 표준 Java kirjasto 전체의 suomi 번역판은 아니다.

```java
import suomi.oma.*;

public class verkko {
    public static void main(String[] argumentit) throws I_O_poikkeus {
        yhteys Yhdistä = yhteys.Avaa("10.0.2.2", 9000);
        try {
            Yhdistä.AIKAKATKAISU(700);
            Yhdistä.tulostuspaikka().Kirjoitus(문자.koodata("안녕하세요\n"));
            syötevirta syöte_ARVO = Yhdistä.syöte_ARVO();
            tulostuspaikka.kirjoitus_numero(syöte_ARVO.Luku());
        } catch (odottaa_AIKAKATKAISU_poikkeus VIRHE) {
            tulostuspaikka.kirjoitus_rivi(VIRHE.설명());
        } finally {
            Yhdistä.Sulje();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
käyttäjätila 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 merkkijono_ARVO 리터럴에 사용하는 표준 클래스다. oma 실행기는 `public static void Suorita_2()`도 진입점으로 받는다.

## 통신과 virta_ARVO

| Luokka_ARVO | suomi 호출 |
|---|---|
| yhteys | `Avaa(OSOITE, portin_numero)`, `syöte_ARVO()`, `tulostuspaikka()`, `AIKAKATKAISU(밀리초)`, `portin_numero()`, `paikallinen_portin_numero()`, `연결됨()`, `tietojärjestelmät_suljettu()`, `Sulje()` |
| saada_portti | `Avaa(portin_numero)`, `saada()`, `portin_numero()`, `AIKAKATKAISU(밀리초)`, `tietojärjestelmät_suljettu()`, `Sulje()` |
| syötevirta | `Luku()`, `Luku(byte[])`, `Luku(byte[], Suorita_2, kesto_ARVO)`, `Sulje()` |
| tietovirta | `Kirjoitus(int)`, `Kirjoitus(byte[])`, `Kirjoitus(byte[], Suorita_2, kesto_ARVO)`, `내보내기()`, `Sulje()` |
| datagrammi_Media | `Avaa(portin_numero)`, `lähettää(OSOITE, portin_numero, teksti)`, `saada()`, `AIKAKATKAISU(밀리초)`, `portin_numero()`, `tietojärjestelmät_suljettu()`, `Sulje()` |
| yhteys_välitys | `Avaa(...)`, `수신열기(...)`는 위 suomi 객체를 palauttaa_KR |
| 검사 | `참인지(ehto, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Luku()`의 tiedoston_nimi 끝은 -1, MATRIISI_ARVO 읽기의 반환값은 todellinen_data 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. portin_numero 0은 빈 번호를 자동 배정한다.
UDP 전문은 nykyinen_kohde oma 커널에서 512바이트까지 받으며, 주소는 numero_ARVO IPv4를 사용한다.
`localhost` 루프백 외의 Nimi 풀이(DNS)는 oma 커널에 아직 없다.

기존 `yhteys_välitys.Yhdistä/kuunnella_päätepiste/saada`, `통신.Avaa/lähettää/saada`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `yhteys`, `saada_portti`, `datagrammi_Media`를 쓴다.

## suomi poikkeus

모든 아래 클래스는 oletusarvo 생성자, `새예외("설명")` 형태의 merkkijono_ARVO 생성자와
`설명()`을 제공한다. todellinen_data generoida 문법은 `new odottaa_AIKAKATKAISU_poikkeus("odotustila 끝")`이다.

| suomi poikkeus | 상위 Luokka_ARVO / 용도 |
|---|---|
| poikkeus | `java.lang.Exception`, 직접 던지는 일반 검사 poikkeus |
| suoritus_poikkeus | `java.lang.RuntimeException` |
| I_O_poikkeus | `java.io.IOException`, suomi tiedoston_nimi·통신 API의 검사 poikkeus |
| odottaa_AIKAKATKAISU_poikkeus | `I_O_poikkeus`, 통신 AIKAKATKAISU 초과 |
| OSOITE_HAKU_poikkeus | `I_O_poikkeus`, OSOITE tarkistaa virhe_ARVO |
| 파일없음예외 | `I_O_poikkeus`, tiedoston_nimi Avaa virhe_ARVO |
| 통신예외 | `I_O_poikkeus`, 표준 SocketException MUUNNA_ARVO |
| pätemätön_argumentti_poikkeus | `java.lang.IllegalArgumentException` |
| numero_muoto_virhe | `pätemätön_argumentti_poikkeus` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| 배열범위예외 / 문자열범위예외 | `범위예외` |
| TYHJÄ_viite_poikkeus | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Tila_poikkeus | `java.lang.IllegalStateException` |
| TYYPPI_lähetys_poikkeus | `java.lang.ClassCastException` |
| 음수배열크기예외 | `java.lang.NegativeArraySizeException` |
| MATRIISI_Store_virhe | `java.lang.ArrayStoreException` |
| säie_Tila_poikkeus | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 odottaa_ARVO 중단 |

`poikkeus`와 `suoritus_poikkeus`는 모든 suomi 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, tiedoston_nimi·통신 전체를 잡으려면 `catch (I_O_poikkeus VIRHE)`를 쓴다.
suomi API가 표준 I_O 오류를 suomi 예외로 변환한다.
기존 suomi 통신 호출에서 `SocketTimeoutException`을 잡던 코드는
`odottaa_AIKAKATKAISU_poikkeus`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
poikkeus 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
nykyinen_kohde oma JVM에 이 20종을 추가했다. 임의의 käyttäjätila Throwable 하위 Luokka_ARVO 전체를
지원하도록 확장했다는 뜻은 아니다.

## kääntää_lähde·Suorita_komento

```sh
cd /home/user/jkoros/platforms/rpi4-native
make kääntää_Järjestelmä
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 testit/자바/한국어통신시험.java
python3 työkalut/Suorita_Tiedosto.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 käyttäjätila JVM ELF 안에 탑재된다. `.jar`는 isäntä javac의
Luokka_ARVO 경로로 사용한다. lähde_puu 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 suomi 예외의 `throws` 선언과 그 import를 인식한다.
oma JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objekti_ARVO·vastake_ARVO 예제 전체의 lähde_puu 컴파일은 isäntä javac를 사용한다.
`/example/java/Tiedostoesimerkki.java`는 게스트 javac로도 컴파일할 numero 있다.

todellinen_data TCP/UDP 예제는 [Verkkoesimerkki.java](../../../example/java/Verkkoesimerkki.java),
Suorita_komento 절차는 [example Lueminut_eb81d7d9](../../../example/README.md),
lähde_puu 명명 원칙은 [명명 Lueminut_eb81d7d9](../명명/Lueminut_eb81d7d9.md)에 있다.

## Swing Ikkuna 예제

`/example/java/Ikkunaesimerkki.java`와 컴파일된 `.class`가 koneen_käynnistys 시 준비된다.
`cd /example/java` Seuraava_kohde `java Ikkunaesimerkki`로 연다. Nimi syöte_ARVO, 인사하기 버튼,
인사말과 osoittaa_ARVO toisto_LASKE päivittää, X 닫기를 지원한다.

| 기능 | suomi 직접 API |
|---|---|
| Runnable / run | `실행할일.Suorita()` |
| ActionListener / actionPerformed | `동작받이.saada_toimi(동작알림 알림)` |
| ActionEvent | `동작알림.komento_SMS()`, `tapahtumalähde()`, `INDEKSI()` |
| JFrame | `Ikkuna(ikkuna_nimi, 폭, 높이)`, `Lisää_elementti(화면구성요소)`, `näyttää_ikkuna()`, `Sulje()`, `보이는가()` |
| JButton | `painike(teksti, 가로, toimiala_toimi, 폭, 높이, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Nimike(...)`, `tekstikenttä(...)` |
| 공통 화면 elementti_ARVO | `화면구성요소.lukea_SMS()`, `kirjoitus_SMS(teksti)`, `자리정하기(가로, toimiala_toimi, 폭, 높이)` |
| SwingUtilities.invokeLater | `tapahtuma_jono.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `työntekijä(실행할일)`, `alku_tehtävä()`, `기다리기()`, `살아있는가()`, `TUOTTO_tehtävä()` |
| 명령행 | `Suorita_2()`, `실행인수.kohde_LASKE()`, `실행인수.teksti(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
oma JVM의 `한국어화면호출`, `prosessi_säie`가 suomi Luokka_ARVO·menetelmä_ARVO·서술자를
해석해 화면 요소와 Suorita_komento 가닥을 직접 만든다. Toiminto 알림도 oma 객체이며
콜백으로 `Suorita`와 `saada_toimi`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Suorita_komento 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 oma JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 isäntä JVM에서 무동작 객체가 생기지 않도록 하는 hylkää_ARVO_e3ecc00b 경로다.
oma JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 toteutus API를
실행할 numero 없다. isäntä javac로 컴파일한 BACK_ARVO oma JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import suomi.oma.*;
public class 가닥예제 implements 실행할일 {
    public void Suorita() { tulostuspaikka.kirjoitus_rivi("suomi 작업 Suorita_komento"); }
    public static void Suorita_2() throws 대기중단예외 {
        työntekijä säie_ARVO = 작업.Suorita_2(new 가닥예제());
        작업.기다리기(säie_ARVO);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
MATRIISI_ARVO argumentit 대신 `실행인수`, 길이는 `문자.tavu_LASKE`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
oma 실행기는 argumentit 없는 `Suorita_2()`을 우선한다.
기존 suomi 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Suorita_2(Runnable)`을 사용하던 코드는 새 suomi 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API Tuki_ARVO 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Luokka_ARVO·menetelmä_ARVO 이름과 서술자가 남는다.
suomi Nimi 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·menetelmä_ARVO 재정의, native Yhdistä, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS tunniste_ARVO](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS menetelmä_ARVO viite](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
