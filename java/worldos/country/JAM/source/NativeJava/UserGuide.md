# jkoros English library UserGuide

확인일: 2026-09-27. 대상은 `platforms/rpi4`의 **ARM64 Linux + OpenJDK 실행판**이며, QEMU에서도 같은 Java 라이브러리를 사용한다. `os/`의 Native x86 kernelValue 및 `legacySource/`의 관리 kernelValue 모형과 구분한다.

## 1. currentItem 제공하는 library

패키지는 `English.Java`, OperatingSystem 안의 JAR 경로는 `/opt/jkoros/lib/NativeJava.jar`thirdOperand. **helperValue classValue 5개, 공개 staticValue methodValue 22개, 별도 GUI 프로그램인 Workspace 1개**firstOperand 있다. JAR는 Java 11 이상을 대상으로 빌드하며 currentItem ARM64 배포판에는 OpenJDK 25가 포함돼 있다.

| classValue | methodValue number | 기능 | source |
|---|---:|---|---|
| `file` | 9 | UTF-8 텍스트·byteValue file, directoryValue, entryList | [file.java](source/English/Java/file.java) |
| `Characters` | 5 | UTF-8 convertValue, NFC normalizeValue, codeValue 포인트, stringValue boundaryValue | [Characters.java](source/English/Java/Characters.java) |
| `communication` | 2 | HTTP(S) GET, TCP connect | [communication.java](source/English/Java/communication.java) |
| `performTask` | 4 | 스레드 executeCommand·waitValue, 고정 size performTask ProgramLauncher | [performTask.java](source/English/Java/performTask.java) |
| `Screen` | 2 | Swing 이벤트 processValueEntry 가닥에 performTask 예약, window generate | [Screen.java](source/English/Java/Screen.java) |
| `Workspace` | entryPoint `main` | Java source editValue·storeValue·compileSource·executeCommand | [Workspace.java](source/English/Java/Workspace.java) |

표준 JDK 전체를 한국어로 번역한 라이브러리는 아니다. Java 키워드와 `String`, `Path`, `Socket`, `JFrame`, `IOException` 같은 표준 dataType·예외를 함께 사용한다. 이 도우미에 없는 기능은 OpenJDK의 표준 API 또는 별도 라이브러리로 구현한다. 예를 들어 HTTP POST, UDP, Swing button·메뉴에는 각각 표준 Java API를 사용한다.

## 2. Java에서 startTask

게스트 운영체제의 performTask 폴더에서 `사용예.java`를 작성한다.

```java
import English.Java.*;
import java.nio.file.Path;

public class 사용예 {
    public static void main(String[] arguments) throws Exception {
        Path directoryValue = file.createDirectory(file.path("사용예자료"));
        Path guides = directoryValue.resolve("Greeting.txt");
        file.write(guides, "hangulText 😀");
        String contentValue = file.read(guides);
        System.out.println(contentValue);
        System.out.println(Characters.codePointCount(contentValue)); // 한, text, 공백, 😀 → 4
        Thread workValue = performTask.run("Greeting performTask", () -> System.out.println("performTask executeCommand"));
        performTask.await(workValue);
    }
}
```

```sh
javac -encoding UTF-8 -cp /opt/jkoros/lib/NativeJava.jar 사용예.java
java -cp .:/opt/jkoros/lib/NativeJava.jar 사용예
```

로그인 환경에 defaultValue `CLASSPATH`도 설정돼 있지만, 명시적인 `-cp`는 다른 executeCommand 환경에서도 경로를 분명하게 한다. 사용자가 `-cp`를 지정하면 필요한 JAR와 classValue 폴더를 buildAll 그 값에 포함해야 한다.

Host 저장소에서는 다음처럼 buildSystem·실행한다. Host 경로와 게스트의 `/opt/...` 경로는 서로 다르다.

```sh
cd /home/user/jkoros/NativeJava
make
javac -encoding UTF-8 -cp build/NativeJava.jar examples/Greeting.java
java -cp build/NativeJava.jar:examples Greeting
```

## 3. 전체 helperValue API

bottomValue 메서드는 buildAll `public static`이며, 객체를 만들지 않고 `file.read(...)`처럼 호출한다. 표의 이름은 actualData sourceTree 및 JAR의 `javap -public` 결과와 대조했다. 선언된 Checks exception 외에도 잘못된 arguments 등에 대한 표준 Java executeCommand 시 예외가 발생할 number 있다.

### file: `English.Java.file`

