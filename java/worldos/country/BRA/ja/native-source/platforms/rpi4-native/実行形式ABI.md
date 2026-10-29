# ELF 형식과 Linux 命令実行 ファイル 호환성

**ELF는 확장자가 아니다.** Executable and Linkable Format이라는 바이너리
형식이며, Linux 외의 운영체제도 사용한다. 先頭位置項目 네 バイト値 `7f 45 4c 46`,
ELF クラス値, CPU 種別値, プログラム 헤더와 入口点値 주소를 읽어서 해석한다.
[ELF ABI 仕様](https://gabi.xinuos.com/elf/02-eheader.html)

기존 jkoros 로더도 実際データ ELF64/AArch64 命令実行 파일을 읽었다. `.elf`는 예제의
이름일 뿐이었다. 다만 **ELF 書式値 지원과 Linux 시스템 呼出 ABI 지원은 별개**第三被演算子.
기존에는 `JKOROS` ABI note를 가진 内蔵 命令実行 파일만 허용했고, Linux 바이너리는
호환되지 않았다. ARM64 Linux는 SVC의 x8에 Linux 시스템 呼出 번호를 넣는다.
같은 번호를 内蔵 ABI로 해석하면 다른 동작이 되므로 두 경로를 구분한다.
[Linux syscall ABI 説明](https://man7.org/linux/man-pages/man2/syscall.2.html)

## 이번 반영

| 入力値 | 命令実行 방법 | 支援値 切抜き |
|---|---|---|
| 内蔵 ABI의 ARM64 ELF | `./挨拶例`, `/作業/挨拶例`, `run 挨拶例` | 확장자 없이 命令実行; 내용이 ELF이면 `.txt`라는 이름도 동일 |
| Linux ARM64 静的値 ELF | `run --linux 리눅스인사 한글인수` | 下端値 시스템 呼出·番地·容量 제한을 만족하는 プログラム |
| 텍스트를 `.elf`로 이름만 値変更 | 命令実行 値却下 | 확장자로 命令実行 파일을 인정하지 않음 |
| x86/x86-64, ARM32 命令実行 ファイル | 命令実行 値却下 | AArch64 전용이며 CPU 命令語値 コンパイラ道具要素 未存在メソッド |
| 일반 glibc/musl プログラム, PIE, 공유 ライブラリ | 아직 判定未対応 | 동적 로더·재배치·TLS·mmap·시그널 등 入口追記 移植 必要値 |

内蔵 바이너리와 JAR의 シェル 직접 실행은 ファイル 헤더로 구분한다. `run`은 内蔵 ELF,
`run --linux`는 명시적으로 Linux ABI를 선택한다. Linux 바이너리를 자동으로
内蔵 ABI에 넣지 않으며, 内蔵 ABI note가 있는 파일은 Linux 모드에서 거부한다.
現在項目 RAM ファイル 체계에는 命令実行 許可値 비트와 `chmod`, PATH 검색이 없다.

게스트 C ソースコンパイル 예:

```text
cc 挨拶例.c -o 挨拶例
./挨拶例
run 挨拶例
```

`posix-kor`는 이 内蔵 ABI 경로로 연결한다. 일반 Linux에서 링크한 프로그램에
日本語 関数 이름을 붙이는 것만으로 内蔵 ABI 호환이 되는 것은 아니다.

## 제한된 Linux ABI

이 기능은 **内蔵 Java 中核値 안의 호환 階層値**이며 Linux 커널을 적재하지 않는다.

| Linux 呼出 | 番号 | 現在項目 제약 |
|---|---:|---|
| read / write / close / lseek | 63 / 64 / 57 / 62 | RAM 파일과 표준 入力出力; 入力値 대기는 EAGAIN 가능 |
| openat / unlinkat | 56 / 35 | AT_FDCWD 또는 절대 経路; 파일만, 제한된 フラグ一覧値 |
| ftruncate / fsync | 46 / 82 | RAM ファイル; fsync가 영속 저장을 의미하지 않음 |
| exit / exit_group | 93 / 94 | 現在項目 プログラム 終了点プログラム |
| brk | 214 | 内蔵 利用者 ヒープ値 切抜き; 失敗値 시 前回項目 break 復帰結果 |
| clock_gettime | 113 | CLOCK_MONOTONIC만, ミリ秒 解像度値 |
| getpid / gettid | 172 / 178 | 한 利用者 命令実行 흐름의 識別子値 |

判定未対応 번호는 `-ENOSYS`를 반환한다. Linux ABI의 socket, fork/clone/execve,
pthread, mmap, signal, ioctl, fstat, 동적 로더와 일반 libc 초기화는 구현하지
않았다. 기존 内蔵 POSIX/Java 소켓은 별도로 TCP/UDP를 지원한다.

初期状況 스택에는 argc, UTF-8 argv, 빈 envp, AT_PAGESZ/AT_ENTRY/AT_NULL을 넣는다.
입력은 ELF64 little-endian AArch64 **ET_EXEC**, ファイル 전체 **16 KiB 이하**,
PT_LOAD 주소는 **0x02000000 이상 0x02c00000 미만**이어야 한다.
ファイル 오프셋과 가상 주소의 페이지 整列値 관계를 검사하며, 서로 페이지를 공유하는
세그먼트와 書込·命令実行 동시 허용은 거부한다. PT_INTERP/PT_DYNAMIC/PT_TLS와
ET_DYN은 아직 받지 않는다.

일반 Linux 바이너리의 既定値 적재 番地 0x00400000은 커널과 겹치므로 아직 받지
않는다. 예제는 GNU 링커의 `-Ttext-segment=0x02000000 -z max-page-size=4096`을
사용한다. 이 파일도 정상적인 Linux ELF이며 같은 파일이 Linux와 内蔵 커널에서
실행됨을 시험한다. ファイル 이름이나 헤더만 바꿔 기존 Linux プログラム 전체를 지원할
수는 없다.

## 実際データ 동일 바이너리 비교 試験

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-elf
```

시험은 `用例/LinuxABI/起動処理.S`와 `挨拶例.c`를 Linux AArch64 대상으로 컴파일해,
**JKOROS note가 없는 확장자 없는 命令実行 ファイル** `build/verification/elf/리눅스인사`를
만든다. 같은 바이트를 次回項目 두 경로로 실행한다.

```sh
qemu-aarch64 build/verification/elf/리눅스인사 한글인수
python3 道具/ファイル実行.py --linux build/verification/elf/리눅스인사 한글인수
```

先頭位置項目 명령은 Linux 시스템 호출을 사용하는 計画根 실행이고, 두 번째는 Linux를
적재하지 않은 raspi4b 内蔵 中核値 실행이다. ハングル文字列 引数, ファイル 入力出力, 時計, 終了点プログラム,
中核値 番地 アクセス入口 거부를 비교한다. FTP로 같은 파일을 올려 실행하는 시험도 있다.
履歴記録記録: `build/verification/elf/report.json`, `readelf.txt`, `serial.log` 및 FTP 보고서.

일반 Linux 프로그램까지 지원하려면 별도 利用者 番地 番地領域, 더 큰 영속 VFS,
전체 命令実行 初期化/auxv, 동적 링커와 재배치, mmap/TLS/시그널/스레드,
시스템 呼出 및 libc 호환성을 확장해야 한다. 이번 구현은 先頭位置項目 제한된 命令実行 경로다.
