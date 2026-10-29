# הפצה_ערך בנה_תמונה לאמת לרשום_שיא

검증일: 2026-09-27 (Asia/Seoul)

יעד: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 עצמי x86 커널을 ARM으로 이식한 결과가 아니다. בפועל_נתונים Pi 보드는 연결되어 있지 않아 חומרה_ערך_9591fb0a 부팅 성공을 확인하지 못했다.

## 배포물

| קובץ | גודל(בית_ערך) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | ארכיון_ערך 시스템 בנה_תמונה; לשחרר_אחסון 후 1,475,747,840 בית_ערך |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 משתמש נתונים בנה_תמונה; לשחרר_אחסון 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | עברית 보조 API와 Java סביבת_עבודה |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 ארכיון_ערך בנה_תמונה 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [ארכיון_ערך לאמת לרשום_שיא](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU לאמת 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 ערך_רשימה](dist/packages.lock.json)과 [원본 מקור_ערך](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | בפועל_נתונים ודא_אמת תוכן_ערך | לרשום_שיא |
|---|---|---|
| ארח מהדר 시험 19개 | 기존 AOT 회귀 시험, `.class` 직접 קלט_ערך, OpenJDK ELF תוכנית_מפעיל, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, נתיב להעביר_ערך, כשל_ערך 시 기존 פלטטקסט 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi בנה_תמונה ארכיטקטורה | MBR 경계, FAT 부팅 파티션, Pi 펌웨어, ARM64 ליבה_ערך, Pi 4 DTB, initramfs, SquashFS 및 קוד_Hash_קובץ | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, 부팅 후 두 런타임의 בפועל_נתונים לבצע_פקודה | [런타임 לרשום_שיא](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 부팅 | קרא 전용 시스템, Java קובץ·יוניקוד_ערך·חריגה·אובייקט_ערך·스레드·HTTP/TCP·ילד_ערך 프로세스, Swing, CJK·아랍어·데바나가리 גופן_ערך, Python קובץ·스레드·소켓·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 לבצע_פקודה קובץ יצר | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 לבצע_פקודה 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | משתמש נתונים, `/etc` הגדרות, `/usr/local/bin` תוכנית_f5044b9b, APK로 설치한 tree, pip 패키지, קובץ 삭제 מידע_מערכת, 소유권, sudo, Java לבצע_פקודה קובץ 유지 | [restore.log](build/verification/restore.log) |
| מערכות_מידע_לא_מקוון 홈 להעביר_ערך | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 מופע_ערך | [migrate.log](build/verification/migrate.log) |
| להעביר_ערך 후 부팅 | 새 נתונים 이미지로 부팅하여 재부팅 복원 항목을 נסה_שנית_ערך ודא_אמת | [migrated-restore.log](build/verification/migrated-restore.log) |
| מערכות_מידע_רגיל יציאה_תוכנית 및 נתונים 무결성 | 일반 부팅 3회 모두 OverlayFS/נתונים התקן_ערך_e13f0cd9 קרא 전용 מתג_מצב 성공; 원본·복사본 ext4의 `e2fsck -fn` יציאה_תוכנית קוד_ערך 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 רצף_ערך 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 יציאה_תוכנית קוד_ערך 0으로 통과했다. [전체 부팅 결과와 לרשום_ערך קוד_Hash_קובץ](build/verification/boot.json)

QEMU 가상 NIC의 DHCP למען 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 חיצוני_ערך 인터넷이나 Pi Wi-Fi의 לאמת 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [화면 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## 구현 범위와 남은 לאמת

### QEMU 그래픽 לבצע_פקודה 보완

מסוף 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. הפצה_ערך 시스템 이미지와 base-id는 변경하지 않아 기존 משתמש נתונים 이미지를 계속 사용할 수 있다.

בפועל_נתונים Xorg/VNC 화면에서 עברית Java סביבת_עבודה, Swing 시험 חלון, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. יציאה_תוכנית 시 시스템 OverlayFS와 נתונים 파일시스템의 קרא 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 시험 תוצאה](build/verification/desktop.json)
- [그래픽 시험 לרשום_ערך](build/verification/desktop.log)
- [키보드·마우스 시험 화면](build/verification/desktop-input.png)
- [인사 예제 화면](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 화면 없는 לבצע_פקודה תוצאה](build/verification/headless-example.log)

קודמקור 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 קובץ·문자·스레드 기능을 실행하고 안내를 출력한다. משתמש 홈의 기존 원문을 자동 교체하지는 않는다. 향후 בנה_תמונה 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 קלט_ערך·גופן_ערך 보완

`make test-korean`으로 בפועל_נתונים Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space מתג_מצב 및 두벌식 מקש_ערך 입력을 시험했다. 양쪽에서 `한글 קלט_ערך`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 משתמש נתונים 이미지에서 실행했으며 מערכות_מידע_רגיל יציאה_תוכנית 시 두 파일시스템의 קרא 전용 전환을 확인했다.

מסוף גופן_ערך 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 בפועל_נתונים קובץ 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 화면 캡처에서 한글·영문 הופעה_ערך, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 משתמש 시스템 변경분에 적용하며 הפצה_ערך ערך_ברירת_מחדל 이미지와 base-id는 유지한다. 기존 קובץ 백업, 동일 수정의 סבב_ערך 적용 방지, 손상된 수정 קובץ 및 다른 base-id דחייה_ערך, משתמש 입력기 הגדרות 병합에 대한 ארח 시험 4개도 통과했다. 원래 משתמש נתונים בנה_תמונה `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 קלט_ערך·גופן_ערך 시험 תוצאה](build/verification/korean.json)
- [קלט_ערך·בפועל_נתונים גופן_ערך 로딩 לרשום_ערך](build/verification/korean.log)
- [Swing·מסוף 한글 화면](build/verification/korean-desktop.png)
- [Java סביבת_עבודה גופן_ערך 화면](build/verification/korean-workbench.png)
- [הגדרות 보존 시험](build/verification/desktop-update-tests.log)

### 남은 לגזור

- 새 בנה_מקור יעד `openjdk`는 **네이티브 תוכנית_מפעיל + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 תמך_ערך 범위는 여전히 제한적이다.
- לבצע_פקודה 프로그램에는 main נקודת_כניסה, 호환 כיתה_ערך 버전과 의존 JAR/JNI가 필요하다. 개별 상용 תוכנית_f5044b9b, 모든 Java מודול_ערך, 모든 문자권을 시험한 것은 아니다.
- עברית Java 라이브러리는 קובץ·문자·통신·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 עברית 번역판은 아니다.
- Pi 4 전용 펌웨어·ליבה_ערך·התקן_ערך_e13f0cd9 트리는 이미지에 들어 있지만 בפועל_נתונים SD 부팅, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- משתמש מדריך_ערך 이동은 동일 시스템 בנה_תמונה מזהה_ערך, ARM64, `/home/user`, UID 1000을 전제로 한다. יציאה_תוכנית 후 소유권·הרשאה_ערך·링크·הרחבה_ערך ערך_תכונה·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

התקן_ערך·מופע_ערך 절차는 [README.md](README.md), בנה_מקור 방식은 [OpenJDK לבצע_פקודה קובץ 안내](../../compiler/OpenJDK-실행파일.md)를 따른다. בנה_תמונה 파일만 생성했으며 בפועל_נתונים SD 카드나 USB 디스크에 기록하지 않았다.