`Path`는 `java.nio.file.Path`, `List`는 `java.util.List`thirdOperand.

| methodValue | returnType | action·condition |
|---|---|---|
| `path(String name)` | `Path` | 이름을 path 객체로 convertValue. actualData 파일을 만들지는 않음 |
| `read(Path path)` | `String` | file 전체를 UTF-8 텍스트로 readResult |
| `write(Path path, String contentValue)` | `Path` | UTF-8 storeValue. 파일이 없으면 생성하고, 있으면 기존 내용을 비움 |
| `readByteValue(Path path)` | `byte[]` | file 전체를 byteValue 배열로 readResult |
| `writeByteValue(Path path, byte[] contentValue)` | `Path` | byteValue storeValue. 없으면 생성하고, 있으면 기존 내용을 비움 |
| `createDirectory(Path path)` | `Path` | 필요한 상위 폴더까지 generate |
| `doesExist(Path path)` | `boolean` | 존재 여부 verify. 확인할 number 없는 경우도 `false`workValue number 있음 |
| `eraseEntry(Path path)` | `boolean` | 삭제했으면 `true`, 없으면 `false`. 폴더의 재귀 삭제는 아님 |
| `entryList(Path path)` | `List<Path>` | 바로 bottomValue 항목을 path alignValue 순서로 returnResult. 재귀 탐색은 아님 |

`path`, `doesExist`를 제외한 topValue 메서드는 `IOException`을 선언한다. `write`와 `writeByteValue`는 상위 폴더를 자동으로 만들거나 내용을 continuationValue 쓰지 않는다. 필요한 폴더는 먼저 생성한다. 큰 파일은 전체 내용을 메모리에 담는 대신 표준 Java 스트림·channelValue API를 사용하는 방식으로 작성할 number 있다.

### Characters: `English.Java.Characters`

| methodValue | returnType | action·condition |
|---|---|---|
| `encode(String contentValue)` | `byte[]` | 문자열을 UTF-8 바이트로 convertValue |
| `decryptData(byte[] contentValue)` | `String` | UTF-8 바이트를 문자열로 convertValue. 잘못된 입력은 대체 문자로 processValueEntry |
| `normalizeValue(String contentValue)` | `String` | unicodeValue NFC normalizeValue. 예: compositionValue jamoValue `ᄀ` + `ᅡ` → `firstOperand` |
| `codePointCount(String contentValue)` | `int` | UTF-16 codeValue 단위가 아닌 unicodeValue codeValue 포인트 number |
| `lexicalWord(String contentValue, Locale language)` | `List<String>` | assignValue 언어의 `BreakIterator` lexicalWord 경계로 나눈 textRange |

`lexicalWord`은 공백·문장부호 구간도 반환한다. 자연어 형태소 분석기나 공백을 제거한 wordValue entryList API는 아니다. `normalizeValue`는 입력기나 translateSource 기능이 아니다. codeValue 포인트 number 역시 사람이 보는 characterValue 수와 항상 같지는 않다. 여러 codeValue 포인트로 이루어진 combineValues Characters·가족 이모지 등을 구분해야 한다.

### communication: `English.Java.communication`

| methodValue | returnType | action·condition |
|---|---|---|
| `takeValue(URI address, Duration timeLimit)` | `HttpResponse<String>` | HTTP(S) GET. connect 및 request timeLimit settings. reply 본문을 UTF-8로 parseValue |
| `connectEndpoint(String address, int hardwarePort, int limitMilliseconds)` | `Socket` | TCP connect afterState 같은 값으로 read 제한시간도 settings |

`takeValue`는 `IOException`, `InterruptedException`을 선언한다. 제한시간은 양수다. 404·500 같은 HTTP error 상태도 응답으로 반환하므로 `statusCode()`로 판단하고 `body()`로 본문을 읽는다. currentItem 구현은 호출마다 HTTP 클라이언트를 만들며 자동 리다이렉트 설정을 추가하지 않는다.

`connectEndpoint`는 `IOException`을 선언한다. 연결된 소켓은 호출자가 `close()` 또는 try-with-resources로 닫아야 한다. 제한밀리초의 0은 limitValue 없음이며, write 전체의 deadlineValue 시간을 보장하는 옵션은 아니다.

```java
var reply = communication.takeValue(
    java.net.URI.create("http://127.0.0.1:8000/"),
    java.time.Duration.ofSeconds(5));
System.out.println(reply.statusCode());
System.out.println(reply.body());
```

