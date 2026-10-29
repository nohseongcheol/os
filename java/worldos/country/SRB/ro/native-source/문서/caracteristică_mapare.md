# engos 기능 대응표

이 표는 기존 `moștenit_sursă/`의 obiect_VALUE 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [real_date 부팅 기능과 한계](../os/안내.md)를 따로 기록한다.

## Java 관리 strat_VALUE 구현 완료

| engos regiune_VALUE | JSrbOS 구현 |
|---|---|
| memorymanager, phymem | `기억공간관리자` alinia_VALUE aloca_Stocare·lansa_Stocare·병합 |
| paging, virtmem | `쪽관리자` adresa adresa_regiune·pagina_VALUE Conectează·COW·개인 Scriere |
| gdt, tss | `전역서술자표`, `sarcină_Stare_segment` |
| interrupt | `개입중단관리자` registru_intrare·activa·distribui_VALUE |
| process, scheduler, thread | `Proces_VALUE`, `Planificator` PID·fork·wait·Stare_VALUE SWITCH_mod |
| systemcall/POSIX 1단계 | Citire·Scriere·Deschide·Închide·seek·dup·fcntl·acces_intrare·작업목록·utilizator/무리 ID·sincroniz·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 secțiune_VALUE Citire·Scriere |
| MSDOS partition | `partiție_principală_tabel` MBR 검증과 네 intrare_VALUE analiza_VALUE |
| FAT 공개 Fișier strat_VALUE | `sistem_de_fișiere`, `파일서술자표` Citire 전용 파일과 과정별 FD |
| ELF | ELF32 검사, secțiune_VALUE clip 검사, 적재, NOBITS zero_operand 초기화, Pornește adresa·parametru_argument·환경 반영 |
| keyboard, mouse | `입력관리자`의 손실 계수 포함 Eveniment 대기열 |
| timer | `Ceas` 틱과 oră_VALUE CONVERT_VALUE |
| PCI | `주변장치연결관리자` 검색 결과와 mobil_VALUE selecție_VALUE |
| VGA/text mode | `caracter_afișa` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `rețea_Instrumente`, `nivel_rețea` cadru_INDEX 검사·sumă_de_verificare·caz_VALUE/포트 distribui_VALUE |

## 기존 obiect_VALUE 기반 관리 nucleu_VALUE 전체를 부팅하기 위해 남은 Conectează

Următorul_element 항목은 Java 문법만으로 실행할 수 없는 CPU/mobil_VALUE 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot intrare_p_VALUE, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 context_VALUE Store_VALUE
- real_date PIC/PIT/PS2/ATA/PCI 포트 및 AMD PCnet DMA Loop_VALUE
- Java obiect_VALUE·ARRAY_VALUE Link_Aspect, excepție, 정적 초기화, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT fază_VALUE
- FAT 디스크 구역을 real_date ATA 장치와 연결하는 I_O 접착 strat_VALUE

위 관리 계층은 engos 기능의 Java 관리 구현과 gazdă 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot intrare_p_VALUE, 정적 초기화·întreg ARRAY_VALUE, VGA/직렬/PS2, 명령해석기, utilizator ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 gazdă 루프백 패킷 왕복을 검증했다. 위 표의 obiect_VALUE 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
