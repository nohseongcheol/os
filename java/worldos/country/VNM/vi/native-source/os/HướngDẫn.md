# Java 네이티브 HệĐiềuHành

이 문서는 기존 **x86 giáTrịNhân**을 설명한다. Raspberry Pi 4의 tựThân ARM64 trạngTháiBanĐầu 이식은 [별도 HướngDẫn](../platforms/rpi4-native/README.md)를 참고한다. giáTrịĐáy x86 NgườiDùng ELF·네트워크·IDE giáTrịCất 기능이 ARM64에 xâyDựngTấtCả 이식된 상태는 아니다.

Java 원문을 tựThân AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 tựThân 제한형 Java TrìnhBiênDịch·JVM ELF를 NgườiDùng 모드에 적재할 trịSố 있다. Linux, engos, koros4와 giáTrịBênNgoài OpenJDK는 게스트에 적재하지 않는다. KhởiĐộng 진입과 cổngPhầnCứng/물리 VùngNhớ 접근은 어셈블리이며, KýTự VàoRaThiếtBịCuối·giáTrịVào mụcGiáTrịTiếnTrình·lệnh phânTíchCúPhápGiáTrị·TácVụ giáTrịMụcĐoạn 관리는 `mãNguồn/*.java`에 있다.

## 게스트 Java phátTriển

`javac Hello.java`, `java Hello`로 부팅된 HệĐiềuHành 안에서 biênDịchNguồn·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 giáTrịTốiĐa 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 trịSố 있다. 이 기능은 tựThân 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·giáTrịHỗTrợ 문법·Tệp 적재·교차 시험은 [Java phátTriển môiTrường](../TàiLiệu/MôiTrườngPhátTriểnJava.md)에 있다. `make test-java`로 검증한다.

## 빌드와 thựcThiLệnh

`compiler/`toánHạngĐầuTiên 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS giáTrịMôĐun, `xorriso`toánHạngĐầuTiên 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. phầnMụcHiệnTại 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 giáTrịCất 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 giáTrịMặcĐịnh 64MiB이며 giáTrịTốiThiểu 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (NgườiDùng ELF giáTrịNhóm TệpĐầuMục)
make run             # ELF 직접 KhởiĐộng, giáTrịNốiTiếp VàoRaThiếtBịCuối
make run-gui         # GRUB ISO KhởiĐộng, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM thựcThiLệnh
make vbox-status     # 전용 VirtualBox VM giáTrịTrạngThái xácMinh
make test            # ELF와 ISO 두 경로의 dữLiệuThựcTế KhởiĐộng/giáTrịVào KiểmThử
make apps            # NgườiDùng 프로그램만 xâyDựngHệThống
make test-network    # NgườiDùng thựcThiLệnh/UDP/bảoVệGiáTrị KiểmThử
```

`make run`은 QEMU의 giáTrịNốiTiếp 표준 입출력을 쓴다. `Ctrl+A`를 누른 giáTrịLùi `X`로 QEMU를 종료할 trịSố 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU cửaSổ/프로세스는 별도로 닫는다. 폴링 방식이라 chờGiáTrị 중에도 Chủ CPU를 사용할 trịSố 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 dữLiệuBộNhớ 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 giáTrịCầnĐến 없다. dữLiệuThựcTế VirtualBox 5.2.42에서 KhởiĐộng, Java tựThân KiểmThử, vỏLệnh giáTrịVào, `run hello vbox`의 ring 3 실행과 làBìnhThường 종료를 확인했다. phầnMụcHiệnTại TruyềnThông 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 trịSố 없어 네트워크 장치를 비활성화한다. giáTrịCất giáTrịTrạngThái 재개와 새 xâyDựngHệThống 반영 방법은 [VirtualBox thựcThiLệnh HướngDẫn](../TàiLiệu/ChạyVirtualBox.md)에 있다.

## 셸에서 NgườiDùng ChươngTrình thựcThiLệnh 및 네트워크 gọiThựcHiện

독립 ELF32 thựcThiLệnh 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 VàoRaThiếtBịCuối ĐầuRa, cácĐốiSố giáTrịTruyVấn, UDP mở·gửi·nhận·닫기를 제공한다. NgườiDùng 코드를 giáTrịNhân 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

phầnMụcCuối 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/CôngCụ/PhụcHồiDữLiệu.py --port 9000`을 먼저 실행한다. 상세 API, ChươngTrình thêmCuốiMục, địaChỉ 공간과 제한은 [NgườiDùng thựcThiLệnh·네트워크 HướngDẫn](NgườiDùng/HướngDẫn.md)에 있다.

KhởiĐộng xácMinh giáTrịCụmTừ:

