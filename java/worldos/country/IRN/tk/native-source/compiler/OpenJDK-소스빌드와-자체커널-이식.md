# OpenJDK gor_agaç 빌드와 자체 Java ýadro_baha 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 자체 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 자체 Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## düz_gor 경로의 bölüji_baha_d8ba4873

| niýet | 입력과 결과 | ýerine_ýetir_buýruk şert |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → 자체 x86 AOT → ELF32 | 해당 CPU·자체 ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | 자체 ARM64 ýadro_baha/ulanyjy ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 gor_agaç → 공식 configure/make → JDK düz_surat | **düz_ulgam niýet OS/CPU의 ýerine_ýetir_buýruk ýumuş_baha_102996da** |

OpenJDK는 Java Faýl 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Birikme,
klas_baha 라이브러리의 C/C++ 구현, programma_programma_paneli, 모듈 düz_surat 및 생성 도구를 함께 빌드한다.
따라서 자체 AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK düz_ulgam 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## gor_agaç düz_ulgam buýruk

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ 컴파일러·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux Kitaphana 빌드에는 X11·şrift_baha 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /Ýol/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /Ýol/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 gor_agaç 트리 밖의 전용 düz_ulgam 디렉터리다.
gor_agaç·düz_ulgam·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 düz_ulgam 디렉터리는 재실행할 수 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI Kitaphana
- `jkoros-openjdk-build.json`: tapgyr_baha·buýruk·gor_agaç 식별 heş_kody_faýl·성공/näsazlyk_baha·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 hasaba_alyş_baha

실패하면 çyk_programma 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 düz_ulgam 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
gor_agaç 빌드만으로 자체 ýadro_baha ýerine_ýetir_buýruk 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **niýet libc/헤더/Kitaphana**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /Ýol/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /Ýol/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /Ýol/OpenJDK소스
```

부트 JDK는 düz_ulgam 호스트에서 실행된다. 교차 düz_ulgam 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## 현재 작업 공간의 tassykla maglumat

분석 기준 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[gor_agaç 출처와 다운로드 heş_kody_faýl](build/openjdk-port/source.json)를 보관한다.
düz_ulgam 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 düz_ulgam 호스트용이며 자체 ýadro_baha 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac ýerine_ýetir_buýruk 시험을 통과했다. 기존 컴파일러 회귀 시험과 새 düz_ulgam Ýol 시험도
총 **25개 통과**했다. 공식 배포 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 tassykla hasaba_alyş_setir](build/openjdk-port/verification.json)은 düz_ulgam 산출물과 ýerine_ýetir_buýruk 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[düz_ulgam hasaba_alyş_setir](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[ýerine_ýetir_buýruk 시험](build/openjdk-port/smoke/report.json)을 각각 확인한다.
ýerine_ýetir_buýruk 시험은 새로 빌드한 java/javac로 한글 gor_agaç, long/double, UTF-8 Faýl,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 hakyky_maglumat JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 자체 ýadro_baha 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

현재 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 수 없으며, 준비한 musl 환경 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 다음 단축 명령으로 같은 musl 환경을 사용한다.
ulanyjy·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 gor_agaç/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 수 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 현재 디렉터리를 유지하므로, 한글 소스도 deň_derejeli_düwün_baha 경로로
컴파일하고 실행할 수 있다. 예를 들어 앞의 시험에서 생성한 소스를 다시 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/자체빌드시험.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 자체빌드시험
```

## 기존 ARM64 OpenJDK를 자체 커널에 복사할 수 있는가

현재는 실행할 수 없다. 저장되어 있는 ARM64 OpenJDK 25의 statiki_baha 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 ýerine_ýetir_buýruk 파일을 **실행하지 않고** ELF와 동적 nyşan·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

자체 커널에 직접 적재할 수 없으면 검사 결과를 저장한 Yza_baha **çyk_programma 코드 3**을 반환한다.
ELF 호환성 검사는 hakyky_maglumat ýadro_baha 로더의 모든 검증을 대체하지 않는다.

