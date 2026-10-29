# engos 기능 대응표

이 표는 기존 `eldre_kilde/`의 objekt_VERDI 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [faktisk_data 부팅 기능과 한계](../os/Viktig_fil_eb81d7d9.md)를 따로 기록한다.

## Java 관리 lag_VERDI 구현 완료

| engos område_VERDI_0e9a97ab | JSjmOS 구현 |
|---|---|
| memorymanager, phymem | `Minne_overordnet` justere_VERDI tildele_lager·frigi_lager·병합 |
| paging, virtmem | `Sidebehandling` e_post e_post_område·page_VERDI Koble_til·COW·개인 Skriv |
| gdt, tss | `전역서술자표`, `oppgave_status_segment` |
| interrupt | `IRQ_overordnet` register_oppføring·aktivere·distribuere_VERDI |
| process, scheduler, thread | `Prosess_VERDI`, `Scheduler` PID·fork·wait·status_VERDI bytt_MODUS |
| systemcall/POSIX 1단계 | Les·Skriv·Åpne·Lukk·seek·dup·fcntl·tilgang_oppføring·작업목록·bruker/무리 ID·synkronisere·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 inndeling_VERDI Les·Skriv |
| MSDOS partition | `primærpartisjon_tabell` MBR 검증과 네 oppføring_VERDI dele_opp_VERDI |
| FAT 공개 Fil lag_VERDI | `filsystem`, `파일서술자표` Les 전용 파일과 과정별 FD |
| ELF | ELF32 검사, inndeling_VERDI klippe 검사, 적재, NOBITS null_operand starte, Kjør_2 e_post·parameter_argument·miljø 반영 |
| keyboard, mouse | `inndata_overordnet`의 손실 계수 포함 Hendelse 대기열 |
| timer | `Klokke` 틱과 TID_VERDI KONVERTER_VERDI |
| PCI | `tilbehør_buss_overordnet` 검색 결과와 enhet_VERDI merket_område_VERDI |
| VGA/text mode | `tegn_vise` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `nettverk_Verktøy`, `nettverkslag` bilde_INDEKS 검사·kontrollsum·kontraktverdi/maskinvare_port distribuere_VERDI |

## 기존 objekt_VERDI 기반 관리 kjerne_VERDI 전체를 부팅하기 위해 남은 Koble_til

Neste_vare 항목은 Java 문법만으로 실행할 nummer 없는 CPU/enhet_VERDI 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot inngangspunkt_VERDI, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 kontekst_VERDI Store_VERDI
- faktisk_data PIC/PIT/PS2/ATA/PCI maskinvare_port 및 AMD PCnet DMA Loop_VERDI
- Java objekt_VERDI·MATRISE_VERDI koble_Oppsett, unntak, statisk_VERDI starte, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT fase_VERDI
- FAT 디스크 구역을 faktisk_data ATA 장치와 연결하는 I_U 접착 lag_VERDI

위 관리 계층은 engos 기능의 Java 관리 구현과 vert 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot inngangspunkt_VERDI, statisk_VERDI starte·heltall MATRISE_VERDI, VGA/직렬/PS2, 명령해석기, bruker ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 vert 루프백 패킷 왕복을 검증했다. 위 표의 objekt_VERDI 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
