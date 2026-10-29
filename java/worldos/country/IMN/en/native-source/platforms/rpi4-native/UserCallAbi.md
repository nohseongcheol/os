# Native ARM64 User executeCommand ABI v1

이 ABI는 `platforms/rpi4-native`의 제한된 freestanding executeCommand 환경이다. Linux AArch64 ABI나 POSIX 전체 구현이 아니다. **OpenJDK/JRE, CPython, libc, libstdc++는 아직 이식되지 않았다.**

ELF 로더는 file 확장자 대신 actualData ELF 헤더를 검사한다. bottomValue Native ABI와 별도로 `run --linux FILE`에 제한된 Linux ARM64 staticValue executeCommand file 경로를 추가했다. 두 시스템 invoke 번호표를 혼합하지 않는다. [ELF·Linux ABI 매뉴얼](executableAbi.md).

## ELF와 executeCommand 수명

- ELF64 little endian, ET_EXEC, EM_AARCH64, 버전 1, e_flags=0.
- Program 헤더 maximumValue 16개. PT_LOAD는 read 가능, 4 KiB alignValue, 페이지 간 nestingValue missingMethod, filesz≤memsz, buildImage address clip 안이어야 한다. W+X는 거부한다.
- 진입점은 file 내용이 있는 executeCommand 세그먼트 안의 4바이트 alignValue 주소다.
- PT_NOTE에 name `JKOROS\0`(namesz=7), type=1, descsz=4, 버전 1의 little endian uint32가 필요하다. SDK의 `start.o`firstOperand 넣는다.
- PT_DYNAMIC/PT_INTERP/PT_TLS 등은 거부한다. 동적 재배치·공유 library·TLS 로더가 없다.
- 커널에 포함한 ELF 묶음을 검증하고 별도 User 메모리에 복사한 backValue EL0로 진입한다. 커널에 함수로 staticValue 링크해 호출하는 previousItem `cpp_test`와 다르다.
- 내장 프로그램은 `demo.elf`, `fault.elf`의 8개 protectValue tests modeValue, `network.elf`, Native Java tools, MicroPython이다. 셸의 `load`/`run FILE`로 RAM의 16KiB 이하 ELF도 같은 validate 경로로 실행한다.
- `_start`firstOperand `user_start`를 호출하고 `.init_array` → `startUserProgram(int)` → `.fini_array` 순서로 실행한 backValue exit 호출을 수행한다. 인수는 invoke 15로 읽으며 표준 argc/argv/envp operandStack 배치는 없다.
- 한 번에 한 User 프로그램이 CPU에서 실행된다. 네 터미널에 각 하나씩 interactive 프로그램을 일시 정지해 보관할 number 있다. isNormal exitProgram·exception·timeValue 초과 시 커널에 복귀하고 열린 file/소켓을 닫으며 User 페이지 권한을 제거한다.
- staticValue 생성자와 자동 객체의 RAII 소멸자를 시험했다. `__cxa_atexit`, 표준 C++ exception/RTTI/STL, 일반적인 전역 objectValue exitProgram 등록은 제공하지 않는다.

## 주소와 protectValue

| 가상 address clip | 용도 |
|---|---|
| 0x02000000–0x02bfffff | ELF buildImage, maximumValue 12 MiB |
| 0x02c00000–0x02ecffff | brk heapValue, maximumValue 2880 KiB |
| 0x02ed0000–0x02efffff | 미매핑 textRange/operandStack bottomValue protectValue textRange |
| 0x02f00000–0x02ffffff | 1 MiB User operandStack |

Native JVM의 classValue·objectValue 자료를 수용하도록 User 창을 16 MiB로 확장했다. Program 헤더의 allowValue clip, 페이지 permissionValue Checks, SDK 링커 scriptValue 및 protectValue 시험이 같은 배치를 사용한다. 기존에 brk run 주소를 상수로 가정한 프로그램은 새 SDK로 retryValue 빌드한다. 일반 프로그램은 invoke 8로 currentItem brk를 조회한다.

