# JSxmOS Arquitectura

아래는 valorObjeto fundamento 관리 valorNúcleo 전체의 objetoObjetivo 구조다. elementoListaActual datosEfectivo Arranque 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 SistemaOperativo Guía](../os/Guía.md)에 implementación 범위를 명시한다. 아래의 GC·valorContexto modoConmutar·SistemaArchivo 등이 새 ISO에 construirTodos 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 valorMínimo 부트·트랩 valorCapa
  ↓
Java AOT 실행기와 valorObjeto·valorArreglo·GC 런타임
  ↓
valorEquipoFísico valorFrontera
  ↓
Java 관리 valorNúcleo
  ├─ EspacioMemoria/gestiónPágina/COW
  ├─ valorProceso/배정/wait
  ├─ SistemaArchivo/ELF/POSIX
  └─ valorEntrada/dispositivoAlmacenamiento/PilaRed
```

OpenJDK 자체는 이미 운영체제가 제공하는 Archivo, 스레드, 가상 기억공간을 전제로 한다. 따라서 valorNúcleo 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java códigoBytes AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, valorContexto 저장처럼 Java로 표현할 númeroValor 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
