# OpenJDK sumber_pohon 빌드와 Asli Java kernel_VALUE 이식

**소스에서 OpenJDK를 만드는 일과, 그 결과를 Asli 커널에서 실행하는 일은 별도다.**
`compiler`에 공식 OpenJDK 빌드를 실행하는 `openjdk-build` 대상을 추가했다.
Java 코드에는 부트 JDK의 javac, HotSpot·네이티브 라이브러리에는 C/C++ 도구를 사용한다.
기존 Asli Java AOT 후단이 Java 전체나 C++ 전체를 처리하게 된 것은 아니다.

## bangun_sumber 경로의 pemisah_VALUE_d8ba4873

| target | 입력과 hasil | Jalankan_perintah kondisi |
|---|---|---|
| `linux`, `kernel`, `user` | 제한된 Java → Asli x86 AOT → ELF32 | 해당 CPU·Asli ABI |
| `arm64.py` | 제한된 Java class → freestanding C → AArch64 | Asli ARM64 kernel_VALUE/ruang_pengguna ABI |
| `openjdk` | Java 앱 → 기존 OpenJDK를 호출하는 실행기와 `.app` | 일치하는 OS/CPU의 설치된 JVM |
| **`openjdk-build`** | OpenJDK 전체 sumber_pohon → 공식 configure/make → JDK build_foto | **bangun target OS/CPU의 Jalankan_perintah kasus_VALUE** |

OpenJDK는 Java berkas 묶음만으로 이루어져 있지 않다. HotSpot VM, JNI Sambung,
Kelas_VALUE 라이브러리의 C/C++ implementasi, apl_peluncur, modul_VALUE build_foto 및 buat 도구를 함께 빌드한다.
따라서 Asli AOT에 Java 명령을 더하는 것만으로 OpenJDK 전체 빌드가 완성되지는 않는다.
공식 절차는 [OpenJDK bangun 문서](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/doc/building.md)를 따른다.

## sumber_pohon bangun perintah

호스트에 해당 OpenJDK 버전이 요구하는 부트 JDK·C/C++ 컴파일러·Autoconf·Make와
개발 헤더를 준비한다. Swing/AWT의 Linux pustaka 빌드에는 X11·font_VALUE 등의
개발 라이브러리도 필요하다. 이 도구가 시스템 패키지를 자동으로 설치하지는 않는다.

```sh
cd /home/user/jkoros
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /jalur/부트JDK --jobs 2 \
  -o compiler/build/openjdk-linux /jalur/OpenJDK소스
```

`--entry`는 지정하지 않는다. `-o`는 sumber_pohon 트리 밖의 전용 bangun 디렉터리다.
sumber_pohon·bangun·부트 JDK 경로에 공백을 허용하지 않는다. 다른 프로젝트의 비어 있지 않은
디렉터리를 덮어쓰지 않으며, 같은 소스의 관리된 bangun 디렉터리는 재실행할 수 있다.

주요 산출물:

- `images/jdk/bin/java`, `images/jdk/bin/javac`
- `images/jdk/lib/server/libjvm.so`, `images/jdk/lib/modules`, JNI pustaka
- `jkoros-openjdk-build.json`: tahap_VALUE·perintah·sumber_pohon 식별 hash_file·성공/kegagalan_VALUE·ABI 검사
- `driver-configure.log`, `images.log`: 단계별 LOG_VALUE

실패하면 Keluar_apl 상태가 0이 아니며 보고서의 `passed`도 false다. 예전 이미지가 남아
있더라도 새 bangun 성공으로 기록하지 않는다. `native_kernel_port_complete`는 false다.
sumber_pohon 빌드만으로 Asli kernel_VALUE Jalankan_perintah 시험을 통과한 것으로 처리하지 않는다.

다른 CPU용 Linux JDK를 만들 때는 대상에 맞는 최신 교차 컴파일러와 **target libc/헤더/pustaka**가 필요하다.
다음은 그러한 도구를 준비한 환경에서 사용하는 형식이다.

