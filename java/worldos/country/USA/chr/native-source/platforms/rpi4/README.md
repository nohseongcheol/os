# jkoros Raspberry Pi 4 실행판

Raspberry Pi 4의 ARM64 Linux 실행판이다. 기존 `../../os`의 자체 x86 Java 커널과 별도 부팅 경로다. Linux가 CPU·ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ·ᎠᏅᏓᏗᏍᏙ_ᎦᏟᏌᏅᎯ·스레드·ᎠᏍᏆᏂᎪᏙᏗ·네트워크를 제공하고, 전체 OpenJDK와 한국어 Java 작업마당이 그 위에서 실행된다.

Linux 없이 부팅하는 **자체 Java ARM64 커널의 초기 이식판**은 [rpi4-native](../rpi4-native/README.md)에 있다. 그 이식판에는 이 문서의 OpenJDK·Python·Swing 기능이 아직 구현되지 않았다.

## 제공 ᎠᏍᏆᏂᎪᏙᏗ

`dist/`에 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 바이너리를 생성한다.

| ᎠᏍᏆᏂᎪᏙᏗ | 용도 |
|---|---|
| `jkoros-rpi4-system.img` | microSD에 기록할 FAT 부팅 파티션 + 읽기 전용 SquashFS 시스템 |
| `jkoros-user.img` | 별도 USB 저장장치에 기록할 ext4 ᎬᏗᏍᎩ ᎦᏟᏌᏅᎯ ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ, 4 GiB |
| `*.img.gz`, `SHA256SUMS` | 전달용 ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ 이미지와 SHA256 ᎪᎯᏳᏙᏗ Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ |
| `openjdk25-jdk-linux-aarch64-musl.tar.gz` | 컴파일된 ARM64 JDK |
| `openjdk25-jre-linux-aarch64-musl.tar.gz` | jlink로 구성한 컴파일된 ARM64 JRE |
| `한국어자바.jar` | 한국어 이름으로 ᎠᏍᏆᏂᎪᏙᏗ·문자·통신·작업·화면을 사용하는 Java ᏧᏂᎪᎵᏰᏗᎢ |
| `manifest.json`, `java-runtimes.json` | ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ/런타임 SHA256, 아키텍처와 구성 |
| `packages.lock.json`, `sources.lock.json` | ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 설치된 패키지 버전·출처·라이선스 msinfo32_exe |

JDK/JRE는 이 실행판과 같은 **Linux ARM64 + musl** 환경용이다. 다른 libc/CPU/운영체제에서 단독 실행을 보장하지 않는다. 네이티브 의존 라이브러리는 ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ 이미지에 함께 들어 있다. JRE는 Java SE와 문자셋·다국어·ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ·ZIP ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ 등 ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ 모듈을 포함하고, 전체 개발 도구는 JDK에 있다.

## 설치와 ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ

1. Raspberry Pi Imager의 ᎬᏗᏍᎩ 지정 ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ 기능으로 `jkoros-rpi4-system.img`를 microSD에 기록한다.
2. **별도 USB ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏂᎩᏍᎩ**에 `jkoros-user.img`를 기록한다. 이미지가 4 GiB이므로 그보다 큰 장치가 필요하다. 장치의 기존 데이터는 ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ 시 지워진다.
3. microSD와 USB ᎦᏟᏌᏅᎯ ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ, HDMI 화면, USB 키보드·마우스를 Raspberry Pi 4에 연결하고 부팅한다.
4. ᎬᏗᏍᎩ 이름은 `user`, 홈은 `/home/user`, UID는 1000이다. 로컬 콘솔은 자동 로그인하며, `sudo`로 개발 도구·시스템 패키지를 설치할 수 있다. SSH 서버는 ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 제공하지 않는다.

ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ 파일을 받은 경우 먼저 `gzip -dk ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ.img.gz`로 풀어 기록할 수 있다. 배포 파일이 모두 같은 폴더에 있으면 `sha256sum -c SHA256SUMS`로 무결성을 확인한다.

