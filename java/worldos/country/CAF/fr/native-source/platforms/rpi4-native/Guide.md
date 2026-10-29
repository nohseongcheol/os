# Raspberry Pi 4 interne Java valeurNoyau — Utilisateur exécuterCommande fondation

élémentListeActuel interne 코드의 COSL 상업 condition, 제3자 고지 및 LGPL extrémitéReconnecter 자료는 [COSL valeurDistribution Guide](GuideDistributionCOSL.md)를 참고한다. modeCommuter valeurAvant GPL 구성의 판단은 [élémentListePrécédentÉlément 라이선스 검토](RévisionExamenLicence.md)에 기록했다.

français Communication·exception 사용법은 [français Java API](JavaFrançais/Guide.md), Fonction·valeurVariable·Fichier 이름의 변경과 어원 근거는 [nommage Guide](nommage/Guide.md)를 참고한다.

Linux 없이 부팅하는 interne AArch64 커널이다. Java AOT valeurNoyau 위에 **ligneCommande interpréteurCommandes, 게스트 Java Compilateur·JVM, MicroPython, EL0 C++ exécuterCommande, Fichier·UDP 루프백 시스템 invoquer, 여러 texteHangul GUI terminal·vi Éditeur·Swing 부분집합**을 제공한다. 커널의 Fichier Données/정책·루프백 valeurTransfert·interpréteurCommandes 상태는 Java, Écran 합성·pixel changerValeur·pointeur·클리핑도 Java로 구현하며, CPU/MMU/Périphérique 경계와 terminal·valeurCaractère écranPeindre 연결은 C와 어셈블리다.

**전체 JDK/JRE·CPython·표준 C++ 런타임·Swing 이식은 아직 완료되지 않았다.** 기존 [ARM64 Linux 실행판](../rpi4/README.md)의 OpenJDK/Python 패키지를 이 interne 커널에 탑재했다고 표시하지 않는다.

새로운 게스트 `cc`/`jaot`, JAR 직접 exécuterCommande, lwIP TCP/UDP와 FTP는 [FTP·C·JAR·AOT 매뉴얼](CompilationEtTransfertFichier.md)을 참고한다. 게스트 SSH·VNC와 Pi4 GENET/PHY·DHCP 드라이버를 추가했다. **SSH·VNC는 QEMU에서 검증하며, matérielPhysique Pi4의 valeurCâblé 송수신은 아직 미검증이다.** exécuterCommande·connexion·valeurMotPasse 확인은 [valeurExtérieur connexion Guide](GuideConnexionExtérieur.md)에 정리했다.

셸은 EL1 valeurNoyau, `java` 등 Utilisateur exécuterCommande 파일은 EL0에서 실행한다.
`ps`·`top`의 표시와 valeurLimite, QEMU 네트워크 exécuterCommande·connexion 방법 및 donnéesEffectif 검증은
[exécuterCommande 계층과 valeurExtérieur Communication inspecterÉtatValeur](ContrôlesRéseauExtérieurEtEnvironnementExécution.md)을 참고한다.

ELF는 확장자가 아닌 donnéesEffectif exécuterCommande 형식으로 검사한다. `./Salutation`처럼 확장자 없이 실행하며, 제한된 Linux ARM64 valeurStatique ELF는 `run --linux texteNomFichier`으로 실행한다. [ELF·Linux ABI valeurPriseEnCharge 범위와 동일 바이너리 Tests](aBICodeExécutable.md).

GUI와 네트워크는 `python3 Outils/exécuterCommande.py --desktop --network`로 함께 사용한다. Java·C·Python의 français Exemples 13개는 [jkoros/example](../../example/README.md)에 있으며, **게스트 Amorçage 시 `/example/java`, `/example/c`, `/example/python`에 자동으로 준비된다.** `example java|c|python`으로 지운 예제를 복원할 nombre 있다. Remmina에서 **F9/Shift+Space/한·opérandeZéro valeurTouche**로 `[EN]`↔`[KO]` 두벌식을 전환한다(`help ko`). `make test-examples`는 같은 GUI VM에서 FTP·donnéesEffectif TCP/UDP·Fichier valeurOctet·그래픽 픽셀을 검증한다.

게스트에서 `cd /example/java` étatValeurAprès `java ExempleFenêtre`로 français Swing 예제를 실행한다. terminal 모서리에 마우스를 대고 **côtéGauche 버튼으로 끌면 크기가 바뀐다**. `terminal size`는 élémentListeActuel valeurColonne·valeurRangée 수를 보여 준다.

## élémentListeActuel valeurPriseEnCharge rogner

