# JCanOS KiếnTrúc

아래는 giáTrịĐốiTượng nềnTảng 관리 giáTrịNhân 전체의 đốiTượngĐốiĐích 구조다. phầnMụcHiệnTại dữLiệuThựcTế KhởiĐộng 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 HệĐiềuHành HướngDẫn](../os/HướngDẫn.md)에 phầnCàiĐặt 범위를 명시한다. 아래의 GC·giáTrịNgữCảnh chếĐộChuyển·HệThốngTệp 등이 새 ISO에 xâyDựngTấtCả 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 giáTrịTốiThiểu 부트·트랩 giáTrịTầng
  ↓
Java AOT 실행기와 giáTrịĐốiTượng·giáTrịMảng·GC 런타임
  ↓
giáTrịPhầnCứng giáTrịRanhGiới
  ↓
Java 관리 giáTrịNhân
  ├─ VùngNhớ/quảnTrịTrang/COW
  ├─ giáTrịTiếnTrình/배정/wait
  ├─ HệThốngTệp/ELF/POSIX
  └─ giáTrịVào/thiếtBịLưuTrữ/NgănXếpMạng
```

OpenJDK 자체는 이미 운영체제가 제공하는 Tệp, 스레드, 가상 기억공간을 전제로 한다. 따라서 giáTrịNhân 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java mãByte AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, giáTrịNgữCảnh 저장처럼 Java로 표현할 trịSố 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
