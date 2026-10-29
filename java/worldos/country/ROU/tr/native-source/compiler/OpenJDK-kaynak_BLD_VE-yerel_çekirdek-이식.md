# OpenJDK kaynak_ağaç 빌드와 Öz Java çekirdek_değer 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 Öz 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 Öz Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## derlemek_kaynak 경로의 sınırlayıcı_değer

| hedef | 입력과 sonuç | yürütmek_komut koşul |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → Öz x86 AOT → ELF32 | 해당 CPU·Öz ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | Öz ARM64 çekirdek_değer/kullanıcı_alanı ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 kaynak_ağaç → 공식 configure/make → JDK BLD_RESİM | **oluştur hedef OS/CPU의 yürütmek_komut sözleşme_değeri** |

OpenJDK는 Java dosya 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Bağlan,
Sınıf_değer 라이브러리의 C/C++ gerçekleme, program_Launcher, modül_değer BLD_RESİM 및 oluşturmak 도구를 함께 빌드한다.
따라서 Öz AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK oluştur 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## kaynak_ağaç oluştur komut

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ derleyici·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux kitaplık 빌드에는 X11·yazı_tipi_değer 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/derleyici.py --target openjdk-build \
  --java-home /yol/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /yol/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 kaynak_ağaç 트리 밖의 전용 oluştur 디렉터리다.
kaynak_ağaç·oluştur·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 oluştur 디렉터리는 재실행할 수 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI kitaplık
- `jkoros-openjdk-build.json`: aşama_değer·komut·kaynak_ağaç 식별 özet_Dosya·성공/hata_değer·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 LOG_değer

실패하면 Çıkış_program 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 oluştur 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
kaynak_ağaç 빌드만으로 Öz çekirdek_değer yürütmek_komut 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **hedef libc/헤더/kitaplık**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/derleyici.py --target openjdk-build \
  --java-home /yol/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /yol/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /yol/OpenJDK소스
```

부트 JDK는 oluştur 호스트에서 실행된다. 교차 oluştur 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## geçerli_öğe 작업 공간의 doğrulamak_5fb2b747 veri

Analiz_değer işlem_kök 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[kaynak_ağaç 출처와 다운로드 özet_Dosya](build/openjdk-port/source.json)를 보관한다.
oluştur 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 oluştur 호스트용이며 Öz çekirdek_değer 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac yürütmek_komut 시험을 통과했다. 기존 derleyici 회귀 시험과 새 oluştur yol 시험도
총 **25개 geçirmek_değer**했다. 공식 dağıtım_değer 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 doğrulamak_5fb2b747 LOG_KAYIT](build/openjdk-port/verification.json)은 oluştur 산출물과 yürütmek_komut 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[oluştur LOG_KAYIT](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[yürütmek_komut sınamalar](build/openjdk-port/smoke/report.json)을 각각 확인한다.
yürütmek_komut 시험은 새로 빌드한 java/javac로 한글 kaynak_ağaç, long/double, UTF-8 dosya,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 fiili_veri JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 Öz çekirdek_değer 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

geçerli_öğe 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 수 없으며, 준비한 musl ortam 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 Sonraki_öğe 단축 명령으로 같은 musl 환경을 사용한다.
kullanıcı_alanı·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 kaynak_ağaç/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 수 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 geçerli_öğe 디렉터리를 유지하므로, 한글 소스도 eş_değer 경로로
컴파일하고 실행할 수 있다. 예를 들어 앞의 시험에서 생성한 소스를 yeniden_denemek_değer 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/yerel_BLD_test.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke yerel_BLD_test
```

## 기존 ARM64 OpenJDK를 Öz 커널에 복사할 수 있는가

현재는 실행할 수 없다. 저장되어 있는 ARM64 OpenJDK 25의 statik_değer 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 yürütmek_komut 파일을 **실행하지 않고** ELF와 동적 simge·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

Öz 커널에 직접 적재할 수 없으면 검사 결과를 저장한 BACK_değer **Çıkış_program KOD_değer 3**을 반환한다.
ELF 호환성 검사는 fiili_veri çekirdek_değer 로더의 모든 검증을 대체하지 않는다.