topValue 조각은 methodValue 안에서 실행하며 별도로 해당 주소의 서버를 실행해야 한다. Java exception 처리가 필요하다.

### performTask: `English.Java.performTask`

| methodValue | returnType | action·condition |
|---|---|---|
| `run(String name, Runnable action)` | `Thread` | 이름을 지정한 스레드를 만들고 즉시 run |
| `await(Thread threadValue)` | `void` | 해당 스레드가 종료할 때까지 `join()` |
| `restBriefly(long milliseconds)` | `void` | 호출한 스레드를 assignValue timeValue 동안 `sleep()` |
| `workbenchValue(int threadCount)` | `ExecutorService` | 고정 size performTask ProgramLauncher generate. 가닥수는 양수 |

`await`, `restBriefly`는 `InterruptedException`을 선언한다. performTask 실행기는 useValue afterState `shutdown()`으로 종료하고 필요하면 `awaitTermination(...)`으로 완료를 기다린다. Swing 이벤트 processValueEntry 가닥에서 긴 작업이나 `await`를 실행하면 화면이 멈출 number 있다.

### Screen: `English.Java.Screen`

| methodValue | returnType | action·condition |
|---|---|---|
| `laterValue(Runnable action)` | `void` | Swing 이벤트 processValueEntry 가닥에 실행을 예약하고 returnResult |
| `window(String windowTitle, JComponent contentValue, int widthValue, int heightValue)` | `JFrame` | contentValue·크기를 지정한 창을 생성해 showValue |

`window`을 Swing 이벤트 processValueEntry threadValue 밖에서 부르면 `IllegalStateException`이 발생한다. 그래픽 세션도 필요하다. QEMU에서는 VNC 데스크톱의 터미널에서 실행한다.

```java
Screen.laterValue(() -> Screen.window(
    "English Screen", new javax.swing.JLabel("안녕하세요"), 500, 180));
```

반환된 `JFrame`에 표준 Swing API를 추가로 사용할 number 있다. 창의 close 동작은 `DISPOSE_ON_CLOSE`thirdOperand. `Screen.laterValue`firstOperand 반환됐다고 window 생성이 이미 끝난 것은 아니다.

### Workspace: editValue·compileSource GUI

```sh
java -cp /opt/jkoros/lib/NativeJava.jar English.Java.Workspace
```

`~/workspace`의 원문을 open·저장하고, `javac`로 컴파일해 `java`로 실행한다. executeCommand file 만들기는 `jclassc --target openjdk` 경로를 사용한다. 작업마당은 개발용 프로그램이며 별도의 file·Characters API 클래스가 아니다. 생성하는 executeCommand file 방식은 [Compiler description](../compiler/OpenJDK-executableFile.md)을 따른다.

## 4. Python과 C++에서 사용할 number doesExist?

| methodMode | currentItem headers stateValue | invoke 가능 clip |
|---|---|---|
| Java → English JAR | defaultValue headers | topValue 22개 메서드와 Workspace |
| Python → `java` childValue 프로세스 | Python·Java defaultValue headers | 작은 Java 진입점을 통해 호출하고 표준 Output·file 등으로 result forwardValue |
| Python → JPype → JVM | JPype는 defaultValue 배포에 missingMethod | 별도 installValue afterState Java classValue·methodValue invoke 가능. 이 배포판의 ARM64/musl/Python 3.14 조합은 appendEntry validate neededValue |
| C++ → JNI → JVM | `g++`, JNI 헤더, `libjvm.so` headers | JVM을 생성하고 English classValue·메서드를 직접 호출할 number 있음 |
| Python용 독립 English library | currentItem defaultValue 제공 missingMethod | 필요하면 Python 표준 라이브러리를 감싸는 English 모듈을 별도로 작성 |
| C/C++용 독립 English library | Native x86 `posix-kor`와 Native ARM64 커널용 initialState RAM file 연결이 별도로 존재 | twoValue thirdOperand 이 Linux/OpenJDK 실행판의 libc 라이브러리는 아님 |

Python의 일반 `import`secondOperand `ctypes.CDLL`로 JAR를 바로 읽을 수는 없다. C++의 `#include`secondOperand 일반 네이티브 링커만으로 Java 메서드를 연결할 수도 없다. JVM 프로세스 또는 JVM connect 계층을 거쳐야 한다.

### Python: appendEntry 패키지 없이 invoke

