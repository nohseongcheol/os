# توزيع_قيمة بنية_صورة التحقق_من_صحة سجل_سجل

검증일: 2026-09-27 (Asia/Seoul)

الهدف: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 ذاتي x86 커널을 ARM으로 이식한 결과가 아니다. الفعلي_بيانات Pi 보드는 연결되어 있지 않아 أجهزة_قيمة إقلاع_الآلة 성공을 확인하지 못했다.

## 배포물

| ملف | حجم(بايت_قيمة) | 설명 |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | أرشيف_قيمة 시스템 بنية_صورة; إصدار_تخزين 후 1,475,747,840 بايت_قيمة |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 فضاء_المستخدم بيانات بنية_صورة; إصدار_تخزين 후 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/한국어자바.jar` | 10,563 | العربية 보조 API와 Java مساحة_عمل |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 أرشيف_قيمة بنية_صورة 모두 끝까지 해제하여 원본 이미지의 SHA256과 일치함을 확인했다. [أرشيف_قيمة التحقق_من_صحة سجل_سجل](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU التحقق_من_صحة 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 إدخال_قائمة_f07b3200](dist/packages.lock.json)과 [원본 نقطة_الأصل_قيمة](dist/sources.lock.json)를 제공한다.

## 통과한 검사

| 검사 | الفعلي_بيانات يتحقق محتوى_قيمة | سجل_سجل |
|---|---|---|
| مضيف محول_برمجي اختبارات 19개 | 기존 AOT 회귀 اختبارات, `.class` 직접 إدخال_قيمة, OpenJDK ELF تطبيق_مشغّل, JAR 의존성, 상속·리플렉션·람다·스레드·리소스, مسار نقل_قيمة, فشل_قيمة 시 기존 مخرجات 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi بنية_صورة تصميم | MBR 경계, FAT إقلاع_الآلة 파티션, Pi 펌웨어, ARM64 نواة_قيمة, Pi 4 DTB, initramfs, SquashFS 및 تجزئة_ملف | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 검사, إقلاع_الآلة 후 두 런타임의 الفعلي_بيانات ينفذ_أمر | [런타임 سجل_سجل](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| 첫 إقلاع_الآلة | قراءة 전용 시스템, Java ملف·유니코드·استثناء·عنصر_قيمة_2ed200e9·스레드·HTTP/TCP·طفل_قيمة 프로세스, Swing, CJK·아랍어·데바나가리 خط_قيمة, Python ملف·스레드·مأخذ_التوصيل_قيمة·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 ينفذ_أمر ملف إنشاء | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 ينفذ_أمر 성공 | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | فضاء_المستخدم بيانات, `/etc` إعدادات, `/usr/local/bin` تطبيق_f5044b9b, APK로 설치한 tree, pip 패키지, ملف 삭제 معلومات_النظام, 소유권, sudo, Java ينفذ_أمر ملف 유지 | [restore.log](build/verification/restore.log) |
| أنظمة_المعلومات_غير_متصل 홈 نقل_قيمة | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 مثيل_قيمة | [migrate.log](build/verification/migrate.log) |
| نقل_قيمة 후 إقلاع_الآلة | 새 بيانات 이미지로 부팅하여 재부팅 복원 항목을 إعادة_محاولة_قيمة يتحقق | [migrated-restore.log](build/verification/migrated-restore.log) |
| أنظمة_المعلومات_عادي خروج_تطبيق 및 بيانات 무결성 | 일반 إقلاع_الآلة 3회 모두 OverlayFS/بيانات جهاز_قيمة قراءة 전용 تبديل_الوضع 성공; 원본·복사본 ext4의 `e2fsck -fn` خروج_تطبيق رمز_قيمة_f3cd31ee 0 | [원본 검사](build/verification/fsck-original.log), [복사본 검사](build/verification/fsck-migrated.log) |

네 تسلسل_قيمة 부팅은 모두 QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 خروج_تطبيق رمز_قيمة_f3cd31ee 0으로 통과했다. [전체 إقلاع_الآلة 결과와 سجل_قيمة تجزئة_ملف](build/verification/boot.json)

QEMU 가상 NIC의 DHCP عنوان 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 خارجي_قيمة 인터넷이나 Pi Wi-Fi의 التحقق_من_صحة 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [화면 캡처](build/verification/swing.png)에서 한글·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## 구현 범위와 남은 التحقق_من_صحة

### QEMU 그래픽 ينفذ_أمر 보완

طرفية 전용 실행에서 `인사.java`가 Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. توزيع_قيمة 시스템 이미지와 base-id는 변경하지 않아 기존 فضاء_المستخدم بيانات 이미지를 계속 사용할 رقم 있다.

الفعلي_بيانات Xorg/VNC 화면에서 العربية Java مساحة_عمل, Swing اختبارات نافذة, 기존 이미지의 `인사.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. خروج_تطبيق 시 시스템 OverlayFS와 بيانات 파일시스템의 قراءة 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 اختبارات نتيجة](build/verification/desktop.json)
- [그래픽 اختبارات سجل_قيمة](build/verification/desktop.log)
- [키보드·마우스 اختبارات 화면](build/verification/desktop-input.png)
- [인사 예제 화면](build/verification/desktop-greeting.png)
- [수정한 예제 원문의 화면 없는 ينفذ_أمر نتيجة](build/verification/headless-example.log)

