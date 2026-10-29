# 배포 верзија_IMAGE потврди LOG_ред

검증일: 2026-09-27 (Asia/Seoul)

цел: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 자체 x86 커널을 ARM으로 이식한 결과가 아니다. реален_податоци Pi 보드는 연결되어 있지 않아 하드웨어 부팅 성공을 확인하지 못했다.

## 배포물

| Датотека | Големина(бајт_VALUE) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | Архива_VALUE 시스템 верзија_IMAGE; издание_Склад 후 1,475,747,840 бајт_VALUE |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 корисник податоци верзија_IMAGE; издание_Склад 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | Македонски 보조 API와 Java работен_простор |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 Архива_VALUE верзија_IMAGE 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [Архива_VALUE потврди LOG_ред](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU потврди 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 внес_Список](dist/packages.lock.json)과 [원본 출처](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | реален_податоци провери Содржина_VALUE | LOG_ред |
|---|---|---|
| вдоми 컴파일러 시험 19개 | 기존 AOT 회귀 시험, `.class` 직접 입력, OpenJDK ELF програма_стартувач, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, ПАТЕКА премести_VALUE, неуспех_VALUE 시 기존 출력 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi верзија_IMAGE 구조 | MBR 경계, FAT 부팅 파티션, Pi 펌웨어, ARM64 јадро_VALUE, Pi 4 DTB, initramfs, SquashFS 및 хаш_датотека | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, 부팅 후 두 런타임의 реален_податоци Изврши_наредба | [런타임 LOG_ред](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 부팅 | Читај 전용 시스템, Java Датотека·UNICODE_VALUE·исклучок·објект_VALUE·스레드·HTTP/TCP·дете_VALUE 프로세스, Swing, CJK·아랍어·데바나가리 фонт_VALUE, Python Датотека·스레드·소켓·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 Изврши_наредба Датотека генерира | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 Изврши_наредба 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | корисник податоци, `/etc` Подесувања, `/usr/local/bin` програма_f5044b9b, APK로 설치한 tree, pip 패키지, Датотека 삭제 msinfo32_exe, 소유권, sudo, Java Изврши_наредба Датотека 유지 | [restore.log](build/verification/restore.log) |
| информатичка_технологија_Исклучен 홈 премести_VALUE | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 копирај_VALUE | [migrate.log](build/verification/migrate.log) |
| премести_VALUE 후 부팅 | 새 податоци 이미지로 부팅하여 재부팅 복원 항목을 다시 провери | [migrated-restore.log](build/verification/migrated-restore.log) |
| 정상 Излез_програма 및 податоци 무결성 | 일반 부팅 3회 모두 OverlayFS/податоци уред_VALUE Читај 전용 SWITCH_MODE 성공; 원본·복사본 ext4의 `e2fsck -fn` Излез_програма CODE_VALUE 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 SEQUENCE_VALUE 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 Излез_програма CODE_VALUE 0으로 통과했다. [전체 부팅 결과와 LOG_VALUE хаш_датотека](build/verification/boot.json)

QEMU 가상 NIC의 DHCP адреса 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 외부 인터넷이나 Pi Wi-Fi의 потврди 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [화면 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## 구현 범위와 남은 потврди

### QEMU 그래픽 Изврши_наредба 보완

Терминал 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. 배포 시스템 이미지와 base-id는 변경하지 않아 기존 корисник податоци 이미지를 계속 사용할 수 있다.

реален_податоци Xorg/VNC 화면에서 Македонски Java работен_простор, Swing 시험 прозорец, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. Излез_програма 시 시스템 OverlayFS와 податоци 파일시스템의 Читај 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 시험 мерка](build/verification/desktop.json)
- [그래픽 시험 LOG_VALUE](build/verification/desktop.log)
- [키보드·마우스 시험 화면](build/verification/desktop-input.png)
- [인사 예제 화면](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 화면 없는 Изврши_наредба мерка](build/verification/headless-example.log)

ИЗВОР 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 Датотека·문자·스레드 기능을 실행하고 안내를 출력한다. корисник 홈의 기존 원문을 자동 교체하지는 않는다. 향후 верзија_IMAGE 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 입력·фонт_VALUE 보완

`make test-korean`으로 реален_податоци Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space SWITCH_MODE 및 두벌식 Клуч_VALUE 입력을 시험했다. 양쪽에서 `한글 입력`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 корисник податоци 이미지에서 실행했으며 정상 Излез_програма 시 두 파일시스템의 Читај 전용 전환을 확인했다.

Терминал фонт_VALUE 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 реален_податоци Датотека 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 화면 캡처에서 한글·영문 прикажи_VALUE, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 корисник 시스템 변경분에 적용하며 배포 стандардна_вредност 이미지와 base-id는 유지한다. 기존 Датотека 백업, 동일 수정의 повторување_VALUE 적용 방지, 손상된 수정 Датотека 및 다른 base-id одбива_VALUE, корисник 입력기 Подесувања 병합에 대한 вдоми 시험 4개도 통과했다. 원래 корисник податоци верзија_IMAGE `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 입력·фонт_VALUE 시험 мерка](build/verification/korean.json)
- [입력·реален_податоци фонт_VALUE 로딩 LOG_VALUE](build/verification/korean.log)
- [Swing·Терминал 한글 화면](build/verification/korean-desktop.png)
- [Java работен_простор фонт_VALUE 화면](build/verification/korean-workbench.png)
- [Подесувања 보존 시험](build/verification/desktop-update-tests.log)

### 남은 клип

- 새 изгради_извор цел `openjdk`는 **네이티브 програма_стартувач + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 Поддршка_VALUE 범위는 여전히 제한적이다.
- Изврши_наредба 프로그램에는 main внес_поен, 호환 класа_VALUE 버전과 의존 JAR/JNI가 필요하다. 개별 상용 програма_f5044b9b, 모든 Java модул_VALUE, 모든 문자권을 시험한 것은 아니다.
- Македонски Java 라이브러리는 Датотека·문자·통신·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 Македонски 번역판은 아니다.
- Pi 4 전용 펌웨어·јадро_VALUE·уред_VALUE 트리는 이미지에 들어 있지만 реален_податоци SD 부팅, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- корисник Именик_VALUE 이동은 동일 시스템 верзија_IMAGE идентификатор_VALUE, ARM64, `/home/user`, UID 1000을 전제로 한다. Излез_програма 후 소유권·дозвола_VALUE·링크·наставка_VALUE атрибут_VALUE·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

инсталирај_VALUE·копирај_VALUE 절차는 [README.md](README.md), изгради_извор 방식은 [OpenJDK Изврши_наредба Датотека информации_пред_употреба_eb81d7d9](../../compiler/OpenJDK-실행파일.md)를 따른다. верзија_IMAGE 파일만 생성했으며 реален_податоци SD 카드나 USB 디스크에 기록하지 않았다.