부팅 프로그램은 ᎦᏟᏌᏅᎯ 장치의 ext4 라벨 `JKDATA`를 찾는다. ᎦᏟᏌᏅᎯ 장치가 없으면 오류와 ᎠᏩᏛᏗ_ᏄᏍᏗᏓᏅ 셸을 표시하며 **자동 포맷하지 않는다**. 처음 부팅하면 `/home/user/workspace/인사.java`가 준비된다. `Ctrl+Space`로 한글 입력을 전환한다. 작업마당의 ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ·ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 단추나 명령창에서 `javac`, `java`, `python3`, `gcc`, `jclassc`를 사용한다.

유선 네트워크는 DHCP로 구성한다. Wi-Fi는 `/home/user/.config/jkoros/wifi.conf`에 `wpa_supplicant` 설정을 넣고 ᎠᏍᏆᏂᎪᏙᏗ 권한을 600으로 설정한 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ 재부팅한다. 국가 코드와 SSID·인증 방식은 사용하는 무선망에 맞춰 지정한다. 현재 ᎠᏉᏅᏗᎢ 인터페이스는 `wlan0`이다.

인터넷 ᎫᏓᎳ 후 NTP로 시간을 맞춘다. Pi 4에 별도 RTC가 없을 때는 이전 ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ 시각 또는 ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 시각에서 시작하므로, HTTPS 이용 전 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 시각이 맞는지 확인한다. ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ 창을 닫아도 ᏦᎳᏂ 관리자는 계속 실행된다.

정상 종료는 `sudo poweroff`다. 부팅 파티션의 `cmdline.txt`에 `jkoros.desktop=off`를 추가하면 그래픽 환경을 시작하지 않는다. 직렬 콘솔은 GPIO UART이며 Bluetooth 대신 PL011을 사용하도록 설정했다.

## 현재 PC의 QEMU에서 그래픽 ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ

