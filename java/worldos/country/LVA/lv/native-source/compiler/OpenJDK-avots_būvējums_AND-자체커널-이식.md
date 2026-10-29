# OpenJDK avots_koks 빌드와 savs Java kodols_VALUE 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 savs 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 savs Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## kompilēt_avots 경로의 norobežotājs_VALUE

| mērķis | 입력과 mērs | Izpildīt_komanda nosacījums |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → savs x86 AOT → ELF32 | 해당 CPU·savs ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | savs ARM64 kodols_VALUE/lietotājs ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 avots_koks → 공식 configure/make → JDK būvējums_IMAGE | **būvējums_sistēma mērķis OS/CPU의 Izpildīt_komanda līguma_vērtība** |

OpenJDK는 Java Fails 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Savienoties,
klase_VALUE 라이브러리의 C/C++ 구현, programma_palaidējs, modulis_VALUE būvējums_IMAGE 및 ģenerēt 도구를 함께 빌드한다.
따라서 savs AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK būvējums_sistēma 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## avots_koks būvējums_sistēma Komanda

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ kompilators·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux bibliotēka 빌드에는 X11·fonts_VALUE 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/kompilators.py --target openjdk-build \
  --java-home /CEĻŠ/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /CEĻŠ/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 avots_koks 트리 밖의 전용 būvējums_sistēma 디렉터리다.
avots_koks·būvējums_sistēma·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 būvējums_sistēma 디렉터리는 재실행할 numurs 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI bibliotēka
- `jkoros-openjdk-build.json`: posms_VALUE·Komanda·avots_koks 식별 jaukšana_Fails·성공/kļūme_VALUE·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 LOG_VALUE

실패하면 Iziet_programma 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 būvējums_sistēma 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
avots_koks 빌드만으로 savs kodols_VALUE Izpildīt_komanda 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **mērķis libc/헤더/bibliotēka**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/kompilators.py --target openjdk-build \
  --java-home /CEĻŠ/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /CEĻŠ/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /CEĻŠ/OpenJDK소스
```

부트 JDK는 būvējums_sistēma 호스트에서 실행된다. 교차 būvējums_sistēma 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## pašreizējais_krājums 작업 공간의 validēt dati

analīze_VALUE Project_sakne 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[avots_koks 출처와 다운로드 jaukšana_Fails](build/openjdk-port/source.json)를 보관한다.
būvējums_sistēma 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 būvējums_sistēma 호스트용이며 savs kodols_VALUE 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac Izpildīt_komanda 시험을 통과했다. 기존 kompilators 회귀 시험과 새 būvējums_sistēma CEĻŠ 시험도
총 **25개 padot_VALUE**했다. 공식 sadale_VALUE 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 validēt LOG_RECORD](build/openjdk-port/verification.json)은 būvējums_sistēma 산출물과 Izpildīt_komanda 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[būvējums_sistēma LOG_RECORD](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[Izpildīt_komanda 시험](build/openjdk-port/smoke/report.json)을 각각 확인한다.
Izpildīt_komanda 시험은 새로 빌드한 java/javac로 한글 avots_koks, long/double, UTF-8 Fails,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 faktisks_dati JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 savs kodols_VALUE 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

pašreizējais_krājums 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 numurs 없으며, 준비한 musl 환경 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 Tālāk_krājums 단축 명령으로 같은 musl 환경을 사용한다.
lietotājs·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 avots_koks/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 numurs 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 pašreizējais_krājums 디렉터리를 유지하므로, 한글 소스도 vienranga_VALUE 경로로
컴파일하고 실행할 numurs 있다. 예를 들어 앞의 시험에서 생성한 소스를 mēģināt_vēlreiz_VALUE 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/자체빌드시험.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 자체빌드시험
```

## 기존 ARM64 OpenJDK를 savs 커널에 복사할 numurs 있는가

현재는 실행할 numurs 없다. 저장되어 있는 ARM64 OpenJDK 25의 정적 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 Izpildīt_komanda 파일을 **실행하지 않고** ELF와 동적 simbols·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

savs 커널에 직접 적재할 numurs 없으면 검사 결과를 저장한 ATPAKAĻ_VALUE **Iziet_programma CODE_VALUE 3**을 반환한다.
ELF 호환성 검사는 faktisks_dati kodols_VALUE 로더의 모든 검증을 대체하지 않는다.

