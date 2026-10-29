# WorldOS — 국가·언어별 Java 운영체제

최신 jkoros **자체 ARM64 Java 커널**의 국가판은 `country/<ISO3>/`에서 빌드·실행합니다.
예전 Linux·OpenJDK 판은 그 아래 언어 코드 폴더에 보존했습니다.

IP는 최상위 [ip.conf](ip.conf)에서 설정합니다. 기본값은 `192.168.0.100`, 넷마스크는
`255.255.255.0`, 게이트웨이는 `192.168.0.1`입니다. 설정 변경 후 실행하면 자체
ARM64 커널을 자동으로 다시 빌드하며 QEMU NAT도 같은 대역을 사용합니다.
국가·언어판만 다르게 설정하려면 해당 판의 `native.json` 옆에 `ip.conf`를 두거나
`IP_CONFIG=/절대경로/ip.conf`를 지정합니다. 독립 복사본은 소스 폴더의 `ip.conf`를
사용합니다. 자체 x86 커널은 `make x86-build`로 다시 빌드합니다. 실제 보드에 쓸
이미지도 설정 변경 후 다시 생성해야 합니다.

```sh
cd /home/user/java/worldos/country/JPN
make build
make desktop ARGS=--network
# Remmina: VNC 127.0.0.1:5902
```

한국어는 `country/KOR`, 영어는 `country/USA`, 중국어는 `country/CHN`입니다.
각 국가 폴더에는 자체 소스와 Java·C·Python 예제, 빌드 의존 자료와
QEMU 압축파일이 실제 파일로 들어 있습니다. 폴더 하나만 복사해도 다른 국가나
공통 저장소 없이 빌드할 수 있습니다. `make clean`은 이 원본들을 보존합니다.

국가판을 별도로 복사하려면 WorldOS 최상위에서 아래 명령을 사용하세요.
새 출력 폴더에 네이티브 소스와 실제 압축파일을 함께 복사하므로 공통 저장소 없이
사용할 수 있습니다. 기존 Linux 언어판과 사용자 디스크는 이 내보내기에 포함되지 않습니다.

```sh
make native-export COUNTRY=KOR OUTPUT=/tmp/worldos-kor-native
make -C /tmp/worldos-kor-native build
```

호스트 빌드 도구는 필요합니다. 기존 공유 링크가 남은 작업 복사본은
`make native-materialize`로 국가별 실제 파일로 바꿀 수 있습니다.
배포용 `pack.sh`도 이 검사를 자동으로 수행합니다. 실행 중 `help input`은
해당 판의 입력 방법을 보여 줍니다.

국가별 생성 범위·명명 미완료 목록·입력 및 문자 조판의 한계는
[자체 커널 국가판 안내](native/README.md)와 각 국가의 `NATIVE.md`에 기록합니다.
국가 폴더가 만들어졌다는 사실을 모든 식별자와 어원의 번역 완료로 해석하면 안 됩니다.
[국가별 현황](native/국가별현황.md), [자체 커널 검증 결과](native/검증결과.md)에서
실제 시험한 판과 남은 번역·조판 범위를 확인할 수 있습니다.

## 기존 Linux·OpenJDK 실행판

사용자가 운영체제 안에서 Java 원문을 작성하고 `javac`로 컴파일한 뒤 전체 OpenJDK로 실행하는 개발 환경이다. Linux 6.18, Alpine 3.24, OpenJDK 25, musl, X.Org, Swing, GCC, 유니코드 글꼴과 Fcitx5 입력기를 포함한다. 이전 jkoros의 제한된 JVM과 별도로 구현했다.

```sh
cd /home/user/java/worldos
make run EDITION=KOR/ko
```

한국어 판의 원본은 [작업마당.java](country/KOR/ko/원문/작업마당.java)와 [체계호출.java](country/KOR/ko/원문/체계호출.java)에 있다. `make run EDITION=JPN/ja`, `make run EDITION=SAU/ar`처럼 다른 판을 선택한다. 실행 전 빌드가 없거나 소스가 변경되면 해당 판만 컴파일한다. 화면의 파일명과 주 클래스 이름을 지정한 뒤 컴파일·실행을 누르면 된다.

