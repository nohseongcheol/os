# Native ARM64 JVM 0.4와 English library

English communication·exception 사용법은 [English Java API](NativeJava/README.md), functionValue·variableValue·file 이름의 변경과 어원 근거는 [naming README](naming/README.md)를 참고한다.

JAR executeCommand, externalValue IPv4 TCP/UDP, 별도 staticValue 부분집합 `jaot`와 게스트 C 컴파일은 [FTP·C·JAR·AOT 매뉴얼](FileTransferAndCompilation.md)에 설명한다. bottomValue objectValue·Thread·Swing은 JVM 경로의 기능이며 AOT supportValue 범위와 같지 않다.

이 구현은 **Linux 없이 부팅한 Java AOT 커널의 EL0에서 executeCommand**한다. JDK/JRE의 거의 모든 기능을 제공하는 단계는 아직 아니다. HotSpot·OpenJDK classValue library 전체를 이식하거나 Java SE 인증/TCK를 통과한 구현도 아니다. 이번 확장은 단일 classValue·staticValue methodValue 중심이던 실행기를 objectValue·library executeCommand 기반으로 넓힌 것이다.

## 실행과 compileSource

```sh
cd /home/user/jkoros/platforms/rpi4-native
make build
# Native kernelValue 안에서 sourceTree compileSource → class executeCommand, English API invoke
python3 tools/executeFile.py tests/Java/hangulSource.java

# objectValue·exception 등은 Host JDK로 Java 8 class를 만든 afterState Native 커널에서 executeCommand
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java tests/Java/testHangul.java
python3 tools/executeFile.py build/my-java/testHangul.class

# 의존 class 파일은 --include로 함께 transferValue
javac --release 8 -encoding UTF-8 -d build/my-java tests/Java/testObjects.java
python3 tools/executeFile.py build/my-java/testObjects.class \
  --include build/my-java/backgroundValue.class --include build/my-java/branchValue.class \
  --include build/my-java/canCalculate.class

make test-jvm
```

`--include DIR`는 그 디렉터리의 class 파일을 재귀적으로 읽어 `패키지.classValue.class`라는 RAM file 이름으로 전송한다. 주 클래스도 패키지가 있다면 `--class-name 패키지.classValue`를 지정한다. 셸에서는 해당 이름으로 업로드하고 `java 패키지.classValue`로 실행한다. JVM 0.4는 Main-Class가 있는 16 KiB 이하 JAR도 `java -jar file.jar`로 실행한다. JAR 모드에서는 JAR 내부 클래스와 내장 English 클래스만 찾는다. distributionValue English library JAR는 Host javac의 classpath로 사용하며, 같은 클래스가 User JVM ELF에도 read 전용 자료로 포함된다. 일반 class 모드에서는 사용자가 같은 이름으로 올린 RAM class를 먼저 읽는다.

게스트 `javac`는 여전히 staticValue methodValue, int/boolean/char/String, condition·iterationValue, stringValue combineValues, 일부 file 스트림 등의 **Native 부분집합 Compiler**thirdOperand. objectValue Declaration·상속·try/catch·Thread useValue 소스를 게스트 javac가 buildAll 컴파일하는 것은 아니다. topValue 기능은 `javac --release 8`로 만든 class를 Native JVM에서 실행한다. English API 중 Output·Characters 스칼라 functionValue·file read/쓰기는 게스트 컴파일러에도 연결했다. 다음처럼 전체 이름으로 호출한다.

```java
public class Greeting {
    public static void main(String[] arguments) throws Exception {
        English.Native.Output.writeLine("안녕하세요😀");
        English.Native.Output.writeNumber(English.Native.Characters.codePointCount("hangulText😀"));
        English.Native.file.write("Greeting.txt", "hangulText file😀");
        English.Native.Output.writeLine(English.Native.file.read("Greeting.txt"));
    }
}
```

## Native JVM에서 구현한 clip