| 확인한 koşul | ARM64 OpenJDK | geçerli_öğe Öz çekirdek_değer |
|---|---|---|
| ELF | PIE/공유 kitaplık, 동적 재배치 | 고정 ADRES ET_EXEC, Öz ABI note |
| program_Launcher | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS reddetmek_değer |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 dosya·루프백·GUI SVC와 협력식 세션 |
| Bellek_veri | VM·GC·Sınıf_değer·KOD_değer 캐시의 동적 ADRES ADRES_bölge | kullanıcı_alanı bölge_değer 16 MiB, BLD_RESİM bölge_değer 12 MiB |
| dosya | 큰 `lib/modules`, 공유 kitaplık 및 veri | RAM dosya 하나당 16 KiB, 영속 depo_değer 없음 |
| Java Sınıf_değer | OpenJDK 25 class 버전 69 | Öz JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·yazı_tipi_değer·Pencere 시스템 | 별도로 구현한 Swing API 부분집합 |

fiili_veri ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 geçerli_öğe 제한은
[ELF 로더](../platforms/rpi4-native/makine/kullanıcı_alanı.c),
[ADRES ADRES_bölge Tanım_değer](../platforms/rpi4-native/makine/kullanıcı_alanı.h),
[RAM dosya gerçekleme](../platforms/rpi4-native/kaynakKod/BellekDosyaları.java),
[kullanıcı_alanı ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 수 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM dosya 업로드 제한을 피하지만,
OpenJDK에 필요한 ADRES ADRES_bölge·스레드·동적 Bağlan 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 işletim_sistemi 호출·Bellek_veri·동적 Bağlan 규약까지 맞지는 않는다.
dosya Boyut 제한이나 ELF biçim_değer 검사만 풀어도 해결되는 문제가 아니다.

## Öz 커널을 유지하면서 이식하는 aşama_değer

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 işletim_sistemi ABI를 갖춘 kullanıcı_alanı 프로그램으로 실행할 수 있다.

기술적으로는 새 운영체제용 OpenJDK donanım_taşımak 또는 충분한 Linux kullanıcı_alanı ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 geçerli_öğe 코드와 fiili_veri 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **işletim_sistemi ABI와 libc 기반**: 큰 dosya·ADRES ADRES_bölge, 페이지 예약/commit_değer/해제와 korumak_değer değiştirmek_değer,
   표준 dosya/Saat 인터페이스, hata Dizin·C 런타임·hedef sysroot를 구현한다.
2. **fiili_veri 네이티브 스레드와 eşitlemek**: pthread에 대응하는 스케줄링·TLS·뮤텍스·koşul değişken_değer,
   원자 işlem_değer_c96707fb·Bellek_veri düzen_değer·중단/깨우기, 신호/özel_durum 문맥과 가드 페이지를 제공한다.
   geçerli_öğe vi/Swing의 artış_değer 대기에서 문맥을 보관하는 기능만으로 대체할 수 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 kitaplık·TLS 또는 이식에 맞는 statik_değer Bağlan,
   JVM 네이티브 simge 해결, 영속 dosya 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS donanım_taşımak**: oluştur 시스템과 `src/hotspot/os`, `os_cpu`에 Öz OS/AArch64 경계를
   구현한다. 기존 AArch64 komut 생성기는 재사용할 수 있지만 OS 종속부를 구현해야 한다.
   첫 yürütmek_komut 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **Sınıf_değer kitaplık·javac**: java.base의 JNI/dosya/네트워크/프로세스 연결과 modül_değer 적재를
   구현한 BACK_değer Öz çekirdek_değer 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 dış_değer 네트워크**: AWT/Java2D의 Pencere·artış_değer·yazı_tipi_değer 백엔드와 fiili_veri NIC/TCP/IP를
   이식한다. geçerli_öğe Öz Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **doğrulamak_5fb2b747**: 단계별 OS ABI sınamalar, OpenJDK jtreg sınamalar, GUI/한글/네트워크 부하 sınamalar,
   fiili_veri Pi4 검증을 수행한다. 일부 sınamalar 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK KOD_değer:
[POSIX Bellek_veri·OS gerçekleme](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS sınır_değer](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·Bellek_veri işlem_değer_girdi](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

Öz Java AOT 자체를 OpenJDK의 Java KOD_değer 전체를 처리하도록 확장하는 경로도 별도 개발이다.
nesne_değer 모델·가상/인터페이스 호출·özel_durum·GC·long/float/double·모든 DİZİ_değer·eşitlemek·동적 호출·
Sınıf_değer başlat/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
