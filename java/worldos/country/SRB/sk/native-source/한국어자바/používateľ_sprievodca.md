# jkoros Slovenský knižnica používateľ_sprievodca

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 vlastné x86 jadro_VALUE 및 `starší_zdroj/`의 관리 jadro_VALUE 모형과 구분한다.

## 1. v_termíne_splatnosti_položka 제공하는 knižnica

패키지는 `Slovenský.자바`, operačný_systém 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **도우미 lekcia_VALUE 5개, 공개 정적 metóda_VALUE 22개, 별도 GUI 프로그램인 pracovný_priestor 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 v_termíne_splatnosti_položka ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| lekcia_VALUE | metóda_VALUE 수 | 기능 | ZDROJ |
|---|---:|---|---|
| `Súbor` | 9 | UTF-8 텍스트·Byte_VALUE Súbor, Adresár_VALUE, položka_Zoznam | [Súbor.java](ZDROJ/Slovenský/자바/Súbor.java) |
| `문자` | 5 | UTF-8 CONVERT_VALUE, NFC normalizovať_VALUE, kód_VALUE 포인트, reťazec_VALUE 경계 | [문자.java](ZDROJ/Slovenský/자바/문자.java) |
| `통신` | 2 | HTTP(S) GET, TCP Pripojiť | [통신.java](ZDROJ/Slovenský/자바/통신.java) |
| `작업` | 4 | 스레드 Vykonať_príkaz·počkaj_VALUE, 고정 Veľkosť 작업 program_spúšťač | [작업.java](ZDROJ/Slovenský/자바/작업.java) |
| `화면` | 2 | Swing 이벤트 Proces_VALUE_položka 가닥에 작업 예약, Okno generovať | [화면.java](ZDROJ/Slovenský/자바/화면.java) |
| `pracovný_priestor` | položka_bod `main` | Java ZDROJ úprava_VALUE·Store_VALUE·kompilovať_zdroj·Vykonať_príkaz | [pracovný_priestor.java](ZDROJ/Slovenský/자바/pracovný_priestor.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 typ_údajov·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing Tlačidlo·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_úloha

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import Slovenský.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] Argumenty) throws Exception {
        Path Adresár_VALUE = Súbor.Create_Adresár(Súbor.Cesta("사용예자료"));
        Path 문서 = Adresár_VALUE.resolve("인사.txt");
        Súbor.Zápis(문서, "한글 😀");
        String obsah_VALUE = Súbor.Čítanie(문서);
        System.out.println(obsah_VALUE);
        System.out.println(문자.bod_kódu_COUNT(obsah_VALUE)); // 한, Spracovanie_textu, 공백, 😀 → 4
        Thread Práca_VALUE = 작업.Spustiť_2("인사 작업", () -> System.out.println("작업 Vykonať_príkaz"));
        작업.기다리기(Práca_VALUE);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 predvolená_hodnota `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Vykonať_príkaz 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 lekcia_VALUE 폴더를 모두 그 값에 포함해야 한다.

hostiteľ 저장소에서는 다음처럼 zostava_systém·실행한다. hostiteľ 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 도우미 API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `Súbor.Čítanie(...)`처럼 호출한다. 표의 이름은 skutočný_údaje zdroj_strom 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 výnimka 외에도 잘못된 Argumenty 등에 대한 표준 Java Vykonať_príkaz 시 예외가 발생할 수 있다.

### Súbor: `Slovenský.자바.Súbor`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| metóda_VALUE | vrátiť_Typ | Akcia·podmienka |
|---|---|---|
| `Cesta(String Názov)` | `Path` | 이름을 Cesta 객체로 CONVERT_VALUE. skutočný_údaje 파일을 만들지는 않음 |
| `Čítanie(Path Cesta)` | `String` | Súbor 전체를 UTF-8 텍스트로 읽음 |
| `Zápis(Path Cesta, String obsah_VALUE)` | `Path` | UTF-8 Store_VALUE. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path Cesta)` | `byte[]` | Súbor 전체를 Byte_VALUE 배열로 읽음 |
| `zapísať_Byte_VALUE(Path Cesta, byte[] obsah_VALUE)` | `Path` | Byte_VALUE Store_VALUE. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `Create_Adresár(Path Cesta)` | `Path` | 필요한 상위 폴더까지 generovať |
| `있는가(Path Cesta)` | `boolean` | 존재 여부 overiť. 확인할 수 없는 경우도 `false`Práca_VALUE 수 있음 |
| `vymazať_položka(Path Cesta)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `položka_Zoznam(Path Cesta)` | `List<Path>` | 바로 아래 항목을 Cesta zarovnať_VALUE 순서로 vrátiť_KR. 재귀 탐색은 아님 |

`Cesta`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Zápis`와 `zapísať_Byte_VALUE`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Kanál_VALUE API를 사용하는 방식으로 작성할 수 있다.

### 문자: `Slovenský.자바.문자`

| metóda_VALUE | vrátiť_Typ | Akcia·podmienka |
|---|---|---|
| `kódovať(String obsah_VALUE)` | `byte[]` | 문자열을 UTF-8 바이트로 CONVERT_VALUE |
| `dešifrovať_údaje(byte[] obsah_VALUE)` | `String` | UTF-8 바이트를 문자열로 CONVERT_VALUE. 잘못된 입력은 대체 문자로 Proces_VALUE_položka |
| `normalizovať_VALUE(String obsah_VALUE)` | `String` | UNICODE_VALUE NFC normalizovať_VALUE. 예: 조합 자모 `ᄀ` + `ᅡ` → `가` |
| `bod_kódu_COUNT(String obsah_VALUE)` | `int` | UTF-16 kód_VALUE 단위가 아닌 UNICODE_VALUE kód_VALUE 포인트 수 |
| `낱말(String obsah_VALUE, Locale Jazyky)` | `List<String>` | Priradiť_VALUE 언어의 `BreakIterator` 낱말 경계로 나눈 SMS_rozsah |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Word_VALUE položka_Zoznam API는 아니다. `normalizovať_VALUE`는 입력기나 Preložiť_zdroj 기능이 아니다. kód_VALUE 포인트 수 역시 사람이 보는 znak_VALUE 수와 항상 같지는 않다. 여러 kód_VALUE 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### 통신: `Slovenský.자바.통신`

| metóda_VALUE | vrátiť_Typ | Akcia·podmienka |
|---|---|---|
| `TAKE_VALUE(URI adresa, Duration časový_limit)` | `HttpResponse<String>` | HTTP(S) GET. Pripojiť 및 požiadavka časový_limit Nastavenia. odozva 본문을 UTF-8로 analyzovať_VALUE |
| `spojiť_účastník(String adresa, int hardvér_port, int 제한밀리초)` | `Socket` | TCP Pripojiť 후 같은 값으로 Čítanie 제한시간도 Nastavenia |

`TAKE_VALUE`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP chyba 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. v_termíne_splatnosti_položka 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`spojiť_účastník`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Zápis 전체의 termín_VALUE 시간을 보장하는 옵션은 아니다.

```java
var odozva = 통신.TAKE_VALUE(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(odozva.statusCode());
System.out.println(odozva.body());
```

위 조각은 metóda_VALUE 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java výnimka 처리가 필요하다.

### 작업: `Slovenský.자바.작업`

| metóda_VALUE | vrátiť_Typ | Akcia·podmienka |
|---|---|---|
| `Spustiť_2(String Názov, Runnable Akcia)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Spustiť_2 |
| `기다리기(Thread vlákno_VALUE)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 Priradiť_VALUE čas_VALUE 동안 `sleep()` |
| `작업대(int počet_vlákien)` | `ExecutorService` | 고정 Veľkosť 작업 program_spúšťač generovať. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 používať_VALUE 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Proces_VALUE_položka 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 수 있다.

### 화면: `Slovenský.자바.화면`

| metóda_VALUE | vrátiť_Typ | Akcia·podmienka |
|---|---|---|
| `나중에(Runnable Akcia)` | `void` | Swing 이벤트 Proces_VALUE_položka 가닥에 실행을 예약하고 vrátiť_KR |
| `Okno(String okno_Názov, JComponent obsah_VALUE, int 너비, int výška_VALUE)` | `JFrame` | obsah_VALUE·크기를 지정한 창을 생성해 zobraziť_VALUE_487749b8 |

`Okno`을 Swing 이벤트 Proces_VALUE_položka vlákno_VALUE 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
화면.나중에(() -> 화면.Okno(
    "Slovenský 화면", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 수 있다. 창의 Zatvoriť 동작은 `DISPOSE_ON_CLOSE`다. `화면.나중에`가 반환됐다고 Okno 생성이 이미 끝난 것은 아니다.

### pracovný_priestor: úprava_VALUE·kompilovať_zdroj GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar Slovenský.자바.pracovný_priestor
```

`~/workspace`의 원문을 Otvoriť·저장하고, `javac`로 컴파일해 `java`로 실행한다. Vykonať_príkaz Súbor 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Súbor·문자 API 클래스가 아니다. 생성하는 Vykonať_príkaz Súbor 방식은 [kompilátor 설명](../compiler/OpenJDK-spustiteľný_súbor.md)을 따른다.

## 4. Python과 C++에서 사용할 수 있는가?

| metóda_MODE | v_termíne_splatnosti_položka 포함 Stav_VALUE | 호출 가능 klip |
|---|---|---|
| Java → Slovenský JAR | predvolená_hodnota 포함 | 위 22개 메서드와 pracovný_priestor |
| Python → `java` dieťa_VALUE 프로세스 | Python·Java predvolená_hodnota 포함 | 작은 Java 진입점을 통해 호출하고 표준 Výstup·Súbor 등으로 KR Dopredu_VALUE |
| Python → JPype → JVM | JPype는 predvolená_hodnota 배포에 없음 | 별도 inštalovať_VALUE 후 Java lekcia_VALUE·metóda_VALUE 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 Pripojiť_položka overiť_5fb2b747 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` 포함 | JVM을 생성하고 Slovenský lekcia_VALUE·메서드를 직접 호출할 수 있음 |
| Python용 독립 Slovenský knižnica | v_termíne_splatnosti_položka predvolená_hodnota 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 Slovenský 모듈을 별도로 작성 |
| C/C++용 독립 Slovenský knižnica | vlastné x86 `posix-kor`와 vlastné ARM64 커널용 počiatočný_stav RAM Súbor 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SECOND_operand `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SECOND_operand 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Pripojiť 계층을 거쳐야 한다.

### Python: Pripojiť_položka 패키지 없이 호출

Vykonať_príkaz 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Hovory.py](예제/다른언어/PYTHON_Hovory.py)다. Python이 Java 진입점을 실행하고 `문자.bod_kódu_COUNT`의 celé_číslo 결과를 받는다. Argumenty 목록을 사용하며 셸 Príkaz 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Vykonať_príkaz·Skončiť_program kód_VALUE·Výstup Proces_VALUE_položka 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_VALUE 그 폴더에서 실행한다. 예제 Súbor 자체는 predvolená_hodnota 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Hovory.py --text '한글 😀'
```

Výstup: `Python → Slovenský.자바.문자.bod_kódu_COUNT: 4`

이 예제의 Python funkcia_VALUE `bod_kódu_COUNT`는 이번 문서의 Pripojiť 예제이며 기존에 설치된 Python 라이브러리는 아니다. v_termíne_splatnosti_položka 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objekt_VALUE 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 Argumenty·KR 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Ďalej_položka 형태로 연결할 수 있다. **아래는 výber_VALUE 가능한 Pripojiť 방법이며, v_termíne_splatnosti_položka 배포판에 JPype가 설치돼 있거나 Vykonať_príkaz 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 lekcia_VALUE 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("Slovenský.자바.문자")
    print(문자.bod_kódu_COUNT(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Pripojiť 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype inštalovať_VALUE·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 skutočný_údaje Vykonať_príkaz 가능한 예제다. JVM을 작업 스레드에서 생성하고 Ďalej_položka 메서드를 찾는다.

```cpp
jclass type = env->FindClass("Slovenský/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "bod_kódu_COUNT", "(Ljava/lang/String;)I");
```

JVM generovať·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generovať·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_VALUE 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

Výstup: `C++ → Slovenský.자바.문자.bod_kódu_COUNT: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI reťazec_VALUE formát_VALUE](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 Slovenský 메서드도 JNI 서명과 Argumenty 자료형을 맞춰 호출할 수 있다. 예를 들어 `Path`를 받는 Súbor API는 먼저 `Súbor.Cesta`로 Java Cesta 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Proces_VALUE_položka vlákno_VALUE 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [vlastné ARM64 Pripojiť](../posix-kor/arm64-native/안내.md)은 C++에서 AOT Java 커널의 RAM Súbor API를 직접 호출하며, 별도 EL0 používateľ 라이브러리로 Súbor/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 Slovenský Java JAR와는 다른 Vykonať_príkaz 기반이며 vlastné 커널은 별도 제한형 Java kompilátor/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java jadro_VALUE Súbor·UDP 루프백·obdĺžnik 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. vlastné 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/안내.md)에는 `otvoriť_Súbor`, `파일자료읽기`, `zapísať_Súbor_údaje`, `Zavrieť_Súbor`, `Create_účastník`, `odoslať_datagram_údaje` 등의 Slovenský C 별칭이 있다. 그러나 구현은 **vlastné jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 vlastné `sys/stat.h` 등의 헤더는 v_termíne_splatnosti_položka ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 Slovenský lekcia_VALUE 라이브러리나 Python용 바인딩을 predvolená_hodnota 제공하는 상태도 아니다. v_termíne_splatnosti_položka Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 구현·빌드해야 한다.

## 5. overiť 범위와 재현

패키지 포함 여부는 [배포 패키지 položka_Zoznam](../platforms/rpi4/dist/packages.lock.json) 및 zostava_systém 루트의 skutočný_údaje 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 predvolená_hodnota 배포 목록과 다를 수 있다.

이번에 **hostiteľ x86_64/OpenJDK 11에서** Python dieťa_VALUE 프로세스 호출과 C++ JNI 직접 호출을 kompilovať_zdroj·실행해 각각 KR 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Pripojiť 예제는 Pripojiť_položka 패키지를 설치하지 않는다.

문서의 Java používať_VALUE 예제도 kompilovať_zdroj·실행했고, 22개 메서드의 문서 포함 여부와 로컬 문서 링크를 확인했다. [예제 overiť_5fb2b747 LOG_RECORD](build/다른언어/overenie_správa.json)

기존 ARM64 QEMU에서는 Java의 Súbor·UNICODE_VALUE·스레드·HTTP 및 Swing 시험 결과가 있다. 이번 Python/C++ Pripojiť 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Vykonať_príkaz 중인 používateľ 환경은 이 문서 작업에서 변경하지 않았다. [기존 operačný_systém overiť_5fb2b747 LOG_RECORD](../platforms/rpi4/VERIFICATION.md)

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

hostiteľ C++ 예제는 위 JNI kompilovať_zdroj 명령의 JDK 경로를 **hostiteľ JDK Cesta**로 바꾸고, ZDROJ `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·knižnica 경로를 hostiteľ x86_64 링크 명령에 섞지 않는다.
