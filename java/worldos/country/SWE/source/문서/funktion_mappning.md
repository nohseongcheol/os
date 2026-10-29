# engos 기능 대응표

이 표는 기존 `äldre_källa/`의 objekt_värde 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [verklig_data maskinstart 기능과 한계](../os/VIKTIGT_eb81d7d9.md)를 따로 기록한다.

## Java 관리 nivå_värde implementation 완료

| engos område_värde_0e9a97ab | JSweOS implementation |
|---|---|
| memorymanager, phymem | `Minne_Ansvarig` justera_värde allokera_minne·släppa_minne·병합 |
| paging, virtmem | `Sidhanteraren` Adress ADRESS_område·page_värde Anslut·COW·개인 Skriv |
| gdt, tss | `GDT`, `uppgift_status_segment` |
| interrupt | `IRQ_Ansvarig` register_post·aktivera·distribuera_värde |
| process, scheduler, thread | `Process_värde`, `Scheduler` PID·fork·wait·status_värde byta_läge |
| systemcall/POSIX 1단계 | Läs·Skriv·Öppna·Stäng·seek·dup·fcntl·ansluta_post·작업목록·användarutrymme/무리 ID·synka·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 avsnitt_värde Läs·Skriv |
| MSDOS partition | `primär_partition_tabell` MBR 검증과 네 post_värde parsa_värde |
| FAT 공개 filnamn nivå_värde | `filsystem`, `파일서술자표` Läs 전용 파일과 과정별 FD |
| ELF | ELF32 검사, avsnitt_värde klipp 검사, 적재, NOBITS noll_operand starta, Kör Adress·parameter_argument·miljö 반영 |
| keyboard, mouse | `indata_Ansvarig`의 손실 계수 deklarationer Händelse 대기열 |
| timer | `Klocka` 틱과 tid_värde KONVERTERA_värde |
| PCI | `tillbehör_buss_Ansvarig` 검색 결과와 enhet_värde markering_värde |
| VGA/text mode | `tecken_visa` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `nätverk_Verktyg`, `nätverksnivå` ram_INDEX 검사·kontrollsumma·kontraktsvärde/maskinvara_port distribuera_värde |

## 기존 objekt_värde 기반 관리 kärna_värde 전체를 부팅하기 위해 남은 Anslut

Nästa_objekt 항목은 Java 문법만으로 실행할 nummer 없는 CPU/enhet_värde 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot startpunkt_värde, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 sammanhang_värde Store_värde
- verklig_data PIC/PIT/PS2/ATA/PCI maskinvara_port 및 AMD PCnet DMA Loop_värde
- Java objekt_värde·MATRIS_värde länkningslayout, fel_31f743d2, statisk_värde starta, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT scen_värde
- FAT 디스크 구역을 verklig_data ATA 장치와 연결하는 indata_utleverans 접착 nivå_värde

위 관리 계층은 engos 기능의 Java 관리 구현과 värd 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot startpunkt_värde, statisk_värde starta·heltal MATRIS_värde, VGA/직렬/PS2, 명령해석기, användarutrymme ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 värd 루프백 패킷 왕복을 검증했다. 위 표의 objekt_värde 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
