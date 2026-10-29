# 자체 ARM64 Java 커널 국가판

`country/<ISO3>/Makefile`은 해당 국가의 jkoros 원문과 지정된 버전의 외부 구성요소를 사용한다.
기존 `country/<ISO3>/<언어>/` Linux·OpenJDK 판과 별도의 실행 기반이다.

`native-vendor.tar.gz`와 `qemu-host.tar.gz`는 각 국가 폴더 안의 독립적인 일반 파일이다.
국가별 `native.json`의 SHA-256과 일치하는지 검사한다. 한 국가의 파일을 바꿔도
다른 국가의 파일은 변하지 않는다. `make clean`은 이 원본 압축파일을 지우지 않는다.

국가판을 독립적으로 옮길 때는 WorldOS 최상위에서
`make native-export COUNTRY=KOR OUTPUT=/새/폴더`를 실행한다. 내보낸 폴더에는
실제 압축파일이 포함되므로 공통 저장소 없이 빌드할 수 있다. 언어별 Linux 판과
사용자 데이터 디스크는 포함하지 않는다. 기존 출력 폴더는 덮어쓰지 않는다.
국가 폴더 자체를 복사해도 다른 폴더의 압축파일을 참조하지 않는다.

`make native-materialize`는 국가별 체크섬을 모두 확인한 뒤 이전 공유 링크를
국가별 실제 파일로 바꾼다. 여러 번 실행해도 같은 상태를 유지한다.
`make test-native-archives`는 버전 보존, 이동, 독립 내보내기와 실패 시 보존 동작을 검사한다.

생성·명명·입력·실행 검증 결과는 이 디렉터리의 도구와 `build/native/`에 기록한다.
[국가별 현황](국가별현황.md)과 [실제 검증 범위·미완료 항목](검증결과.md)을 확인한다.
국가 대표 언어는 golang/worldos의 CLDR 기반 선택표를 보존한다. 한 국가의 모든
주민이 한 언어를 사용한다는 뜻이 아니며, 개별 언어의 역사적 어원은 검증한
문헌이 있을 때만 확정한다. 현지어 명명안과 미번역 목록을 구분한다.

```sh
cd /home/user/java/worldos
make native-build COUNTRY=JPN
make native-desktop COUNTRY=JPN ARGS=--network
make native-run COUNTRY=KOR
make native-image COUNTRY=KOR
```

국가 폴더 안에서는 `make build`, `make run`, `make desktop ARGS=--network`,
`make image`를 사용한다. `RESOLUTION=1920x1080`이 기본값이며 `640x480`도 가능하다.
Remmina의 VNC 주소는 `127.0.0.1:5902`; 다른 포트는 `ARGS="--network --port 5903"`.
동시에 여러 네트워크 판을 실행할 때는 `ARGS="--network --network-host 127.0.0.2 --port 5903"`처럼
호스트 루프백 주소와 VNC 포트를 구분한다. FTP 접속 주소도 해당 루프백 주소를 쓴다.

게스트에서 `help system`으로 IP 설정·ping·상태 조회·종료 명령을 확인한다.
`ipconfig`, `ip`, `ping`, `route`, `netstat`/`ss`, `ps`, `top`, `free`, `df`, `uptime`, `poweroff`와
국가별 별칭을 지원한다. [사용법과 범위](네트워크와체계명령.md), 각 판의 `native-commands.json`을 참고한다.

호스트에는 Python 3, `javac --release 8`을 지원하는 JDK, Clang/Clang++,
`aarch64-linux-gnu-ld`, `aarch64-linux-gnu-ar`, `aarch64-linux-gnu-objcopy`,
`libnewlib-dev`가 필요하다. SD 이미지 제작에는 `mkfs.vfat`, `mcopy`도 필요하다.
국가 폴더의 QEMU 묶음은 x86_64 Linux용이다. 다른 호스트는 `QEMU_AARCH64`에
`raspi4b`를 지원하는 QEMU를 지정한다. 운영체제를 실행하는 것은 그 폴더의
자체 커널이며, QEMU·입력 다리는 호스트 실행 도구다.