이미 ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 중인 QEMU가 있다면 게스트에서 `sudo poweroff`로 종료한다. 같은 ᎦᏟᏌᏅᎯ 이미지를 두 QEMU에서 동시에 열지 않는다. ᎠᏁᏢᏍᎩ 터미널에서 다음을 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4
make run
```

다른 **ᎠᏁᏢᏍᎩ 터미널**에서 화면에 연결한다. 현재 PC에 Remmina가 설치되어 있다.

```sh
remmina -c /home/user/jkoros/platforms/rpi4/build/qemu-5901.remmina
```

처음에는 화면이 검을 수 있다. x86 PC에서 ARM64를 소프트웨어로 에뮬레이션하므로 Java와 다국어 ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ 초기화에 몇 분이 걸릴 수 있다. 부팅과 Java ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ 초기화가 끝나면 데스크톱과 터미널이 표시된다. **VNC 화면 안의 터미널**에서 실행한다.

```sh
cd ~/workspace
javac 인사.java
java 인사
```

`make run`은 기존 `build/manual-user.img`를 사용하고, 없을 때만 새 2 GiB ᎦᏟᏌᏅᎯ 이미지를 만든다. 다른 ᎦᏟᏌᏅᎯ 이미지는 `python3 tools/run_qemu.py --data /ᎠᏍᏓᏩᏛᏍᏗ/ᎦᏟᏌᏅᎯ.img`로 지정한다. VNC는 호스트의 `127.0.0.1:5901`에서만 수신한다. 포트가 사용 중이면 `--vnc-port 5902`로 변경하고 생성된 `build/qemu-5902.remmina`에 연결한다. 정상 종료는 게스트에서 `sudo poweroff`다. Remmina 창을 닫아도 QEMU는 계속 실행된다.

기존 `-display none`과 `jkoros.desktop=off` 조합은 그래픽 장치와 X 서버가 없는 터미널 전용 실행이다. 이 상태에서 `JFrame`을 만들면 `HeadlessException`이 발생한다. `DISPLAY=:0`만 지정하거나 `-Djava.awt.headless=false`만 추가해도 X 서버가 생기지는 않는다.

새 실행기는 가상 그래픽 카드·USB 키보드·마우스를 연결하고 QEMU 전용 initramfs에서 드라이버를 미리 로딩한다. 기존 시스템 이미지와 `base-id`를 그대로 사용하므로 **이번 수정 적용에 `make image`나 ᎦᏟᏌᏅᎯ ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ 재생성은 필요하지 않다**. ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 직렬 터미널로만 사용하려면 `make run-console`을 사용한다.

그래픽으로 부팅한 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ **직렬 콘솔에서** Swing 창을 VNC 화면으로 열고 싶다면 다음처럼 ᎫᏓᎸᎢ_e05f319b 정보도 지정한다.

```sh
export DISPLAY=:0
export XAUTHORITY=/run/user/1000/Xauthority
cd ~/workspace
java 인사
```

이 설정은 `make run`으로 X 서버가 실행된 상태에서만 유효하다. ᎦᏟᏌᏅᎯ_0201f362 예제 `한국어자바/예제/인사.java`에는 화면이 없으면 터미널 결과만 출력하는 분기도 추가했다. 이미 ᎬᏗᏍᎩ 폴더에 저장된 예제는 자동으로 덮어쓰지 않는다.

`make test-desktop`은 별도 ᎦᏟᏌᏅᎯ 이미지에서 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ Xorg/VNC 화면과 USB 키보드·마우스 입력을 Swing으로 검사한다. ᎠᏁᏢᏍᎩ Python의 Pillow가 필요하며 결과와 화면 캡처는 `build/verification/desktop*`에 저장된다. 기존 `make test`의 Swing 시험은 Xvfb를 사용하는 별도 자동 시험이다.

### 한글 입력과 ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ

ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 중인 게스트에서 `sudo poweroff`한 다음, 호스트에서 다시 `make run`하고 위 Remmina 파일로 연결하면 입력기·ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ 수정이 적용된다. 기존 `build/manual-user.img`와 시스템 이미지를 그대로 사용한다. `make image`나 ᎦᏟᏌᏅᎯ ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ 초기화는 필요하지 않다.

VNC 화면 안의 터미널이나 Java 편집기를 클릭하고 **Ctrl+Space**로 한·영을 전환한다. **한/영 ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ**도 등록되어 있다. ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 한글 배열은 두벌식이다. `gksrmf` 키를 누르면 `한글`이 입력된다. ᎠᏁᏢᏍᎩ 입력기는 영문 상태로 두고 게스트의 입력기로 조합한다. 호스트가 Ctrl+Space를 먼저 처리한다면 VNC 클라이언트의 키보드 잡기 기능을 사용한다.

문자 로케일은 `ko_KR.UTF-8`, 입력기는 Fcitx5의 Hangul/XIM이다. 입력기 응답을 확인한 후 터미널과 Java를 실행한다. 터미널은 영문에 DejaVu Sans Mono, 한글에 Noto Sans Mono CJK KR을 사용하며, Java 작업마당은 16 크기의 본문 글꼴과 안티앨리어싱을 사용한다. 새 X 터미널은 `jkoros-terminal`로 ᎨᏛᎢ_ᏧᎬᏩᎶᏗᏯ 수 있다. 터미널 ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ 크기는 `jkoros-terminal -fs 14`처럼 지정할 수 있다. 색상 등 개인 X 리소스 설정은 `~/.Xresources`에서 읽는다.

QEMU 실행기가 전달하는 수정 파일은 ᎬᏗᏍᎩ 자료의 시스템 변경분에 저장된다. 교체 전 시스템 파일은 `~/.jkoros/desktop-updates/`, 기존 Fcitx 설정과 Java ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ 캐시는 `~/.local/state/jkoros/desktop-settings/`에 보관한다. 작업 중인 문서와 설치한 프로그램은 유지한다. 같은 수정 버전은 재부팅 때 반복 적용하지 않아 이후의 개인 설정을 보존한다. 향후 `make image`로 새 이미지를 빌드할 때도 같은 ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 설정이 포함된다.

`make test-korean`은 별도 시험 ᎦᏟᏌᏅᎯ 이미지에서 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ VNC ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ 입력으로 Swing과 xterm에 `한글 입력`을 조합하고, UTF-8 ᎠᏍᏆᏂᎪᏙᏗ Store_ᏧᎬᏩᎶᏗᏯ 결과를 확인한다. 결과와 화면 캡처는 `build/verification/korean*`에 저장한다.

ᏕᎦᎧᎲᎢ 근거: [Fcitx의 XIM·로케일 ᏍᎩᎪᎵᏯ_eb81d7d9](https://fcitx-im.org/wiki/Input_method_related_environment_variables/en), [xterm의 ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ·입력기 옵션](https://invisible-island.net/xterm/manpage/xterm.html).

## 시스템과 ᎬᏗᏍᎩ 환경 분리

```text
microSD: firmware + kernel + initramfs + immutable system
USB(ext4, JKDATA): /user  → ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 중 /home/user
  ├── workspace, .config, .local, .venvs, ᎬᏗᏍᎩ ᎠᏍᏆᏂᎪᏙᏗ
  └── .jkoros/system/
        ├── base-id      같은 시스템 이미지인지 ᎰᎯᏳᏓ
        ├── upper/       /usr, /opt, /etc, 패키지 DB 등 모든 시스템 변경분
        └── work/        OverlayFS 작업 영역
