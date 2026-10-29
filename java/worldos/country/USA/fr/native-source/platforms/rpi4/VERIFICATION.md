# valeurDistribution construireImage valider enregistrementJournal

검증일: 2026-09-27 (Asia/Seoul)

valeurCible: `jkoros-rpi4-aarch64-349b52891a471c8e782da597`

이번 배포는 Raspberry Pi 4용 **ARM64 Linux 실행판**이다. 기존 interne x86 커널을 ARM으로 이식한 결과가 아니다. donnéesEffectif Pi 보드는 연결되어 있지 않아 valeurMatériel Amorçage 성공을 확인하지 못했다.

## 배포물

| Fichier | taille(valeurOctet) | description |
|---|---:|---|
| `dist/jkoros-rpi4-system.img.gz` | 1,218,093,871 | valeurArchive 시스템 construireImage; libérerStockage étatValeurAprès 1,475,747,840 valeurOctet |
| `dist/jkoros-user.img.gz` | 18,761,147 | 빈 Utilisateur Données construireImage; libérerStockage étatValeurAprès 4 GiB |
| `dist/openjdk25-jdk-linux-aarch64-musl.tar.gz` | 177,359,476 | 미리 컴파일된 ARM64 JDK |
| `dist/openjdk25-jre-linux-aarch64-musl.tar.gz` | 48,361,058 | ARM64 JRE |
| `dist/JavaFrançais.jar` | 10,563 | français valeurAuxiliaire API와 Java EspaceTravail |

해시는 [SHA256SUMS](dist/SHA256SUMS)에 기록했다. 두 valeurArchive construireImage construireTous 끝까지 해제하여 original 이미지의 SHA256과 일치함을 확인했다. [valeurArchive valider enregistrementJournal](build/verification/compression.json)

ARM64 게스트에서 직접 확인한 버전은 OpenJDK/Javac 25.0.4, Python 3.14.7, GCC 15.2.0이다. Pi 커널은 6.18.52-0-rpi, QEMU valider 커널은 6.18.53-0-virt다. 서명 검증한 Alpine 패키지 501개로 구성했으며, [패키지 listeEntréeÉlément](dist/packages.lock.json)과 [original valeurOrigine](dist/sources.lock.json)를 제공한다.

## 통과한 Contrôles

| Contrôles | donnéesEffectif vérifier valeurContenuValeur | enregistrementJournal |
|---|---|---|
| Hôte Compilateur Tests 19개 | 기존 AOT 회귀 Tests, `.class` 직접 valeurEntrée, OpenJDK ELF LanceurProgramme, JAR dépendances, 상속·리플렉션·람다·스레드·리소스, chemin valeurDéplacer, valeurÉchec 시 기존 Sortie 보존 | [compiler-tests.log](build/compiler-tests.log) |
| Pi construireImage Architecture | MBR valeurFrontière, FAT Amorçage 파티션, Pi 펌웨어, ARM64 valeurNoyau, Pi 4 DTB, initramfs, SquashFS 및 fichierHachage | [image.json](build/verification/image.json) |
| ARM64 JDK/JRE | 아카이브 해시와 ELF 아키텍처 Contrôles, Amorçage étatValeurAprès 두 런타임의 donnéesEffectif exécuterCommande | [런타임 enregistrementJournal](dist/java-runtimes.json), [seed.log](build/verification/seed.log) |
| élémentListePremier Amorçage | lire 전용 시스템, Java Fichier·valeurUnicode·exception·valeurObjet·스레드·HTTP/TCP·valeurEnfant 프로세스, Swing, CJK·아랍어·데바나가리 valeurPolice, Python Fichier·스레드·valeurPriseRéseau·가상환경·pip, GCC pthread | [seed.log](build/verification/seed.log) |
| ARM64 exécuterCommande Fichier générer | 게스트의 javac/GCC로 Java 프로그램을 ELF 실행기로 묶고 JRE를 동봉; 유효한 JAVA_HOME 없이 exécuterCommande valeurSuccès | [seed.log](build/verification/seed.log) |
| 재부팅 복원 | Utilisateur Données, `/etc` réglages, `/usr/local/bin` Programme, APK로 설치한 tree, pip 패키지, Fichier 삭제 informationSystème, 소유권, sudo, Java exécuterCommande Fichier retenirValeur | [restore.log](build/verification/restore.log) |
| estHorsLigne 홈 valeurDéplacer | 기존 환경을 사용하지 않는 유지보수 부팅에서 `/user` 전체를 새 ext4 이미지에 `cp -a`로 copierValeur | [migrate.log](build/verification/migrate.log) |
| valeurDéplacer étatValeurAprès Amorçage | 새 Données 이미지로 부팅하여 재부팅 복원 항목을 valeurRéessayer vérifier | [migrated-restore.log](build/verification/migrated-restore.log) |
| estNormal programmeQuitter 및 Données 무결성 | 일반 Amorçage 3회 construireTous OverlayFS/Données Périphérique lire 전용 modeCommuter valeurSuccès; original·valeurCopié ext4의 `e2fsck -fn` programmeQuitter valeurCode 0 | [original Contrôles](build/verification/fsck-original.log), [valeurCopié Contrôles](build/verification/fsck-migrated.log) |

