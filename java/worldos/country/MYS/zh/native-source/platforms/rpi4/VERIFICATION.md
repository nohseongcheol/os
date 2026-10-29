# 分发值 构建映像 有效性校验 日志记录

검증일: 2026-09-27 (Asia/Seoul)

目标值: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 内置 x86 커널을 ARM으로 이식한 결과가 아니다. 实际数据 Pi 보드는 연결되어 있지 않아 硬件值 启动 성공을 확인하지 못했다.

## 배포물

| 文件 | 大小(字节值) | 说明 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | 存档值 시스템 构建映像; 释放存储装置 之后状态 1,475,747,840 字节值 |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 用户 数据 构建映像; 释放存储装置 之后状态 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/中文Java.jar` | 10,563 | 中文 辅助值 API와 Java 工作区 |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 存档值 构建映像 构建全部 끝까지 해제하여 原始 이미지의 SHA256과 일치함을 확인했다. [存档值 有效性校验 日志记录](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU 有效性校验 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 条目列表](dist/packages.lock.json)과 [原始 原点值](dist/sources.lock.json)를 제공한다.

## 통과한 检查项

| 检查项 | 实际数据 验证 内容值 | 日志记录 |
|---|---|---|
| 宿主 编译器 测试 19개 | 기존 AOT 회귀 测试, `.class` 직접 输入值, OpenJDK ELF 运行器, JAR 依赖项列, 상속·리플렉션·람다·스레드·리소스, 路径 移动值, 失败值 시 기존 输出 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi 构建映像 结构 | MBR 边界位置值, FAT 启动 파티션, Pi 펌웨어, ARM64 内核值, Pi 4 DTB, initramfs, SquashFS 및 哈希文件 | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 检查项, 启动 之后状态 두 런타임의 实际数据 执行命令 | [런타임 日志记录](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 首位项目 启动 | 读取 전용 시스템, Java 文件·Unicode值·异常·对象值·스레드·HTTP/TCP·子值 프로세스, Swing, CJK·아랍어·데바나가리 字体值, Python 文件·스레드·套接字值·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 执行命令 文件 生成 | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 执行命令 成功值 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | 用户 数据, `/etc` 设置, `/usr/local/bin` 程序, APK로 설치한 tree, pip 패키지, 文件 삭제 系统信息, 소유권, sudo, Java 执行命令 文件 保持值 | [restore.log](build/verification/restore.log) |
| 是否离线 홈 移动值 | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 复制值 | [migrate.log](build/verification/migrate.log) |
| 移动值 之后状态 启动 | 새 数据 이미지로 부팅하여 재부팅 복원 항목을 重试值 验证 | [migrated-restore.log](build/verification/migrated-restore.log) |
| 是否常规 退出程序 및 数据 무결성 | 일반 启动 3회 构建全部 OverlayFS/数据 设备 读取 전용 切换模式 成功值; 原始·已复制值 ext4의 `e2fsck -fn` 退出程序 代码值 0 | [原始 检查项](build/verification/fsck-original.log), [已复制值 检查项](build/verification/fsck-migrated.log) |

네 序列值 부팅은 构建全部 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 退出程序 代码值 0으로 통과했다. [전체 启动 결과와 日志值 哈希文件](build/verification/boot.json)

QEMU 가상 NIC의 DHCP 地址 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 外部值 인터넷이나 Pi Wi-Fi의 有效性校验 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [屏幕 캡처](build/verification/swing.png)에서 韩文文本·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## 实现 범위와 남은 有效性校验

### QEMU 그래픽 执行命令 보완

终端 전용 실행에서 `问候例.java`首位操作数 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. 分发值 시스템 이미지와 base-id는 변경하지 않아 기존 用户 数据 이미지를 继续处理 사용할 数 있다.

实际数据 Xorg/VNC 화면에서 中文 Java 工作区, Swing 测试 窗口, 기존 이미지의 `问候例.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. 退出程序 시 시스템 OverlayFS와 数据 파일시스템의 读取 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 测试 结果](build/verification/desktop.json)
- [그래픽 测试 日志值](build/verification/desktop.log)
- [키보드·마우스 测试 屏幕](build/verification/desktop-input.png)
- [问候例 用例 屏幕](build/verification/desktop-greeting.png)
- [수정한 用例 원문의 屏幕 없는 执行命令 结果](build/verification/headless-example.log)

源代码 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 文件·字符·스레드 기능을 실행하고 안내를 출력한다. 用户 홈의 기존 원문을 자동 교체하지는 않는다. 향후 构建映像 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 韩文文本 输入值·字体值 보완

`make test-korean`으로 实际数据 Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space 切换模式 및 두벌식 键值 입력을 시험했다. 양쪽에서 `韩文文本 输入值`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 用户 数据 이미지에서 실행했으며 是否常规 退出程序 시 두 파일시스템의 读取 전용 전환을 확인했다.

终端 字体值 진단에서 영문 DejaVu Sans Mono와 韩文文本 Noto Sans Mono CJK KR의 实际数据 文件 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 屏幕 캡처에서 韩文文本·영문 显示值, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 用户 시스템 변경분에 적용하며 分发值 默认值 이미지와 base-id는 유지한다. 기존 文件 백업, 동일 수정의 迭代值 적용 방지, 손상된 修改值 文件 및 다른 base-id 拒绝值, 用户 입력기 设置 병합에 대한 宿主 测试 4개도 통과했다. 원래 用户 数据 构建映像 `build/manual-user.img`는 시험에 사용하지 않았다.

- [韩文文本 输入值·字体值 测试 结果](build/verification/korean.json)
- [输入值·实际数据 字体值 로딩 日志值](build/verification/korean.log)
- [Swing·终端 韩文文本 屏幕](build/verification/korean-desktop.png)
- [Java 工作区 字体值 屏幕](build/verification/korean-workbench.png)
- [设置 보존 测试](build/verification/desktop-update-tests.log)

### 남은 裁剪

- 새 编译源代码 目标值 `openjdk`는 **네이티브 运行器 + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 支持值 범위는 여전히 제한적이다.
- 执行命令 프로그램에는 main 条目分, 호환 类值 버전과 의존 JAR/JNI가 필요하다. 개별 상용 程序, 모든 Java 模块值, 모든 문자권을 시험한 것은 아니다.
- 中文 Java 라이브러리는 文件·字符·通信·스레드·Swing을 위한 辅助值 API이며 JDK 전체 API의 中文 번역판은 아니다.
- Pi 4 전용 펌웨어·内核值·设备 트리는 이미지에 들어 있지만 实际数据 SD 启动, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 韩文文本 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- 用户 目录值 이동은 동일 시스템 构建映像 标识符值, ARM64, `/home/user`, UID 1000을 전제로 한다. 退出程序 之后状态 소유권·权限值·링크·扩展名值 属性值·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

安装值·复制值 절차는 [README.md](README.md), 编译源代码 방식은 [OpenJDK 执行命令 文件 指南](../../compiler/OpenJDK-可执行文件文件.md)를 따른다. 构建映像 파일만 생성했으며 实际数据 SD 카드나 USB 디스크에 기록하지 않았다.
