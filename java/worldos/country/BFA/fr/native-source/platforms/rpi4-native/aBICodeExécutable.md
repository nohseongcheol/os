# ELF 형식과 Linux exécuterCommande Fichier 호환성

**ELF는 확장자가 아니다.** Executable and Linkable Format이라는 바이너리
형식이며, Linux 외의 운영체제도 사용한다. élémentListePremier 네 valeurOctet `7f 45 4c 46`,
ELF valeurClasse, CPU valeurGenre, Programme 헤더와 valeurPointEntréeÉlément 주소를 읽어서 해석한다.
[ELF ABI spécification](https://gabi.xinuos.com/elf/02-eheader.html)

기존 jkoros 로더도 donnéesEffectif ELF64/AArch64 exécuterCommande 파일을 읽었다. `.elf`는 예제의
이름일 뿐이었다. 다만 **ELF valeurFormat 지원과 Linux 시스템 invoquer ABI 지원은 별개**opérandeTroisième.
기존에는 `JKOROS` ABI note를 가진 interne exécuterCommande 파일만 허용했고, Linux 바이너리는
호환되지 않았다. ARM64 Linux는 SVC의 x8에 Linux 시스템 invoquer 번호를 넣는다.
같은 번호를 interne ABI로 해석하면 다른 동작이 되므로 두 경로를 구분한다.
[Linux syscall ABI description](https://man7.org/linux/man-pages/man2/syscall.2.html)

## 이번 반영

| valeurEntrée | exécuterCommande 방법 | valeurPriseEnCharge rogner |
|---|---|---|
| interne ABI의 ARM64 ELF | `./Salutation`, `/Tâche/Salutation`, `run Salutation` | 확장자 없이 exécuterCommande; 내용이 ELF이면 `.txt`라는 이름도 동일 |
| Linux ARM64 valeurStatique ELF | `run --linux 리눅스인사 한글인수` | valeurBasExtrémité 시스템 invoquer·adresse·taille 제한을 만족하는 Programme |
| 텍스트를 `.elf`로 이름만 changerValeur | exécuterCommande rejeterValeur | 확장자로 exécuterCommande 파일을 인정하지 않음 |
| x86/x86-64, ARM32 exécuterCommande Fichier | exécuterCommande rejeterValeur | AArch64 전용이며 CPU valeurInstructionMachine outilCompilateur méthodeManquant |
| 일반 glibc/musl Programme, PIE, 공유 bibliothèque | 아직 estNonPrisEnCharge | 동적 로더·재배치·TLS·mmap·시그널 등 ajouterFinEntréeÉlément Portage valeurNécessaire |

interne 바이너리와 JAR의 interpréteurCommandes 직접 실행은 Fichier 헤더로 구분한다. `run`은 interne ELF,
`run --linux`는 명시적으로 Linux ABI를 선택한다. Linux 바이너리를 자동으로
interne ABI에 넣지 않으며, interne ABI note가 있는 파일은 Linux 모드에서 거부한다.
élémentListeActuel RAM Fichier 체계에는 exécuterCommande valeurPermission 비트와 `chmod`, PATH 검색이 없다.

게스트 C compilerSource 예:

```text
cc Salutation.c -o Salutation
./Salutation
run Salutation
```

`posix-kor`는 이 interne ABI 경로로 연결한다. 일반 Linux에서 링크한 프로그램에
français Fonction 이름을 붙이는 것만으로 interne ABI 호환이 되는 것은 아니다.

## 제한된 Linux ABI

이 기능은 **interne Java valeurNoyau 안의 호환 valeurCouche**이며 Linux 커널을 적재하지 않는다.

| Linux invoquer | numéro | élémentListeActuel 제약 |
|---|---:|---|
| read / write / close / lseek | 63 / 64 / 57 / 62 | RAM 파일과 표준 sortieEntrée; valeurEntrée 대기는 EAGAIN 가능 |
| openat / unlinkat | 56 / 35 | AT_FDCWD 또는 절대 chemin; 파일만, 제한된 valeurDrapeaux |
| ftruncate / fsync | 46 / 82 | RAM Fichier; fsync가 영속 저장을 의미하지 않음 |
| exit / exit_group | 93 / 94 | élémentListeActuel Programme programmeQuitter |
| brk | 214 | interne Utilisateur valeurTas rogner; valeurÉchec 시 élémentListePrécédentÉlément break résultatRetourner |
| clock_gettime | 113 | CLOCK_MONOTONIC만, millisecondes valeurRésolution |
| getpid / gettid | 172 / 178 | 한 Utilisateur exécuterCommande 흐름의 valeurIdentificateur |

estNonPrisEnCharge 번호는 `-ENOSYS`를 반환한다. Linux ABI의 socket, fork/clone/execve,
pthread, mmap, signal, ioctl, fstat, 동적 로더와 일반 libc 초기화는 구현하지
않았다. 기존 interne POSIX/Java 소켓은 별도로 TCP/UDP를 지원한다.

étatValeurInitialValeur 스택에는 argc, UTF-8 argv, 빈 envp, AT_PAGESZ/AT_ENTRY/AT_NULL을 넣는다.
입력은 ELF64 little-endian AArch64 **ET_EXEC**, Fichier 전체 **16 KiB 이하**,
PT_LOAD 주소는 **0x02000000 이상 0x02c00000 미만**이어야 한다.
Fichier 오프셋과 가상 주소의 페이지 valeurAligner 관계를 검사하며, 서로 페이지를 공유하는
세그먼트와 écrire·exécuterCommande 동시 허용은 거부한다. PT_INTERP/PT_DYNAMIC/PT_TLS와
ET_DYN은 아직 받지 않는다.

일반 Linux 바이너리의 valeurDéfaut 적재 adresse 0x00400000은 커널과 겹치므로 아직 받지
않는다. 예제는 GNU 링커의 `-Ttext-segment=0x02000000 -z max-page-size=4096`을
사용한다. 이 파일도 정상적인 Linux ELF이며 같은 파일이 Linux와 interne 커널에서
실행됨을 시험한다. Fichier 이름이나 헤더만 바꿔 기존 Linux Programme 전체를 지원할
수는 없다.

## donnéesEffectif 동일 바이너리 비교 Tests

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test-elf
```

시험은 `Exemples/ABILinux/lancer.S`와 `Salutation.c`를 Linux AArch64 대상으로 컴파일해,
**JKOROS note가 없는 확장자 없는 exécuterCommande Fichier** `build/verification/elf/리눅스인사`를
만든다. 같은 바이트를 élémentListeSuivant 두 경로로 실행한다.

```sh
qemu-aarch64 build/verification/elf/리눅스인사 한글인수
python3 Outils/exécuterFichier.py --linux build/verification/elf/리눅스인사 한글인수
```

élémentListePremier 명령은 Linux 시스템 호출을 사용하는 racineProjet 실행이고, 두 번째는 Linux를
적재하지 않은 raspi4b interne valeurNoyau 실행이다. texteHangul arguments, Fichier sortieEntrée, Horloge, programmeQuitter,
valeurNoyau adresse entréeÉlémentAccès 거부를 비교한다. FTP로 같은 파일을 올려 실행하는 시험도 있다.
enregistrementJournal: `build/verification/elf/report.json`, `readelf.txt`, `serial.log` 및 FTP 보고서.

일반 Linux 프로그램까지 지원하려면 별도 Utilisateur adresse régionAdresse, 더 큰 영속 VFS,
전체 exécuterCommande initialiser/auxv, 동적 링커와 재배치, mmap/TLS/시그널/스레드,
시스템 invoquer 및 libc 호환성을 확장해야 한다. 이번 구현은 élémentListePremier 제한된 exécuterCommande 경로다.