네 valeurSéquence 부팅은 construireTous QEMU `virt`, ARM64 Cortex-A72 TCG, RAM 2 GiB, vCPU 2개 환경에서 programmeQuitter valeurCode 0으로 통과했다. [전체 Amorçage 결과와 valeurJournal fichierHachage](build/verification/boot.json)

QEMU 가상 NIC의 DHCP adresse 취득도 확인했다. HTTP/TCP 시험은 루프백 통신이며 valeurExtérieur 인터넷이나 Pi Wi-Fi의 valider 결과로 해석하면 안 된다. Swing은 Xvfb에서 실행했고, [Écran 캡처](build/verification/swing.png)에서 texteHangul·일본어·아랍어·힌디어 문자열이 표시되는 것을 확인했다.

## réalisation 범위와 남은 valider

### QEMU 그래픽 exécuterCommande 보완

terminal 전용 실행에서 `Salutation.java`opérandePremier Swing 창을 만들 때 발생한 `HeadlessException`을 해결하기 위해 `make run`과 `make run-console`을 추가했다. 그래픽 실행은 bochs 가상 GPU, USB 키보드·태블릿, Xorg, 로컬 VNC를 사용한다. QEMU 전용 initramfs가 필요한 드라이버를 기존 루트 파일시스템에서 로딩한다. valeurDistribution 시스템 이미지와 base-id는 변경하지 않아 기존 Utilisateur Données 이미지를 traitementContinuer 사용할 nombre 있다.

donnéesEffectif Xorg/VNC 화면에서 français Java EspaceTravail, Swing Tests fenêtre, 기존 이미지의 `Salutation.java` 창을 표시했다. VNC를 통한 USB 마우스 클릭과 키보드 입력이 Swing 이벤트로 전달되는 것도 확인했다. programmeQuitter 시 시스템 OverlayFS와 Données 파일시스템의 lire 전용 전환을 확인했다. 이번 시험은 Xvfb를 사용하지 않는다.

- [그래픽 Tests résultat](build/verification/desktop.json)
- [그래픽 Tests valeurJournal](build/verification/desktop.log)
- [키보드·마우스 Tests Écran](build/verification/desktop-input.png)
- [Salutation Exemples Écran](build/verification/desktop-greeting.png)
- [수정한 Exemples 원문의 Écran 없는 exécuterCommande résultat](build/verification/headless-example.log)

source 예제에는 `GraphicsEnvironment.isHeadless()` 분기를 추가했다. 화면이 없는 환경에서는 Fichier·Caractères·스레드 기능을 실행하고 안내를 출력한다. Utilisateur 홈의 기존 원문을 자동 교체하지는 않는다. 향후 construireImage 빌드에는 udev의 `add` 이벤트를 명시적으로 발생시키는 수정도 반영된다.

