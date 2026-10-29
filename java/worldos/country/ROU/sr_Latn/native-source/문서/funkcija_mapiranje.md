# engos 기능 대응표

이 표는 기존 `zastareo_izvor/`의 objekat_VALUE 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [stvarni_podaci 부팅 기능과 한계](../os/안내.md)를 따로 기록한다.

## Java 관리 sloj_VALUE 구현 완료

| engos oblast_VALUE_0e9a97ab | JRouOS 구현 |
|---|---|
| memorymanager, phymem | `Memorija_menadžer` poravnati_VALUE dodeliti_Skladište·izdanje_Skladište·병합 |
| paging, virtmem | `stranica_menadžer` adresa adresa_oblast·stranica_VALUE veze·COW·개인 쓰기 |
| gdt, tss | `전역서술자표`, `obaveza_Status_segment` |
| interrupt | `IRQ_menadžer` registar_stavka·omogućiti·distribuirati_VALUE |
| process, scheduler, thread | `Proces_VALUE`, `Planer` PID·fork·wait·Status_VALUE SWITCH_MODE |
| systemcall/POSIX 1단계 | 읽기·쓰기·otvoren·Zatvori·seek·dup·fcntl·pristup_stavka·작업목록·korisnik/무리 ID·sinhronizovati·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 odeljak_VALUE 읽기·쓰기 |
| MSDOS partition | `primarna_particija_tabela` MBR 검증과 네 stavka_VALUE raščlaniti_VALUE |
| FAT 공개 Datoteka sloj_VALUE | `sistem_datoteka`, `파일서술자표` 읽기 전용 파일과 과정별 FD |
| ELF | ELF32 검사, odeljak_VALUE klip 검사, 적재, NOBITS nula_operand 초기화, koristiti adresa·parametar_argument·환경 반영 |
| keyboard, mouse | `입력관리자`의 손실 계수 포함 događaj 대기열 |
| timer | `Sat` 틱과 TIME_VALUE CONVERT_VALUE |
| PCI | `periferijski_uređaj_magistrala_menadžer` 검색 결과와 uređaj_VALUE izbor_VALUE |
| VGA/text mode | `znak_ekran` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `Mreža_Alatke`, `sloj_mreže` kadar_INDEX 검사·kontrolni_zbir·ugovor_VALUE/포트 distribuirati_VALUE |

## 기존 objekat_VALUE 기반 관리 jezgro_VALUE 전체를 부팅하기 위해 남은 veze

Dalje_stavka 항목은 Java 문법만으로 실행할 수 없는 CPU/uređaj_VALUE 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot stavka_p_VALUE, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 문맥 Store_VALUE
- stvarni_podaci PIC/PIT/PS2/ATA/PCI 포트 및 AMD PCnet DMA Loop_VALUE
- Java objekat_VALUE·niz_VALUE Veza_Raspored, izuzetak, 정적 초기화, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT faza_VALUE
- FAT 디스크 구역을 stvarni_podaci ATA 장치와 연결하는 U_I 접착 sloj_VALUE

위 관리 계층은 engos 기능의 Java 관리 구현과 host 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot stavka_p_VALUE, 정적 초기화·ceo_broj niz_VALUE, VGA/직렬/PS2, 명령해석기, korisnik ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 host 루프백 패킷 왕복을 검증했다. 위 표의 objekat_VALUE 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
