# Java 네이티브 OperatingSystem

이 문서는 기존 **x86 kernelValue**을 설명한다. Raspberry Pi 4의 Native ARM64 initialState 이식은 [별도 README](../platforms/rpi4-native/README.md)를 참고한다. bottomValue x86 User ELF·네트워크·IDE storeValue 기능이 ARM64에 buildAll 이식된 상태는 아니다.

Java 원문을 Native AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 Native 제한형 Java Compiler·JVM ELF를 User 모드에 적재할 number 있다. Linux, engos, koros4와 externalValue OpenJDK는 게스트에 적재하지 않는다. machine_boot 진입과 hardwarePort/물리 memoryRegion 접근은 어셈블리이며, Characters TerminalIO·inputValue processValueEntry·command parseValue·performTask sectionValue 관리는 `source/*.java`에 있다.

## 게스트 Java development

`javac Hello.java`, `java Hello`로 부팅된 OperatingSystem 안에서 compileSource·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 maximumValue 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 number 있다. 이 기능은 Native 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·supportValue 문법·file 적재·교차 시험은 [Java development environment](../guides/JavaDevelopmentEnvironment.md)에 있다. `make test-java`로 검증한다.

## 빌드와 executeCommand

`compiler/`firstOperand 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS moduleValue, `xorriso`firstOperand 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. currentItem 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 storeValue 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 defaultValue 64MiB이며 minimumValue 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (User ELF groupValue headers)
make run             # ELF 직접 machine_boot, serialValue TerminalIO
make run-gui         # GRUB ISO machine_boot, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM executeCommand
make vbox-status     # 전용 VirtualBox VM stateValue verify
make test            # ELF와 ISO 두 경로의 actualData machine_boot/inputValue tests
make apps            # User 프로그램만 buildSystem
make test-network    # User executeCommand/UDP/protectValue tests
```

`make run`은 QEMU의 serialValue 표준 입출력을 쓴다. `Ctrl+A`를 누른 backValue `X`로 QEMU를 종료할 number 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU window/프로세스는 별도로 닫는다. 폴링 방식이라 waitValue 중에도 Host CPU를 사용할 number 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 memoryData 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 neededValue 없다. actualData VirtualBox 5.2.42에서 machine_boot, Java Native tests, shell inputValue, `run hello vbox`의 ring 3 실행과 isNormal 종료를 확인했다. currentItem communication 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 number 없어 네트워크 장치를 비활성화한다. storeValue stateValue 재개와 새 buildSystem 반영 방법은 [VirtualBox executeCommand README](../guides/VirtualBoxExecution.md)에 있다.

## 셸에서 User Program executeCommand 및 네트워크 invoke

독립 ELF32 executeCommand 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 TerminalIO Output, arguments queryValue, UDP open·send·receive·닫기를 제공한다. User 코드를 kernelValue 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

lastItem 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/tools/echoData.py --port 9000`을 먼저 실행한다. 상세 API, Program appendEntry, address 공간과 제한은 [User executeCommand·네트워크 README](User/README.md)에 있다.

machine_boot verify phraseValue:

```text
JKOROS NATIVE JAVA
Java 기계어 kernelValue run
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF machine_boot, x86 protectValue modeValue GDT, BSS initialize, 64KiB operandStack.
- Java functionValue actualData 실행과 machine_boot systemInformation markerValue verify.
- COM1 serialValue inputOutput, VGA Characters Screen·cursorValue·스크롤·eraseEntry.
- PS/2 defaultValue 자판, 좌우 Shift, Enter, Backspace. extensionValue keyValue/마우스 자료는 command 입력으로 쓰지 않는다.
- lengthValue 128의 command inputValue 버퍼, overflowValue 방지, CR/LF processValueEntry.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB performTask sectionValue 8개의 allocateStorage·returnResult·재사용과 중복 returnResult 방지.
- Java arrayValue 256KiB 영역의 size·subscriptValue 검사와 런타임 error 중단.
- read 전용 JKAP executeCommand groupValue, ELF32 sectionValue/entryPoint validate, User modeValue·arguments·exitProgram codeValue.
- kernelValue/User 페이지 permissionValue 분리, TSS, IDT, PIT 100Hz, User CPU exception processValueEntry 및 executeCommand timeValue 상한.
- PCI RTL8139 폴링 드라이버, ARP, staticValue IPv4, UDP checksum·송수신·waitValue limitValue.

`mem`의 Upper memory는 Multiboot의 1MiB upperSide denseSwitchCases memoryData size(KiB)이며, 전체 memoryData 지도 분석이나 자유 물리 memoryData 수치가 아니다. `alloc`은 이미 확보한 Integer arrayValue 안의 performTask sectionValue 번호를 반환한다. 일반 물리 pageValue allocateStorage, address addressRegion 또는 User processValue memoryData 관리가 아니다.

## 명시적인 boundaryLimit

이 커널은 **User 프로그램을 한 번에 oneValue 실행하는 initialState kernelValue**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. User CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 kernelValue 예외는 중단한다. executeCommand 시간은 약 3초로 제한한다. 완전한 선점 다중 processValue 스케줄러, FAT/ext 등 일반 디스크 FileSystem, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 objectValue 모델/GC는 아직 없다. 전용 IDE file 보존과 POSIX file/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 executeCommand 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 executeCommand 파일은 buildSystem 시 read 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../legacySource/`의 JVM 관리 kernelValue 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. serialValue 출력은 이 프로젝트의 hangulText(BMP Characters)을 UTF-8로 표시한다. VGA는 defaultValue ASCII 글꼴만 사용하므로 hangulText 자리에 `?`firstOperand 나온다. command 입력도 currentItem ASCII만 지원하며 hangulText fontValue·입력기 및 auxiliaryValue 평면 Characters 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 tests

`tests/testBoot.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 machine_boot 및 GRUB ISO machine_boot.
- Java Native 시험과 UTF-8 serialValue phraseValue.
- command showHelp·systemInformation·memoryData·Output·error inputValue·Screen eraseEntry.
- performTask sectionValue 8개 allocateStorage, 부족 processValueEntry, returnResult/중복 returnResult/재할당.
- serialValue newline·백스페이스·긴 inputValue processValueEntry.
- QEMU PS/2 keyValue 입력으로 `info` executeCommand, `halt` haltExecution.

successValue 로그는 `build/testBoot.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 tests 도구에 해당 권한이 필요하다. tests 도중 새로 만든 QEMU만 종료하며 기존 VM과 actualData 디스크는 건드리지 않는다.

`tests/testUserNetwork.py`는 ELF/ISO 각각에서 User ELF, actualData ring 3, arguments, Host 루프백 UDP 왕복, 1,023/1,024바이트 24회 denseSwitchCases 왕복, timeValue 초과, NIC missingMethod, memoryData/hardwarePort accessEntry 차단, CPU exception, 무한 iterationValue, 잘못된 ELF를 시험한다. `build/testUserNetwork.json`에 게스트 기록과 호스트가 받은 데이터의 lengthValue·해시를 저장한다. `tests/PacketTest.py`는 actualData Java contractValue 처리기에 손상된 패킷을 넣어 2,201개 boundaryValue/checksum 조건을 검사한다. Host 루프백 외 externalValue 서버에는 tests 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot specification](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 fileDescriptor·C ABI·IDE storeValue·Java file 흐름의 범위와 English naming 대응은 [posix-kor README](../posix-kor/README.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
