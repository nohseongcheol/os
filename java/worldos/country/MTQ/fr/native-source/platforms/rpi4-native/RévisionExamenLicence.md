# 자체 ARM64 커널의 외부 코드와 배포 조건

> **상태 변경:** 아래 내용은 GPL 원격 구현을 사용하던 전환 전 검토 기록이다.
> 사용자의 COSL 유지 지시에 따라 wolfSSH/wolfCrypt와 GPL GENET을 교체했다.
> 현재 배포 조건과 제공 자료는 [COSL 배포 안내](GuideDistributionCOSL.md) 및
> [현재 제3자 고지](../../THIRD_PARTY_NOTICES.md)를 따른다.

검토일: 2026-10-04. 대상은 현재 작업 중인 `platforms/rpi4-native`이다. Linux 실행판, 과거 x86 커널, 저장소 전체의 모든 파일에 대한 법률 감사는 아니다. 별도 상용 라이선스 계약이 제시되지 않아 포함된 오픈소스 조건을 기준으로 검토했다. 이 문서는 프로젝트 전체의 라이선스를 새로 지정하는 선언이 아니다.

**무료 배포는 의무가 아니다. 현재 GPL 구성요소를 그대로 결합한 커널을 다른 사람에게 배포한다면 해당 결합 저작물의 소스 제공 의무가 발생하는 구조다.** 개인·조직 내부에서만 개발·사용하는 경우 GPL은 일반적으로 공개 배포를 요구하지 않는다. 수령자에게 제공하는 것이 핵심이며, 언제나 GitHub에 전 세계 공개를 해야 한다는 뜻은 아니다. 다만 수령자의 GPL상 수정·재배포 권리를 NDA나 별도 계약으로 제한할 수는 없다. [GNU의 비공개 사용 설명](https://www.gnu.org/licenses/gpl-faq.html#GPLRequireSourcePostedPublic), [유료 판매 설명](https://www.gnu.org/licenses/gpl-faq.html#DoesTheGPLAllowMoney), [GPLv3 본문](https://www.gnu.org/licenses/gpl-3.0.en.html)

## 현재 확인한 구성

| 구성 | 소스에 명시된 조건 | 현재 연결 및 영향 |
|---|---|---|
| wolfSSH 1.5.0 | GPLv3 또는 별도 상용 라이선스 | `vendor/wolfssh/LICENSING`. `libremote.a`를 자체 커널에 정적으로 연결한다 |
| wolfSSL/wolfCrypt 5.9.4 | GPLv3 또는 별도 상용 라이선스 | `vendor/wolfssl/COPYING`, `LICENSING`. SSH 암호 및 VNC 인증에 사용하며 동일 커널에 연결한다 |
| GENET 드라이버 | GPL-2.0-or-later | `PileRéseau/réseauCâblé.c`는 U-Boot 드라이버에서 이식했다. 커널에 직접 포함되므로 wolfSSL 상용 계약만으로 이 부분의 GPL 조건이 사라지지 않는다 |
| lwIP | BSD 3-clause | `vendor/lwip/COPYING`. 고지 보존 등이 필요하지만 이것만으로 자체 커널 소스 공개를 요구하지 않는다 |
| MicroPython | MIT | `vendor/LICENSE.micropython`. 저작권·허가문 보존 등이 필요하다 |
| TinyCC | LGPL 2.1 계열, 파일별 추가 고지 확인 필요 | `vendor/tinycc/COPYING`. 현재 사용자 영역 컴파일러에 포함. 수정본 소스 및 연결 방식에 따른 재연결 요건 등을 별도로 준수해야 한다 |
| GCC 런타임 일부 | GPLv3 + GCC Runtime Library Exception | `vendor/LICENSE.libgcc-runtime`. 예외 적용 조건을 만족하는 독립 모듈은 비GPL 프로그램에도 사용 가능하다 |

버전별 실제 파일과 최신 공식 안내를 함께 확인했다. 과거 wolfSSL 문서의 GPLv2 설명을 이번 5.9.4에 그대로 적용하면 안 된다. [wolfSSL 5.9.4 다운로드·라이선스](https://www.wolfssl.com/download/), [wolfSSH 공식 라이선스](https://www.wolfssl.com/products/wolfssh/)

현재 `Outils/construireSystème.py`는 Java AOT 커널, 보드 코드, `libnetwork.a`, `libremote.a`를 하나의 `kernel.elf`로 연결한다. 이에 따라 GPL 경로로 이 실행 파일을 배포하면 **라이브러리 원본만 제공하는 것으로는 부족하고, 결합된 자체 커널의 해당 소스와 수정 사항·빌드 스크립트 등을 포함한 Corresponding Source를 제공해야 한다고 판단한다.** 적용 범위의 판단 근거는 현재 연결 구조와 GNU의 결합 저작물 설명이다. [정적·동적 연결에 대한 GNU 설명](https://www.gnu.org/licenses/gpl-faq.html#GPLStaticVsDynamic)

반면 독립적인 사용자 Java/C/Python 프로그램, 단순히 같은 저장 매체에 들어 있는 별도 도구, 과거의 별도 운영체제까지 자동으로 모두 GPL이 되는 것은 아니다. 실제 파생·결합 관계를 확인해야 한다. 컴파일러를 실행했다는 사실만으로 그 출력물이 자동으로 GPL이 되는 것도 아니다. [GPLv3의 결합·단순 집합 구분](https://www.gnu.org/licenses/gpl-3.0.en.html#section5), [컴파일러 출력에 대한 GNU 설명](https://www.gnu.org/licenses/gpl-faq.html#CanIUseGPLToolsForNF)

## 배포 방식별 결론

| 원하는 방식 | 현재 구성에서의 판단 |
|---|---|
| 개인 개발·사내 시험 | 외부 배포가 없다면 일반적으로 소스 공개 의무 없음 |
| GPL 조건을 지키며 무료 배포 | 가능. 해당 소스·수정·고지·라이선스 및 배포 방식에 맞는 제공 수단 필요 |
| GPL 조건을 지키며 유료 판매 | 가능. 판매 가격과 소스 제공 의무는 별개 |
| 현재 커널의 바이너리만 판매하고 해당 소스 비공개 유지 | 별도 허가 없이 현재 GPL 구성 그대로는 곤란 |
| 비공개 제품으로 배포 | wolfSSH/wolfCrypt 상용 허가 확보 또는 교체와 함께, GPL GENET 코드 교체/별도 허가 및 나머지 의존성 검토 필요 |

공개 소스·유료 제품을 선택할 수도 있고, 공개 의무가 없는 구성으로 교체할 수도 있다. 다만 저작권 주석 삭제, 한국어 이름 변경, AOT 컴파일, 단순한 동적 연결 전환만으로 원래 라이선스 의무가 없어지지는 않는다. 실제 판매·하드웨어 제품 배포 전에는 해당 버전·계약·배포 형태를 기준으로 최종 법률 검토를 받는 것이 적절하다.

## 배포 예정인 nohseongcheol/os 라이선스와의 비교

2026-10-04 GitHub API와 원문으로 `main/LICENSE`를 확인했다. 검토한 커밋은 `ae4e4086610389f9abb4887009670d399ebbe9be`, LICENSE blob은 `309fb5f5d8c52d4d872874529aae8bcbf3b0d786`이다. [해당 버전의 LICENSE](https://github.com/nohseongcheol/os/blob/ae4e4086610389f9abb4887009670d399ebbe9be/LICENSE)

문서는 표준 GPL이 아니라 **Custom Open Source License (COSL) v1.0**이다. 도입부에서는 GPL 2 또는 이후 버전을 허용하면서 뒤에서는 별도 제한을 추가한다. 그 제한을 유지한 채 현재 결합 커널 전체를 배포하는 것은 GPL 조건과 호환되지 않는다. GitHub에 소스를 공개해도 추가 제한 문제는 해결되지 않는다.

| COSL 조항 | 현재 GPL 구성과의 충돌 |
|---|---|
| 1항: 사용·수정만 해도 수정 소스 공개, SaaS 사용 시 전체 소스 공개, 파생물에 동일 COSL 요구 | 표준 GPL보다 넓은 공개 의무와 GPL 대신 COSL을 강제하는 추가 제한 |
| 2항: 사용에 대한 특허 계약·로열티, 면제에 저자의 사전 승인 요구 | GPL이 보장하는 권리 행사에 별도 비용·허가를 조건으로 붙이면 충돌. 특허의 실제 등록·유효성·적용 범위는 이번 검토 대상이 아님 |
| 3항: 상업 이용에 별도 상용 계약 및 매출 연동 등 비용 요구 | GPL은 상업 이용을 허용하며, 수령자의 GPL상 권리 행사에 이런 제한을 추가할 수 없음 |

근거는 [GPLv2 6·7항](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html), [GPLv3 5·7·10·11·12항](https://www.gnu.org/licenses/gpl-3.0.en.html)이다. 특히 GPLv3 10항은 GPL상 권리 행사에 추가 라이선스 비용이나 로열티를 부과하는 것을 금지한다. 이는 복사본 판매·설치·지원 서비스의 가격을 받을 수 없다는 뜻은 아니다.

현재 빌드에서 wolfSSH·wolfCrypt와 GPL GENET 드라이버는 자체 커널에 연결된다. `vendor`만 GPL 예외로 표기하고 이들과 결합된 자체 커널에 COSL의 상업 제한을 유지하는 것으로는 해결되지 않는다. 단순히 같은 저장소에 놓인 독립 프로그램까지 일괄 GPL로 바꿔야 한다는 뜻도 아니다.

배포 방안은 다음과 같다.

1. **현재 GPL 코드를 유지:** 결합 커널에 GPLv3 조건을 적용할 수 있도록 자체 코드의 허가를 정리하고, 해당 소스·수정·빌드 자료와 고지를 제공한다. COSL의 추가 제한은 이 GPL 배포에 적용하지 않는다. 유료 판매와 지원 계약은 가능하다.
2. **COSL의 상업 제한을 유지:** wolfSSH·wolfCrypt의 적합한 상용 허가 확보 또는 교체, GPL GENET 코드의 교체 또는 모든 관련 권리자의 별도 허가가 필요하다. 상용 계약을 선택하면 그 계약이 소스의 GitHub 공개까지 허용하는지도 확인해야 한다. LGPL TinyCC와 나머지 구성의 의무는 별도로 남는다.

lwIP의 BSD 조건이나 MicroPython 핵심의 MIT 조건은 저작권·허가문 등을 보존하면서 독자 라이선스 제품에 포함할 수 있다. 이 사실이 GPL 부분과 COSL의 충돌을 해소하지는 않는다.

COSL의 상업 이용 제한은 [OSI 오픈소스 정의의 1·6·7항](https://opensource.org/osd)에도 맞지 않는다. 소스를 열람할 수 있다는 점과 표준적인 오픈소스 라이선스라는 점은 구별해야 한다. 또한 도입부의 GPL 허가와 후속 제한의 모순, 미기입된 관할국·법원 항목은 배포 전 법률 검토로 정리할 필요가 있다. 이 검토는 충돌을 보고하는 것이며, 저장소 LICENSE나 프로젝트의 허가 조건을 변경하지 않았다.
