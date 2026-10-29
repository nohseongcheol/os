# jkoros posix-kor

**자체 ARM64 Java 커널용 C++ Ikgokaganye**은 [arm64-native](arm64-native/faele_ya_MPALE_eb81d7d9.md)에 있다. khenele_boleng 내부 직접 Faele 호출과 EL0 mošomiši 프로그램의 Faele/UDP 루프백 SVC 호출을 별도 라이브러리로 제공한다. 아래 i386 Bokgobadata 및 ARM64 Linux libc와는 nepo·ABI가 다르다.

자체 jkoros 커널에서 실행되는 i386 C 라이브러리와 한국어 API다. go_nea_ditirelo libc를 연결하지 않고 `int 0x80`으로 kgonthe_data 커널의 파일서술자·단말·UDP·lota_boleng 계층을 호출한다. `ya_kgale_mohlodi/`의 go_nea_ditirelo JVM 모형과 별개다.

**현재는 POSIX의 일부 기능을 제공하는 호환 계층이며, POSIX 인증·전체 libc·전체 OpenJDK를 뜻하지 않는다.** 구현 범위와 제한을 아래에 명시한다. 한국어를 먼저 적용했다. 다른 국가·언어의 번역판은 아직 만들지 않았다.

## 빌드와 phethagatša_taelo

```sh
cd /home/user/jkoros
make posix-kor
make iso
make test-posix
make -C os run-store
```

`run-store`는 `os/build/files.img`가 없을 때만 새 전용 파일을 만들고 QEMU IDE 첫 장치로 연결한다. 기존 파일을 덮어써서 초기화하지 않는다. 일반 `make run`은 디스크 없이 실행된다. VirtualBox 실행기의 디스크 연결은 변경하지 않았다.

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

`Sync: 0`은 연결된 전용 매체에 저장했다는 뜻이다. 디스크가 없거나 abela_boleng 형식이 아니면 `Sync: -19`다. 같은 `files.img`로 다시 부팅하면 마지막 kopanya 상태를 복원한다. Java 소스와 `.class`도 같은 lota_boleng 대상이다. `close`나 편집기의 `.save`만으로 재부팅 보존을 보장하지 않으므로 Etšwa_tirišo 전에 `sync`를 실행한다.

## 한국어로 C tirišo_f5044b9b 작성

```c
#include <파일규약.h>

int main(int 인수개수, char **akumente_Lenaneo) {
    (void)인수개수;
    (void)akumente_Lenaneo;
    int 파일서술자 = bula_faele("note.txt", bala_ngwala | 없으면만들기, 0600);
    if (파일서술자 < 0) return 오류번호;
    if (ngwala_faele_data(파일서술자, "hello\n", 6) != 6) return 1;
    if (파일저장확정(파일서술자) < 0) return 오류번호;
    return tswalela_faele(파일서술자);
}
```

작성 원문은 한글을 그대로 유지한다. `Ditholosi/sešupi_Phetošetšo.py`가 aga_lenaneo 복사본의 식별자만 C 표준 UCN 표기로 바꾸어 GCC 7에서도 컴파일되게 한다. molokoloko_boleng, 주석, `#include` 경로는 변환하지 않는다. 이 도구는 C의 모든 전처리 표기법을 해석하는 전처리기가 아니며, 프로젝트가 사용하는 일반 토큰과 include 문법을 대상으로 한다.

라이브러리는 `build/libposix-kor.a`, Diriša 코드는 `build/Thomišo_mošomiši_tirišo.o`, 생성 헤더는 `build/mohlodi/포함/`이다. aga_lenaneo 옵션과 Ikgokaganye 명령은 [Makefile](Makefile), kgonthe_data 예제는 [파일규약시험.c](mohlodi/시험/파일규약시험.c)와 [자료전문시험.c](mohlodi/시험/자료전문시험.c)에 있다. 새 ELF를 OS에 포함하려면 `os/Makefile`의 mošomiši phethagatša_taelo 묶음에 명시적으로 등록한다. 게스트 안에서 C를 컴파일하는 도구는 제공하지 않는다.

표준 C/POSIX 외부 Leina `open`, `read`, `write`, `socket`, `errno`, `main`과 헤더 경로는 유지한다. 한국어 별칭은 같은 함수를 가리킨다. 변수와 구현 파일에는 의미를 드러내는 한국어 이름을 사용한다. Fetolela_mohlodi 근거는 [명명 원칙](명명원칙.md), kgonthe_data 대응은 [용어 대응표](용어대응.tsv)에 기록했다.

## 제공하는 기능

| setsopolwa | 구현 | 현재 제한 |
|---|---|---|
| Faele | open/creat/read/write/close/lseek/unlink/ftruncate/fstat/fsync | 루트의 단일 Leina, ASCII 63바이트, 8개 Faele, 파일당 16KiB |
| 서술자 | dup/dup2, F_DUPFD/F_DUPFD_CLOEXEC/F_GETFD/F_SETFD/F_GETFL/F_SETFL | tiragalo_boleng 하나, 최대 32개; 잠금·exec 미구현 |
| I_O Dipeakanyo | O_RDONLY/O_WRONLY/O_RDWR/O_CREAT/O_EXCL/O_TRUNC/O_APPEND/O_NONBLOCK/O_CLOEXEC | 그 밖의 비트는 ENOTSUP; kgonthe_data mošomiši·그룹 fihlelela_go_tsenya_tshedimošo tumelelo_boleng 검사는 없음 |
| 표준 단말 | 0 Bala, 1·2 Ngwala, paete_boleng thutišo_boleng 입력 | 터미널 rulaganya_boleng·termios·시그널 없음, 한글 fonte_boleng/입력기 없음 |
| UDP | socket/bind/sendto/recvfrom/getsockname, SO_RCVTIMEO | IPv4 UDP만, 묶인 종단점 4개, 전문당 1,024바이트, 수신 대기 Dipeakanyo 최대 2초 |
| atrese | htons/ntohs/htonl/ntohl/inet_pton/inet_ntop | IPv4 숫자 주소만; DNS/IPv6 없음 |
| 작은 C Thekgo_boleng | strlen/strcmp/memcpy/memset/memcmp/puts/putchar | 전체 libc·stdio FILE·malloc 없음 |
| lota_boleng | JKSTORE1 전용 IDE lota_boleng, 두 보존본과 검사합 | FAT/ext tshepedišo_ya_difaele·디렉터리·하드 링크·심볼릭 링크 없음 |
| 게스트 Java | FileInputStream(String).read()/close(), FileOutputStream(String[, boolean]).write(int)/close() | arei_boleng I_O·일반 java.io·예외 tiragalo_boleng_go_tsenya_tshedimošo 없음 |

