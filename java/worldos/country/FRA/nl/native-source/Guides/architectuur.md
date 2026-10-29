# JFraOS architectuur

아래는 object_WAARDE 기반 관리 kernel_WAARDE 전체의 doel_object 구조다. actueel_item werkelijk_gegevens machineopstart 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 besturingssysteem LEESMIJ_eb81d7d9](../os/LEESMIJ_eb81d7d9.md)에 implementatie 범위를 명시한다. 아래의 GC·context_WAARDE switch_MODUS·bestandssysteem 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 laag_WAARDE
  ↓
Java AOT 실행기와 object_WAARDE·MATRIX_WAARDE·GC 런타임
  ↓
hardware_WAARDE grens_WAARDE
  ↓
Java 관리 kernel_WAARDE
  ├─ Geheugen_regio/쪽관리/COW
  ├─ Proces_WAARDE/배정/wait
  ├─ bestandssysteem/ELF/POSIX
  └─ invoer_WAARDE/opslagapparaat/net_stack
```

OpenJDK 자체는 이미 운영체제가 제공하는 bestand, 스레드, 가상 기억공간을 전제로 한다. 따라서 kernel_WAARDE 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, context_WAARDE 저장처럼 Java로 표현할 nummer 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
