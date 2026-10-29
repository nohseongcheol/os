# engos 기능 대응표

이 표는 기존 `SourcesFondamentales/`의 valeurObjet fondation JVM 관리 커널을 설명한다. 새 `compiler/`와 `os/`는 별도 제한형 네이티브 구현이며 [donnéesEffectif Amorçage 기능과 limiteFrontière](../os/Guide.md)를 따로 기록한다.

## Java 관리 valeurCouche réalisation estTerminé

| engos valeurRégion | JMarOS réalisation |
|---|---|
| memorymanager, phymem | `GestionnaireMémoire` valeurAligner allouerStockage·libérerStockage·병합 |
| paging, virtmem | `GestionnairePage` adresse régionAdresse·valeurPage connecter·COW·개인 écrire |
| gdt, tss | `TableDescripteurGlobal`, `SegmentÉtatValeurTâche` |
| interrupt | `GestionnaireInterrompre` registreEntréeÉlément·activer·distribuerValeur |
| process, scheduler, thread | `valeurProcessus`, `Ordonnanceur` PID·fork·wait·valeurÉtatValeur modeCommuter |
| systemcall/POSIX 1단계 | lire·écrire·ouvrir·fermer·seek·dup·fcntl·entréeÉlémentAccès·작업목록·Utilisateur/무리 ID·synchroniser·brk·fork·wait·exec·stat·uname 의미 |
| ATA | `PièceJointeTechnologieAvancé` 512바이트 valeurSection lire·écrire |
| MSDOS partition | `tablePartitionPrimaire` MBR 검증과 네 valeurEntréeÉlément analyserValeur |
| FAT 공개 Fichier valeurCouche | `SystèmeFichier`, `tableDescripteurFichier` lire 전용 파일과 과정별 FD |
| ELF | ELF32 Contrôles, valeurSection rogner Contrôles, 적재, NOBITS opérandeZéro initialiser, lancer adresse·argumentParamètre·environnement 반영 |
| keyboard, mouse | `GestionnaireEntrée`의 손실 계수 Entêtes évènement 대기열 |
| timer | `Horloge` 틱과 valeurTemps convertirValeur |
| PCI | `GestionnaireBusPériphériqueMatériel` 검색 결과와 Périphérique valeurSélection |
| VGA/text mode | `présenterCaractère` 80x25 출력과 스크롤 |
| Ethernet/ARP/IPv4/ICMP/UDP/TCP | `OutilsRéseau`, `CoucheRéseau` indiceCadre Contrôles·sommeContrôle·valeurContrat/portMatériel distribuerValeur |

## 기존 valeurObjet fondation 관리 valeurNoyau 전체를 부팅하기 위해 남은 connecter

élémentListeSuivant 항목은 Java 문법만으로 실행할 nombre 없는 CPU/Périphérique 동작이므로 관리 계층과 별도로 AOT 런타임에 연결해야 한다.

- Multiboot valeurPointEntréeÉlément, CR0/CR2/CR3/CR4, IDT 적재, `iret`, x86 valeurContexte valeurStocker
- donnéesEffectif PIC/PIT/PS2/ATA/PCI portMatériel 및 AMD PCnet DMA valeurBoucle
- Java valeurObjet·valeurTableau DispositionLiens, exception, valeurStatique initialiser, 가비지 수집기
- 컴파일된 Java 메서드를 freestanding i386 기계어로 바꾸는 AOT valeurÉtapePhase
- FAT 디스크 구역을 donnéesEffectif ATA 장치와 연결하는 sortieEntrée 접착 valeurCouche

valeurSommet 관리 계층은 engos 기능의 Java 관리 구현과 Hôte 검증판이다. 별도 `os/`에서는 제한형 AOT, Multiboot valeurPointEntréeÉlément, valeurStatique initialiser·Entier valeurTableau, VGA/valeurSériel/PS2, InterpréteurCommandes, Utilisateur ELF/ring 3/시스템 invoquer, RTL8139/ARP/IPv4/UDP를 연결해 QEMU 부팅과 Hôte 루프백 패킷 왕복을 검증했다. valeurSommet 표의 valeurObjet fondation 관리 기능 전체나 VirtualBox 네트워크 실행까지 검증했다는 뜻은 아니다.
