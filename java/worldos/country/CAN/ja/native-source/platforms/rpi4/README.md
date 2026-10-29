# jkoros Raspberry Pi 4 실행판

Raspberry Pi 4의 ARM64 Linux 실행판이다. 기존 `../../os`의 内蔵 x86 Java 커널과 별도 起動 경로다. Linux가 CPU·装置·記憶データ·스레드·ファイル·네트워크를 제공하고, 전체 OpenJDK와 日本語 Java 작업마당이 그 위에서 실행된다.

Linux 없이 부팅하는 **内蔵 Java ARM64 커널의 初期状況 이식판**은 [rpi4-native](../rpi4-native/README.md)에 있다. 그 이식판에는 이 문서의 OpenJDK·Python·Swing 기능이 아직 구현되지 않았다.

## 제공 ファイル

`dist/`에 実際データ 바이너리를 생성한다.

| ファイル | 용도 |
|---|---|
| `jkoros-rpi4-system.img` | microSD에 기록할 FAT 起動 파티션 + 読取 전용 SquashFS 시스템 |
| `jkoros-user.img` | 별도 USB 저장장치에 기록할 ext4 利用者 データ イメージ構築, 4 GiB |
| `*.img.gz`, `SHA256SUMS` | 전달용 書庫値 이미지와 SHA256 妥当性検査 入口一覧 |
| `openjdk25-jdk-linux-aarch64-musl.tar.gz` | 컴파일된 ARM64 JDK |
| `openjdk25-jre-linux-aarch64-musl.tar.gz` | jlink로 구성한 컴파일된 ARM64 JRE |
| `日本語Java.jar` | 日本語 이름으로 ファイル·文字·通信·作業·화면을 사용하는 Java ライブラリ |
| `manifest.json`, `java-runtimes.json` | イメージ構築/런타임 SHA256, 아키텍처와 구성 |
| `packages.lock.json`, `sources.lock.json` | 実際データ 설치된 패키지 버전·原点値·라이선스 システム情報 |

JDK/JRE는 이 실행판과 같은 **Linux ARM64 + musl** 환경용이다. 다른 libc/CPU/운영체제에서 단독 실행을 보장하지 않는다. 네이티브 의존 라이브러리는 稼働システム 이미지에 함께 들어 있다. JRE는 Java SE와 문자셋·다국어·合言葉値·ZIP ファイルシステム 등 選択状態値 모듈을 포함하고, 전체 開発 도구는 JDK에 있다.

## 설치와 命令実行

1. Raspberry Pi Imager의 利用者 代入値 イメージ構築 기능으로 `jkoros-rpi4-system.img`를 microSD에 기록한다.
2. **별도 USB 記憶装置装置**에 `jkoros-user.img`를 기록한다. 이미지가 4 GiB이므로 그보다 큰 장치가 필요하다. 장치의 기존 데이터는 イメージ構築 履歴記録記録 시 지워진다.
3. microSD와 USB データ 装置, HDMI 画面, USB 키보드·마우스를 Raspberry Pi 4에 연결하고 부팅한다.
4. 利用者 이름은 `user`, 홈은 `/home/user`, UID는 1000이다. 로컬 콘솔은 자동 로그인하며, `sudo`로 開発 道具·시스템 패키지를 설치할 数 있다. SSH 서버는 既定値 제공하지 않는다.

書庫値 파일을 받은 경우 먼저 `gzip -dk ファイル入口名前.img.gz`로 풀어 기록할 数 있다. 配布値 파일이 全体構築 같은 폴더에 있으면 `sha256sum -c SHA256SUMS`로 무결성을 확인한다.

起動 프로그램은 データ 장치의 ext4 라벨 `JKDATA`를 찾는다. データ 장치가 없으면 오류와 状況復旧 셸을 표시하며 **자동 포맷하지 않는다**. 初期項目 부팅하면 `/home/user/workspace/挨拶例.java`先頭位置被演算子 준비된다. `Ctrl+Space`로 ハングル文字列 입력을 전환한다. 작업마당의 ソースコンパイル·命令実行 단추나 명령창에서 `javac`, `java`, `python3`, `gcc`, `jclassc`를 사용한다.

結線済み値 네트워크는 DHCP로 구성한다. Wi-Fi는 `/home/user/.config/jkoros/wifi.conf`에 `wpa_supplicant` 설정을 넣고 ファイル 권한을 600으로 설정한 後端値 재부팅한다. 국가 코드와 SSID·인증 방식은 사용하는 무선망에 맞춰 지정한다. 現在項目 対象値 인터페이스는 `wlan0`이다.

