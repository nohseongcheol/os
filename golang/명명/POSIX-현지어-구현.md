# 현지어 POSIX 함수모음

## 구현 범위

기존 249개 국가·지역판과 46개 문자판 각각에 `posix-<국가코드>` 폴더가 있다. 2026-09-10 확장에서는 언어 코드가 아닌 기존 국가 카탈로그의 대문자 3자리 국가 코드를 사용하도록 이동했다. 예:

| 판 | 독립 소스 폴더 | 읽기 / 쓰기 |
| --- | --- | --- |
| 한국어 | `나라/KOR/posix-KOR` | `읽기` / `쓰기` |
| 일본어 | `나라/JPN/posix-JPN` | `読む` / `書く` |
| 히라가나 | `문자판/JPN/ja_Hira/posix-JPN` | `よむ` / `かく` |
| 가타카나 | `문자판/JPN/ja_Kana/posix-JPN` | `ヨム` / `カク` |
| 중국어 간체 | `문자판/CHN/zh_Hans/posix-CHN` | `读取` / `写入` |
| 중국어 번체 | `문자판/CHN/zh_Hant/posix-CHN` | `讀取` / `寫入` |
| 타밀어 | `문자판/IND/ta_Taml/posix-IND` | `படி` / `எழுது` |

전체 경로와 적용 개수는 [POSIX-목록.tsv](../POSIX-목록.tsv)에 있다. 언어 이름만 붙인 공용 영어 소스 참조가 아니라, 각 판 안에 실제 C 구현·선언·시작 코드·시험 프로그램이 들어 있다. 빌드할 때 다른 나라나 원본 EngOS 소스를 읽지 않는다.

다만 **295개 판의 구현·실행 지원과 모든 언어의 완역은 다르다.** 현재 공개 함수는 기존 49개와 추가 58개를 합한 107개이며, 선택한 구현·매개변수·자료형 이름은 117개다. `brk`·`sbrk` 같은 기존 확장도 이 개수에 포함된다. POSIX 전체 표준의 구현 개수나 인증을 뜻하지 않는다. 원래 커널 호출 중에는 제한적으로만 동작하는 함수도 있다. 각 패키지의 `기능범위.tsv`에 사용자 영역 구현과 커널 의존 구현을 구분했다.

각 폴더의 `이름대응.tsv`에는 제안·기존 사전에서 가져온 제안·미번역을 구분했다. 2026-09-11에는 구조체 필드, 표준 자료형·상수, 오류 코드, 시험 보조 이름 등 233개 항목과 선언 파일 경로를 추가로 현지화했다. 현재 역할과 대응은 `선언용어근거.tsv`에, 아직 그대로인 C 식별자는 사유와 함께 `보존식별자.tsv`에 공개했다. C 문법·기계어 진입점과 미번역을 구분한다. 남아 있는 항목의 완역과 원어민 감수는 미완료다. 특히 인도 22개 지정어에 읽기·쓰기 이름이 있다고 해서 22개 언어의 API 전체 번역이 끝났다는 뜻은 아니다. 7,847개 언어 카탈로그 폴더 역시 독립 구현으로 세지 않는다.

추가 58개의 전체 구절 번역 제안은 한국어·일본어·히라가나·가타카나·중국어 간체/번체에 적용했다. 다른 언어에 영어를 남긴 항목은 `pending-language-review`이며 완역으로 세지 않는다. 현재 107개 함수와 선택 이름 117개 모두 대응이 있는 판은 각각 82개(영어 원문 유지 64개 포함)다. 나머지 213개에는 미번역 또는 언어 미지정 항목이 있다. 기존 49개 함수의 언어별 제안은 유지했다. 새 선언 233개 항목의 언어별 범위와 예외는 [선언 현지화](POSIX-선언-현지화.md)에 따로 기록했다. 전 세계 모든 언어의 모든 이름을 완역한 것은 아니다.

## 추가한 실제 구현 58개

