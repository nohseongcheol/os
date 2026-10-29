# jkoros Nederlands bibliotheek gebruiker_guide

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 Eigen x86 kernel_WAARDE 및 `verouderd_bron/`의 관리 kernel_WAARDE 모형과 구분한다.

## 1. actueel_item 제공하는 bibliotheek

패키지는 `Nederlands.자바`, besturingssysteem 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **helper_WAARDE les_WAARDE 5개, 공개 statisch_WAARDE methode_WAARDE 22개, 별도 GUI 프로그램인 werkgebied 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 actueel_item ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| les_WAARDE | methode_WAARDE nummer | 기능 | broncode |
|---|---:|---|---|
| `bestand` | 9 | UTF-8 텍스트·byte_WAARDE bestand, map_WAARDE, invoer_Lijst_f07b3200 | [bestand.java](broncode/Nederlands/자바/bestand.java) |
| `문자` | 5 | UTF-8 CONVERTEREN_WAARDE, NFC normaliseren_WAARDE, CODE_WAARDE 포인트, tekenreeks_WAARDE grens_WAARDE | [문자.java](broncode/Nederlands/자바/문자.java) |
| `communicatie` | 2 | HTTP(S) GET, TCP Verbinden | [communicatie.java](broncode/Nederlands/자바/communicatie.java) |
| `작업` | 4 | 스레드 Uitvoeren_opdracht·wachten_WAARDE, 고정 Grootte 작업 app_app_lade | [작업.java](broncode/Nederlands/자바/작업.java) |
| `scherm` | 2 | Swing 이벤트 Proces_WAARDE_invoer 가닥에 작업 예약, Venster genereren | [scherm.java](broncode/Nederlands/자바/scherm.java) |
| `werkgebied` | beginpunt `main` | Java broncode Bewerk_WAARDE·Store_WAARDE·compileren_bron·Uitvoeren_opdracht | [werkgebied.java](broncode/Nederlands/자바/werkgebied.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 gegevenstype·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing knop·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_taak

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import Nederlands.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] argumenten) throws Exception {
        Path map_WAARDE = bestand.maken_map(bestand.pad("사용예자료"));
        Path Guides = map_WAARDE.resolve("인사.txt");
        bestand.Schrijven(Guides, "한글 😀");
        String Inhoud_WAARDE = bestand.Lezen(Guides);
        System.out.println(Inhoud_WAARDE);
        System.out.println(문자.codepoint_AANTAL(Inhoud_WAARDE)); // 한, tekst, 공백, 😀 → 4
        Thread Werk_WAARDE = 작업.starten("인사 작업", () -> System.out.println("작업 Uitvoeren_opdracht"));
        작업.기다리기(Werk_WAARDE);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 standaardwaarde `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Uitvoeren_opdracht 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 les_WAARDE 폴더를 모두 그 값에 포함해야 한다.

host 저장소에서는 다음처럼 bouwen·실행한다. host 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 helper_WAARDE API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `bestand.Lezen(...)`처럼 호출한다. 표의 이름은 werkelijk_gegevens bron_structuur 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 uitzondering 외에도 잘못된 argumenten 등에 대한 표준 Java Uitvoeren_opdracht 시 예외가 발생할 nummer 있다.

### bestand: `Nederlands.자바.bestand`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| methode_WAARDE | Retour_TYPE | Actie·toestand |
|---|---|---|
| `pad(String Naam)` | `Path` | 이름을 pad 객체로 CONVERTEREN_WAARDE. werkelijk_gegevens 파일을 만들지는 않음 |
| `Lezen(Path pad)` | `String` | bestand 전체를 UTF-8 텍스트로 읽음 |
| `Schrijven(Path pad, String Inhoud_WAARDE)` | `Path` | UTF-8 Store_WAARDE. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path pad)` | `byte[]` | bestand 전체를 byte_WAARDE 배열로 읽음 |
| `schrijven_byte_WAARDE(Path pad, byte[] Inhoud_WAARDE)` | `Path` | byte_WAARDE Store_WAARDE. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `maken_map(Path pad)` | `Path` | 필요한 상위 폴더까지 genereren |
| `있는가(Path pad)` | `boolean` | 존재 여부 bevestigen. 확인할 nummer 없는 경우도 `false`Werk_WAARDE nummer 있음 |
| `wissen_invoer(Path pad)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `invoer_Lijst_f07b3200(Path pad)` | `List<Path>` | 바로 아래 항목을 pad uitlijnen_WAARDE 순서로 Retour_HR. 재귀 탐색은 아님 |

`pad`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Schrijven`와 `schrijven_byte_WAARDE`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Kanaal_WAARDE API를 사용하는 방식으로 작성할 nummer 있다.

### 문자: `Nederlands.자바.문자`

| methode_WAARDE | Retour_TYPE | Actie·toestand |
|---|---|---|
| `coderen(String Inhoud_WAARDE)` | `byte[]` | 문자열을 UTF-8 바이트로 CONVERTEREN_WAARDE |
| `ontsleutelen_gegevens(byte[] Inhoud_WAARDE)` | `String` | UTF-8 바이트를 문자열로 CONVERTEREN_WAARDE. 잘못된 입력은 대체 문자로 Proces_WAARDE_invoer |
| `normaliseren_WAARDE(String Inhoud_WAARDE)` | `String` | UNICODE_WAARDE NFC normaliseren_WAARDE. 예: samenstelling_WAARDE 자모 `ᄀ` + `ᅡ` → `가` |
| `codepoint_AANTAL(String Inhoud_WAARDE)` | `int` | UTF-16 CODE_WAARDE 단위가 아닌 UNICODE_WAARDE CODE_WAARDE 포인트 nummer |
| `낱말(String Inhoud_WAARDE, Locale Taal)` | `List<String>` | Toewijzen_WAARDE 언어의 `BreakIterator` 낱말 경계로 나눈 sms_bereik |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Word_WAARDE invoer_Lijst_f07b3200 API는 아니다. `normaliseren_WAARDE`는 입력기나 VERTALEN_bron 기능이 아니다. CODE_WAARDE 포인트 nummer 역시 사람이 보는 teken_WAARDE 수와 항상 같지는 않다. 여러 CODE_WAARDE 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### communicatie: `Nederlands.자바.communicatie`

| methode_WAARDE | Retour_TYPE | Actie·toestand |
|---|---|---|
| `NEMEN_WAARDE(URI ADRES, Duration tijdslimiet)` | `HttpResponse<String>` | HTTP(S) GET. Verbinden 및 aanvraag tijdslimiet Instellingen. reactie 본문을 UTF-8로 parseren_WAARDE |
| `Connect_Endpoint(String ADRES, int hardware_poort, int 제한밀리초)` | `Socket` | TCP Verbinden 후 같은 값으로 Lezen 제한시간도 Instellingen |

`NEMEN_WAARDE`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP fout 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. actueel_item 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`Connect_Endpoint`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Schrijven 전체의 deadline_WAARDE 시간을 보장하는 옵션은 아니다.

```java
var reactie = communicatie.NEMEN_WAARDE(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(reactie.statusCode());
System.out.println(reactie.body());
```

위 조각은 methode_WAARDE 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java uitzondering 처리가 필요하다.

### 작업: `Nederlands.자바.작업`

| methode_WAARDE | Retour_TYPE | Actie·toestand |
|---|---|---|
| `starten(String Naam, Runnable Actie)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 starten |
| `기다리기(Thread thread_WAARDE)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 Toewijzen_WAARDE TIJD_WAARDE 동안 `sleep()` |
| `Workbench_WAARDE(int aantal_threads)` | `ExecutorService` | 고정 Grootte 작업 app_app_lade genereren. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 gebruik_WAARDE 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Proces_WAARDE_invoer 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 nummer 있다.

### scherm: `Nederlands.자바.scherm`

| methode_WAARDE | Retour_TYPE | Actie·toestand |
|---|---|---|
| `나중에(Runnable Actie)` | `void` | Swing 이벤트 Proces_WAARDE_invoer 가닥에 실행을 예약하고 Retour_HR |
| `Venster(String venster_Titel, JComponent Inhoud_WAARDE, int 너비, int hoogte_WAARDE)` | `JFrame` | Inhoud_WAARDE·크기를 지정한 창을 생성해 weergeven_WAARDE |

`Venster`을 Swing 이벤트 Proces_WAARDE_invoer thread_WAARDE 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
scherm.나중에(() -> scherm.Venster(
    "Nederlands scherm", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 nummer 있다. 창의 Sluiten 동작은 `DISPOSE_ON_CLOSE`다. `scherm.나중에`가 반환됐다고 Venster 생성이 이미 끝난 것은 아니다.

### werkgebied: Bewerk_WAARDE·compileren_bron GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar Nederlands.자바.werkgebied
```

`~/workspace`의 원문을 Openen·저장하고, `javac`로 컴파일해 `java`로 실행한다. Uitvoeren_opdracht bestand 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 bestand·문자 API 클래스가 아니다. 생성하는 Uitvoeren_opdracht bestand 방식은 [compiler 설명](../compiler/OpenJDK-uitvoerbaar_bestand.md)을 따른다.

## 4. Python과 C++에서 사용할 nummer 있는가?

| methode_MODUS | actueel_item declaraties Status_WAARDE | 호출 가능 clip |
|---|---|---|
| Java → Nederlands JAR | standaardwaarde declaraties | 위 22개 메서드와 werkgebied |
| Python → `java` kind_WAARDE 프로세스 | Python·Java standaardwaarde declaraties | 작은 Java 진입점을 통해 호출하고 표준 tekstuitvoer·bestand 등으로 resultaat Vooruit_WAARDE |
| Python → JPype → JVM | JPype는 standaardwaarde 배포에 없음 | 별도 installeren_WAARDE 후 Java les_WAARDE·methode_WAARDE 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 toevoegen_invoer valideren 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` declaraties | JVM을 생성하고 Nederlands les_WAARDE·메서드를 직접 호출할 nummer 있음 |
| Python용 독립 Nederlands bibliotheek | actueel_item standaardwaarde 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 Nederlands 모듈을 별도로 작성 |
| C/C++용 독립 Nederlands bibliotheek | Eigen x86 `posix-kor`와 Eigen ARM64 커널용 begintoestand RAM bestand 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SECONDE_operand `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SECONDE_operand 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Verbinden 계층을 거쳐야 한다.

### Python: toevoegen_invoer 패키지 없이 호출

Uitvoeren_opdracht 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Oproepen.py](예제/다른언어/PYTHON_Oproepen.py)다. Python이 Java 진입점을 실행하고 `문자.codepoint_AANTAL`의 geheel_getal 결과를 받는다. argumenten 목록을 사용하며 Shell opdracht 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Uitvoeren_opdracht·Einde_app CODE_WAARDE·tekstuitvoer Proces_WAARDE_invoer 방식은 [Python 공식 Guides](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_WAARDE 그 폴더에서 실행한다. 예제 bestand 자체는 standaardwaarde 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Oproepen.py --text '한글 😀'
```

tekstuitvoer: `Python → Nederlands.자바.문자.codepoint_AANTAL: 4`

이 예제의 Python FUNCTIE_WAARDE `codepoint_AANTAL`는 이번 문서의 Verbinden 예제이며 기존에 설치된 Python 라이브러리는 아니다. actueel_item 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java object_WAARDE 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 argumenten·resultaat 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Volgende_item 형태로 연결할 nummer 있다. **아래는 selectie_WAARDE 가능한 Verbinden 방법이며, actueel_item 배포판에 JPype가 설치돼 있거나 Uitvoeren_opdracht 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 les_WAARDE 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("Nederlands.자바.문자")
    print(문자.codepoint_AANTAL(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Verbinden 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype installeren_WAARDE·패키지 빌드는 이번 Guides 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 werkelijk_gegevens Uitvoeren_opdracht 가능한 예제다. JVM을 작업 스레드에서 생성하고 Volgende_item 메서드를 찾는다.

```cpp
jclass type = env->FindClass("Nederlands/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "codepoint_AANTAL", "(Ljava/lang/String;)I");
```

JVM genereren·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 genereren·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_WAARDE 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

tekstuitvoer: `C++ → Nederlands.자바.문자.codepoint_AANTAL: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI tekenreeks_WAARDE opmaak_WAARDE](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 Nederlands 메서드도 JNI 서명과 argumenten 자료형을 맞춰 호출할 nummer 있다. 예를 들어 `Path`를 받는 bestand API는 먼저 `bestand.pad`로 Java pad 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Proces_WAARDE_invoer thread_WAARDE 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [Eigen ARM64 Verbinden](../posix-kor/arm64-native/LEESMIJ_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM bestand API를 직접 호출하며, 별도 EL0 gebruikersruimte 라이브러리로 bestand/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 Nederlands Java JAR와는 다른 Uitvoeren_opdracht 기반이며 Eigen 커널은 별도 제한형 Java compiler/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java kernel_WAARDE bestand·UDP 루프백·rechthoek 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. Eigen 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/LEESMIJ_eb81d7d9.md)에는 `open_Bestand`, `파일자료읽기`, `schrijven_Bestand_gegevens`, `Sluiten_Bestand`, `maken_eindpunt`, `e_mailen_datagram_gegevens` 등의 Nederlands C 별칭이 있다. 그러나 구현은 **Eigen jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 Eigen `sys/stat.h` 등의 헤더는 actueel_item ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 Nederlands les_WAARDE 라이브러리나 Python용 바인딩을 standaardwaarde 제공하는 상태도 아니다. actueel_item Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 implementatie·빌드해야 한다.

## 5. bevestigen 범위와 재현

패키지 declaraties 여부는 [distributie_WAARDE 패키지 invoer_Lijst_f07b3200](../platforms/rpi4/dist/packages.lock.json) 및 bouwen 루트의 werkelijk_gegevens 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 standaardwaarde distributie_WAARDE 목록과 다를 nummer 있다.

이번에 **host x86_64/OpenJDK 11에서** Python kind_WAARDE 프로세스 호출과 C++ JNI 직접 호출을 compileren_bron·실행해 각각 resultaat 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Verbinden 예제는 toevoegen_invoer 패키지를 설치하지 않는다.

문서의 Java gebruik_WAARDE 예제도 compileren_bron·실행했고, 22개 메서드의 Guides declaraties 여부와 로컬 Guides 링크를 확인했다. [예제 valideren LOG_RECORD](build/다른언어/validatie_Rapport.json)

기존 ARM64 QEMU에서는 Java의 bestand·UNICODE_WAARDE·스레드·HTTP 및 Swing tests 결과가 있다. 이번 Python/C++ Verbinden 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Uitvoeren_opdracht 중인 gebruikersruimte 환경은 이 Guides 작업에서 변경하지 않았다. [기존 besturingssysteem valideren LOG_RECORD](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Oproepen.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

host C++ 예제는 위 JNI compileren_bron 명령의 JDK 경로를 **host JDK pad**로 바꾸고, broncode `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·bibliotheek 경로를 host x86_64 링크 명령에 섞지 않는다.
