# giáTrịBảnPhânPhối xâyDựngẢnh thẩmĐịnh bảnGhiNhậtKý

검증일: 2026-09-27 (Asia/Seoul)

giáTrịĐốiĐích: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 tựThân x86 커널을 ARM으로 이식한 결과가 아니다. dữLiệuThựcTế Pi 보드는 연결되어 있지 않아 giáTrịPhầnCứng KhởiĐộng 성공을 확인하지 못했다.

## 배포물

| Tệp | cỡ(giáTrịByte) | môTả |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | giáTrịKhoLưuTrữ 시스템 xâyDựngẢnh; giảiPhóngLưuTrữ trạngTháiSau 1,475,747,840 giáTrịByte |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 NgườiDùng DữLiệu xâyDựngẢnh; giảiPhóngLưuTrữ trạngTháiSau 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/JavaTiếngViệt.jar` | 10,563 | tiếngViệt giáTrịPhụTrợ API와 Java KhôngGianLàmViệc |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 giáTrịKhoLưuTrữ xâyDựngẢnh xâyDựngTấtCả 끝까지 해제하여 nguyênBản 이미지의 SHA256과 일치함을 확인했다. [giáTrịKhoLưuTrữ thẩmĐịnh bảnGhiNhậtKý](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU thẩmĐịnh 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 danhSáchMục](dist/packages.lock.json)과 [nguyênBản giáTrịGốc](dist/sources.lock.json)를 제공한다.

## 통과한 CácPhépKiểmTra

| CácPhépKiểmTra | dữLiệuThựcTế xácMinh giáTrịNộiDung | bảnGhiNhậtKý |
|---|---|---|
| Chủ TrìnhBiênDịch KiểmThử 19개 | 기존 AOT 회귀 KiểmThử, `.class` 직접 giáTrịVào, OpenJDK ELF TrìnhKhởiChạyChươngTrình, JAR cácPhụThuộc, 상속·리플렉션·람다·스레드·리소스, đườngDẫn giáTrịDiChuyển, giáTrịSựThấtBại 시 기존 ĐầuRa 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi xâyDựngẢnh KiếnTrúc | MBR giáTrịRanhGiới, FAT KhởiĐộng 파티션, Pi 펌웨어, ARM64 giáTrịNhân, Pi 4 DTB, initramfs, SquashFS 및 tệpMãBăm | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 CácPhépKiểmTra, KhởiĐộng trạngTháiSau 두 런타임의 dữLiệuThựcTế thựcThiLệnh | [런타임 bảnGhiNhậtKý](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| phầnMụcĐầuTiên KhởiĐộng | đọc 전용 시스템, Java Tệp·giáTrịUnicode·ngoạiLệ·giáTrịĐốiTượng·스레드·HTTP/TCP·giáTrịCon 프로세스, Swing, CJK·아랍어·데바나가리 giáTrịPhôngChữ, Python Tệp·스레드·giáTrịỔCắmMạng·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 thựcThiLệnh Tệp sinh | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 thựcThiLệnh giáTrịThànhCông | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | NgườiDùng DữLiệu, `/etc` cácThiếtLập, `/usr/local/bin` ChươngTrình, APK로 설치한 tree, pip 패키지, Tệp 삭제 thôngTinHệThống, 소유권, sudo, Java thựcThiLệnh Tệp giữLạiGiáTrị | [restore.log](build/verification/restore.log) |
| làNgoạiTuyến 홈 giáTrịDiChuyển | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 saoChépGiáTrị | [migrate.log](build/verification/migrate.log) |
| giáTrịDiChuyển trạngTháiSau KhởiĐộng | 새 DữLiệu 이미지로 부팅하여 재부팅 복원 항목을 giáTrịThửLại xácMinh | [migrated-restore.log](build/verification/migrated-restore.log) |
| làBìnhThường chươngTrìnhRa 및 DữLiệu 무결성 | 일반 KhởiĐộng 3회 xâyDựngTấtCả OverlayFS/DữLiệu ThiếtBị đọc 전용 chếĐộChuyển giáTrịThànhCông; nguyênBản·giáTrịĐãSaoChép ext4의 `e2fsck -fn` chươngTrìnhRa giáTrịMã 0 | [nguyênBản CácPhépKiểmTra](build/verification/fsck-original.log), [giáTrịĐãSaoChép CácPhépKiểmTra](build/verification/fsck-migrated.log) |

네 giáTrịDãy 부팅은 xâyDựngTấtCả QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 chươngTrìnhRa giáTrịMã 0으로 통과했다. [전체 KhởiĐộng 결과와 giáTrịNhậtKý tệpMãBăm](build/verification/boot.json)

QEMU 가상 NIC의 DHCP địaChỉ 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 giáTrịBênNgoài 인터넷이나 Pi Wi-Fi의 thẩmĐịnh 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [MànHình 캡처](build/verification/swing.png)에서 vănBảnHangul·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## phầnCàiĐặt 범위와 남은 thẩmĐịnh

### QEMU 그래픽 thựcThiLệnh 보완

thiếtBịCuối 전용 실행에서 `LờiChào.java`toánHạngĐầuTiên Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. giáTrịBảnPhânPhối 시스템 이미지와 base-id는 변경하지 않아 기존 NgườiDùng DữLiệu 이미지를 việcXửLýTiếpTục 사용할 trịSố 있다.

dữLiệuThựcTế Xorg/VNC 화면에서 tiếngViệt Java KhôngGianLàmViệc, Swing KiểmThử cửaSổ, 기존 이미지의 `LờiChào.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. chươngTrìnhRa 시 시스템 OverlayFS와 DữLiệu 파일시스템의 đọc 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 KiểmThử kếtQuả](build/verification/desktop.json)
- [그래픽 KiểmThử giáTrịNhậtKý](build/verification/desktop.log)
- [키보드·마우스 KiểmThử MànHình](build/verification/desktop-input.png)
- [LờiChào VíDụ MànHình](build/verification/desktop-greeting.png)
- [수정한 VíDụ 원문의 MànHình 없는 thựcThiLệnh kếtQuả](build/verification/headless-example.log)

