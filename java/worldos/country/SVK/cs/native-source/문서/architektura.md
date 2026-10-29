# JSvkOS architektura

아래는 objekt_HODNOTA 기반 관리 jádro_HODNOTA 전체의 cíl_objekt 구조다. dobrá_zboží skutečný_data spuštění_stroje 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 operační_systém 안내](../os/안내.md)에 implementace 범위를 명시한다. 아래의 GC·kontext_HODNOTA SWITCH_MODE·systém_souborů 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 vrstva_HODNOTA
  ↓
Java AOT 실행기와 objekt_HODNOTA·pole_HODNOTA·GC 런타임
  ↓
hardware_HODNOTA mez_HODNOTA
  ↓
Java 관리 jádro_HODNOTA
  ├─ Paměť_oblast/쪽관리/COW
  ├─ Proces_HODNOTA/배정/wait
  ├─ systém_souborů/ELF/POSIX
  └─ vstup_HODNOTA/úložiště/síť_Štos
```

OpenJDK 자체는 이미 운영체제가 제공하는 název_souboru, 스레드, 가상 기억공간을 전제로 한다. 따라서 jádro_HODNOTA 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, kontext_HODNOTA 저장처럼 Java로 표현할 číslo 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