| 기능 | 실행 기반 |
|---|---|
| Java 컴파일·JVM·JIT·GC·리플렉션·스레드 | 전체 OpenJDK 25 |
| Swing·AWT·Java2D·창·입력 | X.Org 또는 시험용 Xvfb, Java Desktop |
| 파일·디렉터리·권한·심볼릭 링크·메모리 매핑 | Linux/musl 및 java.io/java.nio |
| TCP·UDP·DNS·HTTP·HTTPS·TLS | Linux 네트워크와 표준 Java 라이브러리 |
| 프로세스·C/POSIX·pthread·Unix 소켓 | Linux/musl, GCC |
| JNI 네이티브 라이브러리 | OpenJDK JNI 헤더와 GCC |
| 사용자 코드·설정 영구 보관 | 판별 ext4 쓰기 디스크 |
| 여러 문자권의 편집·입력 | UTF-8, Noto, Fcitx5 및 m17n 등 |

표는 실행 기반의 범위다. 모든 JDK API·하드웨어·외부 라이브러리를 각각 시험했다는 뜻은 아니다. JavaFX, JDBC 드라이버, Maven/Gradle 같은 별도 배포 구성요소는 추가 설치 대상이다. 이 이미지의 GUI는 가상 그래픽 장치에서 동작하며 3D 가속·실제 오디오 장치·물리 장치별 드라이버를 모두 검증한 제품은 아니다. POSIX 인증을 주장하지 않는다.

ISO 3166-1 국가·지역 249개, CLDR 48의 국가별 사용 언어 조합 1,578개(언어 코드 777개)를 수록했다. 각 판은 실제 Java 원본·이름 사전·메시지·POSIX 별칭·예제·빌드 도구를 갖는다. 모든 판의 Java 컴파일과 JAR의 국가별 클래스 분리, C 헤더 컴파일을 확인한다. 최신 결과는 [판 검증 보고서](build/edition-verification.json)와 [통합 시험 결과](build/verification/)에 남는다.

**번역·어원 작업은 전체 완료 상태가 아니다.** 영어 대체어 없이 59개 개념의 제안을 갖춘 판은 352개이고, 1,226개 판에는 미번역 개념이 남아 있다. 모든 제안의 원어민·개별 언어 어원 검토는 대기 상태다. 컴퓨터 개념의 역사적 문헌과 각 언어 표현의 어원은 구분하며, 한 국가 전체에 동일한 철학을 부여하지 않는다. [명명 범위](naming/README.md), [명명·독립성 설명](docs/명명과-독립성.md), [수록 현황](naming/coverage.json)을 참고한다.

독립성이란 다른 나라 소스에 의존하지 않고 해당 판만 빌드·실행·수정할 수 있다는 뜻이다. Linux·OpenJDK 등 외부 실행 기반은 공통 캐시를 사용한다. `make export EDITION=KOR/ko OUTPUT=/tmp/worldos-kor`는 외부 실행 이미지까지 포함한 별도 디렉터리를 만든다. 각 나라별로 Linux/OpenJDK 자체를 새로 재작성한 커널은 아니다.

- [실행·빌드·시험·독립 내보내기](docs/실행과-개발.md)
- [검증 범위와 결과](VERIFICATION.md)
- [외부 구성요소와 자료 출처](docs/외부-구성요소.md)
- [기존 GitHub 코드를 old에 보관하고 golang/worldos 올리기](docs/GitHub-업로드.md)

Java/POSIX 표준 API와 언어 키워드는 유지한다. 프로젝트의 Java 클래스·메서드·필드·지역변수·원본 파일명에 언어별 제안을 적용한다. 공통 생성·빌드·시험 도구와 기계가 읽는 고정 메타데이터는 관리 인터페이스로 유지한다. 번역어가 없는 부분을 임의의 어원으로 꾸며 완성된 구현으로 세지 않는다.

외부 배포용 `pack.sh` / `unpack.sh`와 자동 의존성 복원은 [배포 안내](distribution/README.md)를 참고하세요.


자체 커널의 Java 전환은 [native 안내](native/README.md)에 기록한다.
모든 기존 언어판에는 별도의 독립 native-source와 native-* 빌드·실행 목표를 추가한다.
번역이 없는 낱말은 검토 필요로 남기며, 전체 언어의 어원을 검증 완료로 표시하지 않는다.
