# ELF 형식과 Linux Provést_příkaz název_souboru 호환성

**ELF는 확장자가 아니다.** Executable and Linkable Format이라는 바이너리
형식이며, Linux 외의 운영체제도 사용한다. 첫 네 bajt_HODNOTA `7f 45 4c 46`,
ELF Třída_HODNOTA, CPU Druh_HODNOTA, program_f5044b9b 헤더와 vstupní_bod_HODNOTA 주소를 읽어서 해석한다.
[ELF ABI 명세](https://gabi.xinuos.com/elf/02-eheader.html)

기존 jkoros 로더도 skutečný_data ELF64/AArch64 Provést_příkaz 파일을 읽었다. `.elf`는 예제의
이름일 뿐이었다. 다만 **ELF formát_HODNOTA 지원과 Linux 시스템 호출 ABI 지원은 별개**다.
기존에는 `JKOROS` ABI note를 가진 vlastní Provést_příkaz 파일만 허용했고, Linux 바이너리는
호환되지 않았다. ARM64 Linux는 SVC의 x8에 Linux 시스템 호출 번호를 넣는다.
같은 번호를 vlastní ABI로 해석하면 다른 동작이 되므로 두 경로를 구분한다.
[Linux syscall ABI 설명](https://man7.org/linux/man-pages/man2/syscall.2.html)

## 이번 반영

| vstup_HODNOTA | Provést_příkaz 방법 | vzpěra_HODNOTA oříznout |
|---|---|---|
| vlastní ABI의 ARM64 ELF | `./인사`, `/작업/인사`, `run 인사` | 확장자 없이 Provést_příkaz; 내용이 ELF이면 `.txt`라는 이름도 동일 |
| Linux ARM64 statický_HODNOTA ELF | `run --linux 리눅스인사 한글인수` | 아래 시스템 호출·Adresa·Velikost 제한을 만족하는 program_f5044b9b |
| 텍스트를 `.elf`로 이름만 změnit_HODNOTA | Provést_příkaz odmítnout_HODNOTA | 확장자로 Provést_příkaz 파일을 인정하지 않음 |
| x86/x86-64, ARM32 Provést_příkaz název_souboru | Provést_příkaz odmítnout_HODNOTA | AArch64 전용이며 CPU 명령어 kompilátor_nástroj 없음 |
| 일반 glibc/musl program_f5044b9b, PIE, 공유 knihovna | 아직 미지원 | 동적 로더·재배치·TLS·mmap·시그널 등 Připojit_položka 이식 필요 |

vlastní 바이너리와 JAR의 prostředí 직접 실행은 název_souboru 헤더로 구분한다. `run`은 vlastní ELF,
`run --linux`는 명시적으로 Linux ABI를 선택한다. Linux 바이너리를 자동으로
vlastní ABI에 넣지 않으며, vlastní ABI note가 있는 파일은 Linux 모드에서 거부한다.
dobrá_zboží RAM název_souboru 체계에는 Provést_příkaz oprávnění_HODNOTA 비트와 `chmod`, PATH 검색이 없다.

게스트 C kompilovat_zdroj 예:

```text
cc 인사.c -o 인사
./인사
run 인사
```

`posix-kor`는 이 vlastní ABI 경로로 연결한다. 일반 Linux에서 링크한 프로그램에
čeština funkce_HODNOTA 이름을 붙이는 것만으로 vlastní ABI 호환이 되는 것은 아니다.

## 제한된 Linux ABI

이 기능은 **vlastní Java jádro_HODNOTA 안의 호환 vrstva_HODNOTA**이며 Linux 커널을 적재하지 않는다.

| Linux 호출 | INDEX | dobrá_zboží 제약 |
|---|---:|---|
| read / write / close / lseek | 63 / 64 / 57 / 62 | RAM 파일과 표준 vstup_a_výstup; vstup_HODNOTA 대기는 EAGAIN 가능 |
| openat / unlinkat | 56 / 35 | AT_FDCWD 또는 절대 cesta_2; 파일만, 제한된 플래그 |
| ftruncate / fsync | 46 / 82 | RAM název_souboru; fsync가 영속 저장을 의미하지 않음 |
| exit / exit_group | 93 / 94 | dobrá_zboží program_f5044b9b Konec_program |
| brk | 214 | vlastní uživatelský_prostor halda_HODNOTA oříznout; selhání_HODNOTA 시 Předchozí_zboží break Vratka_KV |
| clock_gettime | 113 | CLOCK_MONOTONIC만, 밀리초 řešení_HODNOTA |
| getpid / gettid | 172 / 178 | 한 uživatelský_prostor Provést_příkaz 흐름의 identifikátor_HODNOTA |

미지원 번호는 `-ENOSYS`를 반환한다. Linux ABI의 socket, fork/clone/execve,
pthread, mmap, signal, ioctl, fstat, 동적 로더와 일반 libc 초기화는 구현하지
않았다. 기존 vlastní POSIX/Java 소켓은 별도로 TCP/UDP를 지원한다.

počáteční_stav 스택에는 argc, UTF-8 argv, 빈 envp, AT_PAGESZ/AT_ENTRY/AT_NULL을 넣는다.
입력은 ELF64 little-endian AArch64 **ET_EXEC**, název_souboru 전체 **16 KiB 이하**,
PT_LOAD 주소는 **0x02000000 이상 0x02c00000 미만**이어야 한다.
název_souboru 오프셋과 가상 주소의 페이지 zarovnat_HODNOTA 관계를 검사하며, 서로 페이지를 공유하는
세그먼트와 Zápis·Provést_příkaz 동시 허용은 거부한다. PT_INTERP/PT_DYNAMIC/PT_TLS와
ET_DYN은 아직 받지 않는다.

일반 Linux 바이너리의 výchozí_hodnota 적재 Adresa 0x00400000은 커널과 겹치므로 아직 받지
않는다. 예제는 GNU 링커의 `-Ttext-segment=0x02000000 -z max-page-size=4096`을
사용한다. 이 파일도 정상적인 Linux ELF이며 같은 파일이 Linux와 vlastní 커널에서
실행됨을 시험한다. název_souboru 이름이나 헤더만 바꿔 기존 Linux program_f5044b9b 전체를 지원할
수는 없다.

## skutečný_data 동일 바이너리 비교 zkoušky

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-elf
```

시험은 `예제/리눅스ABI/Spustit_2.S`와 `인사.c`를 Linux AArch64 대상으로 컴파일해,
**JKOROS note가 없는 확장자 없는 Provést_příkaz název_souboru** `build/verification/elf/리눅스인사`를
만든다. 같은 바이트를 Další_zboží 두 경로로 실행한다.

```sh
qemu-aarch64 build/verification/elf/리눅스인사 한글인수
python3 nástroje/Provést_Soubor.py --linux build/verification/elf/리눅스인사 한글인수
```

첫 명령은 Linux 시스템 호출을 사용하는 akce_kořen 실행이고, 두 번째는 Linux를
적재하지 않은 raspi4b vlastní jádro_HODNOTA 실행이다. 한글 argumenty, název_souboru vstup_a_výstup, Hodiny, Konec_program,
jádro_HODNOTA Adresa přístup_položka 거부를 비교한다. FTP로 같은 파일을 올려 실행하는 시험도 있다.
LOGZ_ZÁZNAM: `build/verification/elf/report.json`, `readelf.txt`, `serial.log` 및 FTP 보고서.

일반 Linux 프로그램까지 지원하려면 별도 uživatelský_prostor Adresa ODKAZ_oblast, 더 큰 영속 VFS,
전체 Provést_příkaz inicializovat/auxv, 동적 링커와 재배치, mmap/TLS/시그널/스레드,
시스템 호출 및 libc 호환성을 확장해야 한다. 이번 구현은 첫 제한된 Provést_příkaz 경로다.