| 기능 | réalisation·시험한 rogner | 아직 estNonPrisEnCharge |
|---|---|---|
| Amorçage | Pi4 AArch64 EL1, UART, SD용 construireImage, QEMU raspi4b Amorçage | donnéesEffectif Pi4 보드에서의 펌웨어 Amorçage Tests |
| Java valeurNoyau | valeurStatique Java 부분집합 → freestanding C → AArch64 AOT | 전체 Java valeurObjet/exception/GC/JVM/표준 bibliothèque |
| Java développement Outils | 게스트 interne `javac`/`java`, JVM 0.4/JAR: 다중 valeurClasse·valeurObjet·상속·exception·GC·일부 컬렉션·Thread·IPv4 Socket/UDP·Swing 일부 API, français bibliothèque. 게스트 컴파일러는 valeurStatique Java 부분집합 | 전체 JDK/JRE·HotSpot·Java SE·임의의 모든 JAR·AWT/Swing 전체 |
| Python | donnéesEffectif MicroPython 1.24.1 EL0 Portage, arbreSource compilerSource/exécuterCommande, valeurClasse·exception·GC·큰 Entier·Unicode·Fichier·UDP/Écran connecter | CPython, pip, C valeurExtension, 부동소수점, 일반 OS/스레드/valeurPriseRéseau valeurModule, interactif REPL |
| interpréteurCommandes | UTF-8 valeurÉditer·enregistrementJournal·valeurAchevé, 디렉터리·Fichier commande, valeurVariable·condition·valeurScript, 16 KiB 순차 파이프·리다이렉션, ELF exécuterCommande | 전체 POSIX sh/Bash, Tâche valeurContrôle·동시 프로세스·PTY |
| C/AOT compilerSource | 게스트 TinyCC 및 valeurStatique Java 부분집합 `jaot` → interne ARM64 ELF | 전체 libc·모든 Java valeurClasse AOT |
| C++ | 독립 ELF64를 EL0에서 exécuterCommande; valeurStatique 생성자, RAII 소멸자, FP/SIMD, français Fichier/루프백 invoquer | libc/libstdc++, STL, C++ exception·RTTI·동적 connecter |
| Utilisateur protégerValeur | 4 KiB 페이지, valeurCode RX/Données RW·NX, valeurNoyau·MMIO 차단, guard page, 잘못된 pointeur Contrôles | 다중 Utilisateur valeurPermission, 일반 프로세스/스레드 스케줄러 |
| exécuterCommande valeurTemps valeurLimite | GIC-400 타이머로 무한 valeurItération programmeQuitter; interactif valeurEntrée 대기는 기한 actualiser, 터미널별 EL0 Programme 중단·exécutionReprendre | 일반적인 선점형 다중작업. 긴 valeurNoyau invoquer 도중에는 종료가 지연될 nombre 있음 |
| Fichier | Java RAM Fichier 64개 × 16384바이트, 루트를 포함한 디렉터리 16개, valeurPairRéseau/절대 chemin 63바이트, entréeÉlémentDescripteur 16개 | valeurPermission, 디스크/SD 영속 valeurStocker |
| 네트워크 | lwIP IPv4 TCP/UDP/ARP/ICMP, SLIP, GENET/PHY·DHCP réalisation, 게스트 FTP·SSH·VNC | GENET matérielPhysique valider, Wi-Fi, DNS, 일반 TLS valeurPriseRéseau, RDP |
| GUI | valeurMaximal 네 terminal fenêtre, valeurSélection·valeurDéplacer·X fermer, texteHangul valeurPolice, Swing 부분집합; 게스트 VNC Écran·valeurEntrée·두벌식 | matérielPhysique USB valeurEntrée, 전체 AWT/Swing·Java2D·fenêtre 관리 정책 |
| Tâche valeurFilExécution | valeurNoyau Tâche 2개와 주 Tâche; JVM 내부 valeurFilExécution valeurMaximal 4개, start/join/yield·synchronized | pthread, SMP, Java Thread 전체 API |
| 다국어 | UTF-16 리터럴→UTF-8 UART, texteHangul·일본어·아랍어·이모지, UTF-8 texteNomFichier/datagramme | GUI의 일반 다국어 조판 |

exécuterCommande 버튼 화면은 5×7 영문 글꼴을 쓰며, terminal 창은 Noto CJK/DejaVu에서 생성한 texteHangul·Unicode 비트맵 글꼴을 쓴다. UART와 donnéesEffectif 프레임버퍼의 texteHangul 표시를 시험한다. 루프백은 동일 valeurNoyau 내부의 datagramme 전달이며 IP 패킷을 Ethernet으로 내보내는 드라이버가 아니다. 바깥 IPv4는 lwIP TCP/UDP 스택으로 valeurAuxiliaire UART SLIP 경로를 사용한다. `python3 Outils/exécuterCommande.py --network`로 QEMU NAT를 연결하고 `ftpd start`로 서비스를 시작한다.