인터넷 接続 後続側状況 NTP로 시간을 맞춘다. Pi 4에 별도 RTC가 없을 때는 前回項目 終了点プログラム 時刻印値 또는 イメージ構築 システム構築 시각에서 시작하므로, HTTPS 이용 直前側値 実際データ 시각이 맞는지 확인한다. 編集値 창을 닫아도 窓 관리자는 継続処理工程 실행된다.

判定通常 종료는 `sudo poweroff`第三被演算子. 起動 파티션의 `cmdline.txt`에 `jkoros.desktop=off`를 추가하면 그래픽 환경을 시작하지 않는다. 直列値 콘솔은 GPIO UART이며 Bluetooth 대신 PL011을 사용하도록 설정했다.

## 現在項目 PC의 QEMU에서 그래픽 命令実行

이미 命令実行 중인 QEMU가 있다면 게스트에서 `sudo poweroff`로 종료한다. 같은 データ 이미지를 두 QEMU에서 동시에 열지 않는다. ホスト 터미널에서 다음을 실행한다.

```sh
cd /home/user/jkoros/platforms/rpi4
make run
```

다른 **ホスト 端末**에서 화면에 연결한다. 現在項目 PC에 Remmina가 설치되어 있다.

```sh
remmina -c /home/user/jkoros/platforms/rpi4/build/qemu-5901.remmina
```

처음에는 화면이 검을 数 있다. x86 PC에서 ARM64를 소프트웨어로 에뮬레이션하므로 Java와 다국어 書体値 초기화에 몇 분이 걸릴 数 있다. 부팅과 Java 作業場 초기화가 끝나면 데스크톱과 터미널이 표시된다. **VNC 画面 안의 端末**에서 실행한다.

```sh
cd ~/workspace
javac 挨拶例.java
java 挨拶例
```

`make run`은 기존 `build/manual-user.img`를 사용하고, 없을 때만 새 2 GiB データ 이미지를 만든다. 다른 データ 이미지는 `python3 tools/run_qemu.py --data /経路/データ.img`로 지정한다. VNC는 호스트의 `127.0.0.1:5901`에서만 수신한다. 포트가 使用値 중이면 `--vnc-port 5902`로 변경하고 생성된 `build/qemu-5902.remmina`에 연결한다. 判定通常 종료는 게스트에서 `sudo poweroff`第三被演算子. Remmina 창을 닫아도 QEMU는 継続処理工程 실행된다.

기존 `-display none`과 `jkoros.desktop=off` 조합은 그래픽 장치와 X 서버가 없는 端末 전용 실행이다. 이 상태에서 `JFrame`을 만들면 `HeadlessException`이 발생한다. `DISPLAY=:0`만 지정하거나 `-Djava.awt.headless=false`만 추가해도 X 서버가 생기지는 않는다.

새 실행기는 가상 그래픽 카드·USB 키보드·마우스를 연결하고 QEMU 전용 initramfs에서 드라이버를 미리 로딩한다. 기존 시스템 이미지와 `base-id`를 그대로 사용하므로 **이번 値改変 적용에 `make image`第二被演算子 データ イメージ構築 재생성은 필요하지 않다**. 既定値 直列値 터미널로만 사용하려면 `make run-console`을 사용한다.

그래픽으로 부팅한 後端値 **直列値 콘솔에서** Swing 창을 VNC 화면으로 열고 싶다면 다음처럼 接続状態 정보도 지정한다.

```sh
export DISPLAY=:0
export XAUTHORITY=/run/user/1000/Xauthority
cd ~/workspace
java 挨拶例
```

이 설정은 `make run`으로 X 서버가 실행된 상태에서만 유효하다. ソース 用例 `日本語Java/用例/挨拶例.java`에는 화면이 없으면 端末 결과만 출력하는 분기도 추가했다. 이미 利用者 폴더에 저장된 예제는 자동으로 덮어쓰지 않는다.

`make test-desktop`은 별도 データ 이미지에서 実際データ Xorg/VNC 화면과 USB 키보드·마우스 입력을 Swing으로 검사한다. ホスト Python의 Pillow가 필요하며 결과와 画面 캡처는 `build/verification/desktop*`에 저장된다. 기존 `make test`의 Swing 시험은 Xvfb를 사용하는 별도 자동 시험이다.

