# polski Java komunikacja·We_Wy·wyjątek API

패키지는 `polski.własny`다. host `javac --release 8`로 컴파일한 class를
własny ARM64 커널의 JVM에서 실행한다. komunikacja·nazwa_pliku·wyjątek API는 OpenJDK와 대조한다. 아래의 직접 구현한 화면·작업 wątek_WARTOŚĆ API는 własny JVM 전용이다.
기존 표준 Java biblioteka 전체의 polski 번역판은 아니다.

```java
import polski.własny.*;

public class sieć {
    public static void main(String[] argumenty) throws We_Wy_wyjątek {
        połączenie Połącz = połączenie.Otwórz("10.0.2.2", 9000);
        try {
            Połącz.TIMEOUT(700);
            Połącz.pozycja_wyjścia().Zapis(문자.kodować("안녕하세요\n"));
            strumień_wejściowy wejście_WARTOŚĆ = Połącz.wejście_WARTOŚĆ();
            pozycja_wyjścia.zapis_identyfikator(wejście_WARTOŚĆ.Odczyt());
        } catch (chwileczkę_TIMEOUT_wyjątek błąd) {
            pozycja_wyjścia.zapis_linia(błąd.설명());
        } finally {
            Połącz.Zamknięte();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
przestrzeń_użytkownika 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 ciąg_WARTOŚĆ 리터럴에 사용하는 표준 클래스다. własny 실행기는 `public static void Uruchom_2()`도 진입점으로 받는다.

## 통신과 Stream_WARTOŚĆ

| Klasa_WARTOŚĆ | polski 호출 |
|---|---|
| połączenie | `Otwórz(Adres, numer_portu)`, `wejście_WARTOŚĆ()`, `pozycja_wyjścia()`, `TIMEOUT(밀리초)`, `numer_portu()`, `lokalny_numer_portu()`, `연결됨()`, `systemy_informacyjne_zamknięta()`, `Zamknięte()` |
| odbierać_port | `Otwórz(numer_portu)`, `odbierać()`, `numer_portu()`, `TIMEOUT(밀리초)`, `systemy_informacyjne_zamknięta()`, `Zamknięte()` |
| strumień_wejściowy | `Odczyt()`, `Odczyt(byte[])`, `Odczyt(byte[], Uruchom_2, długość_WARTOŚĆ)`, `Zamknięte()` |
| strumień_wyjściowy | `Zapis(int)`, `Zapis(byte[])`, `Zapis(byte[], Uruchom_2, długość_WARTOŚĆ)`, `내보내기()`, `Zamknięte()` |
| datagram_Kanał | `Otwórz(numer_portu)`, `wysłać(Adres, numer_portu, tekst)`, `odbierać()`, `TIMEOUT(밀리초)`, `numer_portu()`, `systemy_informacyjne_zamknięta()`, `Zamknięte()` |
| połączenie_transport | `Otwórz(...)`, `수신열기(...)`는 위 polski 객체를 Zwrot_KR |
| 검사 | `참인지(choroba, 까닭)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`Odczyt()`의 nazwa_pliku 끝은 -1, TABLICA_WARTOŚĆ 읽기의 반환값은 rzeczywisty_dane 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. numer_portu 0은 빈 번호를 자동 배정한다.
UDP 전문은 bieżący_towar własny 커널에서 512바이트까지 받으며, 주소는 cyfra_WARTOŚĆ IPv4를 사용한다.
`localhost` 루프백 외의 Nazwa 풀이(DNS)는 własny 커널에 아직 없다.

기존 `połączenie_transport.Połącz/nasłuchiwać_uczestnik/odbierać`, `komunikacja.Otwórz/wysłać/odbierać`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `połączenie`, `odbierać_port`, `datagram_Kanał`를 쓴다.

## polski wyjątek

모든 아래 클래스는 wartość_domyślna 생성자, `새예외("설명")` 형태의 ciąg_WARTOŚĆ 생성자와
`설명()`을 제공한다. rzeczywisty_dane generować 문법은 `new chwileczkę_TIMEOUT_wyjątek("stan_oczekiwania 끝")`이다.