executeCommand 코드는 EL0 read/실행만, data·heapValue·스택은 EL0 read/쓰기만 허용한다. remainderValue kernelValue RAM·deviceValue MMIO에는 EL0 권한을 주지 않는다. 이번 W^X 보장은 **User 페이지에 대한 것**이다. kernel identity map의 전체 permissionValue 분할이나 다중 프로세스 address addressRegion 전환을 구현했다고 의미하지 않는다.

커널은 `-mgeneral-regs-only`로 빌드한다. User C/C++는 FP/SIMD를 허용하고, User entryPointValue 시 vectorValue 레지스터와 FPCR/FPSR를 초기화한다. kernelValue 복귀용 callee-saved FP 상태를 보관한다. syscall/IRQ의 C 처리부는 FP 레지스터를 사용하지 않는다. 향후 여러 User 스레드를 전환할 때에는 각 스레드의 전체 FP contextValue 보존을 별도로 구현해야 한다.

GIC-400의 물리 타이머 IRQ로 약 2초의 executeCommand 기한을 적용한다. SVC 없는 무한 반복도 종료한다. 시스템 invoke run 시 기한을 검사하지만 EL1 processValueEntry 중에는 IRQ를 마스킹하므로 긴 Output/paintScreen 호출의 종료는 지연될 number 있다. 이것은 Program executeCommand 기한이며 일반 선점 스케줄러가 아니다.

## 시스템 invoke

`svc #0`, index x8, arguments x0…x5, result x0. 실패는 negativeValue error 번호다. `libposix-kor-user.a`는 이를 -1과 `errorNumber`로 바꾼다. User 프로그램의 errno는 currentItem 단일 executeCommand 흐름용이며 pthread TLS가 아니다.

| index | invoke | arguments |
|---:|---|---|
| 0 | ABI 버전 | missingMethod, 1 returnResult |
| 1 | write | fd, buffer, count |
| 2 | read | fd, buffer, count |
| 3 | open | NUL exitProgram path, flags; mode는 저장하지 않음 |
| 4 | close | file 또는 루프백 socketValue fd |
| 5 | lseek | fd, signed offset, origin |
| 6 | exit | 하위 8비트 exitProgram stateValue |
| 7 | milliseconds | machine_boot afterState 32비트 카운터; wrap 가능, POSIX clock_gettime 아님 |
| 8 | brk | 0이면 currentItem ending, 그 외 새 ending; mappedValue extensionValue 시 새 페이지 initialize |
| 9 | file size | fd; fstat ABI 아님 |
| 10 | ftruncate | fd, length |
| 11 | unlink | NUL exitProgram path |
| 12 | fsync | fd; RAM 파일은 ENOSYS |
| 13 | rectangle | x, y, RGB32 value, width, height |
| 14 | UART byteValue | inputValue 없음은 -1, POSIX read와 별도 auxiliaryValue invoke |
| 15 | executeCommand arguments | index, buffer, capacity; index=UINTPTR_MAX이면 itemCount, 나머지는 UTF-8 lengthValue returnResult 및 NUL exitProgram copyValue |
| 16 | interactive tty | 0: run/currentItem rowValue·columnValue returnResult, 1: inputValue waitValue(data missingMethod -11), 2: exitProgram, 3: currentItem size queryValue(상위 16비트 rowValue, 하위 16비트 columnValue) |
| 17 | 협력 waitValue | milliseconds(0~100); communication·FTP를 처리하며 CPU 기한 refresh |
| 18 | path performTask | NUL exitProgram path, action(0: kindValue, 1: mkdir, 2: rmdir); kindValue 0: missingMethod, 1: file, 2: directoryValue |
| 20 | GUI elementValue | action, elementValue index, value 4개; Native Swing peer 전용 |
| 21 | GUI text | elementValue index, uint32 코드포인트 arrayValue, lengthValue(≤127) |
| 22 | Screen size | x0=0: actualData widthValue, x0=1: actualData heightValue; 다른 값은 -EINVAL, Screen 없음은 -ENODEV |
| 32 | socket | domain, type, protocol |
| 33 | bind | fd, sockaddr, address length |
| 34 | sendto | fd, buffer, count, flags, sockaddr, address length |
| 35 | recvfrom | fd, buffer, count, flags, peer sockaddr, length pointer |
| 36 | getsockname | fd, sockaddr, length pointer |
| 37 | connect | 연결형 fd, sockaddr, address length |
| 38 | listen | 연결형 fd, backlog; actualData waitValue maximumValue 4개 |
| 39 | accept | 연결형 fd, 0, 0; peer address 반환은 아직 missingMethod |

