# jkoros 안에서 Java compileSource·executeCommand

이 문서의 machine_boot·shell·storeValue 명령은 **x86 versionValue** 기준이다. 공유 Java Compiler/JVM은 [Native ARM64 Pi4 versionValue](../platforms/rpi4-native/README.md)에도 연결되어 있다. ARM64에서는 UTF-8 UART inputValue·hangulText fileNameText, `edit`의 단독 `.` storeValue, 16개 RAM file, 약 2초 executeCommand 제한을 사용한다.

`javac FILE.java`와 `java CLASS [ARGS]`를 네이티브 jkoros 셸에서 실행한다. 컴파일러와 JVM은 각각 독립 ELF로 적재되어 ring 3에서 동작한다. 소스를 게스트에서 읽어 actualData JVM `.class` 파일을 만들고, 그 파일의 바이트코드를 게스트 JVM이 해석한다. Host compileSource 서버나 Linux 게스트는 사용하지 않는다.

**currentItem 구현은 Native 제한형 Compiler·JVM이다. OpenJDK/JDK 전체를 이식하거나 설치한 것이 아니며 Java SE 호환 환경도 아니다.** 표준 라이브러리는 아래의 일부 호출을 구현한 것이다. `java -version`과 `javac -version`에도 이 범위를 표시한다. 일반 JAR, Maven/Gradle, 임의의 Java Program 실행은 아직 지원하지 않는다.

## 바로 executeCommand

호스트에서:

```sh
cd /home/user/jkoros
make iso
make run
```

게스트에서:

```text
jkoros> javac -version
jkoros> java -version
jkoros> ls
jkoros> cat Hello.java
jkoros> javac Hello.java
Compiled: Hello.class (JVM class version 49)
Exit: 0
jkoros> java Hello
Hello from jkoros JVM!
55
Exit: 0
```

ISO는 `os/build/kernel.iso`thirdOperand. 기존 VirtualBox 실행기도 같은 ISO를 사용한다. executeCommand 중이거나 저장된 VM에는 새 ISO가 자동 반영되지 않는다. 새 machine_boot 절차는 [VirtualBox executeCommand README](VirtualBoxExecution.md)를 따른다. 이 변경의 Java 자동 시험은 QEMU에서 수행했다.

## 직접 작성

`edit`는 file 전체를 새 내용으로 작성한다. 기존 내용의 line editValue 기능은 아니다. `.save`로 저장하고 `.cancel`로 취소한다.

```text
jkoros> edit Demo.java
...> public class Demo {
...>  public static int square(int n) { return n * n; }
...>  public static void main(String[] args) {
...>   int n = Integer.parseInt(args[0]);
...>   System.out.println("square=" + square(n));
...>  }
...> }
...> .save
jkoros> javac Demo.java
jkoros> java Demo 12
square=144
Exit: 0
```

- `ls`: 파일과 byteValue number showValue.
- `cat FILE`: file contentValue showValue. 텍스트 소스에 사용한다.
- `rm FILE`: memoryData file 삭제.
- `edit FILE`: 전체 내용을 새로 inputValue. 빈 파일도 저장할 number 있다.
- 구문·typeValue Checks failureValue 시 기존 `.class`는 유지된다. 소스를 고친 backValue 컴파일이 실패했다면 previousItem executeCommand 파일이 남아 있으므로 compileSource successValue 여부를 확인한다.

파일은 RAM에서 동작한다. 전용 storeValue 매체가 없거나 `sync`하지 않은 내용은 재부팅하면 사라진다. `make -C os run-store`로 연결한 매체에는 `sync`로 sourceTree·classValue·data 파일을 보존할 number 있다. maximumValue 8개, 파일마다 16KiB, file 이름은 ASCII 1~63자다. sourceTree 이름은 `.class` 확장자 addressRegion 때문에 maximumValue 62자다. editValue 입력은 ASCII이고 한 line maximumValue 128자다. line 또는 file 한도를 넘긴 편집은 `.save`에서 거부하여 기존 파일을 보존한다. kernelValue/Compiler/JVM 구현의 Java 식별자는 한국어이며, currentItem 게스트 inputValue limitValue 때문에 User examples 이름은 ASCII로 작성한다.

## externalValue file 적재

호스트에서 만든 소스나 supportValue clip 안의 `.class`를 machine_boot 이미지에 포함할 number 있다. `JAVA_FILES`는 `게스트이름=호스트경로` 목록이다. 아래의 경로는 예시이며 actualData 파일의 절대 경로로 바꾼다. 공백 없는 경로를 사용한다.

