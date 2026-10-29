# JIsrOS architektúra

아래는 objektum_ÉRTÉK 기반 관리 kernel_ÉRTÉK 전체의 cél_objektum 구조다. aktuális_cikk tényleges_adat 부팅 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 operációs_rendszer fontos_fájl_eb81d7d9](../os/fontos_fájl_eb81d7d9.md)에 구현 범위를 명시한다. 아래의 GC·környezet_ÉRTÉK vált_mód·fájlrendszer 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 réteg_ÉRTÉK
  ↓
Java AOT 실행기와 objektum_ÉRTÉK·TÖMB_ÉRTÉK·GC 런타임
  ↓
hardver_ÉRTÉK határ_ÉRTÉK
  ↓
Java 관리 kernel_ÉRTÉK
  ├─ Memória_régió/쪽관리/COW
  ├─ folyamat_ÉRTÉK/배정/wait
  ├─ fájlrendszer/ELF/POSIX
  └─ bevitel_ÉRTÉK/tárolóeszköz/hálózat_Sor
```

OpenJDK 자체는 이미 운영체제가 제공하는 Fájl, 스레드, 가상 기억공간을 전제로 한다. 따라서 kernel_ÉRTÉK 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, környezet_ÉRTÉK 저장처럼 Java로 표현할 szám 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
