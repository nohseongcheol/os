# engos 기능 대응표

이 표는 기존 `starsze_źródło/`의 obiekt_WARTOŚĆ 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [rzeczywisty_dane rozruch_maszyny 기능과 한계](../os/plik_README_eb81d7d9.md)를 따로 기록한다.

## Java 관리 warstwa_WARTOŚĆ implementacja 완료

| engos region_WARTOŚĆ | JDeuOS implementacja |
|---|---|
| memorymanager, phymem | `Pamięć_Menedżer` wyrównać_WARTOŚĆ przydzielić_Pamięć·wersja_Pamięć·병합 |
| paging, virtmem | `strona_Menedżer` Adres ADRES_region·strona_WARTOŚĆ Połącz·COW·개인 Zapis |
| gdt, tss | `Globalna_deskryptor_tabela`, `zadanie_Stan_odcinek` |
| interrupt | `przerwanie_Menedżer` rejestr_wpis·włączyć·rozproszony_WARTOŚĆ |
| process, scheduler, thread | `Proces_WARTOŚĆ`, `Scheduler` PID·fork·wait·Stan_WARTOŚĆ zmiana_tryb |
| systemcall/POSIX 1단계 | Odczyt·Zapis·Otwórz·Zamknięte·seek·dup·fcntl·dostęp_wpis·작업목록·przestrzeń_użytkownika/무리 ID·synchronizować·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 obszar_WARTOŚĆ_366e0bfa Odczyt·Zapis |
| MSDOS partition | `partycja_podstawowa_tabela` MBR 검증과 네 wpis_WARTOŚĆ analizować_WARTOŚĆ |
| FAT 공개 nazwa_pliku warstwa_WARTOŚĆ | `system_plików`, `Plik_deskryptor_tabela` Odczyt 전용 파일과 과정별 FD |
| ELF | ELF32 검사, obszar_WARTOŚĆ_366e0bfa obcinać 검사, 적재, NOBITS zero_operand inicjuj, Uruchom_2 Adres·parametr_argument·środowisko 반영 |
| keyboard, mouse | `wejście_Menedżer`의 손실 계수 deklaracje Wydarzenie 대기열 |
| timer | `Zegar` 틱과 wartość_czasu KONWERTUJ_WARTOŚĆ |
| PCI | `akcesorium_magistrala_Menedżer` 검색 결과와 urządzenie_WARTOŚĆ zaznaczenie_WARTOŚĆ |
| VGA/text mode | `znak_wyświetlać` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `sieć_Narzędzia`, `warstwa_sieciowa` kadr_INDEKS 검사·suma_kontrolna·wartość_kontraktu/sprzęt_port rozproszony_WARTOŚĆ |

## 기존 obiekt_WARTOŚĆ 기반 관리 jądro_WARTOŚĆ 전체를 부팅하기 위해 남은 Połącz

Dalej_towar 항목은 Java 문법만으로 실행할 identyfikator 없는 CPU/urządzenie_WARTOŚĆ 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot punkt_wejścia_WARTOŚĆ, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 kontekst_WARTOŚĆ Store_WARTOŚĆ
- rzeczywisty_dane PIC/PIT/PS2/ATA/PCI sprzęt_port 및 AMD PCnet DMA Loop_WARTOŚĆ
- Java obiekt_WARTOŚĆ·TABLICA_WARTOŚĆ układ_konsolidacji, wyjątek, statyczny_WARTOŚĆ inicjuj, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT etap_WARTOŚĆ
- FAT 디스크 구역을 rzeczywisty_dane ATA 장치와 연결하는 We_Wy 접착 warstwa_WARTOŚĆ

위 관리 계층은 engos 기능의 Java 관리 구현과 host 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot punkt_wejścia_WARTOŚĆ, statyczny_WARTOŚĆ inicjuj·liczba_całkowita TABLICA_WARTOŚĆ, VGA/직렬/PS2, polecenie_interpreter, przestrzeń_użytkownika ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 host 루프백 패킷 왕복을 검증했다. 위 표의 obiekt_WARTOŚĆ 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
