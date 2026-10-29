# jkoros Isi_Zulu umtapo umsebenzisi_isiqondisi

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 자체 x86 ikhenela_inani 및 `okumisiwe_umthombo/`의 관리 ikhenela_inani 모형과 구분한다.

## 1. 현재 제공하는 umtapo

패키지는 `Isi_Zulu.자바`, isistimu_yokusebenza 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **도우미 uhlobo_inani 5개, 공개 ngaguquki_inani indlela_inani 22개, 별도 GUI 프로그램인 indawo_yokusebenzela 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 현재 ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| uhlobo_inani | indlela_inani 수 | 기능 | umthombo |
|---|---:|---|---|
| `Ihele` | 9 | UTF-8 텍스트·ibhayithi_inani Ihele, umkhombandlela_inani, okufakwayo_Uhlu | [Ihele.java](umthombo/Isi_Zulu/자바/Ihele.java) |
| `문자` | 5 | UTF-8 변환, NFC beka_kujwayeleke_inani, 코드 포인트, uchunge_inani 경계 | [문자.java](umthombo/Isi_Zulu/자바/문자.java) |
| `통신` | 2 | HTTP(S) GET, TCP Xhumanisa | [통신.java](umthombo/Isi_Zulu/자바/통신.java) |
| `작업` | 4 | 스레드 yenza_umyalo·대기, 고정 Ubungako 작업 i_app_ikhabethe_le_app | [작업.java](umthombo/Isi_Zulu/자바/작업.java) |
| `화면` | 2 | Swing 이벤트 Inqubo_inani_okufakwayo 가닥에 작업 예약, ifasitela 생성 | [화면.java](umthombo/Isi_Zulu/자바/화면.java) |
| `indawo_yokusebenzela` | okufakwayo_iphoyinti `main` | Java umthombo hlela_inani·Store_inani·akha_umthombo·yenza_umyalo | [indawo_yokusebenzela.java](umthombo/Isi_Zulu/자바/indawo_yokusebenzela.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 uhlobo_lwemininingwane·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing inkinobho·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 qala_umsebenzi

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import Isi_Zulu.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] 인수) throws Exception {
        Path umkhombandlela_inani = Ihele.yakha_umkhombandlela(Ihele.Indlela_2("사용예자료"));
        Path 문서 = umkhombandlela_inani.resolve("인사.txt");
        Ihele.Bhala(문서, "한글 😀");
        String Okuqukethwe_inani = Ihele.Funda(문서);
        System.out.println(Okuqukethwe_inani);
        System.out.println(문자.코드포인트수(Okuqukethwe_inani)); // 한, Itekisi, 공백, 😀 → 4
        Thread 일 = 작업.Sebenzisa("인사 작업", () -> System.out.println("작업 yenza_umyalo"));
        작업.기다리기(일);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 inani_elimisiwe `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 yenza_umyalo 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 uhlobo_inani 폴더를 모두 그 값에 포함해야 한다.

singatha 저장소에서는 다음처럼 akha_isistimu·실행한다. singatha 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 도우미 API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `Ihele.Funda(...)`처럼 호출한다. 표의 이름은 ulwazi_ngokwenzekile_imininingwane umthombo_isihlahla 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 예외 외에도 잘못된 인수 등에 대한 표준 Java yenza_umyalo 시 예외가 발생할 수 있다.

### Ihele: `Isi_Zulu.자바.Ihele`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| indlela_inani | 반환형 | Isenzo·isimo |
|---|---|---|
| `Indlela_2(String Igama)` | `Path` | 이름을 Indlela_2 객체로 변환. ulwazi_ngokwenzekile_imininingwane 파일을 만들지는 않음 |
| `Funda(Path Indlela_2)` | `String` | Ihele 전체를 UTF-8 텍스트로 읽음 |
| `Bhala(Path Indlela_2, String Okuqukethwe_inani)` | `Path` | UTF-8 Store_inani. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path Indlela_2)` | `byte[]` | Ihele 전체를 ibhayithi_inani 배열로 읽음 |
| `bhala_ibhayithi_inani(Path Indlela_2, byte[] Okuqukethwe_inani)` | `Path` | ibhayithi_inani Store_inani. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `yakha_umkhombandlela(Path Indlela_2)` | `Path` | 필요한 상위 폴더까지 생성 |
| `있는가(Path Indlela_2)` | `boolean` | 존재 여부 qiniseka. 확인할 수 없는 경우도 `false`일 수 있음 |
| `지우기(Path Indlela_2)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `okufakwayo_Uhlu(Path Indlela_2)` | `List<Path>` | 바로 아래 항목을 Indlela_2 qondisa_inani 순서로 반환. 재귀 탐색은 아님 |

`Indlela_2`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Bhala`와 `bhala_ibhayithi_inani`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·umgudu_inani API를 사용하는 방식으로 작성할 수 있다.

### 문자: `Isi_Zulu.자바.문자`

| indlela_inani | 반환형 | Isenzo·isimo |
|---|---|---|
| `부호화(String Okuqukethwe_inani)` | `byte[]` | 문자열을 UTF-8 바이트로 변환 |
| `guqulela_imininingwane(byte[] Okuqukethwe_inani)` | `String` | UTF-8 바이트를 문자열로 변환. 잘못된 입력은 대체 문자로 Inqubo_inani_okufakwayo |
| `beka_kujwayeleke_inani(String Okuqukethwe_inani)` | `String` | IYunikhodi_inani NFC beka_kujwayeleke_inani. 예: 조합 자모 `ᄀ` + `ᅡ` → `가` |
| `코드포인트수(String Okuqukethwe_inani)` | `int` | UTF-16 코드 단위가 아닌 IYunikhodi_inani 코드 포인트 수 |
| `낱말(String Okuqukethwe_inani, Locale Ulimi)` | `List<String>` | yabela_inani 언어의 `BreakIterator` 낱말 경계로 나눈 구간 |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Amagama_inani okufakwayo_Uhlu API는 아니다. `beka_kujwayeleke_inani`는 입력기나 Ukuhumusha_umthombo 기능이 아니다. 코드 포인트 수 역시 사람이 보는 uhlamvusimo_inani 수와 항상 같지는 않다. 여러 코드 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### 통신: `Isi_Zulu.자바.통신`

| indlela_inani | 반환형 | Isenzo·isimo |
|---|---|---|
| `가져오기(URI ikheli, Duration 제한시간)` | `HttpResponse<String>` | HTTP(S) GET. Xhumanisa 및 요청 제한시간 Izinhlelo. phendula 본문을 UTF-8로 zawula_inani |
| `연결하기(String ikheli, int 포트, int 제한밀리초)` | `Socket` | TCP Xhumanisa 후 같은 값으로 Funda 제한시간도 Izinhlelo |

`가져오기`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP Iphutha 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. 현재 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`연결하기`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Bhala 전체의 마감 시간을 보장하는 옵션은 아니다.

```java
var phendula = 통신.가져오기(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(phendula.statusCode());
System.out.println(phendula.body());
```

위 조각은 indlela_inani 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java 예외 처리가 필요하다.

### 작업: `Isi_Zulu.자바.작업`

| indlela_inani | 반환형 | Isenzo·isimo |
|---|---|---|
| `Sebenzisa(String Igama, Runnable Isenzo)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Sebenzisa |
| `기다리기(Thread uhlu_lwemilayezo_inani)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 yabela_inani 시간 동안 `sleep()` |
| `작업대(int 가닥수)` | `ExecutorService` | 고정 Ubungako 작업 i_app_ikhabethe_le_app 생성. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 사용 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Inqubo_inani_okufakwayo 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 수 있다.

### 화면: `Isi_Zulu.자바.화면`

| indlela_inani | 반환형 | Isenzo·isimo |
|---|---|---|
| `나중에(Runnable Isenzo)` | `void` | Swing 이벤트 Inqubo_inani_okufakwayo 가닥에 실행을 예약하고 반환 |
| `ifasitela(String ifasitela_Isihloko, JComponent Okuqukethwe_inani, int 너비, int 높이)` | `JFrame` | Okuqukethwe_inani·크기를 지정한 창을 생성해 khombisa_inani |

`ifasitela`을 Swing 이벤트 Inqubo_inani_okufakwayo uhlu_lwemilayezo_inani 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
화면.나중에(() -> 화면.ifasitela(
    "Isi_Zulu 화면", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 수 있다. 창의 Vala 동작은 `DISPOSE_ON_CLOSE`다. `화면.나중에`가 반환됐다고 ifasitela 생성이 이미 끝난 것은 아니다.

### indawo_yokusebenzela: hlela_inani·akha_umthombo GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar Isi_Zulu.자바.indawo_yokusebenzela
```

`~/workspace`의 원문을 Vula·저장하고, `javac`로 컴파일해 `java`로 실행한다. yenza_umyalo Ihele 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 Ihele·문자 API 클래스가 아니다. 생성하는 yenza_umyalo Ihele 방식은 [컴파일러 설명](../compiler/OpenJDK-실행파일.md)을 따른다.

## 4. Python과 C++에서 사용할 수 있는가?

| indlela_inqubo | 현재 포함 isimo_inani | 호출 가능 isiqeshana |
|---|---|---|
| Java → Isi_Zulu JAR | inani_elimisiwe 포함 | 위 22개 메서드와 indawo_yokusebenzela |
| Python → `java` ingane_inani 프로세스 | Python·Java inani_elimisiwe 포함 | 작은 Java 진입점을 통해 호출하고 표준 출력·Ihele 등으로 결과 dlulisela_phambili_inani |
| Python → JPype → JVM | JPype는 inani_elimisiwe 배포에 없음 | 별도 faka_inani 후 Java uhlobo_inani·indlela_inani 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 추가 qinisekisa 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` 포함 | JVM을 생성하고 Isi_Zulu uhlobo_inani·메서드를 직접 호출할 수 있음 |
| Python용 독립 Isi_Zulu umtapo | 현재 inani_elimisiwe 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 Isi_Zulu 모듈을 별도로 작성 |
| C/C++용 독립 Isi_Zulu umtapo | 자체 x86 `posix-kor`와 자체 ARM64 커널용 초기 RAM Ihele 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`나 `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`나 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Xhumanisa 계층을 거쳐야 한다.

### Python: 추가 패키지 없이 호출

yenza_umyalo 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [파이썬호출.py](예제/다른언어/파이썬호출.py)다. Python이 Java 진입점을 실행하고 `문자.코드포인트수`의 inamba 결과를 받는다. 인수 목록을 사용하며 isihumushi_miyalelo Umlayelo 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 yenza_umyalo·phuma_i_app 코드·출력 Inqubo_inani_okufakwayo 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 Impindamuva_inani 그 폴더에서 실행한다. 예제 Ihele 자체는 inani_elimisiwe 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 파이썬호출.py --text '한글 😀'
```

출력: `Python → Isi_Zulu.자바.문자.코드포인트수: 4`

이 예제의 Python umsebenzi_inani `코드포인트수`는 이번 문서의 Xhumanisa 예제이며 기존에 설치된 Python 라이브러리는 아니다. 현재 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java into_inani 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 인수·결과 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 다음 형태로 연결할 수 있다. **아래는 okukhethiwe_inani 가능한 Xhumanisa 방법이며, 현재 배포판에 JPype가 설치돼 있거나 yenza_umyalo 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 uhlobo_inani 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("Isi_Zulu.자바.문자")
    print(문자.코드포인트수(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Xhumanisa 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype faka_inani·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 ulwazi_ngokwenzekile_imininingwane yenza_umyalo 가능한 예제다. JVM을 작업 스레드에서 생성하고 다음 메서드를 찾는다.

```cpp
jclass type = env->FindClass("Isi_Zulu/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "코드포인트수", "(Ljava/lang/String;)I");
```

JVM 생성·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 생성·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 Impindamuva_inani 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

출력: `C++ → Isi_Zulu.자바.문자.코드포인트수: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI uchunge_inani misa_inani](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 Isi_Zulu 메서드도 JNI 서명과 인수 자료형을 맞춰 호출할 수 있다. 예를 들어 `Path`를 받는 Ihele API는 먼저 `Ihele.Indlela_2`로 Java Indlela_2 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Inqubo_inani_okufakwayo uhlu_lwemilayezo_inani 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [자체 ARM64 Xhumanisa](../posix-kor/arm64-native/NGIFUNDE_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM Ihele API를 직접 호출하며, 별도 EL0 umsebenzisi 라이브러리로 Ihele/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 Isi_Zulu Java JAR와는 다른 yenza_umyalo 기반이며 자체 커널은 별도 제한형 Java 컴파일러/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java ikhenela_inani Ihele·UDP 루프백·사각형 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. 자체 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/NGIFUNDE_eb81d7d9.md)에는 `vula_ifayela`, `파일자료읽기`, `bhala_ifayela_imininingwane`, `vala_ifayela`, `통신종단점만들기`, `자료전문보내기` 등의 Isi_Zulu C 별칭이 있다. 그러나 구현은 **자체 jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 자체 `sys/stat.h` 등의 헤더는 현재 ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 Isi_Zulu uhlobo_inani 라이브러리나 Python용 바인딩을 inani_elimisiwe 제공하는 상태도 아니다. 현재 Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 구현·빌드해야 한다.

## 5. qiniseka 범위와 재현

패키지 포함 여부는 [배포 패키지 okufakwayo_Uhlu](../platforms/rpi4/dist/packages.lock.json) 및 akha_isistimu 루트의 ulwazi_ngokwenzekile_imininingwane 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 inani_elimisiwe 배포 목록과 다를 수 있다.

이번에 **singatha x86_64/OpenJDK 11에서** Python ingane_inani 프로세스 호출과 C++ JNI 직접 호출을 akha_umthombo·실행해 각각 결과 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Xhumanisa 예제는 추가 패키지를 설치하지 않는다.

문서의 Java 사용 예제도 akha_umthombo·실행했고, 22개 메서드의 문서 포함 여부와 로컬 문서 링크를 확인했다. [예제 qinisekisa loga_umugqa](build/다른언어/ukufakazisa_umbiko.json)

기존 ARM64 QEMU에서는 Java의 Ihele·IYunikhodi_inani·스레드·HTTP 및 Swing 시험 결과가 있다. 이번 Python/C++ Xhumanisa 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 yenza_umyalo 중인 umsebenzisi 환경은 이 문서 작업에서 변경하지 않았다. [기존 isistimu_yokusebenza qinisekisa loga_umugqa](../platforms/rpi4/VERIFICATION.md)

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

singatha C++ 예제는 위 JNI akha_umthombo 명령의 JDK 경로를 **singatha JDK Indlela_2**로 바꾸고, umthombo `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·umtapo 경로를 singatha x86_64 링크 명령에 섞지 않는다.