mãNguồn 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 Tệp·KýTự·스레드 기능을 실행하고 안내를 출력한다. NgườiDùng 홈의 기존 원문을 자동 교체하지는 않는다. 향후 xâyDựngẢnh 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### vănBảnHangul giáTrịVào·giáTrịPhôngChữ 보완

`make test-korean`으로 dữLiệuThựcTế Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space chếĐộChuyển 및 두벌식 giáTrịPhím 입력을 시험했다. 양쪽에서 `vănBảnHangul giáTrịVào`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 NgườiDùng DữLiệu 이미지에서 실행했으며 làBìnhThường chươngTrìnhRa 시 두 파일시스템의 đọc 전용 전환을 확인했다.

thiếtBịCuối giáTrịPhôngChữ 진단에서 영문 DejaVu Sans Mono와 vănBảnHangul Noto Sans Mono CJK KR의 dữLiệuThựcTế Tệp 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. MànHình 캡처에서 vănBảnHangul·영문 hiệnGiáTrị, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 NgườiDùng 시스템 변경분에 적용하며 giáTrịBảnPhânPhối giáTrịMặcĐịnh 이미지와 base-id는 유지한다. 기존 Tệp 백업, 동일 수정의 giáTrịLầnLặp 적용 방지, 손상된 chỉnhSửaGiáTrị Tệp 및 다른 base-id từChốiGiáTrị, NgườiDùng 입력기 cácThiếtLập 병합에 대한 Chủ KiểmThử 4개도 통과했다. 원래 NgườiDùng DữLiệu xâyDựngẢnh `build/manual-user.img`는 시험에 사용하지 않았다.

- [vănBảnHangul giáTrịVào·giáTrịPhôngChữ KiểmThử kếtQuả](build/verification/korean.json)
- [giáTrịVào·dữLiệuThựcTế giáTrịPhôngChữ 로딩 giáTrịNhậtKý](build/verification/korean.log)
- [Swing·thiếtBịCuối vănBảnHangul MànHình](build/verification/korean-desktop.png)
- [Java KhôngGianLàmViệc giáTrịPhôngChữ MànHình](build/verification/korean-workbench.png)
- [cácThiếtLập 보존 KiểmThử](build/verification/desktop-update-tests.log)

### 남은 cắtXén

- 새 biênDịchNguồn giáTrịĐốiĐích `openjdk`는 **네이티브 TrìnhKhởiChạyChươngTrình + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 giáTrịHỗTrợ 범위는 여전히 제한적이다.
- thựcThiLệnh 프로그램에는 main điểmMục, 호환 giáTrịLớp 버전과 의존 JAR/JNI가 필요하다. 개별 상용 ChươngTrình, 모든 Java giáTrịMôĐun, 모든 문자권을 시험한 것은 아니다.
- tiếngViệt Java 라이브러리는 Tệp·KýTự·TruyềnThông·스레드·Swing을 위한 giáTrịPhụTrợ API이며 JDK 전체 API의 tiếngViệt 번역판은 아니다.
- Pi 4 전용 펌웨어·giáTrịNhân·ThiếtBị 트리는 이미지에 들어 있지만 dữLiệuThựcTế SD KhởiĐộng, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 vănBảnHangul 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- NgườiDùng giáTrịThưMục 이동은 동일 시스템 xâyDựngẢnh giáTrịĐịnhDanh, ARM64, `/home/user`, UID 1000을 전제로 한다. chươngTrìnhRa trạngTháiSau 소유권·giáTrịQuyền·링크·giáTrịPhầnMởRộng giáTrịThuộcTính·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

càiĐặtGiáTrị·saoChépGiáTrị 절차는 [README.md](README.md), biênDịchNguồn 방식은 [OpenJDK thựcThiLệnh Tệp HướngDẫn](../../compiler/OpenJDK-tệpTệpThựcThi.md)를 따른다. xâyDựngẢnh 파일만 생성했으며 dữLiệuThựcTế SD 카드나 USB 디스크에 기록하지 않았다.
