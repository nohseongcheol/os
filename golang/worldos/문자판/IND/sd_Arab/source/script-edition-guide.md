# IND / sd_Arab

이 소스는 WorldOS 원문 식별자 방언입니다. 결합문자를 삭제하지 않습니다. `make kernel`, `make iso`, `make userland`는 임시 빌드 공간에서만 표준 Go 이름으로 대응합니다.

identifier-mapping.tsv의 project-proposal은 신규 제안, pending-translation은 미번역, reading-needs-review는 일본어 자동 읽기 검토 대상입니다. 완역·원어민 검수를 뜻하지 않습니다. 영문 접두부 T/V와 숫자 꼬리는 형식·공개 여부 및 충돌 구분용입니다. C 공개 규약·기계 명령·파일 확장자·Makefile·src·build는 호환성을 위해 보존합니다.

기존 파일의 편집 내용은 매 빌드에 반영됩니다. 파일 추가·이동 또는 새 식별자 도입 시 script-mapping.json의 파일/식별자 대응도 갱신해야 합니다. 미등록 결합문자는 컴파일 오류로 검출됩니다.