`dup`으로 복제한 서술자는 Faele 위치와 이어쓰기 설정을 공유한다. `FD_CLOEXEC`는 서술자마다 저장한다. `unlink`는 이름만 제거하며, 열린 파일의 내용은 마지막 참조가 닫힐 때까지 접근할 수 있다. 빈 위치를 건너뛰어 쓰거나 길이를 늘린 영역은 0으로 읽힌다. 파일서술자 부족으로 실패한 `open`은 파일을 생성하거나 비우지 않는다. C 호출 실패는 `-1`과 `errno`, 내부 khenele_boleng 호출은 음수 Phošo 번호를 반환한다.

`fstat`는 이 프로젝트 전용 48바이트 구조체에 종류·Bogolo·링크 수·허가 paente_boleng 등을 반환한다. POSIX의 전체 시간 속성은 아직 제공하지 않는다. 다른 운영체제의 `struct stat` 또는 Linux 바이너리 ABI와 호환되지 않는다. `O_CLOEXEC`는 기록할 수 있지만 현재 exec 기능은 없다. 성공하는 TIRO_boleng 이름만으로 전체 POSIX 의미가 구현되었다고 간주하면 안 된다.

UDP는 QEMU RTL8139의 kgonthe_data go_nea_ditirelo 왕복을 지원한다. 짧은 수신 버퍼에는 앞부분을 복사하고 나머지 전문을 버린다. 빈 전문도 송수신한다. `SO_RCVTIMEO` 또는 비차단 수신의 data 없음은 `EAGAIN`이다. TCP를 요청하면 `EPROTONOSUPPORT`를 반환한다. 루프백·브로드캐스트·멀티캐스트·연결형 소켓·listen/accept는 아직 없다. 기존 AOT Java UDP 손잡이는 이 POSIX 서술자와 별개이므로 서로 섞어 닫지 않는다.

모든 mošomiši 프로그램에는 기존 약 3초 phethagatša_taelo 상한이 적용된다. `errno`는 현재 단일 tiragalo_boleng·단일 스레드 변수다. JDK 전체, Swing/AWT/JavaFX, TCP/DNS/HTTP/TLS, 스레드·GC·JIT·동적 연결은 아직 구현하지 않았다. 전체 Java SE phethagatša_taelo 환경을 만들려면 해당 khenele_boleng 기반과 런타임 이식을 계속 진행하거나 별도 Linux 기반 phethagatša_taelo 방식을 결정해야 한다.

## lota_boleng 형식과 kgonthiša_5fb2b747

매체는 512바이트 karolo_boleng 2,048개(1MiB)다. karolo_boleng 0의 `JKSTORE1` sešupi_boleng·Bogolo·fomete_boleng 번호가 모두 맞는 장치만 Ngwala 대상으로 삼는다. karolo_boleng 1과 260에서 각각 259구역짜리 보존본이 시작한다. 각 보존본은 완료 머리 1구역, Faele 표 2구역, Faele data 256구역으로 구성된다.

`fsync`와 `sync`는 이름이 남아 있는 모든 파일의 현재 상태를 저장한다. 반대편 보존본을 무효화한 Morago_boleng Faele 표와 자료를 쓰고 ATA 캐시 비우기를 실행한다. 마지막에 세대 번호와 FNV-1a 검사합을 가진 완료 머리를 기록하고 다시 캐시를 비운다. 부팅 시 검사합과 표가 유효한 가장 ya_bjale_boleng 세대를 선택한다. 검사합은 우발적인 손상을 hwetša_go_tsenya_tshedimošo 위한 것이며 암호학적 무결성 검증은 아니다. kgonthe_data sedirišwa_boleng 전원 차단 시험은 하지 않았다.

복원된 Faele 목록은 부팅 이미지의 setsenywa_sa_tirelwa 예제/`JAVA_FILES` 목록을 대체한다. 새 예제를 이미지에 추가해도 기존 lota_boleng 매체를 연결하면 저장된 목록이 우선한다. 동기화하지 않은 변경은 재부팅 후 사라진다.

`make test-posix`는 한국어 sešupi_boleng 변환, ELF/ISO의 kgonthe_data C ABI 호출, 공유 위치, 삭제된 파일의 수명, Faele/서술자 고갈, sešupi Phošo, 표준 입력, UDP, `fsync`, 재부팅, 손상된 최신 보존본의 회피, 다른 형식의 매체 비변경, 게스트 Java Faele 처리와 OpenJDK 교차 실행을 확인한다. 기록은 `os/build/규약시험.json`, `보존시험.json`, `자바파일시험.json`이다.