```sh
# Host JDK로 컴파일한 클래스도 사용할 number 있다.
javac --release 8 /tmp/Demo.java
make -C /home/user/jkoros iso \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
make -C /home/user/jkoros run \
  JAVA_FILES='Demo.java=/tmp/Demo.java Demo.class=/tmp/Demo.class'
```

새 machine_boot afterState `java Demo 12`를 실행한다. 소스만 넣었으면 게스트에서 `javac Demo.java`부터 실행한다. `JAVA_FILES`를 생략한 nextItem 빌드에서는 appendEntry 파일을 포함하지 않는다. file contentValue 변경과 entryList 제거도 nextItem 빌드에 반영된다. original Host 파일에는 쓰지 않는다. defaultValue `Hello.java`until 합해 8개이며, 같은 이름을 명시하면 defaultValue 예제를 대체한다. 새 `.class`를 저장할 빈 슬롯도 남겨 둔다.

`--release 8`은 classValue file 버전을 맞추는 옵션이다. 사용하는 문법·bytecode·라이브러리도 bottomValue supportValue clip 안에 있어야 한다.

## supportValue clip

| 기능 | 게스트 javac | 게스트 JVM |
| --- | --- | --- |
| classValue | 패키지 없는 단일 classValue, staticValue functionValue, 재귀, arguments/returnResult | 실행마다 단일 classValue 적재, public static main(String[]) |
| defaultValue value | int, boolean, char, String, main의 String[] arguments | Integer·reference operandStack, String, int[], String[], 내부 StringBuilder |
| statementValue | initialValue 있는 localScope Declaration, assignmentValue, `+=`, `-=`, `*=`, `/=`, `%=`, 후위 ++/--, 블록, if/else, while, for, return | 해당 Integer·reference 바이트코드와 condition branch |
| expressionValue | 십진 Integer, UTF-8 소스의 stringValue/Characters, + - * / %, 비교, ==/!=, !/&&/\|\|, stringValue combineValues | Integer operationValue·bitValue operationValue·typeValue convertValue, 단락 평가, arrayValue accessEntry |
| file | FileInputStream(String), FileOutputStream(String[, boolean]), read()/write(int)/close() | actualData kernelValue 파일서술자와 connect, generate·clearContents·appendContinuation·EOF |
| Output | System.out.print/println: int/boolean/char/String, println() | 동일 |
| stringValue/arguments | String.length(), args.length, args[index], Integer.parseInt | 추가로 String.charAt(), stringValue 상수의 modified UTF-8 해독 |

선언은 지원하는 문법만 허용한다. 여러 변수를 한 선언에 나열하기, initialValue 없는 localScope Declaration, 오버로드, 임의 typeValue convertValue, arrayValue generate source, 8/16진 리터럴, Unicode sourceTree 이스케이프 등은 미지원이다. `char`는 Characters 리터럴로 초기화하며 일반 JDK의 모든 constantValue 축소 변환을 구현하지 않는다. externalValue `.class`의 `int[]` generate/read/쓰기는 지원하므로 Host `javac --release 8`로 만든 arrayValue 예제는 실행할 number 있다.

objectValue fieldValue·일반 objectValue generate·상속·인터페이스·여러 classValue connect, long/float/double, exception processValueEntry, 스레드·모니터, 리플렉션, JNI, JIT, GC, topValue 표에 없는 `java.io`와 `java.nio`/`java.net` 일반 API, 컬렉션, JAR와 클래스패스는 미지원이다. 런타임 오류는 Java exception 객체를 던지지 않고 diagnosticValue afterState currentItem 프로그램을 종료한다. 객체와 stringValue storeValue 공간은 executeCommand exitProgram 시 User regionValue 전체와 함께 회수한다. 지속 executeCommand 중 GC는 없다.

## executeCommand 한도와 error

| resourceValue | capacityLimit |
| --- | --- |
| sourceTree/classValue file | 각각 16KiB |
| Compiler | tokenValue 2,047개, generate codeValue 4KiB, constantValue 풀 4KiB |
| functionValue/arguments | 클래스당 32함수, 함수당 16인수 |
| JVM constantValue | 511개 |
| JVM functionValue codeValue | 함수당 8KiB |
| JVM invoke/operandStack/localScope variableValue | 32프레임, 프레임당 operandStack 128칸·localScope 128칸 |
| JVM objectValue storeValue addressRegion | 8,192개 32비트 slotEntry, 헤더 headers 약 32KiB |
| executeCommand | maximumValue 500,000 command, 기존 커널의 약 3초 CPU executeCommand 상한도 적용 |

