# SOM / posix-SOM

현지어 C 원문과 선언을 포함하는 독립 POSIX 함수모음입니다. 다른 판의 소스를 빌드 중 읽지 않습니다.

`make`로 `build/libposix.a`, 시작 코드와 시험 실행파일을 만듭니다. `make verify`는 대응·감사 해시를 검사합니다. `python3 posix_build.py compile --source 사용자.c --output 새실행파일`은 현지어 응용 코드를 변환·연결합니다.

identifier-correspondence.tsv의 함수·변수를 원문에서 사용합니다. file-path-correspondence.tsv에 현지어 선언 파일 경로가 있습니다. 번역 원문은 모든 문자의 결합부호를 받는 C 방언이며, 빌드 시에만 표준 POSIX 연결 이름으로 낮춥니다. 일반 GCC에 직접 전달하는 표준 C 파일이나 별도의 기계어 ABI가 아닙니다. 표준 헤더와 기계어 연결 이름은 build 아래에 생성됩니다.

범위: 현재 구현의 107개 공개 함수와 117개 선택 구현/매개변수/자료형 이름. 주소형·구조체 필드·상수·오류 코드·보조 이름도 declaration-term-evidence.tsv의 현재 역할에 따라 번역합니다. 언어별 제안이 없는 항목과 C 문법·시작 진입점은 preserved-identifiers.tsv에 사유를 구분해 남깁니다. 미번역 항목은 pending-language-review, 기존 사전에서 가져온 기본 동사는 inherited-proposal-needs-review입니다. 모든 언어 완역이나 원어민 감수를 주장하지 않습니다.

`__syscall6` / `__syscall_result` / `sys/syscall.h` / `libposix.a`는 OS 중립 이름입니다. 그러나 구현은 i386 int 0x80 및 이 커널의 호출 규약에 의존하므로 이름 변경이 타 커널 이식 완료를 뜻하지 않습니다. uname은 실행 중인 커널의 실제 정보이며 명칭을 현지어 함수모음이 조작하지 않습니다. POSIX 표준 전체 구현이나 인증을 뜻하지 않습니다. 일부 선언의 실제 지원 범위는 커널에 따릅니다.

추가 함수: 문자열·기억 내용·C 로케일 문자 분류·정수 변환·정렬/검색·환경값 읽기·동적 기억공간 관리. `build/posix-library-runtime`과 현지어 호출 시험에서 동작을 검사합니다. 문자열 길이는 UTF-8 문자 수가 아니라 바이트 수이며, 문화권별 정렬·유니코드 문자 분류는 미구현입니다. malloc 계열과 errno는 단일 스레드 한정입니다. realloc(p, 0)은 해제 가능한 최소 영역을 유지합니다. stdio, 신호, 스레드, 시간, 파일시스템 변경 등 POSIX 전체 기능은 아직 완료되지 않았습니다.
