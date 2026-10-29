# OpenJDK સ્રોત_ટ્રી 빌드와 자체 Java કર્નેલ_મૂલ્ય 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 자체 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 자체 Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## બિલ્ડ_કરો_સ્રોત 경로의 સીમાનિર્ધારક_મૂલ્ય

| લક્ષ્ય | 입력과 પરિમાણ | અમલ_કરો_આદેશ શરત |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → 자체 x86 AOT → ELF32 | 해당 CPU·자체 ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | 자체 ARM64 કર્નેલ_મૂલ્ય/ઉપયોગકર્તા ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 સ્રોત_ટ્રી → 공식 configure/make → JDK બિલ્ડ_છબી | **બિલ્ડ_સિસ્ટમ લક્ષ્ય OS/CPU의 અમલ_કરો_આદેશ કામ_મૂલ્ય** |

OpenJDK는 Java ફાઈલ 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI સંપર્ક_કરો,
વર્ગ_મૂલ્ય 라이브러리의 C/C++ 구현, એપ્લિકેશન_લૉન્ચર, મૉડ્યૂલ_મૂલ્ય બિલ્ડ_છબી 및 જનરેટ_કરો 도구를 함께 빌드한다.
따라서 자체 AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK બિલ્ડ_સિસ્ટમ 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## સ્રોત_ટ્રી બિલ્ડ_સિસ્ટમ આદેશ

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ 컴파일러·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux લાઇબ્રેરી 빌드에는 X11·ફૉન્ટ_મૂલ્ય 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /પથ/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /પથ/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 સ્રોત_ટ્રી 트리 밖의 전용 બિલ્ડ_સિસ્ટમ 디렉터리다.
સ્રોત_ટ્રી·બિલ્ડ_સિસ્ટમ·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 બિલ્ડ_સિસ્ટમ 디렉터리는 재실행할 수 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI લાઇબ્રેરી
- `jkoros-openjdk-build.json`: સ્ટેજ_મૂલ્ય·આદેશ·સ્રોત_ટ્રી 식별 હૅશ_ફાઇલ·성공/નિષ્ફળતા_મૂલ્ય·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 લૉગ_મૂલ્ય

실패하면 પ્રસ્થાન_એપ્લિકેશન 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 બિલ્ડ_સિસ્ટમ 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
સ્રોત_ટ્રી 빌드만으로 자체 કર્નેલ_મૂલ્ય અમલ_કરો_આદેશ 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **લક્ષ્ય libc/헤더/લાઇબ્રેરી**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /પથ/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /પથ/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /પથ/OpenJDK소스
```

부트 JDK는 બિલ્ડ_સિસ્ટમ 호스트에서 실행된다. 교차 બિલ્ડ_સિસ્ટમ 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## 현재 작업 공간의 માન્ય_કરો ડેટા

분석 પ્રોજેક્ટ_રૂટ 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[સ્રોત_ટ્રી 출처와 다운로드 હૅશ_ફાઇલ](build/openjdk-port/source.json)를 보관한다.
બિલ્ડ_સિસ્ટમ 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 બિલ્ડ_સિસ્ટમ 호스트용이며 자체 કર્નેલ_મૂલ્ય 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac અમલ_કરો_આદેશ 시험을 통과했다. 기존 컴파일러 회귀 시험과 새 બિલ્ડ_સિસ્ટમ પથ 시험도
총 **25개 પાસ_કરો_મૂલ્ય**했다. 공식 배포 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 માન્ય_કરો લૉગ_પંક્તિ](build/openjdk-port/verification.json)은 બિલ્ડ_સિસ્ટમ 산출물과 અમલ_કરો_આદેશ 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[બિલ્ડ_સિસ્ટમ લૉગ_પંક્તિ](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[અમલ_કરો_આદેશ 시험](build/openjdk-port/smoke/report.json)을 각각 확인한다.
અમલ_કરો_આદેશ 시험은 새로 빌드한 java/javac로 한글 સ્રોત_ટ્રી, long/double, UTF-8 ફાઈલ,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 વાસ્તવિક_ડેટા JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 자체 કર્નેલ_મૂલ્ય 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

현재 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 수 없으며, 준비한 musl 환경 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 આગલું_આઇટમ 단축 명령으로 같은 musl 환경을 사용한다.
ઉપયોગકર્તા·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 સ્રોત_ટ્રી/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 수 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 현재 디렉터리를 유지하므로, 한글 소스도 પીઅર_મૂલ્ય 경로로
컴파일하고 실행할 수 있다. 예를 들어 앞의 시험에서 생성한 소스를 다시 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/자체빌드시험.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 자체빌드시험
```

## 기존 ARM64 OpenJDK를 자체 커널에 복사할 수 있는가

현재는 실행할 수 없다. 저장되어 있는 ARM64 OpenJDK 25의 સ્થિર_મૂલ્ય 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 અમલ_કરો_આદેશ 파일을 **실행하지 않고** ELF와 동적 પ્રતીક·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

자체 커널에 직접 적재할 수 없으면 검사 결과를 저장한 બેક_મૂલ્ય **પ્રસ્થાન_એપ્લિકેશન 코드 3**을 반환한다.
ELF 호환성 검사는 વાસ્તવિક_ડેટા કર્નેલ_મૂલ્ય 로더의 모든 검증을 대체하지 않는다.