```sh
python3 compiler/컴파일러.py --target openjdk-build \
  --java-home /jalur/호스트용부트JDK \
  --openjdk-target aarch64-linux-gnu \
  --cc /교차도구/bin/aarch64-linux-gnu-gcc \
  --cxx /교차도구/bin/aarch64-linux-gnu-g++ \
  --sysroot /jalur/ARM64-Linux-sysroot --jobs 2 \
  -o compiler/build/openjdk-aarch64 /jalur/OpenJDK소스
```

부트 JDK는 bangun 호스트에서 실행된다. 교차 bangun 결과를 호스트에서 실행하지 않는다.
`aarch64-jkoros`를 지정하는 것만으로 새 OS 이식이 생기지 않으므로 현재는 거부한다.
공식 configure 옵션은 `--configure-arg=--옵션`을 반복해 전달한다.

## saat_ini_item 작업 공간의 validasi data

Analisis_VALUE Tugas_akar 소스는 OpenJDK `jdk25u`, 태그 `jdk-25.0.4+7`, 커밋
`0b8bc780f976dab23ec798018fef0b674e885b0c`이다.
[sumber_pohon 출처와 다운로드 hash_file](build/openjdk-port/source.json)를 보관한다.
bangun 도구는 `build/openjdk-port/host`의 별도 Alpine x86_64 환경에 준비했다.
이 환경은 bangun 호스트용이며 Asli kernel_VALUE 이미지에 들어가지 않는다.

이 소스로 `make images`를 완료하고, 생성한 **OpenJDK 25.0.4-internal / Linux x86_64 musl**의
java·javac Jalankan_perintah 시험을 통과했다. 기존 컴파일러 회귀 시험과 새 bangun jalur 시험도
총 **25개 teruskan_VALUE**했다. 공식 배포 바이너리나 Java SE 호환 인증을 받은 배포판은 아니다.
[통합 validasi LOG_baris](build/openjdk-port/verification.json)은 bangun 산출물과 Jalankan_perintah 시험의
java·libjvm 해시가 일치하는지도 확인한 결과다.

[bangun LOG_baris](build/openjdk-port/linux-x86_64/jkoros-openjdk-build.json)의 `passed`와
[Jalankan_perintah pengujian](build/openjdk-port/smoke/report.json)을 각각 확인한다.
Jalankan_perintah 시험은 새로 빌드한 java/javac로 한글 sumber_pohon, long/double, UTF-8 berkas,
Thread·Linux 루프백 TCP·Swing 이벤트 처리를 검사한다.
`window_tested: false`인 결과는 aktual_data JFrame 화면 시험을 뜻하지 않는다.
Linux에서 한 시험이 Asli kernel_VALUE 시험으로 바뀌는 것은 아니다.

```sh
python3 compiler/test_openjdk_image.py \
  --jdk /실행가능한/빌드결과/images/jdk --output compiler/build/openjdk-port/smoke
```

saat_ini_item 별도 환경에서 만든 JDK는 **Linux x86_64 musl용**이다. 일반 glibc 호스트에서
경로만 지정해 실행할 수 없으며, 준비한 musl lingkungan 또는 일치하는 Linux 환경이 필요하다.
Raspberry Pi용 ARM64 산출물이라고 표시하지 않는다.

준비된 이 작업 공간에서는 Berikutnya_item 단축 명령으로 같은 musl 환경을 사용한다.
ruang_pengguna·마운트·PID 네임스페이스를 허용하는 호스트에서 실행하며, `build`는 앞의 고정 sumber_pohon/전용 환경을 재사용한다. 마운트는 새 네임스페이스 안에서만 생성되고 종료하면 사라진다. 네임스페이스를 사용할 수 없으면 `openjdk_local.py --proot build` 형식의 느린 대체 경로가 있다.

```sh
python3 compiler/openjdk_local.py build
python3 compiler/openjdk_local.py test
python3 compiler/openjdk_local.py java -version
python3 compiler/openjdk_local.py javac -version
```