| polski wyjątek | 상위 Klasa_WARTOŚĆ / 용도 |
|---|---|
| wyjątek | `java.lang.Exception`, 직접 던지는 일반 검사 wyjątek |
| wykonanie_wyjątek | `java.lang.RuntimeException` |
| We_Wy_wyjątek | `java.io.IOException`, polski nazwa_pliku·komunikacja API의 검사 wyjątek |
| chwileczkę_TIMEOUT_wyjątek | `We_Wy_wyjątek`, komunikacja TIMEOUT 초과 |
| ADRES_WYSZUKAJ_wyjątek | `We_Wy_wyjątek`, Adres 확인 awaria_WARTOŚĆ |
| 파일없음예외 | `We_Wy_wyjątek`, nazwa_pliku Otwórz awaria_WARTOŚĆ |
| komunikacja_wyjątek | `We_Wy_wyjątek`, 표준 SocketException KONWERTUJ_WARTOŚĆ |
| nieważny_argument_wyjątek | `java.lang.IllegalArgumentException` |
| identyfikator_format_awaria | `nieważny_argument_wyjątek` |
| 범위예외 | `java.lang.IndexOutOfBoundsException` |
| granice_tablicy_wyjątek / 문자열범위예외 | `범위예외` |
| pusta_referencja_wyjątek | `java.lang.NullPointerException` |
| 산술예외 | `java.lang.ArithmeticException` |
| Stan_wyjątek | `java.lang.IllegalStateException` |
| TYP_koercja_wyjątek | `java.lang.ClassCastException` |
| negatywny_TABLICA_zmienić_rozmiar_awaria | `java.lang.NegativeArraySizeException` |
| TABLICA_Store_awaria | `java.lang.ArrayStoreException` |
| wątek_Stan_wyjątek | `java.lang.IllegalThreadStateException` |
| 대기중단예외 | `java.lang.InterruptedException`, `작업.기다리기`의 chwileczkę_WARTOŚĆ 중단 |

`wyjątek`와 `wykonanie_wyjątek`는 모든 polski 예외의 공통 부모가 아니다. 위 상속 관계를
사용하며, nazwa_pliku·komunikacja 전체를 잡으려면 `catch (We_Wy_wyjątek błąd)`를 쓴다.
polski API가 표준 We_Wy 오류를 polski 예외로 변환한다.
기존 polski komunikacja 호출에서 `SocketTimeoutException`을 잡던 코드는
`chwileczkę_TIMEOUT_wyjątek`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
wyjątek 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
bieżący_towar własny JVM에 이 20종을 추가했다. 임의의 przestrzeń_użytkownika Throwable 하위 Klasa_WARTOŚĆ 전체를
지원하도록 확장했다는 뜻은 아니다.

## kompilować_źródło·Wykonaj_polecenie

```sh
cd /home/user/jkoros/platforms/rpi4-native
make BLD_System
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 testy/자바/한국어통신시험.java
python3 narzędzia/Wykonaj_Plik.py build/한국어사용/한국어통신시험.class
make test-jvm
```

내장 라이브러리는 przestrzeń_użytkownika JVM ELF 안에 탑재된다. `.jar`는 host javac의
Klasa_WARTOŚĆ 경로로 사용한다. źródło_drzewo 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 polski 예외의 `throws` 선언과 그 import를 인식한다.
własny JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·obiekt_WARTOŚĆ·gniazdo_WARTOŚĆ 예제 전체의 źródło_drzewo 컴파일은 host javac를 사용한다.
`/example/java/PrzykładPliku.java`는 게스트 javac로도 컴파일할 identyfikator 있다.

rzeczywisty_dane TCP/UDP 예제는 [PrzykładSieci.java](../../../example/java/PrzykładSieci.java),
Wykonaj_polecenie 절차는 [example plik_README_eb81d7d9](../../../example/README.md),
źródło_drzewo 명명 원칙은 [명명 plik_README_eb81d7d9](../명명/plik_README_eb81d7d9.md)에 있다.

