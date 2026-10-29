# JMozOS arquitetura

아래는 objeto_VALOR 기반 관리 kernel_VALOR 전체의 alvo_objeto 구조다. em_dia_item real_dados arranque_da_máquina 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 SO LEIAME_eb81d7d9](../os/LEIAME_eb81d7d9.md)에 implementação 범위를 명시한다. 아래의 GC·contexto_VALOR mudar_MODO·sistema_de_arquivos 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 camada_VALOR
  ↓
Java AOT 실행기와 objeto_VALOR·MATRIZ_VALOR·GC 런타임
  ↓
hardware_VALOR limite_VALOR
  ↓
Java 관리 kernel_VALOR
  ├─ Memória_região/쪽관리/COW
  ├─ Processo_VALOR/배정/wait
  ├─ sistema_de_arquivos/ELF/POSIX
  └─ entrada_VALOR/dispositivo_de_armazenamento/rede_pilha
```

OpenJDK 자체는 이미 운영체제가 제공하는 ficheiro, 스레드, 가상 기억공간을 전제로 한다. 따라서 kernel_VALOR 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, contexto_VALOR 저장처럼 Java로 표현할 número 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
