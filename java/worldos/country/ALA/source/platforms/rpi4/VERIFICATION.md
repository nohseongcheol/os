# fördelning_värde version_BILD validera LOG_POST

검증일: 2026-09-27 (Asia/Seoul)

mål: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 eget x86 커널을 ARM으로 이식한 결과가 아니다. verklig_data Pi 보드는 연결되어 있지 않아 maskinvara_värde maskinstart 성공을 확인하지 못했다.

## 배포물

| filnamn | Storlek(byte_värde) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | Arkiv_värde 시스템 version_BILD; släppa_minne 후 1,475,747,840 byte_värde |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 användarutrymme data version_BILD; släppa_minne 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | Svenska 보조 API와 Java arbetsyta |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 Arkiv_värde version_BILD 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [Arkiv_värde validera LOG_POST](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU validera 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 post_ange](dist/packages.lock.json)과 [원본 origo_värde](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | verklig_data verifiera Innehåll_värde | LOG_POST |
|---|---|---|
| värd kompilerare tester 19개 | 기존 AOT 회귀 tester, `.class` 직접 indata_värde, OpenJDK ELF app_Startbild, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, sökväg_2 flytta_värde, fel_värde 시 기존 utmatningsposition 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi version_BILD arkitektur | MBR gräns_värde, FAT maskinstart 파티션, Pi 펌웨어, ARM64 kärna_värde, Pi 4 DTB, initramfs, SquashFS 및 hash_fil | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, maskinstart 후 두 런타임의 verklig_data köra_kommando | [런타임 LOG_POST](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 maskinstart | Läs 전용 시스템, Java filnamn·UNICODE_värde·fel_31f743d2·objekt_värde·스레드·HTTP/TCP·barn_värde 프로세스, Swing, CJK·아랍어·데바나가리 teckensnitt_värde, Python filnamn·스레드·socket_värde·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 köra_kommando filnamn generera | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 köra_kommando 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | användarutrymme data, `/etc` Inställningar, `/usr/local/bin` app_f5044b9b, APK로 설치한 tree, pip 패키지, filnamn 삭제 msinfo32_exe, 소유권, sudo, Java köra_kommando filnamn 유지 | [restore.log](build/verification/restore.log) |
| informationsteknik_Offline 홈 flytta_värde | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 kopia_värde | [migrate.log](build/verification/migrate.log) |
| flytta_värde 후 maskinstart | 새 data 이미지로 부팅하여 재부팅 복원 항목을 försöka_igen_värde verifiera | [migrated-restore.log](build/verification/migrated-restore.log) |
| informationsteknik_normal Utgång_app 및 data 무결성 | 일반 maskinstart 3회 모두 OverlayFS/data enhet_värde Läs 전용 byta_läge 성공; 원본·복사본 ext4의 `e2fsck -fn` Utgång_app KOD_värde 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 SEKVENS_värde 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 Utgång_app KOD_värde 0으로 통과했다. [전체 maskinstart 결과와 LOG_värde hash_fil](build/verification/boot.json)

QEMU 가상 NIC의 DHCP Adress 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 extern_värde 인터넷이나 Pi Wi-Fi의 validera 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [skärmbild 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## implementation 범위와 남은 validera

### QEMU 그래픽 köra_kommando 보완

kommandotolk 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. fördelning_värde 시스템 이미지와 base-id는 변경하지 않아 기존 användarutrymme data 이미지를 계속 사용할 nummer 있다.

verklig_data Xorg/VNC 화면에서 Svenska Java arbetsyta, Swing tester Fönster, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. Utgång_app 시 시스템 OverlayFS와 data 파일시스템의 Läs 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 tester RESULTAT](build/verification/desktop.json)
- [그래픽 tester LOG_värde](build/verification/desktop.log)
- [키보드·마우스 tester skärmbild](build/verification/desktop-input.png)
- [인사 예제 skärmbild](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 skärmbild 없는 köra_kommando RESULTAT](build/verification/headless-example.log)

källfil 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 filnamn·문자·스레드 기능을 실행하고 안내를 출력한다. användarutrymme 홈의 기존 원문을 자동 교체하지는 않는다. 향후 version_BILD 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 indata_värde·teckensnitt_värde 보완

`make test-korean`으로 verklig_data Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space byta_läge 및 두벌식 Nyckel_värde 입력을 시험했다. 양쪽에서 `한글 indata_värde`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 användarutrymme data 이미지에서 실행했으며 informationsteknik_normal Utgång_app 시 두 파일시스템의 Läs 전용 전환을 확인했다.

kommandotolk teckensnitt_värde 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 verklig_data filnamn 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. skärmbild 캡처에서 한글·영문 visa_värde, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 användarutrymme 시스템 변경분에 적용하며 fördelning_värde standardvärde 이미지와 base-id는 유지한다. 기존 filnamn 백업, 동일 수정의 sprint_värde 적용 방지, 손상된 수정 filnamn 및 다른 base-id avvisa_värde, användarutrymme 입력기 Inställningar 병합에 대한 värd tester 4개도 통과했다. 원래 användarutrymme data version_BILD `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 indata_värde·teckensnitt_värde tester RESULTAT](build/verification/korean.json)
- [indata_värde·verklig_data teckensnitt_värde 로딩 LOG_värde](build/verification/korean.log)
- [Swing·kommandotolk 한글 skärmbild](build/verification/korean-desktop.png)
- [Java arbetsyta teckensnitt_värde skärmbild](build/verification/korean-workbench.png)
- [Inställningar 보존 tester](build/verification/desktop-update-tests.log)

### 남은 klipp

- 새 kompilera_källa mål `openjdk`는 **네이티브 app_Startbild + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 stöd_värde 범위는 여전히 제한적이다.
- köra_kommando 프로그램에는 main startpunkt, 호환 Kurs_värde 버전과 의존 JAR/JNI가 필요하다. 개별 상용 app_f5044b9b, 모든 Java modul_värde, 모든 문자권을 시험한 것은 아니다.
- Svenska Java 라이브러리는 filnamn·문자·kommunikation·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 Svenska 번역판은 아니다.
- Pi 4 전용 펌웨어·kärna_värde·enhet_värde 트리는 이미지에 들어 있지만 verklig_data SD maskinstart, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- användarutrymme Katalog_värde 이동은 동일 시스템 version_BILD identifierare_värde, ARM64, `/home/user`, UID 1000을 전제로 한다. Utgång_app 후 소유권·behörighet_värde·링크·tillägg_värde attribut_värde·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

installera_värde·kopia_värde 절차는 [README.md](README.md), kompilera_källa 방식은 [OpenJDK köra_kommando filnamn VIKTIGT_eb81d7d9](../../compiler/OpenJDK-körbar_fil_fil.md)를 따른다. version_BILD 파일만 생성했으며 verklig_data SD 카드나 USB 디스크에 기록하지 않았다.
