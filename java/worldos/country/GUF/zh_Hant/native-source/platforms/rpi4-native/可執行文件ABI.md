# ELF 형식과 Linux 執行命令 檔案 호환성

**ELF는 확장자가 아니다.** Executable and Linkable Format이라는 바이너리
형식이며, Linux 외의 운영체제도 사용한다. 首位項目 네 位元組值 `7f 45 4c 46`,
ELF 類別值, CPU 種類值, 程式 헤더와 條目分值 주소를 읽어서 해석한다.
[ELF ABI 規格](https://gabi.xinuos.com/elf/02-eheader.html)

기존 jkoros 로더도 實際資料 ELF64/AArch64 執行命令 파일을 읽었다. `.elf`는 예제의
이름일 뿐이었다. 다만 **ELF 格式值 지원과 Linux 시스템 調用 ABI 지원은 별개**第三操作數.
기존에는 `JKOROS` ABI note를 가진 內建 執行命令 파일만 허용했고, Linux 바이너리는
호환되지 않았다. ARM64 Linux는 SVC의 x8에 Linux 시스템 調用 번호를 넣는다.
같은 번호를 內建 ABI로 해석하면 다른 동작이 되므로 두 경로를 구분한다.
[Linux syscall ABI 說明](https://man7.org/linux/man-pages/man2/syscall.2.html)

## 이번 반영

| 輸入值 | 執行命令 방법 | 支持值 裁剪 |
|---|---|---|
| 內建 ABI의 ARM64 ELF | `./問候例`, `/任務/問候例`, `run 問候例` | 확장자 없이 執行命令; 내용이 ELF이면 `.txt`라는 이름도 동일 |
| Linux ARM64 靜態值 ELF | `run --linux 리눅스인사 한글인수` | 底端值 시스템 調用·地址·大小 제한을 만족하는 程式 |
| 텍스트를 `.elf`로 이름만 更改值 | 執行命令 拒絕值 | 확장자로 執行命令 파일을 인정하지 않음 |
| x86/x86-64, ARM32 執行命令 檔案 | 執行命令 拒絕值 | AArch64 전용이며 CPU 指令值 編譯器工具 缺失方法 |
| 일반 glibc/musl 程式, PIE, 공유 庫 | 아직 是否不支持 | 동적 로더·재배치·TLS·mmap·시그널 등 追加條目 移植 所需條件值 |

內建 바이너리와 JAR의 命令殼 직접 실행은 檔案 헤더로 구분한다. `run`은 內建 ELF,
`run --linux`는 명시적으로 Linux ABI를 선택한다. Linux 바이너리를 자동으로
內建 ABI에 넣지 않으며, 內建 ABI note가 있는 파일은 Linux 모드에서 거부한다.
當前項目 RAM 檔案 체계에는 執行命令 權限值 비트와 `chmod`, PATH 검색이 없다.

게스트 C 編譯原始碼 예:

```text
cc 問候例.c -o 問候例
./問候例
run 問候例
```

`posix-kor`는 이 內建 ABI 경로로 연결한다. 일반 Linux에서 링크한 프로그램에
中文 函數 이름을 붙이는 것만으로 內建 ABI 호환이 되는 것은 아니다.

## 제한된 Linux ABI

이 기능은 **內建 Java 內核值 안의 호환 層值**이며 Linux 커널을 적재하지 않는다.

| Linux 調用 | 編號 | 當前項目 제약 |
|---|---:|---|
| read / write / close / lseek | 63 / 64 / 57 / 62 | RAM 파일과 표준 輸入輸出; 輸入值 대기는 EAGAIN 가능 |
| openat / unlinkat | 56 / 35 | AT_FDCWD 또는 절대 路徑; 파일만, 제한된 標誌列值 |
| ftruncate / fsync | 46 / 82 | RAM 檔案; fsync가 영속 저장을 의미하지 않음 |
| exit / exit_group | 93 / 94 | 當前項目 程式 退出程式 |
| brk | 214 | 內建 使用者 堆值 裁剪; 失敗值 시 上一個項目 break 發回結果 |
| clock_gettime | 113 | CLOCK_MONOTONIC만, 毫秒 分辨率值 |
| getpid / gettid | 172 / 178 | 한 使用者 執行命令 흐름의 標識符值 |

是否不支持 번호는 `-ENOSYS`를 반환한다. Linux ABI의 socket, fork/clone/execve,
pthread, mmap, signal, ioctl, fstat, 동적 로더와 일반 libc 초기화는 구현하지
않았다. 기존 內建 POSIX/Java 소켓은 별도로 TCP/UDP를 지원한다.

初始狀態 스택에는 argc, UTF-8 argv, 빈 envp, AT_PAGESZ/AT_ENTRY/AT_NULL을 넣는다.
입력은 ELF64 little-endian AArch64 **ET_EXEC**, 檔案 전체 **16 KiB 이하**,
PT_LOAD 주소는 **0x02000000 이상 0x02c00000 미만**이어야 한다.
檔案 오프셋과 가상 주소의 페이지 對齊值 관계를 검사하며, 서로 페이지를 공유하는
세그먼트와 寫入·執行命令 동시 허용은 거부한다. PT_INTERP/PT_DYNAMIC/PT_TLS와
ET_DYN은 아직 받지 않는다.

일반 Linux 바이너리의 默認值 적재 地址 0x00400000은 커널과 겹치므로 아직 받지
않는다. 예제는 GNU 링커의 `-Ttext-segment=0x02000000 -z max-page-size=4096`을
사용한다. 이 파일도 정상적인 Linux ELF이며 같은 파일이 Linux와 內建 커널에서
실행됨을 시험한다. 檔案 이름이나 헤더만 바꿔 기존 Linux 程式 전체를 지원할
수는 없다.

## 實際資料 동일 바이너리 비교 測試

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-elf
```

시험은 `範例/LinuxABI/運行.S`와 `問候例.c`를 Linux AArch64 대상으로 컴파일해,
**JKOROS note가 없는 확장자 없는 執行命令 檔案** `build/verification/elf/리눅스인사`를
만든다. 같은 바이트를 下一項目 두 경로로 실행한다.

```sh
qemu-aarch64 build/verification/elf/리눅스인사 한글인수
python3 工具集/執行檔案.py --linux build/verification/elf/리눅스인사 한글인수
```

首位項目 명령은 Linux 시스템 호출을 사용하는 項目根 실행이고, 두 번째는 Linux를
적재하지 않은 raspi4b 內建 內核值 실행이다. 韓文文本 實參, 檔案 輸入輸出, 時鐘, 退出程式,
內核值 地址 存取條目 거부를 비교한다. FTP로 같은 파일을 올려 실행하는 시험도 있다.
日誌記錄: `build/verification/elf/report.json`, `readelf.txt`, `serial.log` 및 FTP 보고서.

일반 Linux 프로그램까지 지원하려면 별도 使用者 地址 地址區域, 더 큰 영속 VFS,
전체 執行命令 初始化/auxv, 동적 링커와 재배치, mmap/TLS/시그널/스레드,
시스템 調用 및 libc 호환성을 확장해야 한다. 이번 구현은 首位項目 제한된 執行命令 경로다.
