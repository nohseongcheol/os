# Java 네이티브 SystèmeExploitation

이 문서는 기존 **x86 valeurNoyau**을 설명한다. Raspberry Pi 4의 interne ARM64 étatValeurInitialValeur 이식은 [별도 Guide](../platforms/rpi4-native/README.md)를 참고한다. valeurBasExtrémité x86 Utilisateur ELF·네트워크·IDE valeurStocker 기능이 ARM64에 construireTous 이식된 상태는 아니다.

Java 원문을 interne AOT 후단으로 x86 기계어로 컴파일해 부팅하는 작은 운영체제다. 커널과 별도로 interne 제한형 Java Compilateur·JVM ELF를 Utilisateur 모드에 적재할 nombre 있다. Linux, engos, koros4와 valeurExtérieur OpenJDK는 게스트에 적재하지 않는다. Amorçage 진입과 portMatériel/물리 EspaceMémoire 접근은 어셈블리이며, Caractères EntréeSortieTerminal·valeurEntrée entréeÉlémentValeurProcessus·commande analyserValeur·Tâche valeurSection 관리는 `source/*.java`에 있다.

## 게스트 Java développement

`javac Hello.java`, `java Hello`로 부팅된 SystèmeExploitation 안에서 compilerSource·실행한다. `edit FILE.java`와 `.save`로 소스를 작성하며 `ls`, `cat`, `rm`을 제공한다. RAM 파일은 valeurMaximal 8개, 각각 16KiB이다. 전용 IDE 매체를 연결하면 `sync`로 보존할 nombre 있다. 이 기능은 interne 제한형 구현이며 전체 OpenJDK/JDK 호환은 아니다. 사용법·valeurPriseEnCharge 문법·Fichier 적재·교차 시험은 [Java développement environnement](../Documentation/EnvironnementDéveloppementJava.md)에 있다. `make test-java`로 검증한다.

## 빌드와 exécuterCommande

`compiler/`opérandePremier 요구하는 도구에 더해 ISO 생성에는 `grub-file`, `grub-mkrescue`, GRUB BIOS valeurModule, `xorriso`opérandePremier 필요하다. 실행에는 QEMU 또는 VirtualBox가 필요하다. élémentListeActuel 설치된 도구만 사용한다. `make run-store`는 새 전용 가상 valeurStocker 매체를 만들어 연결한다. VirtualBox 실행기는 이 프로젝트가 만든 전용 VM만 설정하고 다른 VM은 변경하지 않는다. 가상 메모리는 valeurDéfaut 64MiB이며 valeurMinimal 16MiB가 필요하다.

```sh
cd /home/user/jkoros/os
make                 # build/kernel.elf
make iso             # build/kernel.iso (Utilisateur ELF valeurGroupe Entêtes)
make run             # ELF 직접 Amorçage, valeurSériel EntréeSortieTerminal
make run-gui         # GRUB ISO Amorçage, VGA 창과 PS/2 자판
make vbox            # 상위 폴더의 실행기로 전용 VirtualBox VM exécuterCommande
make vbox-status     # 전용 VirtualBox VM valeurÉtatValeur vérifier
make test            # ELF와 ISO 두 경로의 donnéesEffectif Amorçage/valeurEntrée Tests
make apps            # Utilisateur 프로그램만 construireSystème
make test-network    # Utilisateur exécuterCommande/UDP/protégerValeur Tests
```

`make run`은 QEMU의 valeurSériel 표준 입출력을 쓴다. `Ctrl+A`를 누른 valeurRetourArrièreCôté `X`로 QEMU를 종료할 nombre 있다. `halt`는 게스트 CPU만 정지시키므로 QEMU fenêtre/프로세스는 별도로 닫는다. 폴링 방식이라 attendreValeur 중에도 Hôte CPU를 사용할 nombre 있다.

VirtualBox는 `make vbox`로 실행한다. 새 전용 VM을 donnéesMémoire 64MiB, BIOS, 광학 드라이브 부팅으로 자동 설정하며 디스크는 valeurNécessaire 없다. donnéesEffectif VirtualBox 5.2.42에서 Amorçage, Java interne Tests, interpréteurCommandes valeurEntrée, `run hello vbox`의 ring 3 실행과 estNormal 종료를 확인했다. élémentListeActuel Communication 드라이버는 QEMU의 RTL8139 전용이며 VirtualBox의 PCnet/E1000에서는 네트워크를 사용할 nombre 없어 네트워크 장치를 비활성화한다. valeurStocker valeurÉtatValeur 재개와 새 construireSystème 반영 방법은 [VirtualBox exécuterCommande Guide](../Documentation/LancerVirtualBox.md)에 있다.

