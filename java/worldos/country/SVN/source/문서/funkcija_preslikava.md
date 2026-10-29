# engos 기능 대응표

이 표는 기존 `starejši_vir/`의 predmet_VALUE 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [dejanski_podatki 부팅 기능과 한계](../os/안내.md)를 따로 기록한다.

## Java 관리 sloj_VALUE 구현 완료

| engos območje_VALUE_0e9a97ab | JSvnOS 구현 |
|---|---|
| memorymanager, phymem | `pomnilnik_Upravitelj` poravnati_VALUE dodeliti_Senzor_prostora·izdaja_Senzor_prostora·병합 |
| paging, virtmem | `stran_Upravitelj` naslov naslov_območje·stran_VALUE Poveži·COW·개인 Pisanje |
| gdt, tss | `GDT`, `opravek_stanje_segment` |
| interrupt | `prekinitev_Upravitelj` register_vnos·vklopiti·distribuirati_VALUE |
| process, scheduler, thread | `Proces_VALUE`, `Načrtovalec` PID·fork·wait·stanje_VALUE SWITCH_MODE |
| systemcall/POSIX 1단계 | Branje·Pisanje·Odpri·Zapri·seek·dup·fcntl·dostop_vnos·작업목록·uporabnik/무리 ID·sinhronizirati·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 odsek_VALUE Branje·Pisanje |
| MSDOS partition | `primarna_particija_tabela` MBR 검증과 네 vnos_VALUE razčlenjevati_VALUE |
| FAT 공개 Datoteka sloj_VALUE | `datotečni_sistem`, `파일서술자표` Branje 전용 파일과 과정별 FD |
| ELF | ELF32 검사, odsek_VALUE izrezek 검사, 적재, NOBITS nič_operand inicializirati, Zaženi naslov·parameter_argument·환경 반영 |
| keyboard, mouse | `입력관리자`의 손실 계수 포함 dogodek 대기열 |
| timer | `Ura` 틱과 čas_VALUE CONVERT_VALUE |
| PCI | `zunanji_vodilo_Upravitelj` 검색 결과와 naprava_VALUE izbor_VALUE |
| VGA/text mode | `znak_zaslon` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `mreža_Orodja`, `omrežna_plast` okvir_INDEX 검사·kontrolna_vsota·primer_VALUE/strojna_oprema_vrata distribuirati_VALUE |

## 기존 predmet_VALUE 기반 관리 jedro_VALUE 전체를 부팅하기 위해 남은 Poveži

Naprej_element 항목은 Java 문법만으로 실행할 수 없는 CPU/naprava_VALUE 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot vnos_p_VALUE, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 문맥 Store_VALUE
- dejanski_podatki PIC/PIT/PS2/ATA/PCI strojna_oprema_vrata 및 AMD PCnet DMA Loop_VALUE
- Java predmet_VALUE·ARRAY_VALUE Povezava_Krmarjenje, izjema, statičen_VALUE inicializirati, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT območje_VALUE_29ee1bb7
- FAT 디스크 구역을 dejanski_podatki ATA 장치와 연결하는 V_I 접착 sloj_VALUE

위 관리 계층은 engos 기능의 Java 관리 구현과 gostiti 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot vnos_p_VALUE, statičen_VALUE inicializirati·celo_število ARRAY_VALUE, VGA/직렬/PS2, 명령해석기, uporabnik ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 gostiti 루프백 패킷 왕복을 검증했다. 위 표의 predmet_VALUE 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
