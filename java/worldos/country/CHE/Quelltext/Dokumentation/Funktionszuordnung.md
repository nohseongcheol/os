# engos 기능 대응표

이 표는 기존 `Kernquelltext/`의 objektWert grundlage JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [tatsächlichDaten Startvorgang 기능과 grenzstelleGrenzwert](../os/Anleitung.md)를 따로 기록한다.

## Java 관리 schichtWert umsetzung istFertig

| engos gebietWert | JCheOS umsetzung |
|---|---|
| memorymanager, phymem | `SpeicherVerwalter` ausrichtenWert speichergerätZuteilen·speichergerätFreigeben·병합 |
| paging, virtmem | `SeiteVerwalter` adresse adresseGebiet·seiteWert verbinden·COW·개인 schreiben |
| gdt, tss | `GlobalDeskriptorTabelle`, `AufgabeStatuswertSegment` |
| interrupt | `UnterbrechenVerwalter` eintragRegister·aktivieren·wertVerteilen |
| process, scheduler, thread | `prozessWert`, `Ablaufplaner` PID·fork·wait·statuswertWert umschaltenBetriebsart |
| systemcall/POSIX 1단계 | lesen·schreiben·öffnen·schließen·seek·dup·fcntl·zugriffEintrag·작업목록·Benutzer/무리 ID·synchronisieren·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `FortgeschrittenTechnikAnhang` 512바이트 abschnittWert lesen·schreiben |
| MSDOS partition | `hauptPartitionTabelle` MBR 검증과 네 eintragWert wertAnalysieren |
| FAT 공개 Datei schichtWert | `DateiSystem`, `dateiDeskriptorTabelle` lesen 전용 파일과 과정별 FD |
| ELF | ELF32 Prüfpunkte, abschnittWert beschneiden Prüfpunkte, 적재, NOBITS nullwertOperand initialisieren, ausführenVorgang adresse·parameterArgument·umgebung 반영 |
| keyboard, mouse | `EingabeVerwalter`의 손실 계수 Kopfdateien ereignis 대기열 |
| timer | `Uhr` 틱과 zeitWert wertUmwandeln |
| PCI | `PeripherieBusVerwalter` 검색 결과와 Gerät auswahlWert |
| VGA/text mode | `zeichenDarstellen` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `NetzwerkWerkzeuge`, `NetzwerkSchicht` rahmenIndex Prüfpunkte·kontrollsumme·vertragWert/hardwarePort wertVerteilen |

## 기존 objektWert grundlage 관리 betriebskernWert 전체를 부팅하기 위해 남은 verbinden

nächsterElementeintrag 항목은 Java 문법만으로 실행할 Zahl 없는 CPU/Gerät 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot eintragPunktWert, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 kontextWert ablegenDatenWert
- tatsächlichDaten PIC/PIT/PS2/ATA/PCI hardwarePort 및 AMD PCnet DMA schleifeWert
- Java objektWert·datenfeldWert Bindungsanordnung, ausnahme, statischWert initialisieren, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT stufeWert
- FAT 디스크 구역을 tatsächlichDaten ATA 장치와 연결하는 eingabeAusgabe 접착 schichtWert

oberkanteWert 관리 계층은 engos 기능의 Java 관리 구현과 Wirtssystem 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot eintragPunktWert, statischWert initialisieren·Ganzzahl datenfeldWert, VGA/seriellWert/PS2, Befehlsinterpreter, Benutzer ELF/ring 3/시스템 aufrufen, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 Wirtssystem 루프백 패킷 왕복을 검증했다. oberkanteWert 표의 objektWert grundlage 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
