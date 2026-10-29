# jkoros suomi kirjasto käyttäjä_opas

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 oma x86 ydin_ARVO 및 `vanha_lähde/`의 관리 ydin_ARVO 모형과 구분한다.

## 1. nykyinen_kohde 제공하는 kirjasto

패키지는 `suomi.자바`, käyttöjärjestelmä 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **apuosa_ARVO Luokka_ARVO 5개, 공개 staattinen_ARVO menetelmä_ARVO 22개, 별도 GUI 프로그램인 työtila 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 nykyinen_kohde ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| Luokka_ARVO | menetelmä_ARVO numero | 기능 | lähdetiedosto |
|---|---:|---|---|
| `tiedoston_nimi` | 9 | UTF-8 텍스트·tavu_ARVO tiedoston_nimi, Directory_ARVO, merkintä_luettelo | [tiedoston_nimi.java](lähdetiedosto/suomi/자바/tiedoston_nimi.java) |
| `문자` | 5 | UTF-8 MUUNNA_ARVO, NFC normalisoida_ARVO, KOODI_ARVO 포인트, merkkijono_ARVO rajattu_alue_ARVO | [문자.java](lähdetiedosto/suomi/자바/문자.java) |
| `통신` | 2 | HTTP(S) GET, TCP Yhdistä | [통신.java](lähdetiedosto/suomi/자바/통신.java) |
| `작업` | 4 | 스레드 Suorita_komento·odottaa_ARVO, 고정 Koko 작업 ohjelma_sovellusvalikko | [작업.java](lähdetiedosto/suomi/자바/작업.java) |
| `화면` | 2 | Swing 이벤트 prosessi_ARVO_merkintä 가닥에 작업 예약, Ikkuna generoida | [화면.java](lähdetiedosto/suomi/자바/화면.java) |
| `työtila` | aloituskohta `main` | Java lähdetiedosto muutos_ARVO·Store_ARVO·kääntää_lähde·Suorita_komento | [työtila.java](lähdetiedosto/suomi/자바/työtila.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 tietotyyppi·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing painike·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 alku_tehtävä

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import suomi.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] argumentit) throws Exception {
        Path Directory_ARVO = tiedoston_nimi.Luo_Directory(tiedoston_nimi.polku_2("사용예자료"));
        Path 문서 = Directory_ARVO.resolve("인사.txt");
        tiedoston_nimi.Kirjoitus(문서, "한글 😀");
        String Sisältö_ARVO = tiedoston_nimi.Luku(문서);
        System.out.println(Sisältö_ARVO);
        System.out.println(문자.koodipiste_LASKE(Sisältö_ARVO)); // 한, teksti, 공백, 😀 → 4
        Thread Työ_ARVO = 작업.Suorita_2("인사 작업", () -> System.out.println("작업 Suorita_komento"));
        작업.기다리기(Työ_ARVO);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 oletusarvo `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Suorita_komento 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 Luokka_ARVO 폴더를 모두 그 값에 포함해야 한다.

isäntä 저장소에서는 다음처럼 kääntää_Järjestelmä·실행한다. isäntä 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/인사.java
java -cp build/한국어자바.jar:예제 인사
```

## 3. 전체 apuosa_ARVO API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `tiedoston_nimi.Luku(...)`처럼 호출한다. 표의 이름은 todellinen_data lähde_puu 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 poikkeus 외에도 잘못된 argumentit 등에 대한 표준 Java Suorita_komento 시 예외가 발생할 numero 있다.

### tiedoston_nimi: `suomi.자바.tiedoston_nimi`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| menetelmä_ARVO | palauttaa_TYYPPI | Toiminto·ehto |
|---|---|---|
| `polku_2(String Nimi)` | `Path` | 이름을 polku_2 객체로 MUUNNA_ARVO. todellinen_data 파일을 만들지는 않음 |
| `Luku(Path polku_2)` | `String` | tiedoston_nimi 전체를 UTF-8 텍스트로 lukea_KR |
| `Kirjoitus(Path polku_2, String Sisältö_ARVO)` | `Path` | UTF-8 Store_ARVO. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `lukea_tavu_ARVO(Path polku_2)` | `byte[]` | tiedoston_nimi 전체를 tavu_ARVO 배열로 lukea_KR |
| `kirjoitus_tavu_ARVO(Path polku_2, byte[] Sisältö_ARVO)` | `Path` | tavu_ARVO Store_ARVO. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `Luo_Directory(Path polku_2)` | `Path` | 필요한 상위 폴더까지 generoida |
| `있는가(Path polku_2)` | `boolean` | 존재 여부 tarkistaa. 확인할 numero 없는 경우도 `false`Työ_ARVO numero 있음 |
| `poistaa_merkintä_c8dbc399(Path polku_2)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `merkintä_luettelo(Path polku_2)` | `List<Path>` | 바로 아래 항목을 polku_2 tasaa_ARVO 순서로 palauttaa_KR. 재귀 탐색은 아님 |

`polku_2`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Kirjoitus`와 `kirjoitus_tavu_ARVO`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Media_ARVO API를 사용하는 방식으로 작성할 numero 있다.

### 문자: `suomi.자바.문자`

| menetelmä_ARVO | palauttaa_TYYPPI | Toiminto·ehto |
|---|---|---|
| `koodata(String Sisältö_ARVO)` | `byte[]` | 문자열을 UTF-8 바이트로 MUUNNA_ARVO |
| `pura_salaus_data(byte[] Sisältö_ARVO)` | `String` | UTF-8 바이트를 문자열로 MUUNNA_ARVO. 잘못된 입력은 대체 문자로 prosessi_ARVO_merkintä |
| `normalisoida_ARVO(String Sisältö_ARVO)` | `String` | UNICODE_ARVO NFC normalisoida_ARVO. 예: kokoonpano_ARVO 자모 `ᄀ` + `ᅡ` → `가` |
| `koodipiste_LASKE(String Sisältö_ARVO)` | `int` | UTF-16 KOODI_ARVO 단위가 아닌 UNICODE_ARVO KOODI_ARVO 포인트 numero |
| `낱말(String Sisältö_ARVO, Locale Kieli)` | `List<String>` | Määritä_ARVO 언어의 `BreakIterator` 낱말 경계로 나눈 SMS_alue |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Word_ARVO merkintä_luettelo API는 아니다. `normalisoida_ARVO`는 입력기나 KÄÄNNÄ_lähde 기능이 아니다. KOODI_ARVO 포인트 numero 역시 사람이 보는 merkki_ARVO 수와 항상 같지는 않다. 여러 KOODI_ARVO 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### 통신: `suomi.자바.통신`

| menetelmä_ARVO | palauttaa_TYYPPI | Toiminto·ehto |
|---|---|---|
| `OTA_ARVO(URI OSOITE, Duration aikaraja)` | `HttpResponse<String>` | HTTP(S) GET. Yhdistä 및 pyyntö aikaraja Asetukset. palaute 본문을 UTF-8로 jäsentää_ARVO |
| `YHDISTÄ_päätepiste(String OSOITE, int laitteisto_portti, int 제한밀리초)` | `Socket` | TCP Yhdistä 후 같은 값으로 Luku 제한시간도 Asetukset |

`OTA_ARVO`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP VIRHE 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. nykyinen_kohde 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`YHDISTÄ_päätepiste`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Kirjoitus 전체의 määräaika_ARVO 시간을 보장하는 옵션은 아니다.

```java
var palaute = 통신.OTA_ARVO(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(palaute.statusCode());
System.out.println(palaute.body());
```

위 조각은 menetelmä_ARVO 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java poikkeus 처리가 필요하다.

### 작업: `suomi.자바.작업`

| menetelmä_ARVO | palauttaa_TYYPPI | Toiminto·ehto |
|---|---|---|
| `Suorita_2(String Nimi, Runnable Toiminto)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 Suorita_2 |
| `기다리기(Thread säie_ARVO)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 Määritä_ARVO AIKA_ARVO 동안 `sleep()` |
| `작업대(int säikeiden_määrä)` | `ExecutorService` | 고정 Koko 작업 ohjelma_sovellusvalikko generoida. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 käyttö_ARVO 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 prosessi_ARVO_merkintä 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 numero 있다.

### 화면: `suomi.자바.화면`

| menetelmä_ARVO | palauttaa_TYYPPI | Toiminto·ehto |
|---|---|---|
| `나중에(Runnable Toiminto)` | `void` | Swing 이벤트 prosessi_ARVO_merkintä 가닥에 실행을 예약하고 palauttaa_KR |
| `Ikkuna(String ikkuna_nimi, JComponent Sisältö_ARVO, int 너비, int 높이)` | `JFrame` | Sisältö_ARVO·크기를 지정한 창을 생성해 näyttää_ARVO |

`Ikkuna`을 Swing 이벤트 prosessi_ARVO_merkintä säie_ARVO 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
화면.나중에(() -> 화면.Ikkuna(
    "suomi 화면", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 numero 있다. 창의 Sulje 동작은 `DISPOSE_ON_CLOSE`다. `화면.나중에`가 반환됐다고 Ikkuna 생성이 이미 끝난 것은 아니다.

### työtila: muutos_ARVO·kääntää_lähde GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar suomi.자바.työtila
```

`~/workspace`의 원문을 Avaa·저장하고, `javac`로 컴파일해 `java`로 실행한다. Suorita_komento tiedoston_nimi 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 tiedoston_nimi·문자 API 클래스가 아니다. 생성하는 Suorita_komento tiedoston_nimi 방식은 [kääntäjä 설명](../compiler/OpenJDK-suoritettava_tiedosto.md)을 따른다.

## 4. Python과 C++에서 사용할 numero 있는가?

| menetelmä_tila | nykyinen_kohde esittelyt Tila_ARVO | 호출 가능 leikata |
|---|---|---|
| Java → suomi JAR | oletusarvo esittelyt | 위 22개 메서드와 työtila |
| Python → `java` ali_ARVO 프로세스 | Python·Java oletusarvo esittelyt | 작은 Java 진입점을 통해 호출하고 표준 tulostuspaikka·tiedoston_nimi 등으로 TULOS siirrä_ARVO_24592b8a |
| Python → JPype → JVM | JPype는 oletusarvo 배포에 없음 | 별도 asentaa_ARVO 후 Java Luokka_ARVO·menetelmä_ARVO 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 liitä_merkintä vahvista 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` esittelyt | JVM을 생성하고 suomi Luokka_ARVO·메서드를 직접 호출할 numero 있음 |
| Python용 독립 suomi kirjasto | nykyinen_kohde oletusarvo 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 suomi 모듈을 별도로 작성 |
| C/C++용 독립 suomi kirjasto | oma x86 `posix-kor`와 oma ARM64 커널용 alkutila RAM tiedoston_nimi 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SEKUNNIT_operandi `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SEKUNNIT_operandi 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Yhdistä 계층을 거쳐야 한다.

### Python: liitä_merkintä 패키지 없이 호출

Suorita_komento 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Puhelut.py](예제/다른언어/PYTHON_Puhelut.py)다. Python이 Java 진입점을 실행하고 `문자.koodipiste_LASKE`의 kokonaisluku 결과를 받는다. argumentit 목록을 사용하며 liittymä komento 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Suorita_komento·Lopeta_ohjelma KOODI_ARVO·tulostuspaikka prosessi_ARVO_merkintä 방식은 [Python 공식 문서](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_ARVO 그 폴더에서 실행한다. 예제 tiedoston_nimi 자체는 oletusarvo 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Puhelut.py --text '한글 😀'
```

tulostuspaikka: `Python → suomi.자바.문자.koodipiste_LASKE: 4`

이 예제의 Python funktio_ARVO `koodipiste_LASKE`는 이번 문서의 Yhdistä 예제이며 기존에 설치된 Python 라이브러리는 아니다. nykyinen_kohde 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objekti_ARVO 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 argumentit·TULOS 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Seuraava_kohde 형태로 연결할 numero 있다. **아래는 valinta_ARVO 가능한 Yhdistä 방법이며, nykyinen_kohde 배포판에 JPype가 설치돼 있거나 Suorita_komento 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 Luokka_ARVO 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("suomi.자바.문자")
    print(문자.koodipiste_LASKE(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Yhdistä 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype asentaa_ARVO·패키지 빌드는 이번 문서 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 todellinen_data Suorita_komento 가능한 예제다. JVM을 작업 스레드에서 생성하고 Seuraava_kohde 메서드를 찾는다.

```cpp
jclass type = env->FindClass("suomi/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "koodipiste_LASKE", "(Ljava/lang/String;)I");
```

JVM generoida·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generoida·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_ARVO 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

tulostuspaikka: `C++ → suomi.자바.문자.koodipiste_LASKE: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI merkkijono_ARVO muoto_ARVO](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 suomi 메서드도 JNI 서명과 argumentit 자료형을 맞춰 호출할 numero 있다. 예를 들어 `Path`를 받는 tiedoston_nimi API는 먼저 `tiedoston_nimi.polku_2`로 Java polku_2 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 prosessi_ARVO_merkintä säie_ARVO 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [oma ARM64 Yhdistä](../posix-kor/arm64-native/Lueminut_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM tiedoston_nimi API를 직접 호출하며, 별도 EL0 käyttäjätila 라이브러리로 tiedoston_nimi/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 suomi Java JAR와는 다른 Suorita_komento 기반이며 oma 커널은 별도 제한형 Java kääntäjä/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java ydin_ARVO tiedoston_nimi·UDP 루프백·suorakulmio 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. oma 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/Lueminut_eb81d7d9.md)에는 `avata_Tiedosto`, `lukea_Tiedosto_data`, `kirjoitus_Tiedosto_data`, `Sulje_Tiedosto`, `Luo_päätepiste`, `lähettää_datagrammi_data` 등의 suomi C 별칭이 있다. 그러나 구현은 **oma jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 oma `sys/stat.h` 등의 헤더는 nykyinen_kohde ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 suomi Luokka_ARVO 라이브러리나 Python용 바인딩을 oletusarvo 제공하는 상태도 아니다. nykyinen_kohde Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 toteutus·빌드해야 한다.

## 5. tarkistaa 범위와 재현

패키지 esittelyt 여부는 [jakelu_ARVO 패키지 merkintä_luettelo](../platforms/rpi4/dist/packages.lock.json) 및 kääntää_Järjestelmä 루트의 todellinen_data 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 oletusarvo jakelu_ARVO 목록과 다를 numero 있다.

이번에 **isäntä x86_64/OpenJDK 11에서** Python ali_ARVO 프로세스 호출과 C++ JNI 직접 호출을 kääntää_lähde·실행해 각각 TULOS 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Yhdistä 예제는 liitä_merkintä 패키지를 설치하지 않는다.

문서의 Java käyttö_ARVO 예제도 kääntää_lähde·실행했고, 22개 메서드의 문서 esittelyt 여부와 로컬 문서 링크를 확인했다. [예제 vahvista LOG_TIETUE](build/다른언어/vahvistus_raportti.json)

기존 ARM64 QEMU에서는 Java의 tiedoston_nimi·UNICODE_ARVO·스레드·HTTP 및 Swing testit 결과가 있다. 이번 Python/C++ Yhdistä 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Suorita_komento 중인 käyttäjätila 환경은 이 문서 작업에서 변경하지 않았다. [기존 käyttöjärjestelmä vahvista LOG_TIETUE](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Puhelut.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

isäntä C++ 예제는 위 JNI kääntää_lähde 명령의 JDK 경로를 **isäntä JDK polku_2**로 바꾸고, lähdetiedosto `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·kirjasto 경로를 isäntä x86_64 링크 명령에 섞지 않는다.