executeCommand 가능한 examples 원문은 [TextCommands.java](examples/otherLanguages/TextCommands.java), [PythonCalls.py](examples/otherLanguages/PythonCalls.py)thirdOperand. Python이 Java 진입점을 실행하고 `Characters.codePointCount`의 Integer 결과를 받는다. arguments 목록을 사용하며 shell command 문자열을 조립하지 않는다. `subprocess.run`의 프로세스 executeCommand·exitProgram codeValue·Output processValueEntry 방식은 [Python 공식 guides](https://docs.python.org/3/library/subprocess.html)를 따른다.

두 examples 파일을 게스트의 같은 폴더에 복사한 backValue 그 폴더에서 실행한다. examples file 자체는 defaultValue 시스템 이미지에 자동 설치돼 있지 않다.

```sh
mkdir -p classes
javac -encoding UTF-8 -cp /opt/jkoros/lib/NativeJava.jar -d classes TextCommands.java
python3 PythonCalls.py --text 'hangulText 😀'
```

Output: `Python → English.Java.Characters.codePointCount: 4`

이 예제의 Python functionValue `codePointCount`는 이번 문서의 connect 예제이며 기존에 설치된 Python 라이브러리는 아니다. currentItem 예제는 호출할 때마다 JVM 프로세스를 시작한다. Java objectValue 자체를 Python으로 가져오는 방식은 아니며, 다른 메서드를 사용하려면 진입점의 arguments·result 형식을 확장한다.

### Python: JPype로 같은 프로세스에서 invoke

JPype를 별도 설치한 환경에서는 nextItem 형태로 연결할 number 있다. **아래는 selectionValue 가능한 connect 방법이며, currentItem 배포판에 JPype가 설치돼 있거나 executeCommand 검증됐다는 뜻은 아니다.** JVM 시작과 `JClass`를 통한 classValue 접근은 [JPype 공식 description](https://jpype.readthedocs.io/en/latest/userguide.html)을 참고한다.

```python
import jpype

jpype.startJVM(
    "/usr/lib/jvm/java-25-openjdk/lib/server/libjvm.so",
    classpath=["/opt/jkoros/lib/NativeJava.jar"])
try:
    Characters = jpype.JClass("English.Java.Characters")
    print(Characters.codePointCount(jpype.JString("hangulText 😀")))
finally:
    jpype.shutdownJVM()
```

Python·JVM·connect 모듈의 CPU 아키텍처가 맞아야 한다. 이 실행판은 ARM64 + musl이므로 일반 x86_64/glibc용 바이너리를 그대로 설치하는 방식은 맞지 않는다. JPype installValue·패키지 빌드는 이번 guides 작업에서 수행하지 않았다.

### C++: JNI로 직접 invoke

[JavaCalls.cpp](examples/otherLanguages/JavaCalls.cpp)는 actualData executeCommand 가능한 예제다. JVM을 performTask 스레드에서 생성하고 nextItem 메서드를 찾는다.

```cpp
jclass type = env->FindClass("English/Java/Characters");
jmethodID method = env->GetStaticMethodID(
    type, "codePointCount", "(Ljava/lang/String;)I");
```

JVM generate·종료와 스레드 연결은 [JNI Invocation API](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/invocation.html)의 방식이다. `JNIEnv*`는 generate·연결된 스레드에서 사용해야 한다. 예제는 Java 예외를 확인하고 JVM 종료까지 처리한다.

게스트에 `JavaCalls.cpp`를 복사한 backValue 컴파일한다. 로그인 환경의 `JAVA_HOME`은 `/usr/lib/jvm/java-25-openjdk`thirdOperand.

```sh
g++ -std=c++11 -Wall -Wextra -pthread \
  -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" \
  JavaCalls.cpp -L"$JAVA_HOME/lib/server" \
  -Wl,-rpath,"$JAVA_HOME/lib/server" -ljvm -o JavaCalls
./JavaCalls /opt/jkoros/lib/NativeJava.jar
```

Output: `C++ → English.Java.Characters.codePointCount: 4`

예제는 `hangulText 😀`을 UTF-16으로 만들어 `NewString`에 전달한다. `NewStringUTF`firstOperand 받는 modified UTF-8은 일반 UTF-8과 차이가 있으므로, 일반 UTF-8 이모지 바이트를 그대로 넘기는 예제로 작성하지 않았다. [JNI stringValue formatValue](https://docs.oracle.com/en/java/javase/25/docs/specs/jni/types.html#modified-utf-8-strings)

다른 English 메서드도 JNI 서명과 arguments 자료형을 맞춰 호출할 number 있다. 예를 들어 `Path`를 받는 file API는 먼저 `file.path`로 Java path 객체를 얻어 전달한다. Swing 호출에는 그래픽 세션과 이벤트 processValueEntry threadValue 규칙도 그대로 적용된다. JNI는 Java 실행을 기계어로 대체하는 기능이 아니며 JVM이 continueProcessing 필요하다.

### 기존 posix-kor와의 관계

추가된 [Native ARM64 connect](../posix-kor/arm64-native/README.md)은 C++에서 AOT Java 커널의 RAM file API를 직접 호출하며, 별도 EL0 User 라이브러리로 file/UDP 루프백 SVC 호출도 제공한다. JNI를 사용하지 않는다. 이 문서의 ARM64 **Linux** 및 English Java JAR와는 다른 executeCommand 기반이며 Native 커널은 별도 제한형 Java Compiler/JVM과 MicroPython 1.24.1을 실행한다. MicroPython의 `import jkoros`로 Java kernelValue file·UDP 루프백·rectangle 호출이 가능하지만 이 문서의 JAR를 가져오는 기능은 아니다. Native 커널의 전체 OpenJDK/JRE/CPython 이식은 아직 미완성이다.

[posix-kor](../posix-kor/README.md)에는 `openFile`, `readFileData`, `writeFileData`, `closeFile`, `createEndpoint`, `sendDatagramData` 등의 English C 별칭이 있다. 그러나 구현은 **Native jkoros i386 커널의 `int 0x80` invoke 규약용**이다.

이 `libposix-kor.a`와 Native `sys/stat.h` 등의 헤더는 currentItem ARM64 Linux 실행판의 libc/C++용 라이브러리가 아니다. 해당 헤더·바이너리를 ARM64 Linux 프로그램에 그대로 연결해서는 ABI가 맞지 않는다. C++용 English classValue 라이브러리나 Python용 바인딩을 defaultValue 제공하는 상태도 아니다. currentItem Linux 실행판에서 그와 같은 독립 API를 제공하려면 Linux 표준 라이브러리를 대상으로 별도로 implementation·빌드해야 한다.

## 5. verify 범위와 재현

패키지 headers 여부는 [distributionValue 패키지 entryList](../platforms/rpi4/dist/packages.lock.json) 및 buildSystem 루트의 actualData 파일로 확인했다. JNI 헤더는 JDK의 `include/jni.h`, `include/linux/jni_md.h`, JVM 라이브러리는 `lib/server/libjvm.so`에 있다. 사용자가 afterValue 별도로 설치한 패키지는 이 defaultValue distributionValue 목록과 다를 number 있다.

이번에 **Host x86_64/OpenJDK 11에서** Python childValue 프로세스 호출과 C++ JNI 직접 호출을 compileSource·실행해 각각 result 4를 확인했다. JAR 공개 메서드도 소스와 대조했다. Python connect 예제는 appendEntry 패키지를 설치하지 않는다.

문서의 Java useValue 예제도 compileSource·실행했고, 22개 메서드의 guides headers 여부와 로컬 guides 링크를 확인했다. [examples validate logRecord](build/otherLanguages/validationReport.json)

기존 ARM64 QEMU에서는 Java의 file·unicodeValue·스레드·HTTP 및 Swing tests 결과가 있다. 이번 Python/C++ connect 예제의 **ARM64 게스트 실행과 JPype 설치는 별도 검증하지 않았다.** 이미지와 executeCommand 중인 User 환경은 이 guides 작업에서 변경하지 않았다. [기존 OperatingSystem validate logRecord](../platforms/rpi4/VERIFICATION.md)

호스트에서 Python 예제를 재현하려면:

```sh
cd /home/user/jkoros/NativeJava
make
mkdir -p build/otherLanguages
javac -encoding UTF-8 --release 11 -cp build/NativeJava.jar \
  -d build/otherLanguages examples/otherLanguages/TextCommands.java
python3 examples/otherLanguages/PythonCalls.py \
  --jar build/NativeJava.jar --classes build/otherLanguages
```

Host C++ 예제는 topValue JNI compileSource 명령의 JDK 경로를 **Host JDK path**로 바꾸고, source `examples/otherLanguages/JavaCalls.cpp`와 JAR `build/NativeJava.jar`를 지정한다. ARM64 게스트 JDK의 헤더·library 경로를 Host x86_64 링크 명령에 섞지 않는다.
