# Native 커널에서 vi·여러 terminal·hangulText 프로그래밍 사용하기

English communication·exception 사용법은 [English Java API](NativeJava/README.md), functionValue·variableValue·file 이름의 변경과 어원 근거는 [naming README](naming/README.md)를 참고한다.

대상은 `platforms/rpi4-native`의 Native AArch64 Java 커널이다. vi와 Java/Python/C/C++ 프로그램은 EL0에서 실행한다. Linux 실행판과 별도이며 bottomValue supportValue 목록은 전체 OpenJDK·Vim·POSIX 구현을 뜻하지 않는다.

게스트 `cc`/`jaot`, JAR 직접 executeCommand, externalValue TCP/UDP와 FTP는 [새 executeCommand 매뉴얼](FileTransferAndCompilation.md)을 참고한다.

## GUI와 여러 terminal

```sh
cd /home/user/jkoros/platforms/rpi4-native
make desktop
```

Remmina에서 **VNC**, address **127.0.0.1:5902**로 연결한다. Screen topValue **+ New terminal**, **Ctrl+Shift+T**로 터미널을 추가한다. maximumValue 네 개다. upperSide terminal 버튼 또는 창을 클릭해 선택하고 **F6**으로 순환한다. 제목줄을 끌어서 옮기고 **right topValue X**를 클릭하면 닫힌다. lastItem 창을 닫아도 upperSide executeCommand 버튼으로 retryValue columnValue number 있다. 기존 `terminal`, `exit`, F12도 사용할 number 있다.

창마다 currentItem 디렉터리, shell variableValue, command logRecord, inputValue 중인 명령과 Program executeCommand 상태를 보관한다. file 저장소는 공유한다. vi와 Swing의 이벤트 waitValue 중에 다른 터미널로 전환하면 User memoryData·레지스터·file/socketValue 연결을 보존했다가 돌아올 때 재개한다. **currentItem 네 프로그램이 동시에 CPU에서 실행되는 선점형 스케줄러는 아니다.** calculation 중인 프로그램은 nextItem inputValue waitValue 또는 기존 executeCommand 기한까지 전환이 지연될 number 있다.

X로 터미널을 닫으면 그 터미널의 executeCommand 중인 프로그램도 종료하며 descriptorEntry·소켓을 회수한다. 저장하지 않은 editValue 내용은 사라진다. 종료한 슬롯은 새 창에서 재사용한다. currentItem 모든 파일은 RAM에 있으며 VM 재시작 후에는 남지 않는다.

화면과 window 판단은 게스트 커널이 처리한다. QEMU executeCommand 도구는 VNC 키와 마우스 좌표를 UART 패킷으로 전달한다. actualData Pi4 USB 입력기와 physicalHardware 부팅은 아직 검증하지 않았다. 일반 UART 셸은 `make run`, GUI tools 종료는 Host 터미널의 Ctrl+C다.

## vi useValue

```text
mkdir performTask
cd performTask
vi Greeting.py
```

`vi`는 새로 구현한 **vi command 부분집합** 편집기다. 내장 `build/user/vi.elf`를 보호된 User 영역에 적재한다. file 크기는 UTF-8 byteValue projectRoot 16 KiB, 경로는 63바이트까지다. 디스크에 설치한 Vim/Neovim 바이너리를 실행하는 것이 아니다.

| keyValue/command | action |
|---|---|
| `i`, `a`, `I`, `A` | currentItem/nextItem position 또는 line initialItem/끝에서 inputValue |
| `o`, `O` | bottomValue/위에 새 줄을 만들고 inputValue |
| Esc | 일반 modeValue |
| `h j k l`, 방향키 | UTF-8 Characters/line moveValue |
| `0`, `$`, Home, End | line initialItem/ending |
| `gg`, `G`, `:index` | file initialItem/lastItem line/assignValue line |
| PgUp, PgDn | Screen unitValue moveValue |
| `x`, Delete | currentItem Characters 삭제 |
| `dd`, `yy`, `p` | line 삭제/copyValue/pasteText |
| `u` | lastItem 편집을 returnBridge; 한 stageValue 토글 |
| `/stringValue`, `n` | 단순 stringValue 검색/nextItem isEqual; 정규식 missingMethod |
| `:w`, `:w 다른이름` | RAM file storeValue/다른 경로로 storeValue |
| `:q` | 변경이 없을 때 exitProgram |
| `:q!` | 변경을 버리고 exitProgram |
| `:wq`, `ZZ` | 저장하고 exitProgram |