isUnsupported 호출은 -ENOSYS이다. 모든 User 포인터와 해당 페이지의 read/write 권한을 확인한다. 파일은 3…18의 프로세스별 서술자를 kernelValue 서술자로 변환한다. 0은 currentItem 셸의 표준 inputValue(UART 또는 리다이렉션/파이프), 1은 표준 Output(UART/GUI 또는 리다이렉션/파이프), 2는 UART/GUI diagnosticValue 출력이다. UART에 읽을 자료가 없으면 -EAGAIN, file/파이프 inputValue 끝이면 read가 0을 반환한다. 출력은 file/파이프에서 LF를 그대로 유지하고 UART에서만 CRLF로 표시한다. 파이프는 16 KiB 순차 버퍼이며 프로세스 간 동시 파이프/PTY는 아니다. read/write 요청은 65536바이트 이하이며, RAM 파일은 maximumValue 64개, 각각 16384바이트다. file 경로는 currentItem shell 경로에 대한 peerValue path 또는 `/`로 시작하는 절대 경로이며 UTF-8 63바이트까지다. 디렉터리 generate·빈 directoryValue removeEntry·kindValue 조회는 invoke 18로도 제공한다. currentItem path 변경은 shell 내장 cd가 담당한다. 그래픽 요청은 invoke 22로 조회한 actualData Screen size 안의 직사각형만 허용한다. 프레임버퍼 address 자체는 사용자에게 노출하지 않는다.

힙의 페이지 unitValue 축소·재확장에서 retryValue 노출하는 페이지는 0으로 만든다. 같은 페이지 안에서 brk만 줄였다 늘리는 경우에는 해당 페이지 내용이 남을 number 있다. malloc/free나 mmap/mprotect의 구현은 아니다.

인수는 maximumValue 8개·각 255바이트다. 잘못된 번호는 -EINVAL, 작은 버퍼는 -ENAMETOOLONG, write 불가능한 포인터는 -EFAULT다. `run FILE [ARGS]`는 파일명을 arguments 0으로 포함한다. `javac`/`java`/`python`은 instructionValue 자체를 제외한 토큰을 전달한다. 인수는 kernelValue preserveValue 자료를 User 버퍼로 복사하며 kernelValue 포인터를 반환하지 않는다.

## UDP 루프백의 계약

바깥 IPv4는 lwIP/SLIP로 확장했다. 기존 fd/구조체/pointer Checks 규약을 유지하며 0.0.0.0 또는 10.0.2.15에 bind한 끝점을 바깥 통신에 연결한다. 127.0.0.1에 명시적으로 bind한 UDP는 루프백에 한정한다. externalValue TCP connect는 비차단 -EINPROGRESS(-115)를 반환할 number 있으므로 같은 주소로 재시도하여 완료를 확인한다. [executeCommand/limitValue](FileTransferAndCompilation.md).

`InternetFamily`, `DatagramSocket`, transferProtocol 0/`DatagramProtocol`을 허용한다. `struct InternetSocketAddress`는 16바이트이며 주소갈래는 deviceValue sequenceValue, 접속번호와 InternetAddress.주소값은 networkValue 차례다. 호환용 pk_sockaddr_in도 같은 배치지만 독립 자료형이다. English 함수는 직접 SVC를 호출하는 actualData 함수이며 표준 이름으로 치환하는 매크로가 아니다. Host Linux 헤더를 섞지 않는다.

