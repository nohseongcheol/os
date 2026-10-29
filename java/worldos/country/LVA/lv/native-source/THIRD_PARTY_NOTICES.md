# jkoros 자체 ARM64 배포판의 제3자 코드

이 목록은 `platforms/rpi4-native`의 현재 커널·사용자 도구를 대상으로 한다.
Linux 실행판·과거 x86 산출물·기존 worldos 국가별 복사본의 배포 허가를 인증하는 목록이 아니다.
자체 코드의 COSL 조건은 아래 구성요소의 원래 라이선스와 권리를 대체하지 않는다.

| 구성 | 조건 | 고지와 소스 |
|---|---|---|
| SSH libassh 1.1 | LGPL-2.1-or-later | `platforms/rpi4-native/vendor/libassh/COPYING`, 같은 폴더의 전체 소스 |
| VNC 인증·SHA256 BearSSL 0.6 | MIT | `platforms/rpi4-native/vendor/bearssl/LICENSE.txt` |
| GENET MAC/레지스터 | BSD-2-Clause | `platforms/rpi4-native/vendor/freebsd-genet/if_genet.c`, `if_genetreg.h` |
| BCM54xx PHY Uzstādījumi/레지스터 | BSD-4-Clause | `platforms/rpi4-native/vendor/freebsd-genet/brgphy.c`, `brgphyreg.h` |
| lwIP | BSD-3-Clause | `platforms/rpi4-native/vendor/lwip/COPYING` |
| TinyCC | LGPL-2.1 계열, 파일별 고지 우선 | `platforms/rpi4-native/vendor/tinycc/COPYING` 및 파일별 고지 |
| MicroPython 핵심 | MIT, 아카이브 내부 기타 파일은 개별 고지 | `platforms/rpi4-native/vendor/LICENSE.micropython` |
| uzlib | 파일별 zlib/MIT 등 | `platforms/rpi4-native/vendor/uzlib/`의 원문 고지 |
| GCC 산술 런타임 | GPLv3 + GCC Runtime Library Exception 3.1 | `platforms/rpi4-native/vendor/LICENSE.gcc-gpl3`, `LICENSE.libgcc-runtime` |
| 부팅 펌웨어 | Broadcom 재배포 조건 | `platforms/rpi4-native/vendor/LICENCE.broadcom` |
| Noto CJK / DejaVu 글꼴 | SIL OFL / DejaVu 고지 | `platforms/rpi4-native/vendor/LICENSE.fonts-*` |

**This product includes software developed by Bill Paul.**

PHY 기능·사용을 언급하는 광고 자료에도 위 BSD-4-Clause 문구를 표시해야 한다.
GENET/MAC에는 Michael J Karels와 Jared McNeill, PHY에는 Bill Paul의 고지가 보존되어 있다.

wolfSSH·wolfSSL과 U-Boot 파생 GENET 구현은 현재 자체 ARM64 빌드에서 제거했다.
기존 GPL 코드의 저작권 주석을 COSL로 바꾼 것이 아니라, 다른 라이선스의 구현으로 교체했다.
이전 GPL 산출물이나 백업을 현재 COSL 배포 묶음에 포함하면 안 된다.

LGPL 구성요소를 포함한 바이너리는 `make cosl-dist`가 생성하는 소스·재연결 자료와 함께
배포한다. 고객의 LGPL상 수정·디버깅·재연결 권리는 루트 LICENSE의 우선 조건에서 보장한다.