| 범위 | 함수 |
| --- | --- |
| 기억 내용 복사·검색 | `memcpy`, `memmove`, `memset`, `memcmp`, `memchr` |
| 문자열 길이·복사·결합 | `strlen`, `strnlen`, `strcpy`, `strncpy`, `stpcpy`, `stpncpy`, `strcat`, `strncat`, `strdup`, `strndup` |
| 문자열 비교·검색·분리 | `strcmp`, `strncmp`, `strcoll`, `strxfrm`, `strchr`, `strrchr`, `strstr`, `strspn`, `strcspn`, `strpbrk`, `strtok`, `strtok_r`, `strcasecmp`, `strncasecmp` |
| 한 바이트 문자 분류·대소 변환 | `isalnum`, `isalpha`, `isblank`, `iscntrl`, `isdigit`, `isgraph`, `islower`, `isprint`, `ispunct`, `isspace`, `isupper`, `isxdigit`, `tolower`, `toupper` |
| 동적 기억공간 | `malloc`, `calloc`, `realloc`, `free` |
| 정수 변환·계산 | `strtol`, `strtoul`, `atoi`, `atol`, `abs`, `labs`, `div`, `ldiv` |
| 정렬·탐색·환경값 | `qsort`, `bsearch`, `getenv` |

`memmove`는 겹친 영역의 양방향 복사, `strncpy`는 정해진 길이의 영 채움, `strtol` 계열은 진법·부호·변환 끝·범위 초과를 처리한다. `malloc` 계열은 16바이트 정렬, 해제 영역 재사용·인접 영역 병합, 곱셈 크기 초과 검사를 한다. 실패한 `realloc`은 이전 영역을 보존한다. `realloc(p, 0)`은 이 구현에서 해제 가능한 최소 영역을 유지하도록 정했다.

초기 C/POSIX 로케일과 단일 스레드 환경을 대상으로 한다. UTF-8 문자열의 **문자 수**나 모든 언어의 대소문자를 처리하는 유니코드 라이브러리가 아니다. 문화권별 정렬·분류, 다중 스레드용 할당기·errno는 미구현이다. [미완료 범주](POSIX-남은범위.md)를 참고한다.

## 컴파일과 실행

```sh
cd /home/user/worldos
make posix COUNTRY=KOR
make posix COUNTRY=JPN
make script-posix VARIANT=JPN/ja_Hira
make script-posix VARIANT=JPN/ja_Kana
make script-posix VARIANT=IND/ta_Taml
make shell COUNTRY=KOR
```

`make shell`도 같은 판의 새 POSIX 함수모음을 빌드해 연결한다. 커널·셸의 기존 독립성은 유지된다.

한국어 응용 소스 예:

```c
#include <입출력과실행.h>

int main(void)
{
    const char *인사 = "안녕하세요\n";
    return 쓰기(표준출력번호, 인사, 16) == 16 ? 0 : 1;
}
```

위 예를 UTF-8로 저장했다면 해당 판 안에서 새 출력 경로로 컴파일한다.

```sh
cd /home/user/worldos/나라/KOR/posix-KOR
python3 posix_build.py compile --source /경로/인사.c --output /경로/새실행파일
```

이 C 원문은 결합부호를 포함한 모든 대상 문자를 받아들이는 **현지어 C 방언**이다. `posix_build.py`가 식별자와 정확한 include 경로만 표준 대응 이름으로 변환한다. 문자열·주석·기계어·호출 번호는 바꾸지 않는다. 일반 GCC에 원문을 바로 전달하거나, 기계어 공개 심볼까지 현지어로 바꾼 방식이 아니다. 표준 연결 이름을 유지해 기존 C 프로그램과 같은 라이브러리에 연결할 수 있다. 새 사용자 변수는 그대로 두지만 새 현지어 API 이름을 추가할 때는 `posix.json`의 이름 대응도 등록해야 한다.

산출물은 `build/libposix.a`, `build/crt0.o`, `build/posix-native-probe`, `build/posix-library-runtime`과 기존 회귀시험 ELF다. 응용 실행파일을 해당 커널용 **복제 시험 디스크**의 `USER1`에 설치해야 게스트에서 실행된다. 게스트 ELF의 사용자 정의 연결 배치는 호스트 Linux용이 아니다. 별도 호스트 단위시험은 같은 C 구현을 Linux용 ELF 배치로 다시 연결한다. `posix-native-probe`는 시험 도구가 `USER2`에 설치한 ELF를 읽고 추가 58개 함수 시험도 실행한다.

