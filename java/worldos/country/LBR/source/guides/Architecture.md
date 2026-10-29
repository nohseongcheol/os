# JLbrOS Architecture

아래는 objectValue foundation 관리 kernelValue 전체의 targetObject 구조다. currentItem actualData machine_boot 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 OperatingSystem README](../os/README.md)에 implementation 범위를 명시한다. 아래의 GC·contextValue switchMode·FileSystem 등이 새 ISO에 buildAll 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 minimumValue 부트·트랩 layerValue
  ↓
Java AOT 실행기와 objectValue·arrayValue·GC 런타임
  ↓
hardwareValue boundaryValue
  ↓
Java 관리 kernelValue
  ├─ memoryRegion/pageManagement/COW
  ├─ processValue/배정/wait
  ├─ FileSystem/ELF/POSIX
  └─ inputValue/storageDevice/networkStack
```

OpenJDK 자체는 이미 운영체제가 제공하는 file, 스레드, 가상 기억공간을 전제로 한다. 따라서 kernelValue 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java bytecode AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, contextValue 저장처럼 Java로 표현할 number 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