| 확인한 şert | ARM64 OpenJDK | 현재 자체 ýadro_baha |
|---|---|---|
| ELF | PIE/공유 Kitaphana, 동적 재배치 | 고정 salgy ET_EXEC, 자체 ABI note |
| programma_programma_paneli | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS 거부 |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 Faýl·루프백·GUI SVC와 협력식 세션 |
| ýat_maglumat | VM·GC·klas_baha·코드 캐시의 동적 salgy 공간 | ulanyjy 영역 16 MiB, düz_surat 영역 12 MiB |
| Faýl | 큰 `lib/modules`, 공유 Kitaphana 및 maglumat | RAM Faýl 하나당 16 KiB, 영속 Store_baha 없음 |
| Java klas_baha | OpenJDK 25 class 버전 69 | 자체 JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·şrift_baha·penjire 시스템 | 별도로 구현한 Swing API 부분집합 |

hakyky_maglumat ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 현재 제한은
[ELF 로더](../platforms/rpi4-native/kompýuter/ulanyjy.c),
[salgy 공간 Kesgitleme_baha](../platforms/rpi4-native/kompýuter/ulanyjy.h),
[RAM Faýl 구현](../platforms/rpi4-native/Çeşme/ýat_Faýllar.java),
[ulanyjy ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 수 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM Faýl 업로드 제한을 피하지만,
OpenJDK에 필요한 salgy 공간·스레드·동적 Birikme 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 operasiýa_ulgamy 호출·ýat_maglumat·동적 Birikme 규약까지 맞지는 않는다.
Faýl Ululyk 제한이나 ELF format_baha 검사만 풀어도 해결되는 문제가 아니다.

## 자체 커널을 유지하면서 이식하는 tapgyr_baha

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 operasiýa_ulgamy ABI를 갖춘 ulanyjy 프로그램으로 실행할 수 있다.

기술적으로는 새 운영체제용 OpenJDK 포트 또는 충분한 Linux ulanyjy ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 현재 코드와 hakyky_maglumat 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **operasiýa_ulgamy ABI와 libc 기반**: 큰 Faýl·salgy 공간, 페이지 예약/확정/해제와 gora_baha üýtget_baha,
   표준 Faýl/sagat 인터페이스, Hata indeks·C 런타임·niýet sysroot를 구현한다.
2. **hakyky_maglumat 네이티브 스레드와 sinhronlaşdyr**: pthread에 대응하는 스케줄링·TLS·뮤텍스·şert 변수,
   원자 amal_baha·ýat_maglumat tertip_baha·중단/깨우기, 신호/예외 문맥과 가드 페이지를 제공한다.
   현재 vi/Swing의 입력 대기에서 문맥을 보관하는 기능만으로 대체할 수 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 Kitaphana·TLS 또는 이식에 맞는 statiki_baha Birikme,
   JVM 네이티브 nyşan 해결, 영속 Faýl 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS 포트**: düz_ulgam 시스템과 `src/hotspot/os`, `os_cpu`에 자체 OS/AArch64 경계를
   구현한다. 기존 AArch64 buýruk 생성기는 재사용할 수 있지만 OS 종속부를 구현해야 한다.
   첫 ýerine_ýetir_buýruk 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **klas_baha Kitaphana·javac**: java.base의 JNI/Faýl/네트워크/프로세스 연결과 모듈 적재를
   구현한 Yza_baha 자체 ýadro_baha 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 외부 네트워크**: AWT/Java2D의 penjire·입력·şrift_baha 백엔드와 hakyky_maglumat NIC/TCP/IP를
   이식한다. 현재 자체 Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **tassykla**: 단계별 OS ABI 시험, OpenJDK jtreg 시험, GUI/한글/네트워크 부하 시험,
   hakyky_maglumat Pi4 검증을 수행한다. 일부 시험 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK 코드:
[POSIX ýat_maglumat·OS 구현](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 경계](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·ýat_maglumat Proses_baha_girizmeklik](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

자체 Java AOT 자체를 OpenJDK의 Java 코드 전체를 처리하도록 확장하는 경로도 별도 개발이다.
obýekt_baha 모델·가상/인터페이스 호출·예외·GC·long/float/double·모든 ARRAY_baha·sinhronlaşdyr·동적 호출·
klas_baha ulanyşa_taýýarla/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
