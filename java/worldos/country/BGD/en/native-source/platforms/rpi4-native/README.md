# Raspberry Pi 4 Native Java kernelValue — User executeCommand foundation

currentItem Native 코드의 COSL 상업 condition, 제3자 고지 및 LGPL reconnectEndpoint 자료는 [COSL distributionValue README](CoslDistributionGuide.md)를 참고한다. switchMode beforeValue GPL 구성의 판단은 [previousItem 라이선스 검토](LicenseReview.md)에 기록했다.

English communication·exception 사용법은 [English Java API](NativeJava/README.md), functionValue·variableValue·file 이름의 변경과 어원 근거는 [naming README](naming/README.md)를 참고한다.

Linux 없이 부팅하는 Native AArch64 커널이다. Java AOT kernelValue 위에 **commandLine shell, 게스트 Java Compiler·JVM, MicroPython, EL0 C++ executeCommand, file·UDP 루프백 시스템 invoke, 여러 hangulText GUI terminal·vi Editor·Swing 부분집합**을 제공한다. 커널의 file data/정책·루프백 transferValue·shell 상태는 Java, Screen 합성·pixel changeValue·pointer·클리핑도 Java로 구현하며, CPU/MMU/deviceValue 경계와 terminal·characterValue paintScreen 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 Native 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 executeCommand, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](FileTransferAndCompilation.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, physicalHardware Pi4의 wiredValue 송수신은 아직 미검증이다.** executeCommand·connection·passwordValue 확인은 [externalValue connection README](ExternalConnectionGuide.md)에 정리했다.

셸은 EL1 kernelValue, `java` 등 User executeCommand 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 limitValue, QEMU 네트워크 executeCommand·connection 방법 및 actualData 검증은
[executeCommand 계층과 externalValue communication inspectState](RuntimeAndExternalNetworkChecks.md)을 참고한다.

ELF는 확장자가 아닌 actualData executeCommand 형식으로 검사한다. `./Greeting`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 staticValue ELF는 `run --linux fileNameText`으로 실행한다. [ELF·Linux ABI supportValue 범위와 동일 바이너리 tests](executableAbi.md).

GUI와 네트워크는 `python3 tools/executeCommand.py --desktop --network`로 함께 사용한다. Java·C·Python의 English examples 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 machine_boot 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 number 있다. Remmina에서 **F9/Shift+Space/한·zeroOperand keyValue**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·actualData TCP/UDP·file byteValue·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` afterState `java WindowExample`로 English Swing 예제를 실행한다. terminal 모서리에 마우스를 대고 **leftSide 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 currentItem columnValue·rowValue 수를 보여 준다.

## currentItem supportValue clip

| 기능 | implementation·시험한 clip | 아직 isUnsupported |
|---|---|---|
| machine_boot | Pi4 AArch64 EL1, UART, SD용 buildImage, QEMU raspi4b machine_boot | actualData Pi4 보드에서의 펌웨어 machine_boot tests |
| Java kernelValue | staticValue Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java objectValue/exception/GC/JVM/표준 library |
| Java development tools | 게스트 Native `javac`/`java`, JVM 0.4/JAR: 다중 classValue·objectValue·상속·exception·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, English library. 게스트 컴파일러는 staticValue Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | actualData MicroPython 1.24.1 EL0 Porting, sourceTree compileSource/executeCommand, classValue·exception·GC·큰 Integer·Unicode·file·UDP/Screen connect | CPython, pip, C extensionValue, 부동소수점, 일반 OS/스레드/socketValue moduleValue, interactive REPL |
| shell | UTF-8 editValue·logRecord·completedValue, 디렉터리·file command, variableValue·condition·scriptValue, 16 KiB 순차 파이프·리다이렉션, ELF executeCommand | 전체 POSIX sh/Bash, performTask controlValue·동시 프로세스·PTY |
| C/AOT compileSource | 게스트 TinyCC 및 staticValue Java 부분집합 `jaot` → Native ARM64 ELF | 전체 libc·모든 Java classValue AOT |
| C++ | 독립 ELF64를 EL0에서 executeCommand; staticValue 생성자, RAII 소멸자, FP/SIMD, English file/루프백 invoke | libc/libstdc++, STL, C++ exception·RTTI·동적 connect |
| User protectValue | 4 KiB 페이지, codeValue RX/data RW·NX, kernelValue·MMIO 차단, guard page, 잘못된 pointer Checks | 다중 User permissionValue, 일반 프로세스/스레드 스케줄러 |
| executeCommand timeValue limitValue | GIC-400 타이머로 무한 iterationValue exitProgram; interactive inputValue 대기는 기한 refresh, 터미널별 EL0 Program 중단·resumeExecution | 일반적인 선점형 다중작업. 긴 kernelValue invoke 도중에는 종료가 지연될 number 있음 |
| file | Java RAM file 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, peerValue/절대 path 63바이트, descriptorEntry 16개 | permissionValue, 디스크/SD 영속 storeValue |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP implementation, 게스트 FTP·SSH·VNC | GENET physicalHardware validate, Wi-Fi, DNS, 일반 TLS socketValue, RDP |
| GUI | maximumValue 네 terminal window, selectionValue·moveValue·X close, hangulText fontValue, Swing 부분집합; 게스트 VNC Screen·inputValue·두벌식 | physicalHardware USB inputValue, 전체 AWT/Swing·Java2D·window 관리 정책 |
| performTask threadValue | kernelValue performTask 2개와 주 performTask; JVM 내부 threadValue maximumValue 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, hangulText·일본어·아랍어·이모지, UTF-8 fileNameText/datagram | GUI의 일반 다국어 조판 |

executeCommand 버튼 화면은 5×7 영문 글꼴을 쓰며, terminal 창은 Noto CJK/DejaVu에서 생성한 hangulText·Unicode 비트맵 글꼴을 쓴다. UART와 actualData 프레임버퍼의 hangulText 표시를 시험한다. 루프백은 동일 kernelValue 내부의 datagram 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 auxiliaryValue UART SLIP 경로를 사용한다. `python3 tools/executeCommand.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·executeCommand 제한과 English 사용법은 [Native JVM과 English library](JavaRuntimeEnvironment.md)에 정리했다. classValue file/JAR 배포는 [NativeJava](NativeJava) 소스에서 재현한다. 기존 Linux판 `English.Java`와 별도인 `English.Native` 패키지다.

**vi·여러 window·Swing·hangulText Java/Python/C/C++·posix-kor 예제는 [hangulText development 매뉴얼](DevelopmentGuide.md)에 정리했다.**

GUI terminal executeCommand·단축키·shell command·제한은 [셸과 terminal 사용법](ShellAndTerminal.md)에 정리했다.

## currentItem 컴퓨터에서 executeCommand

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

exitProgram: **Ctrl+A nextItem X**. 게스트 C/AOT tools 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc arithmeticValue auxiliaryValue 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. Host 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 Porting·링크한 것은 아니다. Compiler 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/path/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` supportValue 여부를 확인한 afterState 실행한다.

명령은 **Enter를 눌러 executeCommand**한다. 기존 한 characterValue 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "hangulText arguments 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| command | action |
|---|---|
| `help` / `info` | command·actualData implementation stateValue |
| `ls` / `cat FILE` / `rm FILE` | RAM file entryList·contentValue·삭제 |
| `vi FILE` | User regionValue vi 부분집합, hangulText editValue·storeValue·검색·되돌리기 |
| `edit FILE` | file 전체를 새로 inputValue; 단독 `.` 줄로 storeValue, Ctrl-C로 cancelOperation |
| `javac FILE.java` / `java CLASS [ARGS]` | Native 제한형 Java compileSource·executeCommand |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython compileSource·executeCommand |
| `load FILE` / `hex FILE` | 16진수 바이너리 inputValue/Output; 입력은 단독 `.` 줄로 storeValue |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 Native ABI ELF / 내장 C++ examples |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 performTask / EL0 protectValue tests |
| `gui` / `terminal` | executeCommand Screen / hangulText GUI terminal; F12로 terminal open·close |
| `samples` | 삭제한 defaultValue examples recoverState; 기존 파일은 보존 |

예를 들어 `edit Greeting.java`를 입력한 nextItem bottomValue 소스를 입력한다.

```java
public class Greeting { public static void main(String[] args) { int value = 7; System.out.println("hangulText=" + value); } }
```

그다음 단독 `.` 줄로 저장하고 `javac Greeting.java`, `java Greeting`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. cancelOperation·잘못된 16진수·capacityValue 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, executeCommand 인수는 maximumValue 8개·각각 UTF-8 255바이트다. 일반 command 인수는 maximumValue 32개다. quote·백슬래시·shell variableValue·파이프·리다이렉션 범위는 [shell description](ShellAndTerminal.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, address **127.0.0.1:5902**로 연결한다. 키보드·hangulText Unicode inputValue·명시적 pasteValue·executeCommand 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 tools/executeCommand.py --desktop --network
# 다른 hardwarePort: python3 tools/executeCommand.py --desktop --port 5903
```

종료는 실행한 Host 터미널에서 Ctrl+C다. 기존 `python3 tools/executeCommand.py --vnc 127.0.0.1:2`는 Screen 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. actualData Pi4 USB 입력기는 아직 없으며, VNC connect 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 actualData C++/UDP ELF executeCommand, `Hello.java` compileSource afterState JVM executeCommand, `hello.py` executeCommand, GUI terminal 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interactive 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 memoryData·CPU 문맥을 보관한다. shell·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## actualData 산출물과 Pi4 SD buildImage

```sh
make image   # kernelValue, SD buildImage, machine_boot ZIP, 사용자용 SDK
make sdk     # SDK만 retryValue generate
```

| path | 용도 |
|---|---|
| `build/kernel8.img` | Native kernelValue 기계어, 적재 address 0x80000 |
| `build/kernel.elf`, `kernel.map` | kernelValue symbolValue·link_layout |
| `build/user/demo.elf` | User modeValue C++ file/heapValue/floatingPointValue/그래픽 examples |
| `build/user/network.elf` | User modeValue C++ UDP 루프백 examples |
| `build/user/java-tools.elf` | Native Java 부분집합 Compiler/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | Host javac용 English API classValue; 같은 클래스가 Native JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | English API Java source |
| `build/user/vi.elf` | Native UTF-8 vi command 부분집합 Editor |
| `build/user/python.elf` | Native ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 protectValue tests 전용 |
| `build/libposix-kor-arm64.a` | **kernelValue 내부**에서 Java file 구현을 직접 부르는 기존 connect |
| `build/libposix-kor-user.a` | **EL0 User Program**에서 SVC로 file/루프백을 호출하는 새 connect |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD buildImage |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 machine_boot 파티션에 복사할 file groupValue |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·run codeValue·library·링커 scriptValue·examples |
| `dist/manifest.json`, `build/build.json` | SHA256과 actualData supportValue stateValue |

이미지는 확인된 공식 Pi machine_boot 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·terminal fontValue 라이선스와 fontValue originValue 해시도 동봉한다. file generate 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 buildImage logRecord 도구로 `.img`를 기록하거나 FAT32 machine_boot 파티션 최상위에 ZIP 내용을 푼다. buildImage 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 defaultValue EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**physicalHardware Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD file 구성·kernelValue 체크섬 검사와 물리 Board machine_boot 검증은 별개다. MMU useValue 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 machine_boot 조건을 전제로 한다. threeValue auxiliaryValue 코어는 대기시키며 한 코어만 사용한다.

## C++와 English API useValue

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/FileExample.cpp -o demo.elf
python3 compile.py examples/CommunicationExample.cpp -o network.elf
```

진입점은 `extern "C" int startUserProgram(int)`이다. User C++는 FP/SIMD를 사용할 number 있다. kernelValue C/Java AOT는 일반 레지스터만 사용하므로 exception processValueEntry 중 User FP 상태를 건드리지 않는다. User entryPointValue 시 FP 상태를 초기화하고 kernelValue 복귀에 필요한 상태를 보존한다.

```cpp
#include "FileABI.h"
extern "C" int startUserProgram(int) {
    int file = openFile("Greeting.txt", ReadWrite | CreateIfMissing | TruncateContents, 0600);
    if (file < 0) return 1;
    const char contentValue[] = "안녕하세요";
    int result = writeFileData(file, contentValue, sizeof(contentValue) - 1);
    closeFile(file);
    return result == sizeof(contentValue) - 1 ? 0 : 2;
}
```

[file examples](User/FileExample.cpp)와 [communication examples](User/CommunicationExample.cpp)firstOperand actualData machine_boot tests 대상이다. `FileABI.h`의 이름은 커널용/사용자용 buildAll 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 file processValueEntry 및 루프백 전달은 Java 커널에서 실행한다. `NetworkABI.h`의 socketValue 함수는 currentItem 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 kernelValue 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 nextItem 도구를 사용하면 **새 QEMU를 부팅해 업로드한 actualData 바이트를 재확인한 backValue 게스트에서 executeCommand**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 tools/executeFile.py build/jkoros-native-sdk/demo.elf
python3 tools/executeFile.py examples/Hello.java "hangulText arguments"
python3 tools/executeFile.py examples/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 kernelValue 묶음에 포함되어 이 file 한도를 적용받지 않는다. **C++ 컴파일러는 Host SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 library, PT_TLS, PT_INTERP, PT_DYNAMIC, executeCommand·write 겸용 세그먼트는 로더가 거부한다. 구체적인 invoke index·address clip·오류는 [User ABI](UserCallAbi.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `commitFileStorage`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 permissionValue·dup/fcntl은 없다. 디렉터리와 peerValue/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 maximumValue 512바이트, 소켓은 8개, receiveValue 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. User exitProgram 시 열린 file 서술자와 소켓을 회수한다.

## validate result

`make test-jvm`은 9개 프로그램을 OpenJDK와 actualData Native 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `tools/testBoot.py`는 Java rectangle API의 actualData Screen 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 actualData VNC inputValue·hangulText terminal 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT operationValue result 비교, 런타임 error 중단, isUnsupported Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java kernelValue calculation·UTF-8·C++ 직접 invoke·협력식 performTask 및 프레임버퍼.
- 손상/잘못된 ABI/address 초과/겹친 페이지/W+X 등 ELF rejectValue 사례 22개.
- EL0 C++ 생성자·RAII·floatingPointValue operationValue·file·heapValue 및 잘못된 시스템 invoke pointer.
- kernelValue/codeValue/MMIO write·accessEntry, NX operandStack·NULL executeCommand, guard page, 특권 command 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 afterState isNormal Program 재실행.
- iterationValue executeCommand 시 file/socketValue 누수 방지, UDP 왕복·보낸 address·clippedValue receiveValue·큐 포화·빈 datagram·isUnsupported communication error.
- shell editValue·cancelOperation·16진수 업로드/다운로드·User ELF 실행과 잘못된 ELF rejectValue.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 executeCommand, hangulText classValue·variableValue·fileNameText.
- 여러 window·vi storeValue·editValue·returnBridge·User stateValue 중단/resumeExecution, Swing hangulText inputValue·이벤트·X close, 연결형 루프백, C/C++ hangulText SDK examples.
- MicroPython Unicode·큰 Integer·classValue·GC iterationValue·file import·exception·file·UDP 왕복·timeValue 초과 afterState 복귀.
- GUI selectionValue moveValue, C++/UDP/Java/MicroPython 버튼 executeCommand, 콘솔 복귀 및 actualData 프레임버퍼 픽셀/fontValue.
- 디렉터리·variableValue·condition·file command·scriptValue·순차 파이프·리다이렉션·capacityValue 초과 recoverState, Python stdin/EOF와 Java/Python stdout.
- command logRecord·긴 hangulText inputValue editValue·completedValue·terminal 스크롤, 그래픽 Program exitProgram afterState window 복원, actualData VNC Unicode keyValue·pasteValue·마우스.

[kernelValue tests logRecord](build/verification/implementation-test.log), [shell tests](build/verification/shell/report.json), [VNC tests](build/verification/desktop/report.json), [machine 판독 result](build/verification/report.json), [serialValue logValue](build/verification/serial.log), [GUI Screen](build/verification/gui-python.png)을 확인할 number 있다. VNC RFB 3.8 connect 및 640×480 Screen 정보도 검사한다. [SDK 재컴파일 result](build/verification/sdk.json)는 두 예제의 entryPoint·적재 세그먼트·ABI note가 machine_boot 시험한 ELF와 일치함을 확인한다. symbolValue 등 비적재 메타데이터를 포함한 file 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 clip

Native `javac`는 버전 49 `.class`를 생성하며 JVM은 supportValue 명령으로 구성된 버전 45–52 클래스를 실행한다. staticValue functionValue·재귀·int/boolean/char/String·condition/iterationValue·stringValue 결합과 일부 file 스트림을 지원한다. UTF-8 문자열과 Characters 리터럴, ASCII 및 현대 hangulText 음절/compositionValue jamoValue 식별자를 처리한다. Unicode identifierValue 전체 lookupTable·Unicode sourceTree 이스케이프는 구현하지 않았다. 게스트 sourceTree 컴파일러는 일반 objectValue·exception·Thread 구문을 아직 컴파일하지 못한다. Host `javac --release 8`로 만든 supportValue 부분집합 클래스는 Native JVM 0.4의 objectValue·exception·Thread·UDP와 English API를 사용할 number 있다. Swing은 문서화한 Native API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [Native JVM description](JavaRuntimeEnvironment.md)이 기준이다. 상세 language 범위는 [공유 Java tools description](../../guides/JavaDevelopmentEnvironment.md)을 참고하되, 그 문서의 x86 shell/storeValue/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 sourceTree**를 Native AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 functionValue·classValue·exception·리스트/Dictionary·Unicode·GC·가변 precisionValue 정수를 제공한다. currentItem 구성은 Integer 빌드로 `float`, `complex`, `math`firstOperand 없으며 CPython 전체 표준 library, pip, subprocess, threading, 일반 socket과 defaultValue `open()` file 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 objectValue·모듈은 exitProgram 시 회수되고 RAM 파일만 nextItem 실행에 남는다.

`import jkoros`로 nextItem 시스템 연결을 쓴다. buildAll SVC를 통해 Native Java 커널에 접근한다.

| functionValue | action |
|---|---|
| `stdin(limit)` | currentItem 표준 입력에서 maximumValue limit바이트(0…16384)를 bytes로 readResult; EOF는 빈 bytes, UART data 없음은 OSError(11) |
| `read(name)` | peerValue/절대 RAM 경로의 file 전체를 bytes로 readResult |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 storeValue, 쓴 byteValue number returnResult |
| `remove(name)` | RAM file 삭제 |
| `rect(x, y, w, h, color)` | 선택한 actualData Screen size 안의 rectangle drawingValue; 기존 보드의 RGB32 value |
| `ticks_ms()` | machine_boot afterState milliseconds, 32비트 cycleValue |
| `udp_open(port)` | 127.0.0.1의 UDP socketValue open/bindEndpoint; 0은 자동 hardwarePort |
| `udp_send(fd, port, data)` | 루프백 destinationValue 포트에 str/bytes 버퍼 transferValue |
| `udp_recv(fd)` | `(bytes, 보낸포트)` returnResult; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | socketValue close |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

Porting codeValue: [python/](pythonBridge/), [User Java connect](User/javaBridge.c). 공식 [MicroPython Porting README](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. sourceTree URL·hashFile·라이선스는 [vendor README](vendor/README.md)에 기록했다.

## 남은 performTask

| nextItem stageValue | isComplete projectRoot |
|---|---|
| 영속 storeValue·executeCommand file inputValue | SD/MMC 및 디스크 file 시스템, 시스템/User 볼륨; currentItem ELF file 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 address addressRegion, 선점 스케줄러, TLS, synchronize/waitValue, 신호, mmap/mprotect |
| libc와 C++ 런타임 | Native ABI용 libc, malloc/free, 표준 inputOutput·Clock·environment·locale, libstdc++/exception processValueEntry validate |
| CPython | 해당 libc와 OS API 대상으로 Porting·교차 빌드하고 file/Unicode/스레드/socketValue tests |
| OpenJDK/JRE | HotSpot OS layerValue, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 library Porting; javac/java actualData executeCommand |
| externalValue 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 actualData Board 송수신 validate, DNS·Wi-Fi |
| GUI extensionValue | USB HID, 게스트 입력기·Characters 조판, Swing window size 조절·클리핑 extensionValue, 전체 AWT/Swing Porting |

이 표는 남은 작업이며 implementation isComplete 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 externalValue 네트워크 드라이버는 physicalHardware 검증도 필요하다. [QEMU deviceValue 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

hardwareValue 및 ABI 참고: [BCM2711 peripheral](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC address](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox contractValue](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP controlValue 레지스터 definitionValue](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## English C dataType·Python error·Bundle installValue

C 네트워크 API는 `struct InternetSocketAddress`, enum 상수와 actualData English 함수로
구현한다. macroValue 별칭을 사용하지 않으며 previousItem pk_* ABI도 유지한다.
Python 예제는 `SystemError`, `error.index`, `error.description`을 사용한다.

`python3 tools/executeCommand.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 number 있다. 현재는 Host 중계를
이용하는 제한형 MicroPython sourceTree 설치기이며 CPython pip·자동 dependencies 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 limitValue](PythonBundle.md).

## Screen size selectionValue

`python3 tools/executeCommand.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. terminal moveValue, Swing middle link_layout, Java·C·Python 그리기도 actualData 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [settings·English API·validate README](screenResolution.md).

## English 직접 API와 Screen refresh

`example/java`는 `RunnableTask`, `ActionReceiver`, `ActionNotice`, `button`, `EventQueue`,
`worker`, `run()`을 사용할 number 있다. English GUI/가닥을 Native JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. stringValue 등 javac의 표준
계약과 전체 sourceTree 검토 범위는 [naming README](naming/README.md), 사용법과 호환성 변경은
[English Java API](NativeJava/README.md)를 본다.

terminal moveValue·size 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[Screen refresh description](JavaRuntimeEnvironment.md#terminal-subpartValue-refresh),
[subpartValue refresh Checks](build/verification/redraw/report.json)를 참고한다.
