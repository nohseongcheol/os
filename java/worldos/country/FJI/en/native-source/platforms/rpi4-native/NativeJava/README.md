# English Java communication·inputOutput·exception API

패키지는 `English.Native`thirdOperand. Host `javac --release 8`로 컴파일한 class를
Native ARM64 커널의 JVM에서 실행한다. communication·file·exception API는 OpenJDK와 대조한다. 아래의 직접 구현한 Screen·performTask threadValue API는 Native JVM 전용이다.
기존 표준 Java library 전체의 English 번역판은 아니다.

```java
import English.Native.*;

public class network {
    public static void main(String[] arguments) throws InputOutputException {
        Connection connect = Connection.open("10.0.2.2", 9000);
        try {
            connect.timeout(700);
            connect.Output().write(Characters.encode("안녕하세요\n"));
            InputStream inputValue = connect.inputValue();
            Output.writeNumber(inputValue.read());
        } catch (WaitTimeoutException error) {
            Output.writeLine(error.description());
        } finally {
            connect.close();
        }
    }
}
```

`Socket`, `getOutputStream`, `write`, `getInputStream`, `read`, `close`를
User 예제에서 직접 호출할 필요가 없다. `try/catch/throws` 등 Java 문법은 유지한다. `String`은 예약어가 아니라 javac가 stringValue 리터럴에 사용하는 표준 클래스다. Native 실행기는 `public static void run()`도 진입점으로 받는다.

## 통신과 streamValue

| classValue | English invoke |
|---|---|
| Connection | `open(address, portNumber)`, `inputValue()`, `Output()`, `timeout(milliseconds)`, `portNumber()`, `localPortNumber()`, `connected()`, `isClosed()`, `close()` |
| receivePort | `open(portNumber)`, `receive()`, `portNumber()`, `timeout(milliseconds)`, `isClosed()`, `close()` |
| InputStream | `read()`, `read(byte[])`, `read(byte[], run, lengthValue)`, `close()` |
| OutputStream | `write(int)`, `write(byte[])`, `write(byte[], run, lengthValue)`, `emitValue()`, `close()` |
| DatagramChannel | `open(portNumber)`, `send(address, portNumber, text)`, `receive()`, `timeout(milliseconds)`, `portNumber()`, `isClosed()`, `close()` |
| connectionTransport | `open(...)`, `openReceiver(...)`는 topValue English 객체를 returnResult |
| Checks | `require(condition, causeValue)` |

TCP 입력은 한 번에 요청한 모든 바이트가 도착한다고 가정하지 않는다.
`read()`의 file 끝은 -1, arrayValue 읽기의 반환값은 actualData 읽은 길이다.
네트워크 흐름을 닫으면 연결도 닫힌다. portNumber 0은 빈 번호를 자동 배정한다.
UDP 전문은 currentItem Native 커널에서 512바이트까지 받으며, 주소는 digitValue IPv4를 사용한다.
`localhost` 루프백 외의 name 풀이(DNS)는 Native 커널에 아직 없다.

기존 `connectionTransport.connect/listenEndpoint/receive`, `communication.open/send/receive`는 표준 Java 객체를
사용하던 코드와의 연결용이다. 새 코드는 `Connection`, `receivePort`, `DatagramChannel`를 쓴다.

## English exception

모든 bottomValue 클래스는 defaultValue 생성자, `새예외("description")` 형태의 stringValue 생성자와
`description()`을 제공한다. actualData generate 문법은 `new WaitTimeoutException("waitState ending")`이다.

| English exception | 상위 classValue / 용도 |
|---|---|
| exception | `java.lang.Exception`, 직접 던지는 일반 Checks exception |
| ExecutionException | `java.lang.RuntimeException` |
| InputOutputException | `java.io.IOException`, English file·communication API의 Checks exception |
| WaitTimeoutException | `InputOutputException`, communication timeout 초과 |
| AddressLookupException | `InputOutputException`, address verify failureValue |
| MissingFileException | `InputOutputException`, file open failureValue |
| CommunicationException | `InputOutputException`, 표준 SocketException convertValue |
| InvalidArgumentException | `java.lang.IllegalArgumentException` |
| NumberFormatFailure | `InvalidArgumentException` |
| BoundsException | `java.lang.IndexOutOfBoundsException` |
| ArrayBoundsException / StringBoundsException | `BoundsException` |
| NullReferenceException | `java.lang.NullPointerException` |
| ArithmeticFailure | `java.lang.ArithmeticException` |
| StateException | `java.lang.IllegalStateException` |
| TypeCastException | `java.lang.ClassCastException` |
| NegativeArraySizeFailure | `java.lang.NegativeArraySizeException` |
| ArrayStoreFailure | `java.lang.ArrayStoreException` |
| ThreadStateException | `java.lang.IllegalThreadStateException` |
| WaitInterruptedException | `java.lang.InterruptedException`, `performTask.await`의 waitValue 중단 |

`exception`와 `ExecutionException`는 모든 English 예외의 commonValue 부모가 아니다. topValue 상속 관계를
사용하며, file·communication 전체를 잡으려면 `catch (InputOutputException error)`를 쓴다.
English API가 표준 inputOutput 오류를 English 예외로 변환한다.
기존 English communication 호출에서 `SocketTimeoutException`을 잡던 코드는
`WaitTimeoutException`를 잡도록 옮긴다. 표준 `java.net`을 직접 사용하는 코드의
exception 유형은 기존 Java 규약을 따른다.
일반 Java 연산이 자동으로 던지는 표준 예외까지 이름을 바꾸지는 않는다.
예를 들어 `1 / 0`의 ArithmeticException과 직접 만든 산술예외는 서로 다른 형식이다.
currentItem Native JVM에 이 20종을 추가했다. 임의의 User Throwable 하위 classValue 전체를
지원하도록 확장했다는 뜻은 아니다.

