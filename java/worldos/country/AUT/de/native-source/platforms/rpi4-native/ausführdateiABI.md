# ELF 형식과 Linux befehlAusführen Datei 호환성

**ELF는 확장자가 아니다.** Executable and Linkable Format이라는 바이너리
형식이며, Linux 외의 운영체제도 사용한다. ersterElementeintrag 네 byteWert `7f 45 4c 46`,
ELF klasseWert, CPU artWert, Programm 헤더와 eintragPunktWert 주소를 읽어서 해석한다.
[ELF ABI vorgabe](https://gabi.xinuos.com/elf/02-eheader.html)

기존 jkoros 로더도 tatsächlichDaten ELF64/AArch64 befehlAusführen 파일을 읽었다. `.elf`는 예제의
이름일 뿐이었다. 다만 **ELF formatWert 지원과 Linux 시스템 aufrufen ABI 지원은 별개**dritterOperand.
기존에는 `JKOROS` ABI note를 가진 eigen befehlAusführen 파일만 허용했고, Linux 바이너리는
호환되지 않았다. ARM64 Linux는 SVC의 x8에 Linux 시스템 aufrufen 번호를 넣는다.
같은 번호를 eigen ABI로 해석하면 다른 동작이 되므로 두 경로를 구분한다.
[Linux syscall ABI beschreibung](https://man7.org/linux/man-pages/man2/syscall.2.html)

## 이번 반영

| Eingabewert | befehlAusführen 방법 | unterstützungWert beschneiden |
|---|---|---|
| eigen ABI의 ARM64 ELF | `./Gruß`, `/Aufgabe/Gruß`, `run Gruß` | 확장자 없이 befehlAusführen; 내용이 ELF이면 `.txt`라는 이름도 동일 |
| Linux ARM64 statischWert ELF | `run --linux 리눅스인사 한글인수` | unterkanteWert 시스템 aufrufen·adresse·größe 제한을 만족하는 Programm |
| 텍스트를 `.elf`로 이름만 wertÄndern | befehlAusführen wertZurückweisen | 확장자로 befehlAusführen 파일을 인정하지 않음 |
| x86/x86-64, ARM32 befehlAusführen Datei | befehlAusführen wertZurückweisen | AArch64 전용이며 CPU befehlswortWert übersetzerWerkzeug fehlendMethode |
| 일반 glibc/musl Programm, PIE, 공유 bibliothek | 아직 istNichtUnterstützt | 동적 로더·재배치·TLS·mmap·시그널 등 eintragAnhängen Portierung benötigtWert |

eigen 바이너리와 JAR의 befehlshülle 직접 실행은 Datei 헤더로 구분한다. `run`은 eigen ELF,
`run --linux`는 명시적으로 Linux ABI를 선택한다. Linux 바이너리를 자동으로
eigen ABI에 넣지 않으며, eigen ABI note가 있는 파일은 Linux 모드에서 거부한다.
aktuellElementeintrag RAM Datei 체계에는 befehlAusführen erlaubnisWert 비트와 `chmod`, PATH 검색이 없다.

게스트 C quelltextÜbersetzen 예:

```text
cc Gruß.c -o Gruß
./Gruß
run Gruß
```

`posix-kor`는 이 eigen ABI 경로로 연결한다. 일반 Linux에서 링크한 프로그램에
Deutsch Funktion 이름을 붙이는 것만으로 eigen ABI 호환이 되는 것은 아니다.

## 제한된 Linux ABI

이 기능은 **eigen Java betriebskernWert 안의 호환 schichtWert**이며 Linux 커널을 적재하지 않는다.

| Linux aufrufen | Nummer | aktuellElementeintrag 제약 |
|---|---:|---|
| read / write / close / lseek | 63 / 64 / 57 / 62 | RAM 파일과 표준 eingabeAusgabe; Eingabewert 대기는 EAGAIN 가능 |
| openat / unlinkat | 56 / 35 | AT_FDCWD 또는 절대 pfad; 파일만, 제한된 merkmalbitsWert |
| ftruncate / fsync | 46 / 82 | RAM Datei; fsync가 영속 저장을 의미하지 않음 |
| exit / exit_group | 93 / 94 | aktuellElementeintrag Programm verlassenProzessProgramm |
| brk | 214 | eigen Benutzer speicherhaldeWert beschneiden; fehlschlagWert 시 vorherigElementeintrag break zurückkehrenErgebnis |
| clock_gettime | 113 | CLOCK_MONOTONIC만, millisekunden auflösungWert |
| getpid / gettid | 172 / 178 | 한 Benutzer befehlAusführen 흐름의 bezeichnerWert |

istNichtUnterstützt 번호는 `-ENOSYS`를 반환한다. Linux ABI의 socket, fork/clone/execve,
pthread, mmap, signal, ioctl, fstat, 동적 로더와 일반 libc 초기화는 구현하지
않았다. 기존 eigen POSIX/Java 소켓은 별도로 TCP/UDP를 지원한다.

anfänglichStatuswert 스택에는 argc, UTF-8 argv, 빈 envp, AT_PAGESZ/AT_ENTRY/AT_NULL을 넣는다.
입력은 ELF64 little-endian AArch64 **ET_EXEC**, Datei 전체 **16 KiB 이하**,
PT_LOAD 주소는 **0x02000000 이상 0x02c00000 미만**이어야 한다.
Datei 오프셋과 가상 주소의 페이지 ausrichtenWert 관계를 검사하며, 서로 페이지를 공유하는
세그먼트와 schreiben·befehlAusführen 동시 허용은 거부한다. PT_INTERP/PT_DYNAMIC/PT_TLS와
ET_DYN은 아직 받지 않는다.

일반 Linux 바이너리의 standardwertWert 적재 adresse 0x00400000은 커널과 겹치므로 아직 받지
않는다. 예제는 GNU 링커의 `-Ttext-segment=0x02000000 -z max-page-size=4096`을
사용한다. 이 파일도 정상적인 Linux ELF이며 같은 파일이 Linux와 eigen 커널에서
실행됨을 시험한다. Datei 이름이나 헤더만 바꿔 기존 Linux Programm 전체를 지원할
수는 없다.

## tatsächlichDaten 동일 바이너리 비교 Prüfungen

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-elf
```

시험은 `Beispiele/LinuxABI/ausführenVorgang.S`와 `Gruß.c`를 Linux AArch64 대상으로 컴파일해,
**JKOROS note가 없는 확장자 없는 befehlAusführen Datei** `build/verification/elf/리눅스인사`를
만든다. 같은 바이트를 nächsterElementeintrag 두 경로로 실행한다.

```sh
qemu-aarch64 build/verification/elf/리눅스인사 한글인수
python3 Werkzeuge/dateiAusführen.py --linux build/verification/elf/리눅스인사 한글인수
```

ersterElementeintrag 명령은 Linux 시스템 호출을 사용하는 projektWurzel 실행이고, 두 번째는 Linux를
적재하지 않은 raspi4b eigen betriebskernWert 실행이다. HangulText argumente, Datei eingabeAusgabe, Uhr, verlassenProzessProgramm,
betriebskernWert adresse zugriffEintrag 거부를 비교한다. FTP로 같은 파일을 올려 실행하는 시험도 있다.
protokolldateiAufzeichnung: `build/verification/elf/report.json`, `readelf.txt`, `serial.log` 및 FTP 보고서.

일반 Linux 프로그램까지 지원하려면 별도 Benutzer adresse adresseGebiet, 더 큰 영속 VFS,
전체 befehlAusführen initialisieren/auxv, 동적 링커와 재배치, mmap/TLS/시그널/스레드,
시스템 aufrufen 및 libc 호환성을 확장해야 한다. 이번 구현은 ersterElementeintrag 제한된 befehlAusführen 경로다.
