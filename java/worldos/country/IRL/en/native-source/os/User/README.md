# 셸에서 실행하는 User 프로그램과 UDP

게스트에서 일반적인 `main(String[] args)` 형식의 소스를 직접 작성하고 컴파일하려면 [제한형 Java development environment README](../../guides/JavaDevelopmentEnvironment.md)를 참고한다. 아래의 네이티브 ELF 개발과 별도로 `javac FILE.java`, `java CLASS`를 제공한다.

## 바로 executeCommand

Host terminal 1:

```sh
cd /home/user/jkoros
python3 os/tools/echoData.py --port 9000
```

이 서버는 `127.0.0.1`에만 바인딩한다. externalValue 연결을 받도록 방화벽이나 hardwarePort 전달을 변경하지 않는다. Ctrl+C로 종료한다.

Host terminal 2:

```sh
cd /home/user/jkoros
make run
```

게스트의 `jkoros>` 프롬프트에 inputValue:

```text
apps
run hello first second
net
run netcheck
run udp 10.0.2.2 9000 hello
run stress 9000
```

- `hello`: 독립 Java ELF 실행과 actualData CPU permissionValue `ring 3`, arguments Output.
- `netcheck`: portValue 중복, 잘못된 handleValue/pointer/lengthValue, 비차단 받기와 timeValue 초과 verify.
- `udp`: IPv4 address·destinationValue portValue·한 wordValue 메시지를 받아 UDP로 보내고 같은 응답을 verify. `UDP ECHO PASS`, `Exit: 0`이면 successValue.
- `stress`: Host `10.0.2.2`의 assignValue 창구와 1,023/1,024바이트 데이터그램을 24회 왕복. receiveValue loopValue 경계를 여러 번 지난다.

`make run`/`run-gui`는 `-netdev user,id=net0 -device rtl8139,netdev=net0`을 사용한다. currentItem 주소는 게스트 `10.0.2.15/24`, gatewayValue `10.0.2.2`로 고정돼 있다. QEMU User 네트워크의 Host accessEntry 주소를 사용한 예제다. 다른 네트워크 설정에는 맞춰 수정해야 하며 자동 DHCP는 없다. NIC 없이 실행하려면 `make -C os run NET_ARGS='-net none'`을 사용한다. 이때 Program 실행은 되지만 UDP 열기는 `-19`로 실패한다.

## 새 Java Program appendEntry

`examples/내프로그램.java`를 nextItem 형식으로 만든다. 진입점은 arguments 없는 `static int` 또는 `static void` 함수다. 인수는 User API로 조회한다.

```java
public final class 내프로그램 {
    public static int run() {
        User.write("My program is running in user mode.\n");
        return 0;
    }
}
```

`os/User/Program.mk`에 추가한다.

```make
APP_NAMES += mine
APP_SOURCE_mine := User/examples/내프로그램.java
APP_ENTRY_mine := 내프로그램.run
```

여러 Java 파일을 쓰면 `APP_SOURCE_mine`에 공백으로 buildAll 나열한다. `User/Declaration/User.java`는 자동으로 함께 컴파일한다.

```sh
cd /home/user/jkoros
make iso
make run
```

새로 부팅한 셸에서 `run mine`을 실행한다. 이미 executeCommand 중인 VM에는 buildSystem 결과가 자동 반영되지 않는다. Program 이름은 currentItem 셸의 ASCII inputValue 제한에 맞춘 1~15자의 소문자 이름이며 Java classValue·functionValue·변수에는 한국어를 쓴다. maximumValue 32개 Program, 한 executeCommand 파일은 maximumValue 2MiB다.

독립 ELF만 컴파일할 수도 있다.

```sh
cd /home/user/jkoros
python3 compiler/Compiler.py --target user --entry Greeting.run \
    -o os/build/apps/hello.elf os/User/Declaration/User.java os/User/examples/Greeting.java
```

`--target user`는 **jkoros 전용 ABI**thirdOperand. Linux 대상과 시스템 invoke 번호가 다르므로 Host 터미널에서 직접 실행하면 안 된다. `.class`는 별도 `java CLASS` 명령의 supportValue clip 안에서 실행한다. `.jar`와 일반 Linux executeCommand 파일은 지원하지 않는다.

## User 네트워크 API