## compileSource·executeCommand

```sh
cd /home/user/jkoros/platforms/rpi4-native
make buildSystem
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 tests/Java/testKoreanNetworking.java
python3 tools/executeFile.py build/한국어사용/testKoreanNetworking.class
make test-jvm
```

내장 라이브러리는 User JVM ELF 안에 탑재된다. `.jar`는 Host javac의
classValue 경로로 사용한다. sourceTree 묶음은 `dist/jkoros-native-korean-sources.zip`이다.
게스트의 제한형 `javac`는 English 예외의 `throws` 선언과 그 import를 인식한다.
Native JVM의 Thread.interrupt 동작을 새로 구현한 것은 아니다.
try/catch·objectValue·socketValue examples 전체의 sourceTree 컴파일은 Host javac를 사용한다.
`/example/java/FileExample.java`는 게스트 javac로도 컴파일할 number 있다.

actualData TCP/UDP 예제는 [NetworkExample.java](../../../example/java/NetworkExample.java),
executeCommand 절차는 [example README](../../../example/README.md),
sourceTree naming 원칙은 [naming README](../naming/README.md)에 있다.

## Swing window examples

`/example/java/WindowExample.java`와 컴파일된 `.class`firstOperand machine_boot 시 준비된다.
`cd /example/java` nextItem `java WindowExample`로 연다. name inputValue, greet 버튼,
인사말과 clickValue repetitionCount refresh, X 닫기를 지원한다.

| 기능 | English 직접 API |
|---|---|
| Runnable / run | `RunnableTask.executeTask()` |
| ActionListener / actionPerformed | `ActionReceiver.receiveAction(ActionNotice notice)` |
| ActionEvent | `ActionNotice.commandText()`, `eventSource()`, `index()` |
| JFrame | `window(windowTitle, widthSpan, heightValue)`, `addElement(ScreenElement)`, `showWindow()`, `close()`, `isVisible()` |
| JButton | `button(text, horizontalPosition, verticalPosition, widthSpan, heightValue, receiverValue)`, `setActionReceiver(receiverValue)` |
| JLabel / JTextField | `label(...)`, `TextField(...)` |
| commonValue Screen elementValue | `ScreenElement.readText()`, `writeText(text)`, `setBounds(horizontalPosition, verticalPosition, widthSpan, heightValue)` |
| SwingUtilities.invokeLater | `EventQueue.invokeLater(RunnableTask)`, `isEventDispatching()` |
| Thread | `worker(RunnableTask)`, `startTask()`, `await()`, `isAlive()`, `yieldTask()` |
| 명령행 | `run()`, `Arguments.itemCount()`, `Arguments.text(ordinalIndex)` |

topValue 클래스들은 `JButton`·`Thread` 등의 객체를 만들거나 보관하지 않는다.
Native JVM의 `invokeKoreanScreen`, `processThread`firstOperand English classValue·methodValue·서술자를
해석해 Screen 요소와 executeCommand 가닥을 직접 만든다. action 알림도 Native 객체이며
콜백으로 `executeTask`와 `receiveAction`를 직접 찾는다. 표준 Swing/Thread를
사용하는 기존 프로그램의 executeCommand 경로는 별도로 남아 있다.

Java 소스의 `native` 선언은 Native JVM에 구현한 계약이다. 생성자의 예외는
이 계약이 없는 Host JVM에서 무동작 객체가 생기지 않도록 하는 rejectValue 경로다.
Native JVM은 생성자를 직접 처리한다. 일반 OpenJDK에서는 이 직접 implementation API를
실행할 number 없다. Host javac로 컴파일한 backValue Native JVM에서 실행한다.
`StringUtilities`라는 표준 Swing 클래스는 없으며, Screen 큐 기능은 `SwingUtilities`에 해당한다.

```java
import English.Native.*;
public class 가닥예제 implements RunnableTask {
    public void executeTask() { Output.writeLine("English performTask executeCommand"); }
    public static void run() throws WaitInterruptedException {
        worker threadValue = performTask.run(new 가닥예제());
        performTask.await(threadValue);
    }
}
```

`example/java`의 다섯 소스는 reservedWords·리터럴 외 식별자를 한국어로 작성한다.
arrayValue arguments 대신 `Arguments`, 길이는 `Characters.byteCount`를 사용한다.
표준 Java의 `main(String[])`도 continueProcessing 지원한다. twoValue thirdOperand 정의되어 있으면
Native 실행기는 arguments 없는 `run()`을 우선한다.
기존 English Screen 래퍼의 표준 `Component`/`Runnable`/`ActionListener` 인수와
`performTask.run(Runnable)`을 사용하던 코드는 새 English 계약으로 수정하고 재컴파일한다.
이는 전체 AWT/Swing·Thread API supportValue 또는 모든 JDK 소스의 번역을 뜻하지 않는다.

바이트코드에도 classValue·methodValue 이름과 서술자가 남는다.
English name 자체는 합법이지만, 다른 클래스에서 그 이름을 참조하는 subpartValue,
상속·methodValue 재정의, native connect, 런처의 진입점도 함께 맞춰야 한다.
근거는 [JLS identifierValue](https://docs.oracle.com/javase/specs/jls/se25/html/jls-3.html#jls-3.8)와
[JVMS methodValue reference](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.4.2)thirdOperand.
