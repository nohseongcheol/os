# jkoros Dansk bibliotek bruger_guide

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 eget x86 kerne_VÆRDI 및 `nedarvet_kilde/`의 관리 kerne_VÆRDI 모형과 구분한다.

## 1. aktuel_vare 제공하는 bibliotek

패키지는 `Dansk.자바`, operativsystem 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **hjælper_VÆRDI Hold_VÆRDI 5개, 공개 statisk_VÆRDI metode_VÆRDI 22개, 별도 GUI 프로그램인 arbejdsområde 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 aktuel_vare ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| Hold_VÆRDI | metode_VÆRDI tal | 기능 | KILDE |
|---|---:|---|---|
| `Fil` | 9 | UTF-8 텍스트·byte_VÆRDI Fil, mappe_VÆRDI, post_Liste | [Fil.java](KILDE/Dansk/자바/Fil.java) |
| `문자` | 5 | UTF-8 KONVERTER_VÆRDI, NFC normalisere_VÆRDI, KODE_VÆRDI 포인트, streng_VÆRDI grænse_VÆRDI | [문자.java](KILDE/Dansk/자바/문자.java) |
| `통신` | 2 | HTTP(S) GET, TCP Tilslut | [통신.java](KILDE/Dansk/자바/통신.java) |
| `작업` | 4 | 스레드 Udfør_kommando·vent_VÆRDI, 고정 Størrelse 작업 app_Kvikstart | [작업.java](KILDE/Dansk/자바/작업.java) |
| `skærmbillede` | 2 | Swing 이벤트 Proces_VÆRDI_post 가닥에 작업 예약, Vindue generere | [skærmbillede.java](KILDE/Dansk/자바/skærmbillede.java) |
| `arbejdsområde` | indgangspunkt `main` | Java KILDE Rediger_VÆRDI·Store_VÆRDI·kompilere_kilde·Udfør_kommando | [arbejdsområde.java](KILDE/Dansk/자바/arbejdsområde.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 datatype·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing knap·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_job

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import Dansk.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] Argumenter) throws Exception {
        Path mappe_VÆRDI = Fil.åbne_mappe(Fil.Sti("사용예자료"));
        Path 문서 = mappe_VÆRDI.resolve("인사.txt");
        Fil.Skrive(문서, "한글 😀");
        String Indhold_VÆRDI = Fil.Læse(문서);
        System.out.println(Indhold_VÆRDI);
        System.out.println(문자.tegnkode_TÆL(Indhold_VÆRDI)); // 한, Tekst, 공백, 😀 → 4
        Thread Arbejde_VÆRDI = 작업.Kør_2("인사 작업", () -> System.out.println("작업 Udfør_kommando"));
        작업.기다리기(Arbejde_VÆRDI);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 standardværdi `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Udfør_kommando 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 Hold_VÆRDI 폴더를 모두 그 값에 포함해야 한다.

vært 저장소에서는 다음처럼 build_System·실행한다. vært 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 hjælper_VÆRDI API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `Fil.Læse(...)`처럼 호출한다. 표의 이름은 faktisk_data kilde_træ 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 undtagelse 외에도 잘못된 Argumenter 등에 대한 표준 Java Udfør_kommando 시 예외가 발생할 tal 있다.

### Fil: `Dansk.자바.Fil`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| metode_VÆRDI | returnere_Type | Handling·lidelse |
|---|---|---|
| `Sti(String Navn)` | `Path` | 이름을 Sti 객체로 KONVERTER_VÆRDI. faktisk_data 파일을 만들지는 않음 |
| `Læse(Path Sti)` | `String` | Fil 전체를 UTF-8 텍스트로 읽음 |
| `Skrive(Path Sti, String Indhold_VÆRDI)` | `Path` | UTF-8 Store_VÆRDI. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path Sti)` | `byte[]` | Fil 전체를 byte_VÆRDI 배열로 읽음 |
| `skrive_byte_VÆRDI(Path Sti, byte[] Indhold_VÆRDI)` | `Path` | byte_VÆRDI Store_VÆRDI. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `åbne_mappe(Path Sti)` | `Path` | 필요한 상위 폴더까지 generere |
| `있는가(Path Sti)` | `boolean` | 존재 여부 bekræfte. 확인할 tal 없는 경우도 `false`Arbejde_VÆRDI tal 있음 |
| `slette_post(Path Sti)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `post_Liste(Path Sti)` | `List<Path>` | 바로 아래 항목을 Sti justere_VÆRDI 순서로 returnere_KR. 재귀 탐색은 아님 |

`Sti`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Skrive`와 `skrive_byte_VÆRDI`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Kanal_VÆRDI API를 사용하는 방식으로 작성할 tal 있다.

### 문자: `Dansk.자바.문자`

| metode_VÆRDI | returnere_Type | Handling·lidelse |
|---|---|---|
| `kode(String Indhold_VÆRDI)` | `byte[]` | 문자열을 UTF-8 바이트로 KONVERTER_VÆRDI |
| `dekryptere_data(byte[] Indhold_VÆRDI)` | `String` | UTF-8 바이트를 문자열로 KONVERTER_VÆRDI. 잘못된 입력은 대체 문자로 Proces_VÆRDI_post |
| `normalisere_VÆRDI(String Indhold_VÆRDI)` | `String` | UNICODE_VÆRDI NFC normalisere_VÆRDI. 예: komposition_VÆRDI 자모 `ᄀ` + `ᅡ` → `가` |
| `tegnkode_TÆL(String Indhold_VÆRDI)` | `int` | UTF-16 KODE_VÆRDI 단위가 아닌 UNICODE_VÆRDI KODE_VÆRDI 포인트 tal |
| `낱말(String Indhold_VÆRDI, Locale Sprog)` | `List<String>` | Tildel_VÆRDI 언어의 `BreakIterator` 낱말 경계로 나눈 sms_område |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Ord_VÆRDI post_Liste API는 아니다. `normalisere_VÆRDI`는 입력기나 OVERSÆT_kilde 기능이 아니다. KODE_VÆRDI 포인트 tal 역시 사람이 보는 tegn_VÆRDI 수와 항상 같지는 않다. 여러 KODE_VÆRDI 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### 통신: `Dansk.자바.통신`

| metode_VÆRDI | returnere_Type | Handling·lidelse |
|---|---|---|
| `TAG_VÆRDI(URI mail, Duration tidsbegrænsning)` | `HttpResponse<String>` | HTTP(S) GET. Tilslut 및 anmodning tidsbegrænsning Indstillinger. svar 본문을 UTF-8로 opdele_tekst_VÆRDI |
| `Forbind_slutpunkt(String mail, int hardware_port, int 제한밀리초)` | `Socket` | TCP Tilslut 후 같은 값으로 Læse 제한시간도 Indstillinger |

`TAG_VÆRDI`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP fejl 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. aktuel_vare 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`Forbind_slutpunkt`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Skrive 전체의 deadline_VÆRDI 시간을 보장하는 옵션은 아니다.

```java
var svar = 통신.TAG_VÆRDI(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(svar.statusCode());
System.out.println(svar.body());
```

위 조각은 metode_VÆRDI 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java undtagelse 처리가 필요하다.

### 작업: `Dansk.자바.작업`

| metode_VÆRDI | returnere_Type | Handling·lidelse |
|---|---|---|
| `Kør_2(String Navn, Runnable Handling)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Kør_2 |
| `기다리기(Thread tråd_VÆRDI)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 Tildel_VÆRDI TID_VÆRDI 동안 `sleep()` |
| `Workbench_VÆRDI(int Antal_tråde)` | `ExecutorService` | 고정 Størrelse 작업 app_Kvikstart generere. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 brug_VÆRDI 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Proces_VÆRDI_post 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 tal 있다.

### skærmbillede: `Dansk.자바.skærmbillede`

| metode_VÆRDI | returnere_Type | Handling·lidelse |
|---|---|---|
| `나중에(Runnable Handling)` | `void` | Swing 이벤트 Proces_VÆRDI_post 가닥에 실행을 예약하고 returnere_KR |
| `Vindue(String vindue_Titel, JComponent Indhold_VÆRDI, int 너비, int 높이)` | `JFrame` | Indhold_VÆRDI·크기를 지정한 창을 생성해 vise_VÆRDI |

`Vindue`을 Swing 이벤트 Proces_VÆRDI_post tråd_VÆRDI 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
skærmbillede.나중에(() -> skærmbillede.Vindue(
    "Dansk skærmbillede", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 tal 있다. 창의 Luk 동작은 `DISPOSE_ON_CLOSE`다. `skærmbillede.나중에`가 반환됐다고 Vindue 생성이 이미 끝난 것은 아니다.

### arbejdsområde: Rediger_VÆRDI·kompilere_kilde GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar Dansk.자바.arbejdsområde
```

`~/workspace`의 원문을 Åbn·저장하고, `javac`로 컴파일해 `java`로 실행한다. Udfør_kommando Fil 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Fil·문자 API 클래스가 아니다. 생성하는 Udfør_kommando Fil 방식은 [compiler 설명](../compiler/OpenJDK-eksekverbar_fil.md)을 따른다.

## 4. Python과 C++에서 사용할 tal 있는가?

| metode_HYPPIGST | aktuel_vare 포함 status_VÆRDI | 호출 가능 klippe |
|---|---|---|
| Java → Dansk JAR | standardværdi 포함 | 위 22개 메서드와 arbejdsområde |
| Python → `java` barn_VÆRDI 프로세스 | Python·Java standardværdi 포함 | 작은 Java 진입점을 통해 호출하고 표준 Udgang·Fil 등으로 KR Frem_VÆRDI |
| Python → JPype → JVM | JPype는 standardværdi 배포에 없음 | 별도 installér_VÆRDI 후 Java Hold_VÆRDI·metode_VÆRDI 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 tilføj_post bekræfte_5fb2b747 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` 포함 | JVM을 생성하고 Dansk Hold_VÆRDI·메서드를 직접 호출할 tal 있음 |
| Python용 독립 Dansk bibliotek | aktuel_vare standardværdi 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 Dansk 모듈을 별도로 작성 |
| C/C++용 독립 Dansk bibliotek | eget x86 `posix-kor`와 eget ARM64 커널용 starttilstand RAM Fil 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SEKUND_operand `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SEKUND_operand 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Tilslut 계층을 거쳐야 한다.

### Python: tilføj_post 패키지 없이 호출

Udfør_kommando 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Opkald.py](예제/다른언어/PYTHON_Opkald.py)다. Python이 Java 진입점을 실행하고 `문자.tegnkode_TÆL`의 heltal 결과를 받는다. Argumenter 목록을 사용하며 Shell Kommando 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Udfør_kommando·Afslut_app KODE_VÆRDI·Udgang Proces_VÆRDI_post 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_VÆRDI 그 폴더에서 실행한다. 예제 Fil 자체는 standardværdi 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Opkald.py --text '한글 😀'
```

Udgang: `Python → Dansk.자바.문자.tegnkode_TÆL: 4`

이 예제의 Python FUNKTION_VÆRDI `tegnkode_TÆL`는 이번 문서의 Tilslut 예제이며 기존에 설치된 Python 라이브러리는 아니다. aktuel_vare 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objekt_VÆRDI 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 Argumenter·KR 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Næste_vare 형태로 연결할 tal 있다. **아래는 markering_VÆRDI 가능한 Tilslut 방법이며, aktuel_vare 배포판에 JPype가 설치돼 있거나 Udfør_kommando 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 Hold_VÆRDI 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("Dansk.자바.문자")
    print(문자.tegnkode_TÆL(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Tilslut 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype installér_VÆRDI·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 faktisk_data Udfør_kommando 가능한 예제다. JVM을 작업 스레드에서 생성하고 Næste_vare 메서드를 찾는다.

```cpp
jclass type = env->FindClass("Dansk/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "tegnkode_TÆL", "(Ljava/lang/String;)I");
```

JVM generere·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generere·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_VÆRDI 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

Udgang: `C++ → Dansk.자바.문자.tegnkode_TÆL: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI streng_VÆRDI format_VÆRDI](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 Dansk 메서드도 JNI 서명과 Argumenter 자료형을 맞춰 호출할 tal 있다. 예를 들어 `Path`를 받는 Fil API는 먼저 `Fil.Sti`로 Java Sti 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Proces_VÆRDI_post tråd_VÆRDI 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [eget ARM64 Tilslut](../posix-kor/arm64-native/Vigtigt_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM Fil API를 직접 호출하며, 별도 EL0 bruger 라이브러리로 Fil/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 Dansk Java JAR와는 다른 Udfør_kommando 기반이며 eget 커널은 별도 제한형 Java compiler/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java kerne_VÆRDI Fil·UDP 루프백·rektangel 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. eget 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/Vigtigt_eb81d7d9.md)에는 `åben_fil`, `파일자료읽기`, `skrive_fil_data`, `Luk_fil`, `åbne_slutpunkt`, `maile_datagram_data` 등의 Dansk C 별칭이 있다. 그러나 구현은 **eget jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 eget `sys/stat.h` 등의 헤더는 aktuel_vare ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 Dansk Hold_VÆRDI 라이브러리나 Python용 바인딩을 standardværdi 제공하는 상태도 아니다. aktuel_vare Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 구현·빌드해야 한다.

## 5. bekræfte 범위와 재현

패키지 포함 여부는 [distribution_VÆRDI 패키지 post_Liste](../platforms/rpi4/dist/packages.lock.json) 및 build_System 루트의 faktisk_data 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 standardværdi distribution_VÆRDI 목록과 다를 tal 있다.

이번에 **vært x86_64/OpenJDK 11에서** Python barn_VÆRDI 프로세스 호출과 C++ JNI 직접 호출을 kompilere_kilde·실행해 각각 KR 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Tilslut 예제는 tilføj_post 패키지를 설치하지 않는다.

문서의 Java brug_VÆRDI 예제도 kompilere_kilde·실행했고, 22개 메서드의 문서 포함 여부와 로컬 문서 링크를 확인했다. [예제 bekræfte_5fb2b747 LOG_post](build/다른언어/validering_rapport.json)

기존 ARM64 QEMU에서는 Java의 Fil·UNICODE_VÆRDI·스레드·HTTP 및 Swing 시험 결과가 있다. 이번 Python/C++ Tilslut 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Udfør_kommando 중인 bruger 환경은 이 문서 작업에서 변경하지 않았다. [기존 operativsystem bekræfte_5fb2b747 LOG_post](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Opkald.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

vært C++ 예제는 위 JNI kompilere_kilde 명령의 JDK 경로를 **vært JDK Sti**로 바꾸고, KILDE `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·bibliotek 경로를 vært x86_64 링크 명령에 섞지 않는다.
