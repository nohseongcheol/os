# JSweOS arkitektur

아래는 objekt_värde 기반 관리 kärna_värde 전체의 mål_objekt 구조다. aktuellt_objekt verklig_data maskinstart 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 operativsystem VIKTIGT_eb81d7d9](../os/VIKTIGT_eb81d7d9.md)에 implementation 범위를 명시한다. 아래의 GC·sammanhang_värde byta_läge·filsystem 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 nivå_värde
  ↓
Java AOT 실행기와 objekt_värde·MATRIS_värde·GC 런타임
  ↓
maskinvara_värde gräns_värde
  ↓
Java 관리 kärna_värde
  ├─ Minne_område/쪽관리/COW
  ├─ Process_värde/배정/wait
  ├─ filsystem/ELF/POSIX
  └─ indata_värde/lagringsenhet/nätverk_Stack
```

OpenJDK 자체는 이미 운영체제가 제공하는 filnamn, 스레드, 가상 기억공간을 전제로 한다. 따라서 kärna_värde 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, sammanhang_värde 저장처럼 Java로 표현할 nummer 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
