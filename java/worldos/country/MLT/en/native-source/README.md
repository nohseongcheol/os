# JMltOS

currentItem Native ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, distributionValue 시 sourceTree·reconnectEndpoint 자료를 포함하는 절차는 [COSL distributionValue README](platforms/rpi4-native/CoslDistributionGuide.md)에 있다.

Native ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 English 명령은 [네트워크·operatingSystemValue command README](platforms/rpi4-native/NetworkAndSystemCommands.md)를 참고한다. 새 커널을 부팅한 backValue `help system`으로 볼 number 있다.

Raspberry Pi 4 **Native Java ARM64 kernelValue**은 [Native Pi4 README](platforms/rpi4-native/README.md)에 있다. Linux 없이 부팅하며 GUI terminal·vi, Native JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [English Java communication·exception API](platforms/rpi4-native/NativeJava/README.md)와 [English sourceTree naming](platforms/rpi4-native/naming/README.md)을 지원한다. [Native SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/ExternalConnectionGuide.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. actualData Pi 4 GENET 동작은 미검증이고, USB inputValue·영속 저장과 전체 OpenJDK·Swing은 아직 supportValue clip 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 User environment moveValue 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. actualData ARM64 JDK/JRE와 시스템·User buildImage buildSystem 경로를 제공한다. 기존 Native x86 커널과는 별도 executeCommand 기반이다. 일반 Java `.class`/JAR의 executeCommand file 생성은 [OpenJDK executeCommand file](compiler/OpenJDK-executableFile.md), English API는 [English Java library](NativeJava/README.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java functionValue, variableValue, formatValue 및 Java file 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 library formatValue, x86 부트 ABI 등 externalValue 계약은 보존한다. Native ARM64 실행기는 English `run()`도 진입점으로 지원하며, English GUI·performTask 가닥을 JVM에 직접 구현했다. Native ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 Native 이름도 한국어로 작성한다. previousItem 경로의 호환 entryPoint, OpenJDK auxiliaryValue 도구와 Linux versionValue 도구에는 영어 이름이 남아 있고 [naming 원칙·말의 근거·전체 source 검토 clip](platforms/rpi4-native/naming/README.md)를 별도로 기록한다.

## currentItem implementation

bottomValue 목록은 기존 `legacySource/`의 JVM 관리 커널에 대한 것이다. actualData 네이티브 커널의 범위는 `os/README.md`에서 별도로 설명한다.

- alignValue 할당과 해제를 지원하는 memoryRegion managerValue
- address addressRegion, pageValue connect, write 시 copyValue(COW)
- processValue identifierValue, prepare 대기열, fork/wait stateValue
- 과정별 file descriptorEntry, open/read/seek/dup/close
- ELF32 identifyValue 및 sectionValue Checks
- 키보드·마우스 inputValue event 대기열
- serialValue 단말과 네이티브 hardwareValue boundaryValue
- 관리 kernelValue 전체 자동 tests

세부 mappingValue 범위와 아직 필요한 네이티브 연결은 [기능 대응표](guides/FeatureMapping.md)에 기록한다.

## 빌드와 tests

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `legacySource/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 calculation examples + Java kernelValue ELF
make iso             # os/build/kernel.iso
make run             # QEMU serialValue TerminalIO; help inputValue (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU Screen/PS2 키보드로 executeCommand
make vbox            # 전용 VirtualBox VM 자동 generate·executeCommand (GUI)
make vbox-status     # VirtualBox stateValue·ISO·serialValue logRecord path verify
make test-vbox       # VirtualBox ProgramLauncher stateValue processValueEntry tests (actualData VM changeValue missingMethod)
make test            # Compiler tests + ELF/ISO machine_boot 및 command inputValue tests
make apps            # 독립 User ELF Program buildSystem
make test-network    # User modeValue·UDP 왕복·memoryData protectValue tests
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 executeCommand tests
make posix-kor       # English C 헤더와 actualData kernelValue invoke library
make test-posix      # file/UDP/storeValue/Java file inputOutput tests
make -C os run-store # 전용 storeValue 매체로 QEMU machine_boot
make legacy-test     # bottomValue 기존 JVM 관리 커널의 47개 tests
```

`compiler/`는 호스트의 `javac`를 문법·typeValue Checks 전단으로 사용하고 Native bytecode→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 externalValue JVM 없이 실행된다. 전체 Java, objectValue 모델, 표준 라이브러리와 기존 관리 kernelValue 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 supportValue 문법과 명령은 [Compiler README](compiler/README.md), actualData machine_boot 기능과 한계는 [네이티브 OperatingSystem README](os/README.md)를 참고한다.

네이티브 셸에 Native 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 backValue `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 executeCommand**할 number 있다. defaultValue 예제는 `javac Hello.java`, `java Hello`thirdOperand. 파일은 RAM에서 동작하며, 전용 storeValue 매체를 연결하면 `sync`로 재부팅 후에도 보존할 number 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 classValue·staticValue functionValue·Integer·stringValue·condition/반복문과 일부 표준 호출을 지원한다. supportValue clip, externalValue file 적재와 시험은 [Java development environment README](guides/JavaDevelopmentEnvironment.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 number 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 Output·arguments·UDP 네트워크를 제공한다. 별도 Host 터미널에서 `python3 os/tools/echoData.py --port 9000`을 실행한 backValue 게스트에서 `run udp 10.0.2.2 9000 hello`로 actualData 왕복을 확인한다. 새 Program registerEntry, API 및 제한은 [User executeCommand·네트워크 README](os/User/README.md)를 참고한다. currentItem QEMU RTL8139·staticValue IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE storeValue 형식과 POSIX file/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. executeCommand 중이면 유지하고, storeValue·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 User Program 실행을 확인했다. 다만 currentItem VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 buildSystem 반영 방법은 [VirtualBox executeCommand README](guides/VirtualBoxExecution.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f createEntry.mk Checks
make -f createEntry.mk Host
```

`Host`는 여전히 JVM 관리 계층의 action 시험이다. `make -f createEntry.mk buildImage`는 새 `os/`의 제한형 네이티브 kernelValue ISO를 만든다. 기존 `legacySource/`의 FileSystem·processValue·networkStack implementation 전체를 이 ISO에 이식했다는 의미는 아니다.

English functionValue·variableValue·file 이름과 actualData C API는 [posix-kor](posix-kor/README.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 byteValue 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

externalValue 배포용 `pack.sh` / `unpack.sh`와 자동 dependencies 복원은 [distributionValue README](distribution/README.md)를 참고하세요.