### ハングル文字列 입력과 書体値

命令実行 중인 게스트에서 `sudo poweroff`한 次回項目, 호스트에서 再試行処理値 `make run`하고 上端値 Remmina 파일로 연결하면 입력기·書体値 수정이 적용된다. 기존 `build/manual-user.img`와 시스템 이미지를 그대로 사용한다. `make image`第二被演算子 データ イメージ構築 초기화는 필요하지 않다.

VNC 画面 안의 터미널이나 Java 편집기를 클릭하고 **Ctrl+Space**로 한·영을 전환한다. **한/零被演算子 キー値**도 등록되어 있다. 既定値 ハングル文字列 배열은 두벌식이다. `gksrmf` 키를 누르면 `ハングル文字列`이 입력된다. ホスト 입력기는 영문 상태로 두고 게스트의 입력기로 조합한다. 호스트가 Ctrl+Space를 먼저 처리한다면 VNC 클라이언트의 키보드 잡기 기능을 사용한다.

文字 로케일은 `ko_KR.UTF-8`, 입력기는 Fcitx5의 Hangul/XIM이다. 입력기 응답을 확인한 後続側状況 터미널과 Java를 실행한다. 터미널은 영문에 DejaVu Sans Mono, 한글에 Noto Sans Mono CJK KR을 사용하며, Java 작업마당은 16 크기의 本体本文 글꼴과 안티앨리어싱을 사용한다. 새 X 터미널은 `jkoros-terminal`로 列値 数 있다. 端末 書体値 크기는 `jkoros-terminal -fs 14`처럼 지정할 数 있다. 画素色 등 개인 X 리소스 설정은 `~/.Xresources`에서 읽는다.

QEMU 실행기가 전달하는 値改変 파일은 利用者 자료의 시스템 변경분에 저장된다. 교체 直前側値 시스템 파일은 `~/.jkoros/desktop-updates/`, 기존 Fcitx 설정과 Java 書体値 캐시는 `~/.local/state/jkoros/desktop-settings/`에 보관한다. 作業 중인 문서와 설치한 프로그램은 유지한다. 같은 値改変 버전은 재부팅 때 反復回値 적용하지 않아 이후의 개인 설정을 보존한다. 향후 `make image`로 새 이미지를 빌드할 때도 같은 既定値 설정이 포함된다.

`make test-korean`은 별도 試験 データ 이미지에서 実際データ VNC キー値 입력으로 Swing과 xterm에 `ハングル文字列 入力値`을 조합하고, UTF-8 ファイル 格納値 결과를 확인한다. 결과와 画面 캡처는 `build/verification/korean*`에 저장한다.