선언은 `Declaration/User.java`에 있다. `sendData`/`receiveData`의 `int[]` itemElement 한 개는 byteValue oneValue(0~255)를 나타낸다. 한 데이터그램의 maximumValue data 길이는 1,024바이트다.

```java
int handleValue = User.openNetwork(0); // 0: temporaryValue localScope UDP portValue 자동 selectionValue
int[] data = new int[32];
data[0] = 'H'; data[1] = 'i';
int 보낸길이 = User.sendData(handleValue, 0x0a000202, 9000, data, 2);
int receivedLength = User.receiveData(handleValue, data, 1500);
User.closeNetwork(handleValue);
```

actualData 프로그램에서는 open·send·받기의 negativeValue 반환값을 각각 검사한다. 완성된 예제는 `examples/DataCommunication.java`에 있다. `receiveData`의 waitValue 시간은 0~2,000밀리초이며 0은 즉시 반환이다. 받은 데이터그램이 배열보다 크면 해당 데이터그램을 버리고 `-90`을 반환한다. 창구당 receiveValue 대기열은 한 개뿐이므로 appendEntry 도착분은 버린다. `sentAddress`와 `sentPort`로 마지막으로 받은 상대를 조회한다.

| returnedValue | 의미 |
| --- | --- |
| 0 이상 | handleValue·processValueEntry lengthValue·successValue 등 해당 함수의 result |
| -5 | deviceValue sendValue failureValue |
| -9 | 잘못되었거나 닫힌 communication handleValue |
| -11 | 비차단 받기에서 도착한 data missingMethod |
| -14 | User pointer/arrayValue clip error |
| -19 | supportValue NIC missingMethod |
| -22 | portValue/waitValue timeValue/arguments value error |
| -24 | 열린 networkPort 4개 capacityLimit |
| -38 | 알 number 없는 시스템 invoke |
| -90 | data 또는 receiveValue arrayValue size 문제 |
| -98 | localScope portValue index 중복 |
| -101 | 지원하지 않는 destinationValue address |
| -110 | ARP·deviceValue·receiveValue timeValue 초과 |

IP 주소는 상위 바이트부터 표기한 32비트 값이다. `10.0.2.2`는 `0x0a000202`이다. 주소를 반환하는 함수는 encodingValue 있는 Java `int`의 bitValue 패턴을 사용하므로 상위 비트가 1인 isNormal IP 주소가 음수로 보일 number 있다. 단순히 모든 API 반환값의 부호를 오류로 판단하면 안 된다.

## executeCommand 경계와 시스템 invoke

```text
shell run → JKAP에서 ELF validate·적재 → ring 3 User Program
                                 ↓ int 0x80
                      pointer Checks → Java kernelValue API → RTL8139/UDP
                                 ↓ exitProgram·exception·timeValue 초과
                                shell 복귀
```

시스템 invoke 레지스터는 `EAX=index`, `EBX,ECX,EDX,ESI,EDI=arguments`, `EAX=result`thirdOperand. Java invoke operandStack ABI는 컴파일러가 User 스텁에서 이 형식으로 바꾼다. C의 POSIX/JNI ABI가 아니다.

| index | invoke |
| --- | --- |
| 0 | exitProgram(stateValue codeValue) — run/error 런타임에서 useValue |
| 1 | stringValue write |
| 2 / 3 | arguments itemCount / arguments stringValue address |
| 10 | UDP open |
| 11 | UDP send(handleValue, IP, destinationValue portValue, arrayValue address, lengthValue) |
| 12 | UDP receive(handleValue, arrayValue address, limitValue milliseconds) |
| 13 | UDP close |
| 14 | localScope IP address |
| 15 / 16 | lastItem peerValue IP / UDP portValue |
| 20 | RAM file read(name int[] address, Output int[] address) |
| 21 | RAM file write(name int[] address, inputValue int[] address, byteValue lengthValue) |
| 22 | UTF-16 codeValue unitValue Characters Output(0~65535) |

