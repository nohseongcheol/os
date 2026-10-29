# OpenJDK 原始碼樹 빌드와 內建 Java 內核值 移植

**소스에서 OpenJDK를 만드는 일과, 그 결과를 內建 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 內建 Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## 編譯原始碼 경로의 分隔符值

| 目標值 | 입력과 結果 | 執行命令 條件 |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → 內建 x86 AOT → ELF32 | 해당 CPU·內建 ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | 內建 ARM64 內核值/使用者 ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 原始碼樹 → 공식 configure/make → JDK 構建映像 | **構建系統 目標值 OS/CPU의 執行命令 契約值** |

OpenJDK는 Java 檔案 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI 連接,
類別值 라이브러리의 C/C++ 實現, 運行器, 模塊值 構建映像 및 生成 도구를 함께 빌드한다.
따라서 內建 AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK 構建系統 文檔集](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## 原始碼樹 構建系統 命令

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ 編譯器·Autoconf·Make와
開發 헤더를 준비한다. Swing/AWT의 Linux 庫 빌드에는 X11·字體值 등의
開發 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/編譯器.py --target openjdk-build \
  --java-home /路徑/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /路徑/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 原始碼樹 트리 밖의 전용 構建系統 디렉터리다.
原始碼樹·構建系統·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 構建系統 디렉터리는 재실행할 數 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI 庫
- `jkoros-openjdk-build.json`: 階段值·命令·原始碼樹 識別值 哈希檔案·成功值/失敗值·ABI 檢查項
- `driver-configure.log`, `images.log`: 단계별 日誌值

실패하면 退出程式 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 構建系統 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
原始碼樹 빌드만으로 內建 內核值 執行命令 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 最新值 교차 컴파일러와 **目標值 libc/헤더/庫**首位操作數 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/編譯器.py --target openjdk-build \
  --java-home /路徑/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /路徑/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /路徑/OpenJDK소스
```

부트 JDK는 構建系統 호스트에서 실행된다. 교차 構建系統 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## 當前項目 任務 공간의 有效性校驗 資料

分析值 項目根 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[原始碼樹 출처와 다운로드 哈希檔案](build/openjdk-port/source.json)를 보관한다.
構建系統 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 構建系統 호스트용이며 內建 內核值 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac 執行命令 시험을 통과했다. 기존 編譯器 회귀 시험과 새 構建系統 路徑 시험도
총 **25개 通過值**했다. 공식 分發值 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 有效性校驗 日誌記錄](build/openjdk-port/verification.json)은 構建系統 산출물과 執行命令 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[構建系統 日誌記錄](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[執行命令 測試](build/openjdk-port/smoke/report.json)을 각각 확인한다.
執行命令 시험은 새로 빌드한 java/javac로 韓文文本 原始碼樹, long/double, UTF-8 檔案,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 實際資料 JFrame 屏幕 시험을 뜻하지 않는다.
Linux에서 한 시험이 內建 內核值 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

當前項目 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 數 없으며, 준비한 musl 環境 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 任務 공간에서는 下一項目 단축 명령으로 같은 musl 환경을 사용한다.
使用者·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 原始碼樹/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 數 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 當前項目 디렉터리를 유지하므로, 韓文文本 소스도 對端值 경로로
컴파일하고 실행할 數 있다. 예를 들어 앞의 시험에서 생성한 소스를 重試值 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/原生構建測試.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 原生構建測試
```

## 기존 ARM64 OpenJDK를 內建 커널에 복사할 數 是否執行存在

현재는 실행할 數 없다. 저장되어 있는 ARM64 OpenJDK 25의 靜態值 檢查項 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
檢查項 도구는 執行命令 파일을 **실행하지 않고** ELF와 동적 符號·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

內建 커널에 직접 적재할 數 없으면 檢查項 결과를 저장한 後端值 **退出程式 程式碼值 3**을 반환한다.
ELF 호환성 검사는 實際資料 內核值 로더의 모든 검증을 대체하지 않는다.

| 확인한 條件 | ARM64 OpenJDK | 當前項目 內建 內核值 |
|---|---|---|
| ELF | PIE/공유 庫, 동적 재배치 | 고정 地址 ET_EXEC, 內建 ABI note |
| 運行器 | `/lib/ld-musl-aarch64.so.1` 所需條件值 | PT_INTERP/PT_DYNAMIC/PT_TLS 拒絕值 |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 調用 | 일부 檔案·루프백·GUI SVC와 협력식 세션 |
| 記憶體資料 | VM·GC·類別值·程式碼值 캐시의 동적 地址 地址區域 | 使用者 區域值 16 MiB, 構建映像 區域值 12 MiB |
| 檔案 | 큰 `lib/modules`, 공유 庫 및 資料 | RAM 檔案 하나당 16 KiB, 영속 存儲值 缺失方法 |
| Java 類別值 | OpenJDK 25 class 버전 69 | 內建 JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·字體值·窗口 시스템 | 별도로 구현한 Swing API 부분집합 |

實際資料 ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 當前項目 제한은
[ELF 로더](../platforms/rpi4-native/計算機/使用者.c),
[地址 地址區域 定義值](../platforms/rpi4-native/計算機/使用者.h),
[RAM 檔案 實現](../platforms/rpi4-native/原始碼/記憶體檔案集.java),
[使用者 ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 數 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM 檔案 업로드 제한을 피하지만,
OpenJDK에 필요한 地址 地址區域·스레드·동적 連接 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 操作系統 調用·記憶體資料·동적 連接 규약까지 맞지는 않는다.
檔案 大小 제한이나 ELF 格式值 검사만 풀어도 해결되는 문제가 아니다.

## 內建 커널을 유지하면서 이식하는 階段值

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 操作系統 ABI를 갖춘 使用者 프로그램으로 실행할 數 있다.

기술적으로는 새 운영체제용 OpenJDK 硬件埠 또는 충분한 Linux 使用者 ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 當前項目 코드와 實際資料 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **操作系統 ABI와 libc 基礎**: 큰 檔案·地址 地址區域, 페이지 예약/提交值/해제와 保護值 更改值,
   표준 檔案/時鐘 인터페이스, 錯誤 編號·C 런타임·目標值 sysroot를 구현한다.
2. **實際資料 네이티브 스레드와 同步化**: pthread에 대응하는 스케줄링·TLS·뮤텍스·條件 變量值,
   원자 操作值·記憶體資料 排序值·중단/깨우기, 신호/異常 문맥과 가드 페이지를 제공한다.
   當前項目 vi/Swing의 輸入值 대기에서 문맥을 보관하는 기능만으로 대체할 數 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 庫·TLS 또는 이식에 맞는 靜態值 連接,
   JVM 네이티브 符號 해결, 영속 檔案 시스템, 일반 프로그램의 2초 限制值 재설계를 수행한다.
4. **HotSpot OS 硬件埠**: 構建系統 시스템과 `src/hotspot/os`, `os_cpu`에 內建 OS/AArch64 경계를
   구현한다. 기존 AArch64 命令 생성기는 재사용할 數 있지만 OS 종속부를 구현해야 한다.
   首位項目 執行命令 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **類別值 庫·javac**: java.base의 JNI/檔案/네트워크/프로세스 연결과 模塊值 적재를
   구현한 後端值 內建 內核值 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 外部值 네트워크**: AWT/Java2D의 窗口·輸入值·字體值 백엔드와 實際資料 NIC/TCP/IP를
   이식한다. 當前項目 內建 Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **有效性校驗**: 단계별 OS ABI 測試, OpenJDK jtreg 測試, GUI/韓文文本/네트워크 부하 測試,
   實際資料 Pi4 검증을 수행한다. 일부 測試 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK 程式碼值:
[POSIX 記憶體資料·OS 實現](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 邊界位置值](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·記憶體資料 程序值條目](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

內建 Java AOT 자체를 OpenJDK의 Java 程式碼值 전체를 처리하도록 확장하는 경로도 별도 개발이다.
物件值 모델·가상/인터페이스 調用·異常·GC·long/float/double·모든 陣列值·同步化·동적 調用·
類別值 初始化/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