각 판의 `example/`은 판 내부 실제 소스에 연결된 상대 경로다. 운영체제 안에서도
`/example/java`, `/example/c`, `/example/python`에 설치된다. 일본어판 예:

```sh
cd /example/java
javac 出力例.java
java 出力例
java 窓例
vi 出力例.java
```

`make desktop`의 VNC 화면에서 F9 또는 Shift+Space는 ASCII와 판별 입력기를 전환한다. 호스트 자판/입력기는
영문 상태로 둔다. 일본어는 로마자→가나(`nihongo`→`にほんご`), 한국어는 두벌식,
중국어는 병음 한 음절 후보(공백으로 다음 후보, F9로 확정), 에티오피아 문자는
SERA, 그 밖은 XKeyboardConfig의 해당 자판 표를 사용한다. 중국 간체/번체는
각각 GB2312/Big5 후보 집합을 쓴다. 자동 단어 예측이나 일본어 한자 사전 변환은
아직 없다. 오른쪽 Alt로 AltGr, Ctrl+Shift+U → 16진 코드 → Enter로 유니코드
직접 입력, Ctrl+Shift+V로 명시적 붙여넣기가 가능하다. vi는 `i` 입력,
영문 모드로 돌아온 뒤 Esc와 `:wq`로 저장한다.
`make run`의 직렬 콘솔에서는 호스트 터미널의 입력기 또는 UTF-8 붙여넣기를 사용한다.
이 전환 기능은 실물 Pi 4의 USB 키보드 드라이버를 대신하지 않는다.

이름은 `native-names.tsv`, 미번역 식별자는 `native-pending.tsv`, 근거는
`native-term-evidence.json`에서 확인한다. 원문과 라이브러리 자체의 선언·참조를
바꾸며, Java 클래스의 JVM 서술자도 같이 바꾼다. 표준 Java/C ABI와 예약어는
유지한다. 기존 JDK 전체를 각 언어로 새로 구현했다는 뜻은 아니다.

국가명과 언어별 용어표는 따로 관리한다. 관리형 Java 패키지의 국가 부분은
해당 언어로 쓴 국가명을 사용하고, 프로젝트 이름은 `J` + ISO 3자리 코드의
첫 글자 대문자 형태 + `OS`로 만든다. 중국은 `中国/JChnOS`, 베트남 중국어판은
`越南/JVnmOS`, 베트남어판은 `Việt_Nam/JVnmOS`가 된다. 경로와 package·import,
실행 클래스, 관리형 체계 정보의 시스템 이름을 함께 바꾼다.
`native/inputs/country-names.json`은 CLDR 48의 국가명을 고정한 자료이며 원본
압축파일의 SHA-256과 라이선스를 함께 보존한다. 번역 자료가 없거나 현재 호스트의
Unicode 식별자 지원이 부족한 경우 ISO 코드를 쓰고 미완료 상태를 기록한다.
`MMR/stu`와 `VNM/hnj`는 각각 삼타오어와 몽어판이며, 대표 언어와 구분한다.

베트남어의 원본 한국어 역할 3,656개와 미얀마어 역할 2,783개는 기능 중심 제안이다.
미얀마어의 주소·송신·실행 이미지 관련 오역과 의미 없는 해시 접미사를 수정했다.
미번역 역할, 원래 영어였던 자체 보조 코드, 설명문과 원어민·어원 검토는 남아 있다.
변수명과 표준 인터페이스가 같은 이름을 쓰던 이전 번역은 원본 문맥을 비교해 복구한다.
예를 들어 베트남어의 문서 데이터 변수는 바꾸면서 실제 `README.md` 참조는 맞춘다.

