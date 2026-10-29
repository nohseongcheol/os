# jkoros Italiano Catalogo USER_guida

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 nativo x86 kernel_VALORE 및 `legacy_fonte/`의 관리 kernel_VALORE 모형과 구분한다.

## 1. Regolari_articolo 제공하는 Catalogo

패키지는 `Italiano.자바`, sistema_operativo 안의 JAR 경로는 `/opt/jkoros/lib/한국어자바.jar`다. **helper_VALORE Corso_VALORE 5개, 공개 statico_VALORE metodo_VALORE 22개, 별도 GUI 프로그램인 area_di_lavoro 1개**가 있다. JAR는 Java 11 이상을 대상으로 빌드하며 Regolari_articolo ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| Corso_VALORE | metodo_VALORE numero | 기능 | codiceSorgente |
|---|---:|---|---|
| `file` | 9 | UTF-8 텍스트·byte_VALORE file, elenco_VALORE, voce_elenco | [file.java](codiceSorgente/Italiano/자바/file.java) |
| `문자` | 5 | UTF-8 CONVERTI_VALORE, NFC normalizzare_VALORE, CODICE_VALORE 포인트, stringa_VALORE limite_VALORE | [문자.java](codiceSorgente/Italiano/자바/문자.java) |
| `comunicazione` | 2 | HTTP(S) GET, TCP Connetti | [comunicazione.java](codiceSorgente/Italiano/자바/comunicazione.java) |
| `작업` | 4 | 스레드 Esegui_comando·aspetta_VALORE, 고정 Dimensione 작업 app_Launcher | [작업.java](codiceSorgente/Italiano/자바/작업.java) |
| `schermata` | 2 | Swing 이벤트 Processi_VALORE_voce 가닥에 작업 예약, Finestra generare | [schermata.java](codiceSorgente/Italiano/자바/schermata.java) |
| `area_di_lavoro` | punto_di_ingresso `main` | Java codiceSorgente Modifica_VALORE·Store_VALORE·compilare_fonte·Esegui_comando | [area_di_lavoro.java](codiceSorgente/Italiano/자바/area_di_lavoro.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 tipo_di_dati·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing pulsante·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 START_task

게스트 운영체제의 작업 폴더에서 `사용예.java`를 작성한다.

```java
import Italiano.자바.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] argomenti) throws Exception {
        Path elenco_VALORE = file.Crea_elenco(file.percorso("사용예자료"));
        Path Guides = elenco_VALORE.resolve("messaggio_di_saluto_ae353e94.txt");
        file.Scrittura(Guides, "한글 😀");
        String Contenuto_VALORE = file.Lettura(Guides);
        System.out.println(Contenuto_VALORE);
        System.out.println(문자.punto_di_codice_CONTA_NUMERI(Contenuto_VALORE)); // 한, testo, 공백, 😀 → 4
        Thread lavoro_VALORE = 작업.avvia("messaggio_di_saluto_ae353e94 작업", () -> System.out.println("작업 Esegui_comando"));
        작업.기다리기(lavoro_VALORE);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar 사용예.java
java -cp .:/opt/jkoros/lib/한국어자바.jar 사용예
```

로그인 환경에 valore_predefinito `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 Esegui_comando 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 Corso_VALORE 폴더를 모두 그 값에 포함해야 한다.

host 저장소에서는 다음처럼 costruire·실행한다. host 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/한국어자바
make
javac -encoding UTF-8 -cp build/한국어자바.jar 예제/messaggio_di_saluto_ae353e94.java
java -cp build/한국어자바.jar:예제 messaggio_di_saluto_ae353e94
```

## 3. 전체 helper_VALORE API

아래 메서드는 모두 `public static`이며, 객체를 만들지 않고 `file.Lettura(...)`처럼 호출한다. 표의 이름은 effettivo_dati fonte_albero 및 JAR의 `javap -public` 결과와 대조했다. 선언된 검사 eccezione 외에도 잘못된 argomenti 등에 대한 표준 Java Esegui_comando 시 예외가 발생할 numero 있다.

### file: `Italiano.자바.file`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`다.

| metodo_VALORE | tipo_restituito | Azione·condizione |
|---|---|---|
| `percorso(String Nome)` | `Path` | 이름을 percorso 객체로 CONVERTI_VALORE. effettivo_dati 파일을 만들지는 않음 |
| `Lettura(Path percorso)` | `String` | file 전체를 UTF-8 텍스트로 읽음 |
| `Scrittura(Path percorso, String Contenuto_VALORE)` | `Path` | UTF-8 Store_VALORE. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `바이트읽기(Path percorso)` | `byte[]` | file 전체를 byte_VALORE 배열로 읽음 |
| `scrivere_byte_VALORE(Path percorso, byte[] Contenuto_VALORE)` | `Path` | byte_VALORE Store_VALORE. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `Crea_elenco(Path percorso)` | `Path` | 필요한 상위 폴더까지 generare |
| `있는가(Path percorso)` | `boolean` | 존재 여부 verificare. 확인할 numero 없는 경우도 `false`lavoro_VALORE numero 있음 |
| `cancellare_voce(Path percorso)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `voce_elenco(Path percorso)` | `List<Path>` | 바로 아래 항목을 percorso allineare_VALORE 순서로 Reso_KR. 재귀 탐색은 아님 |

`percorso`, `있는가`를 제외한 위 메서드는 `IOException`을 선언한다. `Scrittura`와 `scrivere_byte_VALORE`는 상위 폴더를 자동으로 만들거나 내용을 이어 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·Canale_VALORE API를 사용하는 방식으로 작성할 numero 있다.

### 문자: `Italiano.자바.문자`

| metodo_VALORE | tipo_restituito | Azione·condizione |
|---|---|---|
| `codificare(String Contenuto_VALORE)` | `byte[]` | 문자열을 UTF-8 바이트로 CONVERTI_VALORE |
| `decifrare_dati(byte[] Contenuto_VALORE)` | `String` | UTF-8 바이트를 문자열로 CONVERTI_VALORE. 잘못된 입력은 대체 문자로 Processi_VALORE_voce |
| `normalizzare_VALORE(String Contenuto_VALORE)` | `String` | UNICODE_VALORE NFC normalizzare_VALORE. 예: composizione_VALORE 자모 `ᄀ` + `ᅡ` → `가` |
| `punto_di_codice_CONTA_NUMERI(String Contenuto_VALORE)` | `int` | UTF-16 CODICE_VALORE 단위가 아닌 UNICODE_VALORE CODICE_VALORE 포인트 numero |
| `낱말(String Contenuto_VALORE, Locale Lingua)` | `List<String>` | Assegna_VALORE 언어의 `BreakIterator` 낱말 경계로 나눈 SMS_intervallo |

`낱말`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 Word_VALORE voce_elenco API는 아니다. `normalizzare_VALORE`는 입력기나 TRADUCI_fonte 기능이 아니다. CODICE_VALORE 포인트 numero 역시 사람이 보는 carattere_VALORE 수와 항상 같지는 않다. 여러 CODICE_VALORE 포인트로 이루어진 결합 문자·가족 이모지 등을 구분해야 한다.

### comunicazione: `Italiano.자바.comunicazione`

| metodo_VALORE | tipo_restituito | Azione·condizione |
|---|---|---|
| `INCLUDI_VALORE(URI e_mail, Duration limite_di_tempo)` | `HttpResponse<String>` | HTTP(S) GET. Connetti 및 richiesta limite_di_tempo Impostazioni. replica 본문을 UTF-8로 analizzare_VALORE |
| `Connect_Endpoint(String e_mail, int hardware_porta, int 제한밀리초)` | `Socket` | TCP Connetti 후 같은 값으로 Lettura 제한시간도 Impostazioni |

`INCLUDI_VALORE`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP errore 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. Regolari_articolo 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`Connect_Endpoint`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 제한 없음이며, Scrittura 전체의 scadenza_VALORE 시간을 보장하는 옵션은 아니다.

```java
var replica = comunicazione.INCLUDI_VALORE(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(replica.statusCode());
System.out.println(replica.body());
```

위 조각은 metodo_VALORE 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java eccezione 처리가 필요하다.

### 작업: `Italiano.자바.작업`

| metodo_VALORE | tipo_restituito | Azione·condizione |
|---|---|---|
| `avvia(String Nome, Runnable Azione)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 avvia |
| `기다리기(Thread thread_VALORE)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `쉬기(long 밀리초)` | `void` | 호출한 스레드를 Assegna_VALORE valore 동안 `sleep()` |
| `Workbench_VALORE(int Conteggio_dei_thread)` | `ExecutorService` | 고정 Dimensione 작업 app_Launcher generare. 가닥수는 양수 |

`기다리기`, `쉬기`는 `InterruptedException`을 선언한다. 작업 실행기는 usare_VALORE 후 `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 Processi_VALORE_voce 가닥에서 긴 작업이나 `기다리기`를 실행하면 화면이 멈출 numero 있다.

### schermata: `Italiano.자바.schermata`

| metodo_VALORE | tipo_restituito | Azione·condizione |
|---|---|---|
| `나중에(Runnable Azione)` | `void` | Swing 이벤트 Processi_VALORE_voce 가닥에 실행을 예약하고 Reso_KR |
| `Finestra(String finestra_titolo, JComponent Contenuto_VALORE, int 너비, int altezza_VALORE)` | `JFrame` | Contenuto_VALORE·크기를 지정한 창을 생성해 mostrare_VALORE |

`Finestra`을 Swing 이벤트 Processi_VALORE_voce thread_VALORE 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
schermata.나중에(() -> schermata.Finestra(
    "Italiano schermata", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 numero 있다. 창의 Chiudi 동작은 `DISPOSE_ON_CLOSE`다. `schermata.나중에`가 반환됐다고 Finestra 생성이 이미 끝난 것은 아니다.

### area_di_lavoro: Modifica_VALORE·compilare_fonte GUI

```sh
java -cp /opt/jkoros/lib/한국어자바.jar Italiano.자바.area_di_lavoro
```

`~/workspace`의 원문을 Apri·저장하고, `javac`로 컴파일해 `java`로 실행한다. Esegui_comando file 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 file·문자 API 클래스가 아니다. 생성하는 Esegui_comando file 방식은 [compilatore 설명](../compiler/OpenJDK-eseguibile.md)을 따른다.

## 4. Python과 C++에서 사용할 numero 있는가?

| metodo_MODA | Regolari_articolo dichiarazioni Stato_VALORE | 호출 가능 ritagliare |
|---|---|---|
| Java → Italiano JAR | valore_predefinito dichiarazioni | 위 22개 메서드와 area_di_lavoro |
| Python → `java` figlio_VALORE 프로세스 | Python·Java valore_predefinito dichiarazioni | 작은 Java 진입점을 통해 호출하고 표준 uscitaTesto·file 등으로 risultato Avanti_VALORE |
| Python → JPype → JVM | JPype는 valore_predefinito 배포에 없음 | 별도 installare_VALORE 후 Java Corso_VALORE·metodo_VALORE 호출 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 Aggiunta_voce convalidare 필요 |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` dichiarazioni | JVM을 생성하고 Italiano Corso_VALORE·메서드를 직접 호출할 numero 있음 |
| Python용 독립 Italiano Catalogo | Regolari_articolo valore_predefinito 제공 없음 | 필요하면 Python 표준 라이브러리를 감싸는 Italiano 모듈을 별도로 작성 |
| C/C++용 독립 Italiano Catalogo | nativo x86 `posix-kor`와 nativo ARM64 커널용 stato_iniziale RAM file 연결이 별도로 존재 | 둘 다 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`SECONDO_operando `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`SECONDO_operando 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM Connetti 계층을 거쳐야 한다.

### Python: Aggiunta_voce 패키지 없이 호출

Esegui_comando 가능한 예제 원문은 [문자명령.java](예제/다른언어/문자명령.java), [PYTHON_Chiamate.py](예제/다른언어/PYTHON_Chiamate.py)다. Python이 Java 진입점을 실행하고 `문자.punto_di_codice_CONTA_NUMERI`의 intero 결과를 받는다. argomenti 목록을 사용하며 Shell comando 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 Esegui_comando·Esci_app CODICE_VALORE·uscitaTesto Processi_VALORE_voce 방식은 [Python 공식 Guides](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 예제 파일을 게스트의 같은 폴더에 복사한 BACK_VALORE 그 폴더에서 실행한다. 예제 file 자체는 valore_predefinito 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/한국어자바.jar -d classes 문자명령.java
python3 PYTHON_Chiamate.py --text '한글 😀'
```

uscitaTesto: `Python → Italiano.자바.문자.punto_di_codice_CONTA_NUMERI: 4`

이 예제의 Python FUNZIONE_VALORE `punto_di_codice_CONTA_NUMERI`는 이번 문서의 Connetti 예제이며 기존에 설치된 Python 라이브러리는 아니다. Regolari_articolo 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java oggetto_VALORE 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 argomenti·risultato 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 호출

JPype를 별도 설치한 환경에서는 Avanti_articolo 형태로 연결할 numero 있다. **아래는 selezione_VALORE 가능한 Connetti 방법이며, Regolari_articolo 배포판에 JPype가 설치돼 있거나 Esegui_comando 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 Corso_VALORE 접근은 [JPype 공식 설명](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/한국어자바.jar"])
try:
    문자 = jpype.JClass("Italiano.자바.문자")
    print(문자.punto_di_codice_CONTA_NUMERI(jpype.JString("한글 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·Connetti 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype installare_VALORE·패키지 빌드는 이번 Guides 작업에서 수행하지 않았다.

### C++: JNI로 직접 호출

[자바호출.cpp](예제/다른언어/자바호출.cpp)는 effettivo_dati Esegui_comando 가능한 예제다. JVM을 작업 스레드에서 생성하고 Avanti_articolo 메서드를 찾는다.

```cpp
jclass type = env->FindClass("Italiano/자바/문자");
jmethodID method = env->GetStaticMethodID(
    type, "punto_di_codice_CONTA_NUMERI", "(Ljava/lang/String;)I");
```

JVM generare·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generare·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `자바호출.cpp`를 복사한 BACK_VALORE 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`다.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  자바호출.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o 자바호출
./자바호출 /opt/jkoros/lib/한국어자바.jar
```

uscitaTesto: `C++ → Italiano.자바.문자.punto_di_codice_CONTA_NUMERI: 4`

예제는 `한글 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`가 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI stringa_VALORE formato_VALORE](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 Italiano 메서드도 JNI 서명과 argomenti 자료형을 맞춰 호출할 numero 있다. 예를 들어 `Path`를 받는 file API는 먼저 `file.percorso`로 Java percorso 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 Processi_VALORE_voce thread_VALORE 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 계속 필요하다.

### 기존 posix-kor와의 관계

추가된 [nativo ARM64 Connetti](../posix-kor/arm64-native/README_eb81d7d9.md)은 C++에서 AOT Java 커널의 RAM file API를 직접 호출하며, 별도 EL0 spazio_utente 라이브러리로 file/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 Italiano Java JAR와는 다른 Esegui_comando 기반이며 nativo 커널은 별도 제한형 Java compilatore/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java kernel_VALORE file·UDP 루프백·rettangolo 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. nativo 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/README_eb81d7d9.md)에는 `aperto_File`, `파일자료읽기`, `scrivere_File_dati`, `Chiudi_File`, `Crea_endpoint`, `inviare_datagramma_dati` 등의 Italiano C 별칭이 있다. 그러나 구현은 **nativo jkoros i386 커널의 `int 0x80` 호출 규약용**이다.

이 `libposix-kor.a`와 nativo `sys/stat.h` 등의 헤더는 Regolari_articolo ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 Italiano Corso_VALORE 라이브러리나 Python용 바인딩을 valore_predefinito 제공하는 상태도 아니다. Regolari_articolo Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 implementazione·빌드해야 한다.

## 5. verificare 범위와 재현

패키지 dichiarazioni 여부는 [distribuzione_VALORE 패키지 voce_elenco](../platforms/rpi4/dist/packages.lock.json) 및 costruire 루트의 effettivo_dati 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 이후 별도로 설치한 패키지는 이 valore_predefinito distribuzione_VALORE 목록과 다를 numero 있다.

이번에 **host x86_64/OpenJDK 11에서** Python figlio_VALORE 프로세스 호출과 C++ JNI 직접 호출을 compilare_fonte·실행해 각각 risultato 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python Connetti 예제는 Aggiunta_voce 패키지를 설치하지 않는다.

문서의 Java usare_VALORE 예제도 compilare_fonte·실행했고, 22개 메서드의 Guides dichiarazioni 여부와 로컬 Guides 링크를 확인했다. [예제 convalidare LOG_riga](build/다른언어/convalida_Report.json)

기존 ARM64 QEMU에서는 Java의 file·UNICODE_VALORE·스레드·HTTP 및 Swing prove 결과가 있다. 이번 Python/C++ Connetti 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 Esegui_comando 중인 spazio_utente 환경은 이 Guides 작업에서 변경하지 않았다. [기존 sistema_operativo convalidare LOG_riga](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/한국어자바
make
mkdir -p build/다른언어
javac -encoding UTF-8 --release 11 -cp build/한국어자바.jar \
  -d build/다른언어 예제/다른언어/문자명령.java
python3 예제/다른언어/PYTHON_Chiamate.py \
  --jar build/한국어자바.jar --classes build/다른언어
```

host C++ 예제는 위 JNI compilare_fonte 명령의 JDK 경로를 **host JDK percorso**로 바꾸고, codiceSorgente `예제/다른언어/자바호출.cpp`와 JAR `build/한국어자바.jar`를 지정한다. ARM64 게스트 JDK의 헤더·Catalogo 경로를 host x86_64 링크 명령에 섞지 않는다.