`/home/user` 아래에서 호출하면 saat_ini_item 디렉터리를 유지하므로, 한글 소스도 serekan_VALUE 경로로
컴파일하고 실행할 수 있다. 예를 들어 앞의 시험에서 생성한 소스를 coba_lagi_VALUE 실행하려면:

```sh
python3 compiler/openjdk_local.py javac -encoding UTF-8 \
  compiler/build/openjdk-port/smoke/자체빌드시험.java
python3 compiler/openjdk_local.py java -Djava.awt.headless=true \
  -cp compiler/build/openjdk-port/smoke 자체빌드시험
```

## 기존 ARM64 OpenJDK를 Asli 커널에 복사할 수 있는가

현재는 실행할 수 없다. 저장되어 있는 ARM64 OpenJDK 25의 statik_VALUE 검사 결과는
[arm64-runtime.json](build/openjdk-port/arm64-runtime.json)에 있다.
검사 도구는 Jalankan_perintah 파일을 **실행하지 않고** ELF와 동적 simbol·모듈을 읽는다.

```sh
python3 compiler/openjdk_probe.py \
  --jdk platforms/rpi4/build/rootfs/usr/lib/jvm/java-25-openjdk \
  -o compiler/build/openjdk-port/arm64-runtime.json --require-native
```

Asli 커널에 직접 적재할 수 없으면 검사 결과를 저장한 BACK_VALUE **Keluar_apl CODE_VALUE 3**을 반환한다.
ELF 호환성 검사는 aktual_data kernel_VALUE 로더의 모든 검증을 대체하지 않는다.

| 확인한 kondisi | ARM64 OpenJDK | saat_ini_item Asli kernel_VALUE |
|---|---|---|
| ELF | PIE/공유 pustaka, 동적 재배치 | 고정 surel ET_EXEC, Asli ABI note |
| apl_peluncur | `/lib/ld-musl-aarch64.so.1` 필요 | PT_INTERP/PT_DYNAMIC/PT_TLS tolak_VALUE |
| 네이티브 VM | pthread, mmap/mprotect, signal, dlopen 등 호출 | 일부 berkas·루프백·GUI SVC와 협력식 세션 |
| Memori_data | VM·GC·Kelas_VALUE·CODE_VALUE 캐시의 동적 surel surel_wilayah | ruang_pengguna wilayah_VALUE 16 MiB, build_foto wilayah_VALUE 12 MiB |
| berkas | 큰 `lib/modules`, 공유 pustaka 및 data | RAM berkas 하나당 16 KiB, 영속 Store_VALUE 없음 |
| Java Kelas_VALUE | OpenJDK 25 class 버전 69 | Asli JVM은 class 45…52 부분집합 |
| Swing | OpenJDK AWT/Java2D/JNI·font_VALUE·Jendela 시스템 | 별도로 구현한 Swing API 부분집합 |

aktual_data ARM64 이미지의 `libjvm.so`는 19,708,720바이트, `lib/modules`는
146,199,951바이트다. 커널의 saat_ini_item 제한은
[ELF 로더](../platforms/rpi4-native/mesin/ruang_pengguna.c),
[surel surel_wilayah Definisi_VALUE](../platforms/rpi4-native/mesin/ruang_pengguna.h),
[RAM berkas implementasi](../platforms/rpi4-native/kodeSumber/BerkasMemori.java),
[ruang_pengguna ABI](../platforms/rpi4-native/USER-ABI.md)에서 확인할 수 있다.
큰 내장 프로그램을 커널에 묶는 기존 경로는 RAM berkas 업로드 제한을 피하지만,
OpenJDK에 필요한 surel surel_wilayah·스레드·동적 Sambung 기능까지 제공하지는 않는다.

같은 AArch64 기계어라는 사실만으로 sistem_operasi 호출·Memori_data·동적 Sambung 규약까지 맞지는 않는다.
berkas Ukuran 제한이나 ELF format_VALUE 검사만 풀어도 해결되는 문제가 아니다.