```text
JKOROS NATIVE JAVA
Java 기계어 giáTrịNhân chạy
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF KhởiĐộng, x86 bảoVệGiáTrị giáTrịChếĐộ GDT, BSS khởiTạo, 64KiB ngănXếpToánHạng.
- Java Hàm dữLiệuThựcTế 실행과 KhởiĐộng thôngTinHệThống giáTrịDấuMốc xácMinh.
- COM1 giáTrịNốiTiếp đầuRaĐầuVào, VGA KýTự MànHình·giáTrịConTrỏVănBản·스크롤·xóaMục.
- PS/2 giáTrịMặcĐịnh 자판, 좌우 Shift, Enter, Backspace. giáTrịPhầnMởRộng giáTrịPhím/마우스 자료는 lệnh 입력으로 쓰지 않는다.
- độDài 128의 lệnh giáTrịVào 버퍼, giáTrịTràn 방지, CR/LF mụcGiáTrịTiếnTrình.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB TácVụ giáTrịMụcĐoạn 8개의 cấpPhátLưuTrữ·kếtQuảTrảVề·재사용과 중복 kếtQuảTrảVề 방지.
- Java giáTrịMảng 256KiB 영역의 cỡ·giáTrịChỉSốDưới 검사와 런타임 lỗi 중단.
- đọc 전용 JKAP thựcThiLệnh giáTrịNhóm, ELF32 giáTrịMụcĐoạn/điểmMục thẩmĐịnh, NgườiDùng giáTrịChếĐộ·cácĐốiSố·chươngTrìnhRa giáTrịMã.
- giáTrịNhân/NgườiDùng 페이지 giáTrịQuyền 분리, TSS, IDT, PIT 100Hz, NgườiDùng CPU ngoạiLệ mụcGiáTrịTiếnTrình 및 thựcThiLệnh giáTrịThờiGian 상한.
- PCI RTL8139 폴링 드라이버, ARP, giáTrịTĩnh IPv4, UDP tổngKiểm·송수신·chờGiáTrị giáTrịGiớiHạn.

`mem`의 Upper memory는 Multiboot의 1MiB bênThượng cácTrườngHợpChuyểnDày dữLiệuBộNhớ cỡ(KiB)이며, 전체 dữLiệuBộNhớ 지도 분석이나 자유 물리 dữLiệuBộNhớ 수치가 아니다. `alloc`은 이미 확보한 SốNguyên giáTrịMảng 안의 TácVụ giáTrịMụcĐoạn 번호를 반환한다. 일반 물리 giáTrịTrang cấpPhátLưuTrữ, địaChỉ miềnĐịaChỉ 또는 NgườiDùng giáTrịTiếnTrình dữLiệuBộNhớ 관리가 아니다.

## 명시적인 giớiHạnRanhGiới

이 커널은 **NgườiDùng 프로그램을 한 번에 giáTrịMột 실행하는 trạngTháiBanĐầu giáTrịNhân**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. NgườiDùng CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 giáTrịNhân 예외는 중단한다. thựcThiLệnh 시간은 약 3초로 제한한다. 완전한 선점 다중 giáTrịTiếnTrình 스케줄러, FAT/ext 등 일반 디스크 HệThốngTệp, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 giáTrịĐốiTượng 모델/GC는 아직 없다. 전용 IDE Tệp 보존과 POSIX Tệp/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 thựcThiLệnh 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 thựcThiLệnh 파일은 xâyDựngHệThống 시 đọc 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../NguồnNềnTảng/`의 JVM 관리 giáTrịNhân 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. giáTrịNốiTiếp 출력은 이 프로젝트의 vănBảnHangul(BMP KýTự)을 UTF-8로 표시한다. VGA는 giáTrịMặcĐịnh ASCII 글꼴만 사용하므로 vănBảnHangul 자리에 `?`toánHạngĐầuTiên 나온다. lệnh 입력도 phầnMụcHiệnTại ASCII만 지원하며 vănBảnHangul giáTrịPhôngChữ·입력기 및 giáTrịPhụTrợ 평면 KýTự 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 KiểmThử

`KiểmThử/ThửKhởiĐộng.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 KhởiĐộng 및 GRUB ISO KhởiĐộng.
- Java tựThân 시험과 UTF-8 giáTrịNốiTiếp giáTrịCụmTừ.
- lệnh hiệnTrợGiúp·thôngTinHệThống·dữLiệuBộNhớ·ĐầuRa·lỗi giáTrịVào·MànHình xóaMục.
- TácVụ giáTrịMụcĐoạn 8개 cấpPhátLưuTrữ, 부족 mụcGiáTrịTiếnTrình, kếtQuảTrảVề/중복 kếtQuảTrảVề/재할당.
- giáTrịNốiTiếp xuốngDòng·백스페이스·긴 giáTrịVào mụcGiáTrịTiếnTrình.
- QEMU PS/2 giáTrịPhím 입력으로 `info` thựcThiLệnh, `halt` việcThựcThiDừngHẳn.

giáTrịThànhCông 로그는 `build/ThửKhởiĐộng.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 KiểmThử 도구에 해당 권한이 필요하다. KiểmThử 도중 새로 만든 QEMU만 종료하며 기존 VM과 dữLiệuThựcTế 디스크는 건드리지 않는다.

`KiểmThử/thửMạngNgườiDùng.py`는 ELF/ISO 각각에서 NgườiDùng ELF, dữLiệuThựcTế ring 3, cácĐốiSố, Chủ 루프백 UDP 왕복, 1,023/1,024바이트 24회 cácTrườngHợpChuyểnDày 왕복, giáTrịThờiGian 초과, NIC phươngThứcThiếu, dữLiệuBộNhớ/cổngPhầnCứng mụcTruyCập 차단, CPU ngoạiLệ, 무한 giáTrịLầnLặp, 잘못된 ELF를 시험한다. `build/thửMạngNgườiDùng.json`에 게스트 기록과 호스트가 받은 데이터의 độDài·해시를 저장한다. `KiểmThử/ThửGóiTin.py`는 dữLiệuThựcTế Java giáTrịQuyƯớc 처리기에 손상된 패킷을 넣어 2,201개 giáTrịRanhGiới/tổngKiểm 조건을 검사한다. Chủ 루프백 외 giáTrịBênNgoài 서버에는 KiểmThử 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot đặcTả](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 bộMôTảTệp·C ABI·IDE giáTrịCất·Java Tệp 흐름의 범위와 tiếngViệt cáchĐặtTên 대응은 [posix-kor HướngDẫn](../posix-kor/HướngDẫn.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
