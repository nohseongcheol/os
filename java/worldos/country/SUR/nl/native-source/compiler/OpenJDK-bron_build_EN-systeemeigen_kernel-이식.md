# OpenJDK bron_structuur 빌드와 Eigen Java kernel_WAARDE 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 Eigen 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 Eigen Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## compileren_bron 경로의 scheidingsteken_WAARDE

| doel | 입력과 resultaat | Uitvoeren_opdracht toestand |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → Eigen x86 AOT → ELF32 | 해당 CPU·Eigen ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | Eigen ARM64 kernel_WAARDE/gebruikersruimte ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 bron_structuur → 공식 configure/make → JDK build_kopie | **bouwen doel OS/CPU의 Uitvoeren_opdracht contractwaarde** |

OpenJDK는 Java bestand 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Verbinden,
les_WAARDE 라이브러리의 C/C++ implementatie, app_app_lade, module_WAARDE build_kopie 및 genereren 도구를 함께 빌드한다.
따라서 Eigen AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK bouwen Guides](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## bron_structuur bouwen opdracht

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ compiler·Autoconf·Make와
ontwikkeling 헤더를 준비한다. Swing/AWT의 Linux bibliotheek 빌드에는 X11·lettertype_WAARDE 등의
ontwikkeling 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/compiler.py --target openjdk-build \
  --java-home /pad/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /pad/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 bron_structuur 트리 밖의 전용 bouwen 디렉터리다.
bron_structuur·bouwen·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 bouwen 디렉터리는 재실행할 nummer 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI bibliotheek
- `jkoros-openjdk-build.json`: fase_WAARDE·opdracht·bron_structuur 식별 hash_Bestand·성공/fout_WAARDE·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 LOG_WAARDE

실패하면 Einde_app 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 bouwen 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
bron_structuur 빌드만으로 Eigen kernel_WAARDE Uitvoeren_opdracht 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **doel libc/헤더/bibliotheek**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/compiler.py --target openjdk-build \
  --java-home /pad/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /pad/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /pad/OpenJDK소스
```

부트 JDK는 bouwen 호스트에서 실행된다. 교차 bouwen 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## actueel_item 작업 공간의 valideren gegevens

Analyseren_WAARDE Taken_wortel 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[bron_structuur 출처와 다운로드 hash_Bestand](build/openjdk-port/source.json)를 보관한다.
bouwen 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 bouwen 호스트용이며 Eigen kernel_WAARDE 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac Uitvoeren_opdracht 시험을 통과했다. 기존 compiler 회귀 시험과 새 bouwen pad 시험도
총 **25개 doorgeven_WAARDE**했다. 공식 distributie_WAARDE 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 valideren LOG_RECORD](build/openjdk-port/verification.json)은 bouwen 산출물과 Uitvoeren_opdracht 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[bouwen LOG_RECORD](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[Uitvoeren_opdracht tests](build/openjdk-port/smoke/report.json)을 각각 확인한다.
Uitvoeren_opdracht 시험은 새로 빌드한 java/javac로 한글 bron_structuur, long/double, UTF-8 bestand,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 werkelijk_gegevens JFrame scherm 시험을 뜻하지 않는다.
Linux에서 한 시험이 Eigen kernel_WAARDE 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

actueel_item 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 nummer 없으며, 준비한 musl omgeving 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 Volgende_item 단축 명령으로 같은 musl 환경을 사용한다.
gebruikersruimte·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 bron_structuur/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 nummer 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 actueel_item 디렉터리를 유지하므로, 한글 소스도 peer_WAARDE 경로로
컴파일하고 실행할 nummer 있다. 예를 들어 앞의 시험에서 생성한 소스를 opnieuw_proberen_WAARDE 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/systeemeigen_build_test.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke systeemeigen_build_test
```

## 기존 ARM64 OpenJDK를 Eigen 커널에 복사할 nummer 있는가

현재는 실행할 nummer 없다. 저장되어 있는 ARM64 OpenJDK 25의 statisch_WAARDE 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 Uitvoeren_opdracht 파일을 **실행하지 않고** ELF와 동적 symbool·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

Eigen 커널에 직접 적재할 nummer 없으면 검사 결과를 저장한 BACK_WAARDE **Einde_app CODE_WAARDE 3**을 반환한다.
ELF 호환성 검사는 werkelijk_gegevens kernel_WAARDE 로더의 모든 검증을 대체하지 않는다.

| 확인한 toestand | ARM64 OpenJDK | actueel_item Eigen kernel_WAARDE |
|---|---|---|
| ELF | PIE/공유 bibliotheek, 동적 재배치 | 고정 ADRES ET_EXEC, Eigen ABI note |
| app_app_lade | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS weigeren_WAARDE |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 bestand·루프백·GUI SVC와 협력식 세션 |
| Geheugen_gegevens | VM·GC·les_WAARDE·CODE_WAARDE 캐시의 동적 ADRES ADRES_regio | gebruikersruimte regio_WAARDE 16 MiB, build_kopie regio_WAARDE 12 MiB |
| bestand | 큰 `lib/modules`, 공유 bibliotheek 및 gegevens | RAM bestand 하나당 16 KiB, 영속 Store_WAARDE 없음 |
| Java les_WAARDE | OpenJDK 25 class 버전 69 | Eigen JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·lettertype_WAARDE·Venster 시스템 | 별도로 구현한 Swing API 부분집합 |

werkelijk_gegevens ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 actueel_item 제한은
[ELF 로더](../platforms/rpi4-native/machine/gebruikersruimte.c),
[ADRES ADRES_regio Definitie_WAARDE](../platforms/rpi4-native/machine/gebruikersruimte.h),
[RAM bestand implementatie](../platforms/rpi4-native/broncode/GeheugenBestanden.java),
[gebruikersruimte ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 nummer 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM bestand 업로드 제한을 피하지만,
OpenJDK에 필요한 ADRES ADRES_regio·스레드·동적 Verbinden 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 besturingssysteem 호출·Geheugen_gegevens·동적 Verbinden 규약까지 맞지는 않는다.
bestand Grootte 제한이나 ELF opmaak_WAARDE 검사만 풀어도 해결되는 문제가 아니다.

## Eigen 커널을 유지하면서 이식하는 fase_WAARDE

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 besturingssysteem ABI를 갖춘 gebruikersruimte 프로그램으로 실행할 nummer 있다.

기술적으로는 새 운영체제용 OpenJDK hardware_poort 또는 충분한 Linux gebruikersruimte ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 actueel_item 코드와 werkelijk_gegevens 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **besturingssysteem ABI와 libc 기반**: 큰 bestand·ADRES ADRES_regio, 페이지 예약/doorvoeren_WAARDE/해제와 beschermen_WAARDE wijzigen_WAARDE,
   표준 bestand/Klok 인터페이스, fout INDEX·C 런타임·doel sysroot를 구현한다.
2. **werkelijk_gegevens 네이티브 스레드와 synchroniseren**: pthread에 대응하는 스케줄링·TLS·뮤텍스·toestand variabele_WAARDE,
   원자 operatie_WAARDE·Geheugen_gegevens order_WAARDE·중단/깨우기, 신호/uitzondering 문맥과 가드 페이지를 제공한다.
   actueel_item vi/Swing의 invoer_WAARDE 대기에서 문맥을 보관하는 기능만으로 대체할 nummer 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 bibliotheek·TLS 또는 이식에 맞는 statisch_WAARDE Verbinden,
   JVM 네이티브 symbool 해결, 영속 bestand 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS hardware_poort**: bouwen 시스템과 `src/hotspot/os`, `os_cpu`에 Eigen OS/AArch64 경계를
   구현한다. 기존 AArch64 opdracht 생성기는 재사용할 nummer 있지만 OS 종속부를 구현해야 한다.
   첫 Uitvoeren_opdracht 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **les_WAARDE bibliotheek·javac**: java.base의 JNI/bestand/네트워크/프로세스 연결과 module_WAARDE 적재를
   구현한 BACK_WAARDE Eigen kernel_WAARDE 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 extern_WAARDE 네트워크**: AWT/Java2D의 Venster·invoer_WAARDE·lettertype_WAARDE 백엔드와 werkelijk_gegevens NIC/TCP/IP를
   이식한다. actueel_item Eigen Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **valideren**: 단계별 OS ABI tests, OpenJDK jtreg tests, GUI/한글/네트워크 부하 tests,
   werkelijk_gegevens Pi4 검증을 수행한다. 일부 tests 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK CODE_WAARDE:
[POSIX Geheugen_gegevens·OS implementatie](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS grens_WAARDE](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·Geheugen_gegevens Proces_WAARDE_invoer](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

Eigen Java AOT 자체를 OpenJDK의 Java CODE_WAARDE 전체를 처리하도록 확장하는 경로도 별도 개발이다.
object_WAARDE 모델·가상/인터페이스 호출·uitzondering·GC·long/float/double·모든 MATRIX_WAARDE·synchroniseren·동적 호출·
les_WAARDE initialiseren/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
