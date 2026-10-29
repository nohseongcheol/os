# JUkrOS architektura

아래는 obiekt_WARTOŚĆ 기반 관리 jądro_WARTOŚĆ 전체의 cel_obiekt 구조다. bieżący_towar rzeczywisty_dane rozruch_maszyny 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 system_operacyjny plik_README_eb81d7d9](../os/plik_README_eb81d7d9.md)에 implementacja 범위를 명시한다. 아래의 GC·kontekst_WARTOŚĆ zmiana_tryb·system_plików 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 warstwa_WARTOŚĆ
  ↓
Java AOT 실행기와 obiekt_WARTOŚĆ·TABLICA_WARTOŚĆ·GC 런타임
  ↓
sprzęt_WARTOŚĆ granica_WARTOŚĆ
  ↓
Java 관리 jądro_WARTOŚĆ
  ├─ Pamięć_region/쪽관리/COW
  ├─ Proces_WARTOŚĆ/배정/wait
  ├─ system_plików/ELF/POSIX
  └─ wejście_WARTOŚĆ/urządzenie_magazynujące/sieć_Stos
```

OpenJDK 자체는 이미 운영체제가 제공하는 nazwa_pliku, 스레드, 가상 기억공간을 전제로 한다. 따라서 jądro_WARTOŚĆ 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, kontekst_WARTOŚĆ 저장처럼 Java로 표현할 identyfikator 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
