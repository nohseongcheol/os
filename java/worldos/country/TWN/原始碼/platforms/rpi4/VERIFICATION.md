# 分發值 構建映像 有效性校驗 日誌記錄

검증일: 2026-09-27 (Asia/Seoul)

目標值: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 內建 x86 커널을 ARM으로 이식한 결과가 아니다. 實際資料 Pi 보드는 연결되어 있지 않아 硬件值 啓動 성공을 확인하지 못했다.

## 배포물

| 檔案 | 大小(位元組值) | 說明 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | 存檔值 시스템 構建映像; 釋放存儲裝置 之後狀態 1,475,747,840 位元組值 |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 使用者 資料 構建映像; 釋放存儲裝置 之後狀態 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/中文Java.jar` | 10,563 | 中文 輔助值 API와 Java 工作區 |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 存檔值 構建映像 構建全部 끝까지 해제하여 原始 이미지의 SHA256과 일치함을 확인했다. [存檔值 有效性校驗 日誌記錄](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU 有效性校驗 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 條目列表](dist/packages.lock.json)과 [原始 原點值](dist/sources.lock.json)를 제공한다.

## 통과한 檢查項

| 檢查項 | 實際資料 驗證 內容值 | 日誌記錄 |
|---|---|---|
| 宿主 編譯器 測試 19개 | 기존 AOT 회귀 測試, `.class` 직접 輸入值, OpenJDK ELF 運行器, JAR 依賴項列, 상속·리플렉션·람다·스레드·리소스, 路徑 移動值, 失敗值 시 기존 輸出 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi 構建映像 結構 | MBR 邊界位置值, FAT 啓動 파티션, Pi 펌웨어, ARM64 內核值, Pi 4 DTB, initramfs, SquashFS 및 哈希檔案 | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 檢查項, 啓動 之後狀態 두 런타임의 實際資料 執行命令 | [런타임 日誌記錄](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 首位項目 啓動 | 讀取 전용 시스템, Java 檔案·Unicode值·異常·物件值·스레드·HTTP/TCP·子值 프로세스, Swing, CJK·아랍어·데바나가리 字體值, Python 檔案·스레드·通訊端值·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 執行命令 檔案 生成 | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 執行命令 成功值 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | 使用者 資料, `/etc` 設置, `/usr/local/bin` 程式, APK로 설치한 tree, pip 패키지, 檔案 삭제 系統信息, 소유권, sudo, Java 執行命令 檔案 保持值 | [restore.log](build/verification/restore.log) |
| 是否離線 홈 移動值 | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 複製值 | [migrate.log](build/verification/migrate.log) |
| 移動值 之後狀態 啓動 | 새 資料 이미지로 부팅하여 재부팅 복원 항목을 重試值 驗證 | [migrated-restore.log](build/verification/migrated-restore.log) |
| 是否常規 退出程式 및 資料 무결성 | 일반 啓動 3회 構建全部 OverlayFS/資料 設備 讀取 전용 切換模式 成功值; 原始·已複製值 ext4의 `e2fsck -fn` 退出程式 程式碼值 0 | [原始 檢查項](build/verification/fsck-original.log), [已複製值 檢查項](build/verification/fsck-migrated.log) |

네 序列值 부팅은 構建全部 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 退出程式 程式碼值 0으로 통과했다. [전체 啓動 결과와 日誌值 哈希檔案](build/verification/boot.json)

QEMU 가상 NIC의 DHCP 地址 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 外部值 인터넷이나 Pi Wi-Fi의 有效性校驗 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [屏幕 캡처](build/verification/swing.png)에서 韓文文本·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## 實現 범위와 남은 有效性校驗

### QEMU 그래픽 執行命令 보완

終端 전용 실행에서 `問候例.java`首位操作數 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. 分發值 시스템 이미지와 base-id는 변경하지 않아 기존 使用者 資料 이미지를 繼續處理 사용할 數 있다.

實際資料 Xorg/VNC 화면에서 中文 Java 工作區, Swing 測試 窗口, 기존 이미지의 `問候例.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. 退出程式 시 시스템 OverlayFS와 資料 파일시스템의 讀取 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 測試 結果](build/verification/desktop.json)
- [그래픽 測試 日誌值](build/verification/desktop.log)
- [키보드·마우스 測試 屏幕](build/verification/desktop-input.png)
- [問候例 範例 屏幕](build/verification/desktop-greeting.png)
- [수정한 範例 원문의 屏幕 없는 執行命令 結果](build/verification/headless-example.log)

原始碼 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 檔案·字元·스레드 기능을 실행하고 안내를 출력한다. 使用者 홈의 기존 원문을 자동 교체하지는 않는다. 향후 構建映像 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 韓文文本 輸入值·字體值 보완

`make test-korean`으로 實際資料 Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space 切換模式 및 두벌식 鍵值 입력을 시험했다. 양쪽에서 `韓文文本 輸入值`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 使用者 資料 이미지에서 실행했으며 是否常規 退出程式 시 두 파일시스템의 讀取 전용 전환을 확인했다.

終端 字體值 진단에서 영문 DejaVu Sans Mono와 韓文文本 Noto Sans Mono CJK KR의 實際資料 檔案 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 屏幕 캡처에서 韓文文本·영문 顯示值, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 使用者 시스템 변경분에 적용하며 分發值 默認值 이미지와 base-id는 유지한다. 기존 檔案 백업, 동일 수정의 迭代值 적용 방지, 손상된 修改值 檔案 및 다른 base-id 拒絕值, 使用者 입력기 設置 병합에 대한 宿主 測試 4개도 통과했다. 원래 使用者 資料 構建映像 `build/manual-user.img`는 시험에 사용하지 않았다.

- [韓文文本 輸入值·字體值 測試 結果](build/verification/korean.json)
- [輸入值·實際資料 字體值 로딩 日誌值](build/verification/korean.log)
- [Swing·終端 韓文文本 屏幕](build/verification/korean-desktop.png)
- [Java 工作區 字體值 屏幕](build/verification/korean-workbench.png)
- [設置 보존 測試](build/verification/desktop-update-tests.log)

### 남은 裁剪

- 새 編譯原始碼 目標值 `openjdk`는 **네이티브 運行器 + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 支持值 범위는 여전히 제한적이다.
- 執行命令 프로그램에는 main 條目分, 호환 類別值 버전과 의존 JAR/JNI가 필요하다. 개별 상용 程式, 모든 Java 模塊值, 모든 문자권을 시험한 것은 아니다.
- 中文 Java 라이브러리는 檔案·字元·通信·스레드·Swing을 위한 輔助值 API이며 JDK 전체 API의 中文 번역판은 아니다.
- Pi 4 전용 펌웨어·內核值·設備 트리는 이미지에 들어 있지만 實際資料 SD 啓動, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 韓文文本 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- 使用者 目錄值 이동은 동일 시스템 構建映像 標識符值, ARM64, `/home/user`, UID 1000을 전제로 한다. 退出程式 之後狀態 소유권·權限值·링크·擴展名值 屬性值·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

安裝值·複製值 절차는 [README.md](README.md), 編譯原始碼 방식은 [OpenJDK 執行命令 檔案 指南](../../compiler/OpenJDK-可執行文件檔案.md)를 따른다. 構建映像 파일만 생성했으며 實際資料 SD 카드나 USB 디스크에 기록하지 않았다.
