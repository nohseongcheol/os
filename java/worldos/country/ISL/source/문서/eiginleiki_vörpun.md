# engos 기능 대응표

이 표는 기존 `eldra_uppruni/`의 hlutur_VALUE 기반 JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [raun_gögn 부팅 기능과 한계](../os/LESTUMIG_eb81d7d9.md)를 따로 기록한다.

## Java 관리 lag_VALUE 구현 완료

| engos 영역 | JIslOS 구현 |
|---|---|
| memorymanager, phymem | `Minni_stjórnandi` stilla_VALUE úthluta_geymsla·losa_geymsla·병합 |
| paging, virtmem | `síða_stjórnandi` slóð 공간·síða_VALUE Tengjast·COW·개인 Skrift |
| gdt, tss | `전역서술자표`, `verk_staða_hluti` |
| interrupt | `IRQ_stjórnandi` skrá_færsla·kveikja·dreifa_VALUE |
| process, scheduler, thread | `Ferli_VALUE`, `Verkraðari` PID·fork·wait·staða_VALUE_e10195a1 SWITCH_MODE |
| systemcall/POSIX 1단계 | Lestur·Skrift·Opna·Loka·seek·dup·fcntl·aðgangur_færsla·작업목록·notandi/무리 ID·samstilla·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `고급기술결합장치` 512바이트 hluti_VALUE Lestur·Skrift |
| MSDOS partition | `기본분할영역표` MBR 검증과 네 færsla_VALUE þátta_VALUE |
| FAT 공개 Skrá lag_VALUE | `skrárkerfi`, `파일서술자표` Lestur 전용 파일과 과정별 FD |
| ELF | ELF32 검사, hluti_VALUE miðlaskrá 검사, 적재, NOBITS 영 frumstilla, Keyra_2 slóð·færibreyta_frumbreyta·환경 반영 |
| keyboard, mouse | `입력관리자`의 손실 계수 포함 atvik 대기열 |
| timer | `klukka` 틱과 TIME_VALUE CONVERT_VALUE |
| PCI | `aukabúnaður_tengibraut_stjórnandi` 검색 결과와 tæki_VALUE val_VALUE |
| VGA/text mode | `stafur_birta` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `Net_Verkfæri`, `Net_lag` ramma_INDEX 검사·prófsumma·samningsvirði/포트 dreifa_VALUE |

## 기존 hlutur_VALUE 기반 관리 kjarni_VALUE 전체를 부팅하기 위해 남은 Tengjast

Áfram_vara 항목은 Java 문법만으로 실행할 númer 없는 CPU/tæki_VALUE 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot færsla_P_VALUE, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 Samhengi_VALUE Store_VALUE
- raun_gögn PIC/PIT/PS2/ATA/PCI 포트 및 AMD PCnet DMA Loop_VALUE
- Java hlutur_VALUE·ARRAY_VALUE tengja_útlit, undantekning, fast_VALUE frumstilla, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT stig_VALUE
- FAT 디스크 구역을 raun_gögn ATA 장치와 연결하는 I_Ú 접착 lag_VALUE

위 관리 계층은 engos 기능의 Java 관리 구현과 hýsa 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot færsla_P_VALUE, fast_VALUE frumstilla·heiltala ARRAY_VALUE, VGA/직렬/PS2, 명령해석기, notandi ELF/ring 3/시스템 호출, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 hýsa 루프백 패킷 왕복을 검증했다. 위 표의 hlutur_VALUE 기반 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