Java의 정확한 API·문법·exécuterCommande 제한과 français 사용법은 [interne JVM과 français bibliothèque](EnvironnementEnvironnementExécutionJava.md)에 정리했다. valeurClasse Fichier/JAR 배포는 [JavaFrançais](JavaFrançais) 소스에서 재현한다. 기존 Linux판 `français.Java`와 별도인 `français.interne` 패키지다.

**vi·여러 fenêtre·Swing·texteHangul Java/Python/C/C++·posix-kor 예제는 [texteHangul développement 매뉴얼](GuideDéveloppement.md)에 정리했다.**

GUI terminal exécuterCommande·단축키·interpréteurCommandes commande·제한은 [셸과 terminal 사용법](TerminalEtInterpréteurCommandes.md)에 정리했다.

## élémentListeActuel 컴퓨터에서 exécuterCommande

```sh
cd /home/user/jkoros/platforms/rpi4-native
make test
make run
```

programmeQuitter: **Ctrl+A élémentListeSuivant X**. 게스트 C/AOT Outils 빌드에는 `make rpi-prepare`로 준비한 ARM64 SDK 헤더와 libgcc valeurArithmétique valeurAuxiliaire 함수도 필요하다. libc나 Linux 커널을 게스트에 넣는 것은 아니다. Hôte 도구는 JDK 11 이상, Python 3.6 이상, Clang/Clang++, AArch64 GNU binutils, Make, `libnewlib-dev` 헤더다. MicroPython은 `/usr/include/newlib` 헤더를 사용하며 다른 위치는 `NEWLIB_INCLUDE`로 지정한다. newlib 런타임을 Portage·링크한 것은 아니다. Compilateur 의미 비교에는 GCC/UBSan도 사용한다. 기존 `../rpi4/build/host`의 QEMU 11.0.3이 있으면 이용하며, 그렇지 않으면 PATH의 QEMU를 사용한다. `QEMU_AARCH64=/절대/chemin/qemu-system-aarch64`로 지정할 수도 있다. `raspi4b` valeurPriseEnCharge 여부를 확인한 étatValeurAprès 실행한다.

명령은 **Enter를 눌러 exécuterCommande**한다. 기존 한 valeurCaractère 명령도 Enter가 필요하다.

```text
javac Hello.java
java Hello "texteHangul arguments 😀"
python hello.py
python -c 'print(2**100)'
ls
cat python.txt
run cpp
net test
gui
```

| commande | action |
|---|---|
| `help` / `info` | commande·donnéesEffectif réalisation valeurÉtatValeur |
| `ls` / `cat FILE` / `rm FILE` | RAM Fichier listeEntréeÉlément·valeurContenuValeur·삭제 |
| `vi FILE` | Utilisateur valeurRégion vi 부분집합, texteHangul valeurÉditer·valeurStocker·검색·되돌리기 |
| `edit FILE` | Fichier 전체를 새로 valeurEntrée; 단독 `.` 줄로 valeurStocker, Ctrl-C로 opérationAnnuler |
| `javac FILE.java` / `java CLASS [ARGS]` | interne 제한형 Java compilerSource·exécuterCommande |
| `python FILE.py [ARGS]` / `python -c 'CODE'` | MicroPython compilerSource·exécuterCommande |
| `load FILE` / `hex FILE` | 16진수 바이너리 valeurEntrée/Sortie; 입력은 단독 `.` 줄로 valeurStocker |
| `run FILE.elf [ARGS]` / `run cpp` | 업로드한 interne ABI ELF / 내장 C++ Exemples |
| `net test` / `tasks` / `selftest` | UDP 루프백 / 협력식 Tâche / EL0 protégerValeur Tests |
| `gui` / `terminal` | exécuterCommande Écran / texteHangul GUI terminal; F12로 terminal ouvrir·fermer |
| `samples` | 삭제한 valeurDéfaut Exemples récupérerÉtatValeur; 기존 파일은 보존 |

예를 들어 `edit Salutation.java`를 입력한 élémentListeSuivant valeurBasExtrémité 소스를 입력한다.

```java
public class Salutation { public static void main(String[] args) { int valeur = 7; System.out.println("texteHangul=" + valeur); } }
```

그다음 단독 `.` 줄로 저장하고 `javac Salutation.java`, `java Salutation`를 실행한다. 편집기는 기존 파일에 커서를 이동하는 방식이 아니라 전체 교체 방식이다. opérationAnnuler·잘못된 16진수·valeurCapacité 초과는 원본을 보존한다. 줄은 4096바이트, 파일은 16384바이트, exécuterCommande 인수는 valeurMaximal 8개·각각 UTF-8 255바이트다. 일반 commande 인수는 valeurMaximal 32개다. guillemet·백슬래시·interpréteurCommandes valeurVariable·파이프·리다이렉션 범위는 [interpréteurCommandes description](TerminalEtInterpréteurCommandes.md)을 참고한다.

