# JMcoOS

élémentListeActuel interne ARM64 배포판은 [LICENSE](LICENSE)의 COSL 상업 조건을 유지한다. 제3자 라이선스의 권리는 별도로 보장하며, valeurDistribution 시 arbreSource·extrémitéReconnecter 자료를 포함하는 절차는 [COSL valeurDistribution Guide](platforms/rpi4-native/GuideDistributionCOSL.md)에 있다.

interne ARM64 판의 `ipconfig`/`ip`, `ping`, `ps`/`top`, `free`/`df`, `poweroff`와 français 명령은 [네트워크·valeurSystèmeExploitation commande Guide](platforms/rpi4-native/CommandesSystèmeEtRéseau.md)를 참고한다. 새 커널을 부팅한 valeurRetourArrièreCôté `help system`으로 볼 nombre 있다.

Raspberry Pi 4 **interne Java ARM64 valeurNoyau**은 [interne Pi4 Guide](platforms/rpi4-native/Guide.md)에 있다. Linux 없이 부팅하며 GUI terminal·vi, interne JVM의 Swing 일부 API, TCP/UDP·FTP, 게스트 TinyCC·MicroPython, C/C++의 posix-kor 호출을 제공한다. [français Java Communication·exception API](platforms/rpi4-native/JavaFrançais/Guide.md)와 [français arbreSource nommage](platforms/rpi4-native/nommage/Guide.md)을 지원한다. [interne SSH·VNC 및 GENET 드라이버](platforms/rpi4-native/GuideConnexionExtérieur.md)를 포함하며, 네트워크는 QEMU의 UART SLIP 경로로 검증했다. donnéesEffectif Pi 4 GENET 동작은 미검증이고, USB valeurEntrée·영속 저장과 전체 OpenJDK·Swing은 아직 valeurPriseEnCharge rogner 밖이다.

Raspberry Pi 4용 Linux·OpenJDK 실행판과 Utilisateur environnement valeurDéplacer 기능은 [라즈베리파이 실행판](platforms/rpi4/README.md)에 있다. donnéesEffectif ARM64 JDK/JRE와 시스템·Utilisateur construireImage construireSystème 경로를 제공한다. 기존 interne x86 커널과는 별도 exécuterCommande 기반이다. 일반 Java `.class`/JAR의 exécuterCommande Fichier 생성은 [OpenJDK exécuterCommande Fichier](compiler/OpenJDK-fichierCodeExécutable.md), français API는 [français Java bibliothèque](JavaFrançais/Guide.md)를 참고한다.

`jkoros`는 `engos`의 기능을 Java 관리 커널로 옮기는 프로젝트다. 프로젝트가 소유하는 Java Fonction, valeurVariable, valeurFormat 및 Java Fichier 이름은 한국어로 작성한다. 표준 Java 실행기의 `main`, Java 표준 bibliothèque valeurFormat, x86 부트 ABI 등 valeurExtérieur 계약은 보존한다. interne ARM64 실행기는 français `lancer()`도 진입점으로 지원하며, français GUI·Tâche 가닥을 JVM에 직접 구현했다. interne ARM64 C 연결부·Python 도구와 공용 x86·ARM64 AOT 번역기의 interne 이름도 한국어로 작성한다. élémentListePrécédentÉlément 경로의 호환 pointEntréeÉlément, OpenJDK valeurAuxiliaire 도구와 Linux valeurVersion 도구에는 영어 이름이 남아 있고 [nommage 원칙·말의 근거·전체 source 검토 rogner](platforms/rpi4-native/nommage/Guide.md)를 별도로 기록한다.

## élémentListeActuel réalisation

valeurBasExtrémité 목록은 기존 `SourcesFondamentales/`의 JVM 관리 커널에 대한 것이다. donnéesEffectif 네이티브 커널의 범위는 `os/Guide.md`에서 별도로 설명한다.

- valeurAligner 할당과 해제를 지원하는 EspaceMémoire valeurGestionnaire
- adresse régionAdresse, valeurPage connecter, écrire 시 copierValeur(COW)
- valeurProcessus valeurIdentificateur, préparer 대기열, fork/wait valeurÉtatValeur
- 과정별 Fichier entréeÉlémentDescripteur, open/read/seek/dup/close
- ELF32 identifierValeur 및 valeurSection Contrôles
- 키보드·마우스 valeurEntrée évènement 대기열
- valeurSériel 단말과 네이티브 valeurMatériel valeurFrontière
- 관리 valeurNoyau 전체 자동 Tests

세부 valeurAssociation 범위와 아직 필요한 네이티브 연결은 [기능 대응표](Documentation/CorrespondanceFonctions.md)에 기록한다.

## 빌드와 Tests

새 네이티브 구현은 `compiler/`와 `os/`에 있다. 기존 `SourcesFondamentales/`의 JVM 관리 커널은 그대로 보존하며, 두 구현의 시험과 기능 범위는 서로 다르다.