| 확인한 શરત | ARM64 OpenJDK | 현재 자체 કર્નેલ_મૂલ્ય |
|---|---|---|
| ELF | PIE/공유 લાઇબ્રેરી, 동적 재배치 | 고정 સરનામું ET_EXEC, 자체 ABI note |
| એપ્લિકેશન_લૉન્ચર | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS નકારો_મૂલ્ય |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 ફાઈલ·루프백·GUI SVC와 협력식 세션 |
| મેમરી_ડેટા | VM·GC·વર્ગ_મૂલ્ય·코드 캐시의 동적 સરનામું 공간 | ઉપયોગકર્તા 영역 16 MiB, બિલ્ડ_છબી 영역 12 MiB |
| ફાઈલ | 큰 `lib/modules`, 공유 લાઇબ્રેરી 및 ડેટા | RAM ફાઈલ 하나당 16 KiB, 영속 સંગ્રહ_કરવો_મૂલ્ય 없음 |
| Java વર્ગ_મૂલ્ય | OpenJDK 25 class 버전 69 | 자체 JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·ફૉન્ટ_મૂલ્ય·વિંડો 시스템 | 별도로 구현한 Swing API 부분집합 |

વાસ્તવિક_ડેટા ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 현재 제한은
[ELF 로더](../platforms/rpi4-native/મશીન/ઉપયોગકર્તા.c),
[સરનામું 공간 વ્યાખ્યા_મૂલ્ય](../platforms/rpi4-native/મશીન/ઉપયોગકર્તા.h),
[RAM ફાઈલ 구현](../platforms/rpi4-native/સ્રોત/મેમરી_ફાઇલો.java),
[ઉપયોગકર્તા ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 수 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM ફાઈલ 업로드 제한을 피하지만,
OpenJDK에 필요한 સરનામું 공간·스레드·동적 સંપર્ક_કરો 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 ઑપરેટિંગ_સિસ્ટમ 호출·મેમરી_ડેટા·동적 સંપર્ક_કરો 규약까지 맞지는 않는다.
ફાઈલ માપ 제한이나 ELF સ્વરૂપ_મૂલ્ય 검사만 풀어도 해결되는 문제가 아니다.

## 자체 커널을 유지하면서 이식하는 સ્ટેજ_મૂલ્ય

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 ઑપરેટિંગ_સિસ્ટમ ABI를 갖춘 ઉપયોગકર્તા 프로그램으로 실행할 수 있다.

기술적으로는 새 운영체제용 OpenJDK હાર્ડવેર_પૉર્ટ 또는 충분한 Linux ઉપયોગકર્તા ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 현재 코드와 વાસ્તવિક_ડેટા 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **ઑપરેટિંગ_સિસ્ટમ ABI와 libc 기반**: 큰 ફાઈલ·સરનામું 공간, 페이지 예약/확정/해제와 રક્ષણ_કરો_મૂલ્ય પરિવર્તન_કરો_મૂલ્ય,
   표준 ફાઈલ/ઘડિયાળ 인터페이스, ભૂલ અનુક્રમણિકા·C 런타임·લક્ષ્ય sysroot를 구현한다.
2. **વાસ્તવિક_ડેટા 네이티브 스레드와 સિંક્રનાઇઝ**: pthread에 대응하는 스케줄링·TLS·뮤텍스·શરત 변수,
   원자 ઑપરેશન_મૂલ્ય·મેમરી_ડેટા ક્રમ_મૂલ્ય·중단/깨우기, 신호/예외 문맥과 가드 페이지를 제공한다.
   현재 vi/Swing의 입력 대기에서 문맥을 보관하는 기능만으로 대체할 수 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 લાઇબ્રેરી·TLS 또는 이식에 맞는 સ્થિર_મૂલ્ય સંપર્ક_કરો,
   JVM 네이티브 પ્રતીક 해결, 영속 ફાઈલ 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS હાર્ડવેર_પૉર્ટ**: બિલ્ડ_સિસ્ટમ 시스템과 `src/hotspot/os`, `os_cpu`에 자체 OS/AArch64 경계를
   구현한다. 기존 AArch64 આદેશ 생성기는 재사용할 수 있지만 OS 종속부를 구현해야 한다.
   첫 અમલ_કરો_આદેશ 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **વર્ગ_મૂલ્ય લાઇબ્રેરી·javac**: java.base의 JNI/ફાઈલ/네트워크/프로세스 연결과 મૉડ્યૂલ_મૂલ્ય 적재를
   구현한 બેક_મૂલ્ય 자체 કર્નેલ_મૂલ્ય 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 외부 네트워크**: AWT/Java2D의 વિંડો·입력·ફૉન્ટ_મૂલ્ય 백엔드와 વાસ્તવિક_ડેટા NIC/TCP/IP를
   이식한다. 현재 자체 Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **માન્ય_કરો**: 단계별 OS ABI 시험, OpenJDK jtreg 시험, GUI/한글/네트워크 부하 시험,
   વાસ્તવિક_ડેટા Pi4 검증을 수행한다. 일부 시험 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK 코드:
[POSIX મેમરી_ડેટા·OS 구현](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 경계](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·મેમરી_ડેટા પ્રક્રિયા_મૂલ્ય_પ્રવેશ](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

자체 Java AOT 자체를 OpenJDK의 Java 코드 전체를 처리하도록 확장하는 경로도 별도 개발이다.
ઑબ્જેક્ટ_મૂલ્ય 모델·가상/인터페이스 호출·예외·GC·long/float/double·모든 અરે_મૂલ્ય·સિંક્રનાઇઝ·동적 호출·
વર્ગ_મૂલ્ય શરૂ_કરો/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