GUI 터미널은 다음과 같이 실행하고 Remmina에서 **VNC**, adresse **127.0.0.1:5902**로 연결한다. 키보드·texteHangul Unicode valeurEntrée·명시적 valeurColler·exécuterCommande 버튼의 마우스 클릭을 QEMU 도구가 UART에 전달한다.

```sh
make desktop
# GUI + 네트워크: python3 Outils/exécuterCommande.py --desktop --network
# 다른 portMatériel: python3 Outils/exécuterCommande.py --desktop --port 5903
```

종료는 실행한 Hôte 터미널에서 Ctrl+C다. 기존 `python3 Outils/exécuterCommande.py --vnc 127.0.0.1:2`는 Écran 보기와 별도 UART 입력을 유지한다. `make run`은 일반 UART 셸이다. donnéesEffectif Pi4 USB 입력기는 아직 없으며, VNC connecter 도구는 QEMU 시험용이다.

GUI의 다섯 버튼은 donnéesEffectif C++/UDP ELF exécuterCommande, `Hello.java` compilerSource étatValeurAprès JVM exécuterCommande, `hello.py` exécuterCommande, GUI terminal 열기를 수행한다. 한 번에 한 프로그램이 CPU에서 실행되며 일반 실행에는 약 2초 기한이 있다. vi·Swing은 interactif 대기에서 기한을 갱신하고 다른 터미널로 전환할 때 donnéesMémoire·CPU 문맥을 보관한다. interpréteurCommandes·편집기에서 입력을 기다리는 시간에는 이 제한이 적용되지 않는다.

## donnéesEffectif 산출물과 Pi4 SD construireImage

```sh
make image   # valeurNoyau, SD construireImage, Amorçage ZIP, 사용자용 SDK
make sdk     # SDK만 valeurRéessayer générer
```

| chemin | 용도 |
|---|---|
| `build/kernel8.img` | interne valeurNoyau 기계어, 적재 adresse 0x80000 |
| `build/kernel.elf`, `kernel.map` | valeurNoyau valeurSymbole·DispositionLiens |
| `build/user/demo.elf` | Utilisateur valeurMode C++ Fichier/valeurTas/valeurPointFlottant/그래픽 Exemples |
| `build/user/network.elf` | Utilisateur valeurMode C++ UDP 루프백 Exemples |
| `build/user/java-tools.elf` | interne Java 부분집합 Compilateur/JVM, 전체 JDK/JRE 아님 |
| `dist/jkoros-native-korean.jar` | Hôte javac용 français API valeurClasse; 같은 클래스가 interne JVM에도 내장됨 |
| `dist/jkoros-native-korean-sources.zip` | français API Java source |
| `build/user/vi.elf` | interne UTF-8 vi commande 부분집합 Éditeur |
| `build/user/python.elf` | interne ABI용 MicroPython 1.24.1, CPython 아님 |
| `build/user/fault.elf` | 의도적 침범/무한 반복을 수행하는 protégerValeur Tests 전용 |
| `build/libposix-kor-arm64.a` | **valeurNoyau 내부**에서 Java Fichier 구현을 직접 부르는 기존 connecter |
| `build/libposix-kor-user.a` | **EL0 Utilisateur Programme**에서 SVC로 Fichier/루프백을 호출하는 새 connecter |
| `dist/jkoros-native-rpi4.img` | 128 MiB MBR/FAT32 SD construireImage |
| `dist/jkoros-native-rpi4-boot.zip` | FAT32 Amorçage 파티션에 복사할 Fichier valeurGroupe |
| `dist/jkoros-native-aarch64-sdk.tar.gz` | 사용자용 헤더·lancer valeurCode·bibliothèque·링커 valeurScript·Exemples |
| `dist/manifest.json`, `build/build.json` | SHA256과 donnéesEffectif valeurPriseEnCharge valeurÉtatValeur |

이미지는 확인된 공식 Pi Amorçage 묶음에서 `start4.elf`, `fixup4.dat`, Pi4 DTB와 disable-bt overlay를 가져온다. Linux kernel/initramfs/rootfs는 넣지 않는다. 펌웨어·MicroPython·terminal valeurPolice 라이선스와 valeurPolice valeurOrigine 해시도 동봉한다. Fichier générer 스크립트는 물리 디스크에 기록하지 않는다.