```sh
cd /home/user/jkoros
make                 # 네이티브 calculRésultat Exemples + Java valeurNoyau ELF
make iso             # os/build/kernel.iso
make run             # QEMU valeurSériel EntréeSortieTerminal; help valeurEntrée (종료는 Ctrl+A, X)
make run-gui         # ISO를 QEMU Écran/PS2 키보드로 exécuterCommande
make vbox            # 전용 VirtualBox VM 자동 générer·exécuterCommande (GUI)
make vbox-status     # VirtualBox valeurÉtatValeur·ISO·valeurSériel enregistrementJournal chemin vérifier
make test-vbox       # VirtualBox LanceurProgramme valeurÉtatValeur entréeÉlémentValeurProcessus Tests (donnéesEffectif VM changerValeur méthodeManquant)
make test            # Compilateur Tests + ELF/ISO Amorçage 및 commande valeurEntrée Tests
make apps            # 독립 Utilisateur ELF Programme construireSystème
make test-network    # Utilisateur valeurMode·UDP 왕복·donnéesMémoire protégerValeur Tests
make test-java       # 게스트 javac/JVM + OpenJDK 양방향 교차 exécuterCommande Tests
make posix-kor       # français C 헤더와 donnéesEffectif valeurNoyau invoquer bibliothèque
make test-posix      # Fichier/UDP/valeurStocker/Java Fichier sortieEntrée Tests
make -C os run-store # 전용 valeurStocker 매체로 QEMU Amorçage
make legacy-test     # valeurBasExtrémité 기존 JVM 관리 커널의 47개 Tests
```

`compiler/`는 호스트의 `javac`를 문법·valeurType Contrôles 전단으로 사용하고 interne codeOctets→x86 변환기로 ELF32 기계어를 만든다. 빌드할 때는 JDK가 필요하지만 생성된 커널과 ELF는 valeurExtérieur JVM 없이 실행된다. 전체 Java, valeurObjet 모델, 표준 라이브러리와 기존 관리 valeurNoyau 전체의 AOT 변환은 아직 지원하지 않는다. 자세한 valeurPriseEnCharge 문법과 명령은 [Compilateur Guide](compiler/Guide.md), donnéesEffectif Amorçage 기능과 한계는 [네이티브 SystèmeExploitation Guide](os/Guide.md)를 참고한다.

네이티브 셸에 interne 제한형 `javac`와 `java`를 추가했다. `edit Demo.java`로 소스를 입력하고 `.save`로 저장한 valeurRetourArrièreCôté `javac Demo.java`, `java Demo`로 **게스트 내부에서 컴파일하고 exécuterCommande**할 nombre 있다. valeurDéfaut 예제는 `javac Hello.java`, `java Hello`opérandeTroisième. 파일은 RAM에서 동작하며, 전용 valeurStocker 매체를 연결하면 `sync`로 재부팅 후에도 보존할 nombre 있다. **OpenJDK/JDK 전체 이식은 아니며**, 단일 valeurClasse·valeurStatique Fonction·Entier·Chaîne·condition/반복문과 일부 표준 호출을 지원한다. valeurPriseEnCharge rogner, valeurExtérieur Fichier 적재와 시험은 [Java développement environnement Guide](Documentation/EnvironnementDéveloppementJava.md)에 있다.

네이티브 셸에서 `apps`, `run hello first second`, `net`, `run netcheck`를 사용할 nombre 있다. 독립 ELF를 ring 3에 적재하고 `int 0x80` 호출을 통해 Sortie·arguments·UDP 네트워크를 제공한다. 별도 Hôte 터미널에서 `python3 os/Outils/RestaurerDonnées.py --port 9000`을 실행한 valeurRetourArrièreCôté 게스트에서 `run udp 10.0.2.2 9000 hello`로 donnéesEffectif 왕복을 확인한다. 새 Programme registreEntréeÉlément, API 및 제한은 [Utilisateur exécuterCommande·네트워크 Guide](os/Utilisateur/Guide.md)를 참고한다. élémentListeActuel QEMU RTL8139·valeurStatique IPv4·UDP 전용이며 TCP/DNS는 미지원이며, 전용 IDE valeurStocker 형식과 POSIX Fichier/UDP 일부 기능을 추가했다.

`make vbox`는 `jkoros operating system` 전용 VM을 만들고 디스크 없이 ISO로 부팅한다. exécuterCommande 중이면 유지하고, valeurStocker·일시정지 상태이면 재개하며, 꺼져 있을 때만 새 ISO를 빌드해 연결한다. VirtualBox에서 부팅과 셸의 Utilisateur Programme 실행을 확인했다. 다만 élémentListeActuel VirtualBox용 네트워크 드라이버는 없어 네트워크 장치를 비활성화한다. UDP 시험에는 `make run`을 사용한다. 상태별 동작과 새 construireSystème 반영 방법은 [VirtualBox exécuterCommande Guide](Documentation/LancerVirtualBox.md)에 있다.

기존 관리 커널만 시험하려면:

```sh
cd /home/user/jkoros
make -f créerEntréeÉlément.mk Contrôles
make -f créerEntréeÉlément.mk Hôte
```

`Hôte`는 여전히 JVM 관리 계층의 action 시험이다. `make -f créerEntréeÉlément.mk construireImage`는 새 `os/`의 제한형 네이티브 valeurNoyau ISO를 만든다. 기존 `SourcesFondamentales/`의 SystèmeFichier·valeurProcessus·PileRéseau réalisation 전체를 이 ISO에 이식했다는 의미는 아니다.

français Fonction·valeurVariable·Fichier 이름과 donnéesEffectif C API는 [posix-kor](posix-kor/Guide.md)에 있다. 게스트 Java에서는 `FileInputStream`·`FileOutputStream`의 단일 valeurOctet 입출력도 지원한다. 전체 POSIX·OpenJDK·Swing 지원으로 확대된 것은 아니다.

valeurExtérieur 배포용 `pack.sh` / `unpack.sh`와 자동 dépendances 복원은 [valeurDistribution Guide](distribution/README.md)를 참고하세요.