Java 주석은 식별자 치환과 별도로 문장 전체를 번역한다.
`inputs/localized-java-prose.json`은 11개 언어 프로필별 일반 주석 131종과
예외 설명문 19종, 라이브러리 오류 안내 20종을 담는다. 원어민 검토가 완료된 자료는 아니다.
이전 용어 치환으로 모양이 달라진 주석은 `comment_aliases`에 문장 전체를 기록해 처리한다.
낱말을 추측해서 바꾸거나 문자열 안의 같은 문장을 번역하지 않는다.
`java_prose.py`를 생성기와 기존 판 수정 도구가 함께 사용한다.
오류 안내는 자체 Java 라이브러리 범위에서만 바꾸며, 문자 시험 표본·저작권·작성자 이름은 보존한다.
`audit_java_localization.py`는 식별자, 경로, 한국어가 남은 주석과 라이브러리 안내를 따로 보고한다.
이 검사는 원래 영어였던 이름과 전체 문서의 완역을 인증하지 않는다.

```sh
python3 tools/apply_country_naming.py --namespace-only --apply
python3 tools/apply_country_naming.py --languages vi my --apply
python3 tools/apply_country_naming.py --prose-only --languages my en ja zh zh_Hans zh_Hant de fr es vi mr --apply
python3 tools/audit_country_naming.py --jobs 8
python3 tools/audit_java_localization.py
python3 tools/verify_country_namespaces.py --jobs 2 \
  --editions country/VNM/zh_Hant country/VNM/hnj country/MMR/stu
python3 tools/check_country_sources.py --languages vi my --countries VNM MMR
python3 native/verify_country_boots.py --all --jobs 2
```

`--namespace-only`는 기존 언어 용어표를 유지하고 국가 이름과 관련 참조만 변경한다.
관리형 Java 시험은 각 대표판의 29개 파일을 컴파일하고 해당 국가 패키지의 시험을
실제로 실행한다. ARM64 부팅과 별개의 결과다. 소스 변경 전 백업은
`build/country-localization/before-*.tar.gz`에 저장하며 사용자 파일은 보존한다.