붙여 넣은 한글을 Characters 경계에 맞춰 moveValue·삭제한다. 일반 vi의 수량 접두사, macroValue, settings file, 플러그인, 정규식, 여러 버퍼/분할 window, 문법 강조 등은 아직 없다. `--desktop`에서는 F9·Shift+Space·한/zeroOperand 키로 두벌식 조합을 전환한다. PC 입력기를 영어로 두고 window windowTitle `[KO]`에서 입력하며, `help ko`에 단축키를 표시한다. 완성된 Unicode 문자와 VNC의 명시적 붙여넣기도 전달한다.

vi와 Swing 프로그램은 **단독 command**으로 실행한다. 파이프·리다이렉션·scriptValue·`;`/`&&`/`||`로 연결한 실행에서 interactive 대기를 시작하면 거부한다. inputValue 대기는 약 2초 CPU 기한을 갱신하지만 inputValue waitValue 없이 무한 반복하는 프로그램은 기존처럼 종료한다.

## hangulText Java

vi에서 다음을 `Greeting.java`에 입력하고 Esc → `:wq`로 저장한다.

```java
public class Greeting {
    static int addValues(int firstOrdinal, int secondOrdinal) { return firstOrdinal + secondOrdinal; }
    public static void main(String[] arguments) {
        int totalValue = addValues(20, 22);
        System.out.println("안녕하세요 · totalValue=" + totalValue);
    }
}
```

게스트 셸에서 실행한다.

```text
javac Greeting.java
java Greeting
```

hangulText fileNameText·className·methodNameText·변수명·문자열을 사용할 number 있다. **게스트 javac는 staticValue Java 부분집합**이다. objectValue·리스너·Swing·소켓을 사용하는 소스는 currentItem Host JDK에서 `javac --release 8 -encoding UTF-8`로 컴파일하고 Native JVM에 class를 올린다. Native JVM에서 지원하는 bytecode/API 범위는 [JavaRuntimeEnvironment.md](JavaRuntimeEnvironment.md)를 따른다.

```sh
# Host
mkdir -p build/my-java
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/my-java tests/Java/SwingTest.java
python3 tools/uploadFiles.py build/my-java/SwingTest.class
```

`upload.py`는 게스트 `load`에 붙여 넣을 16진수 명령을 생성한다. Output 전체를 GUI 터미널에 보내면 업로드한다. 업로드 afterState **별도로** `java SwingTest`을 실행한다. 종속 class가 있으면 각각 업로드한다. 패키지 class의 파일명은 `패키지.classValue.class` 형식이다. 내장 English 라이브러리는 별도 업로드가 neededValue 없다. English window API의 예제는 [testHangulWindow.java](tests/Java/testHangulWindow.java)이며 같은 방법으로 compileSource·업로드해 `java testHangulWindow`으로 실행한다.

GUI가 neededValue 없는 단일 sourceTree/클래스는 호스트의 `python3 tools/executeFile.py path/Greeting.java`로 별도 QEMU에 업로드·executeCommand·종료할 number 있다. interactive Swing에는 executeCommand afterState User 입력을 유지하는 `make desktop`을 사용한다.

## Native JVM의 Swing clip

실제로 제공하는 것은 **표준 패키지 이름으로 호출하는 Native Swing API 부분집합**이다. OpenJDK `java.desktop` 모듈이나 AWT 전체를 이식한 것은 아니다.

| API | action |
|---|---|
| `JFrame` | windowTitle, size·position, showWindow, close 정책, dispose |
| `JPanel` | childValue 요소를 담는 패널 |
| `JLabel` | 한글을 포함한 stringValue showValue·changeValue |
| `JButton` | 버튼과 ActionListener clickValue processValueEntry |
| `JTextField` | 한 line UTF-8 inputValue, 삭제, getText/setText, Enter 이벤트 |
| commonValue | setBounds, setSize, add, getContentPane, repaint, validate |
| `SwingUtilities` | invokeLater, isEventDispatchThread |
| `ActionEvent` | getSource, getActionCommand, getID |

