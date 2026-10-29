# 고정한 외부 소스

## 네트워크·JAR·게스트 C/AOT

- `lwip/`: STABLE-2_2_0_RELEASE의 원본 `src/`와 BSD 형식 `COPYING`. 내려받은 아카이브 SHA-256은 `lwip/SOURCE.txt`. 자체 UART SLIP/raw API 포트는 `../통신망/`에 있다.
- `uzlib/`: 아래 MicroPython v1.24.1의 `lib/uzlib` 중 inflate/CRC/Adler 코드. 원본 파일의 라이선스 고지를 유지한다. 게스트 JAR의 DEFLATE 및 CRC 검사에 사용한다.
- `tinycc/`: 2026-10-03에 고정한 upstream mob 스냅샷 전체. 원본 아카이브 SHA-256은 `tinycc/SOURCE-JKOROS.txt`, LGPL 라이선스는 `tinycc/COPYING`. 원본은 수정하지 않았으며 이식 지원·별도 AOT 변환기는 `../시언어번역기/`에 있다.
- 게스트 C 컴파일러 빌드는 준비된 ARM64 SDK의 선언 헤더와 GCC 15.2.0 `libgcc.a` 산술 보조 함수를 사용한다. GCC 소스: `https://gcc.gnu.org/pub/gcc/releases/gcc-15.2.0/`. 라이선스는 `LICENSE.gcc-gpl3`와 `LICENSE.libgcc-runtime`. musl libc/동적 로더/Linux 시스템 호출 코드를 링크하지 않는다.

SD 이미지에는 lwIP/TinyCC/uzlib/libgcc 고지도 포함한다. TinyCC 포트를 다시 연결할 소스와 객체는 SDK 내보내기 때 `dist/jkoros-native-compiler-source.tar.gz`에 보관한다. 소스 수정 시 `도구/시언어번역기빌드.py`와 `도구/사용자영역빌드.py`로 다시 빌드할 수 있다.

## MicroPython

MicroPython 1.24.1의 공식 태그 소스를 보관한다.

- 출처: https://github.com/micropython/micropython/tree/v1.24.1
- 아카이브: https://codeload.github.com/micropython/micropython/tar.gz/refs/tags/v1.24.1
- SHA256: `a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad`
- 라이선스: [LICENSE.micropython](LICENSE.micropython). 사용한 `py/` 및 `shared/libc`, `shared/runtime` 소스는 각 파일의 MIT 표시를 유지한다.

`도구/파이썬빌드.py`가 아카이브 해시를 검사하고 `build/`에 풀어 자체 포트와 빌드한다. 원본 소스에는 패치를 적용하지 않는다. libc 헤더는 호스트 `libnewlib-dev`를 사용하지만 newlib 런타임은 링크하지 않는다. 문자열·출력 함수는 MicroPython의 freestanding 구현을 사용한다.

아카이브가 없는 다른 체크아웃에서는 프로젝트 루트 `platforms/rpi4-native`에서 다음과 같이 받는다. 빌드 도구는 암묵적으로 다운로드하지 않는다.

```sh
curl --fail --location https://codeload.github.com/micropython/micropython/tar.gz/refs/tags/v1.24.1 -o vendor/micropython-1.24.1.tar.gz
make build
```

Pi4 부팅 펌웨어는 기존 Linux 실행판이 내려받은 공식 묶음에서 필요한 파일만 추출한다. [LICENCE.broadcom](LICENCE.broadcom)은 그 펌웨어의 라이선스이며 자체 Java 커널이나 MicroPython의 라이선스와 별개다.


## 터미널 글꼴

[terminal-font.bin](terminal-font.bin)은 Noto Sans CJK와 DejaVu 글꼴을 8/16×16 흑백 비트맵으로 변환한 `JKOROS terminal bitmap`이다. 원본 이름으로 수정 글꼴을 배포하지 않는다. BMP 65536칸과 U+1F600…U+1F64F 80칸을 저장하며, 모든 코드포인트에 실제 글리프가 있다고 의미하지 않는다. 일반 빌드는 이 고정 바이너리를 사용한다.

- 출처·입력 파일 SHA256·비트맵 SHA256: [terminal-font.json](terminal-font.json).
- Noto CJK 라이선스(SIL OFL): [LICENSE.fonts-noto-cjk](LICENSE.fonts-noto-cjk).
- DejaVu 라이선스: [LICENSE.fonts-dejavu-core](LICENSE.fonts-dejavu-core).
- 재생성: Pillow와 위 JSON에 기록된 호스트 글꼴 설치 후 `python3 도구/터미널글꼴빌드.py`. Pillow/FreeType와 원본 글꼴 버전에 따라 결과가 바뀔 수 있으므로 새 해시를 확인한다.
- SD 이미지와 부팅 ZIP에는 두 라이선스 및 출처 JSON이 동봉된다.

## COSL 배포를 위한 원격·유선망 교체

- `libassh/`: 1.1 전체 소스, LGPL-2.1-or-later. 별도 라이브러리로 컴파일하고 소스와 커널 재연결 자료를 제공한다.
- `bearssl/`: 0.6, MIT. SHA256와 VNC DES 인증만 연결한다.
- `freebsd-genet/`: FreeBSD releng/14.3의 MAC(BSD-2-Clause)·PHY(BSD-4-Clause) 출처. 새 lwIP 포트는 `../통신망/유선망.c`.
- 버전과 해시: `remote-sources.json`. 이전 wolfSSH/wolfSSL과 U-Boot 파생 GENET은 현재 소스 트리에서 제거했다.
- 배포: `make cosl-dist`. 제3자 고지와 LGPL 소스·재연결 묶음을 SD 이미지와 부팅 ZIP에도 포함한다.

This product includes software developed by Bill Paul.
