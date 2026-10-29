# OpenJDK lähde_puu 빌드와 oma Java ydin_ARVO 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 oma 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 oma Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## kääntää_lähde 경로의 erotin_ARVO_d8ba4873

| tavoite | 입력과 TULOS | Suorita_komento ehto |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → oma x86 AOT → ELF32 | 해당 CPU·oma ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | oma ARM64 ydin_ARVO/käyttäjätila ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 lähde_puu → 공식 configure/make → JDK kääntää_KUVA | **kääntää_Järjestelmä tavoite OS/CPU의 Suorita_komento sopimuksen_arvo** |

OpenJDK는 Java tiedoston_nimi 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Yhdistä,
Luokka_ARVO 라이브러리의 C/C++ toteutus, ohjelma_sovellusvalikko, moduuli_ARVO kääntää_KUVA 및 generoida 도구를 함께 빌드한다.
따라서 oma AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK kääntää_Järjestelmä 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## lähde_puu kääntää_Järjestelmä komento

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ kääntäjä·Autoconf·Make와
kehitystuote 헤더를 준비한다. Swing/AWT의 Linux kirjasto 빌드에는 X11·fontti_ARVO 등의
kehitystuote 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/kääntäjä.py --target openjdk-build \
  --java-home /polku_2/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /polku_2/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 lähde_puu 트리 밖의 전용 kääntää_Järjestelmä 디렉터리다.
lähde_puu·kääntää_Järjestelmä·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 kääntää_Järjestelmä 디렉터리는 재실행할 numero 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI kirjasto
- `jkoros-openjdk-build.json`: vaihe_ARVO·komento·lähde_puu 식별 hajautusarvo_Tiedosto·성공/virhe_ARVO·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 LOG_ARVO

실패하면 Lopeta_ohjelma 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 kääntää_Järjestelmä 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
lähde_puu 빌드만으로 oma ydin_ARVO Suorita_komento 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **tavoite libc/헤더/kirjasto**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/kääntäjä.py --target openjdk-build \
  --java-home /polku_2/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /polku_2/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /polku_2/OpenJDK소스
```

부트 JDK는 kääntää_Järjestelmä 호스트에서 실행된다. 교차 kääntää_Järjestelmä 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## nykyinen_kohde 작업 공간의 vahvista data

Analysoi_ARVO aloite_juuri 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[lähde_puu 출처와 다운로드 hajautusarvo_Tiedosto](build/openjdk-port/source.json)를 보관한다.
kääntää_Järjestelmä 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 kääntää_Järjestelmä 호스트용이며 oma ydin_ARVO 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac Suorita_komento 시험을 통과했다. 기존 kääntäjä 회귀 시험과 새 kääntää_Järjestelmä polku_2 시험도
총 **25개 välittää_ARVO**했다. 공식 jakelu_ARVO 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 vahvista LOG_TIETUE](build/openjdk-port/verification.json)은 kääntää_Järjestelmä 산출물과 Suorita_komento 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[kääntää_Järjestelmä LOG_TIETUE](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[Suorita_komento testit](build/openjdk-port/smoke/report.json)을 각각 확인한다.
Suorita_komento 시험은 새로 빌드한 java/javac로 한글 lähde_puu, long/double, UTF-8 tiedoston_nimi,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 todellinen_data JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 oma ydin_ARVO 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

nykyinen_kohde 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 numero 없으며, 준비한 musl ympäristö 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 Seuraava_kohde 단축 명령으로 같은 musl 환경을 사용한다.
käyttäjätila·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 lähde_puu/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 numero 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 nykyinen_kohde 디렉터리를 유지하므로, 한글 소스도 vertaissolmu_ARVO 경로로
컴파일하고 실행할 numero 있다. 예를 들어 앞의 시험에서 생성한 소스를 yrittää_uudelleen_ARVO 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/alkuperäinen_kääntää_testi.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke alkuperäinen_kääntää_testi
```

## 기존 ARM64 OpenJDK를 oma 커널에 복사할 numero 있는가

현재는 실행할 numero 없다. 저장되어 있는 ARM64 OpenJDK 25의 staattinen_ARVO 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 Suorita_komento 파일을 **실행하지 않고** ELF와 동적 symboli·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

oma 커널에 직접 적재할 numero 없으면 검사 결과를 저장한 BACK_ARVO **Lopeta_ohjelma KOODI_ARVO 3**을 반환한다.
ELF 호환성 검사는 todellinen_data ydin_ARVO 로더의 모든 검증을 대체하지 않는다.

