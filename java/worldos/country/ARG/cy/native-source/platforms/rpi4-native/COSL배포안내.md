# COSL 상업 조건을 유지하는 자체 ARM64 배포판

2026-10-04~05 전환. SSH의 GPL wolfSSH/wolfCrypt를 LGPL-2.1-or-later libassh로,
VNC 인증 암호를 MIT BearSSL로, U-Boot 파생 GENET을 FreeBSD BSD 구현으로 교체했다.
유료 라이선스를 구매하거나 제3자 코드의 라이선스를 임의로 변경하지 않았다.

자체 코드에는 [루트 LICENSE](../../LICENSE)를 적용한다.
실제 파일은 저장소 루트 `jkoros/LICENSE`, 고지 목록은 `jkoros/THIRD_PARTY_NOTICES.md`이다.
COSL의 상업 이용 조건·요율을 유지하면서, 모순되던 표준 GPL 허가 도입문을 이 배포판에서
제외하고 제3자 코드와 LGPL 권리를 보장하는 적용 범위를 추가했다. GitHub 저장소에는 아직 게시하지 않았다.

libassh와 TinyCC 자체는 LGPL이므로 그 소스와 수정 사항을 제공해야 한다.
커널 자체 코드 전체를 GPL로 바꾸는 방식은 아니다. 배포받은 고객이 자신의 사용을 위해
수정하고 LGPL 구성요소를 바꾸어 다시 연결하며 이를 디버깅할 수 있어야 한다.
이는 루트 LICENSE에서 COSL의 상충 조항보다 우선한다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
make cosl-dist RESOLUTION=1920x1080
```

생성된 이미지·부팅 ZIP과 `jkoros-native-relink.tar.gz`를 함께 제공한다.
재연결 묶음은 해당 커널의 객체·라이브러리, LGPL 소스와 설정, 빌드·재연결 도구를 포함한다.
기본 재연결은 libassh를 소스에서 다시 컴파일하고 동일 커널 이미지를 재생성한다.
TinyCC 수정은 묶음의 README에 있는 SDK 경로와 `--tinycc` 절차를 따른다.
사용자의 일반 개발 소스 배포에서는 `build/remote`의 접속 비밀 자료와 개인용 바이너리를 제외한다.
배포용 이미지에 내장된 장치 키는 해당 이미지마다 관리해야 한다.

`dist/jkoros-native-rpi4.img`는 SD 이미지, `dist/jkoros-native-rpi4-boot.zip`은
부팅 파일 묶음이다. 둘 다 LICENSE·제3자 고지·ffynhonnell_coeden/재연결 꾸러미를 내부에 포함한다.
`make cosl-check`는 이전 wolfSSH/wolfSSL 소스·심볼이 남았는지와 커널 이미지의 일치 여부를 검사한다.
`make test-relink`는 묶음을 별도 경로에 풀어 원본 커널을 재현한 뒤, TinyCC를 수정하고 다시 연결한
커널에서 수정된 기능을 요구하는 C 소스를 실제로 컴파일·실행한다.

검증 기록: `build/verification/native-remote/report.json`(OpenSSH 암호 인증·키 갱신·Java 실행,
VNC 화면·한글 입력), `build/verification/execution-network-review/report.json`(QEMU 외부 TCP/UDP·FTP),
`build/verification/cosl-relink/report.json`(LGPL 재연결).
GENET의 링·경계·MDIO 동작은 `make test-genet`의 호스트 모의 시험으로 검사한다.

LGPL의 결합 프로그램 배포·재연결 조건은 [GNU LGPL 2.1 제6항](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)에 따른다.
이전 GPL 구성의 백업은 배포 트리 밖 `/home/user/jkoros-gpl-archive-20261004`에 보존했다.

BSD PHY 고지: **This product includes software developed by Bill Paul.**
PHY 기능·사용을 언급하는 광고 자료에도 이 문구를 넣는다.

이 검토·묶음은 현재 자체 ARM64 판에 한정된다. Linux 실행판이나 이전 worldos 국가별
복사본을 같은 배포물에 넣을 때에는 각 원본의 조건을 별도로 적용해야 한다.
실물 Pi4 LAN은 미검증이며, COSL의 특허 효력·요율·관할 문구에 대한 법률 검토를 대신하지 않는다.