設定値 근거: [Fcitx의 XIM·로케일 案内](https://fcitx-im.org/wiki/Input_method_related_environment_variables/en), [xterm의 書体値·입력기 옵션](https://invisible-island.net/xterm/manpage/xterm.html).

## 시스템과 利用者 環境 분리

```text
microSD: firmware + kernel + initramfs + immutable system
USB(ext4, JKDATA): /user  → 命令実行 중 /home/user
  ├── workspace, .config, .local, .venvs, 利用者 ファイル
  └── .jkoros/system/
        ├── base-id      같은 시스템 이미지인지 検証
        ├── upper/       /usr, /opt, /etc, 패키지 DB 등 모든 시스템 변경분
        └── work/        OverlayFS 作業 領域値
```

시스템 既定値 파일은 読取 전용이다. `sudo apk add プログラム`으로 설치한 ファイル, 패키지 데이터베이스, `/etc` 設定値, 기존 파일의 삭제 정보도 利用者 폴더의 OverlayFS 변경분에 들어간다. 따라서 일반 利用者 파일과 利用者 値導入 프로그램을 함께 옮길 数 있다. `/run`, `/tmp`, `/dev/shm`은 일시 자료다.

**移動値 条件:** 양쪽의 시스템 イメージ構築 `base-id`, ARM64 아키텍처, 利用者 経路 `/home/user`, UID 1000이 같아야 한다. 起動 시 イメージ構築 식별자를 검사하며 다르면 해당 변경분을 임의로 적용하지 않는다. 이 버전은 서로 다른 시스템 버전 사이의 자동 마이그레이션을 제공하지 않는다.

두 운영체제를 判定通常 종료하고 다른 Linux에서 データ 장치를 마운트한 後端値, 새 データ 장치에 `user` 폴더가 없는 상태에서 다음처럼 복사한다.

```sh
sudo cp -a /media/OLD/user /media/NEW/
sync
```

命令実行 중에는 이 폴더가 `/home/user`로 보인다. 반드시 隠蔽値 ファイル, 심볼릭 링크, 소유권, 許可値, 拡張子値 属性値, OverlayFS 삭제 정보를 보존해야 한다. ext4 사이의 移動値 또는 Linux의 `sudo cp -a`/적절한 tar 보관을 사용한다. FAT/exFAT에 일반 폴더로 복사하면 이 정보가 보존되지 않는다. `user`를 기존 환경과 병합하지 않는다.

`jkoros-environment info`는 現在項目 환경의 식별자를 보여준다. 判定非接続 보관은 다른 Linux에서 `sudo python3 runtime/environment export --home /media/OLD/user --output /backup/user.tar`로 수행한다. 복원은 빈 대상에서 `sudo tar --xattrs --acls --numeric-owner -xpf /backup/user.tar -C /media/NEW`第三被演算子.

이 구조는 환경의 휴대성을 위한 것이다. 호스트와 격리하는 보안 샌드박스는 아니다. 별도 外部値 디스크·遠隔値 서비스의 データ, 起動 펌웨어 변경은 `/home/user` 이동에 포함되지 않는다.

## プログラム 値導入

日本語 Java 라이브러리는 `/opt/jkoros/lib/日本語Java.jar`에 있다. ファイル·文字·通信·스레드·Swing 補助器値 22개 메서드와 Java 작업마당의 사용법은 [日本語 ライブラリ 利用者手引](../../日本語Java/利用者手引.md)를 참고한다. Python의 Java 프로세스 呼出, C++의 JNI 직접 呼出 예제와 入口追記 설치가 필요한 Python 接続 방식도 구분해 설명한다.

```sh
sudo apk update
sudo apk add tree
python3 -m virtualenv ~/.venvs/dev
. ~/.venvs/dev/bin/activate
pip install 패키지이름
```

Python 가상환경, 직접 빌드한 プログラム, 利用者 설정도 `/home/user`에 둔다. 시스템에 설치하는 패키지도 변경분이 같은 폴더에 보관된다.

## 빌드와 試験

Linux x86-64 システム構築 호스트에서 Python 3, curl, JDK 11 이상, GNU C コンパイラ, make, kmod, squashfs-tools, dosfstools, mtools, e2fsprogs가 필요하다. 일반 イメージ構築 빌드는 root 권한이나 実際データ 디스크 접근을 사용하지 않는다.

```sh
make prepare       # 서명된 ARM64 패키지와 Pi 공식 펌웨어 확보
make prepare-host  # 프로젝트 내부에 最新値 QEMU·jlink·proot 확보
make runtimes      # ARM64 JRE 구성 및 JDK/JRE 아카이브 生成
make image         # 稼働システム イメージ構築 生成; 기존 利用者 이미지는 値維持
make test          # ARM64 起動/命令実行/재부팅/判定非接続 홈 移動値 試験
make verify        # Pi イメージ構築 구조와 ARM64 JDK/JRE 妥当性検査
make release       # 値導入 イメージ構築 書庫値 및 SHA256SUMS 生成
```

`proot`는 ptrace가 허용된 システム構築 환경에서 실행한다. 패키지 검증을 끄는 옵션은 사용하지 않는다. 버전 고정 저장소의 패키지 갱신에 따라 次回項目 システム構築 결과는 달라질 数 있으며, 配布値 이미지의 実際データ 버전과 해시는 錠値 파일에 기록한다.

試験 결과는 `build/verification/`에 있다. QEMU `virt` 시험은 같은 ARM64 利用者 環境·初期状況 起動 コード値·格納値 구조를 검증하지만, 実際データ Pi 4의 HDMI·USB·Wi-Fi·SD 드라이버 동작을 대신 검증하지 않는다. 이 저장소에 実際データ Pi 4 보드를 연결한 起動 결과는 아직 없다.

配布値 결과와 妥当性検査 범위는 [VERIFICATION.md](VERIFICATION.md)를 참조한다. 컴파일러의 OpenJDK 命令実行 ファイル 방식과 제약은 [コンパイラ 案内](../../compiler/OpenJDK-実行形式ファイル.md)에 설명되어 있다.