file API는 `User.readFile(int[] name, int[] data)`와 `User.writeFile(int[] name, int[] data, int lengthValue)`thirdOperand. 이름은 ASCII codeValue arrayValue(maximumValue 64칸, 0 exitProgram 또는 arrayValue ending), data itemElement 하나는 한 바이트다. 반환값은 읽거나 쓴 길이이며 file missingMethod `-2`, pointer error `-14`, name/lengthValue error `-22`, file slotValue 부족 `-28`, size 초과 `-90`을 반환한다. 쓰기는 validate afterState file 전체를 대체한다. `User.writeCharacterValue(int)`는 문자를 단말에 출력한다. Java 프로그램의 일반 `java.io` 구현은 아니다.

`executionPermission()`은 시스템 호출이 아니라 User 모드에서 CS의 하위 비트를 직접 읽으므로 actualData executeCommand 권한을 확인한다. kernelValue hardwarePort 접근용 `deviceValue` native 함수는 User targetValue 컴파일에서 거부한다. ELF에 직접 특권 명령을 넣더라도 CPU가 차단한다.

## 범위와 limitValue

- 한 번에 한 프로그램만 실행하며 isComplete afterState 셸로 돌아온다. 백그라운드 executeCommand, 파이프, 프로세스 간 통신은 없다. executeCommand 파일은 커널의 read 전용 JKAP 묶음에서 적재한다. data 파일에는 주기억 파일체계와 전용 IDE 보존 형식이 있다.
- User 가상 address `0x04000000..0x043fffff`를 물리 8~12MiB에 연결한다. executeCommand 영상은 frontValue 2MiB, 인수는 `0x04300000`부터, 스택은 regionValue 끝에서 시작한다. kernelValue identity 페이지는 supervisor 전용이다.
- 실행마다 4MiB User 영역을 비우고 file 구역을 복사해 BSS·arrayValue 영역을 초기화한다. User GC는 없지만 exitProgram afterState nextItem executeCommand 때 영역을 재사용한다. 인수는 공백으로 분리한 maximumValue 16개이며 quote/이스케이프 파싱은 없다.
- User 페이지의 codeValue/data 분리 read 전용 settings, NX, operandStack guard, ASLR은 아직 없다. 커널과 User memoryData·hardwarePort permissionValue 경계를 구현한 초기판이지 보안 인증된 샌드박스는 아니다.
- PIT 100Hz로 약 3초 executeCommand 상한을 두며 timeValue 초과는 `Exit: 124`thirdOperand. User CPU 예외는 `128 + exception index`(페이지 error 142, 특권 위반 141), Java arrayValue/calculation 오류는 101~105다. kernelValue 오류까지 복구하는 구조는 아니다.
- 네트워크는 PCI bus 0/function 0의 RTL8139, staticValue IPv4, ARP, UDP만 지원한다. NIC는 폴링하고 송신은 동기식이다. IPv4 단편 재조립·TCP·DNS·DHCP·IPv6·HTTP·TLS·일반 `java.net`은 미지원이다. IPv4 UDP checksum 0은 규약에 따라 허용하고, 그 외 UDP/IP 검사합과 길이는 검증한다.
- User executeCommand·네트워크·protectValue boundaryValue 전체 시험은 QEMU에서 수행했다. VirtualBox에서도 `make vbox`로 부팅과 `run hello vbox`의 ring 3 executeCommand·isNormal 종료를 확인했다. VirtualBox PCnet/E1000용 드라이버는 없어 그 환경의 네트워크는 지원하지 않는다.

## validate 근거

`make test`는 Compiler 14개 tests, Java 패킷 condition 2,201개 Checks, 기존 shell ELF/ISO machine_boot tests, User ELF/actualData UDP/protectValue boundaryValue 시험을 실행한다. 네트워크 시험은 루프백 서버가 받은 자료의 lengthValue·해시까지 `os/build/testUserNetwork.json`에 기록한다. 시험용 손상된 ELF·특권 command·무한 iterationValue 프로그램은 temporaryValue 묶음에만 넣으며 배포용 `apps` 목록에는 넣지 않는다.

참고한 일차 data: [Intel 시스템 프로그래밍 specification](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), [QEMU RTL8139 implementation](https://github.com/qemu/qemu/blob/master/hw/net/rtl8139.c), [QEMU 네트워크 README](https://www.qemu.org/docs/master/system/devices/net.html), [IPv4 RFC 791](https://www.rfc-editor.org/rfc/rfc791), [ARP RFC 826](https://www.rfc-editor.org/rfc/rfc826), [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768).