예비 microSD에 construireImage enregistrementJournal 도구로 `.img`를 기록하거나 FAT32 Amorçage 파티션 최상위에 ZIP 내용을 푼다. construireImage 기록은 선택한 카드의 기존 내용을 지우므로 대상을 확인한다. Pi4 valeurDéfaut EEPROM SD 부팅을 전제로 한다. UART는 **3.3V TTL, 115200 8N1**, GPIO14/TXD(8번)→어댑터 RX, GPIO15/RXD(10번)→TX, GND(6번) 연결이다. GPIO에 5V 신호를 연결하지 않는다.

**matérielPhysique Pi4 부팅은 미검증이다.** QEMU `-kernel`은 SD의 VideoCore 펌웨어를 실행하지 않고 커널을 직접 적재한다. SD Fichier 구성·valeurNoyau 체크섬 검사와 물리 CarteMatérielle Amorçage 검증은 별개다. MMU valeurUtiliser 전에는 펌웨어의 캐시/MMU가 꺼져 있고 EL1 또는 EL2로 진입하는 통상 Amorçage 조건을 전제로 한다. valeurTrois valeurAuxiliaire 코어는 대기시키며 한 코어만 사용한다.

## C++와 français API valeurUtiliser

SDK를 풀고 호스트에서 컴파일한다.

```sh
tar -xzf dist/jkoros-native-aarch64-sdk.tar.gz -C build
cd build/jkoros-native-sdk
python3 compile.py examples/ExempleFichier.cpp -o demo.elf
python3 compile.py examples/ExempleCommunication.cpp -o network.elf
```

진입점은 `extern "C" int démarrerProgrammeUtilisateur(int)`이다. Utilisateur C++는 FP/SIMD를 사용할 nombre 있다. valeurNoyau C/Java AOT는 일반 레지스터만 사용하므로 exception entréeÉlémentValeurProcessus 중 Utilisateur FP 상태를 건드리지 않는다. Utilisateur valeurPointEntréeÉlément 시 FP 상태를 초기화하고 valeurNoyau 복귀에 필요한 상태를 보존한다.

```cpp
#include "ABIFichier.h"
extern "C" int démarrerProgrammeUtilisateur(int) {
    int Fichier = ouvrirFichier("Salutation.txt", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600);
    if (Fichier < 0) return 1;
    const char valeurContenuValeur[] = "안녕하세요";
    int résultat = écrireDonnéesFichier(Fichier, valeurContenuValeur, sizeof(valeurContenuValeur) - 1);
    fermerFichier(Fichier);
    return résultat == sizeof(valeurContenuValeur) - 1 ? 0 : 2;
}
```

[Fichier Exemples](Utilisateur/ExempleFichier.cpp)와 [Communication Exemples](Utilisateur/ExempleCommunication.cpp)opérandePremier donnéesEffectif Amorçage Tests 대상이다. `ABIFichier.h`의 이름은 커널용/사용자용 construireTous 같지만 **링크하는 라이브러리가 다르다**. 사용자용은 `svc #0`으로 호출하고 Fichier entréeÉlémentValeurProcessus 및 루프백 전달은 Java 커널에서 실행한다. `ABIRéseau.h`의 valeurPriseRéseau 함수는 élémentListeActuel 사용자용 라이브러리에 구현돼 있다.

새 프로그램은 valeurNoyau 재빌드 없이 `load FILE.elf`와 `run FILE.elf`로 실행한다. 호스트에서 élémentListeSuivant 도구를 사용하면 **새 QEMU를 부팅해 업로드한 donnéesEffectif 바이트를 재확인한 valeurRetourArrièreCôté 게스트에서 exécuterCommande**하고 종료한다. 이 도구의 새 VM에서 만든 RAM 자료는 종료할 때 사라진다.

```sh
cd /home/user/jkoros/platforms/rpi4-native
python3 Outils/exécuterFichier.py build/jkoros-native-sdk/demo.elf
python3 Outils/exécuterFichier.py Exemples/Hello.java "texteHangul arguments"
python3 Outils/exécuterFichier.py Exemples/hello.py
```

이 경로는 16KiB 이하의 `.elf`, `.java`, `.class`, `.py`를 지원한다. 큰 내장 Java/MicroPython ELF 자체는 valeurNoyau 묶음에 포함되어 이 Fichier 한도를 적용받지 않는다. **C++ 컴파일러는 Hôte SDK의 Clang++**이며 게스트 내부 GCC/Clang 컴파일러는 아직 없다. SDK만으로 일반 Linux 프로그램을 실행할 수는 없다. Linux ELF, 동적 bibliothèque, PT_TLS, PT_INTERP, PT_DYNAMIC, exécuterCommande·écrire 겸용 세그먼트는 로더가 거부한다. 구체적인 invoquer numéro·adresse rogner·오류는 [Utilisateur ABI](ABIAppelUtilisateur.md)를 참고한다.