| 확인한 ehto | ARM64 OpenJDK | nykyinen_kohde oma ydin_ARVO |
|---|---|---|
| ELF | PIE/공유 kirjasto, 동적 재배치 | 고정 OSOITE ET_EXEC, oma ABI note |
| ohjelma_sovellusvalikko | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS hylkää_ARVO_e3ecc00b |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 tiedoston_nimi·루프백·GUI SVC와 협력식 세션 |
| Muisti_data | VM·GC·Luokka_ARVO·KOODI_ARVO 캐시의 동적 OSOITE OSOITE_alue | käyttäjätila alue_ARVO_0e9a97ab 16 MiB, kääntää_KUVA alue_ARVO_0e9a97ab 12 MiB |
| tiedoston_nimi | 큰 `lib/modules`, 공유 kirjasto 및 data | RAM tiedoston_nimi 하나당 16 KiB, 영속 Store_ARVO 없음 |
| Java Luokka_ARVO | OpenJDK 25 class 버전 69 | oma JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·fontti_ARVO·Ikkuna 시스템 | 별도로 구현한 Swing API 부분집합 |

todellinen_data ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 nykyinen_kohde 제한은
[ELF 로더](../platforms/rpi4-native/kone/käyttäjätila.c),
[OSOITE OSOITE_alue Määritelmä_ARVO](../platforms/rpi4-native/kone/käyttäjätila.h),
[RAM tiedoston_nimi toteutus](../platforms/rpi4-native/lähdetiedosto/Muisti_Files.java),
[käyttäjätila ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 numero 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM tiedoston_nimi 업로드 제한을 피하지만,
OpenJDK에 필요한 OSOITE OSOITE_alue·스레드·동적 Yhdistä 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 käyttöjärjestelmä 호출·Muisti_data·동적 Yhdistä 규약까지 맞지는 않는다.
tiedoston_nimi Koko 제한이나 ELF muoto_ARVO 검사만 풀어도 해결되는 문제가 아니다.

## oma 커널을 유지하면서 이식하는 vaihe_ARVO

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 käyttöjärjestelmä ABI를 갖춘 käyttäjätila 프로그램으로 실행할 numero 있다.

기술적으로는 새 운영체제용 OpenJDK laitteisto_portti 또는 충분한 Linux käyttäjätila ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 nykyinen_kohde 코드와 todellinen_data 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **käyttöjärjestelmä ABI와 libc 기반**: 큰 tiedoston_nimi·OSOITE OSOITE_alue, 페이지 예약/vahvistaa_muutokset_ARVO/해제와 suojata_ARVO muuttaa_ARVO,
   표준 tiedoston_nimi/Kello 인터페이스, VIRHE INDEKSI·C 런타임·tavoite sysroot를 구현한다.
2. **todellinen_data 네이티브 스레드와 synkronoi**: pthread에 대응하는 스케줄링·TLS·뮤텍스·ehto muuttuja_ARVO,
   원자 leikkaus_ARVO·Muisti_data tilata_ARVO·중단/깨우기, 신호/poikkeus 문맥과 가드 페이지를 제공한다.
   nykyinen_kohde vi/Swing의 syöte_ARVO 대기에서 문맥을 보관하는 기능만으로 대체할 numero 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 kirjasto·TLS 또는 이식에 맞는 staattinen_ARVO Yhdistä,
   JVM 네이티브 symboli 해결, 영속 tiedoston_nimi 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS laitteisto_portti**: kääntää_Järjestelmä 시스템과 `src/hotspot/os`, `os_cpu`에 oma OS/AArch64 경계를
   구현한다. 기존 AArch64 komento 생성기는 재사용할 numero 있지만 OS 종속부를 구현해야 한다.
   첫 Suorita_komento 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **Luokka_ARVO kirjasto·javac**: java.base의 JNI/tiedoston_nimi/네트워크/프로세스 연결과 moduuli_ARVO 적재를
   구현한 BACK_ARVO oma ydin_ARVO 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 ulkoinen_ARVO 네트워크**: AWT/Java2D의 Ikkuna·syöte_ARVO·fontti_ARVO 백엔드와 todellinen_data NIC/TCP/IP를
   이식한다. nykyinen_kohde oma Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **vahvista**: 단계별 OS ABI testit, OpenJDK jtreg testit, GUI/한글/네트워크 부하 testit,
   todellinen_data Pi4 검증을 수행한다. 일부 testit 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK KOODI_ARVO:
[POSIX Muisti_data·OS toteutus](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS rajattu_alue_ARVO](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·Muisti_data prosessi_ARVO_merkintä](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

oma Java AOT 자체를 OpenJDK의 Java KOODI_ARVO 전체를 처리하도록 확장하는 경로도 별도 개발이다.
objekti_ARVO 모델·가상/인터페이스 호출·poikkeus·GC·long/float/double·모든 MATRIISI_ARVO·synkronoi·동적 호출·
Luokka_ARVO alustaa/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
