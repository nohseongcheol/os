# OpenJDK ソース木 빌드와 内蔵 Java 中核値 移植

**소스에서 OpenJDK를 만드는 일과, 그 결과를 内蔵 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 内蔵 Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## ソースコンパイル 경로의 区切り記号値

| 対象値 | 입력과 結果 | 命令実行 条件 |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → 内蔵 x86 AOT → ELF32 | 해당 CPU·内蔵 ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | 内蔵 ARM64 中核値/利用者 ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 ソース木 → 공식 configure/make → JDK イメージ構築 | **システム構築 対象値 OS/CPU의 命令実行 契約値** |

OpenJDK는 Java ファイル 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI 接続,
クラス値 라이브러리의 C/C++ 実装, プログラム実行器, モジュール値 イメージ構築 및 生成 도구를 함께 빌드한다.
따라서 内蔵 AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK システム構築 文書](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## ソース木 システム構築 命令

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ コンパイラ·Autoconf·Make와
開発 헤더를 준비한다. Swing/AWT의 Linux ライブラリ 빌드에는 X11·書体値 등의
開発 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/コンパイラ.py --target openjdk-build \
  --java-home /経路/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /経路/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 ソース木 트리 밖의 전용 システム構築 디렉터리다.
ソース木·システム構築·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 システム構築 디렉터리는 재실행할 数 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI ライブラリ
- `jkoros-openjdk-build.json`: 工程値·命令·ソース木 値識別処理 ハッシュファイル·成功値/失敗値·ABI 検査項目
- `driver-configure.log`, `images.log`: 단계별 履歴記録値

실패하면 終了点プログラム 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 システム構築 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
ソース木 빌드만으로 内蔵 中核値 命令実行 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 最新値 교차 컴파일러와 **対象値 libc/헤더/ライブラリ**先頭位置被演算子 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/コンパイラ.py --target openjdk-build \
  --java-home /経路/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /経路/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /経路/OpenJDK소스
```

부트 JDK는 システム構築 호스트에서 실행된다. 교차 システム構築 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## 現在項目 作業 공간의 妥当性検査 データ

値分析 計画根 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[ソース木 출처와 다운로드 ハッシュファイル](build/openjdk-port/source.json)를 보관한다.
システム構築 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 システム構築 호스트용이며 内蔵 中核値 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac 命令実行 시험을 통과했다. 기존 コンパイラ 회귀 시험과 새 システム構築 経路 시험도
총 **25개 通過値**했다. 공식 配布値 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 妥当性検査 履歴記録記録](build/openjdk-port/verification.json)은 システム構築 산출물과 命令実行 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[システム構築 履歴記録記録](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[命令実行 試験](build/openjdk-port/smoke/report.json)을 각각 확인한다.
命令実行 시험은 새로 빌드한 java/javac로 ハングル文字列 ソース木, long/double, UTF-8 ファイル,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 実際データ JFrame 画面 시험을 뜻하지 않는다.
Linux에서 한 시험이 内蔵 中核値 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

現在項目 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 数 없으며, 준비한 musl 環境 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 作業 공간에서는 次回項目 단축 명령으로 같은 musl 환경을 사용한다.
利用者·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 ソース木/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 数 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 現在項目 디렉터리를 유지하므로, ハングル文字列 소스도 通信相手値 경로로
컴파일하고 실행할 数 있다. 예를 들어 앞의 시험에서 생성한 소스를 再試行処理値 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/自前構築試験.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 自前構築試験
```

## 기존 ARM64 OpenJDK를 内蔵 커널에 복사할 数 実施判定存在

현재는 실행할 数 없다. 저장되어 있는 ARM64 OpenJDK 25의 静的値 検査項目 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
検査項目 도구는 命令実行 파일을 **실행하지 않고** ELF와 동적 記号·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

内蔵 커널에 직접 적재할 数 없으면 検査項目 결과를 저장한 後端値 **終了点プログラム コード値 3**을 반환한다.
ELF 호환성 검사는 実際データ 中核値 로더의 모든 검증을 대체하지 않는다.

| 확인한 条件 | ARM64 OpenJDK | 現在項目 内蔵 中核値 |
|---|---|---|
| ELF | PIE/공유 ライブラリ, 동적 재배치 | 고정 番地 ET_EXEC, 内蔵 ABI note |
| プログラム実行器 | `/lib/ld-musl-aarch64.so.1` 必要値 | PT_INTERP/PT_DYNAMIC/PT_TLS 値却下 |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 呼出 | 일부 ファイル·루프백·GUI SVC와 협력식 세션 |
| 記憶データ | VM·GC·クラス値·コード値 캐시의 동적 番地 番地領域 | 利用者 領域値 16 MiB, イメージ構築 領域値 12 MiB |
| ファイル | 큰 `lib/modules`, 공유 ライブラリ 및 データ | RAM ファイル 하나당 16 KiB, 영속 格納値 未存在メソッド |
| Java クラス値 | OpenJDK 25 class 버전 69 | 内蔵 JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·書体値·窓 시스템 | 별도로 구현한 Swing API 부분집합 |

実際データ ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 現在項目 제한은
[ELF 로더](../platforms/rpi4-native/機械/利用者.c),
[番地 番地領域 定義値](../platforms/rpi4-native/機械/利用者.h),
[RAM ファイル 実装](../platforms/rpi4-native/ソース/記憶ファイル群.java),
[利用者 ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 数 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM ファイル 업로드 제한을 피하지만,
OpenJDK에 필요한 番地 番地領域·스레드·동적 接続 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 稼働システム 呼出·記憶データ·동적 接続 규약까지 맞지는 않는다.
ファイル 容量 제한이나 ELF 書式値 검사만 풀어도 해결되는 문제가 아니다.

## 内蔵 커널을 유지하면서 이식하는 工程値

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 稼働システム ABI를 갖춘 利用者 프로그램으로 실행할 数 있다.

기술적으로는 새 운영체제용 OpenJDK 機器ポート 또는 충분한 Linux 利用者 ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 現在項目 코드와 実際データ 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **稼働システム ABI와 libc 基盤**: 큰 ファイル·番地 番地領域, 페이지 예약/確定値/해제와 値防護 値変更,
   표준 ファイル/時計 인터페이스, エラー 番号·C 런타임·対象値 sysroot를 구현한다.
2. **実際データ 네이티브 스레드와 同期化**: pthread에 대응하는 스케줄링·TLS·뮤텍스·条件 変数値,
   원자 操作値·記憶データ 順序値·중단/깨우기, 신호/例外 문맥과 가드 페이지를 제공한다.
   現在項目 vi/Swing의 入力値 대기에서 문맥을 보관하는 기능만으로 대체할 数 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 ライブラリ·TLS 또는 이식에 맞는 静的値 接続,
   JVM 네이티브 記号 해결, 영속 ファイル 시스템, 일반 프로그램의 2초 上限値 재설계를 수행한다.
4. **HotSpot OS 機器ポート**: システム構築 시스템과 `src/hotspot/os`, `os_cpu`에 内蔵 OS/AArch64 경계를
   구현한다. 기존 AArch64 命令 생성기는 재사용할 数 있지만 OS 종속부를 구현해야 한다.
   先頭位置項目 命令実行 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **クラス値 ライブラリ·javac**: java.base의 JNI/ファイル/네트워크/프로세스 연결과 モジュール値 적재를
   구현한 後端値 内蔵 中核値 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 外部値 네트워크**: AWT/Java2D의 窓·入力値·書体値 백엔드와 実際データ NIC/TCP/IP를
   이식한다. 現在項目 内蔵 Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **妥当性検査**: 단계별 OS ABI 試験, OpenJDK jtreg 試験, GUI/ハングル文字列/네트워크 부하 試験,
   実際データ Pi4 검증을 수행한다. 일부 試験 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK コード値:
[POSIX 記憶データ·OS 実装](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 境界位置値](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·記憶データ プロセス値入口](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

内蔵 Java AOT 자체를 OpenJDK의 Java コード値 전체를 처리하도록 확장하는 경로도 별도 개발이다.
オブジェクト値 모델·가상/인터페이스 呼出·例外·GC·long/float/double·모든 配列値·同期化·동적 呼出·
クラス値 初期化/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
