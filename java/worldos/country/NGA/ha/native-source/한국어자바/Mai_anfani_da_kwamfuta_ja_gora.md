# jkoros 한국어 laburare Mai_anfani_da_kwamfuta_ja_gora

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 자체 x86 Kwara_Daraja 및 `Tsohon_Bayani_tushe/`의 관리 Kwara_Daraja 모형과 구분한다.

## 1. 현재 제공하는 laburare

패키지는 `한국어.자바`, OS 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **도우미 Aji_Daraja 5개, 공개 Tsaye_cik_Daraja tsari_Daraja 22개, 별도 GUI 프로그램인 sararin_aiki 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 현재 ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| Aji_Daraja | tsari_Daraja 수 | 기능 | tushe |
|---|---:|---|---|
| `Fayil` | 9 | UTF-8 텍스트·bayit_Daraja Fayil, ma_ajiya_Daraja, Mashigar_bayanai_Jeri | [Fayil.java](tushe/한국어/자바/Fayil.java) |
| `문자` | 5 | UTF-8 변환, NFC Gajarta_kimar_bayanai_Daraja, lambar_sirri_Daraja 포인트, Zare_Daraja 경계 | [문자.java](tushe/한국어/자바/문자.java) |
| `통신` | 2 | HTTP(S) GET, TCP Haɗi | [통신.java](tushe/한국어/자바/통신.java) |
| `작업` | 4 | 스레드 gudanar_Umarni·jira_Daraja, 고정 Girma 작업 Shiri_Mai_Fara_Ka_ida | [작업.java](tushe/한국어/자바/작업.java) |
| `화면` | 2 | Swing 이벤트 haryar_aikin_na_ura_Daraja_Mashigar_bayanai 가닥에 작업 예약, taga 생성 | [화면.java](tushe/한국어/자바/화면.java) |
| `sararin_aiki` | Mashigar_bayanai_maki `main` | Java tushe gyaran_Daraja·Ajiye_Daraja·Gina_tushe·gudanar_Umarni | [sararin_aiki.java](tushe/한국어/자바/sararin_aiki.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 Nau_in_tarin_bayani·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing maɓali·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 Fara_aiki

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import 한국어.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] 인수) throws Exception {
        Path ma_ajiya_Daraja = Fayil.ƙirƙíra_ma_ajiya(Fayil.Hanyar_shiga("사용예자료"));
        Path 문서 = ma_ajiya_Daraja.resolve("인사.txt");
        Fayil.Yi_Rubutu(문서, "한글 😀");
        String kunshiya_Daraja = Fayil.Yi_Karatu(문서);
        System.out.println(kunshiya_Daraja);
        System.out.println(문자.코드포인트수(kunshiya_Daraja)); // 한, SMS, 공백, 😀 → 4
        Thread 일 = 작업.Tafiyar_da("인사 작업", () -> System.out.println("작업 gudanar_Umarni"));
        작업.기다리기(일);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 Tanadaddiyar_daraja `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 gudanar_Umarni 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 Aji_Daraja 폴더를 모두 그 값에 포함해야 한다.

sauka 저장소에서는 다음처럼 Gina_na_ura·실행한다. sauka 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 도우미 API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `Fayil.Yi_Karatu(...)`처럼 호출한다. 표의 이름은 Na_hakika_Tarin_bayani tushe_Li_irabin_tarin_bayanai 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 banbanchi 외에도 잘못된 인수 등에 대한 표준 Java gudanar_Umarni 시 예외가 발생할 수 있다.

### Fayil: `한국어.자바.Fayil`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| tsari_Daraja | 반환형 | Aiki·Yanayi |
|---|---|---|
| `Hanyar_shiga(String Suna)` | `Path` | 이름을 Hanyar_shiga 객체로 변환. Na_hakika_Tarin_bayani 파일을 만들지는 않음 |
| `Yi_Karatu(Path Hanyar_shiga)` | `String` | Fayil 전체를 UTF-8 텍스트로 읽음 |
| `Yi_Rubutu(Path Hanyar_shiga, String kunshiya_Daraja)` | `Path` | UTF-8 Ajiye_Daraja. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path Hanyar_shiga)` | `byte[]` | Fayil 전체를 bayit_Daraja 배열로 읽음 |
| `Rubuta_bayit_Daraja(Path Hanyar_shiga, byte[] kunshiya_Daraja)` | `Path` | bayit_Daraja Ajiye_Daraja. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `ƙirƙíra_ma_ajiya(Path Hanyar_shiga)` | `Path` | 필요한 상위 폴더까지 생성 |
| `있는가(Path Hanyar_shiga)` | `boolean` | 존재 여부 Tabbatar_da. 확인할 수 없는 경우도 `false`일 수 있음 |
| `share_Mashigar_bayanai(Path Hanyar_shiga)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `Mashigar_bayanai_Jeri(Path Hanyar_shiga)` | `List<Path>` | 바로 아래 항목을 Hanyar_shiga Daidaita_Daraja 순서로 반환. 재귀 탐색은 아님 |

`Hanyar_shiga`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Yi_Rubutu`와 `Rubuta_bayit_Daraja`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·tasha_Daraja API를 사용하는 방식으로 작성할 수 있다.

### 문자: `한국어.자바.문자`

| tsari_Daraja | 반환형 | Aiki·Yanayi |
|---|---|---|
| `부호화(String kunshiya_Daraja)` | `byte[]` | 문자열을 UTF-8 바이트로 변환 |
| `Bude_Tarin_bayani(byte[] kunshiya_Daraja)` | `String` | UTF-8 바이트를 문자열로 변환. 잘못된 입력은 대체 문자로 haryar_aikin_na_ura_Daraja_Mashigar_bayanai |
| `Gajarta_kimar_bayanai_Daraja(String kunshiya_Daraja)` | `String` | Ɗan_maƙalu_Daraja NFC Gajarta_kimar_bayanai_Daraja. 예: 조합 자모 `ᄀ` + `ᅡ` → `가` |
| `코드포인트수(String kunshiya_Daraja)` | `int` | UTF-16 lambar_sirri_Daraja 단위가 아닌 Ɗan_maƙalu_Daraja lambar_sirri_Daraja 포인트 수 |
| `낱말(String kunshiya_Daraja, Locale yare)` | `List<String>` | sanya_Daraja 언어의 `BreakIterator` 낱말 경계로 나눈 구간 |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Microsoft_Word_Daraja Mashigar_bayanai_Jeri API는 아니다. `Gajarta_kimar_bayanai_Daraja`는 입력기나 Fasara_tushe 기능이 아니다. lambar_sirri_Daraja 포인트 수 역시 사람이 보는 Harafi_Daraja 수와 항상 같지는 않다. 여러 lambar_sirri_Daraja 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### 통신: `한국어.자바.통신`

| tsari_Daraja | 반환형 | Aiki·Yanayi |
|---|---|---|
| `가져오기(URI imel, Duration 제한시간)` | `HttpResponse<String>` | HTTP(S) GET. Haɗi 및 요청 제한시간 Saituna. mayar_da_martani 본문을 UTF-8로 Daddatse_Daraja |
| `연결하기(String imel, int kayan_haɗi_na_kwamfuta_fot, int 제한밀리초)` | `Socket` | TCP Haɗi 후 같은 값으로 Yi_Karatu 제한시간도 Saituna |

`가져오기`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP Kuskure 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. 현재 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`연결하기`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Yi_Rubutu 전체의 마감 시간을 보장하는 옵션은 아니다.

```java
var mayar_da_martani = 통신.가져오기(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(mayar_da_martani.statusCode());
System.out.println(mayar_da_martani.body());
```

위 조각은 tsari_Daraja 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java banbanchi 처리가 필요하다.

### 작업: `한국어.자바.작업`

| tsari_Daraja | 반환형 | Aiki·Yanayi |
|---|---|---|
| `Tafiyar_da(String Suna, Runnable Aiki)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Tafiyar_da |
| `기다리기(Thread hira_Daraja)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 sanya_Daraja lokaci_Daraja 동안 `sleep()` |
| `작업대(int 가닥수)` | `ExecutorService` | 고정 Girma 작업 Shiri_Mai_Fara_Ka_ida 생성. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 사용 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 haryar_aikin_na_ura_Daraja_Mashigar_bayanai 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 수 있다.

### 화면: `한국어.자바.화면`

| tsari_Daraja | 반환형 | Aiki·Yanayi |
|---|---|---|
| `나중에(Runnable Aiki)` | `void` | Swing 이벤트 haryar_aikin_na_ura_Daraja_Mashigar_bayanai 가닥에 실행을 예약하고 반환 |
| `taga(String 제목, JComponent kunshiya_Daraja, int 너비, int 높이)` | `JFrame` | kunshiya_Daraja·크기를 지정한 창을 생성해 Nuna_Daraja |

`taga`을 Swing 이벤트 haryar_aikin_na_ura_Daraja_Mashigar_bayanai hira_Daraja 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
화면.나중에(() -> 화면.taga(
    "한국어 화면", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 수 있다. 창의 Rufe 동작은 `DISPOSE_ON_CLOSE`다. `화면.나중에`가 반환됐다고 taga 생성이 이미 끝난 것은 아니다.

### sararin_aiki: gyaran_Daraja·Gina_tushe GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar 한국어.자바.sararin_aiki
```

`~/workspace`의 원문을 Buɗe·저장하고, `javac`로 컴파일해 `java`로 실행한다. gudanar_Umarni Fayil 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Fayil·문자 API 클래스가 아니다. 생성하는 gudanar_Umarni Fayil 방식은 [컴파일러 설명](../compiler/OpenJDK-실행파일.md)을 따른다.

## 4. Python과 C++에서 사용할 수 있는가?

| tsari_yanayin_aiki | 현재 포함 Matsayi_Daraja | 호출 가능 darfi |
|---|---|---|
| Java → 한국어 JAR | Tanadaddiyar_daraja 포함 | 위 22개 메서드와 sararin_aiki |
| Python → `java` yaro_Daraja 프로세스 | Python·Java Tanadaddiyar_daraja 포함 | 작은 Java 진입점을 통해 호출하고 표준 출력·Fayil 등으로 결과 Ingiza_Daraja |
| Python → JPype → JVM | JPype는 Tanadaddiyar_daraja 배포에 없음 | 별도 Girka_Daraja 후 Java Aji_Daraja·tsari_Daraja 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 추가 inganta 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` 포함 | JVM을 생성하고 한국어 Aji_Daraja·메서드를 직접 호출할 수 있음 |
| Python용 독립 한국어 laburare | 현재 Tanadaddiyar_daraja 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 한국어 모듈을 별도로 작성 |
| C/C++용 독립 한국어 laburare | 자체 x86 `posix-kor`와 자체 ARM64 커널용 초기 RAM Fayil 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`나 `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`나 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Haɗi 계층을 거쳐야 한다.

### Python: 추가 패키지 없이 호출

gudanar_Umarni 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [파이썬호출.py](예제/다른언어/파이썬호출.py)다. Python이 Java 진입점을 실행하고 `문자.코드포인트수`의 Lamba_mara 결과를 받는다. 인수 목록을 사용하며 Mai_fayyace_umani Umarni 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 gudanar_Umarni·Mafita_Shiri lambar_sirri_Daraja·출력 haryar_aikin_na_ura_Daraja_Mashigar_bayanai 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 Baya_Daraja 그 폴더에서 실행한다. 예제 Fayil 자체는 Tanadaddiyar_daraja 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 파이썬호출.py --text '한글 😀'
```

출력: `Python → 한국어.자바.문자.코드포인트수: 4`

이 예제의 Python AIKI_Daraja `코드포인트수`는 이번 문서의 Haɗi 예제이며 기존에 설치된 Python 라이브러리는 아니다. 현재 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java abu_Daraja 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 인수·결과 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 다음 형태로 연결할 수 있다. **아래는 bangaren_zaɓi_Daraja 가능한 Haɗi 방법이며, 현재 배포판에 JPype가 설치돼 있거나 gudanar_Umarni 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 Aji_Daraja 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("한국어.자바.문자")
    print(문자.코드포인트수(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Haɗi 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype Girka_Daraja·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 Na_hakika_Tarin_bayani gudanar_Umarni 가능한 예제다. JVM을 작업 스레드에서 생성하고 다음 메서드를 찾는다.

```cpp
jclass type = env->FindClass("한국어/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "코드포인트수", "(Ljava/lang/String;)I");
```

JVM 생성·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 생성·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 Baya_Daraja 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

출력: `C++ → 한국어.자바.문자.코드포인트수: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI Zare_Daraja zubi_Daraja](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 한국어 메서드도 JNI 서명과 인수 자료형을 맞춰 호출할 수 있다. 예를 들어 `Path`를 받는 Fayil API는 먼저 `Fayil.Hanyar_shiga`로 Java Hanyar_shiga 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 haryar_aikin_na_ura_Daraja_Mashigar_bayanai hira_Daraja 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [자체 ARM64 Haɗi](../posix-kor/arm64-native/README_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM Fayil API를 직접 호출하며, 별도 EL0 Mai_anfani_da_kwamfuta 라이브러리로 Fayil/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 한국어 Java JAR와는 다른 gudanar_Umarni 기반이며 자체 커널은 별도 제한형 Java 컴파일러/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java Kwara_Daraja Fayil·UDP 루프백·사각형 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. 자체 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/README_eb81d7d9.md)에는 `buɗe_Fayil`, `파일자료읽기`, `Rubuta_Fayil_Tarin_bayani`, `Rufe_Fayil`, `통신종단점만들기`, `자료전문보내기` 등의 한국어 C 별칭이 있다. 그러나 구현은 **자체 jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 자체 `sys/stat.h` 등의 헤더는 현재 ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 한국어 Aji_Daraja 라이브러리나 Python용 바인딩을 Tanadaddiyar_daraja 제공하는 상태도 아니다. 현재 Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 구현·빌드해야 한다.

## 5. Tabbatar_da 범위와 재현

패키지 포함 여부는 [배포 패키지 Mashigar_bayanai_Jeri](../platforms/rpi4/dist/packages.lock.json) 및 Gina_na_ura 루트의 Na_hakika_Tarin_bayani 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 Tanadaddiyar_daraja 배포 목록과 다를 수 있다.

이번에 **sauka x86_64/OpenJDK 11에서** Python yaro_Daraja 프로세스 호출과 C++ JNI 직접 호출을 Gina_tushe·실행해 각각 결과 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Haɗi 예제는 추가 패키지를 설치하지 않는다.

문서의 Java 사용 예제도 Gina_tushe·실행했고, 22개 메서드의 문서 포함 여부와 로컬 문서 링크를 확인했다. [예제 inganta logu_naɗa](build/다른언어/amincewa_Rahoto.json)

기존 ARM64 QEMU에서는 Java의 Fayil·Ɗan_maƙalu_Daraja·스레드·HTTP 및 Swing 시험 결과가 있다. 이번 Python/C++ Haɗi 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 gudanar_Umarni 중인 Mai_anfani_da_kwamfuta 환경은 이 문서 작업에서 변경하지 않았다. [기존 OS inganta logu_naɗa](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/파이썬호출.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

sauka C++ 예제는 위 JNI Gina_tushe 명령의 JDK 경로를 **sauka JDK Hanyar_shiga**로 바꾸고, tushe `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·laburare 경로를 sauka x86_64 링크 명령에 섞지 않는다.
