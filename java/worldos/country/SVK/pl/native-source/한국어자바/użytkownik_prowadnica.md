# jkoros polski biblioteka użytkownik_prowadnica

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 własny x86 jądro_WARTOŚĆ 및 `starsze_źródło/`의 관리 jądro_WARTOŚĆ 모형과 구분한다.

## 1. bieżący_towar 제공하는 biblioteka

패키지는 `polski.자바`, system_operacyjny 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **pomocnik_WARTOŚĆ Klasa_WARTOŚĆ 5개, 공개 statyczny_WARTOŚĆ metoda_WARTOŚĆ 22개, 별도 GUI 프로그램인 obszar_roboczy 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 bieżący_towar ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| Klasa_WARTOŚĆ | metoda_WARTOŚĆ identyfikator | 기능 | plik_źródłowy |
|---|---:|---|---|
| `nazwa_pliku` | 9 | UTF-8 텍스트·bajt_WARTOŚĆ nazwa_pliku, Katalog_WARTOŚĆ, wpis_Lista | [nazwa_pliku.java](plik_źródłowy/polski/자바/nazwa_pliku.java) |
| `문자` | 5 | UTF-8 KONWERTUJ_WARTOŚĆ, NFC normalizować_WARTOŚĆ, KOD_WARTOŚĆ 포인트, ciąg_WARTOŚĆ granica_WARTOŚĆ | [문자.java](plik_źródłowy/polski/자바/문자.java) |
| `komunikacja` | 2 | HTTP(S) GET, TCP Połącz | [komunikacja.java](plik_źródłowy/polski/자바/komunikacja.java) |
| `작업` | 4 | 스레드 Wykonaj_polecenie·chwileczkę_WARTOŚĆ, 고정 Rozmiar 작업 program_Launcher | [작업.java](plik_źródłowy/polski/자바/작업.java) |
| `화면` | 2 | Swing 이벤트 Proces_WARTOŚĆ_wpis 가닥에 작업 예약, Okno generować | [화면.java](plik_źródłowy/polski/자바/화면.java) |
| `obszar_roboczy` | punkt_wejścia `main` | Java plik_źródłowy Edytuj_WARTOŚĆ·Store_WARTOŚĆ·kompilować_źródło·Wykonaj_polecenie | [obszar_roboczy.java](plik_źródłowy/polski/자바/obszar_roboczy.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 typ_danych·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing przycisk·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_zadanie

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import polski.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] argumenty) throws Exception {
        Path Katalog_WARTOŚĆ = nazwa_pliku.Twórca_Katalog(nazwa_pliku.ścieżka_2("사용예자료"));
        Path 문서 = Katalog_WARTOŚĆ.resolve("인사.txt");
        nazwa_pliku.Zapis(문서, "한글 😀");
        String treść_WARTOŚĆ_cb0f2404 = nazwa_pliku.Odczyt(문서);
        System.out.println(treść_WARTOŚĆ_cb0f2404);
        System.out.println(문자.kod_znaku_ILE_LICZB(treść_WARTOŚĆ_cb0f2404)); // 한, tekst, 공백, 😀 → 4
        Thread Praca_WARTOŚĆ = 작업.Uruchom_2("인사 작업", () -> System.out.println("작업 Wykonaj_polecenie"));
        작업.기다리기(Praca_WARTOŚĆ);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 wartość_domyślna `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Wykonaj_polecenie 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 Klasa_WARTOŚĆ 폴더를 모두 그 값에 포함해야 한다.

host 저장소에서는 다음처럼 BLD_System·실행한다. host 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 pomocnik_WARTOŚĆ API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `nazwa_pliku.Odczyt(...)`처럼 호출한다. 표의 이름은 rzeczywisty_dane źródło_drzewo 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 wyjątek 외에도 잘못된 argumenty 등에 대한 표준 Java Wykonaj_polecenie 시 예외가 발생할 identyfikator 있다.

### nazwa_pliku: `polski.자바.nazwa_pliku`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| metoda_WARTOŚĆ | zwracany_typ | Akcja·choroba |
|---|---|---|
| `ścieżka_2(String Nazwa)` | `Path` | 이름을 ścieżka_2 객체로 KONWERTUJ_WARTOŚĆ. rzeczywisty_dane 파일을 만들지는 않음 |
| `Odczyt(Path ścieżka_2)` | `String` | nazwa_pliku 전체를 UTF-8 텍스트로 읽음 |
| `Zapis(Path ścieżka_2, String treść_WARTOŚĆ_cb0f2404)` | `Path` | UTF-8 Store_WARTOŚĆ. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path ścieżka_2)` | `byte[]` | nazwa_pliku 전체를 bajt_WARTOŚĆ 배열로 읽음 |
| `zapis_bajt_WARTOŚĆ(Path ścieżka_2, byte[] treść_WARTOŚĆ_cb0f2404)` | `Path` | bajt_WARTOŚĆ Store_WARTOŚĆ. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `Twórca_Katalog(Path ścieżka_2)` | `Path` | 필요한 상위 폴더까지 generować |
| `있는가(Path ścieżka_2)` | `boolean` | 존재 여부 확인. 확인할 identyfikator 없는 경우도 `false`Praca_WARTOŚĆ identyfikator 있음 |
| `usunąć_wpis(Path ścieżka_2)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `wpis_Lista(Path ścieżka_2)` | `List<Path>` | 바로 아래 항목을 ścieżka_2 wyrównać_WARTOŚĆ 순서로 Zwrot_KR. 재귀 탐색은 아님 |

`ścieżka_2`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Zapis`와 `zapis_bajt_WARTOŚĆ`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Kanał_WARTOŚĆ API를 사용하는 방식으로 작성할 identyfikator 있다.

### 문자: `polski.자바.문자`

| metoda_WARTOŚĆ | zwracany_typ | Akcja·choroba |
|---|---|---|
| `kodować(String treść_WARTOŚĆ_cb0f2404)` | `byte[]` | 문자열을 UTF-8 바이트로 KONWERTUJ_WARTOŚĆ |
| `odszyfrować_dane(byte[] treść_WARTOŚĆ_cb0f2404)` | `String` | UTF-8 바이트를 문자열로 KONWERTUJ_WARTOŚĆ. 잘못된 입력은 대체 문자로 Proces_WARTOŚĆ_wpis |
| `normalizować_WARTOŚĆ(String treść_WARTOŚĆ_cb0f2404)` | `String` | UNICODE_WARTOŚĆ NFC normalizować_WARTOŚĆ. 예: kompozycja_WARTOŚĆ 자모 `ᄀ` + `ᅡ` → `가` |
| `kod_znaku_ILE_LICZB(String treść_WARTOŚĆ_cb0f2404)` | `int` | UTF-16 KOD_WARTOŚĆ 단위가 아닌 UNICODE_WARTOŚĆ KOD_WARTOŚĆ 포인트 identyfikator |
| `낱말(String treść_WARTOŚĆ_cb0f2404, Locale Język)` | `List<String>` | Przypisz_WARTOŚĆ 언어의 `BreakIterator` 낱말 경계로 나눈 SMS_zakres |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Word_WARTOŚĆ wpis_Lista API는 아니다. `normalizować_WARTOŚĆ`는 입력기나 TŁUMACZ_źródło 기능이 아니다. KOD_WARTOŚĆ 포인트 identyfikator 역시 사람이 보는 znak_WARTOŚĆ 수와 항상 같지는 않다. 여러 KOD_WARTOŚĆ 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### komunikacja: `polski.자바.komunikacja`

| metoda_WARTOŚĆ | zwracany_typ | Akcja·choroba |
|---|---|---|
| `WYCINEK_WARTOŚĆ(URI Adres, Duration limit_czasu)` | `HttpResponse<String>` | HTTP(S) GET. Połącz 및 żądanie limit_czasu Ustawienia. odpowiedź 본문을 UTF-8로 analizować_WARTOŚĆ |
| `punkt_końcowy_połączenia(String Adres, int sprzęt_port, int 제한밀리초)` | `Socket` | TCP Połącz 후 같은 값으로 Odczyt 제한시간도 Ustawienia |

`WYCINEK_WARTOŚĆ`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP błąd 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. bieżący_towar 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`punkt_końcowy_połączenia`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Zapis 전체의 termin_ostateczny_WARTOŚĆ 시간을 보장하는 옵션은 아니다.

```java
var odpowiedź = komunikacja.WYCINEK_WARTOŚĆ(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(odpowiedź.statusCode());
System.out.println(odpowiedź.body());
```

위 조각은 metoda_WARTOŚĆ 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java wyjątek 처리가 필요하다.

### 작업: `polski.자바.작업`

| metoda_WARTOŚĆ | zwracany_typ | Akcja·choroba |
|---|---|---|
| `Uruchom_2(String Nazwa, Runnable Akcja)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Uruchom_2 |
| `기다리기(Thread wątek_WARTOŚĆ)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 Przypisz_WARTOŚĆ wartość_czasu 동안 `sleep()` |
| `Workbench_WARTOŚĆ(int liczba_wątków)` | `ExecutorService` | 고정 Rozmiar 작업 program_Launcher generować. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 używać_WARTOŚĆ 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Proces_WARTOŚĆ_wpis 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 identyfikator 있다.

### 화면: `polski.자바.화면`

| metoda_WARTOŚĆ | zwracany_typ | Akcja·choroba |
|---|---|---|
| `나중에(Runnable Akcja)` | `void` | Swing 이벤트 Proces_WARTOŚĆ_wpis 가닥에 실행을 예약하고 Zwrot_KR |
| `Okno(String okno_Tytuł, JComponent treść_WARTOŚĆ_cb0f2404, int 너비, int wysokość_WARTOŚĆ)` | `JFrame` | treść_WARTOŚĆ_cb0f2404·크기를 지정한 창을 생성해 program_WARTOŚĆ |

`Okno`을 Swing 이벤트 Proces_WARTOŚĆ_wpis wątek_WARTOŚĆ 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
화면.나중에(() -> 화면.Okno(
    "polski 화면", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 identyfikator 있다. 창의 Zamknięte 동작은 `DISPOSE_ON_CLOSE`다. `화면.나중에`가 반환됐다고 Okno 생성이 이미 끝난 것은 아니다.

### obszar_roboczy: Edytuj_WARTOŚĆ·kompilować_źródło GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar polski.자바.obszar_roboczy
```

`~/workspace`의 원문을 Otwórz·저장하고, `javac`로 컴파일해 `java`로 실행한다. Wykonaj_polecenie nazwa_pliku 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 nazwa_pliku·문자 API 클래스가 아니다. 생성하는 Wykonaj_polecenie nazwa_pliku 방식은 [kompilator 설명](../compiler/OpenJDK-plik_wykonywalny.md)을 따른다.

## 4. Python과 C++에서 사용할 identyfikator 있는가?

| metoda_tryb | bieżący_towar deklaracje Stan_WARTOŚĆ | 호출 가능 obcinać |
|---|---|---|
| Java → polski JAR | wartość_domyślna deklaracje | 위 22개 메서드와 obszar_roboczy |
| Python → `java` dziecko_WARTOŚĆ 프로세스 | Python·Java wartość_domyślna deklaracje | 작은 Java 진입점을 통해 호출하고 표준 pozycja_wyjścia·nazwa_pliku 등으로 WYNIK Dalej_WARTOŚĆ |
| Python → JPype → JVM | JPype는 wartość_domyślna 배포에 없음 | 별도 instalować_WARTOŚĆ 후 Java Klasa_WARTOŚĆ·metoda_WARTOŚĆ 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 dołączać_wpis walidować 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` deklaracje | JVM을 생성하고 polski Klasa_WARTOŚĆ·메서드를 직접 호출할 identyfikator 있음 |
| Python용 독립 polski biblioteka | bieżący_towar wartość_domyślna 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 polski 모듈을 별도로 작성 |
| C/C++용 독립 polski biblioteka | własny x86 `posix-kor`와 własny ARM64 커널용 stan_początkowy RAM nazwa_pliku 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SEKUNDA_operand `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SEKUNDA_operand 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Połącz 계층을 거쳐야 한다.

### Python: dołączać_wpis 패키지 없이 호출

Wykonaj_polecenie 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Połączenia.py](예제/다른언어/PYTHON_Połączenia.py)다. Python이 Java 진입점을 실행하고 `문자.kod_znaku_ILE_LICZB`의 liczba_całkowita 결과를 받는다. argumenty 목록을 사용하며 powłoka polecenie 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Wykonaj_polecenie·wyjść_program KOD_WARTOŚĆ·pozycja_wyjścia Proces_WARTOŚĆ_wpis 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_WARTOŚĆ 그 폴더에서 실행한다. 예제 nazwa_pliku 자체는 wartość_domyślna 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Połączenia.py --text '한글 😀'
```

pozycja_wyjścia: `Python → polski.자바.문자.kod_znaku_ILE_LICZB: 4`

이 예제의 Python FUNKCJA_WARTOŚĆ `kod_znaku_ILE_LICZB`는 이번 문서의 Połącz 예제이며 기존에 설치된 Python 라이브러리는 아니다. bieżący_towar 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java obiekt_WARTOŚĆ 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 argumenty·WYNIK 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Dalej_towar 형태로 연결할 identyfikator 있다. **아래는 zaznaczenie_WARTOŚĆ 가능한 Połącz 방법이며, bieżący_towar 배포판에 JPype가 설치돼 있거나 Wykonaj_polecenie 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 Klasa_WARTOŚĆ 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("polski.자바.문자")
    print(문자.kod_znaku_ILE_LICZB(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Połącz 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype instalować_WARTOŚĆ·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 rzeczywisty_dane Wykonaj_polecenie 가능한 예제다. JVM을 작업 스레드에서 생성하고 Dalej_towar 메서드를 찾는다.

```cpp
jclass type = env->FindClass("polski/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "kod_znaku_ILE_LICZB", "(Ljava/lang/String;)I");
```

JVM generować·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generować·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_WARTOŚĆ 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

pozycja_wyjścia: `C++ → polski.자바.문자.kod_znaku_ILE_LICZB: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI ciąg_WARTOŚĆ format_WARTOŚĆ](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 polski 메서드도 JNI 서명과 argumenty 자료형을 맞춰 호출할 identyfikator 있다. 예를 들어 `Path`를 받는 nazwa_pliku API는 먼저 `nazwa_pliku.ścieżka_2`로 Java ścieżka_2 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Proces_WARTOŚĆ_wpis wątek_WARTOŚĆ 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [własny ARM64 Połącz](../posix-kor/arm64-native/plik_README_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM nazwa_pliku API를 직접 호출하며, 별도 EL0 przestrzeń_użytkownika 라이브러리로 nazwa_pliku/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 polski Java JAR와는 다른 Wykonaj_polecenie 기반이며 własny 커널은 별도 제한형 Java kompilator/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java jądro_WARTOŚĆ nazwa_pliku·UDP 루프백·prostokąt 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. własny 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/plik_README_eb81d7d9.md)에는 `otwarty_Plik`, `파일자료읽기`, `zapis_Plik_dane`, `Zamknij_Plik`, `Twórca_uczestnik`, `wysłać_datagram_dane` 등의 polski C 별칭이 있다. 그러나 구현은 **własny jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 własny `sys/stat.h` 등의 헤더는 bieżący_towar ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 polski Klasa_WARTOŚĆ 라이브러리나 Python용 바인딩을 wartość_domyślna 제공하는 상태도 아니다. bieżący_towar Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 implementacja·빌드해야 한다.

## 5. 확인 범위와 재현

패키지 deklaracje 여부는 [dystrybucja_WARTOŚĆ 패키지 wpis_Lista](../platforms/rpi4/dist/packages.lock.json) 및 BLD_System 루트의 rzeczywisty_dane 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 wartość_domyślna dystrybucja_WARTOŚĆ 목록과 다를 identyfikator 있다.

이번에 **host x86_64/OpenJDK 11에서** Python dziecko_WARTOŚĆ 프로세스 호출과 C++ JNI 직접 호출을 kompilować_źródło·실행해 각각 WYNIK 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Połącz 예제는 dołączać_wpis 패키지를 설치하지 않는다.

문서의 Java używać_WARTOŚĆ 예제도 kompilować_źródło·실행했고, 22개 메서드의 문서 deklaracje 여부와 로컬 문서 링크를 확인했다. [예제 walidować LOG_zapis](build/다른언어/walidacja_Raport.json)

기존 ARM64 QEMU에서는 Java의 nazwa_pliku·UNICODE_WARTOŚĆ·스레드·HTTP 및 Swing testy 결과가 있다. 이번 Python/C++ Połącz 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Wykonaj_polecenie 중인 przestrzeń_użytkownika 환경은 이 문서 작업에서 변경하지 않았다. [기존 system_operacyjny walidować LOG_zapis](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Połączenia.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

host C++ 예제는 위 JNI kompilować_źródło 명령의 JDK 경로를 **host JDK ścieżka_2**로 바꾸고, plik_źródłowy `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·biblioteka 경로를 host x86_64 링크 명령에 섞지 않는다.