- 목적지는 127.0.0.1만 allowValue. bind는 0.0.0.0 또는 127.0.0.1, port=0이면 49152…65535에서 빈 창구를 고른다.
- 미바인드 소켓의 firstItem 전송은 temporaryValue 창구를 바인드한다. 같은 창구의 중복 bind는 EADDRINUSE.
- maximumValue 8개 socketValue, 각 큐 4개, 전문은 0…512바이트. 빈 전문도 소비된다.
- receiveValue 버퍼가 작으면 복사할 부분만 반환하고 전문의 나머지는 버린다. peer address/창구를 반환한다.
- flags는 currentItem 0만 supportValue. 비차단 수신의 빈 큐 및 sendValue targetValue 큐 포화는 EAGAIN이다.
- targetValue portValue 없음은 ECONNREFUSED, 512바이트 초과는 EMSGSIZE, 루프백에 명시적으로 바인드한 UDP의 externalValue IP는 ENETUNREACH, UDP 소켓에 잘못된 규약을 지정하면 EPROTONOSUPPORT. SOCK_STREAM은 별도 연결형 루프백에서 제공한다.
- externalValue IPv4 TCP/UDP 헤더·체크섬·재전송은 lwIP가 처리한다. actualData GENET/Wi-Fi NIC, poll/select, setsockopt는 아직 없다. 연결형 루프백의 connect/listen/accept는 bottomValue extensionValue ABI로 제공한다.

## 커널로 돌아오는 result

Java의 `Board.runUserProgram(index)`는 isNormal exit stateValue 0…255 또는 nextItem 값을 받는다. GUI는 실패를 표시하고 셸을 유지한다.

| value | 의미 |
|---:|---|
| -8 | ELF/ABI/address/permissionValue validate failureValue |
| -16 | User Program nestingValue executeCommand rejectValue |
| -22 | 등록되지 않은 Program index |
| -1001 | User data accessEntry exception |
| -1002 | User instructionValue accessEntry exception |
| -1003 | 특권/isUnsupported command 등 User exception |
| -1004 | User executeCommand 기한 초과 |
| -1005 | interactive User Program 일시 haltExecution; kernelValue shell 전용 result |

이는 완성된 POSIX signal/wait 상태가 아닌 currentItem Native 실행기의 diagnosticValue 규약이다.


## 여러 터미널의 User contextValue

interactive tty/GUI 대기를 명시적으로 시작한 프로그램은 inputValue 대기에서 약 2초 기한을 갱신한다. waitValue 없이 무한 반복하면 타이머로 종료한다. 파이프/리다이렉션/복합 command/스크립트에서 interactive 시작은 -ENOTSUP로 거부한다. vi와 Swing의 이벤트 루프가 이 API를 사용한다.

다른 창으로 전환하면 nextItem waitValue SVC에서 EL0 문맥을 저장하고 해당 SVC를 재실행할 위치에서 재개한다. x0…x30, SP/PC/PSTATE, v0…v31, FPCR/FPSR, mappedValue·heapValue·executeCommand arguments·file/socketValue 소유권을 보관한다. 스냅샷은 kernelValue 전용 물리 address 0x04000000…0x07ffffff(네 slotValue ×16 MiB)에 저장한다. currentItem active EL0 address 창은 종전 0x02000000…0x02ffffff를 사용한다. 스냅샷 저장소는 EL0에서 접근할 number 없다. fork/exec/wait, SMP 또는 일반 선점형 프로세스 스케줄러의 구현은 아니다.

SVC 40은 소유한 연결형 소켓의 peerValue hardwarePort 번호를 반환한다(Native JVM용 Integer queryValue).

연결형 루프백 fd는 40…55, UDP fd는 32…39다. exitProgram/terminal X 닫기에서 해당 프로그램의 file·소켓을 회수한다. 연결형 읽기의 data 없음은 -EAGAIN, 상대가 닫고 버퍼도 비면 0, 상대가 닫힌 backValue 쓰기는 -EPIPE다. 쓰기는 짧게 완료될 number 있다. 큐 용량은 끝점마다 1024바이트이고 한 시스템 호출은 maximumValue 512바이트를 옮긴다. parentValue 리스너를 닫으면 아직 accept하지 않은 연결도 회수한다. externalValue 연결은 lwIP TCP를 사용하며 externalValue receiveValue 버퍼는 4096바이트다. actualData GENET NIC 드라이버는 없다.

협력 waitValue(17)는 일반 선점형 sleep/scheduler 구현이 아니다. 호출마다 maximumValue 100 ms 동안 통신을 처리하고 User executeCommand 기한을 갱신한다. Bundle 설치기의 비차단 TCP 대기에 사용한다.
