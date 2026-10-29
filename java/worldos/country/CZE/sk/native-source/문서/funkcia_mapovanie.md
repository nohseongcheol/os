# engos 기능 대응표

이 표는 기존 `starší_zdroj/`의 objekt_VALUE 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [skutočný_údaje 부팅 기능과 한계](../os/안내.md)를 따로 기록한다.

## Java 관리 vrstva_VALUE 구현 완료

| engos oblasť_VALUE_0e9a97ab | JCzeOS 구현 |
|---|---|
| memorymanager, phymem | `기억공간관리자` zarovnať_VALUE vyhradiť_Úložisko·vydať_Úložisko·병합 |
| paging, virtmem | `쪽관리자` adresa adresa_oblasť·strana_VALUE Pripojiť·COW·개인 Zápis |
| gdt, tss | `전역서술자표`, `úloha_Stav_segment` |
| interrupt | `개입중단관리자` register_položka·zapnúť·distribuovať_VALUE |
| process, scheduler, thread | `Proces_VALUE`, `Plánovač` PID·fork·wait·Stav_VALUE SWITCH_MODE |
| systemcall/POSIX 1단계 | Čítanie·Zápis·Otvoriť·Zatvoriť·seek·dup·fcntl·prístup_položka·작업목록·používateľ/무리 ID·synchronizovať·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 sekcia_VALUE Čítanie·Zápis |
| MSDOS partition | `기본분할영역표` MBR 검증과 네 položka_VALUE analyzovať_VALUE |
| FAT 공개 Súbor vrstva_VALUE | `systém_súborov`, `파일서술자표` Čítanie 전용 파일과 과정별 FD |
| ELF | ELF32 검사, sekcia_VALUE klip 검사, 적재, NOBITS 영 incializovať, Spustiť_2 adresa·parameter_argument·환경 반영 |
| keyboard, mouse | `입력관리자`의 손실 계수 포함 Udalosť 대기열 |
| timer | `Hodiny` 틱과 čas_VALUE CONVERT_VALUE |
| PCI | `주변장치연결관리자` 검색 결과와 telefón_VALUE výber_VALUE |
| VGA/text mode | `znak_displej` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `sieť_Nástroje`, `sieťová_vrstva` rám_INDEX 검사·kontrolný_súčet·prípad_VALUE/hardvér_port distribuovať_VALUE |

## 기존 objekt_VALUE 기반 관리 jadro_VALUE 전체를 부팅하기 위해 남은 Pripojiť

Ďalej_položka 항목은 Java 문법만으로 실행할 수 없는 CPU/telefón_VALUE 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot položka_bod_VALUE, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 문맥 Store_VALUE
- skutočný_údaje PIC/PIT/PS2/ATA/PCI hardvér_port 및 AMD PCnet DMA Loop_VALUE
- Java objekt_VALUE·pole_VALUE odkaz_Navigácia, výnimka, 정적 incializovať, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT etapa_VALUE
- FAT 디스크 구역을 skutočný_údaje ATA 장치와 연결하는 vstup_a_výstup 접착 vrstva_VALUE

위 관리 계층은 engos 기능의 Java 관리 구현과 hostiteľ 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot položka_bod_VALUE, 정적 incializovať·celé_číslo pole_VALUE, VGA/직렬/PS2, 명령해석기, používateľ ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 hostiteľ 루프백 패킷 왕복을 검증했다. 위 표의 objekt_VALUE 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
