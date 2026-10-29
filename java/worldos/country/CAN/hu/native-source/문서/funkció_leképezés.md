# engos 기능 대응표

이 표는 기존 `örökség_forrás/`의 objektum_ÉRTÉK 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [tényleges_adat 부팅 기능과 한계](../os/fontos_fájl_eb81d7d9.md)를 따로 기록한다.

## Java 관리 réteg_ÉRTÉK 구현 완료

| engos régió_ÉRTÉK | JCanOS 구현 |
|---|---|
| memorymanager, phymem | `Memória_kezelő` igazít_ÉRTÉK kioszt_tár·kiad_tár·병합 |
| paging, virtmem | `lap_kezelő` CÍM CÍM_régió·lap_ÉRTÉK Kapcsolódás·COW·개인 Írás |
| gdt, tss | `globális_leírótábla`, `teendő_Állapot_szegmens` |
| interrupt | `megszakítás_kezelő` jegyzék_bejegyzés·bekapcsol·eloszt_ÉRTÉK |
| process, scheduler, thread | `folyamat_ÉRTÉK`, `Ütemező` PID·fork·wait·Állapot_ÉRTÉK vált_mód |
| systemcall/POSIX 1단계 | Olvasás·Írás·Megnyitás·Bezárás·seek·dup·fcntl·hozzáfér_bejegyzés·작업목록·felhasználó/무리 ID·szinkronizál·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 szakasz_ÉRTÉK Olvasás·Írás |
| MSDOS partition | `elsődleges_partíció_tábla` MBR 검증과 네 bejegyzés_ÉRTÉK elemez_ÉRTÉK |
| FAT 공개 Fájl réteg_ÉRTÉK | `fájlrendszer`, `파일서술자표` Olvasás 전용 파일과 과정별 FD |
| ELF | ELF32 검사, szakasz_ÉRTÉK klip 검사, 적재, NOBITS nulla_operandus inicializál, Futtatás CÍM·paraméter_argumentum·környezet_5d36e09c 반영 |
| keyboard, mouse | `bevitel_kezelő`의 손실 계수 포함 Esemény 대기열 |
| timer | `Óra` 틱과 IDŐ_ÉRTÉK konvertál_ÉRTÉK |
| PCI | `tartozék_busz_kezelő` 검색 결과와 mobil_ÉRTÉK kijelölés_ÉRTÉK |
| VGA/text mode | `karakter_kijelző` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `hálózat_Eszközök`, `hálózati_réteg` doboz_INDEX 검사·ellenőrzőösszeg·szerződés_értéke/hardver_port eloszt_ÉRTÉK |

## 기존 objektum_ÉRTÉK 기반 관리 kernel_ÉRTÉK 전체를 부팅하기 위해 남은 Kapcsolódás

Tovább_cikk 항목은 Java 문법만으로 실행할 szám 없는 CPU/mobil_ÉRTÉK 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot belépési_pont_ÉRTÉK, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 környezet_ÉRTÉK tár_ÉRTÉK
- tényleges_adat PIC/PIT/PS2/ATA/PCI hardver_port 및 AMD PCnet DMA Loop_ÉRTÉK
- Java objektum_ÉRTÉK·TÖMB_ÉRTÉK csatol_Navigáció, kivétel, statikus_ÉRTÉK inicializál, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT fázis_ÉRTÉK
- FAT 디스크 구역을 tényleges_adat ATA 장치와 연결하는 I_O 접착 réteg_ÉRTÉK

위 관리 계층은 engos 기능의 Java 관리 구현과 gazda 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot belépési_pont_ÉRTÉK, statikus_ÉRTÉK inicializál·egész_szám TÖMB_ÉRTÉK, VGA/직렬/PS2, 명령해석기, felhasználó ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 gazda 루프백 패킷 왕복을 검증했다. 위 표의 objektum_ÉRTÉK 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
