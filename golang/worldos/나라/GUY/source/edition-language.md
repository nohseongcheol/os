# Guyana (GUY) source language

- country: Guyana (GY)
- selected language: en
- CLDR population: 100%
- official status: official
- native language name: English
- target-language vocabulary: 871
- unresolved source-glossary vocabulary: 0
- naming mode: semantic word translation

Identifiers and source paths are composed from reviewed translated meanings. Language-name prefixes, hashes and invented letter-by-letter readings are prohibited. A technical loanword is accepted only when an installed gettext catalog or an explicit reviewed seed establishes common usage. `용어근거.tsv` records unresolved source-glossary fallbacks. ABI entry points, toolchain syntax, CPU registers and international standard abbreviations retain compatibility names. This directory contains its own kernel, assembly, build scripts, diagnostics and POSIX userland wrapper sources.

## 기능·어원 중심 명명 개정

현재 기능에 따른 전체 표현은 `새명명-용어.tsv`, 식별자와 경로 변경은 `새명명-식별자.tsv`, `새명명-경로.tsv`에 기록합니다. 이 표현은 WorldOS 프로젝트 제안이며 공인 표준 번역이나 원어민 감수 완료를 뜻하지 않습니다. 미검토 항목은 `명명검토대기.tsv`에 남겼습니다. 영어 대체 이름은 해당 언어의 번역으로 집계하지 않습니다. C 공개 ABI·헤더 이름·기계 명령·Go 예약어는 유지합니다.