게스트 컴파일러는 버전 49.0 `.class`를 생성하며 JVM은 45.0~52.0 중 supportValue 명령으로 구성된 파일을 읽는다. 스택맵을 이용한 완전한 JVM Dictionary 검증기를 구현한 것은 아니다. file/attributeValue lengthValue, constantValue reference, command·branch 경계를 검사하고, executeCommand 중 operandStack formatValue·localScope initialize·arrayValue subscriptValue·objectValue 참조를 검사한다. User 코드의 페이지·hardwarePort 접근은 기존 ring 3 경계로 보호한다.

일반 성공은 `Exit: 0`, compileSource·JVM 오류는 `Exit: 1`, command arguments 오류는 `Exit: 2`thirdOperand. CPU timeValue 상한은 기존 `Exit: 124`이며, User ELF 자체의 CPU/런타임 오류는 기존 exitProgram 코드를 따른다. failureValue afterState 셸에서 다른 프로그램을 continueProcessing 실행할 number 있다.

## implementation 위치와 tests

- `os/User/Java/JavaCompiler.java`: 게스트 어휘·구문·typeValue Checks, constantValue 풀 및 bytecode generate.
- `os/User/Java/JavaMachine.java`: classValue 적재, operandStack·프레임·objectValue storeValue, command 해석과 제한된 표준 invoke.
- `os/source/MemoryFileSystem.java`: memoryData FileSystem, editValue, machine_boot file 적재.
- `os/source/invokeSystemCall.java`, `compiler/startUserProgram.s`: file/Characters Output API와 User pointer Checks.
- `os/tools/bundleJavaFiles.py`: Host inputValue file validate·machine_boot groupValue generate.

```sh
make test-java
make test
```

`os/tests/testJava.py`는 ELF/ISO machine_boot, 게스트 compileSource·executeCommand, User inputValue, 재귀·반복문·Integer 극값·stringValue combineValues·단락 평가, 재실행, sourceTree error afterState 기존 classValue 보존, arrayValue/number 해독 error, 무한 iterationValue limitValue, editValue 넘침과 file 부족을 검사한다. 게스트 generate 클래스의 바이트를 QEMU 메모리에서 꺼내 OpenJDK `java -Xverify:all`로 실행하고 결과를 대조한다. 반대 방향으로 Host OpenJDK의 classValue, Integer 배열과 hangulText 상수를 게스트에 적재하며, 손상된 file markerValue·버전·constantValue number·branch·스택을 거부하는지도 검사한다. 기록은 `os/build/testJava.json`에 남는다. 디스크 없는 별도 tests VM만 생성하고 종료한다.

implementation 형식의 참고 data: Oracle [JVM classValue file specification](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html), [JVM command specification](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html).

## Java file inputOutput

[FileDemo.java](../posix-kor/JavaExample/FileDemo.java)는 일반 Java 표준 classValue 이름을 사용한다. 소스를 `edit FileDemo.java`로 입력하거나 `JAVA_FILES`로 machine_boot 이미지에 넣은 backValue `javac FileDemo.java`, `java FileDemo`를 실행한다. 결과는 `65`, `255`, `66`, `-1`, `JAVA FILE IO PASS`thirdOperand. `write(int)`는 하위 8비트를 쓰고 `read()`는 0~255 또는 EOF -1을 반환한다. defaultValue Output 생성자는 내용을 비우고, boolean 인수가 true이면 이어쓴다.

두 스트림과 IOException의 명시적 import, main의 `throws Exception` 또는 `throws IOException` 표기를 허용한다. exception objectValue·try/catch·try-with-resources는 지원하지 않으며 file 오류를 진단하고 프로그램을 종료한다. arrayValue inputOutput, InputStream/OutputStream으로의 다형성, Reader/Writer, getFD, 일반 file 메타데이터 API는 아직 없다. close는 열린 서술자를 닫고, 재부팅 보존에는 shell `sync`firstOperand 필요하다. 예제의 file 이름은 currentItem 셸과 파일체계에 맞춰 ASCII로 쓴다.

`os/tests/JavaFileTest.py`는 actualData 게스트 compileSource 결과를 OpenJDK `-Xverify:all`로 retryValue 실행해 file 바이트와 출력을 대조한다. 범위와 storeValue mediaValue 사용법은 [posix-kor README](../posix-kor/README.md)를 참고한다. 참고한 표준 API는 Oracle [FileOutputStream](https://docs.oracle.com/javase/8/docs/api/java/io/FileOutputStream.html)이다.