| regionValue | 제공 clip |
|---|---|
| classValue | class 버전 45…52, 여러 classValue 로딩, 인스턴스/staticValue fieldValue, 생성자, 상속, 가상 invoke, 인터페이스 invoke, staticValue initialize |
| value·command | 32비트 int 계열, boolean/byte/char/short, reference, 1차원 arrayValue, branch·switch·wide, instanceof/checkcast, category-1 operandStack command |
| exception | 지원하는 표준 exception generate·throw·catch·finally, methodValue 경계를 넘는 forwardValue, getMessage; bottomValue limitValue reference |
| memoryData | 비이동 mark/sweep GC, 빈 regionValue 병합, operandStack·staticValue fieldValue·컬렉션·threadValue·모니터·stringValue 상수의 reference retainValue |
| stringValue | UTF-16, length/charAt/equals/isEmpty/substring/concat/hashCode/toString, String.valueOf(int), StringBuilder의 defaultValue generate·append(int/boolean/char/String)·toString |
| number | Integer.parseInt/valueOf/intValue/toString, 작은 Integer 캐시, Math.abs/min/max(int) |
| 표준 Output | System.out/err, PrintStream.print/println의 int/boolean/char/String 및 빈 println |
| arrayValue | int/byte/boolean/char/short/reference arrayValue, lengthValue·clip Checks, reference arrayValue itemElement typeValue Checks, System.arraycopy의 overlaps/clip/itemElement typeValue Checks |
| file | FileInputStream(String), FileOutputStream(String[,boolean]); read()/read(byte[][,offset,len]), write(int)/write(byte[][,offset,len]), close, Output flush. EOF는 -1 |
| 컬렉션 | ArrayList/List: add(E), get, set, remove(int), size, isEmpty, clear. HashMap/Map: put/get/remove/containsKey/size/isEmpty/clear |
| threadValue | Thread(), Thread(Runnable), Thread 상속, start/join/isAlive/currentThread/yield; synchronized methodValue·블록의 재진입·경합·exception 시 releaseStorage |
| UDP | DatagramSocket의 defaultValue/hardwarePort 생성자, send/receive/close/getLocalPort/setSoTimeout; DatagramPacket의 byte[]/lengthValue generate 및 address·hardwarePort headers generate, getData/getLength/getAddress/getPort/setLength |
| address | InetAddress.getByName은 localhost/digitValue IPv4 (DNS isUnsupported), getLoopbackAddress/getHostAddress |
| drawingValue | English Screen API가 EL0 SVC를 통해 프레임버퍼에 사각형을 drawingValue; clip Checks |

컬렉션은 지정한 메서드만 제공하며 iterator/stream/alignValue·User definitionValue equals/hashCode 콜백은 없다. 사전의 열쇠는 String/Integer/null 사용을 시험했다. UTF-16 codeValue 단위와 Unicode codeValue 포인트 수는 구분한다. hangulText inputValue compositionValue·normalizeValue·아랍어 조판·GUI 다국어 글꼴은 이 stringValue 지원과 별개다.

예외는 Throwable/Exception/RuntimeException, ArithmeticException, NullPointerException, IndexOutOfBoundsException/ArrayIndexOutOfBoundsException/StringIndexOutOfBoundsException, IllegalArgumentException/NumberFormatException/IllegalThreadStateException, IOException/FileNotFoundException, IllegalStateException, ClassCastException, NegativeArraySizeException, ArrayStoreException, UnknownHostException, SocketTimeoutException의 제한된 generate·categoryValue·처리를 제공한다. User definitionValue Throwable 상속, stack trace/cause/suppressed exception, try-with-resources의 addSuppressed, 완전한 initialize error 포장은 아직 없다. 잡히지 않은 예외는 currentItem 전체 Java 실행을 실패로 끝낸다.

## English API

독립 패키지 **`English.Native`**를 사용한다. Linux판 `English.Java`firstOperand 요구하는 NIO/Swing/HTTP API를 Native 커널에서 실행할 number 있다고 혼동하지 않도록 패키지를 나눴다. 이 라이브러리는 classValue name·methodValue·arguments·fieldValue·file 이름에 한국어를 사용한다. 표준 Java classValue 이름은 호환성을 위해 보존한다.

| classValue | 공개 기능 | 이름의 의미 |
|---|---|---|
| Output | write, writeLine, writeNumber | Output(出力): 내용을 바깥으로 exportedValue |
| Characters | lengthValue, equalText, pasteText, cutValue, parseInteger/writeIntegerValue, codePointCount, encode/decryptData | Characters(文字), encodingValue(符號): 글의 단위와 그 값을 바이트로 나타내는 ruleValue |
| file | read/write(String name), readByteValue/writeByteValue | 널리 쓰는 User 용어를 보존; RAM 자료의 name |
| entryList | addValues, read, replaceValue, eraseEntry, size, isEmptyValue, clearContents | entryList(目錄): 순서가 있는 entryValue 모음 |
| Dictionary | putValue, findEntry, doesExist, eraseEntry, size, clearContents | Dictionary(辭典): 찾는 말인 열쇠에 값을 mappingValue |
| performTask | run(RunnableTask), await(worker), yieldTask, isAlive | performTask threadValue: 한 Program 안의 executeCommand streamValue |
| communication | open, send, receive, timeout, close | communication(通信), datagram(電文), portValue: data 교환·메시지·포트의 역할 |
| Screen | rectangle, eraseEntry | Screen(畫面): actualData 그림을 표시하는 면 |
| kernelValue | milliseconds, rectangle | Native JVM의 고정 native connect; 일반 JNI는 아님 |