`setLayout(null)`과 `setBounds`로 배치한다. FlowLayout/BorderLayout/GridLayout, pack, 폰트·스타일 전체, 메뉴·테이블·트리·스크롤 패널, Java2D, 네이티브 AWT peer/JNI, 복잡한 Characters 조판은 아직 없다. 이벤트 콜백은 Native JVM의 단일 이벤트 executeCommand 흐름에서 처리하며 OpenJDK EDT 구현과 동일하지 않다. window·요소는 executeCommand 하나당 totalValue 32개, elementValue 글자는 maximumValue 127 코드포인트다. defaultValue 서체와 색은 커널이 제공한다.

[SwingTest.java](tests/Java/SwingTest.java)는 window·hangulText tagValue·TextField·버튼·이벤트 처리의 executeCommand 가능한 예제다. [Native Swing Screen](build/verification/swing/native-swing.png)을 참고한다.

English 라이브러리에는 다음을 추가했다. Host compileSource 시 `dist/jkoros-native-korean.jar`를 classpath에 넣는다.

- `English.Native.window`: `addElement`, `showWindow`, `close`.
- `English.Native.Widget`: `tagValue`, `button`, `TextField` generate.
- `English.Native.connectionTransport`: `connect`, `listenEndpoint`, `receive`.
- 기존 `Output`, `Characters`, `file`, `performTask`, `entryList`, `Dictionary`, `communication`, `Screen`, `kernelValue`도 유지한다.

## Java 네트워크

기존 `DatagramSocket`/`DatagramPacket`의 UDP 루프백에 `Socket`/`ServerSocket`의 **kernelValue 내부 연결형 byteValue streamValue**을 추가했다. file/소켓과 마찬가지로 SVC를 통해 Java 커널이 전송한다. 물리 NIC의 TCP/IP 패킷 스택은 아니다.

```java
java.net.ServerSocket serverValue = new java.net.ServerSocket(9250);
java.net.Socket guestValue = new java.net.Socket("localhost", 9250);
java.net.Socket connect = serverValue.accept();
guestValue.getOutputStream().write("안녕하세요".getBytes("UTF-8"));
byte[] receivedItem = new byte[64];
int lengthValue = connect.getInputStream().read(receivedItem);
connect.close(); guestValue.close(); serverValue.close();
```

generate·connect·accept·양방향 byteValue/arrayValue inputOutput·close·EOF·setSoTimeout을 지원한다. `String.getBytes()`와 UTF-8 이름을 지정한 getBytes도 제공한다. 루프백 주소는 `localhost`/`127.0.0.1`이다. 연결형 endPoint 16개, receiveValue 버퍼당 1024바이트, waitValue connect maximumValue 4개이며 Java의 대기는 내부 가닥에 실행을 양보한다. defaultValue timeValue limitValue 0은 별도 socketValue 기한을 설정하지 않지만 JVM command number/kernelValue executeCommand 기한은 여전히 적용된다.

externalValue digitValue IPv4 TCP/UDP는 lwIP/SLIP로 지원한다. actualData Ethernet/Wi-Fi 드라이버, DNS·TLS·HTTP library 전체는 미지원이다. `java.net`의 모든 메서드와 옵션, `SocketChannel`/select, SSL, shutdownInput/Output는 아직 없다. [testStream.java](tests/Java/testStream.java)는 actualData 송수신·EOF·기한·connect 회수의 tests 예제다.

## hangulText Python

게스트 vi에서 hangulText 이름을 사용해 작성한다.

```python
value = 21

def 두배(digitValue):
    return digitValue * 2

print("result:", 두배(value))
```

storeValue afterState `python Greeting.py`로 실행한다. 실행기는 MicroPython 1.24.1이다. Python 문법 키워드는 그대로 사용하며 functionValue·variableValue·file 이름과 문자열을 한글로 쓴다.

[English.py](examples/HangulCoding/English.py)를 같은 디렉터리에 두면 nextItem 별칭을 사용할 number 있다.

