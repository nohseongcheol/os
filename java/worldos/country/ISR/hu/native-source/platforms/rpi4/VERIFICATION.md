# elosztás_ÉRTÉK épít_KÉP ellenőriz LOG_REKORD

검증일: 2026-09-27 (Asia/Seoul)

cél: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 saját x86 커널을 ARM으로 이식한 결과가 아니다. tényleges_adat Pi 보드는 연결되어 있지 않아 hardver_ÉRTÉK 부팅 성공을 확인하지 못했다.

## 배포물

| Fájl | Méret(bájt_ÉRTÉK) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | archív_ÉRTÉK 시스템 épít_KÉP; kiad_tár 후 1,475,747,840 bájt_ÉRTÉK |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 felhasználó adat épít_KÉP; kiad_tár 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | magyar 보조 API와 Java munkaterület |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 archív_ÉRTÉK épít_KÉP 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [archív_ÉRTÉK ellenőriz LOG_REKORD](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU ellenőriz 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 bejegyzés_Lista](dist/packages.lock.json)과 [원본 eredet_ÉRTÉK](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | tényleges_adat igazol Tartalom_ÉRTÉK | LOG_REKORD |
|---|---|---|
| gazda fordítóprogram 시험 19개 | 기존 AOT 회귀 시험, `.class` 직접 bevitel_ÉRTÉK, OpenJDK ELF app_indító, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, ÚTVONAL áthelyez_ÉRTÉK, hiba_ÉRTÉK 시 기존 Kimenet 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi épít_KÉP architektúra | MBR határ_ÉRTÉK, FAT 부팅 파티션, Pi 펌웨어, ARM64 kernel_ÉRTÉK, Pi 4 DTB, initramfs, SquashFS 및 kivonat_Fájl | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, 부팅 후 두 런타임의 tényleges_adat végrehajt_parancs | [런타임 LOG_REKORD](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 부팅 | Olvasás 전용 시스템, Java Fájl·UNICODE_ÉRTÉK·kivétel·objektum_ÉRTÉK·스레드·HTTP/TCP·gyermek_ÉRTÉK 프로세스, Swing, CJK·아랍어·데바나가리 betűkészlet_ÉRTÉK, Python Fájl·스레드·szoftvercsatorna_ÉRTÉK·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 végrehajt_parancs Fájl generálás | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 végrehajt_parancs 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | felhasználó adat, `/etc` Beállítások, `/usr/local/bin` app_f5044b9b, APK로 설치한 tree, pip 패키지, Fájl 삭제 msinfo32_exe, 소유권, sudo, Java végrehajt_parancs Fájl 유지 | [restore.log](build/verification/restore.log) |
| informatikai_részleg_offline 홈 áthelyez_ÉRTÉK | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 másol_ÉRTÉK | [migrate.log](build/verification/migrate.log) |
| áthelyez_ÉRTÉK 후 부팅 | 새 adat 이미지로 부팅하여 재부팅 복원 항목을 újrapróbál_ÉRTÉK igazol | [migrated-restore.log](build/verification/migrated-restore.log) |
| informatikai_részleg_normál kilép_app 및 adat 무결성 | 일반 부팅 3회 모두 OverlayFS/adat mobil_ÉRTÉK Olvasás 전용 vált_mód 성공; 원본·복사본 ext4의 `e2fsck -fn` kilép_app KÓD_ÉRTÉK 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 szekvencia_ÉRTÉK 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 kilép_app KÓD_ÉRTÉK 0으로 통과했다. [전체 부팅 결과와 LOG_ÉRTÉK kivonat_Fájl](build/verification/boot.json)

QEMU 가상 NIC의 DHCP CÍM 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 külső_ÉRTÉK 인터넷이나 Pi Wi-Fi의 ellenőriz 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [화면 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## 구현 범위와 남은 ellenőriz

### QEMU 그래픽 végrehajt_parancs 보완

Terminál 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. elosztás_ÉRTÉK 시스템 이미지와 base-id는 변경하지 않아 기존 felhasználó adat 이미지를 계속 사용할 szám 있다.

tényleges_adat Xorg/VNC 화면에서 magyar Java munkaterület, Swing 시험 Ablak, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. kilép_app 시 시스템 OverlayFS와 adat 파일시스템의 Olvasás 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 시험 KR](build/verification/desktop.json)
- [그래픽 시험 LOG_ÉRTÉK](build/verification/desktop.log)
- [키보드·마우스 시험 화면](build/verification/desktop-input.png)
- [인사 예제 화면](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 화면 없는 végrehajt_parancs KR](build/verification/headless-example.log)

FORRÁS 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 Fájl·문자·스레드 기능을 실행하고 안내를 출력한다. felhasználó 홈의 기존 원문을 자동 교체하지는 않는다. 향후 épít_KÉP 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 bevitel_ÉRTÉK·betűkészlet_ÉRTÉK 보완

`make test-korean`으로 tényleges_adat Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space vált_mód 및 두벌식 Kulcs_ÉRTÉK 입력을 시험했다. 양쪽에서 `한글 bevitel_ÉRTÉK`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 felhasználó adat 이미지에서 실행했으며 informatikai_részleg_normál kilép_app 시 두 파일시스템의 Olvasás 전용 전환을 확인했다.

Terminál betűkészlet_ÉRTÉK 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 tényleges_adat Fájl 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 화면 캡처에서 한글·영문 bemutató_ÉRTÉK, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 felhasználó 시스템 변경분에 적용하며 elosztás_ÉRTÉK alapértelmezett_érték 이미지와 base-id는 유지한다. 기존 Fájl 백업, 동일 수정의 futam_ÉRTÉK 적용 방지, 손상된 수정 Fájl 및 다른 base-id elutasít_ÉRTÉK, felhasználó 입력기 Beállítások 병합에 대한 gazda 시험 4개도 통과했다. 원래 felhasználó adat épít_KÉP `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 bevitel_ÉRTÉK·betűkészlet_ÉRTÉK 시험 KR](build/verification/korean.json)
- [bevitel_ÉRTÉK·tényleges_adat betűkészlet_ÉRTÉK 로딩 LOG_ÉRTÉK](build/verification/korean.log)
- [Swing·Terminál 한글 화면](build/verification/korean-desktop.png)
- [Java munkaterület betűkészlet_ÉRTÉK 화면](build/verification/korean-workbench.png)
- [Beállítások 보존 시험](build/verification/desktop-update-tests.log)

### 남은 klip

- 새 épít_forrás cél `openjdk`는 **네이티브 app_indító + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 támogat_ÉRTÉK 범위는 여전히 제한적이다.
- végrehajt_parancs 프로그램에는 main belépési_pont, 호환 tanóra_ÉRTÉK 버전과 의존 JAR/JNI가 필요하다. 개별 상용 app_f5044b9b, 모든 Java modul_ÉRTÉK, 모든 문자권을 시험한 것은 아니다.
- magyar Java 라이브러리는 Fájl·문자·kommunikáció·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 magyar 번역판은 아니다.
- Pi 4 전용 펌웨어·kernel_ÉRTÉK·mobil_ÉRTÉK 트리는 이미지에 들어 있지만 tényleges_adat SD 부팅, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- felhasználó címtár_ÉRTÉK 이동은 동일 시스템 épít_KÉP azonosító_ÉRTÉK, ARM64, `/home/user`, UID 1000을 전제로 한다. kilép_app 후 소유권·engedély_ÉRTÉK·링크·bővítmény_ÉRTÉK attribútum_ÉRTÉK·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

telepít_ÉRTÉK·másol_ÉRTÉK 절차는 [README.md](README.md), épít_forrás 방식은 [OpenJDK végrehajt_parancs Fájl fontos_fájl_eb81d7d9](../../compiler/OpenJDK-végrehajtható_Fájl.md)를 따른다. épít_KÉP 파일만 생성했으며 tényleges_adat SD 카드나 USB 디스크에 기록하지 않았다.
