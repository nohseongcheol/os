# JMltOS Architecture

아래는 valeurObjet fondation 관리 valeurNoyau 전체의 objetCible 구조다. élémentListeActuel donnéesEffectif Amorçage 가능한 제한형 구현은 `compiler/`와 `os/`에 있으며 [네이티브 SystèmeExploitation Guide](../os/Guide.md)에 réalisation 범위를 명시한다. 아래의 GC·valeurContexte modeCommuter·SystèmeFichier 등이 새 ISO에 construireTous 포함돼 있지는 않다.

```text
GRUB 또는 UEFI
  ↓
x86 valeurMinimal 부트·트랩 valeurCouche
  ↓
Java AOT 실행기와 valeurObjet·valeurTableau·GC 런타임
  ↓
valeurMatériel valeurFrontière
  ↓
Java 관리 valeurNoyau
  ├─ EspaceMémoire/gestionPage/COW
  ├─ valeurProcessus/배정/wait
  ├─ SystèmeFichier/ELF/POSIX
  └─ valeurEntrée/périphériqueStockage/PileRéseau
```

OpenJDK 자체는 이미 운영체제가 제공하는 Fichier, 스레드, 가상 기억공간을 전제로 한다. 따라서 valeurNoyau 부팅에는 OpenJDK를 그대로 넣지 않고 제한된 Java codeOctets AOT와 작은 런타임을 사용한다.

네이티브 계층에는 `in/out`, `hlt`, CR0/CR2/CR3/CR4, `iret`, valeurContexte 저장처럼 Java로 표현할 nombre 없는 CPU 동작만 남긴다. 정책과 자료구조는 Java에 둔다.
