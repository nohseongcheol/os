# KIR command interpreter

이 폴더는 현지어 원문 식별자 C 소스와 명시적인 `@{현지어식별자}` 빌드 셸 틀을 포함합니다. `make`가 실행 시점에만 컴파일 대응명으로 바꿉니다. `.sh.in`은 Bash 직접 실행 파일이 아닙니다. 다른 국가나 공용 소스가 아니라, 같은 운영체제의 `../posix-<국가코드>` 함수모음을 사용합니다. 새 POSIX 폴더가 아직 없는 경우에만 같은 판의 `../source` 안 기존 함수모음을 사용합니다.

`make` → `build/worldos-shell`; `make verify` → 원문·대응 검사. 커널이 읽는 시험 디스크의 USER1 자리에 실행파일을 설치하면 명령해석기로 시작합니다. 원본 가상 디스크를 덮어쓰지 말고 전용 복제를 사용하세요.

지원: help echo pwd cd cat stat pid uname run udp source exit 및 command-correspondence.tsv의 별칭. UTF-8 명령파일은 `source /파일명`으로 읽습니다. 공백·따옴표·역슬래시·행 끝 주석을 처리합니다. 이 폴더의 `.commands` 예제는 새 시험 디스크의 `/COMMANDS`로 복사되며 `source /commands`로 실행합니다. 최대 입력 511바이트, 인수 15개, 명령파일 중첩 4단계. 변수 확장·파이프·재지정·조건문·반복문·작업 제어가 없는 작은 명령해석기이며 POSIX sh 전체 구현이 아닙니다.

새 이름은 프로젝트 제안이며 원어민 감수·전체 완역을 뜻하지 않습니다. 미번역은 identifier-correspondence.tsv에 남습니다. 영어 진단 문구, C/POSIX ABI와 빌드 도구 인터페이스는 유지합니다. 코드 편집은 다음 빌드에 반영되지만 새 현지어 식별자는 shell.json에도 등록해야 합니다. 현재 화면·자판이 모든 문자의 표시·직접 입력을 지원하는 것은 아니며 UTF-8 파일/직렬 로그로 검사합니다.
