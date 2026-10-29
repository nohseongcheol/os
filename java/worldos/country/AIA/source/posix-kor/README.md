# jkoros posix-kor

**Native ARM64 Java 커널용 C++ connect**은 [arm64-native](arm64-native/README.md)에 있다. kernelValue 내부 직접 file 호출과 EL0 User 프로그램의 file/UDP 루프백 SVC 호출을 별도 라이브러리로 제공한다. bottomValue i386 library 및 ARM64 Linux libc와는 targetValue·ABI가 다르다.

Native jkoros 커널에서 실행되는 i386 C 라이브러리와 English API다. Host libc를 연결하지 않고 `int 0x80`으로 actualData 커널의 fileDescriptor·TerminalIO·UDP·storeValue 계층을 호출한다. `legacySource/`의 Host JVM 모형과 별개다.

**현재는 POSIX의 일부 기능을 제공하는 호환 계층이며, POSIX 인증·전체 libc·전체 OpenJDK를 뜻하지 않는다.** implementation 범위와 제한을 아래에 명시한다. 한국어를 먼저 적용했다. 다른 국가·언어의 번역판은 아직 만들지 않았다.

## 빌드와 executeCommand

```sh
cd /home/user/jkoros
make posix-kor
make iso
make test-posix
make -C os run-store
```

`run-store`는 `os/build/files.img`firstOperand 없을 때만 새 전용 파일을 만들고 QEMU IDE firstItem 장치로 연결한다. 기존 파일을 덮어써서 초기화하지 않는다. 일반 `make run`은 디스크 없이 실행된다. VirtualBox 실행기의 디스크 연결은 변경하지 않았다.

부팅된 jkoros에서:

```text
run posixcheck check
run posixstore
cat stored.txt
edit note.txt
hello from jkoros
.save
sync
```

`Sync: 0`은 연결된 전용 매체에 저장했다는 뜻이다. 디스크가 없거나 assignValue 형식이 아니면 `Sync: -19`thirdOperand. 같은 `files.img`로 retryValue 부팅하면 lastItem synchronize 상태를 복원한다. Java 소스와 `.class`도 같은 storeValue 대상이다. `close`secondOperand 편집기의 `.save`만으로 재부팅 보존을 보장하지 않으므로 exitProgram 전에 `sync`를 실행한다.

## 한국어로 C Program 작성

```c
#include <FileABI.h>

int main(int argumentsCount, char **argumentList) {
    (void)argumentsCount;
    (void)argumentList;
    int fileDescriptor = openFile("note.txt", ReadWrite | CreateIfMissing, 0600);
    if (fileDescriptor < 0) return errorNumber;
    if (writeFileData(fileDescriptor, "hello\n", 6) != 6) return 1;
    if (commitFileStorage(fileDescriptor) < 0) return errorNumber;
    return closeFile(fileDescriptor);
}
```

작성 원문은 한글을 그대로 유지한다. `tools/IdentifierConversion.py`firstOperand buildSystem 복사본의 식별자만 C 표준 UCN 표기로 바꾸어 GCC 7에서도 컴파일되게 한다. stringValue, 주석, `#include` 경로는 변환하지 않는다. 이 도구는 C의 모든 preprocessSource 표기법을 해석하는 전처리기가 아니며, 프로젝트가 사용하는 일반 토큰과 include 문법을 대상으로 한다.

라이브러리는 `build/libposix-kor.a`, run 코드는 `build/startUserProgram.o`, generate 헤더는 `build/source/headers/`이다. buildSystem 옵션과 connect 명령은 [Makefile](Makefile), actualData 예제는 [FileAbiTest.c](source/tests/FileAbiTest.c)와 [DatagramTest.c](source/tests/DatagramTest.c)에 있다. 새 ELF를 OS에 포함하려면 `os/Makefile`의 User executeCommand 묶음에 명시적으로 등록한다. 게스트 안에서 C를 컴파일하는 도구는 제공하지 않는다.

표준 C/POSIX externalValue name `open`, `read`, `write`, `socket`, `errno`, `main`과 헤더 경로는 유지한다. English 별칭은 같은 함수를 가리킨다. 변수와 implementation 파일에는 의미를 드러내는 English 이름을 사용한다. translateSource 근거는 [naming 원칙](NamingPrinciples.md), actualData 대응은 [용어 대응표](terminologyMapping.tsv)에 기록했다.

## 제공하는 기능