| 확인한 nosacījums | ARM64 OpenJDK | pašreizējais_krājums savs kodols_VALUE |
|---|---|---|
| ELF | PIE/공유 bibliotēka, 동적 재배치 | 고정 adrese ET_EXEC, savs ABI note |
| programma_palaidējs | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS noraidīt_VALUE |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 Fails·루프백·GUI SVC와 협력식 세션 |
| atmiņa_dati | VM·GC·klase_VALUE·CODE_VALUE 캐시의 동적 adrese adrese_reģions | lietotājs reģions_VALUE 16 MiB, būvējums_IMAGE reģions_VALUE 12 MiB |
| Fails | 큰 `lib/modules`, 공유 bibliotēka 및 dati | RAM Fails 하나당 16 KiB, 영속 Store_VALUE 없음 |
| Java klase_VALUE | OpenJDK 25 class 버전 69 | savs JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·fonts_VALUE·Logs 시스템 | 별도로 구현한 Swing API 부분집합 |

faktisks_dati ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 pašreizējais_krājums 제한은
[ELF 로더](../platforms/rpi4-native/mašīna/lietotājs.c),
[adrese adrese_reģions definīcija_VALUE](../platforms/rpi4-native/mašīna/lietotājs.h),
[RAM Fails 구현](../platforms/rpi4-native/AVOTS/atmiņa_Faili.java),
[lietotājs ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 numurs 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM Fails 업로드 제한을 피하지만,
OpenJDK에 필요한 adrese adrese_reģions·스레드·동적 Savienoties 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 operētājsistēma 호출·atmiņa_dati·동적 Savienoties 규약까지 맞지는 않는다.
Fails Izmērs 제한이나 ELF formāts_VALUE 검사만 풀어도 해결되는 문제가 아니다.

## savs 커널을 유지하면서 이식하는 posms_VALUE

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 operētājsistēma ABI를 갖춘 lietotājs 프로그램으로 실행할 numurs 있다.

기술적으로는 새 운영체제용 OpenJDK 포트 또는 충분한 Linux lietotājs ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 pašreizējais_krājums 코드와 faktisks_dati 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **operētājsistēma ABI와 libc 기반**: 큰 Fails·adrese adrese_reģions, 페이지 예약/izpilde_VALUE/해제와 aizsargāt_VALUE mainīt_VALUE,
   표준 Fails/Pulkstenis 인터페이스, Kļūda INDEX·C 런타임·mērķis sysroot를 구현한다.
2. **faktisks_dati 네이티브 스레드와 sinhronizēt**: pthread에 대응하는 스케줄링·TLS·뮤텍스·nosacījums mainīgais_VALUE,
   원자 operācija_VALUE·atmiņa_dati secība_VALUE·중단/깨우기, 신호/izņēmums 문맥과 가드 페이지를 제공한다.
   pašreizējais_krājums vi/Swing의 입력 대기에서 문맥을 보관하는 기능만으로 대체할 numurs 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 bibliotēka·TLS 또는 이식에 맞는 정적 Savienoties,
   JVM 네이티브 simbols 해결, 영속 Fails 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS 포트**: būvējums_sistēma 시스템과 `src/hotspot/os`, `os_cpu`에 savs OS/AArch64 경계를
   구현한다. 기존 AArch64 Komanda 생성기는 재사용할 numurs 있지만 OS 종속부를 구현해야 한다.
   첫 Izpildīt_komanda 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **klase_VALUE bibliotēka·javac**: java.base의 JNI/Fails/네트워크/프로세스 연결과 modulis_VALUE 적재를
   구현한 ATPAKAĻ_VALUE savs kodols_VALUE 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 ārējs_VALUE 네트워크**: AWT/Java2D의 Logs·입력·fonts_VALUE 백엔드와 faktisks_dati NIC/TCP/IP를
   이식한다. pašreizējais_krājums savs Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **validēt**: 단계별 OS ABI 시험, OpenJDK jtreg 시험, GUI/한글/네트워크 부하 시험,
   faktisks_dati Pi4 검증을 수행한다. 일부 시험 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK CODE_VALUE:
[POSIX atmiņa_dati·OS 구현](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 경계](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·atmiņa_dati Process_VALUE_ievade](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

savs Java AOT 자체를 OpenJDK의 Java CODE_VALUE 전체를 처리하도록 확장하는 경로도 별도 개발이다.
objekts_VALUE 모델·가상/인터페이스 호출·izņēmums·GC·long/float/double·모든 ARRAY_VALUE·sinhronizēt·동적 호출·
klase_VALUE 초기화/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