```

시스템 ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 파일은 읽기 전용이다. `sudo apk add ᎬᏙᏗ_f5044b9b`으로 설치한 ᎠᏍᏆᏂᎪᏙᏗ, 패키지 데이터베이스, `/etc` ᏕᎦᎧᎲᎢ, 기존 파일의 삭제 정보도 ᎬᏗᏍᎩ 폴더의 OverlayFS 변경분에 들어간다. 따라서 일반 ᎬᏗᏍᎩ 파일과 ᎬᏗᏍᎩ ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ 프로그램을 함께 옮길 수 있다. `/run`, `/tmp`, `/dev/shm`은 일시 자료다.

**ᎯᎲᎾ_ᏧᎬᏩᎶᏗᏯ ᎤᏍᏗᏓᏅ:** 양쪽의 시스템 ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ `base-id`, ARM64 아키텍처, ᎬᏗᏍᎩ ᎠᏍᏓᏩᏛᏍᏗ `/home/user`, UID 1000이 같아야 한다. 부팅 시 ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ 식별자를 검사하며 다르면 해당 변경분을 임의로 적용하지 않는다. 이 버전은 서로 다른 시스템 버전 사이의 자동 마이그레이션을 제공하지 않는다.

두 운영체제를 정상 종료하고 다른 Linux에서 ᎦᏟᏌᏅᎯ 장치를 마운트한 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ, 새 ᎦᏟᏌᏅᎯ 장치에 `user` 폴더가 없는 상태에서 다음처럼 복사한다.

```sh
sudo cp -a /media/OLD/user /media/NEW/
sync
```

ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 중에는 이 폴더가 `/home/user`로 보인다. 반드시 ᎬᏍᎦᏝ_ᏧᎬᏩᎶᏗᏯ ᎠᏍᏆᏂᎪᏙᏗ, 심볼릭 링크, 소유권, 권한, ᎪᏯᏅᎯᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ ᏄᏍᏛ_ᎠᎦᏅᏛᎢ_ᏧᎬᏩᎶᏗᏯ, OverlayFS 삭제 정보를 보존해야 한다. ext4 사이의 ᎯᎲᎾ_ᏧᎬᏩᎶᏗᏯ 또는 Linux의 `sudo cp -a`/적절한 tar 보관을 사용한다. FAT/exFAT에 일반 폴더로 복사하면 이 정보가 보존되지 않는다. `user`를 기존 환경과 병합하지 않는다.

`jkoros-environment info`는 현재 환경의 식별자를 보여준다. 오프라인 보관은 다른 Linux에서 `sudo python3 runtime/environment export --home /media/OLD/user --output /backup/user.tar`로 수행한다. 복원은 빈 대상에서 `sudo tar --xattrs --acls --numeric-owner -xpf /backup/user.tar -C /media/NEW`다.

이 구조는 환경의 휴대성을 위한 것이다. 호스트와 격리하는 보안 샌드박스는 아니다. 별도 외부 디스크·원격 서비스의 ᎦᏟᏌᏅᎯ, 부팅 펌웨어 변경은 `/home/user` 이동에 포함되지 않는다.

## ᎬᏙᏗ_f5044b9b ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ

한국어 Java 라이브러리는 `/opt/jkoros/lib/한국어자바.jar`에 있다. ᎠᏍᏆᏂᎪᏙᏗ·문자·통신·스레드·Swing 도우미 22개 메서드와 Java 작업마당의 사용법은 [한국어 ᏧᏂᎪᎵᏰᏗᎢ ᎬᏗᏍᎩ_ᎠᏓᏎᎮᎯ](../../한국어자바/ᎬᏗᏍᎩ_ᎠᏓᏎᎮᎯ.md)를 참고한다. Python의 Java 프로세스 호출, C++의 JNI 직접 호출 예제와 추가 설치가 필요한 Python ᎫᏓᎳ 방식도 구분해 설명한다.

```sh
sudo apk update
sudo apk add tree
python3 -m virtualenv ~/.venvs/dev
. ~/.venvs/dev/bin/activate
pip install 패키지이름
```

Python 가상환경, 직접 빌드한 ᎬᏙᏗ_f5044b9b, ᎬᏗᏍᎩ 설정도 `/home/user`에 둔다. 시스템에 설치하는 패키지도 변경분이 같은 폴더에 보관된다.

## 빌드와 시험

Linux x86-64 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 호스트에서 Python 3, curl, JDK 11 이상, GNU C 컴파일러, make, kmod, squashfs-tools, dosfstools, mtools, e2fsprogs가 필요하다. 일반 ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ 빌드는 root 권한이나 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 디스크 접근을 사용하지 않는다.

```sh
make prepare       # 서명된 ARM64 패키지와 Pi 공식 펌웨어 확보
make prepare-host  # 프로젝트 내부에 최신 QEMU·jlink·proot 확보
make runtimes      # ARM64 JRE 구성 및 JDK/JRE 아카이브 생성
make image         # ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ 생성; 기존 ᎬᏗᏍᎩ 이미지는 유지
make test          # ARM64 부팅/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ/재부팅/오프라인 홈 ᎯᎲᎾ_ᏧᎬᏩᎶᏗᏯ 시험
make verify        # Pi ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ 구조와 ARM64 JDK/JRE ᎪᎯᏳᏙᏗ
make release       # ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ ᎪᏢᏍᎩ_ᎤᏓᏴᎳᏛ ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ 및 SHA256SUMS 생성
```

`proot`는 ptrace가 허용된 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 환경에서 실행한다. 패키지 검증을 끄는 옵션은 사용하지 않는다. 버전 고정 저장소의 패키지 갱신에 따라 다음 ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 결과는 달라질 수 있으며, 배포 이미지의 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 버전과 해시는 잠금 파일에 기록한다.

시험 결과는 `build/verification/`에 있다. QEMU `virt` 시험은 같은 ARM64 ᎬᏗᏍᎩ 환경·초기 부팅 코드·Store_ᏧᎬᏩᎶᏗᏯ 구조를 검증하지만, ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ Pi 4의 HDMI·USB·Wi-Fi·SD 드라이버 동작을 대신 검증하지 않는다. 이 저장소에 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ Pi 4 보드를 연결한 부팅 결과는 아직 없다.

배포 결과와 ᎪᎯᏳᏙᏗ 범위는 [VERIFICATION.md](VERIFICATION.md)를 참조한다. 컴파일러의 OpenJDK ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ ᎠᏍᏆᏂᎪᏙᏗ 방식과 제약은 [컴파일러 ᏍᎩᎪᎵᏯ_eb81d7d9](../../compiler/OpenJDK-실행파일.md)에 설명되어 있다.
