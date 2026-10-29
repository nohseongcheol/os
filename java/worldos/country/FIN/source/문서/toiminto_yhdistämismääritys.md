# engos 기능 대응표

이 표는 기존 `vanha_lähde/`의 objekti_ARVO 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [todellinen_data koneen_käynnistys 기능과 한계](../os/Lueminut_eb81d7d9.md)를 따로 기록한다.

## Java 관리 kerros_ARVO_e65604ef toteutus 완료

| engos alue_ARVO_0e9a97ab | JFinOS toteutus |
|---|---|
| memorymanager, phymem | `Muisti_Valvoja` tasaa_ARVO jakaa_Tallennus·julkaista_Tallennus·병합 |
| paging, virtmem | `page_Valvoja` OSOITE OSOITE_alue·page_ARVO Yhdistä·COW·개인 Kirjoitus |
| gdt, tss | `전역서술자표`, `tehtävä_Tila_segmentti` |
| interrupt | `IRQ_Valvoja` rekisteri_merkintä·ota_käyttöön·jaa_ARVO |
| process, scheduler, thread | `prosessi_ARVO`, `Aikataulutus` PID·fork·wait·Tila_ARVO MUUTA_tila |
| systemcall/POSIX 1단계 | Luku·Kirjoitus·Avaa·Sulje·seek·dup·fcntl·pääsy_merkintä_68aed533·작업목록·käyttäjätila/무리 ID·synkronoi·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 osa_ARVO Luku·Kirjoitus |
| MSDOS partition | `ensisijainen_osio_taulukko` MBR 검증과 네 merkintä_ARVO_962f286b jäsentää_ARVO |
| FAT 공개 tiedoston_nimi kerros_ARVO_e65604ef | `tiedostojärjestelmä`, `파일서술자표` Luku 전용 파일과 과정별 FD |
| ELF | ELF32 검사, osa_ARVO leikata 검사, 적재, NOBITS nolla_operandi alustaa, Suorita_2 OSOITE·parametri_argumentti·ympäristö 반영 |
| keyboard, mouse | `syöte_Valvoja`의 손실 계수 esittelyt Tapahtuma 대기열 |
| timer | `Kello` 틱과 AIKA_ARVO MUUNNA_ARVO |
| PCI | `lisälaite_väylä_Valvoja` 검색 결과와 laite_ARVO valinta_ARVO |
| VGA/text mode | `merkki_näyttö` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `verkko_Työkalut`, `verkkotaso` kuva_INDEKSI 검사·tarkistussumma·sopimuksen_arvo/laitteisto_portti jaa_ARVO |

## 기존 objekti_ARVO 기반 관리 ydin_ARVO 전체를 부팅하기 위해 남은 Yhdistä

Seuraava_kohde 항목은 Java 문법만으로 실행할 numero 없는 CPU/laite_ARVO 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot aloituskohta_ARVO, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 konteksti_ARVO Store_ARVO
- todellinen_data PIC/PIT/PS2/ATA/PCI laitteisto_portti 및 AMD PCnet DMA Loop_ARVO
- Java objekti_ARVO·MATRIISI_ARVO linkitysasettelu, poikkeus, staattinen_ARVO alustaa, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT vaihe_ARVO
- FAT 디스크 구역을 todellinen_data ATA 장치와 연결하는 I_O 접착 kerros_ARVO_e65604ef

위 관리 계층은 engos 기능의 Java 관리 구현과 isäntä 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot aloituskohta_ARVO, staattinen_ARVO alustaa·kokonaisluku MATRIISI_ARVO, VGA/직렬/PS2, 명령해석기, käyttäjätila ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 isäntä 루프백 패킷 왕복을 검증했다. 위 표의 objekti_ARVO 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
