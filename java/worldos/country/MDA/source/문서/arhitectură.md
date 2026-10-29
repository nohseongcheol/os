# JMdaOS arhitectură

아래는 obiect_VALUE 기반 관리 nucleu_VALUE 전체의 țintă_obiect 구조다. curent_element real_date 부팅 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 sistem_de_operare 안내](../os/안내.md)에 구현 범위를 명시한다. 아래의 GC·context_VALUE SWITCH_mod·sistem_de_fișiere 등이 새 ISO에 모두 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 최소 부트·트랩 strat_VALUE
  ↓
Java AOT 실행기와 obiect_VALUE·ARRAY_VALUE·GC 런타임
  ↓
하드웨어 경계
  ↓
Java 관리 nucleu_VALUE
  ├─ Memorie_regiune/쪽관리/COW
  ├─ Proces_VALUE/배정/wait
  ├─ sistem_de_fișiere/ELF/POSIX
  └─ 입력/dispozitiv_de_stocare/rețea_Teanc
```

OpenJDK 자체는 이미 운영체제가 제공하는 Fișier, 스레드, 가상 기억공간을 전제로 한다. 따라서 nucleu_VALUE 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java 바이트코드 AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, context_VALUE 저장처럼 Java로 표현할 수 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