독일어 `Arbeitsfaden`은 실행의 연속성을 실에 비유하는 기능 중심 명명안이다.
어근 `Faden`의 중·고대 고지 독일어 형태는 [Duden](https://www.duden.de/rechtschreibung/Faden)에
기록돼 있다. 이 어근의 역사와 프로젝트의 새 합성어를 구분한다. 다른 언어의
어원을 이 설명으로 대신하지 않으며, 원어민 검토와 언어별 어원 검토는 별도 과제다.

화면 글꼴은 실제 cmap에 있는 글리프를 Noto·DejaVu에서 골라 생성했다. UTF-8을
보존하지만, 복잡한 인도계 문자 결합 조판과 완전한 오른쪽→왼쪽 배치는 아직
구현되지 않았다. 글리프 수록을 완전한 조판 지원으로 세지 않는다.
[Unicode 양방향 조판 규격](https://www.unicode.org/reports/tr9/)이 설명하는
논리 순서와 표시 순서의 구분도 남은 작업에 포함한다.

현재 커널의 JVM·MicroPython·TinyCC·네트워크·GUI 부분집합을 계승한다.
전체 OpenJDK/Swing, 영구 SD 파일체계, 실물 Pi4 USB 입력·GENET 네트워크 지원은
추가되지 않았다. SD 이미지를 만들 수 있는 것과 실물 Pi4에서 시험한 것은 다르다.

`make native-verify`는 모든 국가의 자료 독립성·이름/예제·입력·글꼴 범위를 검사한다.
`make native-test COUNTRY=JPN`은 실제 QEMU/VNC에서 입력·vi·게스트 컴파일러를
시험한다. 생성 판수와 실제 부팅 시험 판수는 `build/native/` 보고서에서 구분한다.
`make native-test COUNTRY=KOR ARGS=--network`는 TCP·UDP와 FTP JAR 실행도 검사한다.
`make native-relocate COUNTRY=JPN`은 다른 국가와 기존 빌드를 복사하지 않고 새 경로에서 빌드한다.
`make native-test-system COUNTRY=JPN`은 그 국가판을 빌드하고 실제 IP 변경·ICMP·FTP·상태 조회·현지어 명령·종료를 검사한다.


Java 전환 후 국가 실행은 `native-launch.sh`와 `native-java/`의 Java 구현을 사용한다.
`native-edition.py`는 호환 진입점이다. 기존 1,578개 언어판(777개 언어)에도
독립 `native-source/`를 추가한다. 언어판에서는 `make native-build`,
`make native-desktop ARGS=--network`, `make native-run`을 사용한다.
`make -f native.mk x86-iso`는 별도 x86 커널을 만든다.
언어판의 의존성 묶음은 부모 국가에 있으므로 국가 폴더 전체를 복사한다.

추가 소스에는 ARM64·x86/POSIX·기존 관리형 Java 커널·한국어 라이브러리·Linux 실행판
도구가 포함된다. 각 native.json의 upstream_source_sha256으로 공통 기능 원문의
버전을 추적한다. 실행 기반이 다른 기능을 ARM64 이미지에 모두 합친 것은 아니다.
Java 전환 범위와 남은 Python/C 경계는 java_migration 필드에 명시한다.
SSH/VNC·GENET 드라이버 소스도 포함하며, 실제 Pi4 장치 검증과 전체 OpenJDK,
영구 SD 파일체계 및 USB 입력은 여전히 미완료다.

`python3 native/verify_editions.py`는 모든 언어판의 파일 해시·독립성·기능 원문
포함과 Java 도구 컴파일을 검사한다. 실제 부팅 시험은 native/verify_runtime.py로
별도로 수행한다. 명명안과 사전 근거는 native/inputs/term-evidence.json에도 기록한다.
배포 pack.sh는 모든 언어판의 재현 가능한 vendor 파일과 빌드·캐시를 제외하며,
사용자 수정은 보존한다. unpack.sh는 기존의 자동 다운로드·준비 동작을 유지한다.

## 국가·언어판의 이름 번역

`native/inputs/localized-roles/*.json`은 언어 코드별로 보존한 기능 중심 이름 제안입니다.
국가 대표판과 해당 국가 안의 개별 언어판은 각각의 언어 사전을 사용합니다.
마라티어(`mr`)를 힌디어(`hi`)로 처리하거나 다른 문자 체계의 사전을 대신 쓰지 않습니다.
언어 이름을 나타내는 패키지는 해당 언어의 자기 이름을 사용합니다.

공개 IT 용어 수집에는 Microsoft Terminology TBX 자료를 사용합니다.
일본어·중국어 간체/번체·독일어·프랑스어·스페인어는 별도로 직접 작성한
`*-role-words.tsv`와 `reviewed-roles/*.json`의 기능별 명칭으로 구성합니다.
`tools/compose_reviewed_roles.py`는 3,656개 역할의 누락·충돌·예약어·실제 게스트
경로 제한을 검사합니다. 중의적인 사전 낱말의 최단 번역을 그대로 고르지 않고,
전체 역할의 뜻과 어순을 명시적으로 교정합니다. 예를 들어 일본어의 장치는
`装置`, 실행 관리는 `実行管理`이며, 프로세서 이름 `x86`은 좌표로 번역하지 않습니다.
번체 사전은 자체 어휘 선택과 버전이 고정된 OpenCC 문자 자료를 함께 사용합니다.
문자 변환을 다른 중국어 계열 언어의 번역으로 취급하지 않습니다.
낱말의 뜻을 조합한 새 식별자는 현대의 기능 중심 제안이며, 역사적으로 존재했던
컴퓨터 용어라는 주장이 아닙니다. 기존 사전의 역사·어원 근거는
`native-term-evidence.json`에 별도로 남깁니다. 원어민 검토와 전체 어원 검토는 미완료입니다.
언어 예약어, 외부 API, 호출 규약, 저작권·라이선스, 문자값 시험 자료는 보존합니다.

사전에 없는 이름, 게스트의 경로·파일 용량 제한에 맞지 않는 제안은
`native-pending.tsv`와 사전의 `pending_roles`에 남깁니다. 영어 대체어나 다른 언어를
넣고 현지어 번역 완료로 표시하지 않습니다. 현재 모든 언어의 번역이 완료된 상태는 아닙니다.

```sh
# 선택한 언어의 공개 용어 자료를 오프라인 이름 사전으로 저장
python3 tools/collect_terminology_roles.py --languages mr --archive /path/to/MicrosoftTermCollection.zip
# 모든 국가·언어판에 변경을 미리 확인한 뒤 적용; 변경 전 백업을 자동 생성
python3 tools/apply_country_naming.py
python3 tools/apply_country_naming.py --apply
# 기존 de/fr/es 별칭이 외부 API·옵션·경로와 겹친 경우 원본 위치로 대조해 복구
python3 tools/reconcile_country_aliases.py
python3 tools/reconcile_country_aliases.py --apply
# 파일 소유권·참조·공개 클래스명·미번역 이름 확인
python3 tools/audit_country_naming.py
python3 tools/audit_country_naming.py --countries IND --languages mr --require-complete
# 직접 작성한 낱말·역할 교정에서 충돌 없는 이름 사전을 재구성
python3 tools/compose_reviewed_roles.py --language ja --write
# 각 국가 대표판의 현재 소스로 실제 부팅·UTF-8 저장·게스트 Java/Python/C 실행
python3 native/verify_country_boots.py --all --jobs 2 --qemu country/JPN/host/qemu
```

국가별 부팅 결과는 `build/native/country-boots/summary.json`과 각 국가의
`report.json`, `serial.log`에 저장합니다. 성공 결과도 현재 소스 SHA-256과
실행 이미지 SHA-256, Java 실행기·진입 스크립트 SHA-256이 같을 때만 재사용합니다.
소스의 이름·내용과 의존성 버전이
정확히 같은 경우에는 이전에 검증된 이미지를 독립된 일반 파일로 복사하여
컴파일을 재사용할 수 있지만, 해당 국가 폴더의 이미지로 부팅 검사는 다시 합니다.
별도 관리형 Java 트리와 루트 문서 일부를 제외한 보수적인 ARM64 입력이 같은 경우도
통과한 판의 전체 소스·이미지 해시를 먼저 대조한 뒤 독립 복사로 재사용합니다.
제외되는 관리형 Java는 국가별 컴파일·실행 검사로 따로 확인합니다.
입력기의 실제 키 전환·vi·GUI 검사는 `native/verify_runtime.py`로 별도 수행합니다.
이 결과는 QEMU ARM64 검사이며, 모든 언어판·모든 아키텍처·실물 장치의 부팅
검증이나 국가 폴더 전체의 현지어화 완료를 의미하지 않습니다.

기존 판의 갱신과 새 판 생성은 같은 이름 사전과 내장 JVM 자원 이름 제한을 사용합니다.
완료 판에서도 실행기, 삽입된 시험 코드, 파일·폴더 이름에 한국어가 남으면 검사가 실패합니다.
이 검사의 완료 범위는 `native.json`이 관리하는 소스와 native Java 실행기입니다.
이름 잔여 검사는 원래 한국어 식별자·경로 목록을 기준으로 하며, 모든 외래어의
현지어 적합성이나 고정된 영어 도구·경로까지 현지어로 바뀌었음을 보증하지 않습니다.
별도 Linux 실행판의 `edition.py`, `archive.py`, `Workspace.java`, `SystemCalls.java`에는
영어로 작성된 자체 식별자가 남아 있으므로 국가 폴더 전체의 현지어 명명 완료를 뜻하지 않습니다.
원래 영어로 작성된 자체 native 보조 코드도 별도의 의미·참조 분석이 더 필요합니다.
Python 모듈 파일명과 import 식별자는 같은 NFKC 정규형을 사용합니다.
원본 저장소의 소스가 필요하므로 번역 수집·생성은 WorldOS 개발 작업 폴더에서 수행합니다.
일반 국가판 빌드에는 번역 서비스나 TBX 자료가 필요하지 않습니다.

출처: [Microsoft Terminology](https://learn.microsoft.com/en-us/globalization/reference/microsoft-terminology),
[Debian iso-codes](https://salsa.debian.org/iso-codes-team/iso-codes).
