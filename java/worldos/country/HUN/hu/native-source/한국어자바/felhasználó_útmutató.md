# jkoros magyar kódtár felhasználó_útmutató

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 saját x86 kernel_ÉRTÉK 및 `örökség_forrás/`의 관리 kernel_ÉRTÉK 모형과 구분한다.

## 1. aktuális_cikk 제공하는 kódtár

패키지는 `magyar.자바`, operációs_rendszer 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **segéd_ÉRTÉK tanóra_ÉRTÉK 5개, 공개 statikus_ÉRTÉK metódus_ÉRTÉK 22개, 별도 GUI 프로그램인 munkaterület 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 aktuális_cikk ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| tanóra_ÉRTÉK | metódus_ÉRTÉK szám | 기능 | FORRÁS |
|---|---:|---|---|
| `Fájl` | 9 | UTF-8 텍스트·bájt_ÉRTÉK Fájl, címtár_ÉRTÉK, bejegyzés_Lista | [Fájl.java](FORRÁS/magyar/자바/Fájl.java) |
| `문자` | 5 | UTF-8 konvertál_ÉRTÉK, NFC normalizál_ÉRTÉK, KÓD_ÉRTÉK 포인트, sztring_ÉRTÉK határ_ÉRTÉK | [문자.java](FORRÁS/magyar/자바/문자.java) |
| `kommunikáció` | 2 | HTTP(S) GET, TCP Kapcsolódás | [kommunikáció.java](FORRÁS/magyar/자바/kommunikáció.java) |
| `작업` | 4 | 스레드 végrehajt_parancs·várj_ÉRTÉK, 고정 Méret 작업 app_indító | [작업.java](FORRÁS/magyar/자바/작업.java) |
| `화면` | 2 | Swing 이벤트 folyamat_ÉRTÉK_bejegyzés 가닥에 작업 예약, Ablak generálás | [화면.java](FORRÁS/magyar/자바/화면.java) |
| `munkaterület` | belépési_pont `main` | Java FORRÁS szerkeszt_ÉRTÉK·tár_ÉRTÉK·épít_forrás·végrehajt_parancs | [munkaterület.java](FORRÁS/magyar/자바/munkaterület.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 adattípus·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing gomb·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_teendő

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import magyar.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] Argumentumok) throws Exception {
        Path címtár_ÉRTÉK = Fájl.készít_címtár(Fájl.ÚTVONAL("사용예자료"));
        Path 문서 = címtár_ÉRTÉK.resolve("인사.txt");
        Fájl.Írás(문서, "한글 😀");
        String Tartalom_ÉRTÉK = Fájl.Olvasás(문서);
        System.out.println(Tartalom_ÉRTÉK);
        System.out.println(문자.kódpont_DARAB(Tartalom_ÉRTÉK)); // 한, Szöveg, 공백, 😀 → 4
        Thread munka_ÉRTÉK = 작업.Futtatás("인사 작업", () -> System.out.println("작업 végrehajt_parancs"));
        작업.기다리기(munka_ÉRTÉK);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 alapértelmezett_érték `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 végrehajt_parancs 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 tanóra_ÉRTÉK 폴더를 모두 그 값에 포함해야 한다.

gazda 저장소에서는 다음처럼 épít_Rendszer·실행한다. gazda 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 segéd_ÉRTÉK API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `Fájl.Olvasás(...)`처럼 호출한다. 표의 이름은 tényleges_adat forrás_fa 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 kivétel 외에도 잘못된 Argumentumok 등에 대한 표준 Java végrehajt_parancs 시 예외가 발생할 szám 있다.

### Fájl: `magyar.자바.Fájl`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| metódus_ÉRTÉK | visszaküld_beír | Művelet·állapot |
|---|---|---|
| `ÚTVONAL(String Név)` | `Path` | 이름을 ÚTVONAL 객체로 konvertál_ÉRTÉK. tényleges_adat 파일을 만들지는 않음 |
| `Olvasás(Path ÚTVONAL)` | `String` | Fájl 전체를 UTF-8 텍스트로 읽음 |
| `Írás(Path ÚTVONAL, String Tartalom_ÉRTÉK)` | `Path` | UTF-8 tár_ÉRTÉK. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path ÚTVONAL)` | `byte[]` | Fájl 전체를 bájt_ÉRTÉK 배열로 읽음 |
| `ír_bájt_ÉRTÉK(Path ÚTVONAL, byte[] Tartalom_ÉRTÉK)` | `Path` | bájt_ÉRTÉK tár_ÉRTÉK. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `készít_címtár(Path ÚTVONAL)` | `Path` | 필요한 상위 폴더까지 generálás |
| `있는가(Path ÚTVONAL)` | `boolean` | 존재 여부 igazol. 확인할 szám 없는 경우도 `false`munka_ÉRTÉK szám 있음 |
| `töröl_bejegyzés(Path ÚTVONAL)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `bejegyzés_Lista(Path ÚTVONAL)` | `List<Path>` | 바로 아래 항목을 ÚTVONAL igazít_ÉRTÉK 순서로 visszaküld_KR. 재귀 탐색은 아님 |

`ÚTVONAL`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Írás`와 `ír_bájt_ÉRTÉK`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Csatorna_ÉRTÉK API를 사용하는 방식으로 작성할 szám 있다.

### 문자: `magyar.자바.문자`

| metódus_ÉRTÉK | visszaküld_beír | Művelet·állapot |
|---|---|---|
| `kódolás(String Tartalom_ÉRTÉK)` | `byte[]` | 문자열을 UTF-8 바이트로 konvertál_ÉRTÉK |
| `visszafejt_adat(byte[] Tartalom_ÉRTÉK)` | `String` | UTF-8 바이트를 문자열로 konvertál_ÉRTÉK. 잘못된 입력은 대체 문자로 folyamat_ÉRTÉK_bejegyzés |
| `normalizál_ÉRTÉK(String Tartalom_ÉRTÉK)` | `String` | UNICODE_ÉRTÉK NFC normalizál_ÉRTÉK. 예: rész_egész_ÉRTÉK 자모 `ᄀ` + `ᅡ` → `가` |
| `kódpont_DARAB(String Tartalom_ÉRTÉK)` | `int` | UTF-16 KÓD_ÉRTÉK 단위가 아닌 UNICODE_ÉRTÉK KÓD_ÉRTÉK 포인트 szám |
| `낱말(String Tartalom_ÉRTÉK, Locale Nyelv)` | `List<String>` | átruház_ÉRTÉK 언어의 `BreakIterator` 낱말 경계로 나눈 SMS_tartomány |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 szó_ÉRTÉK bejegyzés_Lista API는 아니다. `normalizál_ÉRTÉK`는 입력기나 FORDÍTÁS_forrás 기능이 아니다. KÓD_ÉRTÉK 포인트 szám 역시 사람이 보는 karakter_ÉRTÉK 수와 항상 같지는 않다. 여러 KÓD_ÉRTÉK 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### kommunikáció: `magyar.자바.kommunikáció`

| metódus_ÉRTÉK | visszaküld_beír | Művelet·állapot |
|---|---|---|
| `ÁTHELYEZ_ÉRTÉK(URI CÍM, Duration időkorlát)` | `HttpResponse<String>` | HTTP(S) GET. Kapcsolódás 및 kérés időkorlát Beállítások. válasz 본문을 UTF-8로 elemez_ÉRTÉK |
| `Connect_Endpoint(String CÍM, int hardver_port, int 제한밀리초)` | `Socket` | TCP Kapcsolódás 후 같은 값으로 Olvasás 제한시간도 Beállítások |

`ÁTHELYEZ_ÉRTÉK`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP HIBA 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. aktuális_cikk 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`Connect_Endpoint`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Írás 전체의 határidő_ÉRTÉK 시간을 보장하는 옵션은 아니다.

```java
var válasz = kommunikáció.ÁTHELYEZ_ÉRTÉK(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(válasz.statusCode());
System.out.println(válasz.body());
```

위 조각은 metódus_ÉRTÉK 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java kivétel 처리가 필요하다.

### 작업: `magyar.자바.작업`

| metódus_ÉRTÉK | visszaküld_beír | Művelet·állapot |
|---|---|---|
| `Futtatás(String Név, Runnable Művelet)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Futtatás |
| `기다리기(Thread szál_ÉRTÉK)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 átruház_ÉRTÉK IDŐ_ÉRTÉK 동안 `sleep()` |
| `Workbench_ÉRTÉK(int szálak_száma)` | `ExecutorService` | 고정 Méret 작업 app_indító generálás. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 használ_ÉRTÉK 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 folyamat_ÉRTÉK_bejegyzés 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 szám 있다.

### 화면: `magyar.자바.화면`

| metódus_ÉRTÉK | visszaküld_beír | Művelet·állapot |
|---|---|---|
| `나중에(Runnable Művelet)` | `void` | Swing 이벤트 folyamat_ÉRTÉK_bejegyzés 가닥에 실행을 예약하고 visszaküld_KR |
| `Ablak(String ablak_Cím, JComponent Tartalom_ÉRTÉK, int 너비, int 높이)` | `JFrame` | Tartalom_ÉRTÉK·크기를 지정한 창을 생성해 bemutató_ÉRTÉK |

`Ablak`을 Swing 이벤트 folyamat_ÉRTÉK_bejegyzés szál_ÉRTÉK 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
화면.나중에(() -> 화면.Ablak(
    "magyar 화면", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 szám 있다. 창의 Bezárás 동작은 `DISPOSE_ON_CLOSE`다. `화면.나중에`가 반환됐다고 Ablak 생성이 이미 끝난 것은 아니다.

### munkaterület: szerkeszt_ÉRTÉK·épít_forrás GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar magyar.자바.munkaterület
```

`~/workspace`의 원문을 Megnyitás·저장하고, `javac`로 컴파일해 `java`로 실행한다. végrehajt_parancs Fájl 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Fájl·문자 API 클래스가 아니다. 생성하는 végrehajt_parancs Fájl 방식은 [fordítóprogram 설명](../compiler/OpenJDK-végrehajtható_Fájl.md)을 따른다.

## 4. Python과 C++에서 사용할 szám 있는가?

| metódus_mód | aktuális_cikk 포함 Állapot_ÉRTÉK | 호출 가능 klip |
|---|---|---|
| Java → magyar JAR | alapértelmezett_érték 포함 | 위 22개 메서드와 munkaterület |
| Python → `java` gyermek_ÉRTÉK 프로세스 | Python·Java alapértelmezett_érték 포함 | 작은 Java 진입점을 통해 호출하고 표준 Kimenet·Fájl 등으로 KR Előre_ÉRTÉK |
| Python → JPype → JVM | JPype는 alapértelmezett_érték 배포에 없음 | 별도 telepít_ÉRTÉK 후 Java tanóra_ÉRTÉK·metódus_ÉRTÉK 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 hozzáfűz_bejegyzés ellenőriz 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` 포함 | JVM을 생성하고 magyar tanóra_ÉRTÉK·메서드를 직접 호출할 szám 있음 |
| Python용 독립 magyar kódtár | aktuális_cikk alapértelmezett_érték 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 magyar 모듈을 별도로 작성 |
| C/C++용 독립 magyar kódtár | saját x86 `posix-kor`와 saját ARM64 커널용 kiinduló_állapot RAM Fájl 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`MPERC_operandus `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`MPERC_operandus 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Kapcsolódás 계층을 거쳐야 한다.

### Python: hozzáfűz_bejegyzés 패키지 없이 호출

végrehajt_parancs 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Hívások.py](예제/다른언어/PYTHON_Hívások.py)다. Python이 Java 진입점을 실행하고 `문자.kódpont_DARAB`의 egész_szám 결과를 받는다. Argumentumok 목록을 사용하며 felület Parancs 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 végrehajt_parancs·kilép_app KÓD_ÉRTÉK·Kimenet folyamat_ÉRTÉK_bejegyzés 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_ÉRTÉK 그 폴더에서 실행한다. 예제 Fájl 자체는 alapértelmezett_érték 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Hívások.py --text '한글 😀'
```

Kimenet: `Python → magyar.자바.문자.kódpont_DARAB: 4`

이 예제의 Python FÜGGVÉNY_ÉRTÉK `kódpont_DARAB`는 이번 문서의 Kapcsolódás 예제이며 기존에 설치된 Python 라이브러리는 아니다. aktuális_cikk 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objektum_ÉRTÉK 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 Argumentumok·KR 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Tovább_cikk 형태로 연결할 szám 있다. **아래는 kijelölés_ÉRTÉK 가능한 Kapcsolódás 방법이며, aktuális_cikk 배포판에 JPype가 설치돼 있거나 végrehajt_parancs 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 tanóra_ÉRTÉK 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("magyar.자바.문자")
    print(문자.kódpont_DARAB(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Kapcsolódás 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype telepít_ÉRTÉK·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 tényleges_adat végrehajt_parancs 가능한 예제다. JVM을 작업 스레드에서 생성하고 Tovább_cikk 메서드를 찾는다.

```cpp
jclass type = env->FindClass("magyar/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "kódpont_DARAB", "(Ljava/lang/String;)I");
```

JVM generálás·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generálás·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_ÉRTÉK 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

Kimenet: `C++ → magyar.자바.문자.kódpont_DARAB: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI sztring_ÉRTÉK formáz_ÉRTÉK](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 magyar 메서드도 JNI 서명과 Argumentumok 자료형을 맞춰 호출할 szám 있다. 예를 들어 `Path`를 받는 Fájl API는 먼저 `Fájl.ÚTVONAL`로 Java ÚTVONAL 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 folyamat_ÉRTÉK_bejegyzés szál_ÉRTÉK 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [saját ARM64 Kapcsolódás](../posix-kor/arm64-native/fontos_fájl_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM Fájl API를 직접 호출하며, 별도 EL0 felhasználó 라이브러리로 Fájl/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 magyar Java JAR와는 다른 végrehajt_parancs 기반이며 saját 커널은 별도 제한형 Java fordítóprogram/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java kernel_ÉRTÉK Fájl·UDP 루프백·téglalap 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. saját 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/fontos_fájl_eb81d7d9.md)에는 `készít_Fájl`, `파일자료읽기`, `ír_Fájl_adat`, `bezár_Fájl`, `készít_végpont`, `küld_datagram_adat` 등의 magyar C 별칭이 있다. 그러나 구현은 **saját jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 saját `sys/stat.h` 등의 헤더는 aktuális_cikk ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 magyar tanóra_ÉRTÉK 라이브러리나 Python용 바인딩을 alapértelmezett_érték 제공하는 상태도 아니다. aktuális_cikk Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 구현·빌드해야 한다.

## 5. igazol 범위와 재현

패키지 포함 여부는 [elosztás_ÉRTÉK 패키지 bejegyzés_Lista](../platforms/rpi4/dist/packages.lock.json) 및 épít_Rendszer 루트의 tényleges_adat 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 alapértelmezett_érték elosztás_ÉRTÉK 목록과 다를 szám 있다.

이번에 **gazda x86_64/OpenJDK 11에서** Python gyermek_ÉRTÉK 프로세스 호출과 C++ JNI 직접 호출을 épít_forrás·실행해 각각 KR 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Kapcsolódás 예제는 hozzáfűz_bejegyzés 패키지를 설치하지 않는다.

문서의 Java használ_ÉRTÉK 예제도 épít_forrás·실행했고, 22개 메서드의 문서 포함 여부와 로컬 문서 링크를 확인했다. [예제 ellenőriz LOG_REKORD](build/다른언어/ellenőrzés_jelent.json)

기존 ARM64 QEMU에서는 Java의 Fájl·UNICODE_ÉRTÉK·스레드·HTTP 및 Swing 시험 결과가 있다. 이번 Python/C++ Kapcsolódás 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 végrehajt_parancs 중인 felhasználó 환경은 이 문서 작업에서 변경하지 않았다. [기존 operációs_rendszer ellenőriz LOG_REKORD](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Hívások.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

gazda C++ 예제는 위 JNI épít_forrás 명령의 JDK 경로를 **gazda JDK ÚTVONAL**로 바꾸고, FORRÁS `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·kódtár 경로를 gazda x86_64 링크 명령에 섞지 않는다.
