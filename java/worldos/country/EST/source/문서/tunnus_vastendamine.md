# engos 기능 대응표

이 표는 기존 `pärand_lähe/`의 objekt_VALUE 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [tegelik_andmed 부팅 기능과 한계](../os/안내.md)를 따로 기록한다.

## Java 관리 kiht_VALUE 구현 완료

| engos regioon_VALUE | JEstOS 구현 |
|---|---|
| memorymanager, phymem | `기억공간관리자` joondama_VALUE lisama_salvesti·vabastama_salvesti·병합 |
| paging, virtmem | `쪽관리자` ADDRESS ADDRESS_regioon·leht_VALUE Ühendu·COW·개인 Kirjutamine |
| gdt, tss | `전역서술자표`, `tööüksus_Olek_segment` |
| interrupt | `개입중단관리자` register_kirje·lubama·laiali_jagama_VALUE |
| process, scheduler, thread | `Joonis_VALUE`, `plaanija` PID·fork·wait·Olek_VALUE SWITCH_MODE |
| systemcall/POSIX 1단계 | Lugemine·Kirjutamine·Ava·Suletud·seek·dup·fcntl·pöördus_kirje·작업목록·kasutaja/무리 ID·sünkroonima·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 jaotis_VALUE Lugemine·Kirjutamine |
| MSDOS partition | `primaarsektsioon_tabel` MBR 검증과 네 kirje_VALUE sõeluma_VALUE |
| FAT 공개 Fail kiht_VALUE | `failisüsteem`, `파일서술자표` Lugemine 전용 파일과 과정별 FD |
| ELF | ELF32 검사, jaotis_VALUE klipp 검사, 적재, NOBITS null_operand 초기화, Käivita_2 ADDRESS·parameeter_argument·환경 반영 |
| keyboard, mouse | `입력관리자`의 손실 계수 포함 Sündmus 대기열 |
| timer | `Kell` 틱과 Aeg_VALUE CONVERT_VALUE |
| PCI | `주변장치연결관리자` 검색 결과와 seade_VALUE valim_VALUE |
| VGA/text mode | `märk_ekraan` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `võrk_Tööriistad`, `võrgukiht` raam_INDEX 검사·kontrollsumma·lepingu_väärtus/포트 laiali_jagama_VALUE |

## 기존 objekt_VALUE 기반 관리 tuum_VALUE 전체를 부팅하기 위해 남은 Ühendu

Edasi_kaup 항목은 Java 문법만으로 실행할 number 없는 CPU/seade_VALUE 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot kirje_p_VALUE, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 kontekst_VALUE salv_VALUE
- tegelik_andmed PIC/PIT/PS2/ATA/PCI 포트 및 AMD PCnet DMA Loop_VALUE
- Java objekt_VALUE·ARRAY_VALUE Link_küljend, erand, 정적 초기화, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT etapp_VALUE
- FAT 디스크 구역을 tegelik_andmed ATA 장치와 연결하는 I_O 접착 kiht_VALUE

위 관리 계층은 engos 기능의 Java 관리 구현과 host 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot kirje_p_VALUE, 정적 초기화·täisarv ARRAY_VALUE, VGA/직렬/PS2, 명령해석기, kasutaja ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 host 루프백 패킷 왕복을 검증했다. 위 표의 objekt_VALUE 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