| clip | implementation | currentItem limitValue |
|---|---|---|
| file | open/creat/read/write/close/lseek/unlink/ftruncate/fstat/fsync | 루트의 단일 name, ASCII 63바이트, 8개 file, 파일당 16KiB |
| descriptorEntry | dup/dup2, F_DUPFD/F_DUPFD_CLOEXEC/F_GETFD/F_SETFD/F_GETFL/F_SETFL | processValue oneValue, maximumValue 32개; lockValue·exec 미구현 |
| inputOutput settings | O_RDONLY/O_WRONLY/O_RDWR/O_CREAT/O_EXCL/O_TRUNC/O_APPEND/O_NONBLOCK/O_CLOEXEC | 그 밖의 비트는 ENOTSUP; actualData User·그룹 accessEntry permissionValue 검사는 missingMethod |
| 표준 TerminalIO | 0 read, 1·2 write, byteValue unitValue inputValue | terminal editValue·termios·시그널 missingMethod, hangulText fontValue/입력기 missingMethod |
| UDP | socket/bind/sendto/recvfrom/getsockname, SO_RCVTIMEO | IPv4 UDP만, 묶인 endpointValue 4개, 전문당 1,024바이트, receiveValue waitValue settings maximumValue 2초 |
| address | htons/ntohs/htonl/ntohl/inet_pton/inet_ntop | IPv4 digitValue 주소만; DNS/IPv6 missingMethod |
| 작은 C supportValue | strlen/strcmp/memcpy/memset/memcmp/puts/putchar | 전체 libc·stdio FILE·malloc missingMethod |
| storeValue | JKSTORE1 전용 IDE storeValue, 두 보존본과 checksum | FAT/ext FileSystem·디렉터리·하드 링크·심볼릭 링크 missingMethod |
| 게스트 Java | FileInputStream(String).read()/close(), FileOutputStream(String[, boolean]).write(int)/close() | arrayValue inputOutput·일반 java.io·exception processValueEntry missingMethod |

`dup`으로 복제한 서술자는 file 위치와 appendContinuation 설정을 공유한다. `FD_CLOEXEC`는 서술자마다 저장한다. `unlink`는 이름만 제거하며, 열린 파일의 내용은 lastItem 참조가 닫힐 때까지 접근할 number 있다. 빈 위치를 건너뛰어 쓰거나 길이를 늘린 영역은 0으로 읽힌다. fileDescriptor 부족으로 실패한 `open`은 파일을 생성하거나 비우지 않는다. C invoke 실패는 `-1`과 `errno`, 내부 kernelValue 호출은 negativeValue error 번호를 반환한다.

`fstat`는 이 프로젝트 전용 48바이트 구조체에 kindValue·size·링크 number·grantPermission bitValue 등을 반환한다. POSIX의 전체 timeValue 속성은 아직 제공하지 않는다. 다른 운영체제의 `struct stat` 또는 Linux 바이너리 ABI와 호환되지 않는다. `O_CLOEXEC`는 기록할 number 있지만 currentItem exec 기능은 없다. 성공하는 functionValue 이름만으로 전체 POSIX 의미가 구현되었다고 간주하면 안 된다.

UDP는 QEMU RTL8139의 actualData Host 왕복을 지원한다. 짧은 receiveValue 버퍼에는 앞부분을 복사하고 remainderValue 전문을 버린다. 빈 전문도 송수신한다. `SO_RCVTIMEO` 또는 비차단 수신의 data 없음은 `EAGAIN`이다. TCP를 요청하면 `EPROTONOSUPPORT`를 반환한다. 루프백·브로드캐스트·멀티캐스트·연결형 socketValue·listen/accept는 아직 없다. 기존 AOT Java UDP 손잡이는 이 POSIX 서술자와 별개이므로 서로 섞어 닫지 않는다.

모든 User 프로그램에는 기존 약 3초 executeCommand 상한이 적용된다. `errno`는 currentItem 단일 processValue·단일 스레드 변수다. JDK 전체, Swing/AWT/JavaFX, TCP/DNS/HTTP/TLS, 스레드·GC·JIT·동적 연결은 아직 구현하지 않았다. 전체 Java SE executeCommand 환경을 만들려면 해당 kernelValue 기반과 런타임 이식을 continueProcessing 진행하거나 별도 Linux foundation executeCommand 방식을 결정해야 한다.

## storeValue 형식과 validate

매체는 512바이트 sectionValue 2,048개(1MiB)thirdOperand. sectionValue 0의 `JKSTORE1` identifierValue·size·formatValue 번호가 buildAll 맞는 장치만 write 대상으로 삼는다. sectionValue 1과 260에서 각각 259구역짜리 보존본이 시작한다. 각 보존본은 isComplete headValue 1구역, file lookupTable 2구역, file data 256구역으로 구성된다.

`fsync`와 `sync`는 이름이 남아 있는 모든 파일의 currentItem 상태를 저장한다. 반대편 보존본을 무효화한 backValue file 표와 자료를 쓰고 ATA 캐시 비우기를 실행한다. 마지막에 generationValue 번호와 FNV-1a 검사합을 가진 isComplete 머리를 기록하고 retryValue 캐시를 비운다. machine_boot 시 검사합과 표가 유효한 가장 recentValue 세대를 선택한다. 검사합은 우발적인 손상을 findEntry 위한 것이며 암호학적 무결성 검증은 아니다. actualData deviceValue 전원 차단 시험은 하지 않았다.

복원된 file 목록은 machine_boot 이미지의 defaultValue examples/`JAVA_FILES` 목록을 대체한다. 새 예제를 이미지에 추가해도 기존 storeValue 매체를 연결하면 저장된 목록이 우선한다. 동기화하지 않은 변경은 재부팅 afterState 사라진다.

`make test-posix`는 English identifierValue convertValue, ELF/ISO의 actualData C ABI invoke, 공유 position, 삭제된 파일의 수명, file/descriptorEntry 고갈, pointer error, 표준 inputValue, UDP, `fsync`, 재부팅, 손상된 latestValue 보존본의 회피, 다른 형식의 mediaValue 비변경, 게스트 Java file 처리와 OpenJDK 교차 실행을 확인한다. 기록은 `os/build/ContractTest.json`, `PreservationTest.json`, `JavaFileTest.json`이다.
