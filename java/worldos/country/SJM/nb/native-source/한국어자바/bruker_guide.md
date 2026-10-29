# jkoros norsk bibliotek bruker_guide

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 eget x86 kjerne_VERDI 및 `eldre_kilde/`의 관리 kjerne_VERDI 모형과 구분한다.

## 1. betalt_vare 제공하는 bibliotek

패키지는 `norsk.자바`, operativsystem 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **hjelper_VERDI time_VERDI 5개, 공개 statisk_VERDI metode_VERDI 22개, 별도 GUI 프로그램인 arbeidsområde 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 betalt_vare ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| time_VERDI | metode_VERDI nummer | 기능 | KILDE |
|---|---:|---|---|
| `Fil` | 9 | UTF-8 텍스트·byte_VERDI Fil, katalog_VERDI, oppføring_Liste | [Fil.java](KILDE/norsk/자바/Fil.java) |
| `문자` | 5 | UTF-8 KONVERTER_VERDI, NFC normalisere_VERDI, KODE_VERDI 포인트, streng_VERDI grense_VERDI | [문자.java](KILDE/norsk/자바/문자.java) |
| `통신` | 2 | HTTP(S) GET, TCP Koble_til | [통신.java](KILDE/norsk/자바/통신.java) |
| `작업` | 4 | 스레드 Utfør_kommando·vent_VERDI, 고정 Størrelse 작업 app_appskuff | [작업.java](KILDE/norsk/자바/작업.java) |
| `skjermbilde` | 2 | Swing 이벤트 Prosess_VERDI_oppføring 가닥에 작업 예약, Vindu generere | [skjermbilde.java](KILDE/norsk/자바/skjermbilde.java) |
| `arbeidsområde` | inngangspunkt `main` | Java KILDE Rediger_VERDI·Store_VERDI·kompilere_kilde·Utfør_kommando | [arbeidsområde.java](KILDE/norsk/자바/arbeidsområde.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 datatype·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing Knapp·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_oppgave

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import norsk.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] Argumenter) throws Exception {
        Path katalog_VERDI = Fil.åpne_katalog(Fil.Sti("사용예자료"));
        Path 문서 = katalog_VERDI.resolve("인사.txt");
        Fil.Skriv(문서, "한글 😀");
        String Innhold_VERDI = Fil.Les(문서);
        System.out.println(Innhold_VERDI);
        System.out.println(문자.tegnkode_ANTALL(Innhold_VERDI)); // 한, Tekst, 공백, 😀 → 4
        Thread Arbeid_VERDI = 작업.Kjør_2("인사 작업", () -> System.out.println("작업 Utfør_kommando"));
        작업.기다리기(Arbeid_VERDI);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 standardverdi `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Utfør_kommando 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 time_VERDI 폴더를 모두 그 값에 포함해야 한다.

vert 저장소에서는 다음처럼 bygg_System·실행한다. vert 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 hjelper_VERDI API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `Fil.Les(...)`처럼 호출한다. 표의 이름은 faktisk_data kilde_tre 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 unntak 외에도 잘못된 Argumenter 등에 대한 표준 Java Utfør_kommando 시 예외가 발생할 nummer 있다.

### Fil: `norsk.자바.Fil`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| metode_VERDI | return_Type | Handling·vilkår |
|---|---|---|
| `Sti(String Navn)` | `Path` | 이름을 Sti 객체로 KONVERTER_VERDI. faktisk_data 파일을 만들지는 않음 |
| `Les(Path Sti)` | `String` | Fil 전체를 UTF-8 텍스트로 읽음 |
| `Skriv(Path Sti, String Innhold_VERDI)` | `Path` | UTF-8 Store_VERDI. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path Sti)` | `byte[]` | Fil 전체를 byte_VERDI 배열로 읽음 |
| `skrive_byte_VERDI(Path Sti, byte[] Innhold_VERDI)` | `Path` | byte_VERDI Store_VERDI. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `åpne_katalog(Path Sti)` | `Path` | 필요한 상위 폴더까지 generere |
| `있는가(Path Sti)` | `boolean` | 존재 여부 bekrefte. 확인할 nummer 없는 경우도 `false`Arbeid_VERDI nummer 있음 |
| `slette_oppføring(Path Sti)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `oppføring_Liste(Path Sti)` | `List<Path>` | 바로 아래 항목을 Sti justere_VERDI 순서로 return_KR. 재귀 탐색은 아님 |

`Sti`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Skriv`와 `skrive_byte_VERDI`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Kanal_VERDI API를 사용하는 방식으로 작성할 nummer 있다.

### 문자: `norsk.자바.문자`

| metode_VERDI | return_Type | Handling·vilkår |
|---|---|---|
| `부호화(String Innhold_VERDI)` | `byte[]` | 문자열을 UTF-8 바이트로 KONVERTER_VERDI |
| `dekryptere_data(byte[] Innhold_VERDI)` | `String` | UTF-8 바이트를 문자열로 KONVERTER_VERDI. 잘못된 입력은 대체 문자로 Prosess_VERDI_oppføring |
| `normalisere_VERDI(String Innhold_VERDI)` | `String` | UNICODE_VERDI NFC normalisere_VERDI. 예: sammensetning_VERDI 자모 `ᄀ` + `ᅡ` → `가` |
| `tegnkode_ANTALL(String Innhold_VERDI)` | `int` | UTF-16 KODE_VERDI 단위가 아닌 UNICODE_VERDI KODE_VERDI 포인트 nummer |
| `낱말(String Innhold_VERDI, Locale Språk)` | `List<String>` | overdra_VERDI 언어의 `BreakIterator` 낱말 경계로 나눈 SMS_område |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 ord_VERDI oppføring_Liste API는 아니다. `normalisere_VERDI`는 입력기나 OVERSETT_kilde 기능이 아니다. KODE_VERDI 포인트 nummer 역시 사람이 보는 tegn_VERDI 수와 항상 같지는 않다. 여러 KODE_VERDI 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### 통신: `norsk.자바.통신`

| metode_VERDI | return_Type | Handling·vilkår |
|---|---|---|
| `TA_VERDI(URI e_post, Duration tidsgrense)` | `HttpResponse<String>` | HTTP(S) GET. Koble_til 및 forespørsel tidsgrense Innstillinger. svar 본문을 UTF-8로 dele_opp_VERDI |
| `KOBLE_TIL_deltaker(String e_post, int maskinvare_port, int 제한밀리초)` | `Socket` | TCP Koble_til 후 같은 값으로 Les 제한시간도 Innstillinger |

`TA_VERDI`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP feil 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. betalt_vare 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`KOBLE_TIL_deltaker`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Skriv 전체의 tidsfrist_VERDI 시간을 보장하는 옵션은 아니다.

```java
var svar = 통신.TA_VERDI(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(svar.statusCode());
System.out.println(svar.body());
```

위 조각은 metode_VERDI 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java unntak 처리가 필요하다.

### 작업: `norsk.자바.작업`

| metode_VERDI | return_Type | Handling·vilkår |
|---|---|---|
| `Kjør_2(String Navn, Runnable Handling)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Kjør_2 |
| `기다리기(Thread tråd_VERDI)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 overdra_VERDI TID_VERDI 동안 `sleep()` |
| `Workbench_VERDI(int Trådteller)` | `ExecutorService` | 고정 Størrelse 작업 app_appskuff generere. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 bruk_VERDI 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Prosess_VERDI_oppføring 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 nummer 있다.

### skjermbilde: `norsk.자바.skjermbilde`

| metode_VERDI | return_Type | Handling·vilkår |
|---|---|---|
| `나중에(Runnable Handling)` | `void` | Swing 이벤트 Prosess_VERDI_oppføring 가닥에 실행을 예약하고 return_KR |
| `Vindu(String vindu_Tittel, JComponent Innhold_VERDI, int 너비, int 높이)` | `JFrame` | Innhold_VERDI·크기를 지정한 창을 생성해 vise_VERDI_487749b8 |

`Vindu`을 Swing 이벤트 Prosess_VERDI_oppføring tråd_VERDI 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
skjermbilde.나중에(() -> skjermbilde.Vindu(
    "norsk skjermbilde", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 nummer 있다. 창의 Lukk 동작은 `DISPOSE_ON_CLOSE`다. `skjermbilde.나중에`가 반환됐다고 Vindu 생성이 이미 끝난 것은 아니다.

### arbeidsområde: Rediger_VERDI·kompilere_kilde GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar norsk.자바.arbeidsområde
```

`~/workspace`의 원문을 Åpne·저장하고, `javac`로 컴파일해 `java`로 실행한다. Utfør_kommando Fil 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Fil·문자 API 클래스가 아니다. 생성하는 Utfør_kommando Fil 방식은 [kompilator 설명](../compiler/OpenJDK-kjørbar_fil.md)을 따른다.

## 4. Python과 C++에서 사용할 nummer 있는가?

| metode_MODUS | betalt_vare 포함 status_VERDI | 호출 가능 klippe |
|---|---|---|
| Java → norsk JAR | standardverdi 포함 | 위 22개 메서드와 arbeidsområde |
| Python → `java` barn_VERDI 프로세스 | Python·Java standardverdi 포함 | 작은 Java 진입점을 통해 호출하고 표준 Utgang·Fil 등으로 KR Frem_VERDI |
| Python → JPype → JVM | JPype는 standardverdi 배포에 없음 | 별도 installer_VERDI 후 Java time_VERDI·metode_VERDI 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 Tilføye_oppføring bekrefte_5fb2b747 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` 포함 | JVM을 생성하고 norsk time_VERDI·메서드를 직접 호출할 nummer 있음 |
| Python용 독립 norsk bibliotek | betalt_vare standardverdi 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 norsk 모듈을 별도로 작성 |
| C/C++용 독립 norsk bibliotek | eget x86 `posix-kor`와 eget ARM64 커널용 opprinnelig_tilstand RAM Fil 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SEKUND_operand `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SEKUND_operand 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Koble_til 계층을 거쳐야 한다.

### Python: Tilføye_oppføring 패키지 없이 호출

Utfør_kommando 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Anrop.py](예제/다른언어/PYTHON_Anrop.py)다. Python이 Java 진입점을 실행하고 `문자.tegnkode_ANTALL`의 heltall 결과를 받는다. Argumenter 목록을 사용하며 Shell Kommando 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Utfør_kommando·Utgang_app KODE_VERDI·Utgang Prosess_VERDI_oppføring 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 TILBAKE_VERDI 그 폴더에서 실행한다. 예제 Fil 자체는 standardverdi 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Anrop.py --text '한글 😀'
```

Utgang: `Python → norsk.자바.문자.tegnkode_ANTALL: 4`

이 예제의 Python FUNKSJON_VERDI `tegnkode_ANTALL`는 이번 문서의 Koble_til 예제이며 기존에 설치된 Python 라이브러리는 아니다. betalt_vare 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objekt_VERDI 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 Argumenter·KR 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Neste_vare 형태로 연결할 nummer 있다. **아래는 merket_område_VERDI 가능한 Koble_til 방법이며, betalt_vare 배포판에 JPype가 설치돼 있거나 Utfør_kommando 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 time_VERDI 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("norsk.자바.문자")
    print(문자.tegnkode_ANTALL(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Koble_til 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype installer_VERDI·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 faktisk_data Utfør_kommando 가능한 예제다. JVM을 작업 스레드에서 생성하고 Neste_vare 메서드를 찾는다.

```cpp
jclass type = env->FindClass("norsk/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "tegnkode_ANTALL", "(Ljava/lang/String;)I");
```

JVM generere·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generere·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 TILBAKE_VERDI 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

Utgang: `C++ → norsk.자바.문자.tegnkode_ANTALL: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI streng_VERDI format_VERDI](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 norsk 메서드도 JNI 서명과 Argumenter 자료형을 맞춰 호출할 nummer 있다. 예를 들어 `Path`를 받는 Fil API는 먼저 `Fil.Sti`로 Java Sti 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Prosess_VERDI_oppføring tråd_VERDI 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [eget ARM64 Koble_til](../posix-kor/arm64-native/Viktig_fil_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM Fil API를 직접 호출하며, 별도 EL0 bruker 라이브러리로 Fil/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 norsk Java JAR와는 다른 Utfør_kommando 기반이며 eget 커널은 별도 제한형 Java kompilator/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java kjerne_VERDI Fil·UDP 루프백·rektangel 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. eget 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/Viktig_fil_eb81d7d9.md)에는 `åpen_Fil`, `파일자료읽기`, `skrive_Fil_data`, `Lukk_Fil`, `åpne_deltaker`, `sende_datagram_data` 등의 norsk C 별칭이 있다. 그러나 구현은 **eget jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 eget `sys/stat.h` 등의 헤더는 betalt_vare ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 norsk time_VERDI 라이브러리나 Python용 바인딩을 standardverdi 제공하는 상태도 아니다. betalt_vare Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 구현·빌드해야 한다.

## 5. bekrefte 범위와 재현

패키지 포함 여부는 [distribusjon_VERDI 패키지 oppføring_Liste](../platforms/rpi4/dist/packages.lock.json) 및 bygg_System 루트의 faktisk_data 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 standardverdi distribusjon_VERDI 목록과 다를 nummer 있다.

이번에 **vert x86_64/OpenJDK 11에서** Python barn_VERDI 프로세스 호출과 C++ JNI 직접 호출을 kompilere_kilde·실행해 각각 KR 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Koble_til 예제는 Tilføye_oppføring 패키지를 설치하지 않는다.

문서의 Java bruk_VERDI 예제도 kompilere_kilde·실행했고, 22개 메서드의 문서 포함 여부와 로컬 문서 링크를 확인했다. [예제 bekrefte_5fb2b747 LOG_POST](build/다른언어/validering_rapport.json)

기존 ARM64 QEMU에서는 Java의 Fil·UNICODE_VERDI·스레드·HTTP 및 Swing 시험 결과가 있다. 이번 Python/C++ Koble_til 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Utfør_kommando 중인 bruker 환경은 이 문서 작업에서 변경하지 않았다. [기존 operativsystem bekrefte_5fb2b747 LOG_POST](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Anrop.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

vert C++ 예제는 위 JNI kompilere_kilde 명령의 JDK 경로를 **vert JDK Sti**로 바꾸고, KILDE `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·bibliotek 경로를 vert x86_64 링크 명령에 섞지 않는다.
