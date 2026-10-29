# OpenJDK kilde_træ 빌드와 eget Java kerne_VÆRDI 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 eget 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 eget Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## kompilere_kilde 경로의 afgrænser_VÆRDI

| mål | 입력과 KR | Udfør_kommando lidelse |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → eget x86 AOT → ELF32 | 해당 CPU·eget ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | eget ARM64 kerne_VÆRDI/bruger ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 kilde_træ → 공식 configure/make → JDK build_Image | **build_System mål OS/CPU의 Udfør_kommando kontraktværdi** |

OpenJDK는 Java Fil 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Tilslut,
Hold_VÆRDI 라이브러리의 C/C++ 구현, app_Kvikstart, modul_VÆRDI build_Image 및 generere 도구를 함께 빌드한다.
따라서 eget AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK build_System 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## kilde_træ build_System Kommando

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ compiler·Autoconf·Make와
udvikling 헤더를 준비한다. Swing/AWT의 Linux bibliotek 빌드에는 X11·skrifttype_VÆRDI 등의
udvikling 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/compiler.py --target openjdk-build \
  --java-home /Sti/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /Sti/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 kilde_træ 트리 밖의 전용 build_System 디렉터리다.
kilde_træ·build_System·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 build_System 디렉터리는 재실행할 tal 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI bibliotek
- `jkoros-openjdk-build.json`: fase_VÆRDI·Kommando·kilde_træ 식별 hash_fil·성공/fejl_VÆRDI·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 LOG_VÆRDI

실패하면 Afslut_app 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 build_System 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
kilde_træ 빌드만으로 eget kerne_VÆRDI Udfør_kommando 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **mål libc/헤더/bibliotek**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/compiler.py --target openjdk-build \
  --java-home /Sti/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /Sti/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /Sti/OpenJDK소스
```

부트 JDK는 build_System 호스트에서 실행된다. 교차 build_System 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## aktuel_vare 작업 공간의 bekræfte_5fb2b747 data

Analyse_VÆRDI To_do_rod 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[kilde_træ 출처와 다운로드 hash_fil](build/openjdk-port/source.json)를 보관한다.
build_System 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 build_System 호스트용이며 eget kerne_VÆRDI 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac Udfør_kommando 시험을 통과했다. 기존 compiler 회귀 시험과 새 build_System Sti 시험도
총 **25개 videregive_VÆRDI**했다. 공식 distribution_VÆRDI 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 bekræfte_5fb2b747 LOG_post](build/openjdk-port/verification.json)은 build_System 산출물과 Udfør_kommando 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[build_System LOG_post](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[Udfør_kommando 시험](build/openjdk-port/smoke/report.json)을 각각 확인한다.
Udfør_kommando 시험은 새로 빌드한 java/javac로 한글 kilde_træ, long/double, UTF-8 Fil,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 faktisk_data JFrame skærmbillede 시험을 뜻하지 않는다.
Linux에서 한 시험이 eget kerne_VÆRDI 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

aktuel_vare 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 tal 없으며, 준비한 musl miljø 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 Næste_vare 단축 명령으로 같은 musl 환경을 사용한다.
bruger·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 kilde_træ/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 tal 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 aktuel_vare 디렉터리를 유지하므로, 한글 소스도 peer_VÆRDI 경로로
컴파일하고 실행할 tal 있다. 예를 들어 앞의 시험에서 생성한 소스를 prøve_igen_VÆRDI 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/oprindelig_build_test.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke oprindelig_build_test
```

## 기존 ARM64 OpenJDK를 eget 커널에 복사할 tal 있는가

현재는 실행할 tal 없다. 저장되어 있는 ARM64 OpenJDK 25의 statisk_VÆRDI 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 Udfør_kommando 파일을 **실행하지 않고** ELF와 동적 symbol·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

eget 커널에 직접 적재할 tal 없으면 검사 결과를 저장한 BACK_VÆRDI **Afslut_app KODE_VÆRDI 3**을 반환한다.
ELF 호환성 검사는 faktisk_data kerne_VÆRDI 로더의 모든 검증을 대체하지 않는다.

