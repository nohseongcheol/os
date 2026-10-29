# dystrybucja_WARTOŚĆ BLD_OBRAZ walidować LOG_zapis

검증일: 2026-09-27 (Asia/Seoul)

wartość_docelowa: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 własny x86 커널을 ARM으로 이식한 결과가 아니다. rzeczywisty_dane Pi 보드는 연결되어 있지 않아 sprzęt_WARTOŚĆ rozruch_maszyny 성공을 확인하지 못했다.

## 배포물

| nazwa_pliku | Rozmiar(bajt_WARTOŚĆ) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | Archiwum_WARTOŚĆ 시스템 BLD_OBRAZ; wersja_Pamięć 후 1,475,747,840 bajt_WARTOŚĆ |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 przestrzeń_użytkownika dane BLD_OBRAZ; wersja_Pamięć 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | polski 보조 API와 Java obszar_roboczy |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 Archiwum_WARTOŚĆ BLD_OBRAZ 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [Archiwum_WARTOŚĆ walidować LOG_zapis](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU walidować 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 wpis_Lista](dist/packages.lock.json)과 [원본 źródło_WARTOŚĆ](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | rzeczywisty_dane 확인 treść_WARTOŚĆ_cb0f2404 | LOG_zapis |
|---|---|---|
| host kompilator testy 19개 | 기존 AOT 회귀 testy, `.class` 직접 wejście_WARTOŚĆ, OpenJDK ELF program_Launcher, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, ścieżka_2 przenosić_WARTOŚĆ, awaria_WARTOŚĆ 시 기존 pozycja_wyjścia 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi BLD_OBRAZ architektura | MBR granica_WARTOŚĆ, FAT rozruch_maszyny 파티션, Pi 펌웨어, ARM64 jądro_WARTOŚĆ, Pi 4 DTB, initramfs, SquashFS 및 skrót_Plik | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, rozruch_maszyny 후 두 런타임의 rzeczywisty_dane Wykonaj_polecenie | [런타임 LOG_zapis](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 rozruch_maszyny | Odczyt 전용 시스템, Java nazwa_pliku·UNICODE_WARTOŚĆ·wyjątek·obiekt_WARTOŚĆ·스레드·HTTP/TCP·dziecko_WARTOŚĆ 프로세스, Swing, CJK·아랍어·데바나가리 czcionka_WARTOŚĆ, Python nazwa_pliku·스레드·gniazdo_WARTOŚĆ·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 Wykonaj_polecenie nazwa_pliku generować | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 Wykonaj_polecenie 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | przestrzeń_użytkownika dane, `/etc` Ustawienia, `/usr/local/bin` program_f5044b9b, APK로 설치한 tree, pip 패키지, nazwa_pliku 삭제 msinfo32_exe, 소유권, sudo, Java Wykonaj_polecenie nazwa_pliku 유지 | [restore.log](build/verification/restore.log) |
| systemy_informacyjne_offline 홈 przenosić_WARTOŚĆ | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 kopiować_WARTOŚĆ | [migrate.log](build/verification/migrate.log) |
| przenosić_WARTOŚĆ 후 rozruch_maszyny | 새 dane 이미지로 부팅하여 재부팅 복원 항목을 다시 확인 | [migrated-restore.log](build/verification/migrated-restore.log) |
| systemy_informacyjne_zwykła wyjść_program 및 dane 무결성 | 일반 rozruch_maszyny 3회 모두 OverlayFS/dane urządzenie_WARTOŚĆ Odczyt 전용 zmiana_tryb 성공; 원본·복사본 ext4의 `e2fsck -fn` wyjść_program KOD_WARTOŚĆ 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 SEKWENCJA_WARTOŚĆ 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 wyjść_program KOD_WARTOŚĆ 0으로 통과했다. [전체 rozruch_maszyny 결과와 LOG_WARTOŚĆ skrót_Plik](build/verification/boot.json)

QEMU 가상 NIC의 DHCP Adres 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 zewnętrzny_WARTOŚĆ 인터넷이나 Pi Wi-Fi의 walidować 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [화면 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## implementacja 범위와 남은 walidować

### QEMU 그래픽 Wykonaj_polecenie 보완

interpretator_poleceń 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. dystrybucja_WARTOŚĆ 시스템 이미지와 base-id는 변경하지 않아 기존 przestrzeń_użytkownika dane 이미지를 계속 사용할 identyfikator 있다.

rzeczywisty_dane Xorg/VNC 화면에서 polski Java obszar_roboczy, Swing testy Okno, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. wyjść_program 시 시스템 OverlayFS와 dane 파일시스템의 Odczyt 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 testy WYNIK](build/verification/desktop.json)
- [그래픽 testy LOG_WARTOŚĆ](build/verification/desktop.log)
- [키보드·마우스 testy 화면](build/verification/desktop-input.png)
- [인사 예제 화면](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 화면 없는 Wykonaj_polecenie WYNIK](build/verification/headless-example.log)

plik_źródłowy 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 nazwa_pliku·문자·스레드 기능을 실행하고 안내를 출력한다. przestrzeń_użytkownika 홈의 기존 원문을 자동 교체하지는 않는다. 향후 BLD_OBRAZ 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 wejście_WARTOŚĆ·czcionka_WARTOŚĆ 보완

`make test-korean`으로 rzeczywisty_dane Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space zmiana_tryb 및 두벌식 Klucz_WARTOŚĆ 입력을 시험했다. 양쪽에서 `한글 wejście_WARTOŚĆ`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 przestrzeń_użytkownika dane 이미지에서 실행했으며 systemy_informacyjne_zwykła wyjść_program 시 두 파일시스템의 Odczyt 전용 전환을 확인했다.

interpretator_poleceń czcionka_WARTOŚĆ 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 rzeczywisty_dane nazwa_pliku 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 화면 캡처에서 한글·영문 program_WARTOŚĆ, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 przestrzeń_użytkownika 시스템 변경분에 적용하며 dystrybucja_WARTOŚĆ wartość_domyślna 이미지와 base-id는 유지한다. 기존 nazwa_pliku 백업, 동일 수정의 iteracja_WARTOŚĆ 적용 방지, 손상된 수정 nazwa_pliku 및 다른 base-id odrzucić_WARTOŚĆ, przestrzeń_użytkownika 입력기 Ustawienia 병합에 대한 host testy 4개도 통과했다. 원래 przestrzeń_użytkownika dane BLD_OBRAZ `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 wejście_WARTOŚĆ·czcionka_WARTOŚĆ testy WYNIK](build/verification/korean.json)
- [wejście_WARTOŚĆ·rzeczywisty_dane czcionka_WARTOŚĆ 로딩 LOG_WARTOŚĆ](build/verification/korean.log)
- [Swing·interpretator_poleceń 한글 화면](build/verification/korean-desktop.png)
- [Java obszar_roboczy czcionka_WARTOŚĆ 화면](build/verification/korean-workbench.png)
- [Ustawienia 보존 testy](build/verification/desktop-update-tests.log)

### 남은 obcinać

- 새 kompilować_źródło wartość_docelowa `openjdk`는 **네이티브 program_Launcher + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 wsparcie_WARTOŚĆ 범위는 여전히 제한적이다.
- Wykonaj_polecenie 프로그램에는 main punkt_wejścia, 호환 Klasa_WARTOŚĆ 버전과 의존 JAR/JNI가 필요하다. 개별 상용 program_f5044b9b, 모든 Java moduł_WARTOŚĆ, 모든 문자권을 시험한 것은 아니다.
- polski Java 라이브러리는 nazwa_pliku·문자·komunikacja·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 polski 번역판은 아니다.
- Pi 4 전용 펌웨어·jądro_WARTOŚĆ·urządzenie_WARTOŚĆ 트리는 이미지에 들어 있지만 rzeczywisty_dane SD rozruch_maszyny, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- przestrzeń_użytkownika Katalog_WARTOŚĆ 이동은 동일 시스템 BLD_OBRAZ identyfikator_WARTOŚĆ, ARM64, `/home/user`, UID 1000을 전제로 한다. wyjść_program 후 소유권·pozwolenie_WARTOŚĆ·링크·rozszerzenie_WARTOŚĆ wartość_atrybutu·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

instalować_WARTOŚĆ·kopiować_WARTOŚĆ 절차는 [README.md](README.md), kompilować_źródło 방식은 [OpenJDK Wykonaj_polecenie nazwa_pliku plik_README_eb81d7d9](../../compiler/OpenJDK-plik_wykonywalny.md)를 따른다. BLD_OBRAZ 파일만 생성했으며 rzeczywisty_dane SD 카드나 USB 디스크에 기록하지 않았다.