## Swing Okno 예제

`/example/java/PrzykładOkna.java`와 컴파일된 `.class`가 rozruch_maszyny 시 준비된다.
`cd /example/java` Dalej_towar `java PrzykładOkna`로 연다. Nazwa wejście_WARTOŚĆ, 인사하기 버튼,
인사말과 klikać_WARTOŚĆ powtórzenie_ILE_LICZB odświeżyć, X 닫기를 지원한다.

| 기능 | polski 직접 API |
|---|---|
| Runnable / run | `실행할일.Uruchom()` |
| ActionListener / actionPerformed | `동작받이.odbierać_akcja(akcja_powiadomienie powiadomienie)` |
| ActionEvent | `akcja_powiadomienie.polecenie_SMS()`, `źródło_zdarzenia()`, `INDEKS()` |
| JFrame | `Okno(okno_Tytuł, 폭, wysokość_WARTOŚĆ)`, `Dodaj_element(화면구성요소)`, `program_okno()`, `Zamknięte()`, `보이는가()` |
| JButton | `przycisk(tekst, 가로, gałąź_stanowisko, 폭, wysokość_WARTOŚĆ, 받이)`, `동작맡기기(받이)` |
| JLabel / JTextField | `Etykieta(...)`, `pole_tekstowe(...)` |
| 공통 화면 element_WARTOŚĆ | `화면구성요소.글읽기()`, `zapis_SMS(tekst)`, `자리정하기(가로, gałąź_stanowisko, 폭, wysokość_WARTOŚĆ)` |
| SwingUtilities.invokeLater | `konkurs_kolejka.나중에실행(실행할일)`, `사건처리중인가()` |
| Thread | `pracownik(실행할일)`, `START_zadanie()`, `기다리기()`, `살아있는가()`, `Dochód_zadanie()` |
| 명령행 | `Uruchom_2()`, `실행인수.towar_ILE_LICZB()`, `실행인수.tekst(순번)` |

위 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
własny JVM의 `한국어화면호출`, `Proces_wątek`가 polski Klasa_WARTOŚĆ·metoda_WARTOŚĆ·서술자를
해석해 화면 요소와 Wykonaj_polecenie 가닥을 직접 만든다. Akcja 알림도 własny 객체이며
콜백으로 `Uruchom`와 `odbierać_akcja`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 Wykonaj_polecenie 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 własny JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 host JVM에서 무동작 객체가 생기지 않도록 하는 odrzucić_WARTOŚĆ 경로다.
własny JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 implementacja API를
실행할 identyfikator 없다. host javac로 컴파일한 BACK_WARTOŚĆ własny JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, 화면 큐 기능은 `SwingUtilities`에 해당한다.

```java
import polski.własny.*;
public class 가닥예제 implements 실행할일 {
    public void Uruchom() { pozycja_wyjścia.zapis_linia("polski 작업 Wykonaj_polecenie"); }
    public static void Uruchom_2() throws 대기중단예외 {
        pracownik wątek_WARTOŚĆ = 작업.Uruchom_2(new 가닥예제());
        작업.기다리기(wątek_WARTOŚĆ);
    }
}
```

`example/java`의 다섯 소스는 예약어·리터럴 외 식별자를 한국어로 작성한다.
TABLICA_WARTOŚĆ argumenty 대신 `실행인수`, 길이는 `문자.bajt_ILE_LICZB`를 사용한다.
표준 Java의 `main(String[])`도 계속 지원한다. 둘 다 정의되어 있으면
własny 실행기는 argumenty 없는 `Uruchom_2()`을 우선한다.
기존 polski 화면 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`작업.Uruchom_2(Runnable)`을 사용하던 코드는 새 polski 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API wsparcie_WARTOŚĆ 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 Klasa_WARTOŚĆ·metoda_WARTOŚĆ 이름과 서술자가 남는다.
polski Nazwa 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 부분,
상속·metoda_WARTOŚĆ 재정의, native Połącz, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identyfikator_WARTOŚĆ](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS metoda_WARTOŚĆ odwołanie](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)다.
