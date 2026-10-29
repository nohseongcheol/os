# Raspberry Pi 4 tựThân Java giáTrịNhân — NgườiDùng thựcThiLệnh nềnTảng

phầnMụcHiệnTại tựThân 코드의 COSL 상업 điềuKiện, 제3자 고지 및 LGPL điểmCuốiKếtNốiLại 자료는 [COSL giáTrịBảnPhânPhối HướngDẫn](HướngDẫnBảnPhânPhốiCOSL.md)를 참고한다. chếĐộChuyển giáTrịTrướcKhi GPL 구성의 판단은 [phầnMụcTrướcĐó 라이선스 검토](XemDuyệtGiấyPhép.md)에 기록했다.

tiếngViệt TruyềnThông·ngoạiLệ 사용법은 [tiếngViệt Java API](JavaTiếngViệt/HướngDẫn.md), Hàm·giáTrịBiến·Tệp 이름의 변경과 어원 근거는 [cáchĐặtTên HướngDẫn](cáchĐặtTên/HướngDẫn.md)를 참고한다.

Linux 없이 부팅하는 tựThân AArch64 커널이다. Java AOT giáTrịNhân 위에 **dòngLệnh vỏLệnh, 게스트 Java TrìnhBiênDịch·JVM, MicroPython, EL0 C++ thựcThiLệnh, Tệp·UDP 루프백 시스템 gọiThựcHiện, 여러 vănBảnHangul GUI thiếtBịCuối·vi TrìnhSoạnThảo·Swing 부분집합**을 제공한다. 커널의 Tệp DữLiệu/정책·루프백 giáTrịChuyểnGiao·vỏLệnh 상태는 Java, MànHình 합성·điểmẢnh đổiGiáTrị·conTrỏ·클리핑도 Java로 구현하며, CPU/MMU/ThiếtBị 경계와 thiếtBịCuối·giáTrịKýTự mànHìnhTô 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 tựThân 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 thựcThiLệnh, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](ViệcBiênDịchVàChuyểnGiaoTệp.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, phầnCứngVậtLý Pi4의 giáTrịHữuTuyến 송수신은 아직 미검증이다.** thựcThiLệnh·kếtNối·giáTrịMậtKhẩu 확인은 [giáTrịBênNgoài kếtNối HướngDẫn](HướngDẫnKếtNốiBênNgoài.md)에 정리했다.

셸은 EL1 giáTrịNhân, `java` 등 NgườiDùng thựcThiLệnh 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 giáTrịGiớiHạn, QEMU 네트워크 thựcThiLệnh·kếtNối 방법 및 dữLiệuThựcTế 검증은
[thựcThiLệnh 계층과 giáTrịBênNgoài TruyềnThông xemXétTrạngThái](CácPhépKiểmTraMạngBênNgoàiVàMôiTrườngChạy.md)을 참고한다.

ELF는 확장자가 아닌 dữLiệuThựcTế thựcThiLệnh 형식으로 검사한다. `./LờiChào`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 giáTrịTĩnh ELF는 `run --linux vănBảnTênTệp`으로 실행한다. [ELF·Linux ABI giáTrịHỗTrợ 범위와 동일 바이너리 KiểmThử](aBITệpThựcThi.md).

GUI와 네트워크는 `python3 CôngCụ/thựcThiLệnh.py --desktop --network`로 함께 사용한다. Java·C·Python의 tiếngViệt VíDụ 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 KhởiĐộng 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 trịSố 있다. Remmina에서 **F9/Shift+Space/한·toánHạngKhôngSố giáTrịPhím**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·dữLiệuThựcTế TCP/UDP·Tệp giáTrịByte·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` trạngTháiSau `java VíDụCửaSổ`로 tiếngViệt Swing 예제를 실행한다. thiếtBịCuối 모서리에 마우스를 대고 **bênTrái 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 phầnMụcHiệnTại giáTrịCột·giáTrịHàng 수를 보여 준다.

## phầnMụcHiệnTại giáTrịHỗTrợ cắtXén

| 기능 | phầnCàiĐặt·시험한 cắtXén | 아직 làKhôngHỗTrợ |
|---|---|---|
| KhởiĐộng | Pi4 AArch64 EL1, UART, SD용 xâyDựngẢnh, QEMU raspi4b KhởiĐộng | dữLiệuThựcTế Pi4 보드에서의 펌웨어 KhởiĐộng KiểmThử |
| Java giáTrịNhân | giáTrịTĩnh Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java giáTrịĐốiTượng/ngoạiLệ/GC/JVM/표준 thưViện |
| Java phátTriển CôngCụ | 게스트 tựThân `javac`/`java`, JVM 0.4/JAR: 다중 giáTrịLớp·giáTrịĐốiTượng·상속·ngoạiLệ·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, tiếngViệt thưViện. 게스트 컴파일러는 giáTrịTĩnh Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | dữLiệuThựcTế MicroPython 1.24.1 EL0 ChuyểnNền, câyNguồn biênDịchNguồn/thựcThiLệnh, giáTrịLớp·ngoạiLệ·GC·큰 SốNguyên·Unicode·Tệp·UDP/MànHình nốiKết | CPython, pip, C giáTrịPhầnMởRộng, 부동소수점, 일반 OS/스레드/giáTrịỔCắmMạng giáTrịMôĐun, tươngTác REPL |
| vỏLệnh | UTF-8 giáTrịSửa·bảnGhiNhậtKý·giáTrịĐãHoànTất, 디렉터리·Tệp lệnh, giáTrịBiến·điềuKiện·giáTrịKịchBản, 16 KiB 순차 파이프·리다이렉션, ELF thựcThiLệnh | 전체 POSIX sh/Bash, TácVụ giáTrịĐiềuKhiển·동시 프로세스·PTY |
| C/AOT biênDịchNguồn | 게스트 TinyCC 및 giáTrịTĩnh Java 부분집합 `jaot` → tựThân ARM64 ELF | 전체 libc·모든 Java giáTrịLớp AOT |
| C++ | 독립 ELF64를 EL0에서 thựcThiLệnh; giáTrịTĩnh 생성자, RAII 소멸자, FP/SIMD, tiếngViệt Tệp/루프백 gọiThựcHiện | libc/libstdc++, STL, C++ ngoạiLệ·RTTI·동적 nốiKết |
| NgườiDùng bảoVệGiáTrị | 4 KiB 페이지, giáTrịMã RX/DữLiệu RW·NX, giáTrịNhân·MMIO 차단, guard page, 잘못된 conTrỏ CácPhépKiểmTra | 다중 NgườiDùng giáTrịQuyền, 일반 프로세스/스레드 스케줄러 |
| thựcThiLệnh giáTrịThờiGian giáTrịGiớiHạn | GIC-400 타이머로 무한 giáTrịLầnLặp chươngTrìnhRa; tươngTác giáTrịVào 대기는 기한 làmMới, 터미널별 EL0 ChươngTrình 중단·việcThựcThiTiếpDiễn | 일반적인 선점형 다중작업. 긴 giáTrịNhân gọiThựcHiện 도중에는 종료가 지연될 trịSố 있음 |
| Tệp | Java RAM Tệp 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, giáTrịĐốiTác/절대 đườngDẫn 63바이트, mụcBộMôTả 16개 | giáTrịQuyền, 디스크/SD 영속 giáTrịCất |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP phầnCàiĐặt, 게스트 FTP·SSH·VNC | GENET phầnCứngVậtLý thẩmĐịnh, Wi-Fi, DNS, 일반 TLS giáTrịỔCắmMạng, RDP |
| GUI | giáTrịTốiĐa 네 thiếtBịCuối cửaSổ, giáTrịViệcChọn·giáTrịDiChuyển·X đóng, vănBảnHangul giáTrịPhôngChữ, Swing 부분집합; 게스트 VNC MànHình·giáTrịVào·두벌식 | phầnCứngVậtLý USB giáTrịVào, 전체 AWT/Swing·Java2D·cửaSổ 관리 정책 |
| TácVụ giáTrịLuồngChạy | giáTrịNhân TácVụ 2개와 주 TácVụ; JVM 내부 giáTrịLuồngChạy giáTrịTốiĐa 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, vănBảnHangul·일본어·아랍어·이모지, UTF-8 vănBảnTênTệp/điệnDữLiệu | GUI의 일반 다국어 조판 |

thựcThiLệnh 버튼 화면은 5×7 영문 글꼴을 쓰며, thiếtBịCuối 창은 Noto CJK/DejaVu에서 생성한 vănBảnHangul·Unicode 비트맵 글꼴을 쓴다. UART와 dữLiệuThựcTế 프레임버퍼의 vănBảnHangul 표시를 시험한다. 루프백은 동일 giáTrịNhân 내부의 điệnDữLiệu 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 giáTrịPhụTrợ UART SLIP 경로를 사용한다. `python3 CôngCụ/thựcThiLệnh.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·thựcThiLệnh 제한과 tiếngViệt 사용법은 [tựThân JVM과 tiếngViệt thưViện](MôiTrườngMôiTrườngChạyJava.md)에 정리했다. giáTrịLớp Tệp/JAR 배포는 [JavaTiếngViệt](JavaTiếngViệt) 소스에서 재현한다. 기존 Linux판 `tiếngViệt.Java`와 별도인 `tiếngViệt.tựThân` 패키지다.

**vi·여러 cửaSổ·Swing·vănBảnHangul Java/Python/C/C++·posix-kor 예제는 [vănBảnHangul phátTriển 매뉴얼](HướngDẫnPhátTriển.md)에 정리했다.**

GUI thiếtBịCuối thựcThiLệnh·단축키·vỏLệnh lệnh·제한은 [셸과 thiếtBịCuối 사용법](ThiếtBịCuốiVàVỏLệnh.md)에 정리했다.

## phầnMụcHiệnTại 컴퓨터에서 thựcThiLệnh

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

chươngTrìnhRa: **Ctrl+A phầnMụcKếTiếp X**. 게스트 C/AOT CôngCụ 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc giáTrịSốHọc giáTrịPhụTrợ 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. Chủ 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 ChuyểnNền·링크한 것은 아니다. TrìnhBiênDịch 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/đườngDẫn/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` giáTrịHỗTrợ 여부를 확인한 trạngTháiSau 실행한다.

명령은 **Enter를 눌러 thựcThiLệnh**한다. 기존 한 giáTrịKýTự 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "vănBảnHangul cácĐốiSố 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| lệnh | hànhĐộng |
|---|---|
| `help` / `info` | lệnh·dữLiệuThựcTế phầnCàiĐặt giáTrịTrạngThái |
| `ls` / `cat FILE` / `rm FILE` | RAM Tệp danhSáchMục·giáTrịNộiDung·삭제 |
| `vi FILE` | NgườiDùng giáTrịMiền vi 부분집합, vănBảnHangul giáTrịSửa·giáTrịCất·검색·되돌리기 |
| `edit FILE` | Tệp 전체를 새로 giáTrịVào; 단독 `.` 줄로 giáTrịCất, Ctrl-C로 thaoTácHủy |
| `javac FILE.java` / `java CLASS [ARGS]` | tựThân 제한형 Java biênDịchNguồn·thựcThiLệnh |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython biênDịchNguồn·thựcThiLệnh |
| `load FILE` / `hex FILE` | 16진수 바이너리 giáTrịVào/ĐầuRa; 입력은 단독 `.` 줄로 giáTrịCất |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 tựThân ABI ELF / 내장 C++ VíDụ |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 TácVụ / EL0 bảoVệGiáTrị KiểmThử |
| `gui` / `terminal` | thựcThiLệnh MànHình / vănBảnHangul GUI thiếtBịCuối; F12로 thiếtBịCuối mở·đóng |
| `samples` | 삭제한 giáTrịMặcĐịnh VíDụ khôiPhụcTrạngThái; 기존 파일은 보존 |

예를 들어 `edit LờiChào.java`를 입력한 phầnMụcKếTiếp giáTrịĐáy 소스를 입력한다.

```java
public class LờiChào { public static void main(String[] args) { int giáTrị = 7; System.out.println("vănBảnHangul=" + giáTrị); } }
```

그다음 단독 `.` 줄로 저장하고 `javac LờiChào.java`, `java LờiChào`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. thaoTácHủy·잘못된 16진수·giáTrịSứcChứa 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, thựcThiLệnh 인수는 giáTrịTốiĐa 8개·각각 UTF-8 255바이트다. 일반 lệnh 인수는 giáTrịTốiĐa 32개다. dấuTrích·백슬래시·vỏLệnh giáTrịBiến·파이프·리다이렉션 범위는 [vỏLệnh môTả](ThiếtBịCuốiVàVỏLệnh.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, địaChỉ **127.0.0.1:5902**로 연결한다. 키보드·vănBảnHangul Unicode giáTrịVào·명시적 giáTrịDán·thựcThiLệnh 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 CôngCụ/thựcThiLệnh.py --desktop --network
# 다른 cổngPhầnCứng: python3 CôngCụ/thựcThiLệnh.py --desktop --port 5903
```

종료는 실행한 Chủ 터미널에서 Ctrl+C다. 기존 `python3 CôngCụ/thựcThiLệnh.py --vnc 127.0.0.1:2`는 MànHình 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. dữLiệuThựcTế Pi4 USB 입력기는 아직 없으며, VNC nốiKết 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 dữLiệuThựcTế C++/UDP ELF thựcThiLệnh, `Hello.java` biênDịchNguồn trạngTháiSau JVM thựcThiLệnh, `hello.py` thựcThiLệnh, GUI thiếtBịCuối 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 tươngTác 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 dữLiệuBộNhớ·CPU 문맥을 보관한다. vỏLệnh·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## dữLiệuThựcTế 산출물과 Pi4 SD xâyDựngẢnh

```sh
make image   # giáTrịNhân, SD xâyDựngẢnh, KhởiĐộng ZIP, 사용자용 SDK
make sdk     # SDK만 giáTrịThửLại sinh
```

| đườngDẫn | 용도 |
|---|---|
| `build/kernel8.img` | tựThân giáTrịNhân 기계어, 적재 địaChỉ 0x80000 |
| `build/kernel.elf`, `kernel.map` | giáTrịNhân giáTrịKýHiệu·BốTríLiênKết |
| `build/user/demo.elf` | NgườiDùng giáTrịChếĐộ C++ Tệp/giáTrịVùngNhớĐộng/giáTrịĐiểmDấuPhẩyĐộng/그래픽 VíDụ |
| `build/user/network.elf` | NgườiDùng giáTrịChếĐộ C++ UDP 루프백 VíDụ |
| `build/user/java-tools.elf` | tựThân Java 부분집합 TrìnhBiênDịch/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | Chủ javac용 tiếngViệt API giáTrịLớp; 같은 클래스가 tựThân JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | tiếngViệt API Java mãNguồn |
| `build/user/vi.elf` | tựThân UTF-8 vi lệnh 부분집합 TrìnhSoạnThảo |
| `build/user/python.elf` | tựThân ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 bảoVệGiáTrị KiểmThử 전용 |
| `build/libposix-kor-arm64.a` | **giáTrịNhân 내부**에서 Java Tệp 구현을 직접 부르는 기존 nốiKết |
| `build/libposix-kor-user.a` | **EL0 NgườiDùng ChươngTrình**에서 SVC로 Tệp/루프백을 호출하는 새 nốiKết |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD xâyDựngẢnh |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 KhởiĐộng 파티션에 복사할 Tệp giáTrịNhóm |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·chạy giáTrịMã·thưViện·링커 giáTrịKịchBản·VíDụ |
| `dist/manifest.json`, `build/build.json` | SHA256과 dữLiệuThựcTế giáTrịHỗTrợ giáTrịTrạngThái |

이미지는 확인된 공식 Pi KhởiĐộng 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·thiếtBịCuối giáTrịPhôngChữ 라이선스와 giáTrịPhôngChữ giáTrịGốc 해시도 동봉한다. Tệp sinh 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 xâyDựngẢnh bảnGhiNhậtKý 도구로 `.img`를 기록하거나 FAT32 KhởiĐộng 파티션 최상위에 ZIP 내용을 푼다. xâyDựngẢnh 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 giáTrịMặcĐịnh EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**phầnCứngVậtLý Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Tệp 구성·giáTrịNhân 체크섬 검사와 물리 BoMạch KhởiĐộng 검증은 별개다. MMU giáTrịDùng 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 KhởiĐộng 조건을 전제로 한다. giáTrịBa giáTrịPhụTrợ 코어는 대기시키며 한 코어만 사용한다.

## C++와 tiếngViệt API giáTrịDùng

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/VíDụTệp.cpp -o demo.elf
python3 compile.py examples/VíDụTruyềnThông.cpp -o network.elf
```

진입점은 `extern "C" int bắtChạyChươngTrìnhNgườiDùng(int)`이다. NgườiDùng C++는 FP/SIMD를 사용할 trịSố 있다. giáTrịNhân C/Java AOT는 일반 레지스터만 사용하므로 ngoạiLệ mụcGiáTrịTiếnTrình 중 NgườiDùng FP 상태를 건드리지 않는다. NgườiDùng giáTrịĐiểmMục 시 FP 상태를 초기화하고 giáTrịNhân 복귀에 필요한 상태를 보존한다.

```cpp
#include "ABITệp.h"
extern "C" int bắtChạyChươngTrìnhNgườiDùng(int) {
    int Tệp = mởTệp("LờiChào.txt", GhiĐọc | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
    if (Tệp < 0) return 1;
    const char giáTrịNộiDung[] = "안녕하세요";
    int kếtQuả = ghiDữLiệuTệp(Tệp, giáTrịNộiDung, sizeof(giáTrịNộiDung) - 1);
    đóngTệp(Tệp);
    return kếtQuả == sizeof(giáTrịNộiDung) - 1 ? 0 : 2;
}
```

[Tệp VíDụ](NgườiDùng/VíDụTệp.cpp)와 [TruyềnThông VíDụ](NgườiDùng/VíDụTruyềnThông.cpp)toánHạngĐầuTiên dữLiệuThựcTế KhởiĐộng KiểmThử 대상이다. `ABITệp.h`의 이름은 커널용/사용자용 xâyDựngTấtCả 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Tệp mụcGiáTrịTiếnTrình 및 루프백 전달은 Java 커널에서 실행한다. `ABIMạng.h`의 giáTrịỔCắmMạng 함수는 phầnMụcHiệnTại 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 giáTrịNhân 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 phầnMụcKếTiếp 도구를 사용하면 **새 QEMU를 부팅해 업로드한 dữLiệuThựcTế 바이트를 재확인한 giáTrịLùi 게스트에서 thựcThiLệnh**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 CôngCụ/thựcThiTệp.py build/jkoros-native-sdk/demo.elf
python3 CôngCụ/thựcThiTệp.py VíDụ/Hello.java "vănBảnHangul cácĐốiSố"
python3 CôngCụ/thựcThiTệp.py VíDụ/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 giáTrịNhân 묶음에 포함되어 이 Tệp 한도를 적용받지 않는다. **C++ 컴파일러는 Chủ SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 thưViện, PT_TLS, PT_INTERP, PT_DYNAMIC, thựcThiLệnh·ghi 겸용 세그먼트는 로더가 거부한다. 구체적인 gọiThựcHiện sốHiệu·địaChỉ cắtXén·오류는 [NgườiDùng ABI](ABIGọiNgườiDùng.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `lưuTrữTệpChốt`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 giáTrịQuyền·dup/fcntl은 없다. 디렉터리와 giáTrịĐốiTác/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 giáTrịTốiĐa 512바이트, 소켓은 8개, nhậnGiáTrị 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. NgườiDùng chươngTrìnhRa 시 열린 Tệp 서술자와 소켓을 회수한다.

## thẩmĐịnh kếtQuả

`make test-jvm`은 9개 프로그램을 OpenJDK와 dữLiệuThựcTế tựThân 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `CôngCụ/ThửKhởiĐộng.py`는 Java hìnhChữNhật API의 dữLiệuThựcTế MànHình 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 dữLiệuThựcTế VNC giáTrịVào·vănBảnHangul thiếtBịCuối 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT giáTrịThaoTác kếtQuả 비교, 런타임 lỗi 중단, làKhôngHỗTrợ Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java giáTrịNhân phépTính·UTF-8·C++ 직접 gọiThựcHiện·협력식 TácVụ 및 프레임버퍼.
- 손상/잘못된 ABI/địaChỉ 초과/겹친 페이지/W+X 등 ELF từChốiGiáTrị 사례 22개.
- EL0 C++ 생성자·RAII·giáTrịĐiểmDấuPhẩyĐộng giáTrịThaoTác·Tệp·giáTrịVùngNhớĐộng 및 잘못된 시스템 gọiThựcHiện conTrỏ.
- giáTrịNhân/giáTrịMã/MMIO ghi·mụcTruyCập, NX ngănXếpToánHạng·NULL thựcThiLệnh, guard page, 특권 lệnh 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 trạngTháiSau làBìnhThường ChươngTrình 재실행.
- giáTrịLầnLặp thựcThiLệnh 시 Tệp/giáTrịỔCắmMạng 누수 방지, UDP 왕복·보낸 địaChỉ·giáTrịĐãCắtXén nhậnGiáTrị·큐 포화·빈 điệnDữLiệu·làKhôngHỗTrợ TruyềnThông lỗi.
- vỏLệnh giáTrịSửa·thaoTácHủy·16진수 업로드/다운로드·NgườiDùng ELF 실행과 잘못된 ELF từChốiGiáTrị.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 thựcThiLệnh, vănBảnHangul giáTrịLớp·giáTrịBiến·vănBảnTênTệp.
- 여러 cửaSổ·vi giáTrịCất·giáTrịSửa·cầuNốiTrảVề·NgườiDùng giáTrịTrạngThái 중단/việcThựcThiTiếpDiễn, Swing vănBảnHangul giáTrịVào·이벤트·X đóng, 연결형 루프백, C/C++ vănBảnHangul SDK VíDụ.
- MicroPython Unicode·큰 SốNguyên·giáTrịLớp·GC giáTrịLầnLặp·Tệp import·ngoạiLệ·Tệp·UDP 왕복·giáTrịThờiGian 초과 trạngTháiSau 복귀.
- GUI giáTrịViệcChọn giáTrịDiChuyển, C++/UDP/Java/MicroPython 버튼 thựcThiLệnh, 콘솔 복귀 및 dữLiệuThựcTế 프레임버퍼 픽셀/giáTrịPhôngChữ.
- 디렉터리·giáTrịBiến·điềuKiện·Tệp lệnh·giáTrịKịchBản·순차 파이프·리다이렉션·giáTrịSứcChứa 초과 khôiPhụcTrạngThái, Python stdin/EOF와 Java/Python stdout.
- lệnh bảnGhiNhậtKý·긴 vănBảnHangul giáTrịVào giáTrịSửa·giáTrịĐãHoànTất·thiếtBịCuối 스크롤, 그래픽 ChươngTrình chươngTrìnhRa trạngTháiSau cửaSổ 복원, dữLiệuThựcTế VNC Unicode giáTrịPhím·giáTrịDán·마우스.

[giáTrịNhân KiểmThử bảnGhiNhậtKý](build/verification/implementation-test.log), [vỏLệnh KiểmThử](build/verification/shell/report.json), [VNC KiểmThử](build/verification/desktop/report.json), [máy 판독 kếtQuả](build/verification/report.json), [giáTrịNốiTiếp giáTrịNhậtKý](build/verification/serial.log), [GUI MànHình](build/verification/gui-python.png)을 확인할 trịSố 있다. VNC RFB 3.8 nốiKết 및 640×480 MànHình 정보도 검사한다. [SDK 재컴파일 kếtQuả](build/verification/sdk.json)는 두 예제의 điểmMục·적재 세그먼트·ABI note가 KhởiĐộng 시험한 ELF와 일치함을 확인한다. giáTrịKýHiệu 등 비적재 메타데이터를 포함한 Tệp 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 cắtXén

tựThân `javac`는 버전 49 `.class`를 생성하며 JVM은 giáTrịHỗTrợ 명령으로 구성된 버전 45–52 클래스를 실행한다. giáTrịTĩnh Hàm·재귀·int/boolean/char/String·điềuKiện/giáTrịLầnLặp·ChuỗiKýTự 결합과 일부 Tệp 스트림을 지원한다. UTF-8 문자열과 KýTự 리터럴, ASCII 및 현대 vănBảnHangul 음절/PhốiHợp giáTrịJamo 식별자를 처리한다. Unicode giáTrịĐịnhDanh 전체 Bảng·Unicode câyNguồn 이스케이프는 구현하지 않았다. 게스트 câyNguồn 컴파일러는 일반 giáTrịĐốiTượng·ngoạiLệ·Thread 구문을 아직 컴파일하지 못한다. Chủ `javac --release 8`로 만든 giáTrịHỗTrợ 부분집합 클래스는 tựThân JVM 0.4의 giáTrịĐốiTượng·ngoạiLệ·Thread·UDP와 tiếngViệt API를 사용할 trịSố 있다. Swing은 문서화한 tựThân API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [tựThân JVM môTả](MôiTrườngMôiTrườngChạyJava.md)이 기준이다. 상세 NgônNgữ 범위는 [공유 Java CôngCụ môTả](../../TàiLiệu/MôiTrườngPhátTriểnJava.md)을 참고하되, 그 문서의 x86 vỏLệnh/giáTrịCất/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 câyNguồn**를 tựThân AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 Hàm·giáTrịLớp·ngoạiLệ·리스트/TừĐiển·Unicode·GC·가변 giáTrịĐộChínhXác 정수를 제공한다. phầnMụcHiệnTại 구성은 SốNguyên 빌드로 `float`, `complex`, `math`toánHạngĐầuTiên 없으며 CPython 전체 표준 thưViện, pip, subprocess, threading, 일반 socket과 giáTrịMặcĐịnh `open()` Tệp 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 giáTrịĐốiTượng·모듈은 chươngTrìnhRa 시 회수되고 RAM 파일만 phầnMụcKếTiếp 실행에 남는다.

`import jkoros`로 phầnMụcKếTiếp 시스템 연결을 쓴다. xâyDựngTấtCả SVC를 통해 tựThân Java 커널에 접근한다.

| Hàm | hànhĐộng |
|---|---|
| `stdin(limit)` | phầnMụcHiệnTại 표준 입력에서 giáTrịTốiĐa limit바이트(0…16384)를 bytes로 đọcKếtQuả; EOF는 빈 bytes, UART DữLiệu 없음은 OSError(11) |
| `read(name)` | giáTrịĐốiTác/절대 RAM 경로의 Tệp 전체를 bytes로 đọcKếtQuả |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 giáTrịCất, 쓴 giáTrịByte trịSố kếtQuảTrảVề |
| `remove(name)` | RAM Tệp 삭제 |
| `rect(x, y, w, h, color)` | 선택한 dữLiệuThựcTế MànHình cỡ 안의 hìnhChữNhật HìnhVẽ; 기존 보드의 RGB32 giáTrị |
| `ticks_ms()` | KhởiĐộng trạngTháiSau miliGiây, 32비트 giáTrịChuKỳ |
| `udp_open(port)` | 127.0.0.1의 UDP giáTrịỔCắmMạng mở/GóiTệpThựcThi; 0은 자동 cổngPhầnCứng |
| `udp_send(fd, port, data)` | 루프백 giáTrịĐích 포트에 str/bytes 버퍼 giáTrịChuyểnGiao |
| `udp_recv(fd)` | `(bytes, 보낸포트)` kếtQuảTrảVề; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | giáTrịỔCắmMạng đóng |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

ChuyểnNền giáTrịMã: [python/](cầuNốiPython/), [NgườiDùng Java nốiKết](NgườiDùng/cầuNốiJava.c). 공식 [MicroPython ChuyểnNền HướngDẫn](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. câyNguồn URL·tệpMãBăm·라이선스는 [vendor HướngDẫn](vendor/README.md)에 기록했다.

## 남은 TácVụ

| phầnMụcKếTiếp giáTrịGiaiĐoạn | làĐầyĐủ gốcCâyDựÁn |
|---|---|
| 영속 giáTrịCất·thựcThiLệnh Tệp giáTrịVào | SD/MMC 및 디스크 Tệp 시스템, 시스템/NgườiDùng 볼륨; phầnMụcHiệnTại ELF Tệp 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 địaChỉ miềnĐịaChỉ, 선점 스케줄러, TLS, đồngBộHóa/chờGiáTrị, 신호, mmap/mprotect |
| libc와 C++ 런타임 | tựThân ABI용 libc, malloc/free, 표준 đầuRaĐầuVào·ĐồngHồ·môiTrường·locale, libstdc++/ngoạiLệ mụcGiáTrịTiếnTrình thẩmĐịnh |
| CPython | 해당 libc와 OS API 대상으로 ChuyểnNền·교차 빌드하고 Tệp/Unicode/스레드/giáTrịỔCắmMạng KiểmThử |
| OpenJDK/JRE | HotSpot OS giáTrịTầng, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 thưViện ChuyểnNền; javac/java dữLiệuThựcTế thựcThiLệnh |
| giáTrịBênNgoài 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 dữLiệuThựcTế BoMạch 송수신 thẩmĐịnh, DNS·Wi-Fi |
| GUI giáTrịPhầnMởRộng | USB HID, 게스트 입력기·KýTự 조판, Swing cửaSổ cỡ 조절·클리핑 giáTrịPhầnMởRộng, 전체 AWT/Swing ChuyểnNền |

이 표는 남은 작업이며 phầnCàiĐặt làĐầyĐủ 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 giáTrịBênNgoài 네트워크 드라이버는 phầnCứngVậtLý 검증도 필요하다. [QEMU ThiếtBị 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

giáTrịPhầnCứng 및 ABI 참고: [BCM2711 ngoạiVi](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC địaChỉ](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox giáTrịQuyƯớc](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP giáTrịĐiềuKhiển 레지스터 giáTrịĐịnhNghĩa](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## tiếngViệt C kiểuDữLiệu·Python lỗi·GóiGộp càiĐặtGiáTrị

C 네트워크 API는 `struct ĐịaChỉỔCắmMạngLiênMạng`, enum 상수와 dữLiệuThựcTế tiếngViệt 함수로
구현한다. giáTrịVĩLệnh 별칭을 사용하지 않으며 phầnMụcTrướcĐó pk_* ABI도 유지한다.
Python 예제는 `LỗiHệThống`, `lỗi.sốHiệu`, `lỗi.môTả`을 사용한다.

`python3 CôngCụ/thựcThiLệnh.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 trịSố 있다. 현재는 Chủ 중계를
이용하는 제한형 MicroPython câyNguồn 설치기이며 CPython pip·자동 cácPhụThuộc 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 giáTrịGiớiHạn](GóiGộpPython.md).

## MànHình cỡ giáTrịViệcChọn

`python3 CôngCụ/thựcThiLệnh.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. thiếtBịCuối giáTrịDiChuyển, Swing giữa BốTríLiênKết, Java·C·Python 그리기도 dữLiệuThựcTế 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [cácThiếtLập·tiếngViệt API·thẩmĐịnh HướngDẫn](độPhânGiảiMànHình.md).

## tiếngViệt 직접 API와 MànHình làmMới

`example/java`는 `TácVụChạyĐược`, `BộNhậnHànhĐộng`, `ThôngBáoHànhĐộng`, `nút`, `HàngĐợiSựKiện`,
`bộLàmViệc`, `chạy()`을 사용할 trịSố 있다. tiếngViệt GUI/가닥을 tựThân JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. ChuỗiKýTự 등 javac의 표준
계약과 전체 câyNguồn 검토 범위는 [cáchĐặtTên HướngDẫn](cáchĐặtTên/HướngDẫn.md), 사용법과 호환성 변경은
[tiếngViệt Java API](JavaTiếngViệt/HướngDẫn.md)를 본다.

thiếtBịCuối giáTrịDiChuyển·cỡ 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[MànHình làmMới môTả](MôiTrườngMôiTrườngChạyJava.md#thiếtBịCuối-giáTrịPhầnCon-làmMới),
[giáTrịPhầnCon làmMới CácPhépKiểmTra](build/verification/redraw/report.json)를 참고한다.
