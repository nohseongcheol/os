# 명명 자료의 범위

국가 자료는 iso-codes의 ISO 3166-1 목록, 국가별 언어 관계는 Unicode CLDR 48의 territoryInfo를 사용한다. CLDR의 인구·공용어 자료에 등장하는 모든 국가·언어 조합을 생성한다. 국가와 언어는 일대일 관계가 아니며, 이 자료가 세계의 모든 언어를 망라하지 않는다.

`upstream/`은 같은 작업 공간의 golang/worldos에서 가져온 프로젝트 번역 제안이다. 원어민 검토 완료 자료가 아니다. 운영체제 간 소스 의존성을 없애기 위해 필요한 명명 자료를 이곳에 복사했다. `terms.json`은 이 자료, 이 프로젝트의 직접 제안, 설치된 GNU gettext 번역 카탈로그에서 추출한 문맥별 표현의 고정 스냅샷이다. 실행이나 재생성에 다른 운영체제의 디렉터리가 필요하지 않는다.

표현을 확보하지 못한 개념은 Linux판에서는 영어 식별자를 유지하고 `untranslated`로 기록한다. 한국어 원문에서 전환하는 자체 커널판에서는 한국어 식별자를 유지하고 `native-pending.tsv`에 기록한다. 해당 언어로 번역이 완료된 판으로 세지 않는다. Java/JDK/POSIX의 표준 API, 언어 키워드, ISO 코드, 빌드 도구가 요구하는 고정 파일명은 상호운용성을 위해 유지한다.

국가 전체에 하나의 언어 철학을 가정하지 않는다. 새 용어는 기능의 뜻을 우선하며 역사적 설명은 증거가 있는 컴퓨터 개념의 계보와 구분한다. 각 언어 표현의 역사적 어원을 확인하지 않은 경우 이를 확정적으로 서술하지 않는다. 모든 표현의 `native_review`는 현재 `pending`이다.

2026-10-18 기능 검토는 `functional-review.json`에 기록한다. 20개 언어의
223개 역할을 현재 구현과 대조했다. 소스 불러오기와 시스템 부하, 텍스트 출력과
음성 출력, 파일과 파일명, 디렉터리와 경로를 구분한다. GUI의 실행 중인
`Process` 참조와 자체 커널의 일반 현재 값도 별도 이름으로 관리한다.
사전에서 확인한 어근의 역사와 프로젝트에서 만든 복합 함수명을 구분하며,
문헌 근거가 있는 일부 어근이 전체 언어판의 어원 검증을 대신하지 않는다.

`python3 tools/audit_naming.py --native --record-copyright --compile`은 전체
언어판의 식별자·파일명·독립성, Java 소유 해시와 Linux판 컴파일을 검사한다.
`--record-copyright`는 기존에 요청한 저작권 주석만 추가된 경우에 한해 해시를
갱신하며 임의의 코드 수정을 정상 생성 결과로 처리하지 않는다. 검토가 남은
개념은 `build/naming-review/pending.tsv`, 상세 결과는 같은 폴더의 `audit.json`에 남는다.

국가 폴더 전체의 자체 커널 이름은 `native/country_naming.py`가 관리한다.
국가 코드는 언어 코드가 아니다. `AIA`는 앵귈라이며 대표판은 영어이고,
다언어 국가의 하위 언어판은 폴더에 지정한 언어를 유지한다. CLDR의 `az`와
대표판의 `az_Latn`처럼 명시적으로 선택한 문자 체계도 구분한다.
전체 국가별 선택은 `naming/country-language-policy.json`으로 확인한다.
문자 체계가 없는 `zh`, `ms`판에는 각각 프로젝트 기본 사전인 `zh_Hans`,
`ms_Latn`을 재사용한다. `zh_Hant`, `ms_Arab`처럼 문자를 지정한 다른 판의
사전을 이 기본값으로 덮어쓰지 않는다.

`python3 tools/apply_country_naming.py`는 변경을 미리 계산하고, `--apply`는
독립 파일에 적용한다. 파일명·참조 경로·함수·변수를 함께 바꾸며 변경 전
자료는 `build/country-localization/before-*.tar.gz`에 보관한다. 영문 호환 파일과의
이름 충돌을 검사한다. 기존 번역 별칭이 `start`, `read` 같은 표준 API와
겹치는 경우에는 순차 치환을 거부하며 원래 소스에 최종 사전을 적용해야 한다.

영어의 추가 이름은 `native/inputs/english-functional-names.tsv`와 두 개의
`english-*-names.json`에 전체 식별자 단위로 기록한다. 빌드 시 새 단어를
기계적으로 분해하여 번역하지 않는다. 기존 언어별 전체 역할 사전도 재사용한다.
문자 리터럴과 유니코드 시험 문자열은 이름 변경과 분리하여 보존한다.
Java/JDK·POSIX·외부 의존성의 규격 이름과 저작권 표시는 유지한다.
라이선스 조항·제3자 권리 고지는 고정한 원문을 보존하고, 이동한 파일의
경로 참조만 갱신한다. 근거 원문은 `native/inputs/legal-sources.json`에 보관한다.

`python3 tools/audit_country_naming.py`는 전체 국가·언어 선택, 독립 파일,
미번역 목록과 영어판의 남은 한국어 식별자·경로를 검사한다.
`python3 tools/check_country_sources.py --languages en ar`처럼 지정한 언어의
자체 커널·기존 Java 계층·x86·예제·호스트 도구 컴파일도 검사할 수 있다.
다른 언어의 미번역은 각 판의 `native-pending.tsv`에 남긴다. 한국어가 0개인
영어판도 원어민 감수나 모든 이름의 역사적 어원 검증이 완료되었다는 뜻은 아니다.
`Kernel`의 어근 이력은 [Merriam-Webster](https://www.merriam-webster.com/dictionary/kernel)에
근거하며, 새 복합 함수명 자체의 역사와는 구분한다.
`thread`의 고대 영어 계열 어근과 `port`의 출입구·인터페이스 의미도 같은
사전의 해당 표제어에 근거를 남긴다. `port`는 항구 의미의 어원과 구분한다.