전체 문자 화면 출력·자판 입력 지원은 별도 과제다. UTF-8 원문을 빌드할 수 있다는 것이 모든 글꼴·입력기가 구현됐다는 뜻은 아니다.

## OS 중립 이름

| 이전 구현 이름 | 새 이름 |
| --- | --- |
| `__engos_syscall6` | `__syscall6` |
| `__engos_syscall_result` | `__syscall_result` |
| `engos/syscall.h` | `sys/syscall.h` |
| `libengos_posix.a` | `libposix.a` |
| `_ENGOS_*` 헤더 보호 이름 | `_LIBC_*` |
| 시험 환경변수 `ENGOS=1` | `POSIX_TEST=1` |

`engos`는 POSIX가 요구한 말이 아니다. 이전 함수모음이 EngOS 원본에서 복사됐고 C 선언·호출·어셈블리 정의가 같은 접두어를 사용하고 있었다. 소스 구조상 프로젝트 내부 구현을 구별하는 이름으로 볼 수 있지만, 작성자의 명시적인 설계 설명을 발견한 것은 아니므로 그 이상의 의도를 단정하지 않는다.

`__syscall6`는 호출 번호와 인수 여섯 개를 i386 레지스터에 배치하고 `int 0x80`으로 커널을 호출한다. `__syscall_result`는 이 구현의 음수 오류 반환을 `-1`과 `errno`에 대응시킨다. 이름에서 OS 접두어를 제거해도 CPU·커널 호출 규약 의존성까지 사라지지는 않는다. 다른 CPU나 다른 호출 규약의 커널로 옮길 때는 이 부분의 구현을 맞춰야 한다.

기존 각 판의 `소스` 안 함수모음도 같은 이름으로 고쳤다. 선언·C 호출·어셈블리 심볼·Makefile·시험을 함께 변경하고 기존 명명 감사 해시를 갱신했다. 옛 파일 경로 대응의 원본 열, 과거 `TEST_RESULTS.md`, 기존 빌드 잔여물과 백업은 출처·과거 증거이므로 새 검증처럼 고쳐 쓰지 않았다. `uname`의 기존 커널 정보 문자열은 API 식별자가 아니며 이 작업에서 바꾸지 않았다. 대신 시험이 특정 기증 OS 이름만 요구하지 않도록 했다.

## 현재 기능과 어원에 따른 이름 선택

고유어만 기계적으로 조립하거나 각 언어에 같은 어순을 강요하지 않는다. 어원은 뜻을 이해하는 단서로 사용하되 실제 동작과 충돌하면 현재 기능을 우선한다. 새 표현은 프로젝트 제안이며 공식 권장어나 원어민 감수 결과가 아니다.