### texteHangul valeurEntrée·valeurPolice 보완

`make test-korean`으로 donnéesEffectif Xorg/VNC 화면의 Swing 입력창과 xterm에서 Ctrl+Space modeCommuter 및 두벌식 valeurTouche 입력을 시험했다. 양쪽에서 `texteHangul valeurEntrée`을 조합했고 UTF-8 파일의 내용과 일치했다. 시험은 별도 Utilisateur Données 이미지에서 실행했으며 estNormal programmeQuitter 시 두 파일시스템의 lire 전용 전환을 확인했다.

terminal valeurPolice 진단에서 영문 DejaVu Sans Mono와 texteHangul Noto Sans Mono CJK KR의 donnéesEffectif Fichier 로딩을 확인했다. 한글용으로 요청한 글꼴이 영문 전용 글꼴로 대체되던 Fontconfig 규칙의 우선순위도 수정했다. Écran 캡처에서 texteHangul·영문 afficherValeur, Java 작업마당의 확대된 글꼴과 안티앨리어싱을 확인했다.

수정은 QEMU 전용 initramfs를 통해 Utilisateur 시스템 변경분에 적용하며 valeurDistribution valeurDéfaut 이미지와 base-id는 유지한다. 기존 Fichier 백업, 동일 수정의 valeurItération 적용 방지, 손상된 modifierValeur Fichier 및 다른 base-id rejeterValeur, Utilisateur 입력기 réglages 병합에 대한 Hôte Tests 4개도 통과했다. 원래 Utilisateur Données construireImage `build/manual-user.img`는 시험에 사용하지 않았다.

- [texteHangul valeurEntrée·valeurPolice Tests résultat](build/verification/korean.json)
- [valeurEntrée·donnéesEffectif valeurPolice 로딩 valeurJournal](build/verification/korean.log)
- [Swing·terminal texteHangul Écran](build/verification/korean-desktop.png)
- [Java EspaceTravail valeurPolice Écran](build/verification/korean-workbench.png)
- [réglages 보존 Tests](build/verification/desktop-update-tests.log)

### 남은 rogner

- 새 compilerSource valeurCible `openjdk`는 **네이티브 LanceurProgramme + JVM/JRE** 방식이다. 모든 Java 바이트코드를 JVM 없이 기계어로 변환하는 범용 AOT 컴파일러는 구현하지 않았다. 기존 x86 AOT의 valeurPriseEnCharge 범위는 여전히 제한적이다.
- exécuterCommande 프로그램에는 main pointEntréeÉlément, 호환 valeurClasse 버전과 의존 JAR/JNI가 필요하다. 개별 상용 Programme, 모든 Java valeurModule, 모든 문자권을 시험한 것은 아니다.
- français Java 라이브러리는 Fichier·Caractères·Communication·스레드·Swing을 위한 valeurAuxiliaire API이며 JDK 전체 API의 français 번역판은 아니다.
- Pi 4 전용 펌웨어·valeurNoyau·Périphérique 트리는 이미지에 들어 있지만 donnéesEffectif SD Amorçage, HDMI/KMS, USB, Wi-Fi, 물리 키보드의 texteHangul 입력은 실기 확인이 남아 있다. QEMU는 Pi 장치를 에뮬레이션하는 시험이 아니다.
- Utilisateur valeurRépertoire 이동은 동일 시스템 construireImage valeurIdentificateur, ARM64, `/home/user`, UID 1000을 전제로 한다. programmeQuitter étatValeurAprès 소유권·valeurPermission·링크·valeurExtension valeurAttribut·삭제 정보를 보존하여 복사해야 한다. 다른 OS 버전으로의 자동 이관은 제공하지 않는다.

installerValeur·copierValeur 절차는 [README.md](README.md), compilerSource 방식은 [OpenJDK exécuterCommande Fichier Guide](../../compiler/OpenJDK-fichierCodeExécutable.md)를 따른다. construireImage 파일만 생성했으며 donnéesEffectif SD 카드나 USB 디스크에 기록하지 않았다.
