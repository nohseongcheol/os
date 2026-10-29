# OpenJDK эх_мод 빌드와 자체 Java кернел_утга 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 자체 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 자체 Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## хөрвүүлэх_эх 경로의 тусгаарлах_тэмдэгт_утга

| зорилго | 입력과 결과 | Гүйцэтгэх_команд нөхцөл |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → 자체 x86 AOT → ELF32 | 해당 CPU·자체 ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | 자체 ARM64 кернел_утга/хэрэглэгч ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 эх_мод → 공식 configure/make → JDK хувилбар_зураг | **хувилбар_систем зорилго OS/CPU의 Гүйцэтгэх_команд нөхцөл_байдал_утга** |

OpenJDK는 Java Файл 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Холбох,
класс_утга 라이브러리의 C/C++ 구현, програм_гишүүн, 모듈 хувилбар_зураг 및 생성 도구를 함께 빌드한다.
따라서 자체 AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK хувилбар_систем 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## эх_мод хувилбар_систем Тушаал

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ 컴파일러·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux сан 빌드에는 X11·үсгийн_хэв_утга 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /ЗАМ/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /ЗАМ/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 эх_мод 트리 밖의 전용 хувилбар_систем 디렉터리다.
эх_мод·хувилбар_систем·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 хувилбар_систем 디렉터리는 재실행할 수 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI сан
- `jkoros-openjdk-build.json`: үе_шат_утга_29ee1bb7·Тушаал·эх_мод 식별 Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл·성공/гэмтэл_утга·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 бичих_утга_e0918eb0

실패하면 Гарах_програм 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 хувилбар_систем 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
эх_мод 빌드만으로 자체 кернел_утга Гүйцэтгэх_команд 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **зорилго libc/헤더/сан**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /ЗАМ/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /ЗАМ/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /ЗАМ/OpenJDK소스
```

부트 JDK는 хувилбар_систем 호스트에서 실행된다. 교차 хувилбар_систем 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## 현재 작업 공간의 баталгаажуулах өгөгдөл

분석 기준 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[эх_мод 출처와 다운로드 Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл](build/openjdk-port/source.json)를 보관한다.
хувилбар_систем 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 хувилбар_систем 호스트용이며 자체 кернел_утга 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac Гүйцэтгэх_команд 시험을 통과했다. 기존 컴파일러 회귀 시험과 새 хувилбар_систем ЗАМ 시험도
총 **25개 통과**했다. 공식 배포 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 баталгаажуулах бичих_мөр_6e8b375a](build/openjdk-port/verification.json)은 хувилбар_систем 산출물과 Гүйцэтгэх_команд 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[хувилбар_систем бичих_мөр_6e8b375a](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[Гүйцэтгэх_команд 시험](build/openjdk-port/smoke/report.json)을 각각 확인한다.
Гүйцэтгэх_команд 시험은 새로 빌드한 java/javac로 한글 эх_мод, long/double, UTF-8 Файл,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 бодит_өгөгдөл JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 자체 кернел_утга 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

현재 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 수 없으며, 준비한 musl 환경 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 다음 단축 명령으로 같은 musl 환경을 사용한다.
хэрэглэгч·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 эх_мод/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 수 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 현재 디렉터리를 유지하므로, 한글 소스도 ижил_түвшин_утга 경로로
컴파일하고 실행할 수 있다. 예를 들어 앞의 시험에서 생성한 소스를 다시 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/자체빌드시험.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 자체빌드시험
```

## 기존 ARM64 OpenJDK를 자체 커널에 복사할 수 있는가

현재는 실행할 수 없다. 저장되어 있는 ARM64 OpenJDK 25의 статик_утга 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 Гүйцэтгэх_команд 파일을 **실행하지 않고** ELF와 동적 тэмдэг·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

자체 커널에 직접 적재할 수 없으면 검사 결과를 저장한 Буцах_утга **Гарах_програм 코드 3**을 반환한다.
ELF 호환성 검사는 бодит_өгөгдөл кернел_утга 로더의 모든 검증을 대체하지 않는다.

