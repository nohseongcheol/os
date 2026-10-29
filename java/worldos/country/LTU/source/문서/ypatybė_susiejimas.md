# engos 기능 대응표

이 표는 기존 `senstelėjusi_įranga_šaltinis/`의 objektas_VALUE 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [faktinis_duomenys 부팅 기능과 한계](../os/안내.md)를 따로 기록한다.

## Java 관리 sluoksnis_VALUE 구현 완료

| engos sritis_VALUE_0e9a97ab | JLtuOS 구현 |
|---|---|
| memorymanager, phymem | `기억공간관리자` lygiuoti_VALUE priskirti_Saugykla·išleisti_Saugykla·병합 |
| paging, virtmem | `쪽관리자` ADDRESS ADDRESS_sritis·puslapis_VALUE Prisijungti·COW·개인 Rašymas |
| gdt, tss | `전역서술자표`, `užduotis_Būsena_segmentas` |
| interrupt | `개입중단관리자` registras_įrašas·įjungti·platinti_VALUE |
| process, scheduler, thread | `Procesas_VALUE`, `planuotojas` PID·fork·wait·Būsena_VALUE SWITCH_MODE |
| systemcall/POSIX 1단계 | Skaitymas·Rašymas·Atverti·Užverti·seek·dup·fcntl·prieiga_įrašas·작업목록·naudotojas/무리 ID·sinchronizuoti·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 sekcija_VALUE Skaitymas·Rašymas |
| MSDOS partition | `pirminis_skaidinys_lentelė` MBR 검증과 네 įrašas_VALUE analizuoti_sintaksę_VALUE |
| FAT 공개 Failas sluoksnis_VALUE | `failų_sistema`, `파일서술자표` Skaitymas 전용 파일과 과정별 FD |
| ELF | ELF32 검사, sekcija_VALUE klipas 검사, 적재, NOBITS nulis_operandas 초기화, Paleisti ADDRESS·parametras_argumentas·환경 반영 |
| keyboard, mouse | `입력관리자`의 손실 계수 포함 Įvykis 대기열 |
| timer | `laikrodis` 틱과 TIME_VALUE CONVERT_VALUE |
| PCI | `주변장치연결관리자` 검색 결과와 įrenginys_VALUE žymėjimas_VALUE |
| VGA/text mode | `simbolis_rodyti` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `tinklas_Įrankiai`, `tinklo_funkcionavimo_lygmuo` kadras_INDEX 검사·kontrolinė_suma·sutarties_vertė/aparatūra_jungtis platinti_VALUE |

## 기존 objektas_VALUE 기반 관리 branduolys_VALUE 전체를 부팅하기 위해 남은 Prisijungti

toliau_prekė 항목은 Java 문법만으로 실행할 numeris 없는 CPU/įrenginys_VALUE 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot įrašas_p_VALUE, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 문맥 Store_VALUE
- faktinis_duomenys PIC/PIT/PS2/ATA/PCI aparatūra_jungtis 및 AMD PCnet DMA Loop_VALUE
- Java objektas_VALUE·ARRAY_VALUE sieti_schema, išimtis, 정적 초기화, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT etapas_VALUE
- FAT 디스크 구역을 faktinis_duomenys ATA 장치와 연결하는 Į_I 접착 sluoksnis_VALUE

위 관리 계층은 engos 기능의 Java 관리 구현과 organizuoti 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot įrašas_p_VALUE, 정적 초기화·sveikasis_skaičius ARRAY_VALUE, VGA/직렬/PS2, 명령해석기, naudotojas ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 organizuoti 루프백 패킷 왕복을 검증했다. 위 표의 objektas_VALUE 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
