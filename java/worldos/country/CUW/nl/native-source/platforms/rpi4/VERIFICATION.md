# distributie_WAARDE build_kopie valideren LOG_RECORD

검증일: 2026-09-27 (Asia/Seoul)

doel: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 Eigen x86 커널을 ARM으로 이식한 결과가 아니다. werkelijk_gegevens Pi 보드는 연결되어 있지 않아 hardware_WAARDE machineopstart 성공을 확인하지 못했다.

## 배포물

| bestand | Grootte(byte_WAARDE) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | Archief_WAARDE 시스템 build_kopie; versie_Opslag 후 1,475,747,840 byte_WAARDE |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 gebruikersruimte gegevens build_kopie; versie_Opslag 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | Nederlands 보조 API와 Java werkgebied |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 Archief_WAARDE build_kopie 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [Archief_WAARDE valideren LOG_RECORD](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU valideren 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 invoer_Lijst_f07b3200](dist/packages.lock.json)과 [원본 oorsprong_WAARDE](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | werkelijk_gegevens bevestigen Inhoud_WAARDE | LOG_RECORD |
|---|---|---|
| host compiler tests 19개 | 기존 AOT 회귀 tests, `.class` 직접 invoer_WAARDE, OpenJDK ELF app_app_lade, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, pad verplaatsen_WAARDE_83b651b8, fout_WAARDE 시 기존 tekstuitvoer 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi build_kopie architectuur | MBR grens_WAARDE, FAT machineopstart 파티션, Pi 펌웨어, ARM64 kernel_WAARDE, Pi 4 DTB, initramfs, SquashFS 및 hash_Bestand | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, machineopstart 후 두 런타임의 werkelijk_gegevens Uitvoeren_opdracht | [런타임 LOG_RECORD](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 machineopstart | Lezen 전용 시스템, Java bestand·UNICODE_WAARDE·uitzondering·object_WAARDE·스레드·HTTP/TCP·kind_WAARDE 프로세스, Swing, CJK·아랍어·데바나가리 lettertype_WAARDE, Python bestand·스레드·socket_WAARDE·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 Uitvoeren_opdracht bestand genereren | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 Uitvoeren_opdracht 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | gebruikersruimte gegevens, `/etc` Instellingen, `/usr/local/bin` app_f5044b9b, APK로 설치한 tree, pip 패키지, bestand 삭제 msinfo32_exe, 소유권, sudo, Java Uitvoeren_opdracht bestand behouden_WAARDE | [restore.log](build/verification/restore.log) |
| informatie_Offline 홈 verplaatsen_WAARDE_83b651b8 | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 kopiëren_WAARDE | [migrate.log](build/verification/migrate.log) |
| verplaatsen_WAARDE_83b651b8 후 machineopstart | 새 gegevens 이미지로 부팅하여 재부팅 복원 항목을 opnieuw_proberen_WAARDE bevestigen | [migrated-restore.log](build/verification/migrated-restore.log) |
| informatie_normaal Einde_app 및 gegevens 무결성 | 일반 machineopstart 3회 모두 OverlayFS/gegevens mobiel_WAARDE Lezen 전용 switch_MODUS 성공; 원본·복사본 ext4의 `e2fsck -fn` Einde_app CODE_WAARDE 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 REEKS_WAARDE 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 Einde_app CODE_WAARDE 0으로 통과했다. [전체 machineopstart 결과와 LOG_WAARDE hash_Bestand](build/verification/boot.json)

QEMU 가상 NIC의 DHCP ADRES 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 extern_WAARDE 인터넷이나 Pi Wi-Fi의 valideren 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [scherm 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## implementatie 범위와 남은 valideren

### QEMU 그래픽 Uitvoeren_opdracht 보완

terminal 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. distributie_WAARDE 시스템 이미지와 base-id는 변경하지 않아 기존 gebruikersruimte gegevens 이미지를 계속 사용할 nummer 있다.

werkelijk_gegevens Xorg/VNC 화면에서 Nederlands Java werkgebied, Swing tests Venster, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. Einde_app 시 시스템 OverlayFS와 gegevens 파일시스템의 Lezen 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 tests resultaat](build/verification/desktop.json)
- [그래픽 tests LOG_WAARDE](build/verification/desktop.log)
- [키보드·마우스 tests scherm](build/verification/desktop-input.png)
- [인사 예제 scherm](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 scherm 없는 Uitvoeren_opdracht resultaat](build/verification/headless-example.log)

broncode 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 bestand·문자·스레드 기능을 실행하고 안내를 출력한다. gebruikersruimte 홈의 기존 원문을 자동 교체하지는 않는다. 향후 build_kopie 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 invoer_WAARDE·lettertype_WAARDE 보완

`make test-korean`으로 werkelijk_gegevens Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space switch_MODUS 및 두벌식 toets_WAARDE 입력을 시험했다. 양쪽에서 `한글 invoer_WAARDE`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 gebruikersruimte gegevens 이미지에서 실행했으며 informatie_normaal Einde_app 시 두 파일시스템의 Lezen 전용 전환을 확인했다.

terminal lettertype_WAARDE 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 werkelijk_gegevens bestand 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. scherm 캡처에서 한글·영문 weergeven_WAARDE, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 gebruikersruimte 시스템 변경분에 적용하며 distributie_WAARDE standaardwaarde 이미지와 base-id는 유지한다. 기존 bestand 백업, 동일 수정의 sprint_WAARDE 적용 방지, 손상된 수정 bestand 및 다른 base-id weigeren_WAARDE, gebruikersruimte 입력기 Instellingen 병합에 대한 host tests 4개도 통과했다. 원래 gebruikersruimte gegevens build_kopie `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 invoer_WAARDE·lettertype_WAARDE tests resultaat](build/verification/korean.json)
- [invoer_WAARDE·werkelijk_gegevens lettertype_WAARDE 로딩 LOG_WAARDE](build/verification/korean.log)
- [Swing·terminal 한글 scherm](build/verification/korean-desktop.png)
- [Java werkgebied lettertype_WAARDE scherm](build/verification/korean-workbench.png)
- [Instellingen 보존 tests](build/verification/desktop-update-tests.log)

### 남은 clip

- 새 compileren_bron doel `openjdk`는 **네이티브 app_app_lade + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 steun_WAARDE 범위는 여전히 제한적이다.
- Uitvoeren_opdracht 프로그램에는 main beginpunt, 호환 les_WAARDE 버전과 의존 JAR/JNI가 필요하다. 개별 상용 app_f5044b9b, 모든 Java module_WAARDE, 모든 문자권을 시험한 것은 아니다.
- Nederlands Java 라이브러리는 bestand·문자·communicatie·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 Nederlands 번역판은 아니다.
- Pi 4 전용 펌웨어·kernel_WAARDE·mobiel_WAARDE 트리는 이미지에 들어 있지만 werkelijk_gegevens SD machineopstart, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- gebruikersruimte map_WAARDE 이동은 동일 시스템 build_kopie id_WAARDE, ARM64, `/home/user`, UID 1000을 전제로 한다. Einde_app 후 소유권·machtiging_WAARDE·링크·extensie_WAARDE kenmerkwaarde·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

installeren_WAARDE·kopiëren_WAARDE 절차는 [README.md](README.md), compileren_bron 방식은 [OpenJDK Uitvoeren_opdracht bestand LEESMIJ_eb81d7d9](../../compiler/OpenJDK-uitvoerbaar_bestand.md)를 따른다. build_kopie 파일만 생성했으며 werkelijk_gegevens SD 카드나 USB 디스크에 기록하지 않았다.
