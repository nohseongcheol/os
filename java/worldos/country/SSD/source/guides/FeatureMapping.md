# engos 기능 대응표

이 표는 기존 `legacySource/`의 objectValue foundation JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [actualData machine_boot 기능과 boundaryLimit](../os/README.md)를 따로 기록한다.

## Java 관리 layerValue implementation isComplete

| engos regionValue | JSsdOS implementation |
|---|---|
| memorymanager, phymem | `MemoryManager` alignValue allocateStorage·releaseStorage·병합 |
| paging, virtmem | `PageManager` address addressRegion·pageValue connect·COW·개인 write |
| gdt, tss | `GlobalDescriptorTable`, `TaskStateSegment` |
| interrupt | `InterruptManager` registerEntry·enable·distributeValue |
| process, scheduler, thread | `processValue`, `Scheduler` PID·fork·wait·stateValue switchMode |
| systemcall/POSIX 1단계 | read·write·open·close·seek·dup·fcntl·accessEntry·작업목록·User/무리 ID·synchronize·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `AdvancedTechnologyAttachment` 512바이트 sectionValue read·write |
| MSDOS partition | `primaryPartitionTable` MBR 검증과 네 entryValue parseValue |
| FAT 공개 file layerValue | `FileSystem`, `fileDescriptorTable` read 전용 파일과 과정별 FD |
| ELF | ELF32 Checks, sectionValue clip Checks, 적재, NOBITS zeroOperand initialize, run address·parameterArgument·environment 반영 |
| keyboard, mouse | `InputManager`의 손실 계수 headers event 대기열 |
| timer | `Clock` 틱과 timeValue convertValue |
| PCI | `PeripheralBusManager` 검색 결과와 deviceValue selectionValue |
| VGA/text mode | `characterDisplay` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `NetworkTools`, `NetworkLayer` frameIndex Checks·checksum·contractValue/hardwarePort distributeValue |

## 기존 objectValue foundation 관리 kernelValue 전체를 부팅하기 위해 남은 connect

nextItem 항목은 Java 문법만으로 실행할 number 없는 CPU/deviceValue 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot entryPointValue, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 contextValue storeValue
- actualData PIC/PIT/PS2/ATA/PCI hardwarePort 및 AMD PCnet DMA loopValue
- Java objectValue·arrayValue link_layout, exception, staticValue initialize, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT stageValue
- FAT 디스크 구역을 actualData ATA 장치와 연결하는 inputOutput 접착 layerValue

topValue 관리 계층은 engos 기능의 Java 관리 구현과 Host 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot entryPointValue, staticValue initialize·Integer arrayValue, VGA/serialValue/PS2, CommandInterpreter, User ELF/ring 3/시스템 invoke, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 Host 루프백 패킷 왕복을 검증했다. topValue 표의 objectValue foundation 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
