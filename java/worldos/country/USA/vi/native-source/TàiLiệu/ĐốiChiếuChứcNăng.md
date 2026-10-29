# engos 기능 대응표

이 표는 기존 `NguồnNềnTảng/`의 giáTrịĐốiTượng nềnTảng JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [dữLiệuThựcTế KhởiĐộng 기능과 giớiHạnRanhGiới](../os/HướngDẫn.md)를 따로 기록한다.

## Java 관리 giáTrịTầng phầnCàiĐặt làĐầyĐủ

| engos giáTrịMiền | JUsaOS phầnCàiĐặt |
|---|---|
| memorymanager, phymem | `BộQuảnLýBộNhớ` giáTrịCănChỉnh cấpPhátLưuTrữ·giảiPhóngLưuTrữ·병합 |
| paging, virtmem | `BộQuảnLýTrang` địaChỉ miềnĐịaChỉ·giáTrịTrang nốiKết·COW·개인 ghi |
| gdt, tss | `BảngTraBộMôTảToànCục`, `ĐoạnVùngTrạngTháiTácVụ` |
| interrupt | `BộQuảnLýNgắtXửLý` thanhGhiMục·bật·phânPhốiGiáTrị |
| process, scheduler, thread | `giáTrịTiếnTrình`, `BộLậpLịch` PID·fork·wait·giáTrịTrạngThái chếĐộChuyển |
| systemcall/POSIX 1단계 | đọc·ghi·mở·đóng·seek·dup·fcntl·mụcTruyCập·작업목록·NgườiDùng/무리 ID·đồngBộHóa·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `PhầnGắnCôngNghệNângCao` 512바이트 giáTrịMụcĐoạn đọc·ghi |
| MSDOS partition | `bảngTraPhânVùngChínhThức` MBR 검증과 네 giáTrịMục phânTíchCúPhápGiáTrị |
| FAT 공개 Tệp giáTrịTầng | `HệThốngTệp`, `bảngTraBộMôTảTệp` đọc 전용 파일과 과정별 FD |
| ELF | ELF32 CácPhépKiểmTra, giáTrịMụcĐoạn cắtXén CácPhépKiểmTra, 적재, NOBITS toánHạngKhôngSố khởiTạo, chạy địaChỉ·đốiSốThamSố·môiTrường 반영 |
| keyboard, mouse | `BộQuảnLýĐầuVào`의 손실 계수 TệpĐầuMục sựKiện 대기열 |
| timer | `ĐồngHồ` 틱과 giáTrịThờiGian chuyểnĐổiGiáTrị |
| PCI | `BộQuảnLýĐườngTruyềnChungNgoạiVi` 검색 결과와 ThiếtBị giáTrịViệcChọn |
| VGA/text mode | `hiểnThịKýTự` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `CácCôngCụMạng`, `TầngMạng` chỉSốKhung CácPhépKiểmTra·tổngKiểm·giáTrịQuyƯớc/cổngPhầnCứng phânPhốiGiáTrị |

## 기존 giáTrịĐốiTượng nềnTảng 관리 giáTrịNhân 전체를 부팅하기 위해 남은 nốiKết

phầnMụcKếTiếp 항목은 Java 문법만으로 실행할 trịSố 없는 CPU/ThiếtBị 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot giáTrịĐiểmMục, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 giáTrịNgữCảnh giáTrịCất
- dữLiệuThựcTế PIC/PIT/PS2/ATA/PCI cổngPhầnCứng 및 AMD PCnet DMA giáTrịVòngLặp
- Java giáTrịĐốiTượng·giáTrịMảng BốTríLiênKết, ngoạiLệ, giáTrịTĩnh khởiTạo, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT giáTrịGiaiĐoạn
- FAT 디스크 구역을 dữLiệuThựcTế ATA 장치와 연결하는 đầuRaĐầuVào 접착 giáTrịTầng

giáTrịĐỉnh 관리 계층은 engos 기능의 Java 관리 구현과 Chủ 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot giáTrịĐiểmMục, giáTrịTĩnh khởiTạo·SốNguyên giáTrịMảng, VGA/giáTrịNốiTiếp/PS2, TrìnhThôngDịchLệnh, NgườiDùng ELF/ring 3/시스템 gọiThựcHiện, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 Chủ 루프백 패킷 왕복을 검증했다. giáTrịĐỉnh 표의 giáTrịĐốiTượng nềnTảng 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