RAM 파일은 재부팅 시 사라진다. `stockageFichierConfirmer`은 -1과 ENOSYS를 반환한다. 파일의 mode 인수를 저장하지 않으며 valeurPermission·dup/fcntl은 없다. 디렉터리와 valeurPairRéseau/절대 경로는 같은 RAM 저장소에서 처리한다. UDP 전문은 valeurMaximal 512바이트, 소켓은 8개, recevoirValeur 큐는 소켓당 4개다. 수신할 자료가 없거나 큐가 가득 차면 EAGAIN을 반환한다. Utilisateur programmeQuitter 시 열린 Fichier 서술자와 소켓을 회수한다.

## valider résultat

`make test-jvm`은 9개 프로그램을 OpenJDK와 donnéesEffectif interne 커널에서 실행해 결과를 비교한다. `make test`에도 포함된다. 별도 `Outils/TestAmorçage.py`는 Java rectangle API의 donnéesEffectif Écran 픽셀까지 검사한다. `make test-shell`, `make test-desktop`은 새 셸과 donnéesEffectif VNC valeurEntrée·texteHangul terminal 화면을 검사하며 `make test`에도 포함된다.

`make test-windows`, `make test-swing`, `make test-stream`, `make test-coding`도 제공하며 `make test`에 포함된다.

`make test`는 OpenJDK와 AOT valeurOpération résultat 비교, 런타임 erreur 중단, estNonPrisEnCharge Java 거부와 함께 별도 QEMU VM에서 다음을 검사한다.

- 기존 Java valeurNoyau calculRésultat·UTF-8·C++ 직접 invoquer·협력식 Tâche 및 프레임버퍼.
- 손상/잘못된 ABI/adresse 초과/겹친 페이지/W+X 등 ELF rejeterValeur 사례 22개.
- EL0 C++ 생성자·RAII·valeurPointFlottant valeurOpération·Fichier·valeurTas 및 잘못된 시스템 invoquer pointeur.
- valeurNoyau/valeurCode/MMIO écrire·entréeÉlémentAccès, NX pileOpérande·NULL exécuterCommande, guard page, 특권 commande 차단.
- SVC를 호출하지 않는 무한 반복을 타이머로 종료한 étatValeurAprès estNormal Programme 재실행.
- valeurItération exécuterCommande 시 Fichier/valeurPriseRéseau 누수 방지, UDP 왕복·보낸 adresse·valeurRogné recevoirValeur·큐 포화·빈 datagramme·estNonPrisEnCharge Communication erreur.
- interpréteurCommandes valeurÉditer·opérationAnnuler·16진수 업로드/다운로드·Utilisateur ELF 실행과 잘못된 ELF rejeterValeur.
- 게스트 Java → OpenJDK `-Xverify:all`, OpenJDK → 게스트 JVM 교차 exécuterCommande, texteHangul valeurClasse·valeurVariable·texteNomFichier.
- 여러 fenêtre·vi valeurStocker·valeurÉditer·pontRetourner·Utilisateur valeurÉtatValeur 중단/exécutionReprendre, Swing texteHangul valeurEntrée·이벤트·X fermer, 연결형 루프백, C/C++ texteHangul SDK Exemples.
- MicroPython Unicode·큰 Entier·valeurClasse·GC valeurItération·Fichier import·exception·Fichier·UDP 왕복·valeurTemps 초과 étatValeurAprès 복귀.
- GUI valeurSélection valeurDéplacer, C++/UDP/Java/MicroPython 버튼 exécuterCommande, 콘솔 복귀 및 donnéesEffectif 프레임버퍼 픽셀/valeurPolice.
- 디렉터리·valeurVariable·condition·Fichier commande·valeurScript·순차 파이프·리다이렉션·valeurCapacité 초과 récupérerÉtatValeur, Python stdin/EOF와 Java/Python stdout.
- commande enregistrementJournal·긴 texteHangul valeurEntrée valeurÉditer·valeurAchevé·terminal 스크롤, 그래픽 Programme programmeQuitter étatValeurAprès fenêtre 복원, donnéesEffectif VNC Unicode valeurTouche·valeurColler·마우스.

[valeurNoyau Tests enregistrementJournal](build/verification/implementation-test.log), [interpréteurCommandes Tests](build/verification/shell/report.json), [VNC Tests](build/verification/desktop/report.json), [machine 판독 résultat](build/verification/report.json), [valeurSériel valeurJournal](build/verification/serial.log), [GUI Écran](build/verification/gui-python.png)을 확인할 nombre 있다. VNC RFB 3.8 connecter 및 640×480 Écran 정보도 검사한다. [SDK 재컴파일 résultat](build/verification/sdk.json)는 두 예제의 pointEntréeÉlément·적재 세그먼트·ABI note가 Amorçage 시험한 ELF와 일치함을 확인한다. valeurSymbole 등 비적재 메타데이터를 포함한 Fichier 전체의 SHA256까지 같다고 의미하지는 않는다.

