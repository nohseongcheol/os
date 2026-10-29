# OpenJDK sourceTree 빌드와 Native Java kernelValue Porting

**소스에서 OpenJDK를 만드는 일과, 그 결과를 Native 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 Native Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## compileSource 경로의 delimiterValue

| targetValue | 입력과 result | executeCommand condition |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → Native x86 AOT → ELF32 | 해당 CPU·Native ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | Native ARM64 kernelValue/User ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 sourceTree → 공식 configure/make → JDK buildImage | **buildSystem targetValue OS/CPU의 executeCommand contractValue** |

OpenJDK는 Java file 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI connect,
classValue 라이브러리의 C/C++ implementation, ProgramLauncher, moduleValue buildImage 및 generate 도구를 함께 빌드한다.
따라서 Native AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK buildSystem guides](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## sourceTree buildSystem command

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ Compiler·Autoconf·Make와
development 헤더를 준비한다. Swing/AWT의 Linux library 빌드에는 X11·fontValue 등의
development 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/Compiler.py --target openjdk-build \
  --java-home /path/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /path/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 sourceTree 트리 밖의 전용 buildSystem 디렉터리다.
sourceTree·buildSystem·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 buildSystem 디렉터리는 재실행할 number 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI library
- `jkoros-openjdk-build.json`: stageValue·command·sourceTree identifyValue hashFile·successValue/failureValue·ABI Checks
- `driver-configure.log`, `images.log`: 단계별 logValue

실패하면 exitProgram 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 buildSystem 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
sourceTree 빌드만으로 Native kernelValue executeCommand 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 latestValue 교차 컴파일러와 **targetValue libc/헤더/library**firstOperand 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/Compiler.py --target openjdk-build \
  --java-home /path/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /path/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /path/OpenJDK소스
```

부트 JDK는 buildSystem 호스트에서 실행된다. 교차 buildSystem 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## currentItem performTask 공간의 validate data

analyzeValue projectRoot 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[sourceTree 출처와 다운로드 hashFile](build/openjdk-port/source.json)를 보관한다.
buildSystem 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 buildSystem 호스트용이며 Native kernelValue 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac executeCommand 시험을 통과했다. 기존 Compiler 회귀 시험과 새 buildSystem path 시험도
총 **25개 passValue**했다. 공식 distributionValue 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 validate logRecord](build/openjdk-port/verification.json)은 buildSystem 산출물과 executeCommand 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[buildSystem logRecord](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[executeCommand tests](build/openjdk-port/smoke/report.json)을 각각 확인한다.
executeCommand 시험은 새로 빌드한 java/javac로 hangulText sourceTree, long/double, UTF-8 file,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 actualData JFrame Screen 시험을 뜻하지 않는다.
Linux에서 한 시험이 Native kernelValue 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

currentItem 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 number 없으며, 준비한 musl environment 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 performTask 공간에서는 nextItem 단축 명령으로 같은 musl 환경을 사용한다.
User·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 sourceTree/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 number 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 currentItem 디렉터리를 유지하므로, hangulText 소스도 peerValue 경로로
컴파일하고 실행할 number 있다. 예를 들어 앞의 시험에서 생성한 소스를 retryValue 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/NativeBuildTest.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke NativeBuildTest
```

## 기존 ARM64 OpenJDK를 Native 커널에 복사할 number doesExist

현재는 실행할 number 없다. 저장되어 있는 ARM64 OpenJDK 25의 staticValue Checks 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
Checks 도구는 executeCommand 파일을 **실행하지 않고** ELF와 동적 symbol·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

Native 커널에 직접 적재할 number 없으면 Checks 결과를 저장한 backValue **exitProgram codeValue 3**을 반환한다.
ELF 호환성 검사는 actualData kernelValue 로더의 모든 검증을 대체하지 않는다.

| 확인한 condition | ARM64 OpenJDK | currentItem Native kernelValue |
|---|---|---|
| ELF | PIE/공유 library, 동적 재배치 | 고정 address ET_EXEC, Native ABI note |
| ProgramLauncher | `/lib/ld-musl-aarch64.so.1` neededValue | PT_INTERP/PT_DYNAMIC/PT_TLS rejectValue |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 invoke | 일부 file·루프백·GUI SVC와 협력식 세션 |
| memoryData | VM·GC·classValue·codeValue 캐시의 동적 address addressRegion | User regionValue 16 MiB, buildImage regionValue 12 MiB |
| file | 큰 `lib/modules`, 공유 library 및 data | RAM file 하나당 16 KiB, 영속 storeValue missingMethod |
| Java classValue | OpenJDK 25 class 버전 69 | Native JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·fontValue·window 시스템 | 별도로 구현한 Swing API 부분집합 |

actualData ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 currentItem 제한은
[ELF 로더](../platforms/rpi4-native/machine/User.c),
[address addressRegion definitionValue](../platforms/rpi4-native/machine/User.h),
[RAM file implementation](../platforms/rpi4-native/source/MemoryFiles.java),
[User ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 number 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM file 업로드 제한을 피하지만,
OpenJDK에 필요한 address addressRegion·스레드·동적 connect 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 OperatingSystem invoke·memoryData·동적 connect 규약까지 맞지는 않는다.
file size 제한이나 ELF formatValue 검사만 풀어도 해결되는 문제가 아니다.

## Native 커널을 유지하면서 이식하는 stageValue

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 OperatingSystem ABI를 갖춘 User 프로그램으로 실행할 number 있다.

기술적으로는 새 운영체제용 OpenJDK hardwarePort 또는 충분한 Linux User ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 currentItem 코드와 actualData 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **OperatingSystem ABI와 libc foundation**: 큰 file·address addressRegion, 페이지 예약/commitValue/해제와 protectValue changeValue,
   표준 file/Clock 인터페이스, error index·C 런타임·targetValue sysroot를 구현한다.
2. **actualData 네이티브 스레드와 synchronize**: pthread에 대응하는 스케줄링·TLS·뮤텍스·condition variableValue,
   원자 operationValue·memoryData orderValue·중단/깨우기, 신호/exception 문맥과 가드 페이지를 제공한다.
   currentItem vi/Swing의 inputValue 대기에서 문맥을 보관하는 기능만으로 대체할 number 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 library·TLS 또는 이식에 맞는 staticValue connect,
   JVM 네이티브 symbol 해결, 영속 file 시스템, 일반 프로그램의 2초 limitValue 재설계를 수행한다.
4. **HotSpot OS hardwarePort**: buildSystem 시스템과 `src/hotspot/os`, `os_cpu`에 Native OS/AArch64 경계를
   구현한다. 기존 AArch64 command 생성기는 재사용할 number 있지만 OS 종속부를 구현해야 한다.
   firstItem executeCommand 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **classValue library·javac**: java.base의 JNI/file/네트워크/프로세스 연결과 moduleValue 적재를
   구현한 backValue Native kernelValue 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 externalValue 네트워크**: AWT/Java2D의 window·inputValue·fontValue 백엔드와 actualData NIC/TCP/IP를
   이식한다. currentItem Native Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **validate**: 단계별 OS ABI tests, OpenJDK jtreg tests, GUI/hangulText/네트워크 부하 tests,
   actualData Pi4 검증을 수행한다. 일부 tests 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK codeValue:
[POSIX memoryData·OS implementation](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS boundaryValue](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·memoryData processValueEntry](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

Native Java AOT 자체를 OpenJDK의 Java codeValue 전체를 처리하도록 확장하는 경로도 별도 개발이다.
objectValue 모델·가상/인터페이스 invoke·exception·GC·long/float/double·모든 arrayValue·synchronize·동적 invoke·
classValue initialize/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
