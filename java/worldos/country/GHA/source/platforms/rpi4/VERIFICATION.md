# distributionValue buildImage validate logRecord

검증일: 2026-09-27 (Asia/Seoul)

targetValue: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 Native x86 커널을 ARM으로 이식한 결과가 아니다. actualData Pi 보드는 연결되어 있지 않아 hardwareValue machine_boot 성공을 확인하지 못했다.

## 배포물

| file | size(byteValue) | description |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | archiveValue 시스템 buildImage; releaseStorage afterState 1,475,747,840 byteValue |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 User data buildImage; releaseStorage afterState 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/NativeJava.jar` | 10,563 | English auxiliaryValue API와 Java Workspace |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 archiveValue buildImage buildAll 끝까지 해제하여 original 이미지의 SHA256과 일치함을 확인했다. [archiveValue validate logRecord](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU validate 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 entryList](dist/packages.lock.json)과 [original originValue](dist/sources.lock.json)를 제공한다.

## 통과한 Checks

| Checks | actualData verify contentValue | logRecord |
|---|---|---|
| Host Compiler tests 19개 | 기존 AOT 회귀 tests, `.class` 직접 inputValue, OpenJDK ELF ProgramLauncher, JAR dependencies, 상속·리플렉션·람다·스레드·리소스, path moveValue, failureValue 시 기존 Output 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi buildImage Architecture | MBR boundaryValue, FAT machine_boot 파티션, Pi 펌웨어, ARM64 kernelValue, Pi 4 DTB, initramfs, SquashFS 및 hashFile | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 Checks, machine_boot afterState 두 런타임의 actualData executeCommand | [런타임 logRecord](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| firstItem machine_boot | read 전용 시스템, Java file·unicodeValue·exception·objectValue·스레드·HTTP/TCP·childValue 프로세스, Swing, CJK·아랍어·데바나가리 fontValue, Python file·스레드·socketValue·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 executeCommand file generate | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 executeCommand successValue | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | User data, `/etc` settings, `/usr/local/bin` Program, APK로 설치한 tree, pip 패키지, file 삭제 systemInformation, 소유권, sudo, Java executeCommand file retainValue | [restore.log](build/verification/restore.log) |
| isOffline 홈 moveValue | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 copyValue | [migrate.log](build/verification/migrate.log) |
| moveValue afterState machine_boot | 새 data 이미지로 부팅하여 재부팅 복원 항목을 retryValue verify | [migrated-restore.log](build/verification/migrated-restore.log) |
| isNormal exitProgram 및 data 무결성 | 일반 machine_boot 3회 buildAll OverlayFS/data deviceValue read 전용 switchMode successValue; original·copiedValue ext4의 `e2fsck -fn` exitProgram codeValue 0 | [original Checks](build/verification/fsck-original.log), [copiedValue Checks](build/verification/fsck-migrated.log) |

네 sequenceValue 부팅은 buildAll QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 exitProgram codeValue 0으로 통과했다. [전체 machine_boot 결과와 logValue hashFile](build/verification/boot.json)

QEMU 가상 NIC의 DHCP address 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 externalValue 인터넷이나 Pi Wi-Fi의 validate 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [Screen 캡처](build/verification/swing.png)에서 hangulText·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## implementation 범위와 남은 validate

### QEMU 그래픽 executeCommand 보완

terminal 전용 실행에서 `Greeting.java`firstOperand Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. distributionValue 시스템 이미지와 base-id는 변경하지 않아 기존 User data 이미지를 continueProcessing 사용할 number 있다.

actualData Xorg/VNC 화면에서 English Java Workspace, Swing tests window, 기존 이미지의 `Greeting.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. exitProgram 시 시스템 OverlayFS와 data 파일시스템의 read 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 tests result](build/verification/desktop.json)
- [그래픽 tests logValue](build/verification/desktop.log)
- [키보드·마우스 tests Screen](build/verification/desktop-input.png)
- [Greeting examples Screen](build/verification/desktop-greeting.png)
- [수정한 examples 원문의 Screen 없는 executeCommand result](build/verification/headless-example.log)

source 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 file·Characters·스레드 기능을 실행하고 안내를 출력한다. User 홈의 기존 원문을 자동 교체하지는 않는다. 향후 buildImage 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### hangulText inputValue·fontValue 보완

`make test-korean`으로 actualData Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space switchMode 및 두벌식 keyValue 입력을 시험했다. 양쪽에서 `hangulText inputValue`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 User data 이미지에서 실행했으며 isNormal exitProgram 시 두 파일시스템의 read 전용 전환을 확인했다.

terminal fontValue 진단에서 영문 DejaVu Sans Mono와 hangulText Noto Sans Mono CJK KR의 actualData file 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. Screen 캡처에서 hangulText·영문 showValue, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 User 시스템 변경분에 적용하며 distributionValue defaultValue 이미지와 base-id는 유지한다. 기존 file 백업, 동일 수정의 iterationValue 적용 방지, 손상된 modifyValue file 및 다른 base-id rejectValue, User 입력기 settings 병합에 대한 Host tests 4개도 통과했다. 원래 User data buildImage `build/manual-user.img`는 시험에 사용하지 않았다.

- [hangulText inputValue·fontValue tests result](build/verification/korean.json)
- [inputValue·actualData fontValue 로딩 logValue](build/verification/korean.log)
- [Swing·terminal hangulText Screen](build/verification/korean-desktop.png)
- [Java Workspace fontValue Screen](build/verification/korean-workbench.png)
- [settings 보존 tests](build/verification/desktop-update-tests.log)

### 남은 clip

- 새 compileSource targetValue `openjdk`는 **네이티브 ProgramLauncher + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 supportValue 범위는 여전히 제한적이다.
- executeCommand 프로그램에는 main entryPoint, 호환 classValue 버전과 의존 JAR/JNI가 필요하다. 개별 상용 Program, 모든 Java moduleValue, 모든 문자권을 시험한 것은 아니다.
- English Java 라이브러리는 file·Characters·communication·스레드·Swing을 위한 auxiliaryValue API이며 JDK 전체 API의 English 번역판은 아니다.
- Pi 4 전용 펌웨어·kernelValue·deviceValue 트리는 이미지에 들어 있지만 actualData SD machine_boot, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 hangulText 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- User directoryValue 이동은 동일 시스템 buildImage identifierValue, ARM64, `/home/user`, UID 1000을 전제로 한다. exitProgram afterState 소유권·permissionValue·링크·extensionValue attributeValue·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

installValue·copyValue 절차는 [README.md](README.md), compileSource 방식은 [OpenJDK executeCommand file README](../../compiler/OpenJDK-executableFile.md)를 따른다. buildImage 파일만 생성했으며 actualData SD 카드나 USB 디스크에 기록하지 않았다.