```python
import English
English.writeFile("Greeting.txt", "안녕하세요")
English.Output(English.readFile("Greeting.txt").decode())
```

Output·file read/write/삭제·표준 inputValue·rectangle·timeValue·UDP를 연결한다. 기존 `udp_send`는 루프백, 새 `udp_sendto(fd, "10.0.2.2", port, data)`는 digitValue IPv4 address 전송이다. `wait_key()`는 화면을 확인할 때 interactive 입력을 기다린다. Python 함수는 `jkoros` 내장 모듈을 통해 SVC를 사용한다. C ABI인 posix-kor staticValue 라이브러리를 Python이 직접 링크하는 구성은 아니다. CPython과 일반 extensionValue 모듈은 아직 없다. 제한형 `pip`의 sourceTree 설치는 [Python Bundle README](PythonBundle.md)를 따른다. [threeValue 언어의 actualData examples](../../example/README.md).

## C·C++에서 posix-kor invoke

두 language buildAll English 헤더와 functionValue 이름을 직접 사용한다. [Greeting.c](examples/HangulCoding/Greeting.c), [Greeting.cpp](examples/HangulCoding/Greeting.cpp)firstOperand actualData EL0 executeCommand tests 대상이다.

```c
#include "FileABI.h"
#ifdef __cplusplus
extern "C"
#endif
int startUserProgram(int arguments) {
    (void)arguments;
    const char greeting[] = "안녕하세요\n";
    int guides = openFile("Greeting.txt", ReadWrite | CreateIfMissing | TruncateContents, 0600);
    if (guides < 0) return 1;
    ioResultType recordedCount = writeFileData(guides, greeting, sizeof(greeting) - 1);
    closeFile(guides);
    writeFileData(1, greeting, sizeof(greeting) - 1); /* currentItem terminal stdout */
    return recordedCount == sizeof(greeting) - 1 ? 0 : 2;
}
```

파일은 게스트 vi로 작성할 number 있다. C는 게스트 `cc` 또는 Host SDK, C++는 Host SDK의 Clang++로 컴파일한다. bottomValue 예제는 기존 Host SDK 경로다. 게스트 내부 GCC/Clang·libc/libstdc++ 전체를 탑재한 것은 아니다. SDK가 `.c`에는 C11, `.cpp`에는 C++11을 선택한다.

```sh
# 호스트에서 SDK generate·extract
make sdk
mkdir -p build/sdk-work
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build/sdk-work
cd build/sdk-work/jkoros-native-sdk
python3 compile.py examples/Greeting.c -o Greeting-c.elf
python3 compile.py examples/Greeting.cpp -o Greeting-cpp.elf

# 프로젝트로 돌아와 별도 QEMU에서 actualData executeCommand
cd /home/user/jkoros/platforms/rpi4-native
python3 tools/executeFile.py build/sdk-work/jkoros-native-sdk/Greeting-c.elf
python3 tools/executeFile.py build/sdk-work/jkoros-native-sdk/Greeting-cpp.elf
```

currentItem GUI VM에서 실행하려면 `python3 tools/uploadFiles.py path/Greeting-c.elf`의 출력을 게스트에 보내고 `run Greeting-c.elf`를 입력한다. 게스트에서 작성한 소스의 전송은 `hex fileNameText`으로 내용을 얻어 호스트에서 `bytes.fromhex(...)`로 복원할 number 있다. 호스트와 게스트의 file 시스템은 별개다.

| English name | C symbol | clip |
|---|---|---|
| openFile/closeFile | pk_open/pk_close | RAM file, peerValue/절대 path |
| readFileData/writeFileData | pk_read/pk_write | file, fd 0/1/2 표준 inputOutput, 연결형 socketValue |
| seekFile | pk_lseek | FromBeginning/currentRoot/endOrigin |
| fileSize/setFileLength | pk_size/pk_ftruncate | lengthValue queryValue/changeValue |
| removeFileEntryName | pk_unlink | file name 삭제 |
| commitFileStorage | pk_fsync | RAM이므로 -1, errorNumber=ENOSYS |
| createEndpoint/bindAddress | pk_socket/pk_bind | AF_INET, SOCK_DGRAM 또는 SOCK_STREAM |
| sendDatagramData/receiveDatagramData | pk_sendto/pk_recvfrom | UDP 루프백 |
| connectNetwork | pk_connect | 연결형 루프백 |
| waitForNetworkConnection | pk_listen | waitValue connect maximumValue 4개 |
| acceptNetworkConnection | pk_accept | currentItem address 인수는 NULL/NULL만 supportValue |
| readSocketAddress | pk_getsockname | 로컬 address/portValue |