مصدر 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 ملف·문자·스레드 기능을 실행하고 안내를 출력한다. فضاء_المستخدم 홈의 기존 원문을 자동 교체하지는 않는다. 향후 بنية_صورة 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### 한글 إدخال_قيمة·خط_قيمة 보완

`make test-korean`으로 الفعلي_بيانات Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space تبديل_الوضع 및 두벌식 مفتاح_قيمة 입력을 시험했다. 양쪽에서 `한글 إدخال_قيمة`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 فضاء_المستخدم بيانات 이미지에서 실행했으며 أنظمة_المعلومات_عادي خروج_تطبيق 시 두 파일시스템의 قراءة 전용 전환을 확인했다.

طرفية خط_قيمة 진단에서 영문 DejaVu Sans Mono와 한글 Noto Sans Mono CJK KR의 الفعلي_بيانات ملف 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. 화면 캡처에서 한글·영문 عرض_قيمة_487749b8, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 فضاء_المستخدم 시스템 변경분에 적용하며 توزيع_قيمة قيمة_افتراضية 이미지와 base-id는 유지한다. 기존 ملف 백업, 동일 수정의 تكرار_قيمة 적용 방지, 손상된 수정 ملف 및 다른 base-id يرفض_قيمة, فضاء_المستخدم 입력기 إعدادات 병합에 대한 مضيف اختبارات 4개도 통과했다. 원래 فضاء_المستخدم بيانات بنية_صورة `build/manual-user.img`는 시험에 사용하지 않았다.

- [한글 إدخال_قيمة·خط_قيمة اختبارات نتيجة](build/verification/korean.json)
- [إدخال_قيمة·الفعلي_بيانات خط_قيمة 로딩 سجل_قيمة](build/verification/korean.log)
- [Swing·طرفية 한글 화면](build/verification/korean-desktop.png)
- [Java مساحة_عمل خط_قيمة 화면](build/verification/korean-workbench.png)
- [إعدادات 보존 اختبارات](build/verification/desktop-update-tests.log)

### 남은 يقص

- 새 يحول_برمجياً_مصدر الهدف `openjdk`는 **네이티브 تطبيق_مشغّل + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 دعم_قيمة 범위는 여전히 제한적이다.
- ينفذ_أمر 프로그램에는 main نقطة_الإدخال, 호환 فئة_قيمة_55654bf1 버전과 의존 JAR/JNI가 필요하다. 개별 상용 تطبيق_f5044b9b, 모든 Java وحدة_نمطية_قيمة, 모든 문자권을 시험한 것은 아니다.
- العربية Java 라이브러리는 ملف·문자·통신·스레드·Swing을 위한 보조 API이며 JDK 전체 API의 العربية 번역판은 아니다.
- Pi 4 전용 펌웨어·نواة_قيمة·جهاز_قيمة 트리는 이미지에 들어 있지만 الفعلي_بيانات SD إقلاع_الآلة, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 한글 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- فضاء_المستخدم دليل_قيمة 이동은 동일 시스템 بنية_صورة معرف_قيمة, ARM64, `/home/user`, UID 1000을 전제로 한다. خروج_تطبيق 후 소유권·إذن_قيمة·링크·ملحق_قيمة قيمة_السمة·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

تثبيت_قيمة·مثيل_قيمة 절차는 [README.md](README.md), يحول_برمجياً_مصدر 방식은 [OpenJDK ينفذ_أمر ملف 안내](../../compiler/OpenJDK-실행파일.md)를 따른다. بنية_صورة 파일만 생성했으며 الفعلي_بيانات SD 카드나 USB 디스크에 기록하지 않았다.