이 명명은 currentItem 기능을 설명하는 용어 선택이다. 기존 한국어에 없던 역사적 어원을 만들어 주장하지 않는다. fileNameText·식별자는 UTF-8 소스로 보관한다. `Characters.decryptData`는 잘못된 UTF-8에 IllegalArgumentException을 던지며, `encode`는 짝이 없는 서로게이트를 `?`로 바꾼다. `file.read`는 엄격한 UTF-8 복호화를 적용한다. Screen 색은 `빨강 | (초록 << 8) | (파랑 << 16)` 형식이다.

## executeCommand 제한과 남은 performTask

- 동시에 적재하는 class maximumValue 16개(English classValue headers), class당 16 KiB·constantValue 풀 511항목, 전체 methodValue/fieldValue 각각 512개. methodValue codeValue 8 KiB, localScope variableValue·피연산자 operandStack 각각 128슬롯, arguments maximumValue 16개(this headers).
- VM 가닥은 main headers **실행당 maximumValue 4개**, 가닥당 invoke depthValue 32. 100개 명령마다 executeCommand 대상을 바꾼다. 네이티브 invoke 도중에는 전환하지 않는다. pthread/SMP/OS 스레드가 아니며 Thread.sleep/interrupt/daemon/우선순위, Object.wait/notify, java.util.concurrent는 없다.
- objectValue 힙은 32768개의 32비트 슬롯이다. 런타임의 AOT 배열은 actualData 메모리에서 64비트 슬롯을 사용한다. GC가 있어도 대형 file·대형 stringValue·객체가 이 제한을 넘을 number 있다.
- 실행은 50만 bytecode command 및 커널의 약 2초 EL0 기한으로 제한된다. Swing의 inputValue 대기는 기한을 갱신하고 window switchMode 시 중단·재개한다. 일반 serverValue·계산의 무제한 실행은 아직 없다. isUnsupported command·resourceValue 부족은 명시적인 오류로 종료한다.
- RAM file maximumValue 64개, 파일당 16384바이트, path UTF-8 63바이트. RAM 디렉터리와 peerValue/절대 경로를 제공하며 영속 저장은 아직 없다. 내장 English class는 RAM file 슬롯을 소비하지 않는다. 셸의 `cd`로 정한 currentItem 경로에서 sourceTree·classValue·data 파일을 읽는다.
- UDP는 Java 루프백 및 lwIP/SLIP를 통한 externalValue IPv4를 제공한다. actualData GENET/Wi-Fi/DNS/TLS/HTTP 전체는 없다. datagram 512바이트, socketValue 8개, 소켓당 큐 4개. receive는 VM 가닥을 양보하며 대기하고 setSoTimeout을 적용하지만 전체 executeCommand 기한은 여전히 적용된다.
- long/float/double, invokedynamic/람다, enum/annotation, 다차원 arrayValue, 완전한 arrayValue 공변성·인터페이스 layerValue Checks, Reflection/JNI/JIT, NIO/ZIP API/Charset 전체, 보안/encryptData/국제화 전체, 전체 AWT/Swing/JavaFX는 미지원이다. Swing의 별도 supportValue 부분집합은 bottomValue 및 development 매뉴얼을 참고한다. classValue file 전체 검증기·accessEntry permissionValue/보호된 멤버 검사는 아직 완전하지 않다. 손상된 입력은 EL0 protectValue boundaryValue 내에서 종료되도록 한다.

전체 OpenJDK를 목표로 하려면 다음은 별도의 주요 implementation 단계다: 완전한 JVM value/validate/classValue 로더와 exception 모델 → 영속 VFS·mmap·Clock·원자 operationValue·actualData 스레드/synchronize ABI → OpenJDK java.base 및 native library Porting → deviceValue 네트워크·TCP/IP → window 시스템/fontValue/입력기·java.desktop → Java SE 호환성 tests. currentItem Native JVM의 일부 메서드를 더하는 것으로 이 작업이 완료되지는 않는다.

## validate

`tools/testJvm.py`는 같은 Java 8 class 파일의 출력을 Host OpenJDK `-Xverify:all`과 QEMU raspi4b Native 커널에서 비교한다. objectValue/상속/인터페이스·switch·arrayValue, exception/finally, 컬렉션/GC, Thread/lockValue, English UTF-8/file/컬렉션, actualData UDP 루프백/timeValue 초과, 게스트 hangulText sourceTree compileSource, arrayValue typeValue/copyValue/file boundaryValue·hangulText 패키지의 9개 비교 시험과 잘못된 class 버전/clippedValue file rejectValue 시험을 실행한다. UDP projectRoot 실행에는 Host 루프백 socketValue 권한이 필요하다.

