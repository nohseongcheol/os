# WorldOS SWZ 완전 독립 소스

이 트리는 engos의 현행 기능을 대표 언어(en)의 기능 의미에 따라 명명한 독립 빌드 소스입니다. 언어 이름 토큰과 해시는 식별자에 사용하지 않습니다. Go 언어·런타임 ABI와 POSIX 공개 ABI 이름은 호환성을 위해 유지합니다. `name-correspondence.tsv`, `file-correspondence.tsv`, `glossary.tsv`에서 변환 근거를 추적할 수 있습니다.

## 기능·어원 중심 명명 개정

현재 기능에 따른 전체 표현은 `revised-terms.tsv`, 식별자와 경로 변경은 `revised-identifiers.tsv`, `revised-paths.tsv`에 기록합니다. 이 표현은 WorldOS 프로젝트 제안이며 공인 표준 번역이나 원어민 감수 완료를 뜻하지 않습니다. 미검토 항목은 `naming-review-pending.tsv`에 남겼습니다. 영어 대체 이름은 해당 언어의 번역으로 집계하지 않습니다. C 공개 ABI·헤더 이름·기계 명령·Go 예약어는 유지합니다.