## 셸에서 Utilisateur Programme exécuterCommande 및 네트워크 invoquer

독립 ELF32 exécuterCommande 파일을 적재해 **ring 3**에서 실행한다. `int 0x80` 시스템 호출을 통해 EntréeSortieTerminal Sortie, arguments valeurInterroger, UDP ouvrir·envoyer·recevoir·닫기를 제공한다. Utilisateur 코드를 valeurNoyau 함수로 직접 호출하는 구조가 아니다.

```text
jkoros> apps
jkoros> run hello first second
jkoros> net
jkoros> run netcheck
jkoros> run udp 10.0.2.2 9000 hello
```

élémentListeDernier 명령의 응답을 받으려면 호스트의 별도 터미널에서 `python3 /home/user/jkoros/os/Outils/RestaurerDonnées.py --port 9000`을 먼저 실행한다. 상세 API, Programme ajouterFinEntréeÉlément, adresse 공간과 제한은 [Utilisateur exécuterCommande·네트워크 Guide](Utilisateur/Guide.md)에 있다.

Amorçage vérifier valeurExpressionPhrase:

```text
JKOROS NATIVE JAVA
Java 기계어 valeurNoyau lancer
JAVA SELFTEST PASS
USER ELF: ring 3 / paging / int 0x80
help | info | mem | alloc | free N | echo TEXT | clear | test | halt
apps | run NAME [ARGS] | net
READY
jkoros>
```

## 구현한 기능

- GRUB Multiboot 1 ELF Amorçage, x86 protégerValeur valeurMode GDT, BSS initialiser, 64KiB pileOpérande.
- Java Fonction donnéesEffectif 실행과 Amorçage informationSystème valeurMarqueur vérifier.
- COM1 valeurSériel sortieEntrée, VGA Caractères Écran·valeurCurseur·스크롤·effacerEntréeÉlément.
- PS/2 valeurDéfaut 자판, 좌우 Shift, Enter, Backspace. valeurExtension valeurTouche/마우스 자료는 commande 입력으로 쓰지 않는다.
- longueur 128의 commande valeurEntrée 버퍼, valeurDébordement 방지, CR/LF entréeÉlémentValeurProcessus.
- `help`, `info`, `mem`, `alloc`, `free N`, `echo TEXT`, `clear`, `test`, `halt`.
- 4KiB Tâche valeurSection 8개의 allouerStockage·résultatRetourner·재사용과 중복 résultatRetourner 방지.
- Java valeurTableau 256KiB 영역의 taille·valeurIndiceTableau 검사와 런타임 erreur 중단.
- lire 전용 JKAP exécuterCommande valeurGroupe, ELF32 valeurSection/pointEntréeÉlément valider, Utilisateur valeurMode·arguments·programmeQuitter valeurCode.
- valeurNoyau/Utilisateur 페이지 valeurPermission 분리, TSS, IDT, PIT 100Hz, Utilisateur CPU exception entréeÉlémentValeurProcessus 및 exécuterCommande valeurTemps 상한.
- PCI RTL8139 폴링 드라이버, ARP, valeurStatique IPv4, UDP sommeContrôle·송수신·attendreValeur valeurLimite.

`mem`의 Upper memory는 Multiboot의 1MiB côtéSupérieur casListeCommuterDense donnéesMémoire taille(KiB)이며, 전체 donnéesMémoire 지도 분석이나 자유 물리 donnéesMémoire 수치가 아니다. `alloc`은 이미 확보한 Entier valeurTableau 안의 Tâche valeurSection 번호를 반환한다. 일반 물리 valeurPage allouerStockage, adresse régionAdresse 또는 Utilisateur valeurProcessus donnéesMémoire 관리가 아니다.

## 명시적인 limiteFrontière

