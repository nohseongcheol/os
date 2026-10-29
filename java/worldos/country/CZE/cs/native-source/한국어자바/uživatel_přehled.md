# jkoros čeština knihovna uživatel_přehled

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 vlastní x86 jádro_HODNOTA 및 `starší_verze_zdroj/`의 관리 jádro_HODNOTA 모형과 구분한다.

## 1. dobrá_zboží 제공하는 knihovna

패키지는 `čeština.자바`, operační_systém 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **pomocná_rutina_HODNOTA Třída_HODNOTA 5개, 공개 statický_HODNOTA metoda_HODNOTA 22개, 별도 GUI 프로그램인 pracovní_prostor 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 dobrá_zboží ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| Třída_HODNOTA | metoda_HODNOTA číslo | 기능 | zdrojový_soubor |
|---|---:|---|---|
| `název_souboru` | 9 | UTF-8 텍스트·bajt_HODNOTA název_souboru, Adresář_HODNOTA, položka_Seznam | [název_souboru.java](zdrojový_soubor/čeština/자바/název_souboru.java) |
| `문자` | 5 | UTF-8 CONVERT_HODNOTA, NFC normalizovat_HODNOTA, KÓD_HODNOTA 포인트, řetězec_HODNOTA mez_HODNOTA | [문자.java](zdrojový_soubor/čeština/자바/문자.java) |
| `komunikace` | 2 | HTTP(S) GET, TCP Připojit | [komunikace.java](zdrojový_soubor/čeština/자바/komunikace.java) |
| `작업` | 4 | 스레드 Provést_příkaz·počkej_HODNOTA, 고정 Velikost 작업 program_Launcher | [작업.java](zdrojový_soubor/čeština/자바/작업.java) |
| `화면` | 2 | Swing 이벤트 Proces_HODNOTA_položka 가닥에 작업 예약, Okno generovat | [화면.java](zdrojový_soubor/čeština/자바/화면.java) |
| `pracovní_prostor` | vstupní_bod `main` | Java zdrojový_soubor úprava_HODNOTA·Store_HODNOTA·kompilovat_zdroj·Provést_příkaz | [pracovní_prostor.java](zdrojový_soubor/čeština/자바/pracovní_prostor.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 datový_typ·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing tlačítko·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_úkol

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import čeština.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] argumenty) throws Exception {
        Path Adresář_HODNOTA = název_souboru.Create_Adresář(název_souboru.cesta_2("사용예자료"));
        Path 문서 = Adresář_HODNOTA.resolve("인사.txt");
        název_souboru.Zápis(문서, "한글 😀");
        String Obsah_HODNOTA = název_souboru.Čtení(문서);
        System.out.println(Obsah_HODNOTA);
        System.out.println(문자.bod_kódu_POČET(Obsah_HODNOTA)); // 한, text, 공백, 😀 → 4
        Thread práce_HODNOTA = 작업.Spustit_2("인사 작업", () -> System.out.println("작업 Provést_příkaz"));
        작업.기다리기(práce_HODNOTA);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 výchozí_hodnota `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Provést_příkaz 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 Třída_HODNOTA 폴더를 모두 그 값에 포함해야 한다.

hostit 저장소에서는 다음처럼 BLD_Systém·실행한다. hostit 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 pomocná_rutina_HODNOTA API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `název_souboru.Čtení(...)`처럼 호출한다. 표의 이름은 skutečný_data zdroj_strom 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 výjimka 외에도 잘못된 argumenty 등에 대한 표준 Java Provést_příkaz 시 예외가 발생할 číslo 있다.

### název_souboru: `čeština.자바.název_souboru`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| metoda_HODNOTA | návratový_typ | Akce·podmínka |
|---|---|---|
| `cesta_2(String Název)` | `Path` | 이름을 cesta_2 객체로 CONVERT_HODNOTA. skutečný_data 파일을 만들지는 않음 |
| `Čtení(Path cesta_2)` | `String` | název_souboru 전체를 UTF-8 텍스트로 읽음 |
| `Zápis(Path cesta_2, String Obsah_HODNOTA)` | `Path` | UTF-8 Store_HODNOTA. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path cesta_2)` | `byte[]` | název_souboru 전체를 bajt_HODNOTA 배열로 읽음 |
| `zápis_bajt_HODNOTA(Path cesta_2, byte[] Obsah_HODNOTA)` | `Path` | bajt_HODNOTA Store_HODNOTA. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `Create_Adresář(Path cesta_2)` | `Path` | 필요한 상위 폴더까지 generovat |
| `있는가(Path cesta_2)` | `boolean` | 존재 여부 ověřit. 확인할 číslo 없는 경우도 `false`práce_HODNOTA číslo 있음 |
| `vymazat_položka(Path cesta_2)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `položka_Seznam(Path cesta_2)` | `List<Path>` | 바로 아래 항목을 cesta_2 zarovnat_HODNOTA 순서로 Vratka_KV. 재귀 탐색은 아님 |

`cesta_2`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Zápis`와 `zápis_bajt_HODNOTA`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Kanál_HODNOTA API를 사용하는 방식으로 작성할 číslo 있다.

### 문자: `čeština.자바.문자`

| metoda_HODNOTA | návratový_typ | Akce·podmínka |
|---|---|---|
| `kódovat(String Obsah_HODNOTA)` | `byte[]` | 문자열을 UTF-8 바이트로 CONVERT_HODNOTA |
| `dešifrovat_data(byte[] Obsah_HODNOTA)` | `String` | UTF-8 바이트를 문자열로 CONVERT_HODNOTA. 잘못된 입력은 대체 문자로 Proces_HODNOTA_položka |
| `normalizovat_HODNOTA(String Obsah_HODNOTA)` | `String` | UNICODE_HODNOTA NFC normalizovat_HODNOTA. 예: složení_HODNOTA 자모 `ᄀ` + `ᅡ` → `가` |
| `bod_kódu_POČET(String Obsah_HODNOTA)` | `int` | UTF-16 KÓD_HODNOTA 단위가 아닌 UNICODE_HODNOTA KÓD_HODNOTA 포인트 číslo |
| `낱말(String Obsah_HODNOTA, Locale Jazyk)` | `List<String>` | Přiřadit_HODNOTA 언어의 `BreakIterator` 낱말 경계로 나눈 SMS_oblast |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Word_HODNOTA položka_Seznam API는 아니다. `normalizovat_HODNOTA`는 입력기나 převést_zdroj 기능이 아니다. KÓD_HODNOTA 포인트 číslo 역시 사람이 보는 znak_HODNOTA 수와 항상 같지는 않다. 여러 KÓD_HODNOTA 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### komunikace: `čeština.자바.komunikace`

| metoda_HODNOTA | návratový_typ | Akce·podmínka |
|---|---|---|
| `VZÍT_HODNOTA(URI Adresa, Duration časový_limit)` | `HttpResponse<String>` | HTTP(S) GET. Připojit 및 žádost časový_limit Nastavení. odezva 본문을 UTF-8로 parsovat_HODNOTA |
| `Connect_Endpoint(String Adresa, int hardware_port, int 제한밀리초)` | `Socket` | TCP Připojit 후 같은 값으로 Čtení 제한시간도 Nastavení |

`VZÍT_HODNOTA`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP chyba 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. dobrá_zboží 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`Connect_Endpoint`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Zápis 전체의 konečný_termín_HODNOTA 시간을 보장하는 옵션은 아니다.

```java
var odezva = komunikace.VZÍT_HODNOTA(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(odezva.statusCode());
System.out.println(odezva.body());
```

위 조각은 metoda_HODNOTA 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java výjimka 처리가 필요하다.

### 작업: `čeština.자바.작업`

| metoda_HODNOTA | návratový_typ | Akce·podmínka |
|---|---|---|
| `Spustit_2(String Název, Runnable Akce)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Spustit_2 |
| `기다리기(Thread vlákno_HODNOTA)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 Přiřadit_HODNOTA časová_hodnota 동안 `sleep()` |
| `Workbench_HODNOTA(int počet_vláken)` | `ExecutorService` | 고정 Velikost 작업 program_Launcher generovat. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 použít_HODNOTA 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Proces_HODNOTA_položka 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 číslo 있다.

### 화면: `čeština.자바.화면`

| metoda_HODNOTA | návratový_typ | Akce·podmínka |
|---|---|---|
| `나중에(Runnable Akce)` | `void` | Swing 이벤트 Proces_HODNOTA_položka 가닥에 실행을 예약하고 Vratka_KV |
| `Okno(String okno_Název, JComponent Obsah_HODNOTA, int 너비, int výška_HODNOTA)` | `JFrame` | Obsah_HODNOTA·크기를 지정한 창을 생성해 zobrazit_HODNOTA |

`Okno`을 Swing 이벤트 Proces_HODNOTA_položka vlákno_HODNOTA 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
화면.나중에(() -> 화면.Okno(
    "čeština 화면", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 číslo 있다. 창의 Zavřené 동작은 `DISPOSE_ON_CLOSE`다. `화면.나중에`가 반환됐다고 Okno 생성이 이미 끝난 것은 아니다.

### pracovní_prostor: úprava_HODNOTA·kompilovat_zdroj GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar čeština.자바.pracovní_prostor
```

`~/workspace`의 원문을 Otevřít·저장하고, `javac`로 컴파일해 `java`로 실행한다. Provést_příkaz název_souboru 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 název_souboru·문자 API 클래스가 아니다. 생성하는 Provést_příkaz název_souboru 방식은 [kompilátor 설명](../compiler/OpenJDK-spustitelný_soubor.md)을 따른다.

## 4. Python과 C++에서 사용할 číslo 있는가?

| metoda_MODE | dobrá_zboží deklarace Stav_HODNOTA | 호출 가능 oříznout |
|---|---|---|
| Java → čeština JAR | výchozí_hodnota deklarace | 위 22개 메서드와 pracovní_prostor |
| Python → `java` dítě_HODNOTA 프로세스 | Python·Java výchozí_hodnota deklarace | 작은 Java 진입점을 통해 호출하고 표준 výstupní_pozice·název_souboru 등으로 VÝSLEDEK Vpřed_HODNOTA |
| Python → JPype → JVM | JPype는 výchozí_hodnota 배포에 없음 | 별도 instalovat_HODNOTA 후 Java Třída_HODNOTA·metoda_HODNOTA 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 Připojit_položka ověřit_5fb2b747 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` deklarace | JVM을 생성하고 čeština Třída_HODNOTA·메서드를 직접 호출할 číslo 있음 |
| Python용 독립 čeština knihovna | dobrá_zboží výchozí_hodnota 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 čeština 모듈을 별도로 작성 |
| C/C++용 독립 čeština knihovna | vlastní x86 `posix-kor`와 vlastní ARM64 커널용 počáteční_stav RAM název_souboru 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SEKUNDA_operand `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SEKUNDA_operand 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Připojit 계층을 거쳐야 한다.

### Python: Připojit_položka 패키지 없이 호출

Provést_příkaz 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Hovory.py](예제/다른언어/PYTHON_Hovory.py)다. Python이 Java 진입점을 실행하고 `문자.bod_kódu_POČET`의 integer 결과를 받는다. argumenty 목록을 사용하며 prostředí příkaz 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Provést_příkaz·Konec_program KÓD_HODNOTA·výstupní_pozice Proces_HODNOTA_položka 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_HODNOTA 그 폴더에서 실행한다. 예제 název_souboru 자체는 výchozí_hodnota 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Hovory.py --text '한글 😀'
```

výstupní_pozice: `Python → čeština.자바.문자.bod_kódu_POČET: 4`

이 예제의 Python funkce_HODNOTA `bod_kódu_POČET`는 이번 문서의 Připojit 예제이며 기존에 설치된 Python 라이브러리는 아니다. dobrá_zboží 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objekt_HODNOTA 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 argumenty·VÝSLEDEK 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Další_zboží 형태로 연결할 číslo 있다. **아래는 výběr_HODNOTA 가능한 Připojit 방법이며, dobrá_zboží 배포판에 JPype가 설치돼 있거나 Provést_příkaz 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 Třída_HODNOTA 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("čeština.자바.문자")
    print(문자.bod_kódu_POČET(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Připojit 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype instalovat_HODNOTA·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 skutečný_data Provést_příkaz 가능한 예제다. JVM을 작업 스레드에서 생성하고 Další_zboží 메서드를 찾는다.

```cpp
jclass type = env->FindClass("čeština/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "bod_kódu_POČET", "(Ljava/lang/String;)I");
```

JVM generovat·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generovat·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_HODNOTA 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

výstupní_pozice: `C++ → čeština.자바.문자.bod_kódu_POČET: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI řetězec_HODNOTA formát_HODNOTA](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 čeština 메서드도 JNI 서명과 argumenty 자료형을 맞춰 호출할 číslo 있다. 예를 들어 `Path`를 받는 název_souboru API는 먼저 `název_souboru.cesta_2`로 Java cesta_2 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Proces_HODNOTA_položka vlákno_HODNOTA 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [vlastní ARM64 Připojit](../posix-kor/arm64-native/안내.md)은 C++에서 AOT Java 커널의 RAM název_souboru API를 직접 호출하며, 별도 EL0 uživatelský_prostor 라이브러리로 název_souboru/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 čeština Java JAR와는 다른 Provést_příkaz 기반이며 vlastní 커널은 별도 제한형 Java kompilátor/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java jádro_HODNOTA název_souboru·UDP 루프백·obdélník 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. vlastní 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/안내.md)에는 `otevřít_Soubor`, `파일자료읽기`, `zápis_Soubor_data`, `Zavřít_Soubor`, `Create_účastník`, `poslat_datagram_data` 등의 čeština C 별칭이 있다. 그러나 구현은 **vlastní jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 vlastní `sys/stat.h` 등의 헤더는 dobrá_zboží ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 čeština Třída_HODNOTA 라이브러리나 Python용 바인딩을 výchozí_hodnota 제공하는 상태도 아니다. dobrá_zboží Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 implementace·빌드해야 한다.

## 5. ověřit 범위와 재현

패키지 deklarace 여부는 [distribuce_HODNOTA 패키지 položka_Seznam](../platforms/rpi4/dist/packages.lock.json) 및 BLD_Systém 루트의 skutečný_data 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 výchozí_hodnota distribuce_HODNOTA 목록과 다를 číslo 있다.

이번에 **hostit x86_64/OpenJDK 11에서** Python dítě_HODNOTA 프로세스 호출과 C++ JNI 직접 호출을 kompilovat_zdroj·실행해 각각 VÝSLEDEK 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Připojit 예제는 Připojit_položka 패키지를 설치하지 않는다.

문서의 Java použít_HODNOTA 예제도 kompilovat_zdroj·실행했고, 22개 메서드의 문서 deklarace 여부와 로컬 문서 링크를 확인했다. [예제 ověřit_5fb2b747 LOGZ_ZÁZNAM](build/다른언어/ověření_Zpráva.json)

기존 ARM64 QEMU에서는 Java의 název_souboru·UNICODE_HODNOTA·스레드·HTTP 및 Swing zkoušky 결과가 있다. 이번 Python/C++ Připojit 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Provést_příkaz 중인 uživatelský_prostor 환경은 이 문서 작업에서 변경하지 않았다. [기존 operační_systém ověřit_5fb2b747 LOGZ_ZÁZNAM](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Hovory.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

hostit C++ 예제는 위 JNI kompilovat_zdroj 명령의 JDK 경로를 **hostit JDK cesta_2**로 바꾸고, zdrojový_soubor `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·knihovna 경로를 hostit x86_64 링크 명령에 섞지 않는다.
