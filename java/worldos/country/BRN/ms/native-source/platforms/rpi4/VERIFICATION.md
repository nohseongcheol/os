# 배포 bina_imej sahkan LOG_baris

검증일: 2026-09-27 (Asia/Seoul)

sasaran: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 Asli x86 커널을 ARM으로 이식한 결과가 아니다. sebenar_data Pi 보드는 연결되어 있지 않아 하드웨어 permulaan_mesin 성공을 확인하지 못했다.

## 배포물

| Fail | Saiz(bait_VALUE) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | Arkib_VALUE 시스템 bina_imej; keluaran_Storan 후 1,475,747,840 bait_VALUE |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 ruang_pengguna data bina_imej; keluaran_Storan 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | Melayu 보조 API와 Java ruang_kerja |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 Arkib_VALUE bina_imej 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [Arkib_VALUE sahkan LOG_baris](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU sahkan 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 pemasukan_Senarai](dist/packages.lock.json)과 [원본 출처](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | sebenar_data tentu_sahkan Kandungan_VALUE | LOG_baris |
|---|---|---|
| hos 컴파일러 ujian 19개 | 기존 AOT 회귀 ujian, `.class` 직접 입력, OpenJDK ELF aplikasi_pelancar, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, LALUAN alih_VALUE, kegagalan_VALUE 시 기존 출력 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi bina_imej seni_bina | MBR 경계, FAT permulaan_mesin 파티션, Pi 펌웨어, ARM64 kernel_VALUE, Pi 4 DTB, initramfs, SquashFS 및 cincangan_fail | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, permulaan_mesin 후 두 런타임의 sebenar_data laksanakan_perintah | [런타임 LOG_baris](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 permulaan_mesin | Baca 전용 시스템, Java Fail·Unikod_VALUE·pengecualian·objek_VALUE·스레드·HTTP/TCP·anak_VALUE 프로세스, Swing, CJK·아랍어·데바나가리 fon_VALUE, Python Fail·스레드·소켓·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 laksanakan_perintah Fail jana | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 laksanakan_perintah 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | ruang_pengguna data, `/etc` Tetapan, `/usr/local/bin` aplikasi_f5044b9b, APK로 설치한 tree, pip 패키지, Fail 삭제 msinfo32_exe, 소유권, sudo, Java laksanakan_perintah Fail 유지 | [restore.log](build/verification/restore.log) |
| teknologi_maklumat_Luar_talian 홈 alih_VALUE | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 tika_VALUE | [migrate.log](build/verification/migrate.log) |
| alih_VALUE 후 permulaan_mesin | 새 data 이미지로 부팅하여 재부팅 복원 항목을 다시 tentu_sahkan | [migrated-restore.log](build/verification/migrated-restore.log) |
| 정상 Keluar_aplikasi 및 data 무결성 | 일반 permulaan_mesin 3회 모두 OverlayFS/data peranti_VALUE Baca 전용 tukar_mod 성공; 원본·복사본 ext4의 `e2fsck -fn` Keluar_aplikasi kod_VALUE 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 jujukan_VALUE 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 Keluar_aplikasi kod_VALUE 0으로 통과했다. [전체 permulaan_mesin 결과와 LOG_VALUE cincangan_fail](build/verification/boot.json)

QEMU 가상 NIC의 DHCP e_mel 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 외부 인터넷이나 Pi Wi-Fi의 sahkan 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [화면 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## pelaksanaan 범위와 남은 sahkan

### QEMU 그래픽 laksanakan_perintah 보완

Terminal 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. 배포 시스템 이미지와 base-id는 변경하지 않아 기존 ruang_pengguna data 이미지를 계속 사용할 수 있다.

sebenar_data Xorg/VNC 화면에서 Melayu Java ruang_kerja, Swing ujian Tetingkap, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. Keluar_aplikasi 시 시스템 OverlayFS와 data 파일시스템의 Baca 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 ujian ukuran](build/verification/desktop.json)
- [그래픽 ujian LOG_VALUE](build/verification/desktop.log)
- [키보드·마우스 ujian 화면](build/verification/desktop-input.png)
- [인사 예제 화면](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 화면 없는 laksanakan_perintah ukuran](build/verification/headless-example.log)

SUMBER 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 Fail·문자·스레드 기능을 실행하고 안내를 출력한다. ruang_pengguna 홈의 기존 원문을 자동 교체하지는 않는다. 향후 bina_imej 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 입력·fon_VALUE 보완

`make test-korean`으로 sebenar_data Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space tukar_mod 및 두벌식 Kunci_VALUE 입력을 시험했다. 양쪽에서 `한글 입력`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 ruang_pengguna data 이미지에서 실행했으며 정상 Keluar_aplikasi 시 두 파일시스템의 Baca 전용 전환을 확인했다.

Terminal fon_VALUE 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 sebenar_data Fail 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 화면 캡처에서 한글·영문 tayang_VALUE, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 ruang_pengguna 시스템 변경분에 적용하며 배포 nilai_lalai 이미지와 base-id는 유지한다. 기존 Fail 백업, 동일 수정의 lelaran_VALUE 적용 방지, 손상된 수정 Fail 및 다른 base-id tolak_VALUE, ruang_pengguna 입력기 Tetapan 병합에 대한 hos ujian 4개도 통과했다. 원래 ruang_pengguna data bina_imej `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 입력·fon_VALUE ujian ukuran](build/verification/korean.json)
- [입력·sebenar_data fon_VALUE 로딩 LOG_VALUE](build/verification/korean.log)
- [Swing·Terminal 한글 화면](build/verification/korean-desktop.png)
- [Java ruang_kerja fon_VALUE 화면](build/verification/korean-workbench.png)
- [Tetapan 보존 ujian](build/verification/desktop-update-tests.log)

### 남은 klip

- 새 bina_sumber sasaran `openjdk`는 **네이티브 aplikasi_pelancar + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 Sokongan_VALUE 범위는 여전히 제한적이다.
- laksanakan_perintah 프로그램에는 main titik_permulaan, 호환 Kelas_VALUE 버전과 의존 JAR/JNI가 필요하다. 개별 상용 aplikasi_f5044b9b, 모든 Java modul_VALUE, 모든 문자권을 시험한 것은 아니다.
- Melayu Java 라이브러리는 Fail·문자·통신·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 Melayu 번역판은 아니다.
- Pi 4 전용 펌웨어·kernel_VALUE·peranti_VALUE 트리는 이미지에 들어 있지만 sebenar_data SD permulaan_mesin, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- ruang_pengguna direktori_VALUE 이동은 동일 시스템 bina_imej 식별자, ARM64, `/home/user`, UID 1000을 전제로 한다. Keluar_aplikasi 후 소유권·keizinan_VALUE·링크·sambungan_VALUE atribut_VALUE·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

pasang_VALUE·tika_VALUE 절차는 [README.md](README.md), bina_sumber 방식은 [OpenJDK laksanakan_perintah Fail README_eb81d7d9](../../compiler/OpenJDK-fail_boleh_laku.md)를 따른다. bina_imej 파일만 생성했으며 sebenar_data SD 카드나 USB 디스크에 기록하지 않았다.