| 확인한 нөхцөл | ARM64 OpenJDK | 현재 자체 кернел_утга |
|---|---|---|
| ELF | PIE/공유 сан, 동적 재배치 | 고정 хаяг ET_EXEC, 자체 ABI note |
| програм_гишүүн | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS 거부 |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 Файл·루프백·GUI SVC와 협력식 세션 |
| санах_ой_өгөгдөл | VM·GC·класс_утга·코드 캐시의 동적 хаяг 공간 | хэрэглэгч 영역 16 MiB, хувилбар_зураг 영역 12 MiB |
| Файл | 큰 `lib/modules`, 공유 сан 및 өгөгдөл | RAM Файл 하나당 16 KiB, 영속 хадгалах_утга 없음 |
| Java класс_утга | OpenJDK 25 class 버전 69 | 자체 JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·үсгийн_хэв_утга·цонх 시스템 | 별도로 구현한 Swing API 부분집합 |

бодит_өгөгдөл ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 현재 제한은
[ELF 로더](../platforms/rpi4-native/компьютер/хэрэглэгч.c),
[хаяг 공간 Тайлбар_утга](../platforms/rpi4-native/компьютер/хэрэглэгч.h),
[RAM Файл 구현](../platforms/rpi4-native/ЭХ/санах_ой_Файлууд.java),
[хэрэглэгч ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 수 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM Файл 업로드 제한을 피하지만,
OpenJDK에 필요한 хаяг 공간·스레드·동적 Холбох 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 үйлдлийн_систем 호출·санах_ой_өгөгдөл·동적 Холбох 규약까지 맞지는 않는다.
Файл Хэмжээ 제한이나 ELF формат_утга 검사만 풀어도 해결되는 문제가 아니다.

## 자체 커널을 유지하면서 이식하는 үе_шат_утга_29ee1bb7

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 үйлдлийн_систем ABI를 갖춘 хэрэглэгч 프로그램으로 실행할 수 있다.

기술적으로는 새 운영체제용 OpenJDK 포트 또는 충분한 Linux хэрэглэгч ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 현재 코드와 бодит_өгөгдөл 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **үйлдлийн_систем ABI와 libc 기반**: 큰 Файл·хаяг 공간, 페이지 예약/확정/해제와 хамгаалах_утга өөрчлөх_утга,
   표준 Файл/тактын_дохио 인터페이스, Алдаа индекс·C 런타임·зорилго sysroot를 구현한다.
2. **бодит_өгөгдөл 네이티브 스레드와 синхрончлох**: pthread에 대응하는 스케줄링·TLS·뮤텍스·нөхцөл 변수,
   원자 үйлдэл_утга·санах_ой_өгөгдөл дараалал_утга·중단/깨우기, 신호/예외 문맥과 가드 페이지를 제공한다.
   현재 vi/Swing의 입력 대기에서 문맥을 보관하는 기능만으로 대체할 수 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 сан·TLS 또는 이식에 맞는 статик_утга Холбох,
   JVM 네이티브 тэмдэг 해결, 영속 Файл 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS 포트**: хувилбар_систем 시스템과 `src/hotspot/os`, `os_cpu`에 자체 OS/AArch64 경계를
   구현한다. 기존 AArch64 Тушаал 생성기는 재사용할 수 있지만 OS 종속부를 구현해야 한다.
   첫 Гүйцэтгэх_команд 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **класс_утга сан·javac**: java.base의 JNI/Файл/네트워크/프로세스 연결과 모듈 적재를
   구현한 Буцах_утга 자체 кернел_утга 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 외부 네트워크**: AWT/Java2D의 цонх·입력·үсгийн_хэв_утга 백엔드와 бодит_өгөгдөл NIC/TCP/IP를
   이식한다. 현재 자체 Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **баталгаажуулах**: 단계별 OS ABI 시험, OpenJDK jtreg 시험, GUI/한글/네트워크 부하 시험,
   бодит_өгөгдөл Pi4 검증을 수행한다. 일부 시험 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK 코드:
[POSIX санах_ой_өгөгдөл·OS 구현](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 경계](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·санах_ой_өгөгдөл үйл_явц_утга_оролт](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

자체 Java AOT 자체를 OpenJDK의 Java 코드 전체를 처리하도록 확장하는 경로도 별도 개발이다.
объект_утга 모델·가상/인터페이스 호출·예외·GC·long/float/double·모든 олонлог_утга·синхрончлох·동적 호출·
класс_утга ажилд_бэлдэх/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