## Asli 커널을 유지하면서 이식하는 tahap_VALUE

커널을 Java로 작성했다는 사실은 이식의 장애가 아니다. 이미 제공하는 EL0 C/C++ 실행처럼
OpenJDK의 네이티브 VM도 sistem_operasi ABI를 갖춘 ruang_pengguna 프로그램으로 실행할 수 있다.

기술적으로는 새 운영체제용 OpenJDK 포트 또는 충분한 Linux ruang_pengguna ABI 호환 계층을
구현하는 방식으로 가능하다. 아래는 saat_ini_item 코드와 aktual_data 의존성에 근거한 설계 방향이며,
이미 구현되었다는 목록은 아니다.

1. **sistem_operasi ABI와 libc 기반**: 큰 berkas·surel surel_wilayah, 페이지 예약/penerapan_VALUE/해제와 amankan_VALUE ubah_VALUE,
   표준 berkas/Jam 인터페이스, galat INDEX·C 런타임·target sysroot를 구현한다.
2. **aktual_data 네이티브 스레드와 sinkro**: pthread에 대응하는 스케줄링·TLS·뮤텍스·kondisi variabel_VALUE,
   원자 bedah_VALUE·Memori_data urutan_VALUE·중단/깨우기, 신호/pengecualian 문맥과 가드 페이지를 제공한다.
   saat_ini_item vi/Swing의 입력 대기에서 문맥을 보관하는 기능만으로 대체할 수 없다.
3. **로더와 런타임 수명**: ELF 재배치·공유 pustaka·TLS 또는 이식에 맞는 statik_VALUE Sambung,
   JVM 네이티브 simbol 해결, 영속 berkas 시스템, 일반 프로그램의 2초 제한 재설계를 수행한다.
4. **HotSpot OS 포트**: bangun 시스템과 `src/hotspot/os`, `os_cpu`에 Asli OS/AArch64 경계를
   구현한다. 기존 AArch64 perintah 생성기는 재사용할 수 있지만 OS 종속부를 구현해야 한다.
   첫 Jalankan_perintah 목표는 `java -Xint -version`과 작은 HelloWorld다.
5. **Kelas_VALUE pustaka·javac**: java.base의 JNI/berkas/네트워크/프로세스 연결과 modul_VALUE 적재를
   구현한 BACK_VALUE Asli kernel_VALUE 안에서 `javac Hello.java`, `java Hello`를 확인한다.
6. **GUI와 eksternal_VALUE 네트워크**: AWT/Java2D의 Jendela·입력·font_VALUE 백엔드와 aktual_data NIC/TCP/IP를
   이식한다. saat_ini_item Asli Swing 부분집합이나 루프백 API가 OpenJDK의 구현을 대신하지 않는다.
7. **validasi**: 단계별 OS ABI pengujian, OpenJDK jtreg pengujian, GUI/한글/네트워크 부하 pengujian,
   aktual_data Pi4 검증을 수행한다. 일부 pengujian 통과를 Java SE 전체 호환 인증으로 표시하지 않는다.

근거가 되는 OpenJDK CODE_VALUE:
[POSIX Memori_data·OS implementasi](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/posix/os_posix.cpp),
[Linux AArch64 OS 경계](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os_cpu/linux_aarch64/os_linux_aarch64.cpp),
[Linux 스레드·신호·Memori_data Proses_VALUE_entri](https://github.com/openjdk/jdk25u/blob/jdk-25.0.4%2B7/src/hotspot/os/linux/os_linux.cpp).

Asli Java AOT 자체를 OpenJDK의 Java CODE_VALUE 전체를 처리하도록 확장하는 경로도 별도 개발이다.
objek_VALUE 모델·가상/인터페이스 호출·pengecualian·GC·long/float/double·모든 ARRAY_VALUE·sinkro·동적 호출·
Kelas_VALUE inisialisasi/로딩·JNI 경계가 필요하며, HotSpot C/C++ 빌드와 OS 이식은 그 뒤에도 남는다.
