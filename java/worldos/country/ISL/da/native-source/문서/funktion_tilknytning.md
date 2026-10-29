# engos 기능 대응표

이 표는 기존 `nedarvet_kilde/`의 objekt_VÆRDI 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [faktisk_data 부팅 기능과 한계](../os/Vigtigt_eb81d7d9.md)를 따로 기록한다.

## Java 관리 lag_VÆRDI 구현 완료

| engos område_VÆRDI_0e9a97ab | JIslOS 구현 |
|---|---|
| memorymanager, phymem | `Hukommelse_Leder` justere_VÆRDI tildel_Lager·udgive_Lager·병합 |
| paging, virtmem | `Sidestyring` mail mail_område·side_VÆRDI Tilslut·COW·개인 Skrive |
| gdt, tss | `전역서술자표`, `job_status_segment` |
| interrupt | `IRQ_Leder` register_post·slå_til·fordele_VÆRDI |
| process, scheduler, thread | `Proces_VÆRDI`, `Scheduler` PID·fork·wait·status_VÆRDI SKIFT_HYPPIGST |
| systemcall/POSIX 1단계 | Læse·Skrive·Åbn·Luk·seek·dup·fcntl·åbne_post·작업목록·bruger/무리 ID·synkronisere·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 sektion_VÆRDI Læse·Skrive |
| MSDOS partition | `primær_partition_tabel` MBR 검증과 네 post_VÆRDI_962f286b opdele_tekst_VÆRDI |
| FAT 공개 Fil lag_VÆRDI | `filsystem`, `파일서술자표` Læse 전용 파일과 과정별 FD |
| ELF | ELF32 검사, sektion_VÆRDI klippe 검사, 적재, NOBITS nul_operand starte, Kør_2 mail·parameter_argument·miljø 반영 |
| keyboard, mouse | `input_Leder`의 손실 계수 포함 hændelse 대기열 |
| timer | `Ur` 틱과 TID_VÆRDI KONVERTER_VÆRDI |
| PCI | `tilbehør_bus_Leder` 검색 결과와 enhed_VÆRDI markering_VÆRDI |
| VGA/text mode | `tegn_vise` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `netværk_Værktøjer`, `netværkslag` ramme_INDEKS 검사·kontrolsum·kontraktværdi/hardware_port fordele_VÆRDI |

## 기존 objekt_VÆRDI 기반 관리 kerne_VÆRDI 전체를 부팅하기 위해 남은 Tilslut

Næste_vare 항목은 Java 문법만으로 실행할 tal 없는 CPU/enhed_VÆRDI 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot indgangspunkt_VÆRDI, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 kontekst_VÆRDI Store_VÆRDI
- faktisk_data PIC/PIT/PS2/ATA/PCI hardware_port 및 AMD PCnet DMA Loop_VÆRDI
- Java objekt_VÆRDI·MATRIX_VÆRDI Link_Layout, undtagelse, statisk_VÆRDI starte, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT fase_VÆRDI
- FAT 디스크 구역을 faktisk_data ATA 장치와 연결하는 I_O 접착 lag_VÆRDI

위 관리 계층은 engos 기능의 Java 관리 구현과 vært 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot indgangspunkt_VÆRDI, statisk_VÆRDI starte·heltal MATRIX_VÆRDI, VGA/직렬/PS2, 명령해석기, bruger ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 vært 루프백 패킷 왕복을 검증했다. 위 표의 objekt_VÆRDI 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
