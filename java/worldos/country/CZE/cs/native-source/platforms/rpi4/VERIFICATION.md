# distribuce_HODNOTA BLD_image ověřit_5fb2b747 LOGZ_ZÁZNAM

검증일: 2026-09-27 (Asia/Seoul)

cílová_úroveň: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 vlastní x86 커널을 ARM으로 이식한 결과가 아니다. skutečný_data Pi 보드는 연결되어 있지 않아 hardware_HODNOTA spuštění_stroje 성공을 확인하지 못했다.

## 배포물

| název_souboru | Velikost(bajt_HODNOTA) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | Archiv_HODNOTA 시스템 BLD_image; verze_Storage 후 1,475,747,840 bajt_HODNOTA |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 uživatelský_prostor data BLD_image; verze_Storage 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | čeština 보조 API와 Java pracovní_prostor |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 Archiv_HODNOTA BLD_image 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [Archiv_HODNOTA ověřit_5fb2b747 LOGZ_ZÁZNAM](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU ověřit_5fb2b747 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 položka_Seznam](dist/packages.lock.json)과 [원본 origin_HODNOTA](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | skutečný_data ověřit Obsah_HODNOTA | LOGZ_ZÁZNAM |
|---|---|---|
| hostit kompilátor zkoušky 19개 | 기존 AOT 회귀 zkoušky, `.class` 직접 vstup_HODNOTA, OpenJDK ELF program_Launcher, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, cesta_2 přesunout_HODNOTA, selhání_HODNOTA 시 기존 výstupní_pozice 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi BLD_image architektura | MBR mez_HODNOTA, FAT spuštění_stroje 파티션, Pi 펌웨어, ARM64 jádro_HODNOTA, Pi 4 DTB, initramfs, SquashFS 및 hodnota_hash_Soubor | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, spuštění_stroje 후 두 런타임의 skutečný_data Provést_příkaz | [런타임 LOGZ_ZÁZNAM](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 spuštění_stroje | Čtení 전용 시스템, Java název_souboru·UNICODE_HODNOTA·výjimka·objekt_HODNOTA·스레드·HTTP/TCP·dítě_HODNOTA 프로세스, Swing, CJK·아랍어·데바나가리 písmo_HODNOTA, Python název_souboru·스레드·soket_HODNOTA·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 Provést_příkaz název_souboru generovat | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 Provést_příkaz 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | uživatelský_prostor data, `/etc` Nastavení, `/usr/local/bin` program_f5044b9b, APK로 설치한 tree, pip 패키지, název_souboru 삭제 Informace_o_systému, 소유권, sudo, Java Provést_příkaz název_souboru 유지 | [restore.log](build/verification/restore.log) |
| informační_systémy_Offline 홈 přesunout_HODNOTA | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 instance_HODNOTA | [migrate.log](build/verification/migrate.log) |
| přesunout_HODNOTA 후 spuštění_stroje | 새 data 이미지로 부팅하여 재부팅 복원 항목을 zkusit_znovu_HODNOTA ověřit | [migrated-restore.log](build/verification/migrated-restore.log) |
| informační_systémy_normální Konec_program 및 data 무결성 | 일반 spuštění_stroje 3회 모두 OverlayFS/data mobilní_HODNOTA Čtení 전용 SWITCH_MODE 성공; 원본·복사본 ext4의 `e2fsck -fn` Konec_program KÓD_HODNOTA 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 SEQUENCE_HODNOTA 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 Konec_program KÓD_HODNOTA 0으로 통과했다. [전체 spuštění_stroje 결과와 LOGZ_HODNOTA hodnota_hash_Soubor](build/verification/boot.json)

QEMU 가상 NIC의 DHCP Adresa 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 externí_HODNOTA 인터넷이나 Pi Wi-Fi의 ověřit_5fb2b747 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [화면 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## implementace 범위와 남은 ověřit_5fb2b747

### QEMU 그래픽 Provést_příkaz 보완

interpret_příkazů 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. distribuce_HODNOTA 시스템 이미지와 base-id는 변경하지 않아 기존 uživatelský_prostor data 이미지를 계속 사용할 číslo 있다.

skutečný_data Xorg/VNC 화면에서 čeština Java pracovní_prostor, Swing zkoušky Okno, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. Konec_program 시 시스템 OverlayFS와 data 파일시스템의 Čtení 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 zkoušky VÝSLEDEK](build/verification/desktop.json)
- [그래픽 zkoušky LOGZ_HODNOTA](build/verification/desktop.log)
- [키보드·마우스 zkoušky 화면](build/verification/desktop-input.png)
- [인사 예제 화면](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 화면 없는 Provést_příkaz VÝSLEDEK](build/verification/headless-example.log)

zdrojový_soubor 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 název_souboru·문자·스레드 기능을 실행하고 안내를 출력한다. uživatelský_prostor 홈의 기존 원문을 자동 교체하지는 않는다. 향후 BLD_image 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 vstup_HODNOTA·písmo_HODNOTA 보완

`make test-korean`으로 skutečný_data Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space SWITCH_MODE 및 두벌식 Klíč_HODNOTA 입력을 시험했다. 양쪽에서 `한글 vstup_HODNOTA`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 uživatelský_prostor data 이미지에서 실행했으며 informační_systémy_normální Konec_program 시 두 파일시스템의 Čtení 전용 전환을 확인했다.

interpret_příkazů písmo_HODNOTA 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 skutečný_data název_souboru 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 화면 캡처에서 한글·영문 zobrazit_HODNOTA, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 uživatelský_prostor 시스템 변경분에 적용하며 distribuce_HODNOTA výchozí_hodnota 이미지와 base-id는 유지한다. 기존 název_souboru 백업, 동일 수정의 sprint_HODNOTA 적용 방지, 손상된 수정 název_souboru 및 다른 base-id odmítnout_HODNOTA, uživatelský_prostor 입력기 Nastavení 병합에 대한 hostit zkoušky 4개도 통과했다. 원래 uživatelský_prostor data BLD_image `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 vstup_HODNOTA·písmo_HODNOTA zkoušky VÝSLEDEK](build/verification/korean.json)
- [vstup_HODNOTA·skutečný_data písmo_HODNOTA 로딩 LOGZ_HODNOTA](build/verification/korean.log)
- [Swing·interpret_příkazů 한글 화면](build/verification/korean-desktop.png)
- [Java pracovní_prostor písmo_HODNOTA 화면](build/verification/korean-workbench.png)
- [Nastavení 보존 zkoušky](build/verification/desktop-update-tests.log)

### 남은 oříznout

- 새 kompilovat_zdroj cílová_úroveň `openjdk`는 **네이티브 program_Launcher + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 vzpěra_HODNOTA 범위는 여전히 제한적이다.
- Provést_příkaz 프로그램에는 main vstupní_bod, 호환 Třída_HODNOTA 버전과 의존 JAR/JNI가 필요하다. 개별 상용 program_f5044b9b, 모든 Java modul_HODNOTA, 모든 문자권을 시험한 것은 아니다.
- čeština Java 라이브러리는 název_souboru·문자·komunikace·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 čeština 번역판은 아니다.
- Pi 4 전용 펌웨어·jádro_HODNOTA·mobilní_HODNOTA 트리는 이미지에 들어 있지만 skutečný_data SD spuštění_stroje, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- uživatelský_prostor Adresář_HODNOTA 이동은 동일 시스템 BLD_image identifikátor_HODNOTA, ARM64, `/home/user`, UID 1000을 전제로 한다. Konec_program 후 소유권·oprávnění_HODNOTA·링크·přípona_HODNOTA hodnota_atributu·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

instalovat_HODNOTA·instance_HODNOTA 절차는 [README.md](README.md), kompilovat_zdroj 방식은 [OpenJDK Provést_příkaz název_souboru 안내](../../compiler/OpenJDK-spustitelný_soubor.md)를 따른다. BLD_image 파일만 생성했으며 skutečný_data SD 카드나 USB 디스크에 기록하지 않았다.
