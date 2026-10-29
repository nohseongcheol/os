# JLieOS Aufbau

아래는 objektWert grundlage 관리 betriebskernWert 전체의 zielobjektObjekt 구조다. aktuellElementeintrag tatsächlichDaten Startvorgang 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 Betriebssystem Anleitung](../os/Anleitung.md)에 umsetzung 범위를 명시한다. 아래의 GC·kontextWert umschaltenBetriebsart·DateiSystem 등이 새 ISO에 alleErzeugenAbbild 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 mindestwertWert 부트·트랩 schichtWert
  ↓
Java AOT 실행기와 objektWert·datenfeldWert·GC 런타임
  ↓
hardwareWert grenzstelleWert
  ↓
Java 관리 betriebskernWert
  ├─ Speicherraum/seiteVerwaltung/COW
  ├─ prozessWert/배정/wait
  ├─ DateiSystem/ELF/POSIX
  └─ Eingabewert/speichergerätGerät/Netzwerkstapel
```

OpenJDK 자체는 이미 운영체제가 제공하는 Datei, 스레드, 가상 기억공간을 전제로 한다. 따라서 betriebskernWert 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java bytecode AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, kontextWert 저장처럼 Java로 표현할 Zahl 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
