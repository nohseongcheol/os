# dağıtım_değer BLD_RESİM doğrulamak_5fb2b747 LOG_KAYIT

검증일: 2026-09-27 (Asia/Seoul)

hedef: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 Öz x86 커널을 ARM으로 이식한 결과가 아니다. fiili_veri Pi 보드는 연결되어 있지 않아 donanım_değer makine_başlatma 성공을 확인하지 못했다.

## 배포물

| dosya | Boyut(bayt_değer) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | Arşiv_değer 시스템 BLD_RESİM; sürüm_Depolama 후 1,475,747,840 bayt_değer |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 kullanıcı_alanı veri BLD_RESİM; sürüm_Depolama 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | Türkçe 보조 API와 Java çalışma_alanı |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 Arşiv_değer BLD_RESİM 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [Arşiv_değer doğrulamak_5fb2b747 LOG_KAYIT](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU doğrulamak_5fb2b747 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 girdi_Liste](dist/packages.lock.json)과 [원본 origin_değer](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | fiili_veri doğrulamak içerik_değer | LOG_KAYIT |
|---|---|---|
| konak derleyici sınamalar 19개 | 기존 AOT 회귀 sınamalar, `.class` 직접 artış_değer, OpenJDK ELF program_Launcher, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, yol taşımak_değer_83b651b8, hata_değer 시 기존 metinÇıktısı 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi BLD_RESİM mimari | MBR sınır_değer, FAT makine_başlatma 파티션, Pi 펌웨어, ARM64 çekirdek_değer, Pi 4 DTB, initramfs, SquashFS 및 özet_Dosya | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, makine_başlatma 후 두 런타임의 fiili_veri yürütmek_komut | [런타임 LOG_KAYIT](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 makine_başlatma | Okuma 전용 시스템, Java dosya·UNICODE_değer·özel_durum·nesne_değer·스레드·HTTP/TCP·alt_değer 프로세스, Swing, CJK·아랍어·데바나가리 yazı_tipi_değer, Python dosya·스레드·yuva_değer·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 yürütmek_komut dosya oluşturmak | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 yürütmek_komut 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | kullanıcı_alanı veri, `/etc` Ayarlar, `/usr/local/bin` program_f5044b9b, APK로 설치한 tree, pip 패키지, dosya 삭제 msinfo32_exe, 소유권, sudo, Java yürütmek_komut dosya 유지 | [restore.log](build/verification/restore.log) |
| bilgi_teknolojisi_Çevrimdışı 홈 taşımak_değer_83b651b8 | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 örnek_değer | [migrate.log](build/verification/migrate.log) |
| taşımak_değer_83b651b8 후 makine_başlatma | 새 veri 이미지로 부팅하여 재부팅 복원 항목을 yeniden_denemek_değer doğrulamak | [migrated-restore.log](build/verification/migrated-restore.log) |
| bilgi_teknolojisi_normal Çıkış_program 및 veri 무결성 | 일반 makine_başlatma 3회 모두 OverlayFS/veri cihaz_değer Okuma 전용 geçiş_mod 성공; 원본·복사본 ext4의 `e2fsck -fn` Çıkış_program KOD_değer 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 dizi_değer 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 Çıkış_program KOD_değer 0으로 통과했다. [전체 makine_başlatma 결과와 LOG_değer özet_Dosya](build/verification/boot.json)

QEMU 가상 NIC의 DHCP ADRES 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 dış_değer 인터넷이나 Pi Wi-Fi의 doğrulamak_5fb2b747 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [화면 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## gerçekleme 범위와 남은 doğrulamak_5fb2b747

### QEMU 그래픽 yürütmek_komut 보완

uçbirim 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. dağıtım_değer 시스템 이미지와 base-id는 변경하지 않아 기존 kullanıcı_alanı veri 이미지를 계속 사용할 수 있다.

fiili_veri Xorg/VNC 화면에서 Türkçe Java çalışma_alanı, Swing sınamalar Pencere, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. Çıkış_program 시 시스템 OverlayFS와 veri 파일시스템의 Okuma 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 sınamalar sonuç](build/verification/desktop.json)
- [그래픽 sınamalar LOG_değer](build/verification/desktop.log)
- [키보드·마우스 sınamalar 화면](build/verification/desktop-input.png)
- [인사 예제 화면](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 화면 없는 yürütmek_komut sonuç](build/verification/headless-example.log)

kaynakKod 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 dosya·문자·스레드 기능을 실행하고 안내를 출력한다. kullanıcı_alanı 홈의 기존 원문을 자동 교체하지는 않는다. 향후 BLD_RESİM 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 artış_değer·yazı_tipi_değer 보완

`make test-korean`으로 fiili_veri Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space geçiş_mod 및 두벌식 tuş_değer 입력을 시험했다. 양쪽에서 `한글 artış_değer`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 kullanıcı_alanı veri 이미지에서 실행했으며 bilgi_teknolojisi_normal Çıkış_program 시 두 파일시스템의 Okuma 전용 전환을 확인했다.

uçbirim yazı_tipi_değer 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 fiili_veri dosya 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 화면 캡처에서 한글·영문 şov_değer, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 kullanıcı_alanı 시스템 변경분에 적용하며 dağıtım_değer varsayılan_değer 이미지와 base-id는 유지한다. 기존 dosya 백업, 동일 수정의 öğe_değer_58902391 적용 방지, 손상된 수정 dosya 및 다른 base-id reddetmek_değer, kullanıcı_alanı 입력기 Ayarlar 병합에 대한 konak sınamalar 4개도 통과했다. 원래 kullanıcı_alanı veri BLD_RESİM `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 artış_değer·yazı_tipi_değer sınamalar sonuç](build/verification/korean.json)
- [artış_değer·fiili_veri yazı_tipi_değer 로딩 LOG_değer](build/verification/korean.log)
- [Swing·uçbirim 한글 화면](build/verification/korean-desktop.png)
- [Java çalışma_alanı yazı_tipi_değer 화면](build/verification/korean-workbench.png)
- [Ayarlar 보존 sınamalar](build/verification/desktop-update-tests.log)

### 남은 klip

- 새 derlemek_kaynak hedef `openjdk`는 **네이티브 program_Launcher + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 Destek_değer 범위는 여전히 제한적이다.
- yürütmek_komut 프로그램에는 main giriş_noktası, 호환 Sınıf_değer 버전과 의존 JAR/JNI가 필요하다. 개별 상용 program_f5044b9b, 모든 Java modül_değer, 모든 문자권을 시험한 것은 아니다.
- Türkçe Java 라이브러리는 dosya·문자·iletişim·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 Türkçe 번역판은 아니다.
- Pi 4 전용 펌웨어·çekirdek_değer·cihaz_değer 트리는 이미지에 들어 있지만 fiili_veri SD makine_başlatma, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- kullanıcı_alanı dizin_değer 이동은 동일 시스템 BLD_RESİM tanımlayıcı_değer, ARM64, `/home/user`, UID 1000을 전제로 한다. Çıkış_program 후 소유권·izin_değer·링크·uzantı_değer öznitelik_değer·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

yükle_değer·örnek_değer 절차는 [README.md](README.md), derlemek_kaynak 방식은 [OpenJDK yürütmek_komut dosya 안내](../../compiler/OpenJDK-çalıştırılabilir.md)를 따른다. BLD_RESİM 파일만 생성했으며 fiili_veri SD 카드나 USB 디스크에 기록하지 않았다.
