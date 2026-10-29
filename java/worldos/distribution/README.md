# 외부 배포용 압축과 복원

배포 압축 형식은 gzip을 사용하는 `tar.gz`다. `--level 0..9`로 압축 수준을
지정할 수 있으며 기본값은 9다. 기존 `.tar.xz` 배포본도 `unpack.sh`로 풀 수 있다.

Ubuntu x86_64에서 `./pack.sh`를 실행하면 `dist/worldos-source.tar.gz`, 체크섬,
독립 실행 가능한 `dist/unpack.sh`를 만든다. 원본 파일은 삭제하지 않는다.
압축파일은 2 GB 제한을 검사하며 `./pack.sh /경로/worldos-source.tar.gz`로
출력 위치를 지정할 수 있다.

외부 PC에 압축파일, `.sha256`, `unpack.sh`를 함께 전달하고 실행한다.

```sh
./unpack.sh worldos-source.tar.gz /원하는/새/경로/worldos
make -C /원하는/새/경로/worldos native-build COUNTRY=KOR
make -C /원하는/새/경로/worldos build-all
```

압축 해제 후 의존성을 자동 다운로드한다. 부족한 Ubuntu 빌드 도구는
`sudo apt-get`으로 설치하며 관리자 암호가 필요할 수 있다. 공통 Linux/OpenJDK
실행 환경까지 준비하므로 이후 국가판 및 언어판 빌드를 시작할 수 있다.
Alpine 3.24 저장소의 사용 가능한 패키지를 설치하고 실제 버전을 기록한다.

`--profile native`를 붙이면 자체 ARM64 국가판에 필요한 준비만 수행한다.
호스트 도구가 이미 있으면 `--no-host-install`을 추가한다. `--no-prepare`는
검증을 위해 소스만 풀 때의 명시적 선택이며 기본값은 자동 다운로드다.
네트워크 오류 후에는 풀린 프로젝트에서 `./unpack.sh --prepare`로 재개한다.

빌드 결과, Python 캐시, 로그, VirtualBox 상태, 개인 디스크와 접속 키는 제외한다.
국가별로 풀려 있는 QEMU와 원본 vendor 파일은 국가 폴더의 압축파일에서 다시
복구하므로 제외하고, vendor의 로컬 수정은 보존해 준비 단계에서 적용한다.
Alpine 부트스트랩 다운로드 파일과 사용하지 않는 ISO/패키지 인덱스도 제외한다.

현재 자체 제작한 `native-vendor.tar.gz`, `qemu-host.tar.gz`에는 공개 다운로드
주소가 없다. 따라서 배포 압축파일 안에는 같은 해시의 내용을 한 번 기록하고,
압축 해제 시 각 국가 폴더에 **별도의 일반 파일**로 복사한다. 압축 안에서만
사용하는 tar 하드링크는 압축 해제 후 실제 하드링크로 남지 않는다.
이전 `native/resources/archives/` 저장소는 배포본에서 제외한다.
`tar` 명령으로 직접 풀면 하드링크가 유지될 수 있으므로 반드시 `unpack.sh`로 복원한다.

일반 빌드에는 다른 프로젝트 경로가 필요 없다. 국가별 소스 자체를 재생성할 때만
jkoros 소스가 필요하며, 인접한 `jkoros` 폴더를 찾거나 `JKOROS_ROOT=/경로/jkoros`를
사용한다. 국가 선택표와 이름 사전 입력은 이 프로젝트 안에 포함되어 있다.
게스트 운영체제의 `/home/user` 경로는 호스트 경로와 별개이므로 변경하지 않는다.

249개 국가의 독립 파일을 복원하므로 압축 해제 후 작업 폴더는 2 GB를 넘는다.
실제 다운로드 후 작업 폴더와 빌드 산출물도 더 커질 수 있다. 제외 목록과
압축 크기는 `dist/worldos-source.tar.gz.report.json`에서 확인한다.

동일한 내용의 소스 파일도 압축 안에서 한 번만 저장한다. `unpack.sh`는 이를
각 경로의 독립 일반 파일로 복원하고 파일별 실행 권한을 유지한다.