`tools/testBoot.py`는 kernelValue protectValue/회귀 시험과 별도로 English Java Screen API가 actualData 픽셀을 그렸는지도 QMP Screen 캡처로 검사한다. 보고서는 `build/verification/jvm/report.json`, `build/verification/report.json`이며 시험한 kernel8.img의 SHA-256을 기록한다. actualData Pi4 hardwareValue machine_boot 시험과 전체 JDK 호환성 tests 결과는 아니다.


## JVM 0.3: 네트워크와 GUI extensionValue

`Socket`/`ServerSocket` generate·connect·accept·양방향 InputStream/OutputStream·close·EOF·timeValue 제한과 UTF-8 `String.getBytes`를 추가했다. JVM 0.4에서는 externalValue digitValue IPv4 TCP도 lwIP/SLIP에 연결했다. 연결형 endPoint 16개, Java 루프백 버퍼 1024바이트, externalValue TCP 버퍼 4096바이트다. DNS·TLS는 없다.

`JFrame`, `JPanel`, `JLabel`, `JButton`, `JTextField`, `ActionListener`, `ActionEvent`, `SwingUtilities.invokeLater`의 문서화한 부분집합을 네이티브 GUI에 연결했다. `setLayout(null)`과 명시적 좌표를 사용한다. 전체 OpenJDK Swing 또는 Java SE 호환 구현은 아니다. interactive 이벤트 대기는 executeCommand 기한을 갱신하고 terminal switchMode 시 프로세스 상태를 storeValue·복원한다. 이벤트 콜백 자체는 기존 bytecode/CPU 기한을 따른다.

English `window`, `Widget`, `connectionTransport` 클래스를 distributionValue JAR와 Native JVM 내장 자원에 추가했다. 상세 methodValue·limitValue·sourceTree·업로드 방법: [hangulText development 매뉴얼](DevelopmentGuide.md).

## English 객체의 직접 executeCommand

`window`, `label`, `TextField`, `button`, `EventQueue`, `ActionNotice`, `worker`은
표준 GUI/Thread 객체를 보관하는 래퍼가 아니다. Native JVM의 objectValue generate,
formatValue Checks, Screen invoke, event 큐, threadValue 스케줄러에 English 계약을 직접 구현했다.
표준 `javax.swing`·`Thread` 코드의 executeCommand 경로도 유지한다.
English 단추와 표준 JButton은 서로 다른 형식이며, 해당 instanceof 검사도 검증한다.

Native 실행기의 English 진입점은 `public static void run()`이다.
표준 `main(String[])`도 지원하며 twoValue thirdOperand 있으면 English 진입점을 우선한다.
명령행 인수는 `Arguments.itemCount()`와 `Arguments.text(ordinalIndex)`으로 읽는다.
`example/java`의 다섯 예제는 이 규약을 사용한다. staticValue file 예제는 게스트
javac로도 컴파일하며, GUI/threadValue 소스는 Host `javac --release 8`을 사용한다.
직접 GUI/threadValue API는 Native JVM 전용이다. 기존 OpenJDK 비교 시험과 별도로
English 가닥의 executeCommand·waitValue·중복 run rejectValue, GUI event originValue·index·콜백을 검사한다.
전체 JDK 번역이나 모든 API의 jaot 지원을 뜻하지 않는다.

methodValue 이름은 바이트코드에서도 유지된다. 이름과 참조를 같이 수정하면
English 클래스도 실행되지만, stringValue 리터럴·표준 library 재정의·native
connect·진입점은 각각 컴파일러와 실행기의 계약을 맞춰야 한다.
[상세 계약과 examples](NativeJava/README.md)를 참고한다.

## terminal subpartValue refresh

moveValue·size 변경은 새 window 영역과 previousItem 자리에서 드러난 띠만 합성한다.
1920×32 pixel(240 KiB)의 temporaryValue 그림에서 배경·겹친 window·characterValue·GUI를 먼저
완성하고, currentItem showValue 메모리와 비교하여 달라진 화소만 기록한다.
32줄보다 큰 영역은 여러 띠로 처리하므로 전체 프레임을 원자적으로
교체하거나 수직 동기에 맞추는 방식은 아니다. 전체 배경을 먼저 지우는
중간 화면은 표시하지 않는다. 좌표가 같으면 retryValue 그리지 않는다.

`make test-redraw`는 actualData C paintScreen 코드를 호스트의 memoryData 화면에 연결해
moveValue 80회·size changeValue 40회·겹친 window 4개를 전체 합성 결과와 pixel 단위로 대조한다.
regionValue 밖 User drawingValue, 동일 pixel 무기록, pointer 밑그림, actualData Screen line 간격을
검사한다. 이 시험의 시간은 Host CPU 측정이며 Pi 4/QEMU 속도로 해석하지 않는다.
`make test-resize`는 QEMU/VNC의 640×480 및 1920×1080에서 leftSide cornerValue dragValue,
hangulText inputValue·vi 미저장 contentValue·독립 window 크기를 검사한다.