## Java와 Python의 정확한 rogner

interne `javac`는 버전 49 `.class`를 생성하며 JVM은 valeurPriseEnCharge 명령으로 구성된 버전 45–52 클래스를 실행한다. valeurStatique Fonction·재귀·int/boolean/char/String·condition/valeurItération·Chaîne 결합과 일부 Fichier 스트림을 지원한다. UTF-8 문자열과 Caractères 리터럴, ASCII 및 현대 texteHangul 음절/Combinaison valeurLettreHangul 식별자를 처리한다. Unicode valeurIdentificateur 전체 Table·Unicode arbreSource 이스케이프는 구현하지 않았다. 게스트 arbreSource 컴파일러는 일반 valeurObjet·exception·Thread 구문을 아직 컴파일하지 못한다. Hôte `javac --release 8`로 만든 valeurPriseEnCharge 부분집합 클래스는 interne JVM 0.4의 valeurObjet·exception·Thread·UDP와 français API를 사용할 nombre 있다. Swing은 문서화한 interne API 부분집합을 제공하며 JAR 로더는 제공하지만 전체 AWT/Swing·JDK 표준 라이브러리는 없다. 정확한 범위는 [interne JVM description](EnvironnementEnvironnementExécutionJava.md)이 기준이다. 상세 Langue 범위는 [공유 Java Outils description](../../Documentation/EnvironnementDéveloppementJava.md)을 참고하되, 그 문서의 x86 interpréteurCommandes/valeurStocker/실행시간과 이 ARM64 판의 차이에 유의한다.

MicroPython은 공식 **1.24.1 arbreSource**를 interne AArch64 EL0/SVC 대상으로 빌드했다. Python 문법의 Fonction·valeurClasse·exception·리스트/Dictionnaire·Unicode·GC·가변 valeurPrécision 정수를 제공한다. élémentListeActuel 구성은 Entier 빌드로 `float`, `complex`, `math`opérandePremier 없으며 CPython 전체 표준 bibliothèque, pip, subprocess, threading, 일반 socket과 valeurDéfaut `open()` Fichier 객체는 제공하지 않는다. `python FILE.py` 및 `-c` 실행만 제공하며 REPL은 아직 없다. 각 실행의 valeurObjet·모듈은 programmeQuitter 시 회수되고 RAM 파일만 élémentListeSuivant 실행에 남는다.

`import jkoros`로 élémentListeSuivant 시스템 연결을 쓴다. construireTous SVC를 통해 interne Java 커널에 접근한다.

| Fonction | action |
|---|---|
| `stdin(limit)` | élémentListeActuel 표준 입력에서 valeurMaximal limit바이트(0…16384)를 bytes로 lireRésultat; EOF는 빈 bytes, UART Données 없음은 OSError(11) |
| `read(name)` | valeurPairRéseau/절대 RAM 경로의 Fichier 전체를 bytes로 lireRésultat |
| `write(name, data)` | str/bytes 버퍼를 RAM 파일에 새로 valeurStocker, 쓴 valeurOctet nombre résultatRetourner |
| `remove(name)` | RAM Fichier 삭제 |
| `rect(x, y, w, h, color)` | 선택한 donnéesEffectif Écran taille 안의 rectangle Dessin; 기존 보드의 RGB32 valeur |
| `ticks_ms()` | Amorçage étatValeurAprès millisecondes, 32비트 valeurCycle |
| `udp_open(port)` | 127.0.0.1의 UDP valeurPriseRéseau ouvrir/EmballerExécutables; 0은 자동 portMatériel |
| `udp_send(fd, port, data)` | 루프백 valeurDestination 포트에 str/bytes 버퍼 valeurTransfert |
| `udp_recv(fd)` | `(bytes, 보낸포트)` résultatRetourner; 비어 있으면 `OSError(11)` |
| `udp_close(fd)` | valeurPriseRéseau fermer |

```python
import jkoros
first = jkoros.udp_open(9401)
second = jkoros.udp_open(9402)
jkoros.udp_send(first, 9402, b"hello")
print(jkoros.udp_recv(second))  # (b'hello', 9401)
jkoros.udp_close(first)
jkoros.udp_close(second)
```

