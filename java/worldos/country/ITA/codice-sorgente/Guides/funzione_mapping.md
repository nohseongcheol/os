# engos 기능 대응표

이 표는 기존 `legacy_fonte/`의 oggetto_VALORE 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [effettivo_dati avvio_macchina 기능과 한계](../os/README_eb81d7d9.md)를 따로 기록한다.

## Java 관리 layer_VALORE implementazione 완료

| engos area_VALORE | JItaOS implementazione |
|---|---|
| memorymanager, phymem | `Memoria_manager` allineare_VALORE allocare_Memoria·release_Memoria·병합 |
| paging, virtmem | `Gestione_pagine` e_mail e_mail_area·pagina_VALORE Connetti·COW·개인 Scrittura |
| gdt, tss | `tabella_dei_descrittori_globali`, `task_Stato_segmento` |
| interrupt | `IRQ_manager` registro_voce·abilitare·distribuire_VALORE |
| process, scheduler, thread | `Processi_VALORE`, `Pianificatore` PID·fork·wait·Stato_VALORE SWITCH_MODA |
| systemcall/POSIX 1단계 | Lettura·Scrittura·Apri·Chiudi·seek·dup·fcntl·accesso_voce·작업목록·spazio_utente/무리 ID·sincronizzare·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 sezione_VALORE Lettura·Scrittura |
| MSDOS partition | `partizione_primaria_tabella` MBR 검증과 네 voce_VALORE analizzare_VALORE |
| FAT 공개 file layer_VALORE | `file_system`, `File_descrittore_tabella` Lettura 전용 파일과 과정별 FD |
| ELF | ELF32 검사, sezione_VALORE ritagliare 검사, 적재, NOBITS zero_operando inizializza, avvia e_mail·parametro_argomento·ambiente 반영 |
| keyboard, mouse | `input_manager`의 손실 계수 dichiarazioni Evento 대기열 |
| timer | `clock` 틱과 valore CONVERTI_VALORE |
| PCI | `accessorio_bus_manager` 검색 결과와 cellulare_VALORE selezione_VALORE |
| VGA/text mode | `carattere_display` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `rete_Strumenti`, `livello_rete` frame_INDICE 검사·checksum·valore_di_contratto/hardware_porta distribuire_VALORE |

## 기존 oggetto_VALORE 기반 관리 kernel_VALORE 전체를 부팅하기 위해 남은 Connetti

Avanti_articolo 항목은 Java 문법만으로 실행할 numero 없는 CPU/cellulare_VALORE 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot punto_di_ingresso_VALORE, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 contesto_VALORE Store_VALORE
- effettivo_dati PIC/PIT/PS2/ATA/PCI hardware_porta 및 AMD PCnet DMA Loop_VALORE
- Java oggetto_VALORE·array_VALORE disposizione_di_collegamento, eccezione, statico_VALORE inizializza, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT area_VALORE_29ee1bb7
- FAT 디스크 구역을 effettivo_dati ATA 장치와 연결하는 I_O 접착 layer_VALORE

위 관리 계층은 engos 기능의 Java 관리 구현과 host 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot punto_di_ingresso_VALORE, statico_VALORE inizializza·intero array_VALORE, VGA/seriale_VALORE/PS2, InterpreteComandi, spazio_utente ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 host 루프백 패킷 왕복을 검증했다. 위 표의 oggetto_VALORE 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