| 확인한 lidelse | ARM64 OpenJDK | aktuel_vare eget kerne_VÆRDI |
|---|---|---|
| ELF | PIE/공유 bibliotek, 동적 재배치 | 고정 mail ET_EXEC, eget ABI note |
| app_Kvikstart | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS afvise_VÆRDI |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 Fil·루프백·GUI SVC와 협력식 세션 |
| Hukommelse_data | VM·GC·Hold_VÆRDI·KODE_VÆRDI 캐시의 동적 mail mail_område | bruger område_VÆRDI_0e9a97ab 16 MiB, build_Image område_VÆRDI_0e9a97ab 12 MiB |
| Fil | 큰 `lib/modules`, 공유 bibliotek 및 data | RAM Fil 하나당 16 KiB, 영속 Store_VÆRDI 없음 |
| Java Hold_VÆRDI | OpenJDK 25 class 버전 69 | eget JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·skrifttype_VÆRDI·Vindue 시스템 | 별도로 구현한 Swing API 부분집합 |

faktisk_data ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 aktuel_vare 제한은
[ELF 로더](../platforms/rpi4-native/maskine/bruger.c),
[mail mail_område Definition_VÆRDI](../platforms/rpi4-native/maskine/bruger.h),
[RAM Fil 구현](../platforms/rpi4-native/KILDE/Hukommelse_Filer.java),
[bruger ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 tal 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM Fil 업로드 제한을 피하지만,
OpenJDK에 필요한 mail mail_område·스레드·동적 Tilslut 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 operativsystem 호출·Hukommelse_data·동적 Tilslut 규약까지 맞지는 않는다.
Fil Størrelse 제한이나 ELF format_VÆRDI 검사만 풀어도 해결되는 문제가 아니다.

## eget 커널을 유지하면서 이식하는 fase_VÆRDI

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 operativsystem ABI를 갖춘 bruger 프로그램으로 실행할 tal 있다.

기술적으로는 새 운영체제용 OpenJDK hardware_port 또는 충분한 Linux bruger ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 aktuel_vare 코드와 faktisk_data 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **operativsystem ABI와 libc 기반**: 큰 Fil·mail mail_område, 페이지 예약/udføre_VÆRDI/해제와 beskytte_VÆRDI ændre_VÆRDI,
   표준 Fil/Ur 인터페이스, fejl INDEKS·C 런타임·mål sysroot를 구현한다.
2. **faktisk_data 네이티브 스레드와 synkronisere**: pthread에 대응하는 스케줄링·TLS·뮤텍스·lidelse variabel_VÆRDI,
   원자 kirurgi_VÆRDI·Hukommelse_data ordre_VÆRDI·중단/깨우기, 신호/undtagelse 문맥과 가드 페이지를 제공한다.
   aktuel_vare vi/Swing의 input_VÆRDI 대기에서 문맥을 보관하는 기능만으로 대체할 tal 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 bibliotek·TLS 또는 이식에 맞는 statisk_VÆRDI Tilslut,
   JVM 네이티브 symbol 해결, 영속 Fil 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS hardware_port**: build_System 시스템과 `src/hotspot/os`, `os_cpu`에 eget OS/AArch64 경계를
   구현한다. 기존 AArch64 Kommando 생성기는 재사용할 tal 있지만 OS 종속부를 구현해야 한다.
   첫 Udfør_kommando 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **Hold_VÆRDI bibliotek·javac**: java.base의 JNI/Fil/네트워크/프로세스 연결과 modul_VÆRDI 적재를
   구현한 BACK_VÆRDI eget kerne_VÆRDI 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 ekstern_VÆRDI 네트워크**: AWT/Java2D의 Vindue·input_VÆRDI·skrifttype_VÆRDI 백엔드와 faktisk_data NIC/TCP/IP를
   이식한다. aktuel_vare eget Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **bekræfte_5fb2b747**: 단계별 OS ABI 시험, OpenJDK jtreg 시험, GUI/한글/네트워크 부하 시험,
   faktisk_data Pi4 검증을 수행한다. 일부 시험 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK KODE_VÆRDI:
[POSIX Hukommelse_data·OS 구현](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS grænse_VÆRDI](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·Hukommelse_data Proces_VÆRDI_post](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

eget Java AOT 자체를 OpenJDK의 Java KODE_VÆRDI 전체를 처리하도록 확장하는 경로도 별도 개발이다.
objekt_VÆRDI 모델·가상/인터페이스 호출·undtagelse·GC·long/float/double·모든 MATRIX_VÆRDI·synkronisere·동적 호출·
Hold_VÆRDI starte/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
