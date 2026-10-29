# OpenJDK 源代码树 빌드와 内置 Java 内核值 移植

**소스에서 OpenJDK를 만드는 일과, 그 결과를 内置 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 内置 Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## 编译源代码 경로의 分隔符值

| 目标值 | 입력과 结果 | 执行命令 条件 |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → 内置 x86 AOT → ELF32 | 해당 CPU·内置 ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | 内置 ARM64 内核值/用户 ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 源代码树 → 공식 configure/make → JDK 构建映像 | **构建系统 目标值 OS/CPU의 执行命令 契约值** |

OpenJDK는 Java 文件 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI 连接,
类值 라이브러리의 C/C++ 实现, 运行器, 模块值 构建映像 및 生成 도구를 함께 빌드한다.
따라서 内置 AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK 构建系统 文档集](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## 源代码树 构建系统 命令

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ 编译器·Autoconf·Make와
开发 헤더를 준비한다. Swing/AWT의 Linux 库 빌드에는 X11·字体值 등의
开发 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/编译器.py --target openjdk-build \
  --java-home /路径/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /路径/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 源代码树 트리 밖의 전용 构建系统 디렉터리다.
源代码树·构建系统·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 构建系统 디렉터리는 재실행할 数 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI 库
- `jkoros-openjdk-build.json`: 阶段值·命令·源代码树 识别值 哈希文件·成功值/失败值·ABI 检查项
- `driver-configure.log`, `images.log`: 단계별 日志值

실패하면 退出程序 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 构建系统 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
源代码树 빌드만으로 内置 内核值 执行命令 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 最新值 교차 컴파일러와 **目标值 libc/헤더/库**首位操作数 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/编译器.py --target openjdk-build \
  --java-home /路径/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /路径/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /路径/OpenJDK소스
```

부트 JDK는 构建系统 호스트에서 실행된다. 교차 构建系统 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## 当前项目 任务 공간의 有效性校验 数据

分析值 项目根 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[源代码树 출처와 다운로드 哈希文件](build/openjdk-port/source.json)를 보관한다.
构建系统 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 构建系统 호스트용이며 内置 内核值 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac 执行命令 시험을 통과했다. 기존 编译器 회귀 시험과 새 构建系统 路径 시험도
총 **25개 通过值**했다. 공식 分发值 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 有效性校验 日志记录](build/openjdk-port/verification.json)은 构建系统 산출물과 执行命令 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[构建系统 日志记录](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[执行命令 测试](build/openjdk-port/smoke/report.json)을 각각 확인한다.
执行命令 시험은 새로 빌드한 java/javac로 韩文文本 源代码树, long/double, UTF-8 文件,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 实际数据 JFrame 屏幕 시험을 뜻하지 않는다.
Linux에서 한 시험이 内置 内核值 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

当前项目 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 数 없으며, 준비한 musl 环境 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 任务 공간에서는 下一项目 단축 명령으로 같은 musl 환경을 사용한다.
用户·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 源代码树/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 数 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 当前项目 디렉터리를 유지하므로, 韩文文本 소스도 对端值 경로로
컴파일하고 실행할 数 있다. 예를 들어 앞의 시험에서 생성한 소스를 重试值 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/原生构建测试.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 原生构建测试
```

## 기존 ARM64 OpenJDK를 内置 커널에 복사할 数 是否执行存在

현재는 실행할 数 없다. 저장되어 있는 ARM64 OpenJDK 25의 静态值 检查项 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
检查项 도구는 执行命令 파일을 **실행하지 않고** ELF와 동적 符号·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

内置 커널에 직접 적재할 数 없으면 检查项 결과를 저장한 后端值 **退出程序 代码值 3**을 반환한다.
ELF 호환성 검사는 实际数据 内核值 로더의 모든 검증을 대체하지 않는다.

| 확인한 条件 | ARM64 OpenJDK | 当前项目 内置 内核值 |
|---|---|---|
| ELF | PIE/공유 库, 동적 재배치 | 고정 地址 ET_EXEC, 内置 ABI note |
| 运行器 | `/lib/ld-musl-aarch64.so.1` 所需条件值 | PT_INTERP/PT_DYNAMIC/PT_TLS 拒绝值 |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 调用 | 일부 文件·루프백·GUI SVC와 협력식 세션 |
| 内存数据 | VM·GC·类值·代码值 캐시의 동적 地址 地址区域 | 用户 区域值 16 MiB, 构建映像 区域值 12 MiB |
| 文件 | 큰 `lib/modules`, 공유 库 및 数据 | RAM 文件 하나당 16 KiB, 영속 存储值 缺失方法 |
| Java 类值 | OpenJDK 25 class 버전 69 | 内置 JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·字体值·窗口 시스템 | 별도로 구현한 Swing API 부분집합 |

实际数据 ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 当前项目 제한은
[ELF 로더](../platforms/rpi4-native/计算机/用户.c),
[地址 地址区域 定义值](../platforms/rpi4-native/计算机/用户.h),
[RAM 文件 实现](../platforms/rpi4-native/源代码/内存文件集.java),
[用户 ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 数 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM 文件 업로드 제한을 피하지만,
OpenJDK에 필요한 地址 地址区域·스레드·동적 连接 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 操作系统 调用·内存数据·동적 连接 규약까지 맞지는 않는다.
文件 大小 제한이나 ELF 格式值 검사만 풀어도 해결되는 문제가 아니다.

## 内置 커널을 유지하면서 이식하는 阶段值

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 操作系统 ABI를 갖춘 用户 프로그램으로 실행할 数 있다.

기술적으로는 새 운영체제용 OpenJDK 硬件端口 또는 충분한 Linux 用户 ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 当前项目 코드와 实际数据 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **操作系统 ABI와 libc 基础**: 큰 文件·地址 地址区域, 페이지 예약/提交值/해제와 保护值 更改值,
   표준 文件/时钟 인터페이스, 错误 编号·C 런타임·目标值 sysroot를 구현한다.
2. **实际数据 네이티브 스레드와 同步化**: pthread에 대응하는 스케줄링·TLS·뮤텍스·条件 变量值,
   원자 操作值·内存数据 排序值·중단/깨우기, 신호/异常 문맥과 가드 페이지를 제공한다.
   当前项目 vi/Swing의 输入值 대기에서 문맥을 보관하는 기능만으로 대체할 数 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 库·TLS 또는 이식에 맞는 静态值 连接,
   JVM 네이티브 符号 해결, 영속 文件 시스템, 일반 프로그램의 2초 限制值 재설계를 수행한다.
4. **HotSpot OS 硬件端口**: 构建系统 시스템과 `src/hotspot/os`, `os_cpu`에 内置 OS/AArch64 경계를
   구현한다. 기존 AArch64 命令 생성기는 재사용할 数 있지만 OS 종속부를 구현해야 한다.
   首位项目 执行命令 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **类值 库·javac**: java.base의 JNI/文件/네트워크/프로세스 연결과 模块值 적재를
   구현한 后端值 内置 内核值 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 外部值 네트워크**: AWT/Java2D의 窗口·输入值·字体值 백엔드와 实际数据 NIC/TCP/IP를
   이식한다. 当前项目 内置 Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **有效性校验**: 단계별 OS ABI 测试, OpenJDK jtreg 测试, GUI/韩文文本/네트워크 부하 测试,
   实际数据 Pi4 검증을 수행한다. 일부 测试 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK 代码值:
[POSIX 内存数据·OS 实现](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 边界位置值](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·内存数据 进程值条目](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

内置 Java AOT 자체를 OpenJDK의 Java 代码值 전체를 처리하도록 확장하는 경로도 별도 개발이다.
对象值 모델·가상/인터페이스 调用·异常·GC·long/float/double·모든 数组值·同步化·동적 调用·
类值 初始化/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
