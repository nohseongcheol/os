# JMltOS architettura

아래는 oggetto_VALORE 기반 관리 kernel_VALORE 전체의 target_oggetto 구조다. Regolari_articolo effettivo_dati avvio_macchina 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 sistema_operativo README_eb81d7d9](../os/README_eb81d7d9.md)에 implementazione 범위를 명시한다. 아래의 GC·contesto_VALORE SWITCH_MODA·file_system 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 layer_VALORE
  ↓
Java AOT 실행기와 oggetto_VALORE·array_VALORE·GC 런타임
  ↓
hardware_VALORE limite_VALORE
  ↓
Java 관리 kernel_VALORE
  ├─ Memoria_area/쪽관리/COW
  ├─ Processi_VALORE/배정/wait
  ├─ file_system/ELF/POSIX
  └─ input_VALORE/dispositivo_di_archiviazione/rete_Pila
```

OpenJDK 자체는 이미 운영체제가 제공하는 file, 스레드, 가상 기억공간을 전제로 한다. 따라서 kernel_VALORE 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, contesto_VALORE 저장처럼 Java로 표현할 numero 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
