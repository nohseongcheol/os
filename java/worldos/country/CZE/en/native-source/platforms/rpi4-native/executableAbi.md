# ELF 형식과 Linux executeCommand file 호환성

**ELF는 확장자가 아니다.** Executable and Linkable Format이라는 바이너리
형식이며, Linux 외의 운영체제도 사용한다. firstItem 네 byteValue `7f 45 4c 46`,
ELF classValue, CPU kindValue, Program 헤더와 entryPointValue 주소를 읽어서 해석한다.
[ELF ABI specification](https://gabi.xinuos.com/elf/02-eheader.html)

기존 jkoros 로더도 actualData ELF64/AArch64 executeCommand 파일을 읽었다. `.elf`는 예제의
이름일 뿐이었다. 다만 **ELF formatValue 지원과 Linux 시스템 invoke ABI 지원은 별개**thirdOperand.
기존에는 `JKOROS` ABI note를 가진 Native executeCommand 파일만 허용했고, Linux 바이너리는
호환되지 않았다. ARM64 Linux는 SVC의 x8에 Linux 시스템 invoke 번호를 넣는다.
같은 번호를 Native ABI로 해석하면 다른 동작이 되므로 두 경로를 구분한다.
[Linux syscall ABI description](https://man7.org/linux/man-pages/man2/syscall.2.html)

## 이번 반영

| inputValue | executeCommand 방법 | supportValue clip |
|---|---|---|
| Native ABI의 ARM64 ELF | `./Greeting`, `/performTask/Greeting`, `run Greeting` | 확장자 없이 executeCommand; 내용이 ELF이면 `.txt`라는 이름도 동일 |
| Linux ARM64 staticValue ELF | `run --linux 리눅스인사 한글인수` | bottomValue 시스템 invoke·address·size 제한을 만족하는 Program |
| 텍스트를 `.elf`로 이름만 changeValue | executeCommand rejectValue | 확장자로 executeCommand 파일을 인정하지 않음 |
| x86/x86-64, ARM32 executeCommand file | executeCommand rejectValue | AArch64 전용이며 CPU instructionValue compilerTool missingMethod |
| 일반 glibc/musl Program, PIE, 공유 library | 아직 isUnsupported | 동적 로더·재배치·TLS·mmap·시그널 등 appendEntry Porting neededValue |

Native 바이너리와 JAR의 shell 직접 실행은 file 헤더로 구분한다. `run`은 Native ELF,
`run --linux`는 명시적으로 Linux ABI를 선택한다. Linux 바이너리를 자동으로
Native ABI에 넣지 않으며, Native ABI note가 있는 파일은 Linux 모드에서 거부한다.
currentItem RAM file 체계에는 executeCommand permissionValue 비트와 `chmod`, PATH 검색이 없다.

게스트 C compileSource 예:

```text
cc Greeting.c -o Greeting
./Greeting
run Greeting
```

`posix-kor`는 이 Native ABI 경로로 연결한다. 일반 Linux에서 링크한 프로그램에
English functionValue 이름을 붙이는 것만으로 Native ABI 호환이 되는 것은 아니다.

## 제한된 Linux ABI

이 기능은 **Native Java kernelValue 안의 호환 layerValue**이며 Linux 커널을 적재하지 않는다.

| Linux invoke | index | currentItem 제약 |
|---|---:|---|
| read / write / close / lseek | 63 / 64 / 57 / 62 | RAM 파일과 표준 inputOutput; inputValue 대기는 EAGAIN 가능 |
| openat / unlinkat | 56 / 35 | AT_FDCWD 또는 절대 path; 파일만, 제한된 flagsValue |
| ftruncate / fsync | 46 / 82 | RAM file; fsync가 영속 저장을 의미하지 않음 |
| exit / exit_group | 93 / 94 | currentItem Program exitProgram |
| brk | 214 | Native User heapValue clip; failureValue 시 previousItem break returnResult |
| clock_gettime | 113 | CLOCK_MONOTONIC만, milliseconds resolutionValue |
| getpid / gettid | 172 / 178 | 한 User executeCommand 흐름의 identifierValue |

isUnsupported 번호는 `-ENOSYS`를 반환한다. Linux ABI의 socket, fork/clone/execve,
pthread, mmap, signal, ioctl, fstat, 동적 로더와 일반 libc 초기화는 구현하지
않았다. 기존 Native POSIX/Java 소켓은 별도로 TCP/UDP를 지원한다.

initialState 스택에는 argc, UTF-8 argv, 빈 envp, AT_PAGESZ/AT_ENTRY/AT_NULL을 넣는다.
입력은 ELF64 little-endian AArch64 **ET_EXEC**, file 전체 **16 KiB 이하**,
PT_LOAD 주소는 **0x02000000 이상 0x02c00000 미만**이어야 한다.
file 오프셋과 가상 주소의 페이지 alignValue 관계를 검사하며, 서로 페이지를 공유하는
세그먼트와 write·executeCommand 동시 허용은 거부한다. PT_INTERP/PT_DYNAMIC/PT_TLS와
ET_DYN은 아직 받지 않는다.

일반 Linux 바이너리의 defaultValue 적재 address 0x00400000은 커널과 겹치므로 아직 받지
않는다. 예제는 GNU 링커의 `-Ttext-segment=0x02000000 -z max-page-size=4096`을
사용한다. 이 파일도 정상적인 Linux ELF이며 같은 파일이 Linux와 Native 커널에서
실행됨을 시험한다. file 이름이나 헤더만 바꿔 기존 Linux Program 전체를 지원할
수는 없다.

## actualData 동일 바이너리 비교 tests

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-elf
```

시험은 `examples/LinuxAbi/run.S`와 `Greeting.c`를 Linux AArch64 대상으로 컴파일해,
**JKOROS note가 없는 확장자 없는 executeCommand file** `build/verification/elf/리눅스인사`를
만든다. 같은 바이트를 nextItem 두 경로로 실행한다.

```sh
qemu-aarch64 build/verification/elf/리눅스인사 한글인수
python3 tools/executeFile.py --linux build/verification/elf/리눅스인사 한글인수
```

firstItem 명령은 Linux 시스템 호출을 사용하는 projectRoot 실행이고, 두 번째는 Linux를
적재하지 않은 raspi4b Native kernelValue 실행이다. hangulText arguments, file inputOutput, Clock, exitProgram,
kernelValue address accessEntry 거부를 비교한다. FTP로 같은 파일을 올려 실행하는 시험도 있다.
logRecord: `build/verification/elf/report.json`, `readelf.txt`, `serial.log` 및 FTP 보고서.

일반 Linux 프로그램까지 지원하려면 별도 User address addressRegion, 더 큰 영속 VFS,
전체 executeCommand initialize/auxv, 동적 링커와 재배치, mmap/TLS/시그널/스레드,
시스템 invoke 및 libc 호환성을 확장해야 한다. 이번 구현은 firstItem 제한된 executeCommand 경로다.
