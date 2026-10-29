# ELF 형식과 Linux Esegui_comando file 호환성

**ELF는 확장자가 아니다.** Executable and Linkable Format이라는 바이너리
형식이며, Linux 외의 운영체제도 사용한다. 첫 네 byte_VALORE `7f 45 4c 46`,
ELF Corso_VALORE, CPU Kind_VALORE, app_f5044b9b 헤더와 punto_di_ingresso_VALORE 주소를 읽어서 해석한다.
[ELF ABI specifica](https://gabi.xinuos.com/elf/02-eheader.html)

기존 jkoros 로더도 effettivo_dati ELF64/AArch64 Esegui_comando 파일을 읽었다. `.elf`는 예제의
이름일 뿐이었다. 다만 **ELF formato_VALORE 지원과 Linux 시스템 호출 ABI 지원은 별개**다.
기존에는 `JKOROS` ABI note를 가진 nativo Esegui_comando 파일만 허용했고, Linux 바이너리는
호환되지 않았다. ARM64 Linux는 SVC의 x8에 Linux 시스템 호출 번호를 넣는다.
같은 번호를 nativo ABI로 해석하면 다른 동작이 되므로 두 경로를 구분한다.
[Linux syscall ABI 설명](https://man7.org/linux/man-pages/man2/syscall.2.html)

## 이번 반영

| input_VALORE | Esegui_comando 방법 | Supporto_VALORE ritagliare |
|---|---|---|
| nativo ABI의 ARM64 ELF | `./messaggio_di_saluto_ae353e94`, `/작업/messaggio_di_saluto_ae353e94`, `run messaggio_di_saluto_ae353e94` | 확장자 없이 Esegui_comando; 내용이 ELF이면 `.txt`라는 이름도 동일 |
| Linux ARM64 statico_VALORE ELF | `run --linux 리눅스인사 한글인수` | 아래 시스템 호출·e_mail·Dimensione 제한을 만족하는 app_f5044b9b |
| 텍스트를 `.elf`로 이름만 cambiare_VALORE | Esegui_comando rifiutare_VALORE | 확장자로 Esegui_comando 파일을 인정하지 않음 |
| x86/x86-64, ARM32 Esegui_comando file | Esegui_comando rifiutare_VALORE | AArch64 전용이며 CPU istruzione_VALORE_4c26ea1b compilatore_strumento 없음 |
| 일반 glibc/musl app_f5044b9b, PIE, 공유 Catalogo | 아직 미지원 | 동적 로더·재배치·TLS·mmap·시그널 등 Aggiunta_voce 이식 필요 |

nativo 바이너리와 JAR의 Shell 직접 실행은 file 헤더로 구분한다. `run`은 nativo ELF,
`run --linux`는 명시적으로 Linux ABI를 선택한다. Linux 바이너리를 자동으로
nativo ABI에 넣지 않으며, nativo ABI note가 있는 파일은 Linux 모드에서 거부한다.
Regolari_articolo RAM file 체계에는 Esegui_comando privilegio_VALORE 비트와 `chmod`, PATH 검색이 없다.

게스트 C compilare_fonte 예:

```text
cc messaggio_di_saluto_ae353e94.c -o messaggio_di_saluto_ae353e94
./messaggio_di_saluto_ae353e94
run messaggio_di_saluto_ae353e94
```

`posix-kor`는 이 nativo ABI 경로로 연결한다. 일반 Linux에서 링크한 프로그램에
Italiano FUNZIONE_VALORE 이름을 붙이는 것만으로 nativo ABI 호환이 되는 것은 아니다.

## 제한된 Linux ABI

이 기능은 **nativo Java kernel_VALORE 안의 호환 layer_VALORE**이며 Linux 커널을 적재하지 않는다.

| Linux 호출 | INDICE | Regolari_articolo 제약 |
|---|---:|---|
| read / write / close / lseek | 63 / 64 / 57 / 62 | RAM 파일과 표준 I_O; input_VALORE 대기는 EAGAIN 가능 |
| openat / unlinkat | 56 / 35 | AT_FDCWD 또는 절대 percorso; 파일만, 제한된 플래그 |
| ftruncate / fsync | 46 / 82 | RAM file; fsync가 영속 저장을 의미하지 않음 |
| exit / exit_group | 93 / 94 | Regolari_articolo app_f5044b9b Esci_app |
| brk | 214 | nativo spazio_utente heap_VALORE ritagliare; errore_VALORE 시 Indietro_articolo break Reso_KR |
| clock_gettime | 113 | CLOCK_MONOTONIC만, 밀리초 risoluzione_VALORE |
| getpid / gettid | 172 / 178 | 한 spazio_utente Esegui_comando 흐름의 identificatore_VALORE |

미지원 번호는 `-ENOSYS`를 반환한다. Linux ABI의 socket, fork/clone/execve,
pthread, mmap, signal, ioctl, fstat, 동적 로더와 일반 libc 초기화는 구현하지
않았다. 기존 nativo POSIX/Java 소켓은 별도로 TCP/UDP를 지원한다.

stato_iniziale 스택에는 argc, UTF-8 argv, 빈 envp, AT_PAGESZ/AT_ENTRY/AT_NULL을 넣는다.
입력은 ELF64 little-endian AArch64 **ET_EXEC**, file 전체 **16 KiB 이하**,
PT_LOAD 주소는 **0x02000000 이상 0x02c00000 미만**이어야 한다.
file 오프셋과 가상 주소의 페이지 allineare_VALORE 관계를 검사하며, 서로 페이지를 공유하는
세그먼트와 Scrittura·Esegui_comando 동시 허용은 거부한다. PT_INTERP/PT_DYNAMIC/PT_TLS와
ET_DYN은 아직 받지 않는다.

일반 Linux 바이너리의 valore_predefinito 적재 e_mail 0x00400000은 커널과 겹치므로 아직 받지
않는다. 예제는 GNU 링커의 `-Ttext-segment=0x02000000 -z max-page-size=4096`을
사용한다. 이 파일도 정상적인 Linux ELF이며 같은 파일이 Linux와 nativo 커널에서
실행됨을 시험한다. file 이름이나 헤더만 바꿔 기존 Linux app_f5044b9b 전체를 지원할
수는 없다.

## effettivo_dati 동일 바이너리 비교 prove

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-elf
```

시험은 `예제/리눅스ABI/avvia.S`와 `messaggio_di_saluto_ae353e94.c`를 Linux AArch64 대상으로 컴파일해,
**JKOROS note가 없는 확장자 없는 Esegui_comando file** `build/verification/elf/리눅스인사`를
만든다. 같은 바이트를 Avanti_articolo 두 경로로 실행한다.

```sh
qemu-aarch64 build/verification/elf/리눅스인사 한글인수
python3 strumenti/Esegui_File.py --linux build/verification/elf/리눅스인사 한글인수
```

첫 명령은 Linux 시스템 호출을 사용하는 azione_radice 실행이고, 두 번째는 Linux를
적재하지 않은 raspi4b nativo kernel_VALORE 실행이다. 한글 argomenti, file I_O, clock, Esci_app,
kernel_VALORE e_mail accesso_voce 거부를 비교한다. FTP로 같은 파일을 올려 실행하는 시험도 있다.
LOG_riga: `build/verification/elf/report.json`, `readelf.txt`, `serial.log` 및 FTP 보고서.

일반 Linux 프로그램까지 지원하려면 별도 spazio_utente e_mail e_mail_area, 더 큰 영속 VFS,
전체 Esegui_comando inizializza/auxv, 동적 링커와 재배치, mmap/TLS/시그널/스레드,
시스템 호출 및 libc 호환성을 확장해야 한다. 이번 구현은 첫 제한된 Esegui_comando 경로다.