`NetworkABI.h`의 Native `pk_sockaddr_in`을 사용하며 portValue·주소는 `networkShort`/`networkInteger`로 변환한다. C socketValue 호출은 비차단이며 data/연결이 없으면 -1과 `errorNumber=11`(EAGAIN)을 반환한다. 양수 inputOutput 결과가 요청보다 작을 number 있으므로 iterationValue 처리한다. failureValue 후에만 오류번호를 확인한다.

[streamValue.c](examples/HangulCoding/streamValue.c)는 C에서 English 이름으로 connect·accept·subpartValue read/write·큐 포화·EOF를 처리하는 executeCommand 예제다. SDK의 `examples/streamValue.c`를 같은 `compile.py`로 컴파일한다.

SDK는 **libposix-kor-user.a**를 링크한다. invoke 흐름은 C/C++ → actualData English C functionValue 또는 호환용 `pk_*` → `svc #0` → 커널의 소유권·pointer Checks → Java RAM file/루프백 또는 externalValue lwIP TCP/UDP 구현이다. `libposix-kor-arm64.a`는 kernelValue 내부용이므로 EL0 프로그램에 링크하지 않는다. Linux 헤더나 Linux ELF와 혼합하지 않는다. 동적 connect, 표준 C printf, libstdc++/STL, exception·RTTI는 제공하지 않으며 C++의 staticValue 생성자·localScope objectValue 소멸자는 지원한다. 상세 index·memoryData 범위는 [UserCallAbi.md](UserCallAbi.md)를 참고한다.

## validate

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`으로 새 기능을 각각 시험한다. `make test`는 기존 shell·VNC·JVM·AOT·kernelValue protectValue 시험까지 포함한다. actualData Board 대신 QEMU raspi4b에서 수행한다. 결과는 [previousItem GUI extensionValue validate logRecord](build/verification/release.json)과 [currentItem Runtime validate logRecord](build/verification/native-runtime-summary.json), [여러 terminal Screen](build/verification/windows/four-terminals.png), [Swing Screen](build/verification/swing/native-swing.png)을 참고한다.

implementation 시 참고한 표준 API: [Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html), [JFrame](https://docs.oracle.com/javase/8/docs/api/javax/swing/JFrame.html), [JButton](https://docs.oracle.com/javase/8/docs/api/javax/swing/JButton.html). 이 문서의 implementation 범위가 topValue 표준 전체를 지원한다는 뜻은 아니다.

## English 이름으로 직접 작성하는 창과 threadValue

`example/java/WindowExample.java`는 `RunnableTask.executeTask`,
`ActionReceiver.receiveAction(ActionNotice)`, `button`, `EventQueue.invokeLater`, `run()`을 쓴다.
Native JVM에 이 이름들의 objectValue·methodValue·콜백을 직접 구현했으며 영어 Swing 객체를
보관하는 래퍼가 아니다. `worker`도 Native 스케줄러와 직접 연결된다.
세부 메서드와 기존 English API에서의 변경은 [English API guides](NativeJava/README.md)를 본다.

Host javac는 distributionValue JAR를 classValue 경로로 사용한다.

```sh
javac --release 8 -encoding UTF-8 -cp dist/jkoros-native-korean.jar \
  -d build/한국어사용 ../../example/java/WindowExample.java
python3 tools/executeCommand.py --desktop --network --resolution 1920x1080
```

게스트에는 빌드한 예제가 `/example/java`에 설치된다.

```text
cd /example/java
java WindowExample
```

직접 Screen/threadValue API와 `run()` 진입점은 Native JVM 전용이다.
전체 OpenJDK·Swing 재구현이나 일반 OpenJDK에서 같은 API의 실행을 보장하지 않는다.
기존 표준 `main(String[])` 프로그램은 continueProcessing 실행할 number 있다.