- `read` / `write`: 각각 열린 자료의 내용을 완충영역으로 읽기, 완충영역의 내용을 열린 대상에 쓰기다. 문자 한 개가 아니라 바이트 수를 처리한다. 공통 `count`가 이제 배열 원소 수도 나타내므로 한국어 이름은 단위를 강제하지 않는 `수량`으로 고쳤다. [읽기 명세](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html), [쓰기 명세](https://pubs.opengroup.org/onlinepubs/9699919799.2018edition/functions/write.html).
- `fork`: 갈라진 실행 흐름이라는 뜻을 살려 `실행과정갈라내기`로 제안했다. 새 자식 실행과정을 만드는 동작이다. [fork 명세](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fork.html).
- `execve`: 단순히 새 과정을 만드는 호출이 아니라 현재 실행 내용을 새 것으로 바꾸므로 `실행내용바꾸기`다. [exec 명세](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html).
- `dup` / `dup2`: 복제되는 것은 파일 내용이 아니다. 같은 열린 파일 설명을 참조하는 서술번호를 만들므로 `열린자료참조복제하기`와 `지정번호로열린자료참조복제하기`다. [dup 명세](https://pubs.opengroup.org/onlinepubs/9799919799/functions/dup.html).
- `brk` / `sbrk`: 중단점이나 실행 중지가 아니라 데이터 영역 끝의 이동이다. 이 구현에서 동적 기억영역의 끝을 다루므로 그 기능으로 이름을 제안했다. 이 두 함수는 현행 POSIX 표준 전체에 속한다고 주장해서는 안 된다. [Linux man-pages의 역사·동작 설명](https://www.man7.org/linux/man-pages/man2/brk.2.html).
- `htons` 등: 원래의 host/network와 short/long 구분을 오늘의 정확한 16·32 이진 자리와 바이트 순서로 풀었다. 이름의 16·32는 문자열 길이나 십진 자리수가 아니다.
- `qsort`: 역사적 알고리즘 이름을 구현 의무로 오해하지 않도록 `비교기준으로정렬하기`다. 현재 구현은 추가 동적 할당 없이 힙 정렬을 사용한다. [qsort의 비교 함수·정렬 요구](https://pubs.opengroup.org/onlinepubs/009695399/functions/qsort.html).
- `malloc` / `free`: 기억 내용 자체의 복사나 지우기가 아니라 저장 공간의 확보·반납이므로 `기억공간확보하기` / `기억공간반납하기`다.
- `strlen`: 문자 개수로 오해하지 않도록 `문자열여덟자리묶음길이얻기`다. `strncpy`는 항상 끝의 영을 붙이는 안전 복사가 아니라 한도까지 채우는 동작이므로 `한도만큼문자열채워복사하기`다. [strncpy의 채움·종결 조건](https://pubs.opengroup.org/onlinepubs/7908799/xsh/strncpy.html).

현재 커널의 제한도 유지된다. 일반 파일 쓰기·생성은 읽기 전용 파일체계 제한을 받으며, 통신 시험은 게스트 내부 IPv4 UDP를 대상으로 한다. 번역이 TCP·외부 통신·POSIX 전체 기능을 새로 구현한 것은 아니다.

## 검증·재생성

```sh
make test-posix
make verify-posix
make verify-posix-builds
python3 tools/verify_posix.py --build --boot \
  --disk '/경로/원본시험디스크.vdi' --idle '/경로/대기실행파일'
python3 tools/verify_posix.py --edition KOR --build --boot --full-suite \
  --disk '/경로/원본시험디스크.vdi' --idle '/경로/대기실행파일'
```

부팅 시험은 원본 디스크를 읽어 임시 사본을 만들고 게스트 쓰기는 그 사본의 스냅샷에만 수행한다. 원본 디스크 전후 SHA-256을 비교한다. 각 시험은 실제 실행한 프로그램 및 커널 ISO의 SHA-256을 결과표에 남긴다.

아래는 앞선 함수 확장 시점의 결과다. 2026-09-11 선언 현지화 검증은 [별도 기록](POSIX-선언-현지화.md)에 있다. 함수 확장 결과 위치: `build-verification/posix-expansion/build-all.tsv`, `boot-all.tsv`, `boot-selected.tsv`, `source-disk-all.json`, 판별 `.serial` / `.qemu` / `.build.log`. 검증기에 `--report-dir build-verification/posix-expansion`을 전달하면 과거 결과와 분리한다. 부팅 성공과 이름 완역 여부를 같은 PASS로 세지 않는다.

확장 검증 완료: 전체 295개 판의 빌드·추가 함수 포함 부팅 시험 통과, 대표 8개 판의 8종 회귀시험 64건은 재검사 반영 후 통과, 기존 시험을 포함한 단위시험 79개 통과. 셸도 전체 295개를 새 국가 코드 폴더의 함수모음에 다시 연결했고 대표 8개를 실제 부팅해 통과했다. 국가 249개·문자판 46개의 기존 소스 명명·내용 감사도 통과했다. 원본 가상 디스크는 전후 SHA-256이 같다. [현재 산출물 대조 요약](../build-verification/posix-expansion/delivery-summary.json), [전체 시험 로그](../build-verification/posix-expansion/unit-tests.log).

첫 회귀 64건 중 히라가나판의 통신 시험 1건은 `NTEST:PASS:`와 `close-server` 사이에 배경 작업의 출력이 끼어 연속 성공 표식 검사에서 실패했다. 코드·판정 기준·실행파일·커널을 바꾸지 않은 해당 판 단독 8종 재검사는 모두 통과했다. 최초 FAIL과 원문 로그는 `posix-expansion/boot-selected.tsv` 및 `JPN-ja_Hira-socket.serial`에 그대로 보존했고, 재검사는 `posix-expansion/retry-hira/`에 분리했다. 실행 횟수는 최초 64건과 재검사 8건이며, 최종 64개 서로 다른 회귀 항목이 통과했다는 집계다. 배경 로그 섞임 자체가 해결됐다는 뜻은 아니다.

```sh
python3 tools/summarize_posix.py \
  --report-dir build-verification/posix-expansion \
  --retry-dir build-verification/posix-expansion/retry-hira
```

요약기는 재검사 실행파일·커널이 최초 시험과 동일한지 확인한 뒤 현재 산출물 해시와도 대조한다. 아래의 이전 49개 함수 검증은 과거 기록이며 새 함수의 검증으로 재사용하지 않는다.

이전 49개 함수판은 295개 POSIX 빌드·부팅, 대표 8개 판의 7종 회귀시험 56건, 단위시험 74개를 통과했다. 과거 [검증 요약](../build-verification/posix/delivery-summary.json)은 그 시점의 기록이다.

이전 셸 검사에서도 미국판의 배경 작업 출력이 echo 인수 사이에 끼어 연속 문자열 검사만 실패한 적이 있었다. 당시 원문 로그에서 배경 작업 문구를 분리하면 기대값 `prefix joined a b  tail`과 정확히 일치했고, 검사기나 프로그램을 변경하지 않은 단독 재검사는 통과했다. 과거 로그는 `build-verification/posix/USA-shell-interleaved.serial` / `.qemu`로 보존했다. 이번 확장 후 대표 셸 8개 검사는 모두 통과했다. 전체 295개 셸의 새 부팅 검사를 다시 수행한 것은 아니며, 이번 셸 실행 검증 범위는 위 8개 판이다.

`make install-posix`는 기존 소스 중립화 → 독립 POSIX 생성 → 셸 빌드 연결 갱신 순서다. 이미 생성된 POSIX는 기본적으로 검사 후 유지한다. 옛 언어 코드 폴더는 `python3 tools/migrate_posix_country.py`로 먼저 옮긴다. 새 용어집·함수 구현을 적용하려면 `python3 tools/install_posix.py --refresh`를 사용한다. 감사 해시가 다른 파일은 덮어쓰지 않으며, 갱신 전 생성 파일을 `/tmp/worldos-posix-refresh-backup-*`에 보관한다. 국가 코드 이동 전 전체 폴더·상위 Makefile·진입 설정은 `/tmp/worldos-posix-country-backup-*`에 있다. 사용자 추가 파일과 기존 build 폴더는 보존한다. 중립화 전 원본은 `/tmp/worldos-posix-neutral-backup-*`에 있다. `/tmp` 백업은 장기 보존 장소가 아니므로 필요하면 별도로 보관한다.

선언 경로까지 이동하는 이번 개정은 `python3 tools/install_posix.py --refresh --rename`으로 적용한다. 이어서 `python3 tools/install_shells.py --refresh`로 같은 판의 셸에 새 공개 이름과 include 경로를 반영한다. 이전 경로의 생성 파일은 백업으로 이동하고, 사용자 추가 파일은 지우지 않는다. 응용 코드의 이전 현지어 이름·include 경로는 `posix_build.py compile`의 별칭 대응으로 계속 받는다.

`make country-sources`는 원본에서 기존 국가 소스를 다시 만드는 별도 작업이다. 명명·기능 수정을 되돌릴 수 있으므로 이 작업을 갱신하려고 무심코 실행하면 안 된다.