이 커널은 **Utilisateur 프로그램을 한 번에 valeurUn 실행하는 étatValeurInitialValeur valeurNoyau**이다. PIT IRQ0만 사용하며 키보드와 NIC는 폴링한다. Utilisateur CPU 예외는 해당 프로그램을 끝내고 셸로 복귀시키지만 valeurNoyau 예외는 중단한다. exécuterCommande 시간은 약 3초로 제한한다. 완전한 선점 다중 valeurProcessus 스케줄러, FAT/ext 등 일반 디스크 SystèmeFichier, TCP·DNS·DHCP·IPv6·HTTP, 전체 POSIX, 일반 valeurObjet 모델/GC는 아직 없다. 전용 IDE Fichier 보존과 POSIX Fichier/UDP 일부 기능은 구현했다. JVM은 RAM 파일의 단일 클래스를 exécuterCommande 시 적재하며 일반 ClassLoader나 JAR 로딩은 지원하지 않는다. 네이티브 exécuterCommande 파일은 construireSystème 시 lire 전용 묶음에 넣으며, 일반 Linux ELF를 실행하는 환경이 아니다. 기존 `../SourcesFondamentales/`의 JVM 관리 valeurNoyau 전체를 이식한 것도 아니다.

Java 식별자는 한국어다. valeurSériel 출력은 이 프로젝트의 texteHangul(BMP Caractères)을 UTF-8로 표시한다. VGA는 valeurDéfaut ASCII 글꼴만 사용하므로 texteHangul 자리에 `?`opérandePremier 나온다. commande 입력도 élémentListeActuel ASCII만 지원하며 texteHangul valeurPolice·입력기 및 valeurAuxiliaire 평면 Caractères 출력은 후속 작업이다. `test`는 작은 배열을 새로 할당하고 GC가 없으므로 무한 반복하지 않는다.

## 자동 Tests

`Tests/TestAmorçage.py`는 디스크 없는 독립 QEMU를 생성해 다음을 검증하고 종료한다.

- ELF 직접 Amorçage 및 GRUB ISO Amorçage.
- Java interne 시험과 UTF-8 valeurSériel valeurExpressionPhrase.
- commande afficherAide·informationSystème·donnéesMémoire·Sortie·erreur valeurEntrée·Écran effacerEntréeÉlément.
- Tâche valeurSection 8개 allouerStockage, 부족 entréeÉlémentValeurProcessus, résultatRetourner/중복 résultatRetourner/재할당.
- valeurSériel nouvelleLigne·백스페이스·긴 valeurEntrée entréeÉlémentValeurProcessus.
- QEMU PS/2 valeurTouche 입력으로 `info` exécuterCommande, `halt` exécutionArrêterMachine.

valeurSuccès 로그는 `build/TestAmorçage.json`에 남는다. 로컬 Unix 소켓을 금지하는 샌드박스에서는 Tests 도구에 해당 권한이 필요하다. Tests 도중 새로 만든 QEMU만 종료하며 기존 VM과 donnéesEffectif 디스크는 건드리지 않는다.

`Tests/testRéseauUtilisateur.py`는 ELF/ISO 각각에서 Utilisateur ELF, donnéesEffectif ring 3, arguments, Hôte 루프백 UDP 왕복, 1,023/1,024바이트 24회 casListeCommuterDense 왕복, valeurTemps 초과, NIC méthodeManquant, donnéesMémoire/portMatériel entréeÉlémentAccès 차단, CPU exception, 무한 valeurItération, 잘못된 ELF를 시험한다. `build/testRéseauUtilisateur.json`에 게스트 기록과 호스트가 받은 데이터의 longueur·해시를 저장한다. `Tests/TestPaquet.py`는 donnéesEffectif Java valeurContrat 처리기에 손상된 패킷을 넣어 2,201개 valeurFrontière/sommeContrôle 조건을 검사한다. Hôte 루프백 외 valeurExtérieur 서버에는 Tests 트래픽을 보내지 않는다.

부트 경계는 GNU의 [Multiboot spécification](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html)를 따른다.

새 descripteurFichier·C ABI·IDE valeurStocker·Java Fichier 흐름의 범위와 français nommage 대응은 [posix-kor Guide](../posix-kor/Guide.md)에 있다. `make test-posix`로 ELF/ISO 실행과 재부팅 보존을 검증한다.