Portage valeurCode: [python/](pontPython/), [Utilisateur Java connecter](Utilisateur/pontJava.c). 공식 [MicroPython Portage Guide](https://docs.micropython.org/en/latest/develop/porting.html)를 참고했다. arbreSource URL·fichierHachage·라이선스는 [vendor Guide](vendor/README.md)에 기록했다.

## 남은 Tâche

| élémentListeSuivant valeurÉtapePhase | estTerminé racineProjet |
|---|---|
| 영속 valeurStocker·exécuterCommande Fichier valeurEntrée | SD/MMC 및 디스크 Fichier 시스템, 시스템/Utilisateur 볼륨; élémentListeActuel ELF Fichier 실행은 RAM에 한정 |
| 일반 프로세스·스레드 | 프로세스별 adresse régionAdresse, 선점 스케줄러, TLS, synchroniser/attendreValeur, 신호, mmap/mprotect |
| libc와 C++ 런타임 | interne ABI용 libc, malloc/free, 표준 sortieEntrée·Horloge·environnement·locale, libstdc++/exception entréeÉlémentValeurProcessus valider |
| CPython | 해당 libc와 OS API 대상으로 Portage·교차 빌드하고 Fichier/Unicode/스레드/valeurPriseRéseau Tests |
| OpenJDK/JRE | HotSpot OS valeurCouche, GC/JIT/스레드/신호/동적 연결과 Java 네이티브 bibliothèque Portage; javac/java donnéesEffectif exécuterCommande |
| valeurExtérieur 네트워크 | 추가한 GENET/PHY·DHCP 드라이버의 donnéesEffectif CarteMatérielle 송수신 valider, DNS·Wi-Fi |
| GUI valeurExtension | USB HID, 게스트 입력기·Caractères 조판, Swing fenêtre taille 조절·클리핑 valeurExtension, 전체 AWT/Swing Portage |

이 표는 남은 작업이며 réalisation estTerminé 목록이 아니다. QEMU Pi4 모델에는 GENET Ethernet과 PCIe root port가 없어 valeurExtérieur 네트워크 드라이버는 matérielPhysique 검증도 필요하다. [QEMU Périphérique 지원표](https://www.qemu.org/docs/master/system/arm/raspi.html)

valeurMatériel 및 ABI 참고: [BCM2711 périphériqueMatériel](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf), [Pi4 GIC adresse](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/broadcom/bcm2711.dtsi), [mailbox valeurContrat](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), [Arm ELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst), [Arm FP valeurContrôle 레지스터 valeurDéfinition](https://github.com/ARM-software/arm-trusted-firmware/blob/master/include/arch/aarch64/arch.h).


## français C typeDonnées·Python erreur·Paquet installerValeur

C 네트워크 API는 `struct AdressePriseRéseauInternet`, enum 상수와 donnéesEffectif français 함수로
구현한다. valeurMacro 별칭을 사용하지 않으며 élémentListePrécédentÉlément pk_* ABI도 유지한다.
Python 예제는 `ErreurSystème`, `erreur.numéro`, `erreur.description`을 사용한다.

`python3 Outils/exécuterCommande.py --desktop --network --pip`로 시작하면 게스트에서
`pip install micropython-bisect==3.3.3`을 사용할 nombre 있다. 현재는 Hôte 중계를
이용하는 제한형 MicroPython arbreSource 설치기이며 CPython pip·자동 dépendances 해결·C 확장은
미지원이다. 설치한 `/lib` 자료는 RAM이다. [사용법과 valeurLimite](LotPython.md).

## Écran taille valeurSélection

`python3 Outils/exécuterCommande.py --desktop --network --resolution 1920x1080`으로 Full HD 화면을 사용한다. 기본값은 640×480이며 1280×720도 가능하다. terminal valeurDéplacer, Swing milieu DispositionLiens, Java·C·Python 그리기도 donnéesEffectif 크기를 따른다. SD 영상은 `make image RESOLUTION=1920x1080`으로 만든다. [réglages·français API·valider Guide](résolutionÉcran.md).

## français 직접 API와 Écran actualiser

`example/java`는 `TâcheTâcheExécutable`, `RécepteurAction`, `NotificationAction`, `bouton`, `FileAttenteÉvènement`,
`tâcheFond`, `lancer()`을 사용할 nombre 있다. français GUI/가닥을 interne JVM에 직접
연결했으며, 표준 Swing/Thread를 감싸지 않는다. Chaîne 등 javac의 표준
계약과 전체 arbreSource 검토 범위는 [nommage Guide](nommage/Guide.md), 사용법과 호환성 변경은
[français Java API](JavaFrançais/Guide.md)를 본다.

terminal valeurDéplacer·taille 변경은 바뀐 영역만 합성하고 달라진 화소만 표시한다.
[Écran actualiser description](EnvironnementEnvironnementExécutionJava.md#terminal-valeurSousPartie-actualiser),
[valeurSousPartie actualiser Contrôles](build/verification/redraw/report.json)를 참고한다.
