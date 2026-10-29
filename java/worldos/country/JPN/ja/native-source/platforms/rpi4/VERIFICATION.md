# 配布値 イメージ構築 妥当性検査 履歴記録記録

검증일: 2026-09-27 (Asia/Seoul)

対象値: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 内蔵 x86 커널을 ARM으로 이식한 결과가 아니다. 実際データ Pi 보드는 연결되어 있지 않아 機器値 起動 성공을 확인하지 못했다.

## 배포물

| ファイル | 容量(バイト値) | 説明 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | 書庫値 시스템 イメージ構築; 記憶装置解放 後続側状況 1,475,747,840 バイト値 |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 利用者 データ イメージ構築; 記憶装置解放 後続側状況 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/日本語Java.jar` | 10,563 | 日本語 補助値 API와 Java 作業場 |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 書庫値 イメージ構築 全体構築 끝까지 해제하여 原本 이미지의 SHA256과 일치함을 확인했다. [書庫値 妥当性検査 履歴記録記録](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU 妥当性検査 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 入口一覧](dist/packages.lock.json)과 [原本 原点値](dist/sources.lock.json)를 제공한다.

## 통과한 検査項目

| 検査項目 | 実際データ 検証 内容物値 | 履歴記録記録 |
|---|---|---|
| ホスト コンパイラ 試験 19개 | 기존 AOT 회귀 試験, `.class` 직접 入力値, OpenJDK ELF プログラム実行器, JAR 依存項目, 상속·리플렉션·람다·스레드·리소스, 経路 移動値, 失敗値 시 기존 出力 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi イメージ構築 構造 | MBR 境界位置値, FAT 起動 파티션, Pi 펌웨어, ARM64 中核値, Pi 4 DTB, initramfs, SquashFS 및 ハッシュファイル | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 検査項目, 起動 後続側状況 두 런타임의 実際データ 命令実行 | [런타임 履歴記録記録](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 先頭位置項目 起動 | 読取 전용 시스템, Java ファイル·Unicode値·例外·オブジェクト値·스레드·HTTP/TCP·子値 프로세스, Swing, CJK·아랍어·데바나가리 書体値, Python ファイル·스레드·ソケット値·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 命令実行 ファイル 生成 | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 命令実行 成功値 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | 利用者 データ, `/etc` 設定値, `/usr/local/bin` プログラム, APK로 설치한 tree, pip 패키지, ファイル 삭제 システム情報, 소유권, sudo, Java 命令実行 ファイル 値維持 | [restore.log](build/verification/restore.log) |
| 判定非接続 홈 移動値 | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 値複写 | [migrate.log](build/verification/migrate.log) |
| 移動値 後続側状況 起動 | 새 データ 이미지로 부팅하여 재부팅 복원 항목을 再試行処理値 検証 | [migrated-restore.log](build/verification/migrated-restore.log) |
| 判定通常 終了点プログラム 및 データ 무결성 | 일반 起動 3회 全体構築 OverlayFS/データ 装置 読取 전용 切替方式 成功値; 原本·複写済み値 ext4의 `e2fsck -fn` 終了点プログラム コード値 0 | [原本 検査項目](build/verification/fsck-original.log), [複写済み値 検査項目](build/verification/fsck-migrated.log) |

네 列順値 부팅은 全体構築 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 終了点プログラム コード値 0으로 통과했다. [전체 起動 결과와 履歴記録値 ハッシュファイル](build/verification/boot.json)

QEMU 가상 NIC의 DHCP 番地 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 外部値 인터넷이나 Pi Wi-Fi의 妥当性検査 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [画面 캡처](build/verification/swing.png)에서 ハングル文字列·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## 実装 범위와 남은 妥当性検査

### QEMU 그래픽 命令実行 보완

端末 전용 실행에서 `挨拶例.java`先頭位置被演算子 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. 配布値 시스템 이미지와 base-id는 변경하지 않아 기존 利用者 データ 이미지를 継続処理工程 사용할 数 있다.

実際データ Xorg/VNC 화면에서 日本語 Java 作業場, Swing 試験 窓, 기존 이미지의 `挨拶例.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. 終了点プログラム 시 시스템 OverlayFS와 データ 파일시스템의 読取 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 試験 結果](build/verification/desktop.json)
- [그래픽 試験 履歴記録値](build/verification/desktop.log)
- [키보드·마우스 試験 画面](build/verification/desktop-input.png)
- [挨拶例 用例 画面](build/verification/desktop-greeting.png)
- [수정한 用例 원문의 画面 없는 命令実行 結果](build/verification/headless-example.log)

ソース 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 ファイル·文字·스레드 기능을 실행하고 안내를 출력한다. 利用者 홈의 기존 원문을 자동 교체하지는 않는다. 향후 イメージ構築 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### ハングル文字列 入力値·書体値 보완

`make test-korean`으로 実際データ Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space 切替方式 및 두벌식 キー値 입력을 시험했다. 양쪽에서 `ハングル文字列 入力値`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 利用者 データ 이미지에서 실행했으며 判定通常 終了点プログラム 시 두 파일시스템의 読取 전용 전환을 확인했다.

端末 書体値 진단에서 영문 DejaVu Sans Mono와 ハングル文字列 Noto Sans Mono CJK KR의 実際データ ファイル 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 画面 캡처에서 ハングル文字列·영문 値表示, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 利用者 시스템 변경분에 적용하며 配布値 既定値 이미지와 base-id는 유지한다. 기존 ファイル 백업, 동일 수정의 反復回値 적용 방지, 손상된 値改変 ファイル 및 다른 base-id 値却下, 利用者 입력기 設定値 병합에 대한 ホスト 試験 4개도 통과했다. 원래 利用者 データ イメージ構築 `build/manual-user.img`는 시험에 사용하지 않았다.

- [ハングル文字列 入力値·書体値 試験 結果](build/verification/korean.json)
- [入力値·実際データ 書体値 로딩 履歴記録値](build/verification/korean.log)
- [Swing·端末 ハングル文字列 画面](build/verification/korean-desktop.png)
- [Java 作業場 書体値 画面](build/verification/korean-workbench.png)
- [設定値 보존 試験](build/verification/desktop-update-tests.log)

### 남은 切抜き

- 새 ソースコンパイル 対象値 `openjdk`는 **네이티브 プログラム実行器 + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 支援値 범위는 여전히 제한적이다.
- 命令実行 프로그램에는 main 入口点, 호환 クラス値 버전과 의존 JAR/JNI가 필요하다. 개별 상용 プログラム, 모든 Java モジュール値, 모든 문자권을 시험한 것은 아니다.
- 日本語 Java 라이브러리는 ファイル·文字·通信·스레드·Swing을 위한 補助値 API이며 JDK 전체 API의 日本語 번역판은 아니다.
- Pi 4 전용 펌웨어·中核値·装置 트리는 이미지에 들어 있지만 実際データ SD 起動, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 ハングル文字列 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- 利用者 ディレクトリ値 이동은 동일 시스템 イメージ構築 識別子値, ARM64, `/home/user`, UID 1000을 전제로 한다. 終了点プログラム 後続側状況 소유권·許可値·링크·拡張子値 属性値·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

値導入·値複写 절차는 [README.md](README.md), ソースコンパイル 방식은 [OpenJDK 命令実行 ファイル 案内](../../compiler/OpenJDK-実行形式ファイル.md)를 따른다. イメージ構築 파일만 생성했으며 実際データ SD 카드나 USB 디스크에 기록하지 않았다.
